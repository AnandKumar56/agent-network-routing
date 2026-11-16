# Measured DEV results

All numbers are **DEV diagnostics on a 30-post, 540-pair benchmark** — not held-out evidence, not selected production thresholds. Reproduction details and per-post error lists: `docs/experiments_draft.md`, `docs/checkpoint2_failures.md`, `docs/checkpoint2_snapshot.json` (lossless bitsets; all counts reconstruct from them in 0.003 s).

## 1. Method comparison (diagnostic thresholds)

Metric definition: all-positive slice = 540 non-self pairs (77 positives / 463 explicit negatives); documented slice = 477 pairs (+14 documented positives, silver positives ignored, not counted as errors); silver slice = 526 pairs (+63). Precision = TP/(TP+FP); recall = TP/(TP+FN).

| Method | Threshold | All P/R/F1 (n=540,+77) | Documented P/R/F1 (n=477,+14) | Silver P/R/F1 (n=526,+63) | All TP/FP/FN | Failing posts |
|---|---:|---|---|---|---:|---:|
| M0 raw similarity | 0.65 | 0.364 / 0.623 / 0.459 | 0.116 / 0.786 / 0.202 | 0.306 / 0.587 / 0.402 | 48 / 84 / 29 | 26 |
| M0 similarity + hard filters | 0.65 | 0.505 / 0.623 / 0.558 | 0.190 / 0.786 / 0.306 | 0.440 / 0.587 / 0.503 | 48 / 47 / 29 | 25 |
| M1: filters + rules + dated edges | 0.75 | 0.593 / 0.948 / 0.730 | 0.219 / 1.000 / 0.359 | 0.541 / 0.937 / 0.686 | 73 / 50 / 4 | 14 |

The hard filters removed 19 competitor and 18 instrument false alerts and lost **zero** positives, but recovered none of the 29 misses: filters veto bad matches, they cannot create action opportunities. Rules and dated edges recovered most positives (73 of 77) at the cost of 50 extra alerts.

## 2. Deduplication measured before routing

Exact reposts (same-author normalized-content hash) stop before routing; near reposts (same author + facets, cosine ≥ 0.95, ≤ 7 days) route but suppress already-notified recipients. Labels unchanged throughout.

| Stage | All P/R/F1 | Documented | Silver | All TP/FP/FN |
|---|---|---|---|---:|
| M1 (checkpoint 2, stateless) | 0.593 / 0.948 / 0.730 | 0.219 / 1.000 / 0.359 | 0.541 / 0.937 / 0.686 | 73 / 50 / 4 |
| M1 after exact-repost dedup | 0.619 / 0.948 / 0.749 | 0.237 / 1.000 / 0.384 | 0.567 / 0.937 / 0.707 | 73 / 45 / 4 |

The five removed pairs are the exact repost's delivery omissions, **not** improved business-relevance judgments. Separately, near-repost suppression withheld 14 deliveries (6 labelled-positive, 8 labelled-negative pairs). The delivery-aware universe (526 pairs, +71/−455) scores 67/37/4 = 0.644/0.944/0.766 — a **smaller-universe** score that must not be compared against the 540-pair relevance benchmark or presented as "eight relevance errors repaired."

| Post | Outcome | Cosine | Routed / notified / suppressed |
|---|---|---:|---|
| `p26_exact_repost` | exact duplicate of `p01` | 1.000000 | 0 / 0 / 0 |
| `p29_near_repost` | near duplicate of `p01` | 0.994695 | 5 / 0 / 5 |
| `p09_phonepe_swiggy_repeat_cashback` | near duplicate of `p08` | 0.978604 | 9 / 0 / 9 |

The PhonePe row is a **disclosed policy collision**: first-order and repeat-order promotions share coarse facets but differ in eligibility; the near policy suppresses the repeat promotion's nine deliveries. An eligibility-aware signature is a candidate fix, left to the owner.

## 3. Threshold sweep (F1: all / documented / silver)

| Threshold | M0 raw | M0 filtered | M1 |
|---:|---|---|---|
| 0.40 | 0.252 / 0.058 / 0.216 | 0.311 / 0.076 / 0.270 | 0.311 / 0.076 / 0.270 |
| 0.45 | 0.270 / 0.063 / 0.232 | 0.340 / 0.086 / 0.296 | 0.340 / 0.086 / 0.296 |
| 0.50 | 0.296 / 0.071 / 0.256 | 0.382 / 0.101 / 0.336 | 0.382 / 0.101 / 0.336 |
| 0.55 | 0.327 / 0.085 / 0.282 | 0.435 / 0.129 / 0.385 | 0.446 / 0.128 / 0.397 |
| 0.60 | 0.387 / 0.118 / 0.337 | 0.524 / 0.195 / 0.471 | 0.577 / 0.199 / 0.527 |
| 0.65 | 0.459 / 0.202 / 0.402 | 0.558 / 0.306 / 0.503 | 0.676 / 0.280 / 0.629 |
| 0.70 | 0.448 / 0.256 / 0.434 | 0.487 / 0.345 / 0.479 | 0.712 / 0.337 / 0.667 |
| 0.75 | 0.286 / 0.333 / 0.270 | 0.289 / 0.353 / 0.274 | 0.730 / 0.359 / 0.686 |
| 0.80 | 0.026 / 0.000 / 0.031 | 0.026 / 0.000 / 0.031 | 0.730 / 0.359 / 0.686 |

M1's recipient matrix is **exactly identical at 0.75 and 0.80** — not an accidentally equal aggregate. See the caveat below on what drives this.

## 4. The four misses

All four missed positives belong to one post: `p12_hdfc_online_card_rewards` (an HDFC online-card-rewards offer) misses **Flipkart, Amazon India, Myntra and MakeMyTrip** at similarities 0.636–0.693. The current rule set lacks a card-provider-to-merchant direction; these four are included in the designed judge-stage candidate pool (≥ 0.50 similarity), so the frozen-but-unexecuted M2 would have adjudicated them.

Every other M1 failing post has only extra recipients (full list: `docs/checkpoint2_failures.md`); the 50 extra-alert pairs all have rule and/or dated-edge support, and **none** is similarity-only (all 50 are below similarity 0.75).

## 5. The instructive example: Bajaj Finserv vs Bajaj Auto

Flipkart's mobile No-Cost-EMI post (cosine with each): **Bajaj Finserv 0.741158** — notified (EMI-financing capability rules + the date-valid May 2018 financing edge). **Bajaj Auto 0.590627** — not notified at the diagnostic thresholds (no financing rule or partner hint; rejected by raw similarity too, though a 0.55 raw threshold would wrongly admit it). The instrument gate alone does not reject a manufacturer with no payment role — the capability profile and dated-edge evidence do. This is the brand-name trap the design exists to avoid: "Bajaj" the financier and "Bajaj" the motorcycle maker are different businesses.

Other inspectable rows: Swiggy Diwali → PhonePe is notified via `food_checkout_complement` + the valid March 2018 payment edge despite cosine 0.590314; the card-only Swiggy offer reaches ICICI (card issuer) but the instrument gate vetoes even PhonePe's valid payment hint, and rejects UPI-only Google Pay and Paytm despite raw cosine ≥ 0.65.

## 6. Source ablation at 0.75 (why the plateau is what it is)

| Variant | P / R / F1 | TP / FP / FN |
|---|---|---:|
| Filtered similarity only | 1.000 / 0.169 / 0.289 | 13 / 0 / 64 |
| Similarity + rules | 0.607 / 0.922 / 0.732 | 71 / 46 / 6 |
| Similarity + dated edges | 0.707 / 0.377 / 0.492 | 29 / 12 / 48 |
| Full M1 | 0.593 / 0.948 / 0.730 | 73 / 50 / 4 |

## 7. Honest statements (required)

1. **Documented recall is partly circular.** Dated relationship edges and documented positive labels were derived from the same public sources; recovering those labels with those edges is a consistency check, not independent generalization evidence. Neither the documented slice nor the shared DEV negatives is a source-independent held-out benchmark.
2. **M1 at 0.75 and 0.80 is driven by rules and dated edges, not similarity.** Filtered similarity alone contributes only 13 TP / 0 FP; all 50 original false-alert pairs have rule or edge support. The identical recipient matrices at 0.75/0.80 do not establish a robust semantic threshold.
3. **All numbers are DEV.** The 30 posts include synthetic fixtures and shared-source series; adjusting anything after seeing these results is development, and no held-out evaluation has run. Held-out current offers remain sealed; the judge prompt and thresholds are frozen before their execution.
4. **M2 was designed and frozen but not executed.** The five-model judge comparison (`docs/checkpoint3_m2_config.json`: 314-pair pool including all 77 positives and all four misses; anonymization and injection controls) ran zero paid calls. No model or production threshold is selected.
