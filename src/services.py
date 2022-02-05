import structlog
from dependency_injector.wiring import Provide, inject

from .container import Container
from .db.repositories.document import DocumentRepository

log = structlog.get_logger(__name__)


class DocumentService:
    @inject
    def get_status_by_document_id(
        self,
        document_id: int,
        document_repository: DocumentRepository = Provide[
            Container.document_repository
        ],
    ) -> str:
        document = document_repository.get_by_id(document_id)
        log.info("document_service.get_status", document=document.dict())
        return document.processing_status
