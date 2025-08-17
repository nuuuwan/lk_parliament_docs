from dataclasses import dataclass

import roman

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
        i = roman.fromRoman(num.lower())
        return roman.toRoman(i + 1).upper()

    @classmethod
    def get_re_title(cls):
        return r"^\s*PART\s*(?P<num>[IVX]*)\s*"
