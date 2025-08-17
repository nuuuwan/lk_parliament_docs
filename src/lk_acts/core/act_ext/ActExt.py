from dataclasses import dataclass
from functools import cached_property
from itertools import chain

from lk_acts.core.act_ext.ActExtBodyPages import ActExtBodyPages
from lk_acts.core.act_ext.ActExtPDF import ActExtPDF
from lk_acts.core.act_ext.ActExtTitlePage import ActExtTitlePage


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

    def to_dict(self):
        return dict(
            n_pages=self.n_pages,
            title_page=self.title_page.to_dict(),
            body_pages=self.body_pages.to_dict(),
        )
