import os
from functools import cached_property

import nltk
import pandas as pd
from datasets import Dataset
from utils import Hash, JSONFile, Log

from lk_acts.core import Act

log = Log("HuggingFaceDataset")


class HuggingFaceDataset:
    DIR_DATA_HF = os.path.join("data", "hf")
    ACTS_JSON_PATH = os.path.join(DIR_DATA_HF, "acts.json")
    CHUNKS_JSON_PATH = os.path.join(DIR_DATA_HF, "chunks.json")
    DATASET_SUFFIX = "2020-2024"
    HUGGINGFACE_USERNAME = os.environ.get("HUGGINGFACE_USERNAME")
    MIN_YEAR, MAX_YEAR = 2020, 2024

    MAX_CHUNK_SIZE = 2000
    MIN_SENTENCE_OVERLAP = 1

    @cached_property
    def acts_list(self):
        act_list = Act.list_all()
        acts_with_all_data = [act for act in act_list if act.has_txt]
        acts_in_range = [
            act
            for act in acts_with_all_data
            if self.MIN_YEAR <= act.year_int <= self.MAX_YEAR
        ]
        return acts_in_range

    @staticmethod
    def to_act_data(act: Act) -> dict:

        return dict(
            act_id=act.act_id,
            description=act.description,
            year=act.year,
            sub_num=act.doc_sub_num,
            date=act.date,
            act_type=act.act_type.name,
            source_url=act.url_pdf_en,
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
            + f" ({n_rows:,} acts, {file_size_m:.2f} MB)"
        )

    @staticmethod
    def chunk_by_sentence(content: str) -> list[str]:
        sentences = nltk.sent_tokenize(content)

        chunks = []
        current_sentences = []
        current_size = 0
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if (
                current_size + len(sentence) + 1
                > HuggingFaceDataset.MAX_CHUNK_SIZE
            ):
                current = " ".join(current_sentences).strip()
                chunks.append(current)
                overlap = HuggingFaceDataset.MIN_SENTENCE_OVERLAP
                current_sentences = current_sentences[-overlap:]
                current_size = sum(len(s) for s in current_sentences)
            else:
                current_sentences.append(sentence)
                current_size += len(sentence) + 1

        if current_sentences:
            current = " ".join(current_sentences).strip()
            chunks.append(current)

        return chunks

    @staticmethod
    def get_data_list_for_act(act):
        raw_chunks = act.text_content.split("\n\n")
        chunks = []
        for raw_chunk in raw_chunks:
            chunks.extend(HuggingFaceDataset.chunk_by_sentence(raw_chunk))

        d_list = []
        for chunk_index, chunk_text in enumerate(chunks):
            chunk_id = f"{act.act_id}-{chunk_index:04d}"
            d = dict(
                chunk_id=chunk_id,
                act_id=act.act_id,
                act_description=act.description,
                act_year=act.year,
                act_sub_num=act.doc_sub_num,
                act_source_url=act.url_pdf_en,
                language="en",
                chunk_index=chunk_index,
                md5=Hash.md5(chunk_text),
                chunk_size_bytes=len(chunk_text.encode("utf-8")),
                chunk_text=chunk_text,
            )
            d_list.append(d)
        return d_list

    def build_chunks(self):
        nltk.download("punkt")
        nltk.download("punkt_tab")

        d_list = []
        for act in self.acts_list:
            d_list.extend(HuggingFaceDataset.get_data_list_for_act(act))

        JSONFile(self.CHUNKS_JSON_PATH).write(d_list)
        n_rows = len(d_list)
        file_size_m = os.path.getsize(self.CHUNKS_JSON_PATH) / (1024 * 1024)
        log.info(
            f"Wrote {self.CHUNKS_JSON_PATH}"
            + f" ({n_rows:,} chunks, {file_size_m:.2f} MB)"
        )

    def upload_to_hugging_face(self):
        acts_df = pd.read_json(self.ACTS_JSON_PATH)
        chunks_df = pd.read_json(self.CHUNKS_JSON_PATH)

        acts_ds = Dataset.from_pandas(acts_df)
        chunks_ds = Dataset.from_pandas(chunks_df)

        hf_username = self.HUGGINGFACE_USERNAME
        hf_project = f"{hf_username}/lk-acts-{self.DATASET_SUFFIX}"
        log.debug(f"{hf_project=}")

        for ds, label in [(acts_ds, "acts"), (chunks_ds, "chunks")]:
            dataset_id = f"{hf_project}-{label}"
            repo_id = ds.push_to_hub(dataset_id)
            log.info(f"Uploaded {dataset_id} to {repo_id}")
