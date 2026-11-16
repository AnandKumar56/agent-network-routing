"""Export measured checkpoint-2 errors without editing labels or owner verdicts."""

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(relative):
    return json.loads((ROOT / relative).read_text())


def export_review():
    destination = ROOT / "docs/fp_review.csv"
    if destination.exists():
        raise FileExistsError("Review already exists; preserve any owner adjudication.")
    snapshot = load("docs/checkpoint2_snapshot.json")
    measurements = load("docs/checkpoint3_review_measurements.json")
    for name, digest in snapshot["data_hashes"].items():
        assert hashlib.sha256((ROOT / f"data/{name}.json").read_bytes()).hexdigest() == digest
    agents = load("data/agents.json")
    posts = load("data/posts.json")
    labels = {row["post_id"]: row for row in load("data/eval_labels.json")}
    assert snapshot["agent_order"] == [agent["slug"] for agent in agents]
    assert snapshot["post_order"] == [post["slug"] for post in posts]
    assert measurements["threshold"] == 0.75
    rules = {row["id"] for row in load("data/routing_rules.json")["rules"]}
    edges = {row["id"] for row in load("data/relationships.json")}
    expected_pairs = set()
    for i, predicted in enumerate(snapshot["diagnostic_recipient_bits"]["M1"]):
        positive = snapshot["labels_bits"]["documented"][i] | snapshot["labels_bits"]["silver"][i]
        errors = (predicted & snapshot["labels_bits"]["negative"][i]) | (positive & ~predicted)
        expected_pairs.update((i, j) for j in range(len(agents)) if errors & (1 << j))
    rows = []
    groups = Counter()
    for i, j, similarity, rule_ids, edge_ids in measurements["rows"]:
        assert set(rule_ids) <= rules and set(edge_ids) <= edges
        post, agent = posts[i], agents[j]
        predicted = bool(snapshot["diagnostic_recipient_bits"]["M1"][i] & (1 << j))
        kind = "false_alert" if predicted else "miss"
        label_group = "must_not_notify" if predicted else "expected_recipients"
        label = next(row for row in labels[post["id"]][label_group] if row["agent_id"] == agent["id"])
        reason = label["reason"]
        if post["slug"] == "p26_exact_repost":
            reason = "Exact-repost delivery omission, not a business-relevance error; dedup now blocks routing."
        elif kind == "miss":
            reason = "M1 lacks card-provider-to-merchant coverage. v2: " + reason
        sources = ["similarity>=0.75" if similarity >= 0.75 else "similarity<0.75"]
        sources += ["rule:" + rule_id for rule_id in rule_ids]
        sources += ["edge:" + edge_id for edge_id in edge_ids]
        rows.append({
            "post_id": post["id"], "post_title": post["title"],
            "agent": agent["company_name"], "source": " | ".join(sources),
            "similarity": f"{similarity:.6f}", "reason": " ".join(reason.split()),
            "owner_verdict": "", "error_type": kind, "post_slug": post["slug"],
            "agent_id": agent["id"], "agent_slug": agent["slug"], "owner_reason": "",
        })
        if predicted:
            assert similarity < 0.75
            groups["rule+dated_edge" if rule_ids and edge_ids else "rule" if rule_ids else "dated_edge"] += 1
    assert {(row[0], row[1]) for row in measurements["rows"]} == expected_pairs
    assert len(rows) == len(expected_pairs) == 54
    counts = Counter(row["error_type"] for row in rows)
    assert counts == {"false_alert": 50, "miss": 4}
    assert dict(groups) == snapshot["false_alert_source_groups"]
    with destination.open("x", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"file": "docs/fp_review.csv", "rows": len(rows), "counts": counts,
                      "all_owner_verdicts_empty": True, "v2_hashes_unchanged": True}))


if __name__ == "__main__":
    export_review()
