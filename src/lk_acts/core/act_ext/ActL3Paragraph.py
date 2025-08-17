from dataclasses import dataclass

from lk_acts.core.act_ext.ActL4SubParagraph import ActL4SubParagraph
from lk_acts.core.act_ext.ActLevel import ActLevel


@dataclass
class ActL3Paragraph(ActLevel):

    @classmethod
    def get_depth(cls):
        return 3

    @classmethod
    def get_child_cls(cls):
        return ActL4SubParagraph

    @classmethod
    def get_re_title(cls):
        return r"^\s*\(\s*(?P<num>[a-z])\s*\)\s*(?P<text>.+)"
