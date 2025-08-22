import os
import unittest

from utils_future import PDFFile

TEST_PDF_FILE = PDFFile(os.path.join("tests", "data", "image-2790.pdf"))


class TestCase(unittest.TestCase):

    def test_compress(self):
        compressed_pdf_file = TEST_PDF_FILE.compress()
        self.assertLessEqual(compressed_pdf_file.size, TEST_PDF_FILE.size)

    def test_get_ocr_block_info_list(self):
        block_info_list = TEST_PDF_FILE.get_block_info_list()
        self.assertEqual(len(block_info_list), 0)

        ocr_block_info_list = TEST_PDF_FILE.get_ocr_block_info_list()
        self.assertEqual(len(ocr_block_info_list), 40)
        first_ocr_block_info = ocr_block_info_list[0]
        print(first_ocr_block_info)
        self.assertEqual(
            first_ocr_block_info,
            {
                "i_page": 1,
                "par_num": 1,
                "text": "Ae sy geo abicay: \\ CESS - + PARLIAMENT OF THE DEMOCRATIC SOCIALIST REPUBLIC OF SRI LANKA APPROPRIATION ACT, No. 18 OF 1989 [Certified on 30th December 1989) Printed on the Orders of Government Published as a Supplement to Part Il of the Gazette of the Democratic Socialist Republic of Sri Lanka of January 05, 1990 YREITID A TRE THPAXTMMGET OY COWROIENNE PRIEEMG, £0 LATA 50 mi FORCEAKED AT IE OVEEROGGT? PURLECATIONS NUAELV, COUORO Price : Rs. 2.70 Postage : Rs. 3.10",  # noqa: E501
                "mean_p_confidence": 0.68,
            },
        )
