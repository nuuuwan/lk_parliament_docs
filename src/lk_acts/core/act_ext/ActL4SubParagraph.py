from dataclasses import dataclass

import roman

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
        i = roman.fromRoman(num.lower())
        return roman.toRoman(i + 1).lower()

    @classmethod
    def get_re_title(cls):
        return r"^\s*\(\s*(?P<num>[iv]*)\s*\)\s*(?P<text>.+)"
