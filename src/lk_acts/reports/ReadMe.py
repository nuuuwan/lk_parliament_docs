from pathlib import Path

from utils import File, Log

from lk_acts.core import Act
from lk_acts.pages import ActsBillsPage
from lk_acts.reports.ChartYear import ChartYear
from utils_future import Markdown

log = Log("ReadMe")


class ReadMe:
    PATH = Path("README.md")

    def __init__(self):
        self.doc_list = Act.list_all()
        self.n_docs = len(self.doc_list)
        self.year_to_list = Act.year_to_list()
        self.year_to_type_to_list = Act.year_to_type_to_list()
        self.data_size_g = Act.get_dir_data_size() / (1_000_000_000.0)
        self.status_summary = Act.get_status_summary()

    @property
    def lines_for_year_chart(self):
        image_path = ChartYear(self.year_to_type_to_list).draw()
        return [f"![Year Chart]({image_path})", ""]

    @staticmethod
    def get_lines_for_doc(doc):
        return [
            f"- {doc.act_type.emoji} `{doc.num}`"
            + f" [{doc.description}]({doc.url})"
            + f" ({doc.date})"
        ]

    @property
    def lines_for_docs(self):
        lines = [
            f"## Acts ({self.n_docs:,})",
            "",
        ]
        for year, doc_list in self.year_to_list.items():
            n_docs = len(doc_list)
            lines.extend([f"### {year} ({n_docs:,})", ""])
            for doc in doc_list:
                lines.extend(self.get_lines_for_doc(doc))
            lines.extend([""])
        return lines + [""]

    @property
    def lines_for_status_summary(self):
        status_summary = self.status_summary
        return (
            [
                "## Processing status",
                "",
                "- **metadata**: name, year, number, and links to PDFs.",
                "- **pdf**: the English source PDF."
                + " Sinhala and Tamil PDFs are not yet downloaded.",
                "- **blocks**: text blocks extracted from the PDF.",
                "- **text**: full text assembled from the blocks.",
                "- **ocr_blocks**: text blocks extracted via OCR (costly).",
                "- **ocr_text**: full text assembled from OCR blocks.",
                "- **act_json**: structured representation of the Act"
                + " parsed from text.",
                "",
            ]
            + Markdown.table(status_summary)
            + [""]
        )

    @property
    def lines_for_hugging_face(self):
        lines = ["## 🤗 Hugging Face (🆕)", "", "### Datasets", ""]
        for label in ["lk-acts-acts", "lk-acts-chunks"]:
            url = f"https://huggingface.co/datasets/nuuuwan/{label}"
            lines.append(f"- [{label}]({url})")
        lines.append("")
        return lines

    @property
    def lines(self):
        url = ActsBillsPage.URL
        url_raw_data = "https://github.com/nuuuwan/lk_acts_data/tree/main/data"
        return (
            [
                "# 🇱🇰 Acts from the Sri Lankan Parliament"
                + " ([lk_acts]"
                + "(https://github.com/nuuuwan/lk_acts))",
                "",
                f"Scraped  **{self.n_docs:,}** acts"
                + f" ({self.data_size_g:.1f} GB) from"
                + f" [www.parliament.lk]({url})."
                "",
                f"📦 Raw Data - [{url_raw_data}]({url_raw_data})",
                "",
            ]
            + self.lines_for_year_chart
            + self.lines_for_status_summary
            + self.lines_for_hugging_face
            + self.lines_for_docs
        )

    def write(self):
        File(self.PATH).write_lines(self.lines)
        log.info(f"Wrote {self.PATH}")
