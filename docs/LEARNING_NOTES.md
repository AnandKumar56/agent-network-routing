# Learning notes

This is a running explanation, not a claim that unfinished experiments have passed. Each empty **My notes** section is for Anand to fill in.

## 1. What setup proved

The earlier setup verified the pinned packages, seed 42, an approved secret and persistent Drive caches. One Mistral NeMo request returned valid connectivity-test JSON in 2.662 seconds. It cost an estimated USD 0.00000066. This proves that a paid request can work; it says nothing about whether the model can route business posts correctly. The later runtime's different cache state is explained in step 5 below.

Examples to inspect:
- `{"ok": true}` is a formatting/connectivity test, not a relevance decision.
- Saving a response to Drive lets a rerun reuse it without paying again.
- A browser connection succeeding does not prove that the notebook-read tool or kernel request succeeded.

### My notes

## 2. Why this is a DEV set

We will use these 30 posts to explore errors and compare methods. That makes them a development set: adjusting rules and thresholds after seeing their results is allowed, but the final score is not independent evidence of generalization. Anand will supply unseen current offers later.

There are 14 documented positive labels and 63 inferred positive labels. Documented means a source supports the partnership or offer link. Inferred means a plausible complementary action, so those labels are silver rather than unquestionable truth. We exclude the 30 author-self pairs from metrics. The remaining universe contains 540 pairs: 77 positives and 463 explicit negatives.

Examples to inspect:
- Flipkart to Bajaj Finserv for the sourced No Cost EMI offer is documented.
- Flipkart to TVS Credit for a possible mobile-financing offer is inferred; it is not proof of participation in that sale.
- PhonePe's historical UPI/cashback post is a market update. It cannot certify a genuine UPI cashback promotion in the future held-out set.

### My notes

## 3. Why relationship dates matter

A relationship learned from a later announcement must not improve a historical prediction. The planned rule is to use an edge only when its `valid_from` is not later than the post's evaluation clock. If an offer edge has a documented end, its expiry must also be respected. Unknown historical start dates must not be invented or backdated.

Capability profiles remain static November 2026 simulations. Dating relationships reduces one kind of future-information leakage; it does not turn those profiles into a full historical company census.

Examples to inspect:
- A 2023 Swiggy/HDFC co-brand edge cannot enrich the November 2020 Diwali post.
- The March 2018 Swiggy/PhonePe source can support a November 2020 relationship hint, subject to the recorded limitations.
- Bajaj Finserv's lending role may complement a mobile sale. Bajaj Auto's manufacturing role does not, even though their names overlap.

### My notes

## 4. What embeddings and the two baselines will test

An embedding is a list of numbers representing text. We use the same 384-dimensional BGE model for posts and separate interest statements. Cosine similarity measures how closely two such lists point in the same direction; it is not a probability or proof of business relevance. The best matching interest supplies an agent's similarity score.

M0 asks whether similarity alone is enough to collect relevant candidates. M1 adds capability rules and date-valid partner evidence. We will document shared hard filters so an improvement is not incorrectly attributed to embeddings or relationships. We will inspect individual errors before selecting thresholds.

Examples to inspect when results are available:
- An EMI post may resemble both consumer financing and vehicle financing; inspect which interest statement caused each match.
- A card-only food promotion should not reach a UPI-only scoped profile merely because both mention checkout.
- An explicit Swiggy/HDFC co-brand card is more specific than a generic food-payment opportunity.

### My notes

## 5. Why clean execution is not the same as readiness

The latest output review found 22 populated code cells with completed outputs and no recorded Python exceptions. Packages, the already-authorized secret, the client and a new NeMo JSON smoke test worked. However, the last check still says Drive and DEV data are absent.

The live cache cell was changed to enable `/content/cache`. That avoids the earlier Drive exception but does not mount Drive. Runtime-only cache files can disappear after a reset. A ledger in a different directory also does not automatically remember earlier requests: the current ledger began at zero despite the historical paid smoke request. Known combined estimated spend is USD 0.00000132 for two smoke requests, not a reset to zero.

Examples to inspect in `docs/COLAB_OUTPUT_REVIEW.md`:
- Cell 23 says JSON validation is `True`; this is not a successful business-routing prediction.
- Cell 24 says client state is present but Drive and DEV data are `False`; the embedding experiment still cannot read its approved input.
- Cell 14 initially showed zero requests, then cell 22 logged one new request. The earlier Drive-recorded request still belongs in the original session's spend history.

Bajaj Finserv versus Bajaj Auto has no measured routing result yet. We must not treat successful setup as a pass for that distinction.

### My notes

## 6. The simpler experiment path and two mid-tier smoke tests

Anand replaced Drive input with the owner-uploaded `/content/data.zip`, to be extracted into `/content/data`. Persistent Drive caching and ledger reconciliation are no longer prerequisites. New paid calls append model, input/output tokens, cost and timing to `/content/usage.csv`. We conservatively allow USD 0.01 for all earlier spend when checking the USD 1.50 ceiling; this is an upper bound, not a new measured charge or a reset of history.

The existing cached catalogue still contains all three original models at unchanged prices. Two additional candidates are `google/gemini-2.5-flash` (USD 0.30 input / 2.50 output per million tokens) and `openai/gpt-4.1-mini` (USD 0.40 / 1.60). Each received one JSON-mode request capped at 32 output tokens, with a 20-second timeout and no automatic retries. The working client and authorized secret were reused.

Examples to inspect:
- GPT-4.1-mini returned exactly `{"ok": true}` in 1.937 seconds, with 22 input / 5 output tokens and USD 0.00001680 estimated cost. It passed this tiny compatibility test, not the business-routing evaluation.
- Gemini 2.5 Flash returned `Here is` in 2.066 seconds, with 12 input / 2 output tokens and USD 0.00000860 estimated cost. It failed JSON validation under this request. The cause is not established; we did not silently increase its token cap or call it a pass.
- NeMo, Gemma 3 4B and Llama 3.1 8B remain present at their recorded prices. Catalogue-count changes are intentionally ignored.

These two calls total USD 0.00002540. The conservative cumulative upper bound is USD 0.01002540. Final model and threshold choices still belong to Anand.

### My notes

## 7. The DEV input is now available

The uploaded ZIP was extracted into `/content/data`. It contains 19 agents, 30 posts and 30 per-post label rows. Removing the 30 author-self pairs leaves 540 evaluated pairs: 14 documented positives, 63 silver positives and 463 explicit negatives. No Drive mount, ledger reconciliation or successful setup step was repeated.

Examples to inspect:
- Flipkart's own mobile post paired with Flipkart is outside the 540-pair evaluation, even if their texts are very similar.
- Flipkart to Bajaj Finserv is a documented positive; Flipkart to TVS Credit is a silver financing opportunity, not verified sale participation.
- The 30 label rows each describe recipients and non-recipients for one post; they are not just 30 binary pair labels.

### My notes

## 8. Why a tiny token cap can change a smoke result

The owner authorized exactly one Gemini Flash retry with a 64-token output cap and the unchanged JSON instruction. Flash now returned exactly `{"ok": true}` in 2.108 seconds, with 12 input / 5 output tokens and USD 0.00001610 estimated cost. Its finish reason was `stop`. We retain Flash and GPT-4.1-mini as candidates, without choosing a final judge model.

Examples to inspect:
- Flash at 32 tokens returned `Here is` and failed validation. At 64 tokens it returned the requested JSON and passed. These are measured observations, not a proven internal explanation.
- GPT-4.1-mini passed its original 32-token request. This does not establish that it will beat Flash on business relevance.
- The retry is a third new paid-call row in `/content/usage.csv`; new experiment spend is USD 0.00004150. Earlier spend remains owner-confirmed below USD 0.01, with no reconciliation required.

### My notes

## 9. BGE-small embeddings and repost similarity

An embedding maps text to 384 numbers. We embedded each of the 51 interest statements separately and each of the 30 posts as title plus content. After normalizing vector lengths, their dot product is cosine similarity. An agent's score is its highest-scoring interest, so a relevant financing interest is not diluted by unrelated interests.

Model loading/downloading took 3.021 seconds; embedding computation took 5.519 seconds. All vectors are finite and 384-dimensional. The runtime saved the vectors in `/content/data/embeddings.json` and the score matrix in `/content/results/bge_scores.npz`.

Examples to inspect:
- `p01_flipkart_mobile_emi` versus `p26_exact_repost`: cosine 1.000000, as expected for identical title/content.
- `p01_flipkart_mobile_emi` versus `p29_near_repost`: cosine 0.994695, above the required 0.95. Word order changed, but the financing offer stayed very similar.
- A high cosine is not proof of business action or a deduplication decision. Exact reposts must be blocked separately; near reposts route normally while suppressing recipients already notified in the earlier sequence.

### My notes

## 10. What raw similarity gets wrong, and what filters fix

We swept nine thresholds from 0.40 to 0.80. Both M0 variants reached their highest pooled DEV F1 at 0.65 in this sweep, but that is a diagnostic result, not Anand's final threshold choice. Raw M0 precision/recall/F1 was 0.364/0.623/0.459. Adding shared filters changed it to 0.505/0.623/0.558. The filters removed 37 false alerts (19 competitor and 18 instrument errors) without recovering any of the 29 missed positives.

The documented slice counts only its 14 positives plus 463 shared DEV negatives, ignoring the 63 silver positives. The silver slice counts its 63 positives plus those same negatives, ignoring documented positives. Their evaluated pair counts are 477 and 526. We do not call correctly predicted silver opportunities false positives in the documented slice. The negative judgments remain inferred/policy-based, so this is not a fully source-documented benchmark. `docs/experiments_draft.md` contains the sweep and confusion counts.

Examples to inspect:
- Flipkart EMI: Bajaj Finserv scores 0.741158, above 0.65; Bajaj Auto scores 0.590627, below it. At 0.55, raw similarity would wrongly include Bajaj Auto. Cosine thresholds do not guarantee business-role correctness.
- Swiggy Diwali to PhonePe scores 0.590314 and is missed at 0.65 by both M0 methods. Filters can veto an incompatible match; they cannot add a missing complementary partner.
- Card-only Swiggy: Google Pay scores 0.651691 and Paytm 0.664607. Raw M0 includes them, but the instrument gate rejects their UPI-only profiles. ICICI scores 0.750701 and stays eligible.

These are stateless pair baselines, not the completed notification pipeline. Content screening, quota/fan-out state and duplicate-notification suppression are not yet evaluated. Exact repost and safety fixture errors remain visible rather than being hidden by their expected labels.

### My notes

## 11. What M1 adds, and why recall is not enough

M1 keeps the same shared filters, then combines similarity with capability rules, subscriptions and date-valid relationships. In this coverage baseline a rule or valid partner hint can add a candidate even below the semantic threshold. Static profile partner lists are not a shortcut. The rules match capability tags, not company names.

At its diagnostic DEV threshold 0.75, M1 precision/recall/F1 is 0.593/0.948/0.730: 73 correct alerts, 50 incorrect alerts and four missed positives. It reaches all 14 documented positives and 59 of 63 silver positives. The identical recipient matrix at 0.75 and 0.80 shows a plateau, but it is a DEV observation, not a final threshold choice. Every split and confusion count is in `docs/experiments_draft.md`.

Examples to inspect:
- Swiggy to PhonePe scores only 0.590314 and both M0 methods miss it at 0.65. M1 adds it through the food-checkout capability rule and the valid March 2018 payment relationship.
- Flipkart EMI reaches Bajaj Finserv through financing capabilities and its dated campaign edge. Bajaj Auto has neither financing rule nor edge and remains below the diagnostic semantic thresholds. The instrument gate does not ban every manufacturer; genuine vehicle-financing complementarity remains possible.
- Google Pay and Paytm are still rejected from the card-only post. Even PhonePe's rule and valid payment-partner hint cannot bypass its incompatible instrument role.

### My notes

## 12. Temporal enforcement changes the evidence, not necessarily the recipient

The implemented relationship helper requires a real edge to have a start date no later than the post's `as_of`, and respects an end date when present. Every actual M1 hint passed these checks. Static `declared_partners` does not restore a filtered-out edge. The profiles remain static November 2026 simulations, so temporal edges do not eliminate every kind of historical leakage.

Examples to inspect:
- Swiggy Diwali is evaluated at November 12, 2020. A deliberately unsafe comparison ignoring dates includes the HDFC co-brand edge from July 26, 2023. Actual M1 removes that hint despite HDFC appearing in the static partner list. HDFC still gets a generic card-checkout rule, so its recipient decision does not change. Claiming it vanished would be false.
- PhonePe's March 22, 2018 relationship remains a valid hint on that 2020 post, while a March 21, 2018 clock excludes it. The expired 2025 ICICI/Swiggy offer hint is absent from a November 2026 post.
- After the card offer's expiry, raw similarity still suggests six recipients because it ignores time. Filtered M0 and M1 suggest zero. This separates historical relevance at `as_of` from the explicit expired-offer test.

The now-aware per-post helper reproduced all three measured matrices on the 30 posts. The Flipkart May 13, 2018 campaign start is sourced retrospectively by a May 14 report; we do not call this strict point-in-time knowledge.

### My notes

## 13. Why the source ablation matters

We investigated M1's 50 false alerts rather than calling higher recall a finished solution. At 0.75, filtered similarity alone has 13 correct alerts and zero false alerts but misses 64 positives. Adding rules raises this to 71 correct / 46 false; adding dated edges on top raises it to 73 correct / 50 false. More evidence recovers two positives but adds four errors and slightly reduces pooled F1 from 0.732 to 0.730.

Examples to inspect:
- The Swiggy-specific PhonePe first-order cashback goes to eight extra agents under broad capability rules. Knowing that a merchant can accept UPI does not show that it can use this particular promotion.
- Bajaj Finserv's motorcycle-loan post wrongly reaches Amazon India and MakeMyTrip through date-valid partner edges. A relationship may be real but scoped to different products. HDFC, ICICI and Axis also get overly broad EMI-rule matches.
- The exact repost still produces the five EMI recipients in these stateless baselines. Its remedy is agreed notification deduplication, not asking an embedding or judge to reinterpret identical text. The near repost's measured 0.994695 cosine is not a cache-savings or notification-suppression result.

M1's only four missed positives are the four merchants on HDFC's online-card-rewards post, exposing a missing card-provider-to-merchant rule direction. Options for later comparison are narrower rule conditions, treating partner hints as evidence rather than unconditional acceptance, and judging uncertain candidates. Their trade-offs and final thresholds remain Anand's decisions. No M2 or additional smoke test ran after these baselines.

### My notes

## 14. What is preserved if the runtime resets

The local draft contains the measured three-method table, threshold sweep, confusion counts and concrete examples. `docs/checkpoint2_failures.md` contains the failing-post list and all M1 missed/extra recipients. `docs/checkpoint2_snapshot.json` stores compact label/recipient bitsets and all sweep counts without copying source bodies. A local check reproduced the diagnostic confusion counts and matched all six DEV input hashes in 0.003 seconds.

Examples to inspect:
- The snapshot's `count_order` is documented TP, silver TP, shared-negative FP. At M1 0.75 it is 14/59/50, giving pooled TP=73, FP=50 and FN=4.
- Its recipient bitsets preserve exact pair decisions, not just a headline F1. `checkpoint2_failures.md` explains how to decode a missed or extra agent.
- `p04` remains a market update. Its Zomato extra is an error under the current silver/DEV label policy, not independent proof that merchant action is impossible.

The larger embedding files are still temporary in `/content`; no Drive recovery or saved-notebook sync was undertaken. Final thresholds and models remain open. We pause at checkpoint 2 for Anand's reply.

### My notes

## 15. Restore the experiment, not a different dataset

After Anand accepted checkpoint 2, the runtime had reset. He authorized a minimal restore rather than more setup or catalogue checks. Six local v2 file hashes match the checkpoint exactly. Recomputed BGE vectors reproduce both repost cosines, and every M1 pair decision reproduces the checkpoint. Prior spending still counts; a fresh usage file does not mean free earlier calls.

Examples to inspect:
- The restored 540-pair M1 matrix is still 73 TP, 50 extras and four misses.
- Exact/near fixture cosines remain 1.000000 and 0.994695; the embedding method did not change.
- No owner label was reconstructed from a model answer or changed during recovery.

### My notes

## 16. Relevance and delivery answer different questions

An exact repost stops before routing. That removes five old delivery omissions, not five mistaken business judgments. Near reposts still route, but recipients already notified in the earlier sequence receive no second notification. We therefore score routed relevance separately from delivery suppression.

M1 after exact dedup has P/R/F1=0.619/0.948/0.749 on the same 540 pairs, with 73 TP, 45 relevance extras and four misses. Near suppression removes 14 deliveries. Six of those pairs are labelled positive, so naively scoring the notification list against all 77 positives would falsely create six new misses. The separate delivery-aware universe excludes suppressed pairs and reports its smaller support explicitly.

Examples to inspect:
- `p26_exact_repost` has duplicate status, no routing invocation and no new notification.
- `p29_near_repost` still routes to five EMI partners, but sends no second notification to them.
- The real first-order/repeat-order PhonePe promotions also match the amended policy at cosine 0.978604. Their eligibility differs despite identical coarse facets. We disclose this risk; changing the signature or policy remains Anand's choice.

### My notes

## 17. Owner adjudication is not model self-correction

The review CSV preserves all 54 original errors, even the five deliveries now fixed by dedup. Similarity and rule/edge IDs let Anand distinguish a broad rule, an out-of-scope real relationship, a delivery omission and a debatable silver label. Empty verdict and reason fields mean the owner has not yet decided. A model's prediction is not authority to rewrite the truth it is evaluated against.

Examples to inspect:
- All 50 original extras have rule/edge support and similarity below 0.75, so a 0.75/0.80 plateau is mostly a rules-and-edges result.
- HDFC's online rewards post misses four merchants at similarities 0.636426 to 0.692624. They will be eligible for M2's broader >=0.50 candidate pool.
- Documented labels and dated edges share sources. Perfect documented recall is partly circular consistency, not independent generalization evidence.

Fill `owner_verdict` with `system_wrong`, `label_wrong`, or `unsure`, and `owner_reason` with your reason. Only returned adjudication can authorize `stage1-dataset-v3`; v2 stays preserved for a side-by-side comparison.

### My notes
