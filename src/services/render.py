import io
import os

import structlog
from dependency_injector.wiring import Provide, inject
from pdf2image import convert_from_path
from PIL import Image
from PIL.PpmImagePlugin import PpmImageFile
from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError

from ..constants import MAX_IMAGE_SIZE
from ..container import Container
from ..db import repositories
from ..db.models import ProcessingStatus
from ..models import Document
from . import errors

log = structlog.get_logger(__name__)


class RenderService:
    @inject
    def __init__(
        self,
        path_documents: str = Provide[Container.config.provided.path_documents],
        path_images: str = Provide[Container.config.provided.path_images],
    ) -> None:
        self.path_documents = path_documents
        self.path_images = path_images

    @staticmethod
    def check_document(data: bytes) -> int:
        """Check if document is a valid PDF.

        Args:
            data: Binary data of document.

        Raises:
            PdfInvalidError: File is not valid.

        Returns:
            Number of pages in document.

        """
        try:
            bytes_stream = io.BytesIO(data)
            pdf = PdfFileReader(bytes_stream)
            return pdf.getNumPages()
        except PdfReadError as exc:
            log.exception("pdf_read.error", exc=exc)
            raise errors.PdfInvalidError

    @inject
    def render_document(
        self,
        document_id: int,
        document_repository: repositories.Document = Provide[
            Container.document_repository
        ],
        processed_image_repository=None,
    ) -> None:
        log.info("render_document.started")

        document = document_repository.get_by_id(document_id)
        if document.processing_status != ProcessingStatus.NEW:
            log.error("render_document.not_new", document_id=document_id)
            return

        self._convert_pages(document, processed_image_repository)

        document.processing_status = ProcessingStatus.FINISHED
        document_repository.update(document)

        log.info("render_document.success")

    @inject
    def _convert_pages(
        self,
        document: Document,
        processed_image_repository: repositories.ProcessedImage = Provide[
            Container.processed_image_repository
        ],
    ):
        document_path = os.path.join(self.path_documents, document.file_path)
        images = convert_from_path(document_path)
        for page_number, image in enumerate(images):
            page_number += 1  # Don't want indexing from 0
            self._normalize_image_size(image)
            file_path = f"document{document.id}_page{page_number}.png"
            full_path = os.path.join(self.path_images, file_path)
            image.save(full_path, "PNG")
            processed_image_repository.create(document.id, page_number, file_path)

    @staticmethod
    def _normalize_image_size(image: PpmImageFile) -> None:
        """Scale image to fit max size without changing aspect ratio."""
        image.thumbnail(MAX_IMAGE_SIZE, Image.ANTIALIAS)
