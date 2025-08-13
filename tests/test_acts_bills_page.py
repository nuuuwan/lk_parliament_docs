import unittest

from lpd import ActsBillsPage


class TestCase(unittest.TestCase):
    @unittest.skip("Skipping test for ActsBillsPage")
    def test_get_doc_list_for_acts(self):
        page = ActsBillsPage("2024", "acts")
        doc_list = page.get_doc_list()
        self.assertEqual(len(doc_list), 17)

        first_doc = doc_list[0]
        self.assertEqual(
            first_doc,
            {
                "doc_type_name": "acts",
                "date": "2024-09-13",
                "description": "Code of Criminal Procedure (Amendment)",
                "endorsed_date": "2024-09-13",
                "lang_to_source_url": {
                    "en": "https://www.parliament.lk/uploads/acts/gbills/english/6359.pdf",  # noqa: E501
                    "si": "https://www.parliament.lk/uploads/acts/gbills/sinhala/6359.pdf",  # noqa: E501
                    "ta": "https://www.parliament.lk/uploads/acts/gbills/tamil/6359.pdf",  # noqa: E501
                },
                "doc_num": "50/2024",
                "doc_id": "50-2024",
            },
        )

    def test_get_doc_list_for_bills(self):
        page = ActsBillsPage("2024", "bills")
        doc_list = page.get_doc_list()
        self.assertEqual(len(doc_list), 17)

        first_doc = doc_list[0]
        print(first_doc)

        self.assertEqual(
            first_doc,
            {
                "doc_type_name": "bills",
                "date": "2024-09-13",
                "description": "Code of Criminal Procedure (Amendment)",
                "endorsed_date": "2024-09-13",
                "lang_to_source_url": {
                    "en": "https://www.parliament.lk/uploads/acts/gbills/english/6359.pdf",
                    "si": "https://www.parliament.lk/uploads/acts/gbills/sinhala/6359.pdf",
                    "ta": "https://www.parliament.lk/uploads/acts/gbills/tamil/6359.pdf",
                },
                "doc_num": "50/2024",
                "doc_id": "50-2024",
            },
        )
