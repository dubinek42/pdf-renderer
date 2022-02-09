import json

import structlog
from dependency_injector.wiring import Provide, inject
from dramatiq.errors import ConnectionError
from flask import Response, request, send_from_directory

from ... import services
from ...container import Container
from ...messaging import tasks

log = structlog.get_logger(__name__)


@inject
def get_result_page(
    document_id: int,
    page: int,
    base_path: str = Provide[Container.config.provided.path_images],
    processed_image_service: services.ProcessedImage = Provide[
        Container.processed_image_service
    ],
) -> Response:
    log.debug("get_result_page.started")
    image = processed_image_service.get_one_page(document_id, page)
    return send_from_directory(base_path, image.file_path)


@inject
def get_result_full(
    document_id: int,
    processed_image_service: services.ProcessedImage = Provide[
        Container.processed_image_service
    ],
) -> Response:
    log.debug("get_result_full.started")
    images = processed_image_service.get_all_by_document_id(document_id)
    response = processed_image_service.compose_multipart_response(images)
    return Response(response.to_string(), mimetype=response.content_type)


@inject
def get_status(
    document_id: int, document_service=Provide[Container.document_service]
) -> Response:
    return Response(
        document_service.get_status_by_document_id(document_id).json(),
        status=200,
        mimetype="application/json",
    )


@inject
def upload_document(
    document_service: services.Document = Provide[Container.document_service],
) -> Response:
    document_id = document_service.create_document(request.data)
    try:
        tasks.render_document.send(document_id)
        log.info("upload_document.task_sent_to_broker", document_id=document_id)
    except ConnectionError as exc:
        log.exception("upload_document.send_task_to_broker.failed", exc=exc)

    return Response(
        json.dumps({"id": document_id, "message": "Document sucessfully uploaded."}),
        status=201,
        mimetype="application/json",
    )
