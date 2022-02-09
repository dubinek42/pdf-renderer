from ..settings import Config
from . import app

application = app.PdfRendererAPI(Config()).app
