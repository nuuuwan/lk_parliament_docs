import re

import pymupdf
from utils import Log

log = Log("PDFText")


class PDFText:
    MIN_TEXT_SIZE = 1_000

    def __log_text_info_and_return__(self, text, label):
        size = len(text)
        log.debug(f"[{label}] Extracted {size:,} chars from {str(self)}")
        return text

    @staticmethod
    def __clean_block_text__(block_text: str) -> str:
        block_text = block_text or ""
        block_text = block_text.replace("\n", " ")
        block_text = re.sub(r"[^\x00-\x7F]+", "", block_text)
        block_text = re.sub(r"\s+", " ", block_text)
        block_text = block_text.strip()
        return block_text

    @staticmethod
    def __parse_lines_inner__(span, block_text_parts, fonts, sizes):
        t = span.get("text", "")
        if t:
            block_text_parts.append(t)
        f = span.get("font")
        if f:
            fonts.add(f)
        s = span.get("size")
        if s is not None:
            sizes.add(s)

    @staticmethod
    def __parse_lines__(b):
        block_text_parts = []
        fonts = set()
        sizes = set()
        for line in b.get("lines", []):
            for span in line.get("spans", []):
                PDFText.__parse_lines_inner__(
                    span, block_text_parts, fonts, sizes
                )
        block_text = "".join(block_text_parts)
        block_text = PDFText.__clean_block_text__(block_text)
        return fonts, sizes, block_text

    def get_block_info_list(self):
        doc = pymupdf.open(self.path)
        block_info_list = []
        for page in doc:
            for b in page.get_text("dict").get("blocks", []):
                if b.get("type", 0) != 0:
                    continue
                fonts, sizes, block_text = self.__parse_lines__(b)
                if not block_text:
                    continue
                bbox = tuple([round(x, 2) for x in b.get("bbox", [])])

                block_info = dict(
                    page_number=page.number,
                    bbox=bbox,
                    fonts=sorted(fonts),
                    sizes=sorted(sizes),
                    text=block_text,
                )
                block_info_list.append(block_info)
        return block_info_list
