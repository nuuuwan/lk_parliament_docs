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
    def get_child_cls(cls):
        raise NotImplementedError

    @classmethod
    def get_next_num(cls, num):
        raise NotImplementedError

    @classmethod
    def get_re_title(cls):
        raise NotImplementedError

    def to_dict(self):
        return dict(
            class_name=self.__class__.__name__,
            num=self.num,
            text=self.text,
            pre_block_list=[block.text for block in self.pre_block_list],
            child_level_list=[
                child.to_dict() for child in self.child_level_list
            ],
            post_block_list=[block.text for block in self.post_block_list],
        )

    def to_md_lines(self):
        tab_unit = " " * 4
        tabs = tab_unit * self.get_depth()
        child_tabs = tab_unit + tabs
        lines = [f"{tabs}{self.num}. {self.text}"]

        for block in self.pre_block_list:
            lines.append(f"{child_tabs}- {block.text}")

        for child in self.child_level_list:
            lines.extend(child.to_md_lines())

        for block in self.post_block_list:
            lines.append(f"{child_tabs}- {block.text}")

        return lines

    @classmethod
    def get_title_match(cls, text):
        return re.match(cls.get_re_title(), text)

    @classmethod
    def __get_level_to_block_list__(  # noqa: C901
        cls, block_List: list[PDFBlock]
    ):
        level_to_block_list = {}
        pre_block_list = []
        cur_num = None
        next_num = None
        for block in block_List:
            if "Italic" in block.font_family:
                continue
            match = cls.get_title_match(block.text)
            if match:
                num = match.group("num")
                if next_num is None or num == next_num:
                    level_to_block_list[num] = [block]
                    cur_num = num
                    next_num = cls.get_next_num(num)
                elif cur_num:
                    level_to_block_list[cur_num].append(block)
            elif cur_num:
                level_to_block_list[cur_num].append(block)
            else:
                pre_block_list.append(block)
        return list(level_to_block_list.values()), pre_block_list

    @classmethod
    def from_block_list(cls, block_list: list[PDFBlock]):
        first_block = block_list[0]
        match = cls.get_title_match(first_block.text)
        assert match
        text = (
            match.group("text").strip()
            if "text" in match.re.groupindex
            else ""
        )

        child_level_list = []
        pre_block_list = block_list[1:]
        child_cls = cls.get_child_cls()
        if child_cls:
            inner_block_list = block_list[1:]
            child_match = child_cls.get_title_match(text)
            if child_match:
                inner_block_list = [
                    PDFBlock(
                        bbox=first_block.bbox,
                        text=text,
                        font_family=first_block.font_family,
                        font_size=first_block.font_size,
                    )
                ] + inner_block_list
                text = ""
            desc_cls = child_cls
            while desc_cls is not None and inner_block_list:
                child_level_list, pre_block_list = (
                    desc_cls.list_from_block_list(inner_block_list)
                )
                if child_level_list:
                    break
                desc_cls = desc_cls.get_child_cls()

        return cls(
            num=match.group("num"),
            text=text,
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
