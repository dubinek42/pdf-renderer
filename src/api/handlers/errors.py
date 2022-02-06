import json

from flask import Response
from src.db.sessions import SessionNotOpenError

from ...db.repositories.repository import EntityNotFoundError


def handle_session_not_open(error: SessionNotOpenError):
    return Response(
        json.dumps({"code": 500, "message": "Failed to connect to database."}),
        status=500,
        mimetype="application/json",
    )


def handle_entity_not_found(error: EntityNotFoundError):
    return Response(
        json.dumps(
            {
                "code": 404,
                "message": f"No {error.entity_name.value} was found "
                f"with id {error.entity_id}.",
            }
        ),
        status=404,
        mimetype="application/json",
    )


blueprint = {
    SessionNotOpenError: handle_session_not_open,
    EntityNotFoundError: handle_entity_not_found,
}
