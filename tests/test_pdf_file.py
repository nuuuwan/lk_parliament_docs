import os
import unittest

from utils_future import PDFFile

TEST_PDF_FILE = PDFFile(os.path.join("tests", "data", "image-2790.pdf"))


class TestCase(unittest.TestCase):

    def test_compress(self):
        compressed_pdf_file = TEST_PDF_FILE.compress()
        self.assertLessEqual(compressed_pdf_file.size, TEST_PDF_FILE.size)

    def test_get_ocr_block_info_list(self):

        for (
            file_id,
            e_n_block_info_list,
            e_n_ocr_block_info_list,
            e_text_list_10,
        ) in [
            [
                "image-2790",
                0,
                901,
                [
                    "",
                    "",
                    "",
                    " Ae",
                    " sy geo",
                    " abicay: \\",
                    " CESS",
                    " - + PARLIAMENT OF THE DEMOCRATIC",
                    " SOCIALIST REPUBLIC OF",
                    " SRI LANKA",
                ],
            ]
        ]:
            pdf_path = os.path.join("tests", "data", f"{file_id}.pdf")
            pdf_file = PDFFile(pdf_path)
            block_info_list = pdf_file.get_block_info_list()
            self.assertEqual(len(block_info_list), e_n_block_info_list)

            ocr_block_info_list = pdf_file.get_ocr_block_info_list()

            text_list_10 = [d["text"] for d in ocr_block_info_list[:10]]
            print(text_list_10)
            self.assertEqual(
                text_list_10,
                e_text_list_10,
            )

            self.assertEqual(len(ocr_block_info_list), e_n_ocr_block_info_list)
