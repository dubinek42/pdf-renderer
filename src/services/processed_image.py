import os

import structlog
from requests_toolbelt import MultipartEncoder

from ..db import repositories
from ..db.models import ProcessedImage, ProcessingStatus
from ..services.errors import ProcessingNotFinishedError

log = structlog.get_logger(__name__)


class ProcessedImageService:
    """Service for handling all business logic with processed images.

    Attributes:
        base_path: Full path to folder where images are stored.
        document_repository: Repository for handling db operations
        processed_image_repository: Repository for handling db operations.

    Raises:
        ProcessingNotFinishedError: Processing of document into image is not done.

    """

    def __init__(
        self,
        base_path: str,
        document_repository: repositories.Document,
        processed_image_repository: repositories.ProcessedImage,
    ) -> None:
        self.base_path = base_path
        self.document_repository = document_repository
        self.processed_image_repository = processed_image_repository

    def get_all_by_document_id(self, document_id: int) -> list[ProcessedImage]:
        images = self._get_images_from_repository(document_id)
        self._check_all_files(images)
        return images

    def get_one_page(self, document_id: int, page: int) -> ProcessedImage:
        self._check_processing_status(document_id)
        log.debug("get_one_page.processing_status.ok")
        return self.processed_image_repository.get_by_pk(document_id, page)

    def compose_multipart_response(
        self, images: list[ProcessedImage]
    ) -> MultipartEncoder:
        fields = {
            f"field{id}": (
                f"document{image.document_id}_page{image.page_number}.png",
                open(os.path.join(self.base_path, image.file_path), "rb"),
                "image/png",
            )
            for id, image in enumerate(images)
        }
        return MultipartEncoder(fields=fields)

    def _get_images_from_repository(self, document_id) -> list[ProcessedImage]:
        self._check_processing_status(document_id)
        return self.processed_image_repository.get_by_document_id(document_id)

    def _check_processing_status(self, document_id: int) -> None:
        document = self.document_repository.get_by_id(document_id)
        if document.processing_status != ProcessingStatus.FINISHED:
            log.error("check_processing_status.not_finished")
            raise ProcessingNotFinishedError(document_id)

    def _check_all_files(self, images: list[ProcessedImage]) -> None:
        for image in images:
            self._check_file(image.file_path)

    def _check_file(self, filename: str) -> None:
        full_path = os.path.join(self.base_path, filename)
        try:
            with open(full_path, "rb") as _:
                log.debug("check_file.ok", filename=filename)
        except Exception as exc:
            log.exception("check_file.failed", exc=exc)
            raise
