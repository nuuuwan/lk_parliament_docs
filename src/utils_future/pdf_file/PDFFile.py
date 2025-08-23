from utils import Log

from utils_future.FileFuture import FileFuture
from utils_future.pdf_file.PDFCompressMixin import PDFCompressMixin
from utils_future.pdf_file.PDFOCRTextMixin import PDFOCRTextMixin
from utils_future.pdf_file.PDFTextMixin import PDFTextMixin

log = Log("PDFFile")


class PDFFile(FileFuture, PDFCompressMixin, PDFTextMixin, PDFOCRTextMixin):

    def __init__(self, path):
        assert path.endswith(".pdf")
        super().__init__(path)
