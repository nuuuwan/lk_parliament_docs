import unittest

from lpd import Doc


class TestCase(unittest.TestCase):
    def test_list_all(self):
        doc_list = Doc.list_all()
        self.assertGreater(len(doc_list), 0)
