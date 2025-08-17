# flake8: noqa
import os
import unittest

from lk_acts import ActExt

TEST_PDF_PATH = os.path.join("tests", "data", "en.pdf")


class TestCase(unittest.TestCase):
    def test_from_pdf(self):
        act_ext = ActExt.from_pdf(TEST_PDF_PATH)
        self.assertEqual(act_ext.n_pages, 72)
        self.assertEqual(act_ext.n_sections, 71)
        print()
        print(act_ext.title_page.to_dict())
        print()
        self.assertEqual(
            act_ext.title_page.to_dict(),
            {
                "title": "Public Financial Management Act",
                "num": "44",
                "year": "2024",
                "date_certified": "2024-08-08",
                "date_published": "2024-08-09",
                "price": 114.0,
                "price_postage": 150.0,
            },
        )

        first_section = act_ext.body_pages.section_list[0]
        print()
        print(first_section.to_dict())
        print()
        self.assertEqual(
            first_section.to_dict(),
            {
                "num": 1,
                "short_description": "Short title and date of operation",
                "text": "",
                "subsection_list": [
                    {
                        "num": 1,
                        "text": "This Act may be cited as the Public Financial Management Act, No. 44 of 2024.",
                        "inner_text_list": [],
                    },
                    {
                        "num": 2,
                        "text": "All the provisions of this Act other than the provisions specified in subsection (3), shall come into operation on the date on which the Bill becomes an Act of Parliament.",
                        "inner_text_list": [],
                    },
                    {
                        "num": 3,
                        "text": "The Minister of Finance shall for the implementation of the provisions specified in paragraphs ( a ) and ( b ) of this subsection, appoint such date or dates by Order published in the  Gazette  -",
                        "inner_text_list": [
                            "( a ) the date or dates from which the provisions of paragraph ( f ) of subsection (5) of section 11, subsection (1) of section 17, paragraph ( b ) of subsection (2) of section 18, section 36 and paragraph ( a ) of subsection (1) of section 47 shall come into operation:",
                            "Provided that, the provisions of paragraph ( f ) of subsection (5) of section 11 shall come into operation on a date not later than thirtieth day of June 2025; and",
                            "( b ) the date from which the provisions of subsection (2) of section 34 shall apply in respect of the entities specified in subparagraph (ii) of paragraph ( a ) of subsection (2) of section 3.",
                        ],
                    },
                ],
                "inner_text_list": [],
            },
        )

        act_ext.write_md(os.path.join("tests", "data", "en.md"))
        act_ext.write_json(os.path.join("tests", "data", "en.json"))
