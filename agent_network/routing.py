"""M1 routing: candidates = filters AND (similarity OR rules OR dated edges OR subscription)."""
from __future__ import annotations

import numpy as np

from .evidence import relationship_hints, rule_hits
from .facets import explicitly_subscribed, hard_filter


def eligible_row(data, post, now: str | None = None) -> np.ndarray:
    return np.array([hard_filter(data, post, agent, now) for agent in data.agents], dtype=bool)


def extras_row(data, post, now: str | None = None) -> np.ndarray:
    return np.array([
        bool(rule_hits(data, post, agent) or relationship_hints(data, post, agent, now) or explicitly_subscribed(post, agent))
        for agent in data.agents
    ], dtype=bool)


def route_post(data, scores, slug: str, method: str = "M1", threshold: float = 0.75, now: str | None = None) -> np.ndarray:
    i = data.post_index[slug]
    post = data.posts[i]
    candidates = scores[i] >= threshold
    if method == "M0 raw":
        eligible = np.array([agent["id"] != post["author_agent_id"] for agent in data.agents], dtype=bool)
        return candidates & eligible
    eligible = eligible_row(data, post, now)
    if method == "M0 filtered":
        return candidates & eligible
    if method != "M1":
        raise ValueError(method)
    return (candidates | extras_row(data, post, now)) & eligible


def metric_row(data, prediction: np.ndarray, scope: str = "all") -> dict:
    """scope 'all' uses documented|silver positives; other scopes ignore the
    other positive basis instead of counting it as an error."""
    target = data.positive if scope == "all" else getattr(data, scope)
    universe = (target | data.negative) & data.non_self
    tp = int((prediction & target & universe).sum())
    fp = int((prediction & data.negative & universe).sum())
    fn = int((~prediction & target & universe).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0
    return {"scope": scope, "n": int(universe.sum()), "n_positive": int((target & universe).sum()),
            "tp": tp, "fp": fp, "fn": fn, "precision": round(precision, 6), "recall": round(recall, 6), "f1": round(f1, 6)}
