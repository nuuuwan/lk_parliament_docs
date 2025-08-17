import os
import unittest

from lk_acts import ActExt

TEST_PDF_PATH = os.path.join("tests", "input", "en.pdf")


class TestCase(unittest.TestCase):
    def test_from_pdf(self):
        act_ext = ActExt.from_pdf(TEST_PDF_PATH)
        print(act_ext.to_dict())
        self.assertEqual(
            act_ext.to_dict(),
            {
                "n_pages": 5,
                "title_page": {
                    "date_certified": "13th of  May, 2024",
                    "date_published": "May 17, 2024",
                    "price": "12.00",
                    "price_postage": "150.00",
                },
                "body_pages": {"section_list": []},
            },
        )
