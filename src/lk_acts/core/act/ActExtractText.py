import os
from functools import cached_property

from utils import File, JSONFile, Log

from utils_future import PDFFile

log = Log("ActExtractText")


class ActExtractText:

    @cached_property
    def blocks_path(self):
        return os.path.join(self.dir_act_data, "blocks.json")

    @cached_property
    def block_info_list(self):
        return PDFFile(self.pdf_path).get_block_info_list()

    def extract_blocks(self):
        if not os.path.exists(self.pdf_path):
            return None
        if os.path.exists(self.blocks_path):
            return self.blocks_path

        block_info_list = self.block_info_list
        n_blocks = len(block_info_list)
        JSONFile(self.blocks_path).write(block_info_list)
        log.info(f"Wrote {self.blocks_path} ({n_blocks:,} blocks)")
        return self.blocks_path

    @cached_property
    def text_path(self):
        return os.path.join(self.dir_act_data, "en.txt")

    @cached_property
    def block_text(self):
        return "\n\n".join(
            [block_info["text"] for block_info in self.block_info_list]
        )

    def extract_text(self):
        if not os.path.exists(self.pdf_path):
            return None
        if os.path.exists(self.text_path):
            return self.text_path

        block_text = self.block_text
        n_chars = len(block_text)
        File(self.text_path).write(self.block_text)
        log.info(f"Wrote {self.text_path} ({n_chars:,} chars)")
        return self.text_path
