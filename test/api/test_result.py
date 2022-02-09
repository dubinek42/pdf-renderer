import pytest
from src.container import Container  # pylint: disable=import-error
from src.db.models import ProcessingStatus  # pylint: disable=import-error


@pytest.mark.parametrize("endpoint", ["/result/1", "/result/1/1"])
def test_result_not_found(client, processed_image_service, endpoint):
    container = Container()
    with container.processed_image_service.override(processed_image_service):
        response = client.get(endpoint)

    assert response.status_code == 404


@pytest.mark.parametrize("page", ["", "/1"])
def test_result_not_finished(client, document_factory, processed_image_service, page):
    document = document_factory()
    container = Container()
    with container.processed_image_service.override(processed_image_service):
        response = client.get(f"/result/{document.id}{page}")

    assert response.status_code == 409


def test_result_full(
    client,
    mocker,
    document_repository,
    processed_image_repository,
    processed_image_service,
):
    document_id = document_repository.create(1, "test")
    document = document_repository.get_by_id(document_id)
    document.processing_status = ProcessingStatus.FINISHED
    document_repository.update(document)
    processed_image_repository.create(1, 1, "test")

    container = Container()
    mocker.patch("src.services.processed_image.ProcessedImageService._check_file")
    mocker.patch(
        "src.services.processed_image.ProcessedImageService.get_all_by_document_id",
        return_value=[],
    )

    with container.processed_image_service.override(processed_image_service):
        response = client.get(f"/result/{document_id}")

    assert response.status_code == 200
    assert response.content_type.startswith("multipart/form-data")


def test_result_one_page(
    client,
    mocker,
    document_repository,
    processed_image_repository,
    processed_image_service,
):
    document_id = document_repository.create(1, "test")
    document = document_repository.get_by_id(document_id)
    document.processing_status = ProcessingStatus.FINISHED
    document_repository.update(document)
    processed_image_repository.create(1, 1, "test")

    container = Container()
    mocker.patch("src.services.processed_image.ProcessedImageService._check_file")
    mocker.patch("werkzeug.utils.send_from_directory", return_value={"ok": "ok"})
    with container.processed_image_service.override(processed_image_service):
        response = client.get(f"/result/{document.id}/1")

    assert response.status_code == 200
    assert response.json == {"ok": "ok"}
