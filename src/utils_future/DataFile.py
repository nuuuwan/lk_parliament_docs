import os
from functools import cached_property

from utils import JSONFile


class DataFile(JSONFile):
    def __init__(self, obj, get_path, get_data):
        super().__init__(get_path(obj))
        self.obj = obj
        self.get_path = get_path
        self.get_data = get_data

    @cached_property
    def path_fail(self):
        return self.path + ".fail"

    @cached_property
    def data(self):
        if os.path.exists(self.path):
            return self.read()

        if os.path.exists(self.path_fail):
            return None

        data = self.get_data(self.obj)
        if data is not None:
            self.write(data)
            return data

        JSONFile(self.path_fail).write("")
        return None
