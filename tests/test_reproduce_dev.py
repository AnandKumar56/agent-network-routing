"""Reproduce the measured DEV numbers in docs/RESULTS.md from the approved v2 fixtures."""
import numpy as np

from agent_network.dedup import dedup_sequence, duplicate_stage, post_dedup_key
from agent_network.evidence import relationship_hints
from agent_network.facets import hard_filter
from agent_network.routing import metric_row, route_post

P26 = "p26_exact_repost"


def test_label_universe(data):
    assert data.summary() == {"agents": 19, "posts": 30, "non_self_pairs": 540,
                              "documented_positives": 14, "silver_positives": 63, "negatives": 463}


def test_m0_raw_and_filtered_at_diagnostic_threshold(data, embeddings):
    scores, _ = embeddings
    raw = metric_row(data, route_post(data, scores, "p01_flipkart_mobile_emi", "M0 raw", 0.65))
    assert raw["tp"] >= 0
    counts = np.vstack([route_post(data, scores, post["slug"], "M0 raw", 0.65) for post in data.posts])
    assert tuple(metric_row(data, counts)[key] for key in ("tp", "fp", "fn")) == (48, 84, 29)
    counts = np.vstack([route_post(data, scores, post["slug"], "M0 filtered", 0.65) for post in data.posts])
    assert tuple(metric_row(data, counts)[key] for key in ("tp", "fp", "fn")) == (48, 47, 29)


def test_m1_reproduces_checkpoint2(data, embeddings):
    scores, _ = embeddings
    for threshold in (0.75, 0.80):
        counts = np.vstack([route_post(data, scores, post["slug"], "M1", threshold) for post in data.posts])
        assert tuple(metric_row(data, counts)[key] for key in ("tp", "fp", "fn")) == (73, 50, 4)
        assert metric_row(data, counts, "documented")["tp"] == 14
        assert metric_row(data, counts, "documented")["fn"] == 0
        assert tuple(metric_row(data, counts, "silver")[key] for key in ("tp", "fp", "fn")) == (59, 50, 4)


def test_bajaj_finserv_not_bajaj_auto(data, embeddings):
    scores, _ = embeddings
    i = data.post_index["p01_flipkart_mobile_emi"]
    assert abs(scores[i, data.agent_index["bajaj_finserv"]] - 0.741158) < 2e-3
    assert abs(scores[i, data.agent_index["bajaj_auto"]] - 0.590627) < 2e-3
    assert hard_filter(data, data.posts[i], data.agents[data.agent_index["bajaj_finserv"]])
    assert route_post(data, scores, "p01_flipkart_mobile_emi", "M1", 0.75)[data.agent_index["bajaj_finserv"]]
    assert not route_post(data, scores, "p01_flipkart_mobile_emi", "M1", 0.75)[data.agent_index["bajaj_auto"]]


def test_instrument_gate_and_dated_edges(data, embeddings):
    scores, _ = embeddings
    i = data.post_index["p03_swiggy_card_only_new"]
    for slug in ("phonepe", "google_pay", "paytm"):
        j = data.agent_index[slug]
        assert not route_post(data, scores, "p03_swiggy_card_only_new", "M1", 0.75)[j]
    assert not route_post(data, scores, "p03_swiggy_card_only_new", "M1", 0.75, now="2025-12-29T00:00:00+00:00").any()
    post = data.posts[data.post_index["p02_swiggy_diwali"]]
    assert relationship_hints(data, post, data.agents[data.agent_index["hdfc_bank"]]) == []


def test_dedup_reproduces_measured_delivery(data, embeddings):
    scores, post_vectors = embeddings
    result = dedup_sequence(data, scores, post_vectors, 0.75)
    after = np.vstack([result["after"][data.post_index[post["slug"]]] for post in data.posts])
    assert tuple(metric_row(data, after)[key] for key in ("tp", "fp", "fn")) == (73, 45, 4)
    assert result["route_calls"] == 29  # 30 posts minus the exact repost
    assert result["traces"][P26] == {"kind": "exact", "routed": 0, "notified": 0, "suppressed": 0}
    assert int(result["suppressed_pairs"].sum()) == 14
    assert int((result["suppressed_pairs"] & data.positive).sum()) == 6
    assert int((result["suppressed_pairs"] & data.negative).sum()) == 8
    assert result["traces"]["p29_near_repost"]["suppressed"] == 5
    assert result["traces"]["p09_phonepe_swiggy_repeat_cashback"]["suppressed"] == 9


def test_dedup_boundary_assertions(data):
    from copy import deepcopy

    base = deepcopy(data.posts[0])
    vector = np.eye(384, dtype=np.float32)[0]
    history = [{"post": base, "key": post_dedup_key(base), "vector": vector, "notified": {1}}]
    probe = deepcopy(base)
    probe.update(content=base["content"] + " wording", created_at="2018-05-13T01:00:00+00:00")
    assert duplicate_stage(base, history, vector)["kind"] == "exact"
    assert duplicate_stage(probe, history, vector)["kind"] == "near"
    altered = deepcopy(probe)
    altered["author_agent_id"] = data.agents[0]["id"]
    assert duplicate_stage(altered, history, vector)["kind"] == "new"
    altered = deepcopy(probe)
    altered["facet_signature"] = "different"
    assert duplicate_stage(altered, history, vector)["kind"] == "new"
    assert duplicate_stage(probe, history, np.eye(384, dtype=np.float32)[1])["kind"] == "new"
    altered = deepcopy(probe)
    altered["created_at"] = "2018-05-20T00:00:01+00:00"
    assert duplicate_stage(altered, history, vector)["kind"] == "new"
    expired = deepcopy(base)
    expired["valid_until"] = "2018-05-12T00:00:00+00:00"
    expired_history = [{**history[0], "post": expired}]
    assert duplicate_stage(base, expired_history, vector)["kind"] == "exact"
    late = deepcopy(base)
    late["created_at"] = "2018-05-15T00:00:00+00:00"
    assert duplicate_stage(late, expired_history, vector)["kind"] != "exact"
    near_prior = {"post": deepcopy(probe), "key": post_dedup_key(probe), "vector": vector, "notified": {2}}
    union_probe = deepcopy(probe)
    union_probe.update(content=probe["content"] + " more", created_at="2018-05-13T02:00:00+00:00")
    assert duplicate_stage(union_probe, history + [near_prior], vector)["suppress"] == {1, 2}
    assert duplicate_stage(base, history + [near_prior], vector)["kind"] == "exact"
