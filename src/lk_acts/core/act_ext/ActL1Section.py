from dataclasses import dataclass

from lk_acts.core.act_ext.ActL2Subsection import ActL2Subsection
from lk_acts.core.act_ext.ActLevel import ActLevel
from lk_acts.core.act_ext.PDFBlock import PDFBlock


@dataclass
class ActL1Section(ActLevel):
    num: int
    short_description: str
    text: str
    subsection_list: list[ActL2Subsection]
    inner_block_list: list[PDFBlock]

    @classmethod
    def get_re_title(cls):
        return r"^(?P<num>\d+)\s*\.\s*(?P<text>.+)"

    def to_dict(self):
        return dict(
            num=self.num,
            short_description=self.short_description,
            text=self.text,
            subsection_list=[
                sub_section.to_dict() for sub_section in self.subsection_list
            ],
            inner_text_list=[block.text for block in self.inner_block_list],
        )

    def to_md_lines(self):
        lines = [f"{self.num}. **{self.short_description}** - {self.text}"]
        for subsection in self.subsection_list:
            lines.extend(subsection.to_md_lines())
        for block in self.inner_block_list:
            lines.append(f"    - {block.text}")
        return lines + [""]

    @staticmethod
    def parse_short_description(block_list: list[PDFBlock]):
        short_description = None
        rem_block_list = []
        for block in block_list:
            if block.font_size <= 8:
                if not short_description:
                    short_description = block.text.strip()
            else:
                rem_block_list.append(block)
        return short_description, rem_block_list

    @classmethod
    def from_block_list(cls, block_list: list[PDFBlock]):
        first_block = block_list[0]
        match = cls.get_title_match(first_block)
        assert match

        short_description, rem_block_list = (
            ActL1Section.parse_short_description(block_list[1:])
        )

        text = match.group("text").strip()
        if text.startswith("("):
            rem_block_list = [
                PDFBlock(
                    text=text,
                    bbox=first_block.bbox,
                    font_family=first_block.font_family,
                    font_size=first_block.font_size,
                )
            ] + rem_block_list
            text = ""

        subsection_list, pre_block_list = (
            ActL2Subsection.list_from_block_list(rem_block_list)
        )

        return cls(
            num=int(match.group("num")),
            text=text,
            short_description=short_description,
            subsection_list=subsection_list,
            inner_block_list=(
                pre_block_list + rem_block_list
                if not subsection_list
                else pre_block_list
            ),
        )
