# flake8: noqa
import os
import unittest

from lk_acts import ActExt

TEST_PDF_PATH = os.path.join("tests", "input", "en.pdf")


class TestCase(unittest.TestCase):
    def test_from_pdf(self):
        act_ext = ActExt.from_pdf(TEST_PDF_PATH)
        self.assertEqual(act_ext.n_pages, 5)
        self.assertEqual(act_ext.n_sections, 5)

        first_section = act_ext.body_pages.section_list[0]
        print(first_section.to_dict())
        self.assertEqual(
            first_section.to_dict(),
            {
                "num": 1,
                "short_description": "Short title",
                "text": "This Act may be cited as the Shop and Office Employees (Regulation of Employment and Remuneration) (Amendment) Act, No.  28  of 2024.",
                "sub_section_list": [],
            },
        )
