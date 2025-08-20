import os
from functools import cached_property

from utils import File, Log

from utils_future import PDFFile

log = Log("ActExtractText")


class ActExtractText:
    @cached_property
    def pdf_path(self):
        raise NotImplementedError

    @cached_property
    def dir_act_data(self):
        raise NotImplementedError

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
