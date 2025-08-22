import os
from functools import cached_property

from utils import File, JSONFile, Log

log = Log("DataFile")


class DataFile(File):
    def __init__(self, obj, get_path, get_data):
        super().__init__(get_path(obj))
        self.obj = obj
        self.get_path = get_path
        self.get_data = get_data

    @cached_property
    def exists(self):
        return os.path.exists(self.path)

    @cached_property
    def size(self):
        return os.path.getsize(self.path)

    @cached_property
    def size_humanized(self):
        size = self.size
        if size > 1_000_000:
            return f"{size / 1_000_000:.1f} MB"
        if size > 1_000:
            return f"{size / 1_000:.1f} KB"
        return f"{size} bytes"

    @cached_property
    def path_fail(self):
        return self.path + ".fail"

    def __get_data_hot__(self):
        data = self.get_data(self.obj)
        if data is not None:
            self.write(data)
            return data
        JSONFile(self.path_fail).write("")
        return None

    def io_class(self):
        return JSONFile if self.path.endswith(".json") else File

    def read(self):
        contents = self.io_class()(self.path).read()
        return contents

    @staticmethod
    def get_write_message(data):
        if isinstance(data, list):
            return f"{len(data):,} items"
        if isinstance(data, str):
            return f"{len(data):,} chars"
        raise ValueError(f"Unsupported data type: {type(data).__name__}")

    def write(self, data):
        contents = self.io_class()(self.path).write(data)
        log.info(
            f"Wrote {self.path}"
            + f" ({self.get_write_message(data)}, {self.size_humanized})"
        )
        return contents

    @cached_property
    def data(self):
        if os.path.exists(self.path):
            return self.read()

        if os.path.exists(self.path_fail):
            return None

        return self.__get_data_hot__()
