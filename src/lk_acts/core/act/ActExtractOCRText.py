import os
from functools import cached_property

from utils import JSONFile, Log

from utils_future import PDFFile

log = Log("ActExtractOCRText")


class ActExtractOCRText:

    @cached_property
    def ocr_blocks_path(self):
        return os.path.join(self.dir_act_data, "ocr_blocks.json")

    def extract_ocr_blocks(self):
        if not os.path.exists(self.pdf_path):
            return None
        if os.path.exists(self.ocr_blocks_path):
            return self.blocks_path

        ocr_block_info_list = PDFFile(self.pdf_path).get_ocr_block_info_list()
        n_blocks = len(ocr_block_info_list)
        JSONFile(self.ocr_blocks_path).write(ocr_block_info_list)
        log.info(f"Wrote {self.ocr_blocks_path} ({n_blocks:,} OCR blocks)")
        return self.ocr_blocks_path
