import os
from dataclasses import dataclass
from functools import cache

from utils import JSONFile, Log

log = Log("Doc")


@dataclass
class Doc:
    doc_num: str
    date: str
    description: str
    lang_to_source_url: dict[str, str]

    @classmethod
    @cache
    def get_doc_type_name(cls) -> str:
        return "acts"

    @staticmethod
    def from_dict(data: dict) -> "Doc":
        return Doc(
            doc_num=data["doc_num"],
            date=data["date"],
            description=data["description"],
            lang_to_source_url=data["lang_to_source_url"],
        )

    @property
    def doc_id(self) -> str:
        return self.doc_num.replace("/", "-").strip()

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
    def dir_doc_data(self):
        dir_doc_data = os.path.join(
            "data", self.get_doc_type_name(), self.year, self.doc_id
        )
        if not os.path.exists(dir_doc_data):
            os.makedirs(dir_doc_data)
        return dir_doc_data

    @property
    def metadata_json_path(self):
        return os.path.join(self.dir_doc_data, "metadata.json")

    def write(self):
        if os.path.exists(self.metadata_json_path):
            return
        data = self.to_dict()
        JSONFile(self.metadata_json_path).write(data)
        log.info(f"Wrote {self.metadata_json_path}")
