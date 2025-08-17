# flake8: noqa
import os
import unittest

from lk_acts import ActExt

TEST_PDF_PATH = os.path.join("tests", "data", "en.pdf")


class TestCase(unittest.TestCase):
    def test_from_pdf(self):
        act_ext = ActExt.from_pdf(TEST_PDF_PATH)
        act_ext.write_md(TEST_PDF_PATH[:-4] + ".md")
        act_ext.write_json(TEST_PDF_PATH[:-4] + ".json")

        self.assertEqual(act_ext.n_pages, 31)

        self.assertEqual(len(act_ext.body_pages.pre_section_list), 12)
        self.assertEqual(len(act_ext.body_pages.part_list), 0)

        print()
        print(act_ext.title_page.to_dict())
        print()
        self.assertEqual(
            act_ext.title_page.to_dict(),
            {
                "title": "Companies (Amendment) Act",
                "num": "12",
                "year": "2025",
                "date_certified": "2025-08-04",
                "date_published": "2025-08-07",
                "price": 80.0,
                "price_postage": 150.0,
            },
        )

        preamble = act_ext.body_pages.preamble
        print()
        print(preamble)
        print()
        self.assertEqual(
            preamble,
            [
                "Companies (Amendment) Act, No. 12 Of 2025 1",
                "[Certiﬁ Ed On 04Th Of August, 2025]",
                "L.D.- O. 61/2024",
                "A N   A Ct   To   Amend   The  C Ompanies  A Ct , N O . 07  Of  2007",
                "Be It Enacted By The Parliament Of The Democratic Socialist  Republic Of Sri Lanka As Follows: -",
            ],
        )

        section = act_ext.body_pages.pre_section_list[0]
        print()
        print(section.to_dict())
        print()
        self.assertEqual(
            section.to_dict(),
            {
                "class_name": "ActL1Section",
                "num": "1",
                "text": "",
                "pre_block_list": [],
                "child_level_list": [
                    {
                        "class_name": "ActL2Subsection",
                        "num": "1",
                        "text": "This Act may be cited as the Companies  (Amendment) Act, No. 12 of 2025. ",
                        "pre_block_list": [
                            "Short title and the  date of operation"
                        ],
                        "child_level_list": [],
                        "post_block_list": [],
                    },
                    {
                        "class_name": "ActL2Subsection",
                        "num": "2",
                        "text": "The provisions of this Act other than the provisions  of this section shall come into operation on such date as the  Minister may appoint by Order published in the  Gazette . ",
                        "pre_block_list": [],
                        "child_level_list": [],
                        "post_block_list": [],
                    },
                    {
                        "class_name": "ActL2Subsection",
                        "num": "3",
                        "text": "The provisions of this section shall come into operation  on the date on which the Bill becomes an Act of Parliament.",
                        "pre_block_list": [],
                        "child_level_list": [],
                        "post_block_list": [],
                    },
                ],
                "post_block_list": [],
            },
        )
