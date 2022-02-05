from ...db.models import Document
from ...models import Document as DocumentModel
from .repository import Repository


class DocumentRepository(Repository):
    def get_by_id(self, document_id: int) -> DocumentModel:
        with self._open_session() as session:
            document = (
                session.query(Document).filter(Document.id == document_id).first()
            )
            return DocumentModel.from_orm(document)
