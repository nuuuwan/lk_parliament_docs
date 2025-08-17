import re
from dataclasses import dataclass
from functools import cached_property

import PyPDF2


class ActExtPDF:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    @cached_property
    def page_text_list(self) -> list[str]:
        text_list = []
        with open(self.pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text_list.append(page.extract_text())
        print("-" * 80)
        print(text_list[0])
        print("-" * 80)
        return text_list

    @cached_property
    def n_pages(self) -> int:
        return len(self.page_text_list)


@dataclass
class ActExt:
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
    def __extract__(re_expr, text: str) -> float:
        for line in text.split("\n"):
            match = re.search(re_expr, line)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def from_pdf(pdf_path):
        act_ext_pdf = ActExtPDF(pdf_path)

        first_page_text = act_ext_pdf.page_text_list[0]
        price = ActExt.__extract__(ActExt.RE_PRICE, first_page_text)
        price_postage = ActExt.__extract__(
            ActExt.RE_PRICE_POSTAGE, first_page_text
        )
        date_certified = ActExt.__extract__(
            ActExt.RE_DATE_CERTIFIED, first_page_text
        )
        date_published = ActExt.__extract__(
            ActExt.RE_DATE_PUBLISHED, first_page_text
        )

        return ActExt(
            n_pages=act_ext_pdf.n_pages,
            date_certified=date_certified,
            date_published=date_published,
            price=price,
            price_postage=price_postage,
        )
