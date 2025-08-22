import os
from functools import cached_property

from utils import Log

from lk_acts.core.act.ActExtractText import ActExtractText
from utils_future import DataFile, PDFFile

log = Log("ActExtractOCRText")


class ActExtractOCRText:
    MIN_OCR_BLOCK_TEXT_CHARS = ActExtractText.MIN_BLOCK_TEXT_CHARS

    # ocr_blocks

    @cached_property
    def data_file_ocr_blocks(self):
        return DataFile(
            self,
            lambda obj: os.path.join(obj.dir_act_data, "ocr_blocks.json"),
            lambda obj: (
                PDFFile(obj.pdf_path).get_ocr_block_info_list()
                if PDFFile(obj.pdf_path).exists
                else None
            ),
        )

    @cached_property
    def ocr_block_info_list(self):
        return self.data_file_ocr_blocks.data

    @cached_property
    def has_ocr_blocks(self):
        return self.data_file_ocr_blocks.exists

    def extract_ocr_blocks(self):
        self.ocr_block_info_list

    # ocr_block_text

    @cached_property
    def data_file_ocr_block_text(self):
        return DataFile(
            self,
            lambda obj: os.path.join(obj.dir_act_data, "en.ocr.txt"),
            lambda obj: (
                "\n\n".join(
                    [
                        block_info["text"]
                        for block_info in obj.ocr_block_info_list
                    ]
                )
                if obj.ocr_block_info_list
                else None
            ),
        )

    @cached_property
    def ocr_block_text(self):
        return self.data_file_ocr_block_text.data

    @cached_property
    def is_ocr_block_text_valid(self):
        return (
            self.ocr_block_text
            and len(self.ocr_block_text) >= self.MIN_OCR_BLOCK_TEXT_CHARS
        )

    @cached_property
    def has_ocr_text(self):
        return self.data_file_ocr_block_text.exists

    def extract_ocr_text(self):
        self.ocr_block_text

    # -----

    @cached_property
    def has_some_text(self):
        return self.has_text or self.has_ocr_text

    @cached_property
    def some_text(self):
        return self.block_text or self.ocr_block_text or None
