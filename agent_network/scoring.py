"""BGE-small similarity scoring, matching the measured Colab protocol exactly:
title + newline + content; one vector per interest statement; no query prefix;
L2 normalization; agent score = max cosine across its interests."""
from __future__ import annotations

from pathlib import Path

import numpy as np

MODEL = "BAAI/bge-small-en-v1.5"


def compute_scores(data, cache_path: str | Path | None = None, model: str = MODEL):
    cache = Path(cache_path) if cache_path else None
    if cache and cache.exists():
        blob = np.load(cache)
        if blob["scores"].shape == (len(data.posts), len(data.agents)):
            return blob["scores"], blob["post_vectors"]
    from fastembed import TextEmbedding

    embedder = TextEmbedding(model_name=model, cache_dir=str(Path(__file__).resolve().parents[1] / ".models"), threads=2)
    interest_texts = [text for agent in data.agents for text in agent["interests"]]
    interest_owner = np.array([j for j, agent in enumerate(data.agents) for _ in agent["interests"]])
    post_texts = [post["title"] + "\n" + post["content"] for post in data.posts]

    def embed(texts):
        vectors = np.vstack(list(embedder.embed(texts, batch_size=16))).astype(np.float32)
        return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    interest_vectors = embed(interest_texts)
    post_vectors = embed(post_texts)
    scores = np.column_stack([
        (post_vectors @ interest_vectors[interest_owner == j].T).max(axis=1)
        for j in range(len(data.agents))
    ])
    if cache:
        cache.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(cache, scores=scores, post_vectors=post_vectors)
    return scores, post_vectors
