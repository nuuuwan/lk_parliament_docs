import os
import unittest

from lpd import ActsBillsPage


class TestCase(unittest.TestCase):
    @unittest.skip("Slow")
    def test_scrape(self):
        page = ActsBillsPage("acts", "2023")
        doc_list = page.scrape()
        self.assertEqual(len(doc_list), 43)

        first_doc = doc_list[0]
        self.assertEqual(
            first_doc.to_dict(),
            {
                "doc_type_nam": "acts",
                "doc_num": "28/2024",
                "date": "2024-05-13",
                "description": "Shop and Office Employees (Regulation of Employment and Remuneration) (Amendment)",  # noqa: E501
                "lang_to_source_url": {
                    "en": "https://www.parliament.lk/uploads/acts/gbills/english/6332.pdf",  # noqa: E501
                    "si": "https://www.parliament.lk/uploads/acts/gbills/sinhala/6332.pdf",  # noqa: E501
                    "ta": "https://www.parliament.lk/uploads/acts/gbills/tamil/6332.pdf",  # noqa: E501
                },
                "doc_id": "28-2024",
            },
        )
        self.assertTrue(os.path.exists(first_doc.metadata_json_path))
