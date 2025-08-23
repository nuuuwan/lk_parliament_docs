import os
import unittest

from lk_acts import PageActsBills


class TestCase(unittest.TestCase):
    @unittest.skip("Slow")
    def test_scrape(self):
        page = PageActsBills("acts", "2023")
        doc_list = page.scrape()
        self.assertEqual(len(doc_list), 43)

        first_doc = doc_list[0]
        self.assertEqual(
            first_doc.to_dict(),
            {
                "num": "28/2024",
                "date": "2024-05-13",
                "description": "Shop and Office Employees (Regulation of Employment and Remuneration) (Amendment)",  # noqa: E501
                "url_pdf_en": "https://www.parliament.lk/uploads/acts/gbills/english/6332.pdf",  # noqa: E501,
                "act_id": "2024-028",
                "act_type": "Amendment",
            },
        )
        self.assertTrue(os.path.exists(first_doc.metadata_json_path))
