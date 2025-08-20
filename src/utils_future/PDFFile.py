import os
from functools import cache, cached_property
from multiprocessing import Pool, cpu_count
from tempfile import NamedTemporaryFile

import pymupdf
import pytesseract
from pdf2image import convert_from_path
from utils import File, Log

log = Log("PDFFile")


class PDFFile(File):
    DPI_TARGET = 75
    QUALITY = 25

    def __init__(self, path):
        assert path.endswith(".pdf")
        super().__init__(path)

    def __str__(self):
        size_m = self.size / 1000_000
        return f"{self.path} ({size_m:.2f} MB)"

    def __hash__(self):
        return hash(self.path)

    @cached_property
    def size(self):
        return os.path.getsize(self.path) if os.path.exists(self.path) else 0

    @staticmethod
    def __get_image_text_from_im__(i_page, im):
        tmp_img_path = NamedTemporaryFile(suffix=".png", delete=False).name
        im.save(tmp_img_path, format="PNG")
        try:
            image_text = pytesseract.image_to_string(
                str(tmp_img_path), lang="eng"
            )
            log.debug(f"[Page {i_page}] Extracted {len(image_text):,} B")
            return image_text
        except Exception as e:
            log.error(f"[Page {i_page}] Error extracting text from page: {e}")
            return None

    def __worker__(self, x):
        return self.__get_image_text_from_im__(x[0], x[1])

    @cache
    def get_image_text(self):
        im_list = convert_from_path(self.path, dpi=PDFFile.DPI_TARGET)
        n_pages = len(im_list)
        log.debug(f"{n_pages=}")
        n_cpus = cpu_count()
        log.debug(f"{n_cpus=}")

        page_text_list = Pool(processes=n_cpus).map(
            self.__worker__,
            enumerate(im_list, start=1),
        )

        page_text_list = [
            page_text for page_text in page_text_list if page_text is not None
        ]

        text = "\n\n".join(page_text_list)
        size_k = len(text) / 1_000
        log.debug(f"Extracted {size_k:.0f}KB from {str(self)}")
        return text

    @staticmethod
    def __compress_with_pymupdf__(input_path, output_path):
        assert input_path != output_path
        doc = pymupdf.open(input_path)

        doc.rewrite_images(
            dpi_target=PDFFile.DPI_TARGET,
            dpi_threshold=PDFFile.DPI_TARGET + 1,
            quality=PDFFile.QUALITY,
        )
        doc.ez_save(output_path)

    def compress(self) -> "PDFFile":
        input_path = self.path
        output_path = input_path[:-4] + ".compressed.pdf"
        self.__compress_with_pymupdf__(input_path, output_path)
        output_pdf_file = PDFFile(output_path)
        log.debug(f"Compressed {self} to {output_pdf_file}")
        return output_pdf_file
