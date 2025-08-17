import re
from dataclasses import dataclass
from functools import cached_property

import pymupdf


@dataclass
class PDFBlock:
    bbox: tuple[float, float, float, float]
    text: str

    @staticmethod
    def extract(re_expr, block_list: list["PDFBlock"]) -> float:
        for block in block_list:
            match = re.search(re_expr, block.text)
            if match:
                return match.group(1)
        return None


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
                block = PDFBlock(
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
        pass


@dataclass
class ActExtTitlePage:

    date_certified: str
    date_published: str
    price: float
    price_postage: float

    RE_PRICE = r"Price\s*:\s*Rs\.\s*([0-9]+(?:\.\d{2})?)"
    RE_PRICE_POSTAGE = r"Postage\s*:\s*Rs\.\s*([0-9]+(?:\.\d{2})?)"
    RE_DATE_CERTIFIED = r"Certified on\s+([^\]]+)"
    RE_DATE_PUBLISHED = r"of\s+([A-Za-z]+\s+\d{1,2},\s*\d{4})"

    @classmethod
    def from_block_list(cls, block_list):

        price = PDFBlock.extract(cls.RE_PRICE, block_list)
        price_postage = PDFBlock.extract(cls.RE_PRICE_POSTAGE, block_list)
        date_certified = PDFBlock.extract(cls.RE_DATE_CERTIFIED, block_list)
        date_published = PDFBlock.extract(cls.RE_DATE_PUBLISHED, block_list)

        return cls(
            date_certified=date_certified,
            date_published=date_published,
            price=price,
            price_postage=price_postage,
        )

    def to_dict(self):
        return dict(
            date_certified=self.date_certified,
            date_published=self.date_published,
            price=self.price,
            price_postage=self.price_postage,
        )


@dataclass
class ActSection:
    num: int
    text: str

    def to_dict(self):
        return dict(num=self.num, text=self.text)


@dataclass
class ActExtBodyPages:
    section_list: list[ActSection]

    @classmethod
    def from_block_list(cls, __):
        return ActExtBodyPages(section_list=[])

    def to_dict(self):
        return dict(
            section_list=[section.to_dict() for section in self.section_list]
        )


@dataclass
class ActExt:
    n_pages: int
    title_page: ActExtTitlePage
    body_pages: ActExtBodyPages

    @classmethod
    def from_pdf(cls, pdf_path):
        act_ext_pdf = ActExtPDF(pdf_path)

        return cls(
            n_pages=act_ext_pdf.n_pages,
            title_page=ActExtTitlePage.from_block_list(
                act_ext_pdf.page_block_list[0]
            ),
            body_pages=ActExtBodyPages.from_block_list(
                act_ext_pdf.page_block_list[1]
            ),
        )

    def to_dict(self):
        return dict(
            n_pages=self.n_pages,
            title_page=self.title_page.to_dict(),
            body_pages=self.body_pages.to_dict(),
        )
