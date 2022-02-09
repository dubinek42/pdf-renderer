import dramatiq
import structlog

from ..container import Container
from .broker import broker

log = structlog.get_logger(__name__)

dramatiq.set_broker(broker)


@dramatiq.actor
def render_document(document_id: int):
    log.info("render_document.started")

    container = Container()
    render_service = container.render_service()

    render_service.render_document(document_id)

    log.info("render_document.finished")
