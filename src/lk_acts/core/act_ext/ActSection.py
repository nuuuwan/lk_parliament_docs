import re
from dataclasses import dataclass

from lk_acts.core.act_ext.ActSubsection import ActSubsection
from lk_acts.core.act_ext.PDFBlock import PDFBlock


@dataclass
class ActSection:
    num: int
    short_description: str
    text: str
    subsection_list: list[ActSubsection]

    RE_SECTION = r"^(?P<num>\d+)\s*\.\s*(?P<text>.+)"

    def to_dict(self):
        return dict(
            num=self.num,
            short_description=self.short_description,
            text=self.text,
            subsection_list=[
                sub_section.to_dict() for sub_section in self.subsection_list
            ],
        )

    def to_md_lines(self):
        lines = [f"{self.num}. **{self.short_description}** - {self.text}"]
        for subsection in self.subsection_list:
            lines.extend(subsection.to_md_lines())
        return lines + [""]

    @staticmethod
    def parse_short_description(block_list: list[PDFBlock]):
        for block in block_list:
            if block.font_size <= 8:
                return block.text

    @staticmethod
    def __get_title_match__(block: PDFBlock):
        return re.match(ActSection.RE_SECTION, block.text)

    @staticmethod
    def __get_section_to_block_list__(block_List: list[PDFBlock]):
        section_to_block_list = []
        for block in block_List:
            if "Italic" in block.font_family:
                continue
            match = ActSection.__get_title_match__(block)
            if match:
                section_to_block_list.append([block])
            elif section_to_block_list:
                section_to_block_list[-1].append(block)
        return section_to_block_list

    @classmethod
    def from_block_list(cls, block_list: list[PDFBlock]):
        first_block = block_list[0]
        match = ActSection.__get_title_match__(first_block)
        assert match
        return cls(
            num=int(match.group("num")),
            text=match.group("text"),
            short_description=ActSection.parse_short_description(
                block_list[1:]
            ),
            subsection_list=ActSubsection.list_from_block_list(
                block_list[1:]
            ),
        )

    @classmethod
    def list_from_block_list(cls, block_list: list[PDFBlock]):
        section_to_block_list = cls.__get_section_to_block_list__(block_list)
        return [
            cls.from_block_list(section) for section in section_to_block_list
        ]
