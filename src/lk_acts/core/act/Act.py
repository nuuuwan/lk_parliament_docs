from lk_acts.core.act.ActDownloadPDF import ActDownloadPDF
from lk_acts.core.act.ActExtractText import ActExtractText
from lk_acts.core.act.ActStatus import ActStatus


class Act(ActDownloadPDF, ActExtractText, ActStatus):
    pass
