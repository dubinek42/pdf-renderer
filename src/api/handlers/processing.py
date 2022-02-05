import json

from flask import Response


def get_result(file_id: int) -> Response:
    return Response(
        json.dumps({"code": 404, "message": f"No file was found for id {file_id}."}),
        status=404,
        mimetype="application/json",
    )


def get_status(file_id: int) -> Response:
    return Response(
        json.dumps({"code": 404, "message": f"File with id {file_id} was not found."}),
        status=404,
        mimetype="application/json",
    )


def upload_file() -> Response:
    return Response(
        json.dumps({"code": 400, "message": "Uploaded file must be a valid PDF."}),
        status=400,
        mimetype="application/json",
    )
