import os
import unittest

from utils import File

from utils_future import PDFFile

TEST_PDF_FILE = PDFFile(os.path.join("tests", "data", "image-0073.pdf"))


class TestCase(unittest.TestCase):
    def test_get_image_text(self):
        image_text = TEST_PDF_FILE.get_image_text()
        self.assertGreater(len(image_text), 1_000)

    def test_compress(self):
        compressed_pdf_file = TEST_PDF_FILE.compress()
        self.assertLessEqual(compressed_pdf_file.size, TEST_PDF_FILE.size)

    def test_get_text_content_with_compress(self):
        compressed_pdf_file = TEST_PDF_FILE.compress()

        image_text_from_compressed = compressed_pdf_file.get_image_text()
        self.assertGreater(len(image_text_from_compressed), 1_000)

        image_text_from_uncompressed = TEST_PDF_FILE.get_image_text()

        File(os.path.join("tests", "data", "image_compressed.txt")).write(
            image_text_from_compressed
        )
        File(os.path.join("tests", "data", "image_uncompressed.txt")).write(
            image_text_from_uncompressed
        )

        ratio = len(image_text_from_compressed) / len(
            image_text_from_uncompressed
        )
        self.assertGreater(ratio, 0.9)
