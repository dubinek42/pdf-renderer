import json

from flask import Response
from werkzeug.exceptions import RequestEntityTooLarge

from ...db.repositories.repository import EntityNotFoundError
from ...db.sessions import SessionNotOpenError
from ...services.errors import PdfInvalidError, ProcessingNotFinishedError


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


def handle_pdf_invalid(error: PdfInvalidError) -> Response:
    return Response(
        json.dumps({"code": 400, "message": "Invalid format of document."}),
        status=400,
        mimetype="application/json",
    )


def handle_processing_not_finished(error: ProcessingNotFinishedError) -> Response:
    return Response(
        json.dumps(
            {
                "code": 409,
                "message": f"Document with id {error.document_id} "
                "is not yet fully processed.",
            }
        ),
        status=409,
        mimetype="application/json",
    )


def handle_request_entity_too_large(error: RequestEntityTooLarge):
    return Response(
        json.dumps(
            {"code": 413, "message": "The document is too large to be uploaded."}
        ),
        status=413,
        mimetype="application/json",
    )


def handle_session_not_open(error: SessionNotOpenError) -> Response:
    return Response(
        json.dumps({"code": 500, "message": "Failed to connect to database."}),
        status=500,
        mimetype="application/json",
    )


blueprint = {
    EntityNotFoundError: handle_entity_not_found,
    PdfInvalidError: handle_pdf_invalid,
    ProcessingNotFinishedError: handle_processing_not_finished,
    RequestEntityTooLarge: handle_request_entity_too_large,
    SessionNotOpenError: handle_session_not_open,
}
