import structlog

from ...db.models import Document, EntityName, ProcessingStatus
from ...models import Document as DocumentModel
from .repository import EntityNotFoundError, Repository

log = structlog.get_logger(__name__)


class DocumentRepository(Repository):
    def create(self, pages_count: int, file_name: str) -> int:
        """Create record of uploaded file.

        Args:
            pages_count: Number of pages in document.
            file_name: Name of the uploaded file.

        Returns:
            Id of db object.

        """
        document = Document(
            processing_status=ProcessingStatus.NEW.value,
            pages_count=pages_count,
            file_path=file_name,
        )
        with self._open_session() as session:
            session.add(document)
            session.commit()
            session.refresh(document)
        return document.id

    def get_by_id(self, document_id: int) -> DocumentModel:
        """Get document record from db.

        Args:
            document_id: Document identifier.

        Raises:
            EntityNotFoundError: Document with requested id does not exist.

        Returns:
            Document object.

        """
        with self._open_session() as session:
            document = (
                session.query(Document).filter(Document.id == document_id).first()
            )
            if document is None:
                log.error("get_by_id.not_found", document_id=document_id)
                raise EntityNotFoundError(str(document_id), EntityName.DOCUMENT)
            return DocumentModel.from_orm(document)
