import os
import unittest

from lk_acts import Act

TEST_ACT = Act.list_all()[0]


class TestCase(unittest.TestCase):

    def test_to_dict(self):
        self.assertEqual(
            TEST_ACT.to_dict(),
            {
                "num": "14/2025",
                "date": "2025-08-18",
                "description": "Sri Lanka Electricity (Amendment)",
                "url_pdf_en": "https://www.parliament.lk/uploads/acts/gbills/english/6385.pdf",  # noqa: E501
                "act_id": "2025-014",
                "act_type": "Amendment",
            },
        )

    def test_write(self):
        TEST_ACT.write()
        self.assertTrue(os.path.exists(TEST_ACT.metadata_json_path))

    def test_list_all(self):
        doc_list = Act.list_all()
        self.assertGreaterEqual(len(doc_list), 0)
