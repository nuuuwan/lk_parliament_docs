from dataclasses import dataclass

from lk_acts.core.act_ext.ActL3Paragraph import ActL3Paragraph
from lk_acts.core.act_ext.ActLevel import ActLevel


@dataclass
class ActL2Subsection(ActLevel):

    @classmethod
    def get_depth(cls):
        return 2

    @classmethod
    def get_child_cls(cls):
        return ActL3Paragraph

    @classmethod
    def get_next_num(cls, num):
        return str(int(num) + 1)

    @classmethod
    def get_re_title(cls):
        return r"^\s*\((?P<num>\d+)\)\s*(?P<text>.+)"
