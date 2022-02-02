from . import app


def main():
    application = app.PdfRendererAPI()
    application.app.run()


if __name__ == "__main__":
    main()
