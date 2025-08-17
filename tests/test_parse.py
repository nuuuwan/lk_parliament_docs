import unittest

from utils_future import Parse


class TestCase(unittest.TestCase):
    def test_float(self):
        for x, expected_float in [
            (0, 0.0),
            (1, 1.0),
            (100.01, 100.01),
            ("10.0", 10.0),
            ("hello", None),
        ]:
            self.assertEqual(Parse.float(x), expected_float)

    def test_date(self):
        for x, expected_date in [
            ("2023-01-01", "2023-01-01"),
            ("01/01/2023", "2023-01-01"),
            ("January 1, 2023", "2023-01-01"),
            ("hello", None),
            ("13th of  May, 2024", "2024-05-13"),
            ("May 17, 2024", "2024-05-17"),
        ]:
            self.assertEqual(Parse.date(x), expected_date)
