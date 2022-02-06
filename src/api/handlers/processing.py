import json

from dependency_injector.wiring import Provide, inject
from flask import Response, send_from_directory

from ... import services
from ...container import Container


@inject
def get_result_page(
    document_id: int,
    page: int,
    base_path: str = Provide[Container.config.provided.path_images],
) -> Response:
    processed_image_service = services.ProcessedImage()
    image = processed_image_service.get_one_page(document_id, page)
    return send_from_directory(base_path, image.file_path)


def get_result_full(document_id: int) -> Response:
    processed_image_service = services.ProcessedImage()
    images = processed_image_service.get_all_by_document_id(document_id)
    response = processed_image_service.compose_multipart_response(images)
    return Response(response.to_string(), mimetype=response.content_type)


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
