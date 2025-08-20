import pymupdf
from utils import Log

log = Log("PDFFile")


class PDFCompress:
    DPI_TARGET = 75
    QUALITY = 25

    @staticmethod
    def __compress_with_pymupdf__(input_path, output_path):
        assert input_path != output_path
        doc = pymupdf.open(input_path)

        doc.rewrite_images(
            dpi_target=PDFCompress.DPI_TARGET,
            dpi_threshold=PDFCompress.DPI_TARGET + 1,
            quality=PDFCompress.QUALITY,
        )
        doc.ez_save(output_path)

    def compress(self):
        input_path = self.path
        output_path = input_path[:-4] + ".compressed.pdf"
        self.__compress_with_pymupdf__(input_path, output_path)
        output_pdf_file = self.__class__(output_path)
        log.debug(f"Compressed {self} to {output_pdf_file}")
        return output_pdf_file
