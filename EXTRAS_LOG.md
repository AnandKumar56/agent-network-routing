# Stage 1 extras log

## Beyond the brief

- Colab setup uses six verified package pins, seed 42, manual-only secret access, timed requests and conservative spend reservations. The original caches are persistent on Drive; the latest live runtime temporarily uses `/content/cache`, with Drive still absent. The official Colab MCP release is pinned to `b85ab6ec5206e06fdd289ff4ff3f9c4ee767b422`.
- The approved routing amendments and working agreement are preserved separately in `docs/PLAN_AMENDMENTS.md` and `docs/WORKING_AGREEMENT.md`.
- Dataset: sourced company simulations, clearly fictional safety authors, reasoned positive and negative labels, reviewed source snapshots and deterministic UUIDs. Checkpoint 1 is in `docs/DATASET_REVIEW.md`.

## Quality bars to report

- Setup: Python 3.13.18; all six package pins verified; Drive check passed in 0.047 seconds.
- Free model catalogue: 454 entries in 1.774 seconds; known finite chat rates loaded for 400 entries.
- One Mistral NeMo smoke completion: valid JSON in 2.662 seconds; 24 input and 6 output tokens; estimated USD 0.00000066, approximately INR 0.000065. Response and usage are saved to Drive.
- Dataset integrity validation passed on November 15, 2026: 19 agents (16 real companies, 3 fictional authors), 30 posts (24 sourced, 6 synthetic/derived), 20 reviewed sources with matching hashes, 77 positive labels (14 documented, 63 inferred) and 493 explicit negative labels.
- The approved DEV update passed local portable validation in 0.114 seconds and optional source-body hash validation in 0.110 seconds: 21 reviewed sources, dated relationships, static-profile disclosure and all ten specifications preserved. The evaluated universe excludes 30 author-self pairs: 14 documented positives, 63 silver positives and 463 negatives.
- All ten hard-case specifications are present and internally consistent. This is not a routing pass: hard case 4 is the owner-approved DEV market update, never a verified UPI cashback pass; near-duplicate cosine is unmeasured.
- The saved notebook's 22 code cells compile, contain at most 25 lines and have no saved outputs. No further paid calls were made during dataset construction or validation.
- Routing precision, recall, F1, hard-case passes, cache savings and routing latency are not yet measured. No final model or thresholds have been chosen.
- Latest manual Colab execution, reviewed around 15:35 IST: 22 populated code cells have completed outputs without Python exceptions; Drive and DEV checks still fail. Catalogue 452 entries in 5.629 seconds; 398 known finite chat prices. A second NeMo smoke passed in 2.374 seconds, with 24/6 tokens and USD 0.00000066 estimated cost. Known cumulative estimated spend: USD 0.00000132. No cells or requests were rerun during this output review.

## Trade-offs and limits to state

- This session is Stage 1 only. No API app, database, delivery worker or dashboard has been built.
- The model shortlist is a provisional trial pool, not an unrestricted cheapest-model ranking or a quality result.
- The approved DEV input location is `/content/drive/MyDrive/agent-network-experiments/data`; no clone URL is needed. That folder is not yet visible in the latest live kernel. The local project is not a Git repository.
- Historical offers will be evaluated with `now = as_of`; expiry is a separate test after `valid_until`. A sourced simulation does not imply company participation or endorsement.
- Dataset approval is DEV-only. PhonePe's historical source reports UPI use and instant cashbacks but not UPI-only promotional eligibility. Its five merchant action labels are silver, not redemption entitlements. Later unseen offers will be held out.
- Profiles are scoped, static November 2026 simulations. Shared-source posts are not independent samples; unknown offer expiry stays null. Generic card promotion opportunities and issuer-specific balance conversion use distinct DEV label interpretations.
- A cache-location change hid the original ledger and caused a new uncached smoke request. Preserve both histories and reconcile them before paid experiments. Local cache success is not proof of Drive persistence.
- Original session start: `2026-11-15T03:59:03.629000+00:00`; original planning stop: `2026-11-15T07:19:03.629000+00:00`, now superseded, not reset. Soft progress checkpoint: Sunday 17:30 IST. Real submission deadline: Monday 10:00 AM IST.

## Checkpoint 2 — measured DEV baselines, November 15, 2026

This is the latest status; earlier entries above are historical. The owner-uploaded `/content/data.zip` replaced the Drive input requirement. No ledger reconciliation or reservations are prerequisites now; paid calls append model, tokens and cost to `/content/usage.csv`. No setup rerun or notebook review was undertaken for this checkpoint.

- Evaluated all 540 non-self pairs: 77 positives (14 documented, 63 silver) and 463 negatives. BGE-small produced 51 interest vectors and 30 post vectors, each 384-dimensional. Load/download took 3.021 seconds; embedding computation took 5.519 seconds.
- Original/exact repost cosine: **1.000000**; original/near repost cosine: **0.994695**, exceeding 0.95. This does not establish notification suppression or judge-cache savings.
- Diagnostic DEV thresholds, not final choices: raw M0 at 0.65 has all-positive P/R/F1 **0.364/0.623/0.459**, TP/FP/FN **48/84/29**; filtered M0 at 0.65 has **0.505/0.623/0.558**, **48/47/29**; M1 at 0.75 has **0.593/0.948/0.730**, **73/50/4**. Failing-post counts are **26/25/14** respectively.
- Documented P/R/F1 (n=477, positive support=14): raw **0.116/0.786/0.202**, filtered **0.190/0.786/0.306**, M1 **0.219/1.000/0.359**. Silver (n=526, positive support=63): **0.306/0.587/0.402**, **0.440/0.587/0.503**, **0.541/0.937/0.686**. Each split ignores the other-basis positives and includes the same 463 DEV negatives.
- M1 recipients are identical at thresholds 0.75 and 0.80. All 50 false alerts have rule or dated-edge support; adding dated edges to rules at 0.75 recovers two positives but adds four false alerts. No final source policy was selected.
- Actual M1 hints obey relationship dates; static `declared_partners` cannot restore the 2023 HDFC edge on the 2020 Swiggy post. HDFC still matches the generic food-checkout rule, so its recipient decision does not disappear. Profiles remain static November 2026 simulations.
- The separate expiry clock yields six raw recipients and zero filtered/M1 recipients. Instrument gating, merchant exemption and the competitor-subscription exception were tested. No full ten-hard-case pass, content-quarantine, notification-deduplication or cache-savings result is claimed. Hard case 4 remains a historical market update.
- Flash's single authorized 64-token retry returned exact JSON in 2.108 seconds, with 12/5 tokens and USD 0.00001610 cost. Flash and GPT-4.1-mini remain candidates. Three new paid calls total USD **0.00004150**; prior spend is owner-confirmed below USD 0.01, giving a cumulative upper bound below USD **0.01004150**. No further smoke tests or M2 calls ran.
- Full tables, sweeps and explanations are in `docs/experiments_draft.md` and `docs/LEARNING_NOTES.md`. `docs/checkpoint2_snapshot.json` preserves lossless confusion counts and recipient/label bitsets; `docs/checkpoint2_failures.md` lists errors. All six runtime input hashes match local DEV files; reproduction took 0.003 seconds. No source bodies were copied into these results.
- Measurements were preserved at 16:49:36 IST. At 17:02:24 IST the original elapsed time was about 453.3 minutes; the Sunday 17:30 soft checkpoint and Monday November 16, 2026, 10:00 AM IST deadline remain unchanged. Checkpoint 2 awaits Anand's reply. M2, semantic-cache tests, notification deduplication, safety, latency and final `docs/experiments.md` are unstarted; the explicitly deferred notebook/Drive/status-document work remains deferred.
