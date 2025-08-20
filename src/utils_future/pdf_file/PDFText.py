import re

import pymupdf
from utils import Log

log = Log("PDFText")


class PDFText:
    MIN_TEXT_SIZE = 1_000

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

    def get_text(self) -> str:
        block_text = self.get_block_text()
        if len(block_text) >= PDFText.MIN_TEXT_SIZE:
            return block_text

        raw_text = self.get_raw_text()
        if len(raw_text) >= PDFText.MIN_TEXT_SIZE:
            return raw_text

        image_text = self.get_image_text()
        if len(image_text) >= PDFText.MIN_TEXT_SIZE:
            return image_text

        raise ValueError(f"[{self}] No valid text found.")
