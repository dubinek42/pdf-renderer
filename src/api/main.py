from . import app

application = app.PdfRendererAPI().app


def main():
    application.run()


if __name__ == "__main__":
    main()
