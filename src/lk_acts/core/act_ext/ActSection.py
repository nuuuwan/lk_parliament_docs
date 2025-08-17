import re
from dataclasses import dataclass

from lk_acts.core.act_ext.ActSubsection import ActSubsection
from lk_acts.core.act_ext.PDFBlock import PDFBlock


@dataclass
class ActSection:
    num: int
    short_description: str
    text: str
    sub_section_list: list[ActSubsection]

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

    @staticmethod
    def __get_section_to_block_list__(block_List: list[PDFBlock]):
        section_to_block_list = []
        for block in block_List:
            match = re.match(ActSection.RE_SECTION, block.text)
            if match:
                section_to_block_list.append([block])
            if section_to_block_list:
                section_to_block_list[-1].append(block)
        return section_to_block_list

    @classmethod
    def from_block_list(cls, block_list: list[PDFBlock]):
        first_block = block_list[0]
        match = re.match(cls.RE_SECTION, first_block.text)
        assert match
        return cls(
            num=int(match.group("num")),
            text=match.group("text"),
            short_description=ActSection.parse_short_description(
                block_list[1:]
            ),
            sub_section_list=ActSubsection.list_from_block_list(
                block_list[1:]
            ),
        )

    @classmethod
    def list_from_block_list(cls, block_list: list[PDFBlock]):
        section_to_block_list = cls.__get_section_to_block_list__(block_list)
        return [
            cls.from_block_list(section) for section in section_to_block_list
        ]
