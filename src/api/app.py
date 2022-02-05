import connexion

from .. import services
from ..container import Container


class PdfRendererAPI:
    def __init__(self) -> None:
        self.app = self._create_app()

    def _create_app(self):
        app = connexion.FlaskApp(__name__, specification_dir="openapi/")
        app.add_api("api.yaml")

        Container().wire(modules=[services])

        return app
