from functools import cached_property

import pymupdf

from lk_acts.core.act_ext.PDFBlock import PDFBlock


class ActExtPDF:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    @staticmethod
    def remove_non_ascii(x):
        return x.encode("ascii", errors="ignore").decode()

    @staticmethod
    def __parse_raw_block_hacks__(block):
        # HACK
        for delim in [
            "..",
            "   \t ",
        ]:
            if delim in block.text:
                tokens = block.text.split(delim)
                if len(tokens) == 2:
                    text1, text2 = tokens
                    return [
                        PDFBlock(
                            bbox=block.bbox,
                            text=text1.strip(),
                            font_family=block.font_family,
                            font_size=block.font_size,
                        ),
                        PDFBlock(
                            bbox=block.bbox,
                            text=text2.strip(),
                            font_family=block.font_family,
                            font_size=block.font_size,
                        ),
                    ]
        return [block]

    @staticmethod
    def __parse_raw_block__(raw_block):

        span = raw_block["lines"][0]["spans"][0]

        text_list = []
        for line in raw_block["lines"]:
            for span in line["spans"]:
                text_list.append(span.get("text", ""))
        text = " ".join(text_list)
        text = text.strip()
        text = ActExtPDF.remove_non_ascii(text)

        block = PDFBlock(
            bbox=raw_block["bbox"],
            text=text,
            font_family=span.get("font"),
            font_size=span.get("size"),
        )

        return ActExtPDF.__parse_raw_block_hacks__(block)

    @staticmethod
    def __parse_page__(page):
        raw = page.get_text("dict")
        block_list = []
        for raw_block in raw["blocks"]:
            if raw_block.get("type", 0) != 0:
                continue
            blocks = ActExtPDF.__parse_raw_block__(raw_block)
            block_list.extend(blocks)
        block_list.sort(key=lambda box: box.bbox[1])
        return block_list

    @cached_property
    def page_block_list(self) -> list[list[PDFBlock]]:
        doc = pymupdf.open(self.pdf_path)

        page_block_list = []
        for page in doc:
            page_block_list.append(self.__parse_page__(page))

        return page_block_list

    @cached_property
    def n_pages(self) -> int:
        return len(self.page_block_list)

    def analyze(self):
        pass
