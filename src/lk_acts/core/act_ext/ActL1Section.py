from dataclasses import dataclass

from lk_acts.core.act_ext.ActL2Subsection import ActL2Subsection
from lk_acts.core.act_ext.ActLevel import ActLevel


@dataclass
class ActL1Section(ActLevel):

    @classmethod
    def get_depth(cls):
        return 1

    @classmethod
    def get_child_cls(cls):
        return ActL2Subsection

    @classmethod
    def get_next_num(cls, num):
        return str(int(num) + 1)

    @classmethod
    def get_re_title(cls):
        return r"^(?P<num>\d+)\s*\.\s*(?P<text>.+)"
