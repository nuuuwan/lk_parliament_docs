import os
from pathlib import Path

from utils import JSONFile, Log

from lk_acts.core.act.ActRead import ActRead

log = Log("ActWrite")


class ActWrite(ActRead):
    DIR_DATA = "data"

    @property
    def dir_act_data(self):
        dir_act_data = os.path.join(
            self.DIR_DATA,
            self.get_doc_type_name(),
            self.decade,
            self.year,
            self.act_id,
        )
        if not os.path.exists(dir_act_data):
            os.makedirs(dir_act_data)
        return dir_act_data

    @property
    def metadata_json_path(self):
        return os.path.join(self.dir_act_data, "metadata.json")

    def write(self):
        if os.path.exists(self.metadata_json_path):
            return
        data = self.to_dict()
        JSONFile(self.metadata_json_path).write(data)
        log.info(f"✅ Wrote {self.metadata_json_path}")

    @property
    def url(self):
        return self.dir_act_data

    @staticmethod
    def get_dir_data_size():
        path = Path(ActWrite.DIR_DATA)
        return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
