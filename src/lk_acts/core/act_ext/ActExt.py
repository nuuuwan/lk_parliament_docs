import re
from dataclasses import dataclass
from functools import cached_property
from itertools import chain

import pymupdf


@dataclass
class PDFBlock:
    bbox: tuple[float, float, float, float]
    text: str
    font_family: str
    font_size: float

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
    def page_block_list(self) -> list[list[PDFBlock]]:
        doc = pymupdf.open(self.pdf_path)

        page_block_list = []
        for page in doc:
            print("\n" * 2)
            print("-" * 32)
            raw = page.get_text("dict")
            block_list = []
            for raw_block in raw["blocks"]:

                if raw_block.get("type", 0) != 0:
                    continue
                span = raw_block["lines"][0]["spans"][0]

                text_list = []
                for line in raw_block["lines"]:
                    for span in line["spans"]:
                        text_list.append(span.get("text", ""))
                text = " ".join(text_list)

                block = PDFBlock(
                    bbox=raw_block["bbox"],
                    text=text,
                    font_family=span.get("font"),
                    font_size=span.get("size"),
                )
                print(block)
                print("." * 32)
                block_list.append(block)

            block_list.sort(key=lambda box: box.bbox[1])
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
class ActSubSection:
    num: int
    text: str
    inner_block_list: list[PDFBlock]

    RE_SUB_SECTION = r"^\((?P<num>\d+)\)\s*(?P<text>.+)"

    def to_dict(self):
        return dict(
            num=self.num,
            text=self.text,
            inner_text_list=[block.text for block in self.inner_block_list],
        )

    @classmethod
    def list_from_block_list(cls, block_list: list[PDFBlock]):
        sub_section_d_list = []

        for block in block_list:
            match = re.match(cls.RE_SUB_SECTION, block.text)
            if not match:
                if sub_section_d_list:
                    sub_section_d_list[-1]["inner_block_list"].append(block)
                continue

            section_d = dict(
                num=int(match.group("num")),
                text=match.group("text"),
                inner_block_list=[],
            )
            sub_section_d_list.append(section_d)

        sub_section_list = []
        for sub_section_d in sub_section_d_list:
            section = ActSubSection(
                num=sub_section_d["num"],
                text=sub_section_d["text"],
                inner_block_list=sub_section_d["inner_block_list"],
            )
            sub_section_list.append(section)
        return sub_section_list


@dataclass
class ActSection:
    num: int
    short_description: str
    text: str
    sub_section_list: list[ActSubSection]

    RE_SECTION = r"^(?P<num>\d+)\s*\.\s*(?P<text>.+)"

    def to_dict(self):
        return dict(
            num=self.num,
            short_description=self.short_description,
            text=self.text,
            sub_section_list=[
                sub_section.to_dict() for sub_section in self.sub_section_list
            ],
        )

    @staticmethod
    def parse_short_description(block_list: list[PDFBlock]):
        for block in block_list:
            if block.font_size <= 8:
                return block.text

    @classmethod
    def list_from_block_list(cls, block_list: list[PDFBlock]):
        section_d_list = []

        for block in block_list:
            match = re.match(cls.RE_SECTION, block.text)
            if not match:
                if section_d_list:
                    section_d_list[-1]["inner_block_list"].append(block)
                continue

            section_d = dict(
                num=int(match.group("num")),
                text=match.group("text"),
                inner_block_list=[],
            )
            section_d_list.append(section_d)

        section_list = []
        for section_d in section_d_list:
            section = ActSection(
                num=section_d["num"],
                short_description=ActSection.parse_short_description(
                    section_d["inner_block_list"]
                ),
                text=section_d["text"],
                sub_section_list=ActSubSection.list_from_block_list(
                    section_d["inner_block_list"]
                ),
            )
            section_list.append(section)
        return section_list


@dataclass
class ActExtBodyPages:
    section_list: list[ActSection]

    def to_dict(self):
        return dict(
            section_list=[section.to_dict() for section in self.section_list]
        )

    @classmethod
    def from_block_list(cls, block_list):
        return ActExtBodyPages(
            section_list=ActSection.list_from_block_list(block_list)
        )


@dataclass
class ActExt:
    n_pages: int
    title_page: ActExtTitlePage
    body_pages: ActExtBodyPages

    @cached_property
    def n_sections(self):
        return len(self.body_pages.section_list)

    @classmethod
    def from_pdf(cls, pdf_path):
        act_ext_pdf = ActExtPDF(pdf_path)

        return cls(
            n_pages=act_ext_pdf.n_pages,
            title_page=ActExtTitlePage.from_block_list(
                act_ext_pdf.page_block_list[0]
            ),
            body_pages=ActExtBodyPages.from_block_list(
                list(chain.from_iterable(act_ext_pdf.page_block_list[1:]))
            ),
        )

    def to_dict(self):
        return dict(
            n_pages=self.n_pages,
            title_page=self.title_page.to_dict(),
            body_pages=self.body_pages.to_dict(),
        )
