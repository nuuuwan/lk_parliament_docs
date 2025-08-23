import os

from utils import Log

log = Log("ActCleanupMixin")


class ActCleanupMixin:

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
