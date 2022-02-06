import structlog
from dependency_injector.wiring import Provide, inject

from ..api.responses.processing import ProcessingStatus
from ..container import Container
from ..db.repositories.document import DocumentRepository

log = structlog.get_logger(__name__)


class DocumentService:
    @inject
    def get_status_by_document_id(
        self,
        document_id: int,
        document_repository: DocumentRepository = Provide[
            Container.document_repository
        ],
    ) -> ProcessingStatus:
        document = document_repository.get_by_id(document_id)
        return ProcessingStatus(
            id=document.id,
            pages=document.pages_count,
            status=document.processing_status,
        )
