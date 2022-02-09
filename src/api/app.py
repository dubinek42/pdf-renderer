import logging
import sys

import connexion
from pydantic import BaseSettings
import structlog

from .. import services
from ..constants import MAX_UPLOAD_SIZE_BYTES
from ..container import Container
from ..settings import Config
from .handlers import errors, processing


class PdfRendererAPI:
    def __init__(self, config: BaseSettings) -> None:
        self.config = config
        self.app = self._create_app()

    def _create_app(self):
        app = connexion.FlaskApp(__name__, specification_dir="openapi/")
        app.add_api("api.yaml")

        container = Container()
        container.wire(modules=[services, processing])
        self._configure_logging(self.config.debug)
        app.app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_SIZE_BYTES
        app.app.container = container
        self._register_error_handlers(app)

        return app

    @staticmethod
    def _configure_logging(debug: bool) -> None:
        level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(stream=sys.stderr, format="%(message)s", level=level)
        structlog.configure(
            processors=[
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.dev.ConsoleRenderer(),
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    @staticmethod
    def _register_error_handlers(app: connexion.FlaskApp):
        for error, handler in errors.blueprint.items():
            app.add_error_handler(error, handler)
