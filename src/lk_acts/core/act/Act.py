from lk_acts.core.act.ActBase import ActBase
from lk_acts.core.act.ActCleanupMixin import ActCleanupMixin
from lk_acts.core.act.ActDownloadPDFMixin import ActDownloadPDFMixin
from lk_acts.core.act.ActExtractOCRTextMixin import ActExtractOCRTextMixin
from lk_acts.core.act.ActExtractTextMixin import ActExtractTextMixin
from lk_acts.core.act.ActReadMixin import ActReadMixin
from lk_acts.core.act.ActStatusMixin import ActStatusMixin
from lk_acts.core.act.ActWriteMixin import ActWriteMixin


class Act(
    ActBase,
    ActWriteMixin,
    ActReadMixin,
    ActDownloadPDFMixin,
    ActExtractTextMixin,
    ActExtractOCRTextMixin,
    ActStatusMixin,
    ActCleanupMixin,
):
    pass
