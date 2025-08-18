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
        act_list = cls.list_all()
        n_metadata = sum(
            [1 for act in act_list if act.status["has_metadata"]]
        )
        n_pdf = sum([1 for act in act_list if act.status["has_pdf"]])
        n_act_json = sum(
            [1 for act in act_list if act.status["has_act_json"]]
        )

        return dict(
            metadata=n_metadata,
            pdf=n_pdf,
            act_json=n_act_json,
        )
