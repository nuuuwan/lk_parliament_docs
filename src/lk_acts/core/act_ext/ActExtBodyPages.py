from dataclasses import dataclass

from lk_acts.core.act_ext.ActL0Part import ActL0Part
from lk_acts.core.act_ext.ActL1Section import ActL1Section


@dataclass
class ActExtBodyPages:
    preamble: list[str]
    pre_section_list: list[ActL1Section]
    part_list: list[ActL0Part]

    def to_dict(self):
        return dict(
            preamble=self.preamble,
            pre_section_list=[
                section.to_dict() for section in self.pre_section_list
            ],
            part_list=[part.to_dict() for part in self.part_list],
        )

    @classmethod
    def from_block_list(cls, block_list):
        part_list, pre_block_list = ActL0Part.list_from_block_list(block_list)
        pre_section_list = []
        preamble = []
        if pre_block_list:
            pre_section_list, pre2_block_list = (
                ActL1Section.list_from_block_list(pre_block_list)
            )
            preamble = [
                block.text.strip().title() for block in pre2_block_list
            ]

        return ActExtBodyPages(
            preamble=preamble,
            pre_section_list=pre_section_list,
            part_list=part_list,
        )

    def to_md_lines(self):
        lines = []
        for line in self.preamble:
            lines.extend([line])
        lines.append("")
        for section in self.pre_section_list:
            lines.extend(section.to_md_lines())

        lines.append("")
        for part in self.part_list:
            lines.extend(part.to_md_lines())
        return lines
