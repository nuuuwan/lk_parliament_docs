import os

from utils import JSONFile, Log

log = Log("DocWrite")


class DocWrite:
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
