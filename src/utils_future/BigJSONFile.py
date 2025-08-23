import os
from functools import cached_property

from utils import JSONFile, Log

log = Log("BigJSONFile")


class BigJSONFile(JSONFile):
    MIN_BIG_FILE_SIZE = 50_000_000

    @cached_property
    def exists(self):
        return os.path.exists(self.path)

    @cached_property
    def size(self):
        return os.path.getsize(self.path) if self.exists else 0

    @cached_property
    def size_humanized(self):
        size = self.size
        for unit, label in [
            [1_000_000_000, "GB"],
            [1_000_000, "MB"],
            [1_000, "kB"],
        ]:
            if size > unit:
                return f"{size/unit:.1f} {label}"

        return size + " B"

    def __str__(self):
        return f"{self.path} ({self.size_humanized})"

    def split(self):
        file_path = self.path
        assert os.path.exists(file_path)
        file_size = os.path.getsize(file_path)
        if file_size < self.MIN_BIG_FILE_SIZE:
            log.info(f"{self} is not big enough to split")
            return
        log.info(f"Splitting {self}")

        n_splits = file_size // self.MIN_BIG_FILE_SIZE + 1

        data_list = JSONFile(file_path).read()
        n_data = len(data_list)
        split_size = n_data // n_splits + 1
        for i in range(n_splits):
            i_start = i * split_size
            i_end = min((i + 1) * split_size, file_size)
            split_data_list = data_list[i_start:i_end]
            split_file_path = file_path + f"-part-{i:02d}.json"
            split_file = BigJSONFile(split_file_path)
            split_file.write(split_data_list)
            log.info(f"✅ Wrote {split_file}")
        os.remove(file_path)
        log.info(f"❌ Removed {self}")
