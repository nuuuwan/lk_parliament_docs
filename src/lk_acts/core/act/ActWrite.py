import os
from pathlib import Path

from utils import JSONFile, Log

from lk_acts.core.act.ActRead import ActRead

log = Log("ActWrite")


class ActWrite(ActRead):

    @staticmethod
    def get_dir_year(year):
        year = str(year)
        decade = year[:3] + "0s"
        return os.path.join(ActRead.DIR_DATA, "acts", decade, year)

    @staticmethod
    def get_dir_act_data(act_id):
        tokens = act_id.split("-")
        year = tokens[0]
        return os.path.join(ActWrite.get_dir_year(year), act_id)

    @property
    def dir_act_data(self):
        dir_act_data = self.get_dir_act_data(self.act_id)
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
