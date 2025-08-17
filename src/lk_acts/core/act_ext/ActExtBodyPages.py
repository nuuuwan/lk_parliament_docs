from dataclasses import dataclass

from lk_acts.core.act_ext.ActL0Part import ActL0Part
from lk_acts.core.act_ext.ActL1Section import ActL1Section


@dataclass
class ActExtBodyPages:
    preamble: list[str]
    section_list: list[ActL1Section]

    def to_dict(self):
        return dict(
            preamble=self.preamble,
            section_list=[section.to_dict() for section in self.section_list],
        )

    @classmethod
    def from_block_list(cls, block_list):
        section_list, pre_block_list = ActL0Part.list_from_block_list(
            block_list
        )
        print("section_list", len(section_list))

        preamble = [block.text.strip().title() for block in pre_block_list]
        return ActExtBodyPages(
            preamble=preamble,
            section_list=section_list,
        )

    def to_md_lines(self):
        lines = []
        for line in self.preamble:
            lines.extend([line])
        lines.append("")
        for section in self.section_list:
            lines.extend(section.to_md_lines())
        return lines
