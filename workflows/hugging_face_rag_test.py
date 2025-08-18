#!/usr/bin/env python3

import os

import numpy as np
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from transformers import pipeline

DS_NAME = "nuuuwan/lk-acts-2020-2024-chunks"
TOP_K = 4
EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GEN_MODEL = "google/flan-t5-base"


# 1) Load dataset
ds = load_dataset(DS_NAME, split="train")
cols = list(ds.column_names)


META_URL = "act_source_url"
TEXT_COL = "chunk_text"

texts = ds[TEXT_COL]

# 2) Build embeddings (in-memory)
emb_model = SentenceTransformer(EMB_MODEL)
embs = emb_model.encode(
    texts,
    convert_to_numpy=True,
    normalize_embeddings=True,
    batch_size=128,
    show_progress_bar=True,
)

# 3) Simple retriever
norm = lambda v: v / (np.linalg.norm(v) + 1e-9)


def retrieve(q, k=TOP_K):
    qv = norm(emb_model.encode(q, convert_to_numpy=True))
    scores = (embs @ qv).astype(float)
    idx = scores.argsort()[-k:][::-1]
    return [(int(i), float(scores[i])) for i in idx]


# 4) Lightweight generator (Flan-T5 by default)
gen = pipeline("text2text-generation", model=GEN_MODEL, device_map="auto")

PROMPT_TMPL = (
    "Answer the legal question using ONLY the context.\n"
    "Quote exact sections when relevant and keep it concise.\n"
    "If the answer isn't clearly stated, say so.\n\n"
    "Question: {q}\n\nContext:\n{ctx}\n\nAnswer:"
)


def cite(i):
    r = ds[int(i)]
    parts = []
    if META_URL and r.get(META_URL):
        parts.append(str(r[META_URL]))
    return " | ".join(parts) or f"Row {i}"


if __name__ == "__main__":
    print(
        f"Loaded {len(ds)} chunks from {DS_NAME}. Using {TEXT_COL!r} as text column."
    )
    print("Ask a question (Ctrl+C to quit).\n")
    try:
        while True:
            q = input("> ").strip()
            if not q:
                continue
            hits = retrieve(q)
            ctx = "\n\n---\n".join(
                (ds[TEXT_COL][i] or "")[:1500] for i, _ in hits
            )  # trim per chunk
            prompt = PROMPT_TMPL.format(q=q, ctx=ctx)
            print("-" * 64)
            print("PROMPT")
            print("-" * 64)
            print(prompt)
            print("-" * 64)

            out = gen(
                prompt,
                max_new_tokens=256,
                truncation=True,
            )[
                0
            ]["generated_text"].strip()
            print(f"\n{out}\n")
            print("Sources:")
            for j, (i, s) in enumerate(hits, 1):
                print(f"[{j}] {cite(i)} (score={s:.3f})")
            print()
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")
