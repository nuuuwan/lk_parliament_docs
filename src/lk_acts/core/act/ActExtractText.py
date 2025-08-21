import os
from functools import cached_property

from utils import File, JSONFile, Log

from utils_future import PDFFile

log = Log("ActExtractText")


class ActExtractText:
    MIN_BLOCK_TEXT_CHARS = 100

    @cached_property
    def block_info_list(self):
        return PDFFile(self.pdf_path).get_block_info_list()

    @cached_property
    def block_text(self):
        return "\n\n".join(
            [block_info["text"] for block_info in self.block_info_list]
        )

    @cached_property
    def is_block_text_valid(self):
        return (
            self.block_text
            and len(self.block_text) >= self.MIN_BLOCK_TEXT_CHARS
        )

    @cached_property
    def blocks_path(self):
        return os.path.join(self.dir_act_data, "blocks.json")

    @cached_property
    def block_fail_path(self):
        return os.path.join(self.dir_act_data, "blocks.json.fail")

    def extract_blocks(self):
        if not os.path.exists(self.pdf_path):
            return None
        if os.path.exists(self.blocks_path):
            return self.blocks_path
        if os.path.exists(self.block_fail_path):
            return None
        if not self.is_block_text_valid:
            File(self.block_fail_path).write("")
            log.debug(f"[{self}] block_Text invalid.")
            return None

        block_info_list = self.block_info_list
        n_blocks = len(block_info_list)
        JSONFile(self.blocks_path).write(block_info_list)
        log.info(f"Wrote {self.blocks_path} ({n_blocks:,} blocks)")
        return self.blocks_path

    @cached_property
    def text_path(self):
        return os.path.join(self.dir_act_data, "en.txt")

    @cached_property
    def text_fail_path(self):
        return os.path.join(self.dir_act_data, "en.txt.fail")

    def extract_text(self):
        if not os.path.exists(self.pdf_path):
            return None
        if os.path.exists(self.text_path):
            return self.text_path
        if os.path.exists(self.text_fail_path):
            return None
        if not self.is_block_text_valid:
            File(self.text_fail_path).write("")
            log.debug(f"[{self}] block_text invalid.")
            return None

        block_text = self.block_text
        n_chars = len(block_text)
        File(self.text_path).write(block_text)
        log.info(f"Wrote {self.text_path} ({n_chars:,} chars)")
        return self.text_path
