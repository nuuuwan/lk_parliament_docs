from dataclasses import dataclass

from lk_acts.core.act_ext.ActL3Paragraph import ActL3Paragraph
from lk_acts.core.act_ext.ActLevel import ActLevel
from lk_acts.core.act_ext.PDFBlock import PDFBlock


@dataclass
class ActL2Subsection(ActLevel):
    num: int
    text: str
    paragraph_list: list[ActL3Paragraph]
    inner_block_list: list[PDFBlock]

    @classmethod
    def get_re_title(cls):
        return r"^\s*\((?P<num>\d+)\)\s*(?P<text>.+)"

    def to_dict(self):
        return dict(
            num=self.num,
            text=self.text,
            paragraph_list=[
                paragraph.to_dict() for paragraph in self.paragraph_list
            ],
            inner_text_list=[block.text for block in self.inner_block_list],
        )

    def to_md_lines(self):
        lines = [f"    {self.num}. {self.text}"]
        for paragraph in self.paragraph_list:
            lines.extend(paragraph.to_md_lines())
        for block in self.inner_block_list:
            lines.append(f"        - {block.text}")
        return lines + [""]

    @classmethod
    def from_block_list(cls, block_list: list[PDFBlock]):
        first_block = block_list[0]
        match = cls.get_title_match(first_block)
        assert match
        paragraph_list, pre_block_list = ActL3Paragraph.list_from_block_list(
            block_list[1:]
        )
        return cls(
            num=int(match.group("num")),
            text=match.group("text"),
            paragraph_list=paragraph_list,
            inner_block_list=pre_block_list,
        )
