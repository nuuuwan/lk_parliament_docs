import os
import unittest

from utils_future import DataFile


class TestCase(unittest.TestCase):
    def test_data(self):
        for obj in [{"name": "Nuwan"}]:

            def get_data(obj1):
                return obj1

            def get_path(obj):
                return os.path.join(
                    "tests", "data", f"data_file.{obj['name']}.json"
                )

            data_file = DataFile(obj, get_path, get_data)
            self.assertEqual(data_file.data, obj)
