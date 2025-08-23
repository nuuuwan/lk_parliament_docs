from lk_acts.core.act.ActCleanup import ActCleanup
from lk_acts.core.act.ActRead import ActRead
from lk_acts.core.act.ActStatus import ActStatus


class Act(ActRead, ActStatus, ActCleanup):
    pass
