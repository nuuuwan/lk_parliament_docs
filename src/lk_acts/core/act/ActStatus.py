import os
from functools import cached_property


class ActStatus:

    @cached_property
    def has_metadata(self):
        return os.path.exists(self.metadata_json_path)

    @cached_property
    def has_pdf(self):
        return os.path.exists(self.pdf_path)

    @cached_property
    def has_blocks(self):
        return os.path.exists(self.blocks_path)

    @cached_property
    def has_txt(self):
        return os.path.exists(self.txt_path)

    @cached_property
    def has_act_json(self):
        return os.path.exists(os.path.join(self.dir_act_data, "act.json"))

    @cached_property
    def status(self):

        return dict(
            has_metadata=self.has_metadata,
            has_pdf=self.has_pdf,
            has_blocks=self.has_blocks,
            has_txt=self.has_txt,
            has_act_json=self.has_act_json,
        )

    @classmethod
    def get_status_summary(cls):
        decade_to_list = cls.decade_to_list()

        d_list = []
        for decade, act_list in decade_to_list.items():
            n_metadata = sum(
                [1 for act in act_list if act.status["has_metadata"]]
            )
            n_pdf = sum([1 for act in act_list if act.status["has_pdf"]])
            n_blocks = sum(
                [1 for act in act_list if act.status["has_blocks"]]
            )
            n_txt = sum([1 for act in act_list if act.status["has_txt"]])
            n_act_json = sum(
                [1 for act in act_list if act.status["has_act_json"]]
            )

            d = dict(
                decade=decade,
                n_metadata=n_metadata,
                n_pdf=n_pdf,
                n_blocks=n_blocks,
                n_txt=n_txt,
                n_act_json=n_act_json,
            )
            d_list.append(d)

        total_n_metadata = sum(d["n_metadata"] for d in d_list)
        total_n_pdf = sum(d["n_pdf"] for d in d_list)
        total_n_blocks = sum(d["n_blocks"] for d in d_list)
        total_n_txt = sum(d["n_txt"] for d in d_list)
        total_n_act_json = sum(d["n_act_json"] for d in d_list)

        totals_d = dict(
            decade="Total",
            n_metadata=total_n_metadata,
            n_pdf=total_n_pdf,
            n_blocks=total_n_blocks,
            n_txt=total_n_txt,
            n_act_json=total_n_act_json,
        )
        d_list.append(totals_d)

        return d_list
