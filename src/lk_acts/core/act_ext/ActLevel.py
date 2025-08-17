import re

from lk_acts.core.act_ext.PDFBlock import PDFBlock


class ActLevel:
    @classmethod
    def get_re_title(cls):
        raise NotImplementedError

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
        raise NotImplementedError

    @classmethod
    def list_from_block_list(cls, block_list: list[PDFBlock]):
        level_to_block_list, pre_block_list = cls.__get_level_to_block_list__(
            block_list
        )
        return [
            cls.from_block_list(level) for level in level_to_block_list
        ], pre_block_list
