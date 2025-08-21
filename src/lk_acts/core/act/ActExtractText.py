import os
from functools import cached_property

from utils import JSONFile, Log

from utils_future import PDFFile

log = Log("ActExtractText")


class ActExtractText:

    @cached_property
    def blocks_path(self):
        return os.path.join(self.dir_act_data, "blocks.json")

    def extract_blocks(self):
        if not os.path.exists(self.pdf_path):
            return None
        if os.path.exists(self.blocks_path):
            return self.blocks_path

        block_info_list = PDFFile(self.pdf_path).get_block_info_list()
        n_blocks = len(block_info_list)
        JSONFile(self.blocks_path).write(block_info_list)
        log.info(f"Wrote {self.blocks_path} ({n_blocks:,} blocks)")
        return self.blocks_path
