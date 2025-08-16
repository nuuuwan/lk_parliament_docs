from pathlib import Path

from utils import File, Log, Time, TimeFormat

from lpd import Doc

log = Log("ReadMe")


class ReadMe:
    PATH = Path("README.md")

    def __init__(self):
        self.doc_list = Doc.list_all()
        self.n_docs = len(self.doc_list)

    @property
    def timestamp(self):
        return TimeFormat.TIME.format(Time.now())

    @property
    def lines(self):
        return [
            "# 🇱🇰 Documents from the Sri Lankan Parliament"
            + " ([lk_parliament_docs]"
            + "(https://github.com/nuuuwan/lk_parliament_docs))",
            "",
            f"Scraped  **{self.n_docs:,}** documents from"
            + " [www.parliament.lk](https://www.parliament.lk/en)"
            + f" as of **{self.timestamp}**.",
            "",
        ]

    def write(self):
        File(self.PATH).write_lines(self.lines)
        log.info(f"Wrote {self.PATH}")
