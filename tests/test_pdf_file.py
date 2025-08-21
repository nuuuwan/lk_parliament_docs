import os
import unittest

from utils_future import PDFFile

TEST_PDF_FILE = PDFFile(os.path.join("tests", "data", "image-0073.pdf"))


class TestCase(unittest.TestCase):

    def test_compress(self):
        compressed_pdf_file = TEST_PDF_FILE.compress()
        self.assertLessEqual(compressed_pdf_file.size, TEST_PDF_FILE.size)

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
                "text": "PARLIAMENT OF THE DEMOCRATIC"
                + " SOCIALIST REPUBLIC OF SRI LANKA",
            },
        )

    def test_get_image_block_info_list(self):
        image_block_info_list = TEST_PDF_FILE.get_image_block_info_list()
        self.assertEqual(len(image_block_info_list), 182)
