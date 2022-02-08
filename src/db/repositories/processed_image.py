import structlog

from ...db.models import EntityName, ProcessedImage
from ...models import ProcessedImage as ProcessedImageModel
from .repository import EntityNotFoundError, Repository

log = structlog.get_logger(__name__)


class ProcessedImageRepository(Repository):
    def get_by_pk(self, document_id: int, page_number: int) -> ProcessedImageModel:
        """Get processed image by primary key.

        Primary key is the combination of document_id and page_number.

        Args:
            document_id: Document identifier.
            page_number: Page number.

        Raises:
            EntityNotFoundError: Requested image was not found.

        Returns:
            Object of processed image.

        """
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
                log.error(
                    "get_by_pk.not_found",
                    document_id=document_id,
                    page_number=page_number,
                )
                raise EntityNotFoundError(
                    f"document_id {document_id}, page {page_number}",
                    EntityName.PROCESSED_IMAGE,
                )
            return ProcessedImageModel.from_orm(image)

    def get_by_document_id(self, document_id: int) -> list[ProcessedImageModel]:
        """Get all processed images for document id.

        Args:
            document_id: Document identifier.

        Raises:
            EntityNotFoundError: No image was found for the document.

        Returns:
            All found processed images.

        """
        with self._open_session() as session:
            images = (
                session.query(ProcessedImage)
                .filter(ProcessedImage.document_id == document_id)
                .all()
            )
            if len(images) < 1:
                log.error("get_by_document_id.not_found", document_id=document_id)
                raise EntityNotFoundError(str(document_id), EntityName.PROCESSED_IMAGE)
            return [ProcessedImageModel.from_orm(image) for image in images]
