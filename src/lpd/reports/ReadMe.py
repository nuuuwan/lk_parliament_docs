from pathlib import Path

from utils import File, Log, Time, TimeFormat

from lpd.core import Doc
from lpd.reports.ChartYear import ChartYear

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

    @property
    def lines_for_year_chart(self):
        image_path = ChartYear(self.year_to_list).draw()
        return [f"![Year Chart]({image_path})", ""]

    @staticmethod
    def get_lines_for_doc(doc):
        return [
            f"- {doc.emoji} `{doc.doc_num}`"
            + f" [{doc.description}]({doc.url})"
            + f" ({doc.date})"
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
        return (
            [
                "# 🇱🇰 Documents from the Sri Lankan Parliament"
                + " ([lk_parliament_docs]"
                + "(https://github.com/nuuuwan/lk_parliament_docs))",
                "",
                f"Scraped  **{self.n_docs:,}** documents from"
                + " [www.parliament.lk](https://www.parliament.lk/en)"
                + f" as of **{self.timestamp}**.",
                "",
            ]
            + self.lines_for_year_chart
            + self.lines_for_docs
        )

    def write(self):
        File(self.PATH).write_lines(self.lines)
        log.info(f"Wrote {self.PATH}")
