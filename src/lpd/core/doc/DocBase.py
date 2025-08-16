from dataclasses import dataclass
from functools import cache


@dataclass
class DocBase:
    doc_num: str
    date: str
    description: str
    lang_to_source_url: dict[str, str]

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
        return int(tokens[0])

    @property
    def doc_id(self) -> str:
        return f"{self.year}-{self.doc_sub_num:03d}"

    @property
    def year(self) -> str:
        return self.date[:4]

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
    def emoji(self):
        for keyword, emoji in {
            "amendment": "✏️",
            "repeal": "❌",
            "appropriation": "💰",
            "special provision": "📜",
            "incorporation": "🏢",
        }.items():
            if keyword in self.description.lower():
                return emoji
        return "🏛️"
