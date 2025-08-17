import re
from dataclasses import dataclass

from lk_acts.core.act_ext.ActSubSection import ActSubSection
from lk_acts.core.act_ext.PDFBlock import PDFBlock


@dataclass
class ActSection:
    num: int
    short_description: str
    text: str
    sub_section_list: list[ActSubSection]

    RE_SECTION = r"^(?P<num>\d+)\s*\.\s*(?P<text>.+)"

    def to_dict(self):
        return dict(
            num=self.num,
            short_description=self.short_description,
            text=self.text,
            sub_section_list=[
                sub_section.to_dict() for sub_section in self.sub_section_list
            ],
        )

    @staticmethod
    def parse_short_description(block_list: list[PDFBlock]):
        for block in block_list:
            if block.font_size <= 8:
                return block.text

    @classmethod
    def list_from_block_list(cls, block_list: list[PDFBlock]):
        section_d_list = []

        for block in block_list:
            match = re.match(cls.RE_SECTION, block.text)
            if not match:
                if section_d_list:
                    section_d_list[-1]["inner_block_list"].append(block)
                continue

            section_d = dict(
                num=int(match.group("num")),
                text=match.group("text"),
                inner_block_list=[],
            )
            section_d_list.append(section_d)

        section_list = []
        for section_d in section_d_list:
            section = ActSection(
                num=section_d["num"],
                short_description=ActSection.parse_short_description(
                    section_d["inner_block_list"]
                ),
                text=section_d["text"],
                sub_section_list=ActSubSection.list_from_block_list(
                    section_d["inner_block_list"]
                ),
            )
            section_list.append(section)
        return section_list
