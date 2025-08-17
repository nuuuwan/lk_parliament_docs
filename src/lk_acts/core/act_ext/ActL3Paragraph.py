from dataclasses import dataclass

from lk_acts.core.act_ext.ActLevel import ActLevel
from lk_acts.core.act_ext.PDFBlock import PDFBlock


@dataclass
class ActL3Paragraph(ActLevel):
    num: str
    text: str
    inner_block_list: list[PDFBlock]

    @classmethod
    def get_re_title(cls):
        return r"^\s*\(\s*(?P<num>[a-z])\s*\)\s*(?P<text>.+)"

    def to_dict(self):
        return dict(
            num=self.num,
            text=self.text,
            inner_text_list=[block.text for block in self.inner_block_list],
        )

    def to_md_lines(self):
        lines = [f"        {self.num}. {self.text}"]
        for block in self.inner_block_list:
            lines.append(f"            - {block.text}")
        return lines + [""]

    @classmethod
    def from_block_list(cls, block_list: list[PDFBlock]):
        first_block = block_list[0]
        match = ActL3Paragraph.get_title_match(first_block)
        assert match
        return cls(
            num=match.group("num"),
            text=match.group("text"),
            inner_block_list=block_list[1:],
        )
