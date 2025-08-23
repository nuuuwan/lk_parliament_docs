import os
from functools import cached_property

from lk_acts.core.act.ActExtractOCRText import ActExtractOCRText


class ActStatus(ActExtractOCRText):
    STATUS_FIELD_LIST = [
        "metadata",
        "pdf",
        "blocks",
        "text",
        "ocr_blocks",
        "ocr_text",
        "act_json",
    ]

    @cached_property
    def has_act_json(self):
        return os.path.exists(os.path.join(self.dir_act_data, "act.json"))

    @cached_property
    def status(self):
        return dict(
            has_metadata=self.has_metadata,
            has_pdf=self.has_pdf,
            has_blocks=self.has_blocks,
            has_text=self.has_text,
            has_ocr_blocks=self.has_ocr_blocks,
            has_ocr_text=self.has_ocr_text,
            has_act_json=self.has_act_json,
        )

    @staticmethod
    def __get_totals_row__(d_list):
        k_list = list(d_list[0].keys())
        totals_d = dict(decade="Total")
        for k in k_list:
            if k != "decade":
                totals_d[k] = sum(d[k] for d in d_list)
        return totals_d

    @classmethod
    def get_status_summary(cls):
        decade_to_list = cls.decade_to_list()
        d_list = []
        for decade, act_list in decade_to_list.items():
            d = dict(decade=decade)
            for k in cls.STATUS_FIELD_LIST:
                d[f"n_{k}"] = sum(
                    1 for act in act_list if act.status[f"has_{k}"]
                )
            d_list.append(d)

        d_list.append(cls.__get_totals_row__(d_list))
        return d_list
