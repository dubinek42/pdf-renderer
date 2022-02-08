import os
import uuid

import structlog
from dependency_injector.wiring import Provide, inject

from ..api.responses.processing import ProcessingStatus
from ..container import Container
from ..db import repositories
from .render import RenderService

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
        pages_count = RenderService.check_document(document)
        file_path = self._generate_file_name()

        self._save_file(document, file_path)
        new_id = document_repository.create(pages_count, file_path)

        return new_id

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
