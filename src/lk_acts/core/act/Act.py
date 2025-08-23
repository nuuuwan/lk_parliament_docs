from lk_acts.core.act.ActBase import ActBase
from lk_acts.core.act.ActCleanup import ActCleanup
from lk_acts.core.act.ActDownloadPDF import ActDownloadPDF
from lk_acts.core.act.ActExtractOCRText import ActExtractOCRText
from lk_acts.core.act.ActExtractText import ActExtractText
from lk_acts.core.act.ActRead import ActRead
from lk_acts.core.act.ActStatus import ActStatus
from lk_acts.core.act.ActWrite import ActWrite


class Act(
    ActBase,
    ActWrite,  # <- ActBase
    ActRead,  # <- ActBase
    ActDownloadPDF,  # <- ActBase
    ActExtractText,  # <- ActBase, ActDownloadPDF
    ActExtractOCRText,  # <- ActBase, ActDownloadPDF , ActExtraText
    ActStatus,  # <- ActBase, ActWrite, #ActRead,
    # ActDownloadPDF, ActExtractText, ActExtractOCRText
    ActCleanup,  # ActDownloadPDF, ActExtractText, ActExtractOCRText
):
    pass
