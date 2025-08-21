import os
from functools import cached_property

from utils import File, JSONFile, Log

from utils_future import PDFFile

log = Log("ActExtractText")


class ActExtractText:

    @cached_property
    def txt_path(self):
        return os.path.join(self.dir_act_data, "en.txt")

    def extract_text(self):
        if os.path.exists(self.txt_path):
            return self.txt_path
        if not os.path.exists(self.pdf_path):
            return None
        try:
            text = PDFFile(self.pdf_path).get_text()
            File(self.txt_path).write(text)
            log.info(f"Wrote {self.txt_path} ({len(text):,} chars)")
        except Exception as e:
            log.error(f"[{self}] {e}")
            return None

    @cached_property
    def blocks_path(self):
        return os.path.join(self.dir_act_data, "blocks.json")

    def extract_blocks(self):
        if not os.path.exists(self.pdf_path):
            return None
        if os.path.exists(self.blocks_path):
            return self.blocks_path

        blocks_info_list = PDFFile(self.pdf_path).get_blocks_info_list()
        n_blocks = len(blocks_info_list)
        JSONFile(self.blocks_path).write(blocks_info_list)
        log.info(f"Wrote {self.blocks_path} ({n_blocks:,} blocks)")
        return self.blocks_path
