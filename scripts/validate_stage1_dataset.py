"""Validate source and fixture integrity without embeddings, routing or model calls."""

import ast
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import unicodedata
import uuid


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def normalized(text):
    text = re.sub(r"https?://\S+", " ", text.casefold())
    text = "".join(" " if unicodedata.category(c)[0] in {"P", "S"} else c for c in text)
    return " ".join(text.split())


def aware(value):
    parsed = datetime.fromisoformat(value)
    assert parsed.tzinfo is not None and parsed.utcoffset().total_seconds() == 0, value
    return parsed


def validate(verify_local_snapshots=False):
    agents, posts, labels = load("agents.json"), load("posts.json"), load("eval_labels.json")
    taxonomy, rules = load("taxonomy.json"), load("routing_rules.json")
    relationships, cases = load("relationships.json"), load("hard_cases.json")
    source_manifest, manifest = load("source_manifest.json"), load("dataset_manifest.json")
    agent_ids = {a["id"] for a in agents}
    a_by_id = {a["id"]: a for a in agents}
    a_by_slug = {a["slug"]: a for a in agents}
    p_by_id, p_by_slug = {p["id"]: p for p in posts}, {p["slug"]: p for p in posts}
    sources = {s["source_id"]: s for s in source_manifest}
    assert len(agent_ids) == len(agents) == 19
    assert len(p_by_id) == len(posts) == len(p_by_slug) == len(labels) == 30
    assert len({a["slug"] for a in agents}) == 19
    assert sum(not a["is_synthetic"] for a in agents) == 16
    assert sum(not p["is_synthetic"] for p in posts) == 24
    assert {c["number"] for c in cases} == set(range(1, 11))
    verified_snapshots = 0
    portable_fields = {"source_id", "source_url", "checked_at_utc", "snapshot_sha256",
                       "source_date", "semantic_review", "review_notes"}
    assert len(sources) == len(source_manifest)
    for source in sources.values():
        assert set(source) == portable_fields, source["source_id"]
        assert source["semantic_review"] == "reviewed_for_listed_claims"
        assert source["source_url"].startswith("https://")
        assert re.fullmatch(r"[0-9a-f]{64}", source["snapshot_sha256"])
        assert source["review_notes"].strip() and len(source["review_notes"]) <= 400
        aware(source["checked_at_utc"])
        if source["source_date"]:
            datetime.strptime(source["source_date"], "%Y-%m-%d")
        if verify_local_snapshots:
            raw = (DATA / "source_snapshots" / f"{source['source_id']}.txt").read_bytes()
            assert hashlib.sha256(raw).hexdigest() == source["snapshot_sha256"]
            verified_snapshots += 1
    for company in agents:
        uuid.UUID(company["id"])
        assert type(company["is_synthetic"]) is bool
        assert set(company["capabilities"]) <= set(taxonomy["capabilities"])
        assert len(company["interests"]) >= 1 and company["profile_version"] == 1
        assert company["profile_temporal_scope"] == "static_november_2026_simulation"
        assert aware(company["profile_as_of"]).date().isoformat() == "2026-11-15"
        assert set(company["declared_partners"]) <= set(a_by_slug)
        if company["is_synthetic"]:
            assert company["company_name"].startswith("Demo ") and not company["sources"]
        else:
            assert company["source_ids"] and set(company["source_ids"]) <= set(sources)
        facts = load(f"fact_sheets/{company['slug']}.json")
        assert facts["agent_id"] == company["id"] and facts["is_synthetic"] == company["is_synthetic"]
        for fact in facts["facts"]:
            assert fact["source_id"] in sources
            assert fact["source_url"] == sources[fact["source_id"]]["source_url"]
            assert fact["allowed_numeric_tokens"] == re.findall(r"\d[\d,]*(?:\.\d+)?%?", fact["text"])
    for item in posts:
        uuid.UUID(item["id"])
        assert type(item["is_synthetic"]) is bool and item["author_agent_id"] in agent_ids
        assert a_by_id[item["author_agent_id"]]["slug"] == item["author_slug"]
        assert len(item["title"]) <= 140 and len(item["content"]) <= 2000
        assert item["offer_type"] in taxonomy["offer_types"]
        assert set(item["facets"]["categories"]) <= set(taxonomy["categories"])
        assert set(item["facets"]["instruments"]) <= set(taxonomy["instruments"])
        assert set(item["facets"]["partner_types_wanted"]) <= set(taxonomy["capabilities"])
        assert item["facets"]["offer_type"] == item["offer_type"]
        as_of = aware(item["as_of"])
        aware(item["created_at"])
        if item["valid_until"]:
            assert aware(item["valid_until"]) >= as_of
        if not item["is_synthetic"]:
            assert not a_by_id[item["author_agent_id"]]["is_synthetic"]
            assert item["source_id"] in sources and item["source_url"] == sources[item["source_id"]]["source_url"]
        elif item.get("derived_from"):
            original = p_by_id[item["derived_from"]]
            assert original["source_id"] == item["source_id"]
            assert original["author_agent_id"] == item["author_agent_id"]
        else:
            assert a_by_id[item["author_agent_id"]]["is_synthetic"]
            assert item["source_url"].startswith("fixture://")
        assert normalized(item["content"]) == item["normalized_content"]
        digest = hashlib.sha256((item["author_agent_id"] + item["normalized_content"]).encode()).hexdigest()
        assert item["dedup_key"] == digest
        facets = {k: sorted(v) if isinstance(v, list) else v for k, v in item["facets"].items()}
        assert item["facet_signature"] == hashlib.sha256(json.dumps(facets, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    instrument_map = rules["instrument_to_capability"]
    assert instrument_map == taxonomy["instrument_to_capability"]
    payment_roles = set(instrument_map.values())
    competitor_pairs = {frozenset(pair) for pair in rules["competitor_pairs"]}
    assert rules["competitor_exception"] == "explicit_subscription_only"
    assert rules["brand_name_matching"] is False
    assert rules["thresholds"]["status"] == "unselected"
    assert "valid_from <= now" in rules["relationship_time_policy"]
    assert "must not bypass" in rules["declared_partner_policy"]
    rows = {row["post_id"]: row for row in labels}
    assert set(rows) == set(p_by_id)
    positive_count = documented_count = negative_count = 0
    for row in rows.values():
        item = p_by_id[row["post_id"]]
        assert row["post_slug"] == item["slug"] and row["now"] == item["as_of"]
        assert row["approval_scope"] == "dev_only" and row["owner_review_required"] is False
        positives, negatives = row["expected_recipients"], row["must_not_notify"]
        positive_ids, negative_ids = {r["agent_id"] for r in positives}, {r["agent_id"] for r in negatives}
        assert len(positive_ids) == len(positives) and len(negative_ids) == len(negatives)
        assert not positive_ids & negative_ids and positive_ids | negative_ids == agent_ids
        assert item["author_agent_id"] not in positive_ids
        for label in positives + negatives:
            assert label["agent_slug"] == a_by_id[label["agent_id"]]["slug"]
            assert label["reason"].strip() and label["basis"] in {"documented", "inferred"}
            if label["basis"] == "documented":
                assert label["source_id"] in sources and label["evidence_url"] == sources[label["source_id"]]["source_url"]
        for label in positives:
            candidate = a_by_id[label["agent_id"]]
            assert frozenset([item["author_slug"], candidate["slug"]]) not in competitor_pairs
            capabilities = set(candidate["capabilities"]) & payment_roles
            required = {instrument_map[tag] for tag in item["facets"]["instruments"]}
            assert not required or not capabilities or required & capabilities, (item["slug"], candidate["slug"])
        positive_count += len(positives)
        documented_count += sum(label["basis"] == "documented" for label in positives)
        negative_count += len(negatives)
    for relationship in relationships:
        assert relationship["source_agent_id"] in agent_ids and relationship["target_agent_id"] in agent_ids
        assert relationship["basis"] in {"documented", "inferred"}
        if relationship["basis"] == "documented":
            assert relationship["source_id"] in sources and relationship["evidence_url"]
            assert relationship["valid_from"] is not None
            aware(relationship["valid_from"])
            assert relationship["valid_from_basis"] in {"dated_source_observation", "documented_launch_date", "documented_offer_start", "documented_campaign_start_in_retrospective_source", "first_observed_snapshot_not_historical_start"}
            if relationship["valid_from_basis"] == "first_observed_snapshot_not_historical_start":
                assert relationship["valid_from"][:10] == relationship["snapshot_date"]
            if relationship["valid_until"]:
                assert aware(relationship["valid_until"]) >= aware(relationship["valid_from"])
        else:
            assert relationship["type"] in {"competitor", "same_brand_unrelated"}
            assert relationship["valid_from"] is None and relationship["valid_from_basis"] == "static_dev_policy_not_dated_relationship"
    hdfc_edge = next(e for e in relationships if e["source_slug"] == "swiggy" and e["target_slug"] == "hdfc_bank")
    assert hdfc_edge["valid_from"] == "2023-07-26T00:00:00+00:00"
    assert hdfc_edge["source_id"] == "hdfc_swiggy_launch_2023"
    assert aware(hdfc_edge["valid_from"]) > aware(p_by_slug["p02_swiggy_diwali"]["as_of"])
    phonepe_edge = next(e for e in relationships if e["source_slug"] == "phonepe" and e["target_slug"] == "swiggy")
    assert phonepe_edge["valid_from"] == "2018-03-22T00:00:00+00:00"
    for case in cases:
        assert case["post_id"] in p_by_id and case["post_slug"] == p_by_id[case["post_id"]]["slug"]
        aware(case["now"])
        row = rows[case["post_id"]]
        expected_slugs = {r["agent_slug"] for r in row["expected_recipients"]}
        if case["number"] != 10:
            assert set(case.get("must_include", [])) <= expected_slugs
            assert not set(case.get("must_exclude", [])) & expected_slugs
        if "expected_recipients" in case and case["number"] != 10:
            assert not row["expected_recipients"]
    original, exact, near = [p_by_slug[s] for s in ["p01_flipkart_mobile_emi", "p26_exact_repost", "p29_near_repost"]]
    assert original["dedup_key"] == exact["dedup_key"] and exact["duplicate_of"] == original["id"]
    assert original["facet_signature"] == near["facet_signature"] and original["dedup_key"] != near["dedup_key"]
    assert (aware(exact["created_at"]) - aware(original["created_at"])).total_seconds() <= 24 * 3600
    expiry = next(c for c in cases if c["number"] == 10)
    assert aware(expiry["now"]) > aware(p_by_id[expiry["post_id"]]["valid_until"])
    injection = next(c for c in cases if c["number"] == 8)
    assert len(injection["variants"]) == 5
    assert all(v["is_synthetic"] and a_by_slug[v["author_slug"]]["is_synthetic"] for v in injection["variants"])
    assert manifest["positive_labels"] == positive_count and manifest["negative_labels"] == negative_count
    assert manifest["documented_positive_labels"] == documented_count
    assert manifest["inferred_positive_labels"] == positive_count - documented_count == 63
    assert documented_count == 14 and positive_count == 77 and negative_count == 493
    assert manifest["dataset_approval"] == "approved_dev" and manifest["dataset_role"] == "DEV"
    assert manifest["author_self_pairs_excluded"] == len(posts) == 30
    assert manifest["evaluated_pairs"] == len(posts) * (len(agents) - 1) == 540
    assert manifest["evaluated_negative_labels"] == negative_count - len(posts) == 463
    market_case = next(c for c in cases if c["number"] == 4)
    assert "market_update" in market_case["name"] and market_case["test_scope"] == "market_update_not_cashback_promotion"
    assert p_by_id[market_case["post_id"]]["offer_type"] == "market_update"
    notebook_path = ROOT / "notebooks/01_routing_experiments.ipynb"
    notebook = json.loads(notebook_path.read_text()) if notebook_path.is_file() else {"cells": []}
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    for cell in code_cells:
        source = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
        assert len(source.splitlines()) <= 25
        ast.parse(source)
        assert not cell["outputs"]
    source_check = f"{verified_snapshots} local source hashes match" if verify_local_snapshots else "portable metadata only; source bodies not reread"
    print(f"PASS: {len(agents)} agents, {len(posts)} posts, {len(sources)} reviewed sources; {source_check}.")
    print(f"PASS: 540 non-self pairs: {documented_count} documented positives, {positive_count-documented_count} silver positives, 463 negatives.")
    print("PASS: dated relationships and static-profile disclosure; approved DEV, not held-out data.")
    print("PASS: all 10 hard-case specifications are present and consistent. Routing and near-duplicate cosine are NOT tested.")
    if code_cells:
        print(f"PASS: {len(code_cells)} notebook code cells compile and contain at most 25 lines; final model and thresholds are unselected.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DATA, help="Validate a portable DEV folder, including the owner's snapshot-free Drive copy.")
    parser.add_argument("--verify-local-snapshots", action="store_true", help="Also require and hash the ignored local source bodies. Not needed in Drive.")
    args = parser.parse_args()
    DATA = args.data_dir.resolve()
    validate(args.verify_local_snapshots)
