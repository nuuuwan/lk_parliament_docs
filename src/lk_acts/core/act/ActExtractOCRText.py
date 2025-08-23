import os
from functools import cache, cached_property

from utils import Log

from lk_acts.core.act.ActExtractText import ActExtractText
from utils_future import DataFile, PDFFile

log = Log("ActExtractOCRText")


class ActExtractOCRText:
    MIN_OCR_BLOCK_TEXT_CHARS = ActExtractText.MIN_BLOCK_TEXT_CHARS

    @cached_property
    def dir_act_data(self):
        raise NotImplementedError  # ActBase

    @cached_property
    def pdf_path(self):
        raise NotImplementedError  # ActDownloadPDF

    @cached_property
    def text(self):
        raise NotImplementedError  # ActExtractText

    # ocr_blocks
    @cached_property
    def data_file_ocr_blocks(self):
        return DataFile(
            lambda: os.path.join(self.dir_act_data, "ocr_blocks.json"),
            lambda: (
                PDFFile(self.pdf_path).get_ocr_block_info_list()
                if PDFFile(self.pdf_path).exists
                else None
            ),
        )

    @cached_property
    def ocr_blocks_path(self):
        return self.data_file_ocr_blocks.path

    @cached_property
    def ocr_blocks_fail_path(self):
        return self.data_file_ocr_blocks.path_fail

    @cached_property
    def ocr_block_info_list(self):
        return self.data_file_ocr_blocks.data

    @cached_property
    def has_ocr_blocks(self):
        return self.data_file_ocr_blocks.exists

    def extract_ocr_blocks(self):
        return self.ocr_block_info_list

    # ocr_text
    @cached_property
    def data_file_ocr_text(self):
        return DataFile(
            lambda: os.path.join(self.dir_act_data, "en.ocr.txt"),
            lambda: (
                "\n\n".join(
                    [
                        block_info["text"]
                        for block_info in self.ocr_block_info_list
                    ]
                )
                if self.ocr_block_info_list
                else None
            ),
        )

    @cached_property
    def ocr_text_path(self):
        return self.data_file_ocr_text.path

    @cached_property
    def ocr_text_fail_path(self):
        return self.data_file_ocr_text.path_fail

    @cached_property
    def ocr_text(self):
        return self.data_file_ocr_text.data

    @cached_property
    def is_ocr_text_valid(self):
        return (
            self.ocr_text
            and len(self.ocr_text) >= self.MIN_OCR_BLOCK_TEXT_CHARS
        )

    @cached_property
    def has_ocr_text(self):
        return self.data_file_ocr_text.exists

    def extract_ocr_text(self):
        return self.ocr_text

    @cache
    def get_ocr_block_info_list(self, min_mean_p_confidence=-1):
        return (
            [
                block_info
                for block_info in self.ocr_block_info_list
                if block_info["mean_p_confidence"] >= min_mean_p_confidence
            ]
            if self.ocr_block_info_list
            else []
        )

    @cache
    def get_ocr_text(self, min_mean_p_confidence=-1):
        return "\n\n".join(
            [
                block_info["text"]
                for block_info in self.get_ocr_block_info_list(
                    min_mean_p_confidence=min_mean_p_confidence
                )
            ]
        )

    # common text

    @cache
    def get_text(self, min_mean_p_confidence=-1):
        return (
            self.text
            or self.get_ocr_text(min_mean_p_confidence=min_mean_p_confidence)
            or None
        )
