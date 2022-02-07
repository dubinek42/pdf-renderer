import io
import os
import uuid

import structlog
from dependency_injector.wiring import Provide, inject
from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError

from ..api.responses.processing import ProcessingStatus
from ..container import Container
from ..db import repositories
from . import errors

log = structlog.get_logger(__name__)


class DocumentService:
    @inject
    def get_status_by_document_id(
        self,
        document_id: int,
        document_repository: repositories.Document = Provide[
            Container.document_repository
        ],
    ) -> ProcessingStatus:
        document = document_repository.get_by_id(document_id)
        return ProcessingStatus(
            id=document.id,
            pages=document.pages_count,
            status=document.processing_status,
        )

    @inject
    def create_document(
        self,
        document: bytes,
        document_repository: repositories.Document = Provide[
            Container.document_repository
        ],
    ) -> int:
        """Save uploaded file and create db record from it.

        Check if document is valid. Then count pages, save file
        to storage and save info to db.

        Args:
            document: Binary data of uploaded file.
            document_repository: Repository for handling documents in db.

        Returns:
            Id of the new db record.

        """
        pages_count = self._check_document(document)
        file_path = self._generate_file_name()

        self._save_file(document, file_path)
        new_id = document_repository.create(pages_count, file_path)

        return new_id

    def _check_document(self, data: bytes) -> int:
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

    @staticmethod
    def _generate_file_name() -> str:
        """Generate random name for pdf file."""
        return str(uuid.uuid4()) + ".pdf"

    @inject
    def _save_file(
        self,
        data: bytes,
        filename: str,
        base_path: str = Provide[Container.config.provided.path_documents],
    ) -> None:
        """Save the file to storage."""
        with open(os.path.join(base_path, filename), "wb") as file:
            file.write(data)
