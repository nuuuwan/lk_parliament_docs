import re
from dataclasses import dataclass

from lk_acts.core.act_ext.PDFBlock import PDFBlock


@dataclass
class ActLevel:
    num: int
    text: str
    child_level_list: list["ActLevel"]
    pre_block_list: list[PDFBlock]
    post_block_list: list[PDFBlock]

    @classmethod
    def get_depth(cls):
        raise NotImplementedError

    @classmethod
    def get_child_class(cls):
        raise NotImplementedError

    @classmethod
    def get_re_title(cls):
        raise NotImplementedError

    def to_dict(self):
        return dict(
            num=self.num,
            text=self.text,
            pre_block_list=[block.text for block in self.pre_block_list],
            child_level_list=[
                child.to_dict() for child in self.child_level_list
            ],
            post_block_list=[block.text for block in self.post_block_list],
        )

    def to_md_lines(self):
        lines = [f"{self.num}. {self.text}"]
        tabs = " " * (self.get_depth() - 1) * 4

        for block in self.pre_block_list:
            lines.append(f"{tabs}- {block.text}")
        lines.append("")

        for child in self.child_level_list:
            lines.extend(child.to_md_lines())
        lines.append("")

        for block in self.post_block_list:
            lines.append(f"{tabs}- {block.text}")
        lines.append("")

        return lines

    @classmethod
    def get_title_match(cls, block: PDFBlock):
        return re.match(cls.get_re_title(), block.text)

    @classmethod
    def __get_level_to_block_list__(cls, block_List: list[PDFBlock]):
        level_to_block_list = []
        pre_block_list = []
        for block in block_List:
            if "Italic" in block.font_family:
                continue
            match = cls.get_title_match(block)
            if match:
                level_to_block_list.append([block])
            elif level_to_block_list:
                level_to_block_list[-1].append(block)
            else:
                pre_block_list.append(block)
        return level_to_block_list, pre_block_list

    @classmethod
    def from_block_list(cls, block_list: list[PDFBlock]):
        first_block = block_list[0]
        match = cls.get_title_match(first_block)
        assert match

        child_class = cls.get_child_class()
        if child_class:
            child_level_list, pre_block_list = (
                cls.get_child_class().list_from_block_list(block_list[1:])
            )
        else:
            child_level_list = []
            pre_block_list = block_list[1:]

        return cls(
            num=match.group("num"),
            text=match.group("text"),
            pre_block_list=pre_block_list,
            child_level_list=child_level_list,
            post_block_list=[],
        )

    @classmethod
    def list_from_block_list(cls, block_list: list[PDFBlock]):
        level_to_block_list, pre_block_list = cls.__get_level_to_block_list__(
            block_list
        )
        return [
            cls.from_block_list(level) for level in level_to_block_list
        ], pre_block_list
