import os
from functools import cached_property

from utils import File, JSONFile, Log

from lk_acts.core.act.ActExtractText import ActExtractText
from utils_future import PDFFile

log = Log("ActExtractOCRText")


class ActExtractOCRText:
    MIN_OCR_BLOCK_TEXT_CHARS = ActExtractText.MIN_BLOCK_TEXT_CHARS

    @cached_property
    def ocr_block_info_list(self):
        return PDFFile(self.pdf_path).get_ocr_block_info_list()

    @cached_property
    def ocr_block_text(self):
        return "\n\n".join(
            [block_info["text"] for block_info in self.ocr_block_info_list]
        )

    @cached_property
    def is_ocr_block_text_valid(self):
        return (
            self.ocr_block_text
            and len(self.ocr_block_text) >= self.MIN_OCR_BLOCK_TEXT_CHARS
        )

    @cached_property
    def ocr_blocks_path(self):
        return os.path.join(self.dir_act_data, "ocr_blocks.json")

    @cached_property
    def has_ocr_blocks(self):
        return os.path.exists(self.ocr_blocks_path)

    @cached_property
    def ocr_blocks_fail_path(self):
        return os.path.join(self.dir_act_data, "ocr_blocks.json.fail")

    def extract_ocr_blocks(self):
        if not os.path.exists(self.pdf_path):
            return None
        if os.path.exists(self.ocr_blocks_path):
            return self.blocks_path
        if os.path.exists(self.ocr_blocks_fail_path):
            return None
        if not self.is_ocr_block_text_valid:
            File(self.ocr_blocks_fail_path).write("")
            log.debug(f"[{self}] ocr_block_text invalid.")
            return None

        ocr_block_info_list = self.ocr_block_info_list
        n_blocks = len(ocr_block_info_list)
        JSONFile(self.ocr_blocks_path).write(ocr_block_info_list)
        log.info(f"Wrote {self.ocr_blocks_path} ({n_blocks:,} OCR blocks)")
        return self.ocr_blocks_path

    @cached_property
    def ocr_text_path(self):
        return os.path.join(self.dir_act_data, "en.ocr.txt")

    @cached_property
    def has_ocr_text(self):
        return os.path.exists(self.ocr_text_path)

    @cached_property
    def ocr_text_fail_path(self):
        return os.path.join(self.dir_act_data, "en.ocr.txt.fail")

    def extract_ocr_text(self):
        if not os.path.exists(self.pdf_path):
            return None
        if os.path.exists(self.ocr_text_path):
            return self.ocr_text_path
        if os.path.exists(self.ocr_text_fail_path):
            return None
        if not self.is_ocr_block_text_valid:
            File(self.ocr_text_fail_path).write("")
            log.debug(f"[{self}] block_text invalid.")
            return None

        ocr_block_text = self.ocr_block_text
        n_chars = len(ocr_block_text)
        File(self.ocr_text_path).write(ocr_block_text)
        log.info(f"Wrote {self.ocr_text_path} ({n_chars:,} chars)")
        return self.ocr_text_path
