import re
from dataclasses import dataclass

from lk_acts.core.act_ext.PDFBlock import PDFBlock


@dataclass
class ActSubsection:
    num: int
    text: str
    inner_block_list: list[PDFBlock]

    RE_SUB_SECTION = r"^\((?P<num>\d+)\)\s*(?P<text>.+)"

    def to_dict(self):
        return dict(
            num=self.num,
            text=self.text,
            inner_text_list=[block.text for block in self.inner_block_list],
        )

    @classmethod
    def list_from_block_list(cls, block_list: list[PDFBlock]):
        sub_section_d_list = []

        for block in block_list:
            match = re.match(cls.RE_SUB_SECTION, block.text)
            if not match:
                if sub_section_d_list:
                    sub_section_d_list[-1]["inner_block_list"].append(block)
                continue

            section_d = dict(
                num=int(match.group("num")),
                text=match.group("text"),
                inner_block_list=[],
            )
            sub_section_d_list.append(section_d)

        sub_section_list = []
        for sub_section_d in sub_section_d_list:
            section = ActSubsection(
                num=sub_section_d["num"],
                text=sub_section_d["text"],
                inner_block_list=sub_section_d["inner_block_list"],
            )
            sub_section_list.append(section)
        return sub_section_list
