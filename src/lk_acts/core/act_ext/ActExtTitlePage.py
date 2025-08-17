from dataclasses import dataclass

from lk_acts.core.act_ext.PDFBlock import PDFBlock


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
