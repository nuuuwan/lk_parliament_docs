# flake8: noqa E501
import unittest

from lk_acts import Act


class TestCase(unittest.TestCase):

    def test_parse(self):
        for act_id, expected_d in [
            [
                "2025-001",
                {
                    "act_name": "Local Authorities Elections(Special Provisions)Act",
                    "act_number": 1,
                    "act_year": 2025,
                    "date_certified": "2025-02-17",
                    "published_as": "A Supplement To Part Ii Of The Gazette Of The Democraticsocialist Republic Of Sri Lanka Of February 21, 2025",
                    "price": 35.0,
                    "price_postage": 150.0,
                },
            ],
            [
                "2020-001",
                {
                    "date_certified": "2020-02-26",
                    "price": 16.0,
                    "price_postage": 15.0,
                    "published_as": "A Supplement To Part Ii Of The Gazette Of The Democraticsocialist Republic Of Sri Lanka Of February 28, 2020",
                    "act_name": "Institute Of Environmentalprofessionals, Sri Lanka (Incorporation)Act",
                    "act_number": 1,
                    "act_year": 2020,
                },
            ],
            [
                "2010-007",
                {
                    "price": 35.0,
                    "price_postage": 12.5,
                    "published_as": "A Supplement To Part Ii Of The Gazette Of The Democraticsocialist Republic Of Sri Lanka Of July 16, 2010",
                    "date_certified": "2010-07-13",
                    "act_name": "Appropriation Act",
                    "act_number": 7,
                    "act_year": 2010,
                },
            ],
        ]:
            act = Act.from_id(act_id)
            actual_d = act.parse_text()
            if actual_d != expected_d:
                print()
                print(act_id)
                print(actual_d)
                print("-" * 80)
            self.assertEqual(actual_d, expected_d)

    # def test_parse_all(self):
    #     for act in Act.list_all():
    #         act.parse_text()
