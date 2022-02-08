import dramatiq
import structlog

from .. import services
from ..container import Container
from .broker import broker

log = structlog.get_logger(__name__)

dramatiq.set_broker(broker)

Container().wire(modules=[services])


@dramatiq.actor
def render_document(document_id: int):
    log.info("render_document.started")
    services.Render().render_document(document_id)
    log.info("render_document.finished")
