"""Evidence sources: capability rules and DATED relationship hints."""
from __future__ import annotations

from datetime import datetime


def rule_hits(data, post, agent) -> list[str]:
    """Capability rules: structured facets -> required recipient capabilities."""
    facets = post["facets"]
    values = {
        "instruments_any": facets.get("instruments", []),
        "categories_any": facets.get("categories", []),
        "offer_types_any": [facets["offer_type"]],
        "author_capabilities_any": data.agent_by_id[post["author_agent_id"]]["capabilities"],
    }
    hits = []
    for rule in data.rules["rules"]:
        matches = all(
            bool(facets.get("partner_types_wanted")) if key == "partner_types_wanted"
            else bool(set(values[key]) & set(required))
            for key, required in rule["when"].items()
        )
        wanted = facets.get(rule.get("capabilities_from", ""), []) or rule.get("capabilities_any", [])
        if matches and set(agent["capabilities"]) & set(wanted):
            hits.append(rule["id"])
    return hits


def relationship_hints(data, post, agent, now: str | None = None) -> list[str]:
    """Date-valid relationship edges only: valid_from <= clock <= valid_until.

    Static declared_partners are deliberately NOT a candidate source: a 2023
    edge must never support a 2020 post, no matter what today's profile says.
    """
    clock = datetime.fromisoformat(now or post["as_of"])
    hints = []
    for edge in data.relationships:
        forward = edge["source_agent_id"] == post["author_agent_id"] and edge["target_agent_id"] == agent["id"]
        reverse = edge["direction"] == "both" and edge["target_agent_id"] == post["author_agent_id"] and edge["source_agent_id"] == agent["id"]
        if not (forward or reverse) or edge["type"] in ("competitor", "same_brand_unrelated"):
            continue
        if not edge.get("valid_from") or datetime.fromisoformat(edge["valid_from"]) > clock:
            continue
        if edge.get("valid_until") and datetime.fromisoformat(edge["valid_until"]) < clock:
            continue
        hints.append(edge["id"])
    return hints
