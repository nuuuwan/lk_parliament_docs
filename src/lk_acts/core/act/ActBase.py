from functools import cache, cached_property

from utils import Log

from lk_acts.core.ActType import ActType

log = Log("ActBase")


class ActBase:
    def __init__(
        self, num: str, date: str, description: str, url_pdf_en: str
    ):
        self.num = num
        self.date = date
        self.description = description
        self.url_pdf_en = url_pdf_en

    def __str__(self):
        return f"Act({self.act_id})"

    def __hash__(self):
        return hash(str(self))

    @classmethod
    @cache
    def get_doc_type_name(cls) -> str:
        return "acts"

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            num=data["num"],
            date=data["date"],
            description=data["description"],
            url_pdf_en=data["url_pdf_en"],
        )

    @property
    def doc_sub_num(self) -> int:
        tokens = self.num.split("/")
        if len(tokens) == 2:
            try:
                sum_num_int = int(tokens[0])
                return f"{sum_num_int:03d}"
            except ValueError as e:
                log.error(f'Error parsing doc_sub_num with "{self.num}": {e}')
        return self.description.lower().replace(" ", "-")

    @property
    def act_id(self) -> str:
        return f"{self.year}-{self.doc_sub_num}"

    @property
    def year(self) -> str:
        return self.date[:4]

    @property
    def year_int(self) -> str:
        return int(self.year)

    @property
    def decade(self) -> str:
        return self.year[:3] + "0s"

    @cached_property
    def act_type(self) -> ActType:
        return ActType.from_description(self.description)

    def to_dict(self) -> dict:
        return dict(
            num=self.num,
            date=self.date,
            description=self.description,
            url_pdf_en=self.url_pdf_en,
            act_id=self.act_id,
            act_type=self.act_type.name,
        )
