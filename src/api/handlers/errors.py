import json

from flask import Response

from ...db.repositories.repository import EntityNotFoundError
from ...db.sessions import SessionNotOpenError
from ...services.errors import CannotOpenFileError, ProcessingNotFinishedError


def handle_cannot_open_file(error: CannotOpenFileError):
    return Response(
        json.dumps(
            {
                "code": 404,
                "message": "Requested file cannot be opened.",
            },
            status=404,
            mimetype="application/json",
        )
    )


def handle_entity_not_found(error: EntityNotFoundError) -> Response:
    return Response(
        json.dumps(
            {
                "code": 404,
                "message": f"No {error.entity_name} was found "
                f"with id {error.entity_id}.",
            }
        ),
        status=404,
        mimetype="application/json",
    )


def handle_processing_not_finished(error: ProcessingNotFinishedError) -> Response:
    return Response(
        json.dumps(
            {
                "code": 102,
                "message": f"Document with id {error.document_id} "
                "is not yet fully processed.",
            }
        ),
        status=102,
        mimetype="application/json",
    )


def handle_session_not_open(error: SessionNotOpenError) -> Response:
    return Response(
        json.dumps({"code": 500, "message": "Failed to connect to database."}),
        status=500,
        mimetype="application/json",
    )


blueprint = {
    CannotOpenFileError: handle_cannot_open_file,
    EntityNotFoundError: handle_entity_not_found,
    ProcessingNotFinishedError: handle_processing_not_finished,
    SessionNotOpenError: handle_session_not_open,
}
