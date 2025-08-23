import os
from functools import cached_property

import pandas as pd
from datasets import Dataset
from utils import Hash, JSONFile, Log

from lk_acts.core import Act
from utils_future import BigJSONFile, Chunker

log = Log("HuggingFaceDataset")


class HuggingFaceDataset:
    DIR_DATA_HF = os.path.join(Act.DIR_DATA, "hf")
    ACTS_JSON_PATH = os.path.join(DIR_DATA_HF, "acts.json")
    CHUNKS_JSON_PATH = os.path.join(DIR_DATA_HF, "chunks.json")
    HUGGING_FACE_USERNAME = os.environ.get("HUGGING_FACE_USERNAME")
    HUGGING_FACE_TOKEN = os.environ.get("HUGGING_FACE_TOKEN")
    MIN_MEAN_P_CONFIDENCE_FOR_OCR_TEXT = 0.5

    MAX_CHUNK_SIZE = 2000
    MIN_OVERLAP_SIZE = 200

    @cached_property
    def acts_list(self):
        act_list = Act.list_all()

        acts_with_txt_data = [
            act
            for act in act_list
            if act.get_text(
                HuggingFaceDataset.MIN_MEAN_P_CONFIDENCE_FOR_OCR_TEXT
            )
        ]
        return acts_with_txt_data

    @staticmethod
    def to_act_data(act: Act) -> dict:
        return dict(
            act_id=act.act_id,
            act_description=act.description,
            act_year=act.year,
            act_sub_num=act.doc_sub_num,
            act_date=act.date,
            act_type=act.act_type.name,
            act_source_url=act.url_pdf_en,
        )

    def build_acts(self):
        data_list = [
            HuggingFaceDataset.to_act_data(act) for act in self.acts_list
        ]
        os.makedirs(self.DIR_DATA_HF, exist_ok=True)
        JSONFile(self.ACTS_JSON_PATH).write(data_list)
        n_rows = len(data_list)
        file_size_m = os.path.getsize(self.ACTS_JSON_PATH) / (1024 * 1024)
        log.info(
            f"Wrote {self.ACTS_JSON_PATH}"
            + f" ({n_rows:,} acts, {file_size_m:.1f} MB)"
        )

    @staticmethod
    def get_data_list_for_act(act):
        chunks = Chunker.chunk(
            act.get_text(
                HuggingFaceDataset.MIN_MEAN_P_CONFIDENCE_FOR_OCR_TEXT
            ),
            HuggingFaceDataset.MAX_CHUNK_SIZE,
            HuggingFaceDataset.MIN_OVERLAP_SIZE,
        )
        d_list = []
        for chunk_index, chunk_text in enumerate(chunks):
            chunk_id = f"{act.act_id}-{chunk_index:04d}"
            d = HuggingFaceDataset.to_act_data(act) | dict(
                chunk_id=chunk_id,
                chunk_index=chunk_index,
                language="en",
                md5=Hash.md5(chunk_text),
                chunk_size_bytes=len(chunk_text.encode("utf-8")),
                chunk_text=chunk_text,
            )
            d_list.append(d)

        return d_list

    def build_chunks(self):
        d_list = []
        for act in self.acts_list:
            d_list.extend(HuggingFaceDataset.get_data_list_for_act(act))

        JSONFile(self.CHUNKS_JSON_PATH).write(d_list)
        n_rows = len(d_list)
        file_size_m = os.path.getsize(self.CHUNKS_JSON_PATH) / (1024 * 1024)
        log.info(
            f"Wrote {self.CHUNKS_JSON_PATH}"
            + f" ({n_rows:,} chunks, {file_size_m:.1f} MB)"
        )

    def upload_to_hugging_face(self, do_upload=False):
        acts_df = pd.read_json(self.ACTS_JSON_PATH)
        chunks_df = pd.read_json(self.CHUNKS_JSON_PATH)

        acts_ds = Dataset.from_pandas(acts_df)
        chunks_ds = Dataset.from_pandas(chunks_df)

        assert self.HUGGING_FACE_USERNAME
        assert self.HUGGING_FACE_TOKEN
        hf_project = f"{self.HUGGING_FACE_USERNAME}/lk-acts"
        log.debug(f"🤗 {hf_project=}")

        for ds, label in [(acts_ds, "acts"), (chunks_ds, "chunks")]:
            dataset_id = f"{hf_project}-{label}"
            if do_upload:
                repo_id = ds.push_to_hub(
                    dataset_id, token=self.HUGGING_FACE_TOKEN
                )
                log.info(f"🤗 Uploaded {dataset_id} to {repo_id}")

    def split_big_files(self):
        BigJSONFile(self.ACTS_JSON_PATH).split()
        BigJSONFile(self.CHUNKS_JSON_PATH).split()

    def build_and_upload(self, do_upload=False):
        self.build_acts()
        self.build_chunks()
        self.upload_to_hugging_face(do_upload)
        self.split_big_files()
