# flake8: noqa
import os
import unittest

from utils import JSONFile, Log

from lk_acts import ActExt

TEST_PDF_PATH = os.path.join("tests", "data", "en.pdf")

DIR_TESTS_DATA = os.path.join("tests", "data")

log = Log("test_act_ext")

# Copy data Example
# cp -r data/acts/2020s/2025/2025-012 tests/data

FORCE_MODE = True


class TestCase(unittest.TestCase):

    def __test_helper__(self, dir_path, label, get_actual):
        json_file = JSONFile(os.path.join(dir_path, f"_{label}.json"))
        actual = get_actual()
        if not os.path.exists(json_file.path) or FORCE_MODE:
            json_file.write(actual)
        expected = json_file.read()
        if actual != expected:
            print(actual)
            print("." * 16)
            print(expected)
            print("-" * 32)
        self.assertEqual(actual, expected)

    def test_from_pdf(self):
        for dir_name in os.listdir(DIR_TESTS_DATA):
            # if dir_name not in ["2025-011"]:
            #     continue
            dir_path = os.path.join(DIR_TESTS_DATA, dir_name)
            if not os.path.isdir(dir_path):
                continue
            # os.system(f"open {dir_path}")

            pdf_path = os.path.join(dir_path, "en.pdf")
            act_ext = ActExt.from_pdf(pdf_path)

            act_ext.write_md(os.path.join(dir_path, "_README.md"))

            self.__test_helper__(
                dir_path, "title_page", act_ext.title_page.to_dict
            )

            self.__test_helper__(dir_path, "stats", act_ext.get_stats)

            def get_preamble():
                return act_ext.body_pages.preamble

            self.__test_helper__(dir_path, "preamble", get_preamble)

            self.__test_helper__(dir_path, "act", act_ext.to_dict)
