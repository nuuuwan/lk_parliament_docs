from dataclasses import dataclass

from lk_acts.core.act_ext.ActSection import ActSection


@dataclass
class ActExtBodyPages:
    preamble: list[str]
    section_list: list[ActSection]

    def to_dict(self):
        return dict(
            preamble=self.preamble,
            section_list=[section.to_dict() for section in self.section_list],
        )

    @classmethod
    def from_block_list(cls, block_list):
        section_list, preamble = ActSection.list_from_block_list(block_list)
        return ActExtBodyPages(
            preamble=preamble,
            section_list=section_list,
        )

    def to_md_lines(self):
        lines = []
        for line in self.preamble:
            lines.extend([line, ""])
        for section in self.section_list:
            lines.extend(section.to_md_lines())
        return lines
