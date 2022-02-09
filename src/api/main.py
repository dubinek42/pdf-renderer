from . import app
from ..settings import Config

application = app.PdfRendererAPI(Config()).app


def main():
    application.run()


if __name__ == "__main__":
    main()
