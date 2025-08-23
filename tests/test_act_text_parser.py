# flake8: noqa E501
import unittest

from lk_acts import Act


class TestCase(unittest.TestCase):

    def test_parse(self):
        for act_id, expected_d in [
            [
                "2025-001",
                {
                    "name": "Local Authorities Elections(Special Provisions)Act",
                    "number": 1,
                    "year": 2025,
                    "date": "2025-02-17",
                    "published_as": "A Supplement To Part Ii Of The Gazette Of The Democraticsocialist Republic Of Sri Lanka Of February 21, 2025",
                    "price": 35.0,
                    "price_postage": 150.0,
                },
            ]
        ]:
            act = Act.from_id(act_id)
            self.assertEqual(act.parse_text(), expected_d)

    # def test_parse_all(self):
    #     for act in Act.list_all():
    #         act.parse_text()
