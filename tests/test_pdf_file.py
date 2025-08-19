import os
import unittest

from utils_future import PDFFile

TEST_PDF_FILE = PDFFile(os.path.join("tests", "data", "image.pdf"))


class TestCase(unittest.TestCase):
    def test_get_image_text(self):

        text = TEST_PDF_FILE.get_image_text()
        self.assertEqual(len(text), 20_542)
