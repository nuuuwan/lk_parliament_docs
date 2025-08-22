import os
from functools import cached_property

from utils import Log

from utils_future import DataFile, PDFFile

log = Log("ActExtractText")


class ActExtractText:
    MIN_BLOCK_TEXT_CHARS = 100

    # block_info_list

    @cached_property
    def data_file_block_info_list(self):
        return DataFile(
            self,
            lambda obj: os.path.join(self.dir_act_data, "blocks.json"),
            lambda obj: (
                PDFFile(self.pdf_path).get_block_info_list()
                if PDFFile(self.pdf_path).exists
                else None
            ),
        )

    @cached_property
    def block_info_list(self):
        return self.data_file_block_info_list.data

    @cached_property
    def has_blocks(self):
        return self.data_file_block_info_list.exists

    def extract_blocks(self):
        self.data_file_block_info_list.data

    # block_text

    @cached_property
    def data_file_block_text(self):
        return DataFile(
            self,
            lambda obj: os.path.join(self.dir_act_data, "en.txt"),
            lambda obj: (
                "\n\n".join(
                    [block_info["text"] for block_info in self.block_info_list]
                )
                if self.block_info_list
                else None
            ),
        )

    @cached_property
    def block_text(self):
        return self.data_file_block_text.data

    @cached_property
    def is_block_text_valid(self):
        return (
            self.block_text
            and len(self.block_text) >= self.MIN_BLOCK_TEXT_CHARS
        )

    @cached_property
    def has_text(self):
        return self.data_file_block_text.exists

    def extract_text(self):
        self.data_file_block_text.data
