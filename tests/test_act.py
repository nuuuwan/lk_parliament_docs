import unittest

from lk_acts import Act


class TestCase(unittest.TestCase):
    def test_list_all(self):
        doc_list = Act.list_all()
        self.assertGreaterEqual(len(doc_list), 0)
