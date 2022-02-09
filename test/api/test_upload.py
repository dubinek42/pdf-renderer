from dramatiq.errors import ConnectionError
from src.container import Container


def test_upload_wrong_format(client):
    response = client.post("/upload")
    assert response.status_code == 400


def test_upload_ok(client, mocker, document_service):
    container = Container()
    mocker.patch("src.services.render.RenderService.check_document", return_value=1)
    mocker.patch("src.services.document.DocumentService._save_file")
    mocker.patch("src.messaging.tasks.render_document.send")

    with container.document_service.override(document_service):
        response = client.post("/upload")

    assert response.status_code == 201


def test_upload_broker_dead(client, mocker, document_service):
    container = Container()
    mocker.patch("src.services.render.RenderService.check_document", return_value=1)
    mocker.patch("src.services.document.DocumentService._save_file")
    mocked = mocker.patch(
        "src.messaging.tasks.render_document.send",
        side_effect=ConnectionError(message=""),
    )

    with container.document_service.override(document_service):
        response = client.post("/upload")

    assert mocked.called
    assert response.status_code == 201
