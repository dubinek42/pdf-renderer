import io

import structlog
from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError

from . import errors

log = structlog.get_logger(__name__)


class RenderService:
    @staticmethod
    def check_document(data: bytes) -> int:
        """Check if document is a valid PDF.

        Args:
            data: Binary data of document.

        Raises:
            PdfInvalidError: File is not valid.

        Returns:
            Number of pages in document.

        """
        try:
            bytes_stream = io.BytesIO(data)
            pdf = PdfFileReader(bytes_stream)
            return pdf.getNumPages()
        except PdfReadError as exc:
            log.exception("pdf_read.error", exc=exc)
            raise errors.PdfInvalidError
