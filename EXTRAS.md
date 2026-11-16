# Extras: what was added beyond the brief, quality bars, trade-offs

Copied and consolidated from `EXTRAS_LOG.md` (which remains the chronological log). Status line at the end reflects November 16, 2026.

## Beyond the brief

- **Deduplication before routing** (owner amendment): exact-repost (same-author normalized-content SHA256) and near-repost (same author + facets, cosine ≥ 0.95 within 7 days) detection with a measured chronological sequence; exact reposts stop before routing with zero judge calls and zero notifications; near reposts suppress already-notified recipients without touching relevance labels. Twelve boundary assertions + unchanged-input-hash assertion passed.
- **Owner error-review CSV** (`docs/fp_review.csv`): all 50 original false-alert pairs and 4 misses with measured float32 similarities, supporting rule IDs and date-valid edge IDs, v2 label reasons, error type and blank `owner_verdict`/`owner_reason`; a reproducible exporter (`scripts/export_fp_review.py`) validates every pair and source group (38 rule-only / 8 rule+edge / 4 edge-only) and refuses to overwrite an existing review.
- **Frozen, unexecuted M2 judge configuration** (`docs/checkpoint3_m2_config.json`): strict-JSON `decisions` envelope, opaque `agent_N` IDs mapped to canonical UUIDs, no labels in payloads, request-specific cache keys (amended pair keys + full request fingerprint, which correctly separates the two PhonePe offer texts that share a pair key), one bounded validation retry, disclosed degraded fallback, five-model comparison plan over a 314-pair candidate pool (all 77 positives, all four misses, ≤18 candidates/post), plus designed name-anonymization and injection/allowed-ID controls for the best two models.
- **Honest-metric discipline:** separate documented/silver slices that ignore each other's positives instead of manufacturing false positives; delivery suppression reported as delivery behavior, never as relevance improvement; a smaller-universe delivery score explicitly marked non-comparable.
- **Working agreements as first-class files:** owner rulings (`docs/PLAN_AMENDMENTS.md`) and execution/spend/secret safeguards (`docs/WORKING_AGREEMENT.md`) preserved verbatim; every network call timed with `time.perf_counter` under a 60-second interrupt rule.
- **Persistent, reproducible artifacts:** lossless checkpoint snapshot (label/recipient bitsets, nine-threshold sweeps, ablations, six input hashes), failing-post lists, a dependency-free 0.003 s local reproduction of every confusion count, and a runtime reset survived with all six v2 hashes verified and every M1 decision reproduced in 0.043 s.

## Quality bars (real numbers)

- Setup: Python 3.13.18, six verified package pins, seed 42; free catalogue 454 entries in 1.774 s.
- Dataset: 19 agents (16 real companies + 3 clearly fictional authors), 30 posts (24 sourced + 6 synthetic/derived), 21 reviewed sources with matching hashes, deterministic UUIDs, 77 positive labels (14 documented / 63 inferred), 463 explicit negatives, all ten hard-case specifications present; local portable validation 0.114 s.
- Embeddings: BGE-small (`BAAI/bge-small-en-v1.5`), 51 interest + 30 post vectors, 384-d, L2-normalized; load 2.381 s / compute 3.959 s after reset; exact repost cosine 1.000000, near repost 0.994695 (both reproduce checkpoint 2 exactly).
- Routing (540 pairs): raw M0@0.65 → 48/84/29 (F1 0.459); filtered M0@0.65 → 48/47/29 (F1 0.558); M1@0.75 → 73/50/4 (F1 0.730; documented recall 1.000, silver F1 0.686); after exact dedup → 73/45/4 (F1 0.749). Reproduction 0.043 s; dedup sequence 0.0437 s.
- Spend discipline: every paid call logged with tokens, latency and estimated cost; total conservative upper bound **USD 0.01004150**; M2 never executed, so no M2 cost.
- Requests: 20-second timeouts, zero automatic retries, one authorized 64-token JSON retry for Gemini Flash (2.108 s, `{"ok": true}`); JSON-object mode compatibility verified for GPT-4.1-mini and Flash.

## Trade-offs and honest costs

- **Coverage vs precision:** rules+edges buy recall (73/77 positives) at 50 extra alerts; similarity-only is precise (13 TP, 0 FP) but misses 64. The judge stage is the designed arbiter for exactly this trade-off — it was frozen but not executed, so the trade-off remains **open, honestly**.
- **Recall vs independent evidence:** documented recall (1.000) is partly circular because edges and labels share sources. We chose to say so rather than present it as generalization.
- **Policy stability vs edge cases:** the near-repost policy suppresses nine legitimate-looking deliveries on the PhonePe collision; we kept the owner's policy and disclosed the collision rather than quietly re-tuning after seeing the result.
- **Bounded execution vs completeness:** one-small-cell, ≤60 s, bounded-retries discipline meant some planned sweeps (variance trials, ten-hard-case pass, quarantine tests) were not run rather than run loosely.
- **Time-boxed scope:** Stage 1 delivers design + benchmark + measured routing experiments; the API/database/delivery worker/dashboard are design-only (see `docs/DESIGN.md` §7).

## Status (Nov 16, 2026)

Checkpoint 2 measured and accepted; reset recovery verified against six hashes; dedup and the 54-row owner review complete; M2 designed and frozen with zero paid calls; v3 label changes await owner verdicts; no held-out evaluation performed; held-out offers remain sealed.
