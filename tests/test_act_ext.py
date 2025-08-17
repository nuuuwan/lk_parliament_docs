import os
import unittest

from lk_acts import ActExt

TEST_PDF_PATH = os.path.join("tests", "input", "en.pdf")


class TestCase(unittest.TestCase):
    def test_from_pdf(self):
        act_ext = ActExt.from_pdf(TEST_PDF_PATH)
        print(act_ext)

        self.assertEqual(act_ext.n_pages, 5)
        self.assertEqual(act_ext.date_certified, "13th of  May, 2024")
        self.assertEqual(act_ext.date_published, "May 17, 2024")

        self.assertEqual(act_ext.price, "12.00")
        self.assertEqual(act_ext.price_postage, "150.00")
