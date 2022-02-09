from src.api.responses.processing import ProcessingStatus
from src.container import Container
from src.db.repositories.repository import EntityNotFoundError


def test_get_status_ok(client, mocker):
    def mock_get_status(*args):
        return ProcessingStatus(id=1, pages=1, status="new")

    mocker.patch(
        "src.services.document.DocumentService.get_status_by_document_id",
        mock_get_status,
    )

    response = client.get("/status/1")

    assert response.status_code == 200
    assert response.json == {"id": 1, "pages": 1, "status": "new"}


def test_get_status_not_found(client, mocker):
    def mock_get_status(document_id, *args):
        raise EntityNotFoundError(document_id, "Document")

    mocker.patch(
        "src.services.document.DocumentService.get_status_by_document_id",
        mock_get_status,
    )

    response = client.get("/status/1")

    assert response.status_code == 404
    assert response.json.get("code") == 404
    assert "message" in response.json


def test_status_injected(client, document_service, document_factory):
    container = Container()
    document = document_factory()
    with container.document_service.override(document_service):
        response = client.get(f"/status/{document.id}")

    assert response.status_code == 200
