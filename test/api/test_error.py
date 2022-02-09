from src.db.sessions import SessionNotOpenError
from werkzeug.exceptions import RequestEntityTooLarge


def test_entity_too_large(client, mocker):
    mocked = mocker.patch(
        "src.services.document.DocumentService.get_status_by_document_id",
        side_effect=RequestEntityTooLarge,
    )
    response = client.get("/status/1")

    assert mocked.called
    assert response.status_code == 413


def test_session_not_open(client, mocker):
    mocked = mocker.patch(
        "src.db.sessions.SessionFactory.open_session", side_effect=SessionNotOpenError
    )
    response = client.get("/status/1")

    assert mocked.called
    assert response.status_code == 500
