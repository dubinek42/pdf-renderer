import os
import uuid

import structlog

from ..api.responses.processing import ProcessingStatus
from ..db import repositories
from .render import RenderService

log = structlog.get_logger(__name__)


class DocumentService:
    def __init__(
        self, base_path: str, document_repository: repositories.Document
    ) -> None:
        self.base_path = base_path
        self.document_repository = document_repository

    def get_status_by_document_id(self, document_id: int) -> ProcessingStatus:
        document = self.document_repository.get_by_id(document_id)
        return ProcessingStatus(
            id=document.id,
            pages=document.pages_count,
            status=document.processing_status,
        )

    def create_document(self, document: bytes) -> int:
        """Save uploaded file and create db record from it.

        Check if document is valid. Then count pages, save file
        to storage and save info to db.

        Args:
            document: Binary data of uploaded file.
            document_repository: Repository for handling documents in db.

        Returns:
            Id of the new db record.

        """
        pages_count = RenderService.check_document(document)
        file_path = self._generate_file_name()

        self._save_file(document, file_path)
        new_id = self.document_repository.create(pages_count, file_path)

        return new_id

    @staticmethod
    def _generate_file_name() -> str:
        """Generate random name for pdf file."""
        return str(uuid.uuid4()) + ".pdf"

    def _save_file(self, data: bytes, filename: str) -> None:
        """Save the file to storage."""
        with open(os.path.join(self.base_path, filename), "wb") as file:
            file.write(data)
