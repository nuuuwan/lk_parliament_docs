# flake8: noqa
import os
import unittest

from lk_acts import ActExt

TEST_PDF_PATH = os.path.join("tests", "data", "en.pdf")


class TestCase(unittest.TestCase):
    def test_from_pdf(self):
        act_ext = ActExt.from_pdf(TEST_PDF_PATH)
        self.assertEqual(act_ext.n_pages, 5)
        self.assertEqual(act_ext.n_sections, 5)

        print(act_ext.title_page.to_dict())
        self.assertEqual(
            act_ext.title_page.to_dict(),
            {
                "title": "SHOP AND OFFICE EMPLOYEES (REGULATION OF EMPLOYMENT AND REMUNERATION) (AMENDMENT)  ACT",
                "num": "28",
                "year": "2024",
                "date_certified": "13th of  May, 2024",
                "date_published": "May 17, 2024",
                "price": "12.00",
                "price_postage": "150.00",
            },
        )

        first_section = act_ext.body_pages.section_list[0]
        print(first_section.to_dict())
        self.assertEqual(
            first_section.to_dict(),
            {
                "num": 1,
                "short_description": "Short title",
                "text": "This Act may be cited as the Shop and Office Employees (Regulation of Employment and Remuneration) (Amendment) Act, No.  28  of 2024.",
                "subsection_list": [],
                "inner_text_list": [],
            },
        )

        act_ext.write_md(os.path.join("tests", "data", "en.md"))
