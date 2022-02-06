from ...db.models import Document, EntityName
from ...models import Document as DocumentModel
from .repository import EntityNotFoundError, Repository


class DocumentRepository(Repository):
    def get_by_id(self, document_id: int) -> DocumentModel:
        with self._open_session() as session:
            document = (
                session.query(Document).filter(Document.id == document_id).first()
            )
            if document is None:
                raise EntityNotFoundError(document_id, EntityName.DOCUMENT)
            return DocumentModel.from_orm(document)
