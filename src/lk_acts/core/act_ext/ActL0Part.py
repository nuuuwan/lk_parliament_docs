from dataclasses import dataclass

from lk_acts.core.act_ext.ActL1Section import ActL1Section
from lk_acts.core.act_ext.ActLevel import ActLevel


@dataclass
class ActL0Part(ActLevel):

    @classmethod
    def get_depth(cls):
        return 0

    @classmethod
    def get_child_cls(cls):
        return ActL1Section

    @classmethod
    def get_next_num(cls, num):
        roman_nums = [  # HACK!
            "I",
            "II",
            "III",
            "IV",
            "V",
            "VI",
            "VII",
            "VIII",
            "IX",
            "X",
            "XI",
            "XII",
            "XIII",
            "XIV",
            "XV",
            "XVI",
            "XVII",
            "XVIII",
            "XIX",
            "XX",
        ]
        if num in roman_nums:
            return roman_nums[roman_nums.index(num) + 1]
        return None

    @classmethod
    def get_re_title(cls):
        return r"^\s*PART\s*(?P<num>[IVX]*)\s*"
