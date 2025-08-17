import re
from dataclasses import dataclass

from lk_acts.core.act_ext.PDFBlock import PDFBlock


@dataclass
class ActExtTitlePage:
    title: str
    num: str
    year: str
    date_certified: str
    date_published: str
    price: float
    price_postage: float

    RE_PRICE = r"Price\s*:\s*Rs\.\s*([0-9]+(?:\.\d{2})?)"
    RE_PRICE_POSTAGE = r"Postage\s*:\s*Rs\.\s*([0-9]+(?:\.\d{2})?)"
    RE_DATE_CERTIFIED = r"Certified on\s+([^\]]+)"
    RE_DATE_PUBLISHED = r"of\s+([A-Za-z]+\s+\d{1,2},\s*\d{4})"

    @staticmethod
    def __extract_heading__(
        block_list: list[PDFBlock],
    ) -> tuple[str, str, str]:
        pattern = re.compile(
            r"^(?P<title>.+?),\s+No\.\s+(?P<num>\d{2})\s+OF\s+(?P<year>\d{4})$"
        )
        match = None
        for block in block_list:
            match = pattern.search(block.text)
            if match:
                break
        if not match:
            raise ValueError("Invalid title page format")
        return match.group("title"), match.group("num"), match.group("year")

    @classmethod
    def from_block_list(cls, block_list):
        title, num, year = ActExtTitlePage.__extract_heading__(block_list)
        price = PDFBlock.extract(cls.RE_PRICE, block_list)
        price_postage = PDFBlock.extract(cls.RE_PRICE_POSTAGE, block_list)
        date_certified = PDFBlock.extract(cls.RE_DATE_CERTIFIED, block_list)
        date_published = PDFBlock.extract(cls.RE_DATE_PUBLISHED, block_list)

        return cls(
            title=title,
            num=num,
            year=year,
            date_certified=date_certified,
            date_published=date_published,
            price=price,
            price_postage=price_postage,
        )

    def to_dict(self):
        return dict(
            title=self.title,
            num=self.num,
            year=self.year,
            date_certified=self.date_certified,
            date_published=self.date_published,
            price=self.price,
            price_postage=self.price_postage,
        )
