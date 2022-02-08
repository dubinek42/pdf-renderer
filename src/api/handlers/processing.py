import json

import structlog
from dependency_injector.wiring import Provide, inject
from dramatiq.errors import ConnectionError
from flask import Response, request, send_from_directory

from ... import services
from ...container import Container

log = structlog.get_logger(__name__)


@inject
def get_result_page(
    document_id: int,
    page: int,
    base_path: str = Provide[Container.config.provided.path_images],
) -> Response:
    log.debug("get_result_page.started")
    processed_image_service = services.ProcessedImage()
    image = processed_image_service.get_one_page(document_id, page)
    return send_from_directory(base_path, image.file_path)


def get_result_full(document_id: int) -> Response:
    log.debug("get_result_full.started")
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
    document_service = services.Document()
    document_id = document_service.create_document(request.data)

    try:
        services.Render().do_the_thing.send(document_id)
    except ConnectionError as exc:
        log.exception("upload_document.send_task_to_broker.failed", exc=exc)

    return Response(
        json.dumps({"id": document_id, "message": "Document sucessfully uploaded."}),
        status=201,
        mimetype="application/json",
    )
