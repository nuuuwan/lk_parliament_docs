from dataclasses import dataclass
from functools import cache


@dataclass
class DocBase:
    doc_num: str
    date: str
    description: str
    lang_to_source_url: dict[str, str]

    DOC_ACT_TYPE_TO_EMOJI = {
        "amendment": "✏️",
        "repeal": "❌",
        "appropriation": "💰",
        "special-provision": "📜",
        "incorporation": "🏢",
        "amendment-to-the-constitution": "🧽",
    }
    EMOJI_GENERAL = "🏛️"

    @classmethod
    @cache
    def get_doc_type_name(cls) -> str:
        return "acts"

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            doc_num=data["doc_num"],
            date=data["date"],
            description=data["description"],
            lang_to_source_url=data["lang_to_source_url"],
        )

    @property
    def doc_sub_num(self) -> int:
        tokens = self.doc_num.split("/")
        if len(tokens) == 2:
            sum_num_int = int(tokens[0])
            return f"{sum_num_int:03d}"
        return self.description.lower().replace(" ", "-")

    @property
    def doc_id(self) -> str:
        return f"{self.year}-{self.doc_sub_num}"

    @property
    def year(self) -> str:
        return self.date[:4]

    @property
    def decade(self) -> str:
        return self.year[:3] + "0s"

    def to_dict(self) -> dict:
        return dict(
            doc_type_nam=self.get_doc_type_name(),
            doc_num=self.doc_num,
            date=self.date,
            description=self.description,
            lang_to_source_url=self.lang_to_source_url,
            doc_id=self.doc_id,
        )

    @property
    def doc_act_type(self):
        for doc_act_type in self.DOC_ACT_TYPE_TO_EMOJI.keys():
            if doc_act_type in self.description.lower().replace(" ", "-"):
                return doc_act_type
        return "general"

    @property
    def emoji(self):
        return self.DOC_ACT_TYPE_TO_EMOJI.get(
            self.doc_act_type, self.EMOJI_GENERAL
        )
