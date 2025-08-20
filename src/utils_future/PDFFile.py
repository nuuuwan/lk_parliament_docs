import os
import re
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
    MIN_TEXT_SIZE = 1_000

    def __init__(self, path):
        assert path.endswith(".pdf")
        super().__init__(path)

    def __str__(self):
        size_m = self.size / 1000_000
        if size_m > 1:
            return f"{self.path} ({size_m:.1f} MB)"
        size_k = self.size / 1_000
        return f"{self.path} ({size_k:.1f} kB)"

    def __hash__(self):
        return hash(self.path)

    @cached_property
    def size(self):
        return os.path.getsize(self.path) if os.path.exists(self.path) else 0

    def __log_text_info_and_return__(self, text, label):
        size_k = len(text) / 1_000
        log.debug(f"[{label}] Extracted {size_k:.1f} kB from {str(self)}")
        return text

    def get_raw_text(self) -> str:
        doc = pymupdf.open(self.path)
        page_text_list = []
        for page in doc:
            page_text = page.get_text()
            page_text_list.append(page_text)
        doc.close()
        text = "\n\n".join(page_text_list)
        return self.__log_text_info_and_return__(text, "Raw text")

    @staticmethod
    def __clean_block_text__(block_text: str) -> str:
        block_text = block_text or ""
        block_text = block_text.replace("\n", " ")
        block_text = re.sub(r"[^\x00-\x7F]+", "", block_text)
        block_text = re.sub(r"\s+", " ", block_text)
        block_text = block_text.strip()
        return block_text

    def get_block_text(self) -> str:
        doc = pymupdf.open(self.path)
        block_text_list = []
        for page in doc:
            blocks = page.get_text("blocks")
            blocks = sorted(blocks, key=lambda b: (b[1], b[0]))
            for block in blocks:
                block_type = block[6] if len(block) > 6 else 0
                if block_type != 0:
                    continue
                block_text = block[4] if len(block) > 4 else ""
                block_text = self.__clean_block_text__(block_text)
                if block_text:
                    block_text_list.append(block_text)
        text = "\n\n".join(block_text_list)
        return self.__log_text_info_and_return__(text, "Block text")

    @staticmethod
    def __get_image_text_from_image_path__(i_page, image_path):
        try:
            image_text = pytesseract.image_to_string(image_path, lang="eng")
            log.debug(f"[Page {i_page}] Extracted {len(image_text):,} B")
            return image_text
        except Exception as e:
            log.error(f"[Page {i_page}] Error extracting text from page: {e}")
            return None

    def __worker__(self, x):
        return self.__get_image_text_from_image_path__(x[0], x[1])

    @cache
    def get_image_text(self):
        im_list = convert_from_path(self.path, dpi=PDFFile.DPI_TARGET)
        n_pages = len(im_list)
        log.debug(f"{n_pages=}")
        n_cpus = cpu_count()
        log.debug(f"{n_cpus=}")

        temp_image_path_list = []
        for im in im_list:
            temp_img_path = NamedTemporaryFile(
                suffix=".png", delete=False
            ).name
            im.save(temp_img_path, format="PNG")
            temp_image_path_list.append(temp_img_path)

        page_text_list = Pool(processes=n_cpus).map(
            self.__worker__,
            enumerate(temp_image_path_list, start=1),
        )

        page_text_list = [
            page_text for page_text in page_text_list if page_text is not None
        ]

        text = "\n\n".join(page_text_list)
        return self.__log_text_info_and_return__(text, "Image text")

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

    def get_text(self) -> str:
        block_text = self.get_block_text()
        if len(block_text) >= PDFFile.MIN_TEXT_SIZE:
            return block_text

        raw_text = self.get_raw_text()
        if len(raw_text) >= PDFFile.MIN_TEXT_SIZE:
            return raw_text

        image_text = self.get_image_text()
        if len(image_text) >= PDFFile.MIN_TEXT_SIZE:
            return image_text

        raise ValueError(f"[{self}] No valid text found.")
