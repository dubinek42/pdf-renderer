from ...db.models import EntityName, ProcessedImage
from ...models import ProcessedImage as ProcessedImageModel
from .repository import EntityNotFoundError, Repository


class ProcessedImageRepository(Repository):
    def get_by_pk(self, document_id: int, page_number: int) -> ProcessedImageModel:
        with self._open_session() as session:
            image = (
                session.query(ProcessedImage)
                .filter(
                    ProcessedImage.document_id == document_id,
                    ProcessedImage.page_number == page_number,
                )
                .first()
            )
            if image is None:
                raise EntityNotFoundError(
                    f"document_id {document_id}, page {page_number}",
                    EntityName.PROCESSED_IMAGE,
                )
            return ProcessedImageModel.from_orm(image)

    def get_by_document_id(self, document_id: int) -> list[ProcessedImageModel]:
        with self._open_session() as session:
            images = (
                session.query(ProcessedImage)
                .filter(ProcessedImage.document_id == document_id)
                .all()
            )
            if len(images) < 1:
                raise EntityNotFoundError(str(document_id), EntityName.PROCESSED_IMAGE)
            return [ProcessedImageModel.from_orm(image) for image in images]
