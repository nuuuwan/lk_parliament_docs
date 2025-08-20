import os
from functools import cached_property

from utils import File, Log

from utils_future.pdf_file.PDFCompress import PDFCompress
from utils_future.pdf_file.PDFImageText import PDFImageText
from utils_future.pdf_file.PDFText import PDFText

log = Log("PDFFile")


class PDFFile(File, PDFCompress, PDFText, PDFImageText):

    def __init__(self, path):
        assert path.endswith(".pdf")
        super().__init__(path)

    def __str__(self):
        size_m = self.size / 1000_000.0
        if size_m > 1:
            return f"{self.path} ({size_m:.1f} MB)"
        size_k = self.size / 1_000.0
        return f"{self.path} ({size_k:.1f} kB)"

    def __hash__(self):
        return hash(self.path)

    @cached_property
    def size(self):
        return os.path.getsize(self.path) if os.path.exists(self.path) else 0
