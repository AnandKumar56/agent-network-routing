# Routing experiments draft

This file preserves measured results locally because `/content` can disappear after a runtime reset. The dataset is DEV, not held-out. Sections are chronological; the newest checkpoint section records current status. Earlier pending statements describe the state at that earlier step.

## Trial pool compatibility

The existing cached catalogue confirms the original three IDs and unchanged USD input/output prices per million tokens: NeMo 0.02/0.03, Gemma 3 4B 0.04/0.08, and Llama 3.1 8B 0.05/0.08. No new catalogue fetch or setup rerun was used.

| Additional model | USD input/output per million | JSON mode, output cap 32 | Seconds | Input/output tokens | Estimated USD cost |
|---|---:|---|---:|---:|---:|
| `google/gemini-2.5-flash` | 0.30 / 2.50 | Failed: `Here is` | 2.066 | 12 / 2 | 0.00000860 |
| `openai/gpt-4.1-mini` | 0.40 / 1.60 | Passed: `{"ok": true}` | 1.937 | 22 / 5 | 0.00001680 |

These are compatibility tests only. Neither is a final model choice. Each request had a 20-second timeout, zero automatic retries and a row in `/content/usage.csv`. New-call spend is USD 0.00002540; earlier spend is below USD 0.01, giving a conservative cumulative upper bound of USD 0.01002540. No ledger reconciliation or reservations are used.

## Checkpoint 2 results

Pending the owner-uploaded `/content/data.zip`, extracted to `/content/data`. The first extraction attempt found no ZIP at that path. No alternate dataset or Drive plumbing was substituted.

- BGE-small embeddings: not measured.
- M0 threshold sweep: not measured.
- M1 dated relationship rules and instrument gate: not measured.
- Documented/inferred metrics, failing posts and Bajaj Finserv versus Bajaj Auto: pending, not passed.

## DEV input received

The owner-uploaded ZIP was extracted into `/content/data`, omitting source bodies. The runtime now reports only the requested counts:

| Agents | Posts | Label rows | Non-self pairs | Documented positives | Silver positives |
|---:|---:|---:|---:|---:|---:|
| 19 | 30 | 30 | 540 | 14 | 63 |

There are 77 positives and 463 explicit non-self negatives. This is the approved DEV set. Drive history, saved-notebook sync, README and dataset-review wording are deferred until the session end, and only if time permits. The original session start remains `2026-11-15T03:59:03.629000+00:00`. At 16:14:56 IST the elapsed time was about 405.9 minutes, with about 75 minutes until the 17:30 soft checkpoint.

## Authorized Gemini Flash retry

Exactly one retry used the same JSON instruction, `temperature=0`, JSON-object mode and a 64-token output cap. It returned exactly `{"ok": true}` with finish reason `stop`. No other smoke tests were run.

| Model | Output cap | JSON valid | Seconds | Input/output tokens | Estimated USD cost |
|---|---:|---|---:|---:|---:|
| `google/gemini-2.5-flash` | 64 | Yes | 2.108 | 12 / 5 | 0.00001610 |

This establishes compatibility for this tiny request at 64 tokens; it does not prove routing quality or conclusively explain the 32-token failure. Both Flash and GPT-4.1-mini remain comparison candidates. Three new calls total USD 0.00004150, with a conservative cumulative upper bound below USD 0.01004150. The retry appended to `/content/usage.csv`.

## Step 1: BGE-small embeddings measured

`BAAI/bge-small-en-v1.5` produced 51 separate interest vectors and 30 post vectors, each with 384 dimensions. Post input is title, newline and content; both interests and posts use `embed()` with no query prefix. Vectors are L2-normalized. An agent score is the maximum cosine across its interest statements, not a probability or an average of its profile.

| Measurement | Value |
|---|---:|
| Model load/download, seconds | 3.021 |
| Embedding computation, seconds | 5.519 |
| Original vs exact repost cosine | 1.000000 |
| Original vs near repost cosine | 0.994695 |
| Near repost meets cosine >= 0.95 | Yes |

The exact and near fixtures share the author's ID and facet signature. Their normalization hashes distinguish the near repost from the exact repost. The near cosine is now measured, not assumed. Notification suppression remains a separate sequence-level policy; high similarity by itself does not suppress a notification.

Runtime artifacts: `/content/data/embeddings.json` and `/content/results/bge_scores.npz`. Embedding inference used the already-installed package; no setup, authorization or client construction was repeated. This local table survives a runtime reset; the larger runtime artifacts remain temporary.

## Step 2: M0 raw and M0 with shared filters

Raw M0 thresholds the best interest cosine only. The filtered baseline additionally excludes the author, inactive recipients, non-published posts, expired posts, excluded industries, competitors without explicit subscriptions and incompatible payment-instrument roles. Every historical post uses `now = as_of`. Merchants or manufacturers without payment-instrument capability are not rejected by the instrument gate. No notification quota history, fan-out cap, content screen or duplicate-notification suppression is included in these stateless pair baselines. Those later policy stages must not be mistaken for semantic improvements.

### Metric definition and counts

All-positive metrics use 540 non-self pairs: 77 positives and 463 explicit DEV negatives. The documented-positive slice uses 477 pairs: 14 documented positives plus the same 463 negatives, ignoring silver positives rather than calling them false positives. The silver slice uses 526 pairs: 63 silver positives plus the same 463 negatives, ignoring documented positives. The shared negatives are DEV policy/inference judgments, not independently documented negative evidence. Split precision therefore does not mean a fully documented benchmark. `n` is evaluated pairs; `+` is positive support. Precision's denominator is TP+FP, recall's is TP+FN; counts below make each auditable.

### Threshold stability: F1 all / documented / silver

| Threshold | M0 raw | M0 filtered |
|---:|---:|---:|
| 0.40 | 0.252 / 0.058 / 0.216 | 0.311 / 0.076 / 0.270 |
| 0.45 | 0.270 / 0.063 / 0.232 | 0.340 / 0.086 / 0.296 |
| 0.50 | 0.296 / 0.071 / 0.256 | 0.382 / 0.101 / 0.336 |
| 0.55 | 0.327 / 0.085 / 0.282 | 0.435 / 0.129 / 0.385 |
| 0.60 | 0.387 / 0.118 / 0.337 | 0.524 / 0.195 / 0.471 |
| 0.65 | 0.459 / 0.202 / 0.402 | 0.558 / 0.306 / 0.503 |
| 0.70 | 0.448 / 0.256 / 0.434 | 0.487 / 0.345 / 0.479 |
| 0.75 | 0.286 / 0.333 / 0.270 | 0.289 / 0.353 / 0.274 |
| 0.80 | 0.026 / 0.000 / 0.031 | 0.026 / 0.000 / 0.031 |

Counts for each column's triple: all n=540/+77; documented n=477/+14; silver n=526/+63. Full precision, recall, F1 and confusion counts for every threshold are saved in `/content/results/m0_metrics.json`.

### Diagnostic DEV maxima, not selected thresholds

| Method | Threshold | All P/R/F1 (n=540,+77) | Documented P/R/F1 (n=477,+14) | Silver P/R/F1 (n=526,+63) |
|---|---:|---:|---:|---:|
| M0 raw | 0.65 | 0.364 / 0.623 / 0.459 | 0.116 / 0.786 / 0.202 | 0.306 / 0.587 / 0.402 |
| M0 filtered | 0.65 | 0.505 / 0.623 / 0.558 | 0.190 / 0.786 / 0.306 | 0.440 / 0.587 / 0.503 |

At 0.65, raw M0 has TP=48, FP=84, FN=29; filtered M0 has TP=48, FP=47, FN=29. Both have documented TP=11/FN=3 and silver TP=37/FN=26. The filters removed 19 competitor errors and 18 instrument errors, with no positive lost. They did not recover a single missed action opportunity. Raw M0 fails on 26 posts; filtered M0 on 25.

Inspectable examples:
- Flipkart EMI to Bajaj Finserv: cosine 0.741158, best interest `No Cost EMI for mobile phones and appliances`, accepted by both at 0.65. Bajaj Auto: 0.590627, best interest `Motorcycle product launches and vehicle demand`, rejected by both at 0.65 but would be accepted at a 0.55 raw threshold. The instrument gate does not itself reject a manufacturer with no payment role.
- Swiggy Diwali to PhonePe: cosine 0.590314, best interest `Cashback campaigns at food-delivery checkout`. Both methods miss it at 0.65 despite the documented checkout relationship.
- Card-only Swiggy offer: ICICI 0.750701 is accepted. Google Pay 0.651691 and Paytm 0.664607 cross the raw threshold, but the instrument gate rejects both. PhonePe 0.642068 is below 0.65 and also explicitly instrument-incompatible.

## Step 3 and checkpoint 2: M1 with real temporal enforcement

M1 accepts an eligible pair if similarity crosses the swept threshold, a capability rule hits, an explicit subscription applies, or a date-valid relationship supplies a hint. Rule hits and partner hints are unconditional additions in this coverage baseline, not the final banded/judged pipeline. `valid_from <= as_of` and `as_of <= valid_until` when an end exists are implemented in `relationship_hints()`, not just written in policy. Static `declared_partners` is not a candidate source. Competitor and instrument filters remain binding after combining all sources.

Profiles and sector-competitor annotations are still static November 2026 DEV simulations. The Flipkart/Bajaj May 13 edge uses a May 14 retrospective campaign report; temporal validity does not imply that a live router knew that evidence on May 13. Undated current product relationships begin at their recorded first-observed snapshot, not an invented historical start.

### Three-method diagnostic comparison

These are each method's highest pooled DEV F1 in this sweep, not selected production thresholds. Values are precision / recall / F1. `n` is evaluated pairs and `+` is positive support; other-basis positives are ignored in each split, while the same 463 DEV negatives are included.

| Method | Diagnostic threshold | All P/R/F1 (n=540,+77) | Documented P/R/F1 (n=477,+14) | Silver P/R/F1 (n=526,+63) |
|---|---:|---:|---:|---:|
| M0 raw | 0.65 | 0.364 / 0.623 / 0.459 | 0.116 / 0.786 / 0.202 | 0.306 / 0.587 / 0.402 |
| M0 filtered | 0.65 | 0.505 / 0.623 / 0.558 | 0.190 / 0.786 / 0.306 | 0.440 / 0.587 / 0.503 |
| M1 | 0.75 | 0.593 / 0.948 / 0.730 | 0.219 / 1.000 / 0.359 | 0.541 / 0.937 / 0.686 |

| Method | All TP/FP/FN | Documented TP/FP/FN | Silver TP/FP/FN | Posts with at least one error |
|---|---:|---:|---:|---:|
| M0 raw | 48 / 84 / 29 | 11 / 84 / 3 | 37 / 84 / 26 | 26 |
| M0 filtered | 48 / 47 / 29 | 11 / 47 / 3 | 37 / 47 / 26 | 25 |
| M1 | 73 / 50 / 4 | 14 / 50 / 0 | 59 / 50 / 4 | 14 |

### Threshold stability: F1 all / documented / silver

Each triple uses all n=540/+77, documented n=477/+14, silver n=526/+63.

| Threshold | M0 raw | M0 filtered | M1 |
|---:|---:|---:|---:|
| 0.40 | 0.252 / 0.058 / 0.216 | 0.311 / 0.076 / 0.270 | 0.311 / 0.076 / 0.270 |
| 0.45 | 0.270 / 0.063 / 0.232 | 0.340 / 0.086 / 0.296 | 0.340 / 0.086 / 0.296 |
| 0.50 | 0.296 / 0.071 / 0.256 | 0.382 / 0.101 / 0.336 | 0.382 / 0.101 / 0.336 |
| 0.55 | 0.327 / 0.085 / 0.282 | 0.435 / 0.129 / 0.385 | 0.446 / 0.128 / 0.397 |
| 0.60 | 0.387 / 0.118 / 0.337 | 0.524 / 0.195 / 0.471 | 0.577 / 0.199 / 0.527 |
| 0.65 | 0.459 / 0.202 / 0.402 | 0.558 / 0.306 / 0.503 | 0.676 / 0.280 / 0.629 |
| 0.70 | 0.448 / 0.256 / 0.434 | 0.487 / 0.345 / 0.479 | 0.712 / 0.337 / 0.667 |
| 0.75 | 0.286 / 0.333 / 0.270 | 0.289 / 0.353 / 0.274 | 0.730 / 0.359 / 0.686 |
| 0.80 | 0.026 / 0.000 / 0.031 | 0.026 / 0.000 / 0.031 | 0.730 / 0.359 / 0.686 |

M1 has exactly the same recipient matrix at 0.75 and 0.80, not just an accidentally identical aggregate F1. This plateau is driven by rule and partner additions. It does not establish that either threshold generalizes to unseen posts.

### Inspectable routing examples

| Post and recipient | Cosine | M0 raw at 0.65 | Filtered M0 at 0.65 | M1 at 0.75 | Inspectable reason |
|---|---:|---|---|---|---|
| Flipkart EMI to Bajaj Finserv | 0.741158 | Yes | Yes | Yes | EMI capability rules plus the date-valid May 2018 financing edge |
| Flipkart EMI to Bajaj Auto | 0.590627 | No | No | No | No financing rule or partner hint; below the diagnostic semantic thresholds |
| Swiggy Diwali to PhonePe | 0.590314 | No | No | Yes | `food_checkout_complement` plus the March 2018 payment edge |
| Card-only Swiggy to ICICI | 0.750701 | Yes | Yes | Yes | Card capability plus the date-valid offer edge |
| Card-only Swiggy to PhonePe | 0.642068 | No | No | No | Instrument gate vetoes even its rule and date-valid payment hint |
| Card-only Swiggy to Google Pay | 0.651691 | Yes | No | No | UPI-only profile fails the card instrument gate |
| Card-only Swiggy to Paytm | 0.664607 | Yes | No | No | UPI-only profile fails the card instrument gate |

`declared_partner_types` in the EMI rule trace means the post's structured `partner_types_wanted` capability tags. It does not read the agent profile's static `declared_partners`. Bajaj Auto is not universally hard-banned: genuine two-wheeler financing complementarity remains allowed. At a low semantic threshold an irrelevant manufacturer can still slip through M1's semantic branch, so this baseline is not a final relevance guarantee.

### Temporal before and after, without pretending the recipient vanished

| Post clock | Candidate | Unsafe counterfactual, ignoring dates | Actual M1 hints with dates enforced | Actual recipient result |
|---|---|---|---|---|
| Swiggy Diwali, 2020-11-12 | HDFC Bank | `co_brand_card`, valid_from 2023-07-26 | None, despite HDFC in static `declared_partners` | Still notified by `food_checkout_complement`, not by the future edge |
| Same 2020 post | PhonePe | March 2018 payment relationship | March 2018 `payment_partner` retained | Notified through valid evidence and the generic rule |

Assertions verified every actual M1 relationship hint against that post's `as_of` and edge end date. A pre-March-22-2018 PhonePe hint is excluded; the expired 2025 ICICI/Swiggy offer hint is absent from a November 2026 post. The separate expired-offer clock returns 6 raw-similarity recipients but zero filtered-M0 and M1 recipients. All 30 per-post calls of the now-aware routing helper reproduced each of the three measured matrices. A synthetic subscription copy verified the competitor exception without changing DEV profiles or labels; a merchant with no payment role was not instrument-gated.

### Where each method fails

- **M0 raw, similarity stage:** 84 false alerts and 29 misses. Topic overlap admits competitors and wrong payment roles. At 0.65 the shared layer removes 19 competitor and 18 instrument false alerts.
- **Filtered M0, complementarity stage:** still misses 29 positives, including Swiggy to PhonePe. Filters veto bad matches but cannot create action opportunities. It still has 47 false alerts.
- **M1, candidate-source scope:** high recall but 50 false alerts. At 0.75, 38 false alerts are rule-only, 8 have both rule and dated-edge support, and 4 are edge-only. None is solely a high-similarity alert. Its only four missed positives are Flipkart, Amazon India, Myntra and MakeMyTrip on `p12_hdfc_online_card_rewards`; the current rules lack a suitable card-provider-to-merchant direction.
- **Separate delivery/safety policies:** these stateless baselines do not implement notification deduplication or content quarantine. M1 still emits the five EMI recipients for `p26_exact_repost`, contributing five false alerts. A measured near-repost cosine is not a passed no-second-notification or cache test. Quiet synthetic fixtures at a threshold are not proof of quarantine. No ten-hard-case pass count is claimed.

### Investigation: more relationship evidence is not automatically better

At the same 0.75 threshold, the following ablation isolates sources. All rows use n=540/+77.

| Variant | P / R / F1 | TP / FP / FN |
|---|---:|---:|
| Filtered similarity only | 1.000 / 0.169 / 0.289 | 13 / 0 / 64 |
| Similarity plus rules | 0.607 / 0.922 / 0.732 | 71 / 46 / 6 |
| Similarity plus dated edges | 0.707 / 0.377 / 0.492 | 29 / 12 / 48 |
| Full M1 | 0.593 / 0.948 / 0.730 | 73 / 50 / 4 |

Adding dated edges on top of rules recovers two positives but adds four false alerts, slightly lowering F1 from 0.732 to 0.730. No final source policy is selected from this DEV comparison.

Concrete failures:
- `p08_phonepe_swiggy_first_cashback`: the Swiggy-specific introduction wrongly reaches Zomato, Flipkart, Amazon India, Myntra, MakeMyTrip, HDFC, ICICI and Axis. Broad UPI-merchant and card-role rules miss the campaign's scope.
- `p18_bajaj_finserv_bike_finance`: wrong extras are Amazon India, MakeMyTrip, HDFC, ICICI and Axis. Date-valid retail/travel partners are not necessarily partners for every motorcycle loan; a general EMI capability is not enough either.
- `p26_exact_repost`: wrong new recipients are HDFC, ICICI, Axis, Bajaj Finserv and TVS Credit. This requires the already-agreed exact-repost policy, not a different embedding threshold.

Checkpoint 2 is complete and awaits Anand's reply. Models and thresholds are still unselected. Flash passed its single authorized 64-token JSON retry; no further paid calls followed. New-call spend is USD 0.00004150, with earlier spend owner-confirmed below USD 0.01. Drive reconciliation, saved-notebook sync, README and dataset-review wording remain deferred.

### Local persistence and reproduction check

- `docs/checkpoint2_failures.md` lists failing posts for all three methods and every M1 missed/extra recipient.
- `docs/checkpoint2_snapshot.json` preserves all nine thresholds' confusion counts, all diagnostic label/recipient bitsets, the temporal example, source ablations, spend and six input hashes. It contains no source bodies. Bit `j` refers to `agent_order[j]`; `count_order` specifies documented TP, silver TP and shared-negative FP. These counts reconstruct every split's precision, recall and F1, including their supports.
- A dependency-free local check reproduced all diagnostic confusion counts from the saved bitsets in 0.003 seconds. All six runtime DEV input hashes match their local files, so there is no metadata-copy discrepancy to fix.
- The snapshot was measured at 16:49:36 IST, about 440.5 minutes from the original start. Checkpoint 2 finished before the 17:30 soft checkpoint. This does not reset earlier elapsed time or spending.

The exact-repost raw dot product is 1.000000119 in float32, a tiny rounding overshoot of the mathematical cosine bound. The six-decimal table reports 1.000000; the near cosine and threshold outcomes are unaffected. The snapshot keeps the raw measurement rather than silently altering it.

## Checkpoint 3 work: authorization and honest framing

Anand accepted checkpoint 2 and authorized deduplication first, a 54-pair owner-review CSV, then a five-model M2 comparison and two cheap controls on the best two models. No v2 labels will change without his returned verdict and reason. `stage1-dataset-v3` and the v2/v3 score comparison are deferred until that adjudication arrives. The sealed current-offer set must not be inspected, and prompts and thresholds must be frozen before held-out execution. Variance trials remain unauthorized until Anand chooses the top two.

**Documented recall is partly circular.** Dated relationship edges and documented positive labels were derived from the same public sources. Recovering those labels using those edges is a consistency check, not independent evidence that M1 generalizes to new relationships or campaigns. Static November 2026 profiles add another historical limitation. Neither the documented slice nor its shared DEV negatives constitute a source-independent held-out benchmark.

**M1 at 0.75 and 0.80 is driven by rules and dated edges, not similarity.** At 0.75, filtered similarity alone yields 13 TP and zero FP; rules and edges expand this to 73 TP and 50 FP. All 50 original false-alert pairs have rule or edge support. Identical recipient matrices at 0.75 and 0.80 are therefore not evidence of a robust semantic threshold. The five exact-repost pairs are delivery-stage omissions in checkpoint 2, not mistakes about those companies' business relevance.

The clock at the start of this authorized continuation was 19:22:40 IST on November 15. The original start remains `2026-11-15T03:59:03.629000+00:00`; elapsed time includes the checkpoint pause. Monday November 16, 2026, 10:00 AM IST remains the deadline. No setup, notebook review, ledger reconciliation or held-out inspection was repeated.

### Authorized reset recovery

The dedup measurement stopped immediately because the runtime had reset. A bounded check found all original arrays, the client, DEV inputs and `/content/usage.csv` absent. Anand explicitly selected **Minimal restore**: restore the approved local v2 inputs, only necessary prior package pins and the authorized client; recompute BGE unchanged. Drive work, catalogue fetches, smoke tests and label changes remain excluded. This later authorization supersedes the earlier no-setup-rerun rule only for this recovery.

Dependency restoration took 18.282 seconds. Browser transfer failed, including its sole bounded CORS retry; the prepared direct payload restored all six unchanged JSON files and the checkpoint snapshot in 0.013 seconds. Every input hash matches checkpoint 2. BGE load took 2.381 seconds and recomputation 3.959 seconds with the same model, title/newline/content inputs, separate interests, no query prefix and L2 normalization. Exact/near cosines exactly reproduce the original float32 values. All 540 M1 decisions reproduce checkpoint 2 in 0.043 seconds, including the 0.75/0.80 plateau. Earlier spending is not reset: the conservative pre-reset upper bound remains USD 0.01004150.

### Dedup measured before routing

Chronological history uses `created_at`, same-author normalized-content SHA256 first, then same-author/same-facet cosine >=0.95 within seven days. Exact matches take priority over all near matches. Near suppression unions recipients actually notified across matching earlier posts. Runtime copies receive `status="duplicate"` and `duplicate_of`; v2 files and labels stay unchanged. The sequence took 0.043712 seconds. Twelve dedup boundary assertions passed, with an additional unchanged-input-hash assertion.

| Stage | All P/R/F1 (n=540,+77) | Documented (n=477,+14) | Silver (n=526,+63) | All TP/FP/FN |
|---|---:|---:|---:|---:|
| Checkpoint-2 stateless M1 | 0.593 / 0.948 / 0.730 | 0.219 / 1.000 / 0.359 | 0.541 / 0.937 / 0.686 | 73 / 50 / 4 |
| M1 routing after exact dedup | 0.619 / 0.948 / 0.749 | 0.237 / 1.000 / 0.384 | 0.567 / 0.937 / 0.707 | 73 / 45 / 4 |

The five removed pairs are exact-repost delivery omissions, not improved business-relevance judgments. The remaining 45 extras are disputes against v2 relevance labels; the four HDFC-to-merchant misses remain. Near posts still route normally, so suppression does not manufacture relevance false negatives in this table.

| Post | Dedup outcome | Cosine | Routed / new notifications / suppressed |
|---|---|---:|---:|
| `p26_exact_repost` | Exact duplicate of `p01` | 1.000000 | 0 / 0 / 0 |
| `p29_near_repost` | Near duplicate of `p01` | 0.994695 | 5 / 0 / 5 |
| `p09_phonepe_swiggy_repeat_cashback` | Near duplicate of `p08` | 0.978604 | 9 / 0 / 9 |

**Policy risk:** the first-order and repeat-order PhonePe promotions have different eligibility but the same coarse facets. The authorized near-repost policy suppresses the repeat promotion's nine M1 deliveries. This is not just a paraphrase fixture. We retain the owner's policy and disclose the collision rather than narrowing facets, changing the 0.95 threshold or relabelling either post ourselves. An eligibility-aware signature could avoid this collision but would require a later owner decision.

Delivery-aware evaluation excludes the 14 legitimately suppressed pairs from its universe, without modifying labels. It has 526 pairs, 71 positives and 455 negatives: TP/FP/FN=67/37/4, P/R/F1=0.644/0.944/0.766. The documented slice has n=467/+12, TP/FP/FN=12/37/0, P/R/F1=0.245/1.000/0.393; silver has n=514/+59, 55/37/4, 0.598/0.932/0.728. Six positive and eight negative deliveries were suppressed. This smaller-universe delivery score must not be presented as the same relevance benchmark or as eight business-relevance errors repaired.

### Owner review prepared, labels unchanged

`docs/fp_review.csv` contains all **50 original false-alert pairs and four original misses**, including the five now-blocked exact-repost deliveries. It includes post ID/title, agent name/ID/slug, measured similarity, all supporting rule and date-valid edge IDs, the v2 one-line reason, error type and empty `owner_verdict`/`owner_reason`. Verdict choices are `system_wrong`, `label_wrong`, or `unsure`; Anand should add his reason in `owner_reason`. A generic v2 negative reason is shown as generic evidence, not expanded into an invented campaign-specific judgment.

`docs/checkpoint3_review_measurements.json` preserves the exact float32-derived similarities and source IDs. `python3 scripts/export_fp_review.py` reproduces the CSV from those measurements and approved metadata, verifies all 54 original pairs and the 38 rule-only / 8 rule-plus-edge / 4 edge-only groups, and refuses to overwrite an existing review. No v3 labels or v2/v3 scores exist until Anand returns adjudication with reasons.
