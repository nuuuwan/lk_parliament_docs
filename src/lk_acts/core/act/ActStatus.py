import os
from functools import cached_property


class ActStatus:

    @property
    def metadata_json_path(self):
        raise NotImplementedError

    @property
    def pdf_path(self):
        raise NotImplementedError

    @property
    def dir_act_data(self):
        raise NotImplementedError

    @classmethod
    def list_all(cls):
        raise NotImplementedError

    @cached_property
    def status(self):
        has_metadata = os.path.exists(self.metadata_json_path)
        has_pdf = os.path.exists(self.pdf_path)
        has_act_json = os.path.exists(
            os.path.join(self.dir_act_data, "act.json")
        )

        return dict(
            has_metadata=has_metadata,
            has_pdf=has_pdf,
            has_act_json=has_act_json,
        )

    @classmethod
    def get_status_summary(cls):
        year_to_list = cls.year_to_list()

        d_list = []
        for year, act_list in year_to_list.items():
            n_metadata = sum(
                [1 for act in act_list if act.status["has_metadata"]]
            )
            n_pdf = sum([1 for act in act_list if act.status["has_pdf"]])
            n_act_json = sum(
                [1 for act in act_list if act.status["has_act_json"]]
            )

            d = dict(
                year=year,
                n_metadata=n_metadata,
                n_pdf=n_pdf,
                n_act_json=n_act_json,
            )
            d_list.append(d)
        return d_list
