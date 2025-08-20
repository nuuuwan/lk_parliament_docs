import os
from functools import cache, cached_property
from tempfile import NamedTemporaryFile

import pymupdf
import pytesseract
from pdf2image import convert_from_path
from utils import File, Log

log = Log("PDFFile")


class PDFFile(File):
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
        im = im.convert("RGB")
        tmp_img_path = NamedTemporaryFile(suffix=".png", delete=False).name
        im.save(tmp_img_path, format="PNG")
        try:
            return pytesseract.image_to_string(str(tmp_img_path), lang="eng")
        except Exception as e:
            log.error(f"[Page {i_page}] Error extracting text from page: {e}")
            return None

    @cache
    def get_image_text(self):
        im_list = convert_from_path(self.path, dpi=300)
        page_text_list = []
        for i_page, im in enumerate(im_list, start=1):
            page_text = self.__get_image_text_from_im__(i_page, im)
            if page_text is not None:
                page_text_list.append(page_text)

        text = "\n\n".join(page_text_list)
        size_k = len(text) / 1_000
        log.debug(f"Extracted {size_k:.0f}KB from {str(self)}")
        return text

    @staticmethod
    def __compress_with_pymupdf__(input_path, output_path):
        assert input_path != output_path

        doc = pymupdf.open(input_path)
        doc.rewrite_images(
            dpi_target=60,
            dpi_threshold=61,
            quality=25,
        )
        doc.ez_save(output_path)

    def compress(self) -> "PDFFile":
        input_path = self.path
        output_path = input_path[:-4] + ".compressed.pdf"
        self.__compress_with_pymupdf__(input_path, output_path)
        output_pdf_file = PDFFile(output_path)
        log.debug(f"Compressed {self} to {output_pdf_file}")
        return output_pdf_file
