from dataclasses import dataclass

from lk_acts.core.act_ext.ActLevel import ActLevel


@dataclass
class ActL4SubParagraph(ActLevel):

    @classmethod
    def get_depth(cls):
        return 4

    @classmethod
    def get_child_cls(cls):
        return None

    @classmethod
    def get_next_num(cls, num):
        roman_nums = [  # HACK!
            "i",
            "ii",
            "iii",
            "iv",
            "v",
            "vi",
            "vii",
            "viii",
            "ix",
            "x",
        ]
        if num in roman_nums:
            return roman_nums[roman_nums.index(num) + 1]
        return None

    @classmethod
    def get_re_title(cls):
        return r"^\s*\(\s*(?P<num>[iv]*)\s*\)\s*(?P<text>.+)"
