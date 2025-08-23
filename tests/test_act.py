import unittest

from lk_acts import Act


class TestCase(unittest.TestCase):
    def test_list_all(self):
        doc_list = Act.list_all()
        self.assertGreaterEqual(len(doc_list), 0)

    def test_first_act(self):
        first_act = Act.list_all()[0]
        self.assertEqual(
            first_act.to_dict(),
            {
                "num": "14/2025",
                "date": "2025-08-18",
                "description": "Sri Lanka Electricity (Amendment)",
                "url_pdf_en": "https://www.parliament.lk/uploads/acts/gbills/english/6385.pdf",
                "act_id": "2025-014",
                "act_type": "Amendment",
            },
        )
