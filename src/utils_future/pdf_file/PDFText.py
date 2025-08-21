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

    def get_block_info_list(self):
        doc = pymupdf.open(self.path)
        block_info_list = []
        for page in doc:
            for b in page.get_text("dict").get("blocks", []):
                if b.get("type", 0) != 0:
                    continue

                bbox = tuple([round(x, 2) for x in b.get("bbox", [])])
                block_text_parts = []

                fonts = set()
                sizes = set()
                for line in b.get("lines", []):
                    for span in line.get("spans", []):
                        t = span.get("text", "")
                        if t:
                            block_text_parts.append(t)
                        f = span.get("font")
                        if f:
                            fonts.add(f)
                        s = span.get("size")
                        if s is not None:
                            sizes.add(s)

                block_text = "".join(block_text_parts)
                block_text = self.__clean_block_text__(block_text)
                if not block_text:
                    continue

                block_info = dict(
                    page_number=page.number,
                    bbox=bbox,
                    fonts=sorted(fonts),
                    sizes=sorted(sizes),
                    text=block_text,
                )
                block_info_list.append(block_info)
        return block_info_list

    def get_block_text(self) -> str:
        block_info_list = self.get_block_info_list()
        text = "\n\n".join(
            [block_info["text"] for block_info in block_info_list]
        )
        self.__log_text_info_and_return__(text, "Block info list text")
        return block_info_list

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
