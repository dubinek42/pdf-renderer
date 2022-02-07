class CannotOpenFileError(Exception):
    pass


class ProcessingNotFinishedError(Exception):
    def __init__(self, document_id: int) -> None:
        self.document_id = document_id


class PdfInvalidError(Exception):
    pass
