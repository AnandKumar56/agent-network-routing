"""Stage 1 routing core: load approved v2 DEV fixtures and label matrices."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def _load(name: str):
    return json.loads((DATA / f"{name}.json").read_text())


class DevData:
    """Approved v2 dataset: 19 agents, 30 posts, 540 evaluated non-self pairs."""

    def __init__(self, root: Path = DATA):
        self.agents = _load("agents")
        self.posts = _load("posts")
        self.rules = _load("routing_rules")
        self.relationships = _load("relationships")
        self.labels = {row["post_id"]: row for row in _load("eval_labels")}
        self.agent_by_id = {agent["id"]: agent for agent in self.agents}
        self.agent_index = {agent["slug"]: j for j, agent in enumerate(self.agents)}
        self.post_index = {post["slug"]: i for i, post in enumerate(self.posts)}
        self.competitor_pairs = {frozenset(pair) for pair in self.rules["competitor_pairs"]}
        self.instrument_to_capability = dict(self.rules["instrument_to_capability"])
        self.instrument_caps = set(self.instrument_to_capability.values())

        n_posts, n_agents = len(self.posts), len(self.agents)
        self.documented = np.zeros((n_posts, n_agents), dtype=bool)
        self.silver = np.zeros((n_posts, n_agents), dtype=bool)
        self.negative = np.zeros((n_posts, n_agents), dtype=bool)
        for i, post in enumerate(self.posts):
            row = self.labels[post["id"]]
            for entry in row["expected_recipients"]:
                j = self.agent_index.get(self.agent_by_id[entry["agent_id"]]["slug"])
                if entry["basis"] == "documented":
                    self.documented[i, j] = True
                else:
                    self.silver[i, j] = True
            for entry in row["must_not_notify"]:
                if entry["agent_id"] == post["author_agent_id"]:
                    continue  # author-self pair is outside the 540-pair evaluated universe
                self.negative[i, self.agent_index[self.agent_by_id[entry["agent_id"]]["slug"]]] = True

        self.positive = self.documented | self.silver
        self.non_self = self.positive | self.negative

    def summary(self) -> dict:
        return {
            "agents": len(self.agents),
            "posts": len(self.posts),
            "non_self_pairs": int(self.non_self.sum()),
            "documented_positives": int(self.documented.sum()),
            "silver_positives": int(self.silver.sum()),
            "negatives": int(self.negative.sum()),
        }
