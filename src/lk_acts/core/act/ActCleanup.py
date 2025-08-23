import os
from functools import cached_property

from utils import Log

log = Log("ActCleanup")


class ActCleanup:
    @cached_property
    def pdf_fail_path(self):
        raise NotImplementedError  # ActDownloadPDF

    @cached_property
    def blocks_fail_path(self):
        raise NotImplementedError  # ActExtractText

    @cached_property
    def text_fail_path(self):
        raise NotImplementedError  # ActExtractText

    @cached_property
    def ocr_blocks_fail_path(self):
        raise NotImplementedError  # ActExtractOCRText

    @cached_property
    def ocr_text_fail_path(self):
        raise NotImplementedError  # ActExtractOCRText

    def __delete_files_if_exists__(self, file_path_list):
        for delete_path in file_path_list:
            if os.path.exists(delete_path):
                os.remove(delete_path)
                log.debug(f"[{self}] ❌ Deleted {delete_path}")

    def cleanup_fails(self):
        self.__delete_files_if_exists__(
            [
                self.pdf_fail_path,
                self.blocks_fail_path,
                self.text_fail_path,
                self.ocr_blocks_fail_path,
                self.ocr_text_fail_path,
            ],
        )
