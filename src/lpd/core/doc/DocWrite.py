import os
from pathlib import Path

from utils import JSONFile, Log

from lpd.core.doc.DocRead import DocRead

log = Log("DocWrite")


class DocWrite(DocRead):
    DIR_DATA = "data"

    @property
    def dir_doc_data(self):
        dir_doc_data = os.path.join(
            self.DIR_DATA,
            self.get_doc_type_name(),
            self.decade,
            self.year,
            self.doc_id,
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
        log.info(f"✅ Wrote {self.metadata_json_path}")

    @property
    def url(self):
        return self.dir_doc_data

    @staticmethod
    def get_dir_data_size():
        path = Path(DocWrite.DIR_DATA)
        return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
