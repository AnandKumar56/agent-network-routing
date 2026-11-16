# Known limits

Stated plainly. Each limit is either measured or an explicitly unmeasured gap; nothing here is hand-waved.

## Evaluation limits

- **DEV, not held-out.** Every number in `docs/RESULTS.md` comes from a 30-post development benchmark (540 non-self pairs). Held-out current offers remain sealed and were never inspected. Any threshold chosen after seeing DEV results is a development choice, not validation.
- **Documented recall is partly circular.** Dated edges and documented labels share the same public sources, so documented recall (1.000 for M1) is partly source-consistency, not independent generalization. The shared 463 negatives are DEV policy/inference judgments, not documented negative evidence; split precision therefore overstates benchmark quality.
- **Small and dependent dataset.** 77 positive labels (14 documented / 63 inferred) over 30 posts; shared-source posts carry `series_id` and are not independent samples. One post owns all four misses.
- **The 0.75/0.80 plateau is not threshold robustness.** M1's recipient matrix is identical at both thresholds because rules and dated edges dominate; all 50 false-alert pairs have rule/edge support and similarity below 0.75. This plateau says nothing about semantic-threshold generalization.
- **Delivery-aware score is a smaller universe.** The 526-pair delivery score excludes 14 legitimately suppressed pairs; it must not be compared with the 540-pair relevance score or read as "eight relevance errors repaired."

## Policy limits (measured, disclosed)

- **PhonePe near-repost collision.** The first-order and repeat-order PhonePe promotions have different eligibility but identical coarse facets; the authorized near-repost policy (same author + facets, cosine ≥ 0.95, ≤ 7 days) suppresses the repeat promotion's nine deliveries. We retained the owner's policy and disclosed the collision instead of silently narrowing facets or changing the threshold. An eligibility-aware signature would need an owner decision and is unmeasured.
- **Near-repost suppression is measured once, not stress-tested.** Suppression semantics (union of actually-notified recipients) passed twelve boundary assertions, but no broader notification-suppression pass (many-author, cross-day, cache-interaction) was run.
- **Quarantine and abuse handling are designed, not measured.** No content quarantine pass, rate-limit test, or injection-attack evaluation was executed. Vague/spam/injection fixtures were scored in the (unexecuted) M2 pool; a threshold-quiet fixture is not proof of quarantine.
- **No full ten-hard-case pass count is claimed.** All ten specifications are present and internally consistent in the dataset; hard case 4 is the owner-approved historical market update, never a verified UPI cashback promotion.

## Stage-1 scope limits

- **No app was built.** No FastAPI service, database, webhook delivery worker, dashboard, quotas or fan-out state exists. The routing core logic is prototyped in Colab and (optional minimal build) as a Python package; delivery, feedback execution and multi-tenancy are design-only.
- **Static profiles.** Agent profiles are November 2026 simulations checked against public sources, not historical reconstructions; a May 2018 post is routed with what is knowable from today's profile plus date-valid edges. Temporal validity of an edge does not imply a live router knew that evidence at post time (the Flipkart/Bajaj May 13 edge uses a May 14 retrospective report).
- **`declared_partners` is deliberately not a candidate source.** Static partner lists are excluded so that undated convenience cannot shortcut dated evidence; this also means the router can miss declared-but-undated partnerships by design.
- **M2 (judge stage) is frozen but unexecuted.** No five-model comparison, no anonymization or injection control results, no variance trials, no model selection, no judge-threshold tuning. `docs/checkpoint3_m2_config.json` preserves exactly what would run.
- **Owner adjudication pending.** `docs/fp_review.csv` holds all 54 original error pairs with blank `owner_verdict`/`owner_reason`; no v3 label changes exist, and none will be made without returned verdicts and reasons.
- **Spend.** Total paid usage stays under a conservative upper bound of USD 0.01004150 (connectivity/compatibility smoke tests only). M2 cost was never incurred.
