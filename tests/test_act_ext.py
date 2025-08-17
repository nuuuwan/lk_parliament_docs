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

        self.assertEqual(act_ext.n_pages, 72)

        self.assertEqual(len(act_ext.body_pages.pre_section_list), 2)
        self.assertEqual(len(act_ext.body_pages.part_list), 18)

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

        preamble = act_ext.body_pages.preamble
        print()
        print(preamble)
        print()
        self.assertEqual(
            preamble,
            [
                "[Certified On 08Th Of August, 2024]",
                "L.D.—O. 48/2023",
                "A N  A Ct   To   Make   Provisions   To   Strengthen   Accountability  ,",
                "Oversight ,  Management   And   Control   Of   Public   Funds   In   The P Ublic  F Inancial  M Anagement   Framework   With   The   View   To",
                "Improving  F Iscal  P Olicy   For   Better   Macroeconomic",
                "Management ;  To   Clarify   Institutional   Responsibilities   Related",
                "To  F Inancial  M Anagement ;  To   Strengthen   Budgetary",
                "Management ,  To   Facilitate   Public   Scrutiny   Of  F Iscal  P Olicy",
                "And   Performance ;  To   Repeal   The   Sections  8  And  14  Of  P Art   Ii",
                "Of   The  F Inance  A Ct , N O . 38  Of  1971;  To   Repeal   The  F Iscal M Anagement  (R Esponsibility ) A Ct , N O . 3  Of  2003  And   To",
                "Provide   For    Matters   Connected   Therewith   Or   Incidental",
                "Thereto .",
                "Be It Enacted By The Parliament Of The Democratic Socialist Republic Of Sri Lanka As Follows: -",
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
                        "text": "This Act may be cited as the Public Financial Management Act, No. 44 of 2024.",
                        "pre_block_list": [
                            "Short title and date of operation"
                        ],
                        "child_level_list": [],
                        "post_block_list": [],
                    },
                    {
                        "class_name": "ActL2Subsection",
                        "num": "2",
                        "text": "All the provisions of this Act other than the provisions specified in subsection (3), shall come into operation on the date on which the Bill becomes an Act of Parliament.",
                        "pre_block_list": [],
                        "child_level_list": [],
                        "post_block_list": [],
                    },
                    {
                        "class_name": "ActL2Subsection",
                        "num": "3",
                        "text": "The Minister of Finance shall for the implementation of the provisions specified in paragraphs ( a ) and ( b ) of this subsection, appoint such date or dates by Order published in the  Gazette  -",
                        "pre_block_list": [],
                        "child_level_list": [
                            {
                                "class_name": "ActL3Paragraph",
                                "num": "a",
                                "text": "the date or dates from which the provisions of paragraph ( f ) of subsection (5) of section 11, subsection (1) of section 17, paragraph ( b ) of subsection (2) of section 18, section 36 and paragraph ( a ) of subsection (1) of section 47 shall come into operation:",
                                "pre_block_list": [
                                    "Provided that, the provisions of paragraph ( f ) of subsection (5) of section 11 shall come into operation on a date not later than thirtieth day of June 2025; and"
                                ],
                                "child_level_list": [],
                                "post_block_list": [],
                            },
                            {
                                "class_name": "ActL3Paragraph",
                                "num": "b",
                                "text": "the date from which the provisions of subsection (2) of section 34 shall apply in respect of the entities specified in subparagraph (ii) of paragraph ( a ) of subsection (2) of section 3.",
                                "pre_block_list": ["Objects of the Act"],
                                "child_level_list": [],
                                "post_block_list": [],
                            },
                        ],
                        "post_block_list": [],
                    },
                ],
                "post_block_list": [],
            },
        )
