from dataclasses import dataclass

from lk_acts.core.act_ext.ActLevel import ActLevel


@dataclass
class ActL4SubParagraph(ActLevel):

    @classmethod
    def get_depth(cls):
        return 4

    @classmethod
    def get_child_class(cls):
        return None

    @classmethod
    def get_re_title(cls):
        return r"^\s*\(\s*(?P<num>[a-z])\s*\)\s*(?P<text>.+)"
