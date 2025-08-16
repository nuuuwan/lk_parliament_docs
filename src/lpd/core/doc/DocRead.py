import os

from utils import JSONFile, Log

from lpd.core.doc.DocBase import DocBase

log = Log("DocRead")


class DocRead(DocBase):
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
    def list_all(cls):
        doc_list = []
        for metadata_file_path in DocRead.__gen_metadata_file_paths__():
            doc = cls.from_file(metadata_file_path)
            doc_list.append(doc)
        log.info(f"Read {len(doc_list):,} docs.")
        return doc_list
