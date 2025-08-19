import os
from functools import cached_property

from utils import File, Log

log = Log("PDFFile")


class PDFFile(File):
    def __init__(self, path):
        assert path.endswith(".pdf")
        super().__init__(path)

    def __str__(self):
        size_m = self.size / 1000_000
        return f"{self.path} ({size_m:.2f} MB)"

    @cached_property
    def size(self):
        return os.path.getsize(self.path) if os.path.exists(self.path) else 0

    def ocr(self, output_pdf_path=None) -> "PDFFile":
        import ocrmypdf

        if not output_pdf_path:
            output_pdf_path = self.path[:-4] + ".ocr.pdf"
        ocrmypdf.ocr(self.path, output_pdf_path, language="eng")
        output_pdf_file = PDFFile(output_pdf_path)
        log.info(f"Wrote {str(self)} -> {str(output_pdf_file)}")
