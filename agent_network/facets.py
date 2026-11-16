"""Facet hard filters: binding gates that no later stage may override."""
from __future__ import annotations

from datetime import datetime


def explicitly_subscribed(post, agent) -> bool:
    """True when the recipient explicitly subscribed to the author agent."""
    targets = {post["author_agent_id"]}
    for item in agent.get("subscriptions", []):
        if isinstance(item, str):
            if item in targets:
                return True
        elif item.get("type") == "agent" and item.get("target") in targets:
            return True
    return False


def hard_filter(data, post, agent, now: str | None = None) -> bool:
    """Six binding gates: self, recipient status, post status, expiry,
    excluded industry, competitor (with explicit-subscription exception),
    and payment-instrument compatibility."""
    clock = datetime.fromisoformat(now or post["as_of"])
    if agent["id"] == post["author_agent_id"] or agent["status"] != "active":
        return False
    if post["status"] != "published":
        return False
    if post.get("valid_until") and clock > datetime.fromisoformat(post["valid_until"]):
        return False
    author = data.agent_by_id[post["author_agent_id"]]
    if author["industry"] in agent.get("exclude_industries", []):
        return False
    if frozenset((post["author_slug"], agent["slug"])) in data.competitor_pairs and not explicitly_subscribed(post, agent):
        return False
    instruments = post["facets"].get("instruments", [])
    payment_role = set(agent["capabilities"]) & data.instrument_caps
    compatible = {data.instrument_to_capability[tag] for tag in instruments}
    # Merchants without any payment capability are exempt from the instrument gate.
    return not instruments or not payment_role or bool(payment_role & compatible)


def eligible_matrix(data) -> "np.ndarray":
    import numpy as np

    return np.array([[hard_filter(data, post, agent) for agent in data.agents] for post in data.posts])
