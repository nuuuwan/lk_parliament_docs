import re
from dataclasses import dataclass
from functools import cached_property

import pymupdf


class ActExtPDF:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    @cached_property
    def page_block_list(self) -> list[str]:
        doc = pymupdf.open(self.pdf_path)

        page_block_list = []
        for page in doc:
            raw_block_list = page.get_text("blocks")
            block_list = []
            for x0, y0, x1, y1, text, *_ in raw_block_list:
                block = dict(
                    bbox=(x0, y0, x1, y1),
                    text=text.strip(),
                )
                block_list.append(block)

            page_block_list.append(block_list)
        return page_block_list

    @cached_property
    def n_pages(self) -> int:
        return len(self.page_block_list)

    def analyze(self):
        doc = pymupdf.open(self.pdf_path)
        page = doc[1]

        blocks = page.get_text("blocks")

        for x0, y0, x1, y1, text, *_ in blocks:
            print("-" * 32)
            print((x0, y0, x1, y1))
            print("." * 8)
            print(text.strip())


@dataclass
class ActExtTitlePage:
    n_pages: int
    date_certified: str
    date_published: str
    price: float
    price_postage: float

    RE_PRICE = r"Price\s*:\s*Rs\.\s*([0-9]+(?:\.\d{2})?)"
    RE_PRICE_POSTAGE = r"Postage\s*:\s*Rs\.\s*([0-9]+(?:\.\d{2})?)"
    RE_DATE_CERTIFIED = r"Certified on\s+([^\]]+)"
    RE_DATE_PUBLISHED = r"of\s+([A-Za-z]+\s+\d{1,2},\s*\d{4})"

    @staticmethod
    def __extract__(re_expr, block_list: list[str]) -> float:
        for block in block_list:
            text = block["text"]
            match = re.search(re_expr, text)
            if match:
                return match.group(1)
        return None

    @classmethod
    def from_pdf(cls, pdf_path):
        act_ext_pdf = ActExtPDF(pdf_path)
        act_ext_pdf.analyze()
        first_page_block_list = act_ext_pdf.page_block_list[0]

        price = cls.__extract__(ActExt.RE_PRICE, first_page_block_list)
        price_postage = cls.__extract__(
            ActExt.RE_PRICE_POSTAGE, first_page_block_list
        )
        date_certified = cls.__extract__(
            ActExt.RE_DATE_CERTIFIED, first_page_block_list
        )
        date_published = cls.__extract__(
            ActExt.RE_DATE_PUBLISHED, first_page_block_list
        )

        return cls(
            n_pages=act_ext_pdf.n_pages,
            date_certified=date_certified,
            date_published=date_published,
            price=price,
            price_postage=price_postage,
        )


class ActExt(ActExtTitlePage):
    pass
