import pytest
from src.db.models import ProcessingStatus
from src.db.repositories.repository import EntityNotFoundError
from src.models import Document


def test_not_found(document_repository):
    with pytest.raises(EntityNotFoundError):
        _ = document_repository.get_by_id(1)


def test_get_by_id(document_repository, document_factory):
    document = document_factory()
    result = document_repository.get_by_id(document.id)
    assert result is not None
    assert result.id == document.id
    assert result.processing_status == document.processing_status
    assert result.file_path == document.file_path


@pytest.mark.parametrize(
    "pages_count, file_name",
    [(1, "asdf.pdf"), (80, "qwert.pdf"), ("1", "test.pdf")],
)
def test_create(document_repository, pages_count, file_name):
    new_id = document_repository.create(pages_count=pages_count, file_name=file_name)
    document = document_repository.get_by_id(new_id)

    assert isinstance(document, Document)
    assert new_id == document.id
    assert int(pages_count) == document.pages_count
    assert ProcessingStatus.NEW == document.processing_status
    assert file_name == document.file_path


def test_update(document_repository):
    document_id = document_repository.create(1, "qwerttyuuiiuytre")
    old_document = document_repository.get_by_id(document_id)

    old_document.processing_status = ProcessingStatus.FINISHED
    document_repository.update(old_document)
    updated_document = document_repository.get_by_id(document_id)

    assert ProcessingStatus.FINISHED == updated_document.processing_status
