import re
from dataclasses import dataclass

from lk_acts.core.act_ext.PDFBlock import PDFBlock


@dataclass
class ActL2Subsection:
    num: int
    text: str
    inner_block_list: list[PDFBlock]

    RE_SUBSECTION = r"^\s*\((?P<num>\d+)\)\s*(?P<text>.+)"

    def to_dict(self):
        return dict(
            num=self.num,
            text=self.text,
            inner_text_list=[block.text for block in self.inner_block_list],
        )

    def to_md_lines(self):
        lines = [f"    {self.num}. {self.text}"]
        for block in self.inner_block_list:
            lines.append(f"        - {block.text}")
        return lines + [""]

    @staticmethod
    def __get_title_match__(block: PDFBlock):
        return re.match(ActL2Subsection.RE_SUBSECTION, block.text)

    @staticmethod
    def __get_subsection_to_block_list__(block_List: list[PDFBlock]):
        subsection_to_block_list = []
        for block in block_List:

            match = ActL2Subsection.__get_title_match__(block)
            if match:
                subsection_to_block_list.append([block])
            elif subsection_to_block_list:
                subsection_to_block_list[-1].append(block)
        return subsection_to_block_list

    @classmethod
    def from_block_list(cls, block_list: list[PDFBlock]):
        first_block = block_list[0]
        match = ActL2Subsection.__get_title_match__(first_block)
        assert match
        return cls(
            num=int(match.group("num")),
            text=match.group("text"),
            inner_block_list=block_list[1:],
        )

    @classmethod
    def list_from_block_list(cls, block_list: list[PDFBlock]):
        subsection_to_block_list = cls.__get_subsection_to_block_list__(
            block_list
        )
        return [
            cls.from_block_list(subsection)
            for subsection in subsection_to_block_list
        ]
