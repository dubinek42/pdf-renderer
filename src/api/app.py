import logging

import connexion
import structlog

from .. import services
from ..container import Container
from ..settings import Config


class PdfRendererAPI:
    def __init__(self) -> None:
        self.app = self._create_app()

    def _create_app(self):
        app = connexion.FlaskApp(__name__, specification_dir="openapi/")
        app.add_api("api.yaml")

        Container().wire(modules=[services])
        self._configure_logging(Config().debug)

        return app

    @staticmethod
    def _configure_logging(debug: bool) -> None:
        level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(level=level)
        structlog.configure_once(
            processors=[
                structlog.threadlocal.merge_threadlocal,
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(),
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
        )
