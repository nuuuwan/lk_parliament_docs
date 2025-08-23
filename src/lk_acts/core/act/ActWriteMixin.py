import os
from functools import cache, cached_property
from pathlib import Path

from utils import JSONFile, Log

log = Log("ActWriteMixin")


class ActWriteMixin:

    MAX_YEAR = 2025
    MIN_YEAR = 1940
    DIR_DATA = os.path.join("..", "lk_acts_data", "data")

    @staticmethod
    def get_dir_year(year, local=False):
        year = str(year)
        decade = year[:3] + "0s"
        return os.path.join(
            "data" if local else ActWriteMixin.DIR_DATA, "acts", decade, year
        )

    @staticmethod
    def get_dir_act_data(act_id, local=False):
        tokens = act_id.split("-")
        year = tokens[0]
        return os.path.join(ActWriteMixin.get_dir_year(year, local), act_id)

    @property
    def dir_act_data(self):
        dir_act_data = self.get_dir_act_data(self.act_id)
        if not os.path.exists(dir_act_data):
            os.makedirs(dir_act_data)
        return dir_act_data

    @property
    def dir_act_data_local(self):
        return self.get_dir_act_data(self.act_id, local=True)

    @property
    def metadata_json_path(self):
        return os.path.join(self.dir_act_data, "metadata.json")

    @cached_property
    def has_metadata(self):
        return os.path.exists(self.metadata_json_path)

    def write(self):
        data = self.to_dict()
        JSONFile(self.metadata_json_path).write(data)
        log.info(f"✅ Wrote {self.metadata_json_path}")

    @property
    def url(self):
        return (
            "https://github.com/nuuuwan/lk_acts_data/tree/main/"
            + self.dir_act_data_local
        )

    @staticmethod
    def get_dir_data_size():
        path = Path(ActWriteMixin.DIR_DATA)
        return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())

    @cache
    def is_within_valid_time_range(self):
        return self.year_int in range(self.MIN_YEAR, self.MAX_YEAR + 1)
