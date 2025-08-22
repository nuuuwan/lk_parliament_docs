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
            e_first_ocr_block_info,
        ) in [
            [
                "image-2790",
                0,
                40,
                {
                    "i_page": 1,
                    "par_num": 1,
                    "text": "Ae sy geo abicay: \\ CESS - + PARLIAMENT OF THE DEMOCRATIC SOCIALIST REPUBLIC OF SRI LANKA APPROPRIATION ACT, No. 18 OF 1989 [Certified on 30th December 1989) Printed on the Orders of Government Published as a Supplement to Part Il of the Gazette of the Democratic Socialist Republic of Sri Lanka of January 05, 1990 YREITID A TRE THPAXTMMGET OY COWROIENNE PRIEEMG, £0 LATA 50 mi FORCEAKED AT IE OVEEROGGT? PURLECATIONS NUAELV, COUORO Price : Rs. 2.70 Postage : Rs. 3.10",  # noqa: E501
                    "mean_p_confidence": 0.68,
                },
            ]
        ]:
            pdf_path = os.path.join("tests", "data", f"{file_id}.pdf")
            pdf_file = PDFFile(pdf_path)
            block_info_list = pdf_file.get_block_info_list()
            self.assertEqual(len(block_info_list), e_n_block_info_list)

            ocr_block_info_list = pdf_file.get_ocr_block_info_list()
            self.assertEqual(len(ocr_block_info_list), e_n_ocr_block_info_list)
            first_ocr_block_info = ocr_block_info_list[0]
            print(first_ocr_block_info)
            self.assertEqual(
                first_ocr_block_info,
                e_first_ocr_block_info,
            )
