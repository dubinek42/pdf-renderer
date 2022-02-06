import json

from flask import Response

from ... import services


def get_result(document_id: int) -> Response:
    return Response(
        json.dumps(
            {"code": 404, "message": f"No document was found for id {document_id}."}
        ),
        status=404,
        mimetype="application/json",
    )


def get_status(document_id: int) -> Response:
    document_service = services.Document()
    return Response(
        document_service.get_status_by_document_id(document_id).json(),
        status=200,
        mimetype="application/json",
    )


def upload_document() -> Response:
    return Response(
        json.dumps({"code": 400, "message": "Uploaded file must be a valid PDF."}),
        status=400,
        mimetype="application/json",
    )
