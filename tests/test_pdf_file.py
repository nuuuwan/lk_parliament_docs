import os
import unittest

from utils import File

from utils_future import PDFFile

TEST_PDF_FILE = PDFFile(os.path.join("tests", "data", "image-0073.pdf"))


class TestCase(unittest.TestCase):

    def test_get_raw_text(self):
        text = TEST_PDF_FILE.get_raw_text()
        self.assertGreater(len(text), 100)

    def test_get_block_text(self):
        text = TEST_PDF_FILE.get_block_text()
        self.assertGreater(len(text), 100)

    def test_get_block_info_list(self):
        block_info_list = TEST_PDF_FILE.get_block_info_list()
        first_block_info = block_info_list[0]
        self.assertEqual(
            first_block_info,
            {
                "page_number": 0,
                "bbox": (63.11, 155.46, 359.21, 216.89),
                "fonts": ["*Times New Roman-Bold-4790"],
                "sizes": [17.0],
                "text": "PARLIAMENT OF THE DEMOCRATIC SOCIALIST REPUBLIC OF SRI LANKA",
            },
        )

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

    def test_get_image_block_info_list(self):
        image_block_info_list = TEST_PDF_FILE.get_image_block_info_list()
        self.assertEqual(len(image_block_info_list), 124)
