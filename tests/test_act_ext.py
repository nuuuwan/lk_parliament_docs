# flake8: noqa
import json
import os
import unittest

from lk_acts import ActExt

TEST_PDF_PATH = os.path.join("tests", "input", "en.pdf")


class TestCase(unittest.TestCase):
    def test_from_pdf(self):
        act_ext = ActExt.from_pdf(TEST_PDF_PATH)
        self.assertEqual(act_ext.n_pages, 5)
        print(json.dumps(act_ext.to_dict(), indent=2))
