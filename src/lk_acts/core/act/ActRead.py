import os
from functools import cache

from utils import JSONFile, Log

from lk_acts.core.act.ActBase import ActBase

log = Log("ActRead")


class ActRead(ActBase):
    @staticmethod
    def __gen_metadata_file_paths__():
        for cur_root, _, files in os.walk("data"):
            for file in files:
                file_path = os.path.join(cur_root, file)
                if file == "metadata.json":
                    yield file_path

    @classmethod
    def from_file(cls, file_path: str):
        d = JSONFile(file_path).read()
        return cls.from_dict(d)

    @classmethod
    @cache
    def list_all(cls):
        doc_list = []
        for metadata_file_path in ActRead.__gen_metadata_file_paths__():
            doc = cls.from_file(metadata_file_path)
            doc_list.append(doc)
        doc_list.sort(
            key=lambda x: (
                x.act_id,
                x.date,
            ),
            reverse=True,
        )
        log.info(f"Read {len(doc_list):,} docs.")
        return doc_list

    @classmethod
    @cache
    def year_to_list(cls):
        doc_list = cls.list_all()
        idx = {}
        for doc in doc_list:
            idx.setdefault(doc.year, []).append(doc)
        return idx

    @classmethod
    @cache
    def year_to_type_to_list(cls):
        doc_list = cls.list_all()
        idx = {}
        for doc in doc_list:
            idx.setdefault(doc.year, {}).setdefault(
                doc.act_type.name, []
            ).append(doc)
        return idx
