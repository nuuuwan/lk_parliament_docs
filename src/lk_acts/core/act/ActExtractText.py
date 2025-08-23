import os
from functools import cached_property

from utils import Log

from utils_future import DataFile, PDFFile

log = Log("ActExtractText")


class ActExtractText:
    MIN_BLOCK_TEXT_CHARS = 100

    @cached_property
    def dir_act_data(self):
        raise NotImplementedError

    @cached_property
    def pdf_path(self):
        raise NotImplementedError

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
    def blocks_path(self):
        return self.data_file_block_info_list.path

    @cached_property
    def blocks_fail_path(self):
        return self.data_file_block_info_list.path_fail

    @cached_property
    def block_info_list(self):
        return self.data_file_block_info_list.data

    @cached_property
    def has_blocks(self):
        return self.data_file_block_info_list.exists

    def extract_blocks(self):
        return self.data_file_block_info_list.data

    # text

    @cached_property
    def data_file_text(self):
        return DataFile(
            self,
            lambda obj: os.path.join(self.dir_act_data, "blocks.txt"),
            lambda obj: (
                "\n\n".join(
                    [
                        block_info["text"]
                        for block_info in self.block_info_list
                    ]
                )
                if self.block_info_list
                else None
            ),
        )

    @cached_property
    def text_path(self):
        return self.data_file_text.path

    @cached_property
    def text_fail_path(self):
        return self.data_file_text.path_fail

    @cached_property
    def text(self):
        return self.data_file_text.data

    @cached_property
    def is_text_valid(self):
        return self.text and len(self.text) >= self.MIN_BLOCK_TEXT_CHARS

    @cached_property
    def has_text(self):
        return self.data_file_text.exists

    def extract_text(self):
        return self.data_file_text.data
