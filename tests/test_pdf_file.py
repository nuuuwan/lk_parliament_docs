import os
import unittest

from tests.data.TEST_DATA_FOR_OCR import TEST_DATA_FOR_OCR
from utils_future import PDFFile

TEST_PDF_FILE = PDFFile(os.path.join("tests", "data", "image-2790.pdf"))


class TestCase(unittest.TestCase):

    def test_compress(self):
        compressed_pdf_file = TEST_PDF_FILE.compress()
        self.assertLessEqual(compressed_pdf_file.size, TEST_PDF_FILE.size)

    def test_ocr(self):  # noqa: CFQ001
        N_HEAD = 20
        a_list = []
        for (
            file_id,
            e_n_block_info_list,
            e_n_ocr_block_info_list,
            e_text_list_head,
        ) in TEST_DATA_FOR_OCR:

            pdf_file = PDFFile(
                os.path.join("tests", "data", f"{file_id}-en.pdf")
            )

            block_info_list = pdf_file.get_block_info_list()
            a_n_block_info_list = len(block_info_list)

            ocr_block_info_list = pdf_file.get_ocr_block_info_list()
            a_n_ocr_block_info_list = len(ocr_block_info_list)
            a_text_list_head = [
                d["text"] for d in ocr_block_info_list[:N_HEAD]
            ]

            a = [
                file_id,
                a_n_block_info_list,
                a_n_ocr_block_info_list,
                a_text_list_head,
            ]
            a_list.append(a)

        for e, a in zip(TEST_DATA_FOR_OCR, a_list):
            [
                file_id,
                e_n_block_info_list,
                e_n_ocr_block_info_list,
                e_text_list_head,
            ] = e
            [
                _,
                a_n_block_info_list,
                a_n_ocr_block_info_list,
                a_text_list_head,
            ] = a
            self.assertEqual(a_n_block_info_list, e_n_block_info_list)
            self.assertEqual(a_n_ocr_block_info_list, e_n_ocr_block_info_list)
            self.assertEqual(a_text_list_head, e_text_list_head)
