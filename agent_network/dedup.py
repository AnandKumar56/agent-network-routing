"""Deduplication measured before routing (owner amendment).

Exact: same-author normalized-content SHA256; stops routing entirely while the
earlier post remains valid or within 24 hours.
Near: same author, same facet signature, cosine >= 0.95 within seven days;
suppresses recipients already notified for matching earlier posts.
Labels are never modified by dedup; suppression is delivery behavior only.
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime, timedelta

import numpy as np

_URL = re.compile(r"https?://\S+")
_NON_WORD = re.compile(r"[^a-z0-9]+")


def normalized_post_content(text: str) -> str:
    text = _URL.sub(" ", text).casefold()
    return " ".join(_NON_WORD.sub(" ", text).split())


def post_dedup_key(post) -> str:
    # Always computed from normalized content; equals the stored dedup_key for
    # every approved post (asserted in tests), but stays correct for edited copies.
    return hashlib.sha256(normalized_post_content(post["content"]).encode()).hexdigest()


def duplicate_stage(post, history, vector, near_threshold: float = 0.95, near_days: int = 7) -> dict:
    created = datetime.fromisoformat(post["created_at"])
    key = post_dedup_key(post)
    for entry in history:
        prior = entry["post"]
        if entry["key"] != key or prior["author_agent_id"] != post["author_agent_id"]:
            continue
        if datetime.fromisoformat(prior["created_at"]) > created:
            continue
        valid = bool(prior.get("valid_until")) and created <= datetime.fromisoformat(prior["valid_until"])
        recent = created - datetime.fromisoformat(prior["created_at"]) <= timedelta(hours=24)
        if valid or recent:
            return {"kind": "exact", "suppress": set()}
    suppress: set[int] = set()
    matched = False
    for entry in history:
        prior = entry["post"]
        if prior["author_agent_id"] != post["author_agent_id"] or prior.get("facet_signature") != post.get("facet_signature"):
            continue
        if created - datetime.fromisoformat(prior["created_at"]) > timedelta(days=near_days):
            continue
        if float(np.dot(vector, entry["vector"])) >= near_threshold:
            matched = True
            suppress |= entry["notified"]
    return {"kind": "near" if matched else "new", "suppress": suppress}


def dedup_sequence(data, scores, post_vectors, threshold: float = 0.75) -> dict:
    """Chronological dedup, then M1 routing. Exact reposts invoke zero routing
    calls; near reposts route but suppress already-notified recipients."""
    from .routing import route_post

    n_agents = len(data.agents)
    order = sorted(range(len(data.posts)), key=lambda i: datetime.fromisoformat(data.posts[i]["created_at"]))
    history: list[dict] = []
    after = np.zeros_like(scores, dtype=bool)
    notifications = np.zeros_like(scores, dtype=bool)
    suppressed_pairs = np.zeros_like(scores, dtype=bool)
    traces = {}
    route_calls = 0
    for i in order:
        post = data.posts[i]
        stage = duplicate_stage(post, history, post_vectors[i])
        if stage["kind"] == "exact":
            routed = np.zeros(n_agents, dtype=bool)  # zero routing calls
        else:
            routed = route_post(data, scores, post["slug"], "M1", threshold)
            route_calls += 1
        suppress_mask = np.zeros(n_agents, dtype=bool)
        for j in stage["suppress"]:
            suppress_mask[j] = True
        notified = np.zeros(n_agents, dtype=bool) if stage["kind"] == "exact" else routed & ~suppress_mask
        # Relevance prediction: near posts still route normally; only the exact
        # repost's row is zeroed (it never routed).
        after[i] = routed
        notifications[i] = notified
        if stage["kind"] == "near":
            suppressed_pairs[i] = routed & suppress_mask
        traces[post["slug"]] = {"kind": stage["kind"], "routed": int(routed.sum()), "notified": int(notified.sum()), "suppressed": int(routed.sum() - notified.sum())}
        history.append({"post": post, "key": post_dedup_key(post), "vector": post_vectors[i], "notified": {int(j) for j in np.flatnonzero(notified)}})
    return {"after": after, "notifications": notifications, "suppressed_pairs": suppressed_pairs, "traces": traces, "route_calls": route_calls}
