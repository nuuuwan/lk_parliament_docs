from pathlib import Path

from utils import File, Log, Time, TimeFormat

from lpd import Doc

log = Log("ReadMe")


class ReadMe:
    PATH = Path("README.md")

    def __init__(self):
        self.doc_list = Doc.list_all()
        self.n_docs = len(self.doc_list)
        self.year_to_list = Doc.year_to_list()

    @property
    def timestamp(self):
        return TimeFormat.TIME.format(Time.now())

    @staticmethod
    def get_lines_for_doc(doc):
        return [
            f"- `{doc.doc_num}` [{doc.description}]({doc.url}) ({doc.date})"
        ]

    @property
    def lines_for_docs(self):
        lines = [f"## Documents ({self.n_docs})", ""]
        for year, doc_list in self.year_to_list.items():
            n_docs = len(doc_list)
            lines.extend([f"### {year} ({n_docs:,})", ""])
            for doc in doc_list:
                lines.extend(self.get_lines_for_doc(doc))
            lines.extend([""])
        return lines + [""]

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
        ] + self.lines_for_docs

    def write(self):
        File(self.PATH).write_lines(self.lines)
        log.info(f"Wrote {self.PATH}")
