import pytest
from src.db.repositories.repository import EntityNotFoundError
from src.models import ProcessedImage


def test_get_by_pk_not_found(processed_image_repository):
    with pytest.raises(EntityNotFoundError):
        processed_image_repository.get_by_pk(1, 1)


def test_get_by_pk(
    document_factory, processed_image_factory, processed_image_repository
):
    _ = document_factory()
    image = processed_image_factory()
    result = processed_image_repository.get_by_pk(image.document_id, image.page_number)

    assert result == ProcessedImage.from_orm(image)


def test_get_by_document_not_found(processed_image_repository):
    with pytest.raises(EntityNotFoundError):
        processed_image_repository.get_by_document_id(1)


def test_get_by_document(
    document_factory, processed_image_factory, processed_image_repository
):
    _ = document_factory()
    image = processed_image_factory()
    result = processed_image_repository.get_by_document_id(image.document_id)

    assert len(result) == 1
    assert result[0] == ProcessedImage.from_orm(image)
