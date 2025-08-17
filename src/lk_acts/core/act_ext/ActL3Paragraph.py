import re
from dataclasses import dataclass

from lk_acts.core.act_ext.PDFBlock import PDFBlock


@dataclass
class ActL3Paragraph:
    num: str
    text: str
    inner_block_list: list[PDFBlock]

    RE_PARAGRAPH = r"^\s*\(\s*(?P<num>[a-z])\s*\)\s*(?P<text>.+)"

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

    @staticmethod
    def __get_title_match__(block: PDFBlock):
        return re.match(ActL3Paragraph.RE_PARAGRAPH, block.text)

    @staticmethod
    def __get_paragraph_to_block_list__(block_List: list[PDFBlock]):
        paragraph_to_block_list = []
        inner_block_list = []
        for block in block_List:

            match = ActL3Paragraph.__get_title_match__(block)
            if match:
                paragraph_to_block_list.append([block])
            elif paragraph_to_block_list:
                paragraph_to_block_list[-1].append(block)
            else:
                inner_block_list.append(block)
        return paragraph_to_block_list, inner_block_list

    @classmethod
    def from_block_list(cls, block_list: list[PDFBlock]):
        first_block = block_list[0]
        match = ActL3Paragraph.__get_title_match__(first_block)
        assert match
        return cls(
            num=match.group("num"),
            text=match.group("text"),
            inner_block_list=block_list[1:],
        )

    @classmethod
    def list_from_block_list(cls, block_list: list[PDFBlock]):
        paragraph_to_block_list, inner_block_list = (
            cls.__get_paragraph_to_block_list__(block_list)
        )
        return [
            cls.from_block_list(subsection)
            for subsection in paragraph_to_block_list
        ], inner_block_list
