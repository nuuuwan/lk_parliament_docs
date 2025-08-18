import os
from functools import cached_property

from utils import CSVFile, Log

from lk_acts.core import Act, ActExt

log = Log("HuggingFaceDataset")


class HuggingFaceDataset:
    DIR_DATA_HF = os.path.join("data", "hf")
    ACTS_CSV_PATH = os.path.join(DIR_DATA_HF, "acts.csv")

    @cached_property
    def acts_list(self):
        act_list = Act.list_all()
        acts_with_all_data = [act for act in act_list if act.has_act_json]
        return acts_with_all_data

    @staticmethod
    def to_act_data(act: Act) -> dict:
        act_ext = ActExt.from_act_id(act.act_id)
        title_page = act_ext.title_page
        return dict(
            act_id=act.act_id,
            title=title_page.title,
            year=title_page.year,
            num=title_page.num,
            date_certified=title_page.date_certified,
            date_published=title_page.date_published,
            act_type=act.act_type.name,
            url_pdf_en=act.url_pdf_en,
            n_pages=act_ext.n_pages,
        )

    def build_acts(self):
        data_list = [
            HuggingFaceDataset.to_act_data(act) for act in self.acts_list
        ]
        os.makedirs(self.DIR_DATA_HF, exist_ok=True)
        CSVFile(self.ACTS_CSV_PATH).write(data_list)
        n_rows = len(data_list)
        file_size_m = os.path.getsize(self.ACTS_CSV_PATH) / (1024 * 1024)
        log.info(
            f"Wrote {self.ACTS_CSV_PATH}"
            + f" ({n_rows:,} rows, {file_size_m:.2f} MB)"
        )
