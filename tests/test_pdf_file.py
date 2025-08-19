import os
import unittest

from utils_future import PDFFile


class TestCase(unittest.TestCase):
    def test_ocr(self):
        pdf_file = PDFFile(os.path.join("tests", "data", "image.pdf"))
        output_pdf_file = pdf_file.ocr()
        self.assertTrue(os.path.exists(output_pdf_file.path))
