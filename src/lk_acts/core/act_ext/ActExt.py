import os
from dataclasses import dataclass
from functools import cached_property
from itertools import chain

from utils import File, JSONFile, Log

from lk_acts.core.act import Act
from lk_acts.core.act_ext.ActExtBodyPages import ActExtBodyPages
from lk_acts.core.act_ext.ActExtPDF import ActExtPDF
from lk_acts.core.act_ext.ActExtTitlePage import ActExtTitlePage

log = Log("ActExt")


@dataclass
class ActExt:
    n_pages: int
    title_page: ActExtTitlePage
    body_pages: ActExtBodyPages

    @cached_property
    def n_sections(self):
        return len(self.body_pages.section_list)

    @classmethod
    def from_pdf(cls, pdf_path):
        act_ext_pdf = ActExtPDF(pdf_path)

        return cls(
            n_pages=act_ext_pdf.n_pages,
            title_page=ActExtTitlePage.from_block_list(
                act_ext_pdf.page_block_list[0]
            ),
            body_pages=ActExtBodyPages.from_block_list(
                list(chain.from_iterable(act_ext_pdf.page_block_list[1:]))
            ),
        )

    @classmethod
    def from_act_id(cls, act_id):
        dir_path = Act.get_dir_act_data(act_id)
        pdf_path = os.path.join(dir_path, "en.pdf")
        assert os.path.exists(pdf_path), f"PDF not found: {pdf_path}"
        return cls.from_pdf(pdf_path)

    def to_dict(self):
        return dict(
            n_pages=self.n_pages,
            title_page=self.title_page.to_dict(),
            body_pages=self.body_pages.to_dict(),
        )

    def to_md_lines(self):
        return self.title_page.to_md_lines() + self.body_pages.to_md_lines()

    def write_md(self, md_path):
        content = "\n".join(self.to_md_lines()).replace("\n\n\n", "\n\n")
        File(md_path).write(content)
        log.info(f"Wrote {md_path}")

    def write_json(self, json_path):
        JSONFile(json_path).write(self.to_dict())
        log.info(f"Wrote {json_path}")
