here us the plan path file:///run/media/anand/16E6E701E6E6DFCB/Users/akn91/Projects/agent social network/Task 1 plan and location of the repo folder this one one we are currently here but still im pasting the path /run/media/anand/16E6E701E6E6DFCB/Users/akn91/Projects/agent social network here is the repo and here is the prompt Approved, with these rulings. Save this whole message verbatim as
problem1-agent-network/docs/PLAN_AMENDMENTS.md. It overrides the plan wherever they differ.

REPO
Repo root: <FILL IN YOUR ABSOLUTE PATH>. Work inside problem1-agent-network/. The plan file will be at
problem1-agent-network/PLAN_1_agent_social_network.md. If you still cannot find it, tell me and I will paste its contents.
Do not start step 1 until the Colab MCP tools are available.

1. REAL VS SYNTHETIC DATA
Add is_synthetic (bool) to every post and agent. Injection, spam and vague-post cases are synthetic
fixtures. Give them clearly fictional authors (for example "Demo Spammer Co") and never attribute
them to a real company. The duplicate repost is derived from a real post and is marked
derived_from. About 24 real posts plus about 6 synthetic ones is fine.

2. EXPIRED SNAPSHOTS
Every post gets as_of (default snapshot_date, or the offer's start date). The routing function takes a
now parameter. Evaluate each post with now = as_of. The expired-offer hard case is a separate test
that runs the same post with now after valid_until and must produce no routing.

3. DEDUPLICATION
- dedup_key = sha256(author_id + normalized_content). Normalization: lowercase, collapse whitespace,
  strip punctuation, emoji and URLs.
- Exact repost by the same author while the earlier post is still valid (or within 24 hours): store it
  with status "duplicate" and duplicate_of, and do not route it.
- Near duplicate: same author, same facet_signature, embedding cosine >= 0.95 with a post from the
  last 7 days: route normally but suppress notifications to agents already notified for the earlier post.
- The unique (post_id, agent_id) constraint stays as a retry guard only.
- The duplicate hard case passes when the repost creates no new notifications and zero judge calls.

4. JUDGE CACHE KEY
cache_key = sha256(author_id + facet_signature + candidate_agent_id + candidate_profile_version
+ relationship_hints_hash + model_id + judge_prompt_version).
Correctness first. In experiment 2.6 measure the hit rate, and only then consider sharing across
similar authors.

5. VARIANCE TRIALS
Include trial_id in the cache key for variance runs, so each of the 3 trials is an independent call.
Cache each trial's response separately so reruns are free. Run 3 trials only for the top 2 models.

6. ROUTING POLICY
a) Instrument compatibility gate (a hard rule before the judge):
   - Map instruments to capabilities: upi -> upi_payments, credit_card -> credit_cards,
     debit_card -> debit_cards, emi and no_cost_emi -> emi_financing, wallet -> wallet_payments,
     bnpl -> bnpl, net_banking -> banking_accounts.
   - If the post lists any instruments, a candidate that has any payment-instrument capability
     (those tags) must match at least one of them, else reject.
   - Candidates with no payment-instrument capability (merchants, retailers) are not gated.
   - A card-only offer therefore excludes UPI-only apps.
b) Competitors: the hard filter is the only owner of this rule. A competitor pair is excluded unless
   there is an explicit subscription. Remove the partnership-request exception for now. Remove the
   competitor sentence from the judge prompt and instead state in it that all candidates have already
   passed hard filters.

TIME
Your total of 7h50m is right if nothing is done in advance. Stage 1 budget for this session:
Phase 0 Colab parts 15 min, dataset 60 min, experiments 2 hours. If you reach 3h20m total, stop
and report where you are. Cut order: fewer variance runs, fewer threshold sweeps, fewer
synthetic cases. Never cut the hard cases or the labels.

Now begin step 1 once the Colab MCP is connected. after this install colab mcp server add it to config so i can complete auth

## Later owner approval: DEV set and Phase 2

Dataset approved as the DEV set, with these conditions:
1. Metrics: exclude author-self pairs. Report results separately for documented labels (14 positives) and inferred labels (63). Treat inferred as silver.
2. Add valid_from to every dated relationship edge (for example Swiggy and PhonePe 2018, Swiggy and HDFC co-brand card 2023). Rules and M1 ignore edges where valid_from is later than now. Disclose that capability profiles are static November 2026 simulations.
3. Hard case 4 stays labelled "market update", not "UPI cashback passed". I will supply a held-out set of current offers later, including a real UPI cashback.
4. Do not commit data/source_snapshots/ to git. Keep URL, date, hash and our own short factual summary only. Add the folder to .gitignore.
5. I am copying data/ (without source_snapshots) into Drive at MyDrive/agent-network-experiments/data. Read it from there. No clone URL needed.
6. Proceed to Phase 2 now. Remaining time by your clock: 85 minutes. Plan: embeddings plus M0 and M1 (20 min) then checkpoint 2; add 1 or 2 stronger mid-tier models to the trial pool and smoke test JSON mode on each (10 min); M2 judge runs (25 min); cache, safety and latency (15 min); docs/experiments.md (10 min). Skip variance trials if time is short.
7. No more plumbing cells. Keep outputs small.

## Later owner authorization: soft timing and teaching

Authorized. The 3h20m cap was a planning guide, not the real deadline. The real deadline is Monday 10:00 AM IST. Replace the hard stop with soft checkpoints: report progress at about 17:30 IST and I will decide then.

Explore properly. If a result looks surprising, investigate it.

Teach as you go. I want to understand and own this work.
- Before each phase: 3 lines on what we test and why.
- After each result: what it means in plain words, plus 2 or 3 concrete examples I can inspect, especially failures and the Bajaj Finserv vs Bajaj Auto trap.
- Keep docs/LEARNING_NOTES.md with a plain explanation of each step and an empty "My notes" section after each, for me to fill in.
- When a choice has trade-offs, show me the alternatives and let me decide.

Keep following the seven DEV-set conditions. Keep outputs small. follow this for the rest

## Existing Colab clarification

let me tell you there already a collab is running i would say check that instead of going for the new collab

## Latest owner decision: stop setup and run the experiments

Review received, it is accurate. Decision: stop auditing and setup now. About six hours went into setup and no experiment has run.

1. Drop persistent Drive caching. I am uploading data.zip to /content/data.zip myself. Unzip it to /content/data and read from there. This replaces DEV condition 5.
2. Drop the ledger reconciliation. Total spend is under USD 0.01. From now on append one row per paid call to /content/usage.csv (model, tokens, cost) and stop at USD 1.50 total. No reservation system, no more guard cells.
3. Ignore the catalogue change from 454 to 452. Only confirm that the three trial models still exist at the same prices.
4. Add 1 or 2 stronger mid-tier models to the trial pool (search the catalogue for ids containing haiku, flash or mini). Smoke test JSON mode on each with a 32 token call.
5. Go straight to Phase 2: embeddings with bge-small, then M0 with a threshold sweep, then M1 with relationship rules, valid_from and the instrument gate. Checkpoint 2 right after M0 and M1: the results table split by documented and inferred labels, the failing posts, and the Bajaj Finserv vs Bajaj Auto result.
6. Teach as you go: 3 lines before each step, plain meaning plus 2 or 3 examples after. Start docs/LEARNING_NOTES.md.
7. Copy results tables into docs/experiments_draft.md locally at each checkpoint, since the runtime can reset.
Do not review the notebook again. Do not rerun setup. Report only at checkpoint 2.

## Latest owner instruction: uploaded DEV input and three baseline methods

Uploaded /content/data.zip. Unzip to /content/data. Quick check: print counts only (agents, posts, labels, non-self pairs 540, documented 14, silver 63).

Defer until the very end of the session, and only if time allows: Drive reconciliation, saved notebook sync, README and DATASET_REVIEW wording. The unreconciled ledger history does not matter; spend is under USD 0.01.

Gemini Flash: retry once with a higher token cap (64) and the same JSON instruction. If it still adds text, drop it and keep GPT-4.1-mini as the stronger candidate. Do not run more smoke tests yet.

Now Phase 2:
1. Embeddings with bge-small. Print the near-repost cosine for the exact and near duplicate fixtures.
2. Report three methods on the 540 non-self pairs: M0 raw similarity (best interest similarity per agent, sweep thresholds); M0 plus shared hard filters (competitor filter, instrument gate, expiry); and M1 (filters plus relationship rules, subscriptions and dated edges).
3. Implement temporal enforcement in M1 for real: ignore any relationship edge whose valid_from is later than the post's as_of, and do not let static declared_partners bypass it. Show it with a concrete example: an older Swiggy post must not use the 2023 Swiggy and HDFC edge, with a before and after.
4. Metrics: precision, recall and F1 for all positives, for documented only, and for silver only. Print the counts (n) beside each metric. Show the threshold sweep as a small table so I can see where results are stable, not just the single best point.
5. Checkpoint 2 report, short: the three-row table, the stage where each method fails, and these inspectable examples: Flipkart EMI vs Bajaj Finserv and Bajaj Auto, Swiggy to PhonePe, the card-only offer vs UPI-only apps, and the temporal example. Teach as before: 3 lines before, plain meaning after.
6. Append to docs/experiments_draft.md and docs/LEARNING_NOTES.md at each step.

Report at the 17:30 IST soft checkpoint even if mid-way. Keep outputs small and cells small. Wait for my reply after checkpoint 2. check that

## Checkpoint 2 accepted: deduplication, owner review and five-model M2

Checkpoint 2 accepted. Good report. Next:

1. Dedup first. Add the exact and near duplicate stage before routing (author plus normalized content hash, then cosine >= 0.95 within the same author). Report M1 metrics before and after. These repost alerts are not routing errors.

2. Review table for me. Write docs/fp_review.csv with the 50 false alerts and 4 misses: post_id, post title, agent, source (similarity, rule id, edge id), similarity, one-line reason, and an empty column "owner_verdict" (system_wrong, label_wrong, unsure). I will fill it. Do not change any labels yourself. After I return it, save the adjudicated labels as stage1-dataset-v3 with each change logged with my reason, and report v2 and v3 scores side by side.

3. Honest framing. In docs/experiments_draft.md state that documented recall is partly circular because dated edges came from the same sources as documented labels, and that M1 at .75 or .80 is driven by rules and edges, not similarity.

4. M2 (while I fill in the review). Candidates for the judge are all M1 candidates plus any agent with similarity >= 0.50 that M1 rejected, so we can see if the judge recovers misses. One call per post, strict JSON, prompt from the plan section 9 with the amendments (all candidates already passed hard filters). Run the same 30 posts on the 3 small models plus GPT-4.1-mini and Gemini Flash. Max_tokens capped, usage logged to /content/usage.csv, cache key per the amendment including trial_id, bounded retries.
   Report per model: precision, recall, F1 for all, documented and silver with n; false alerts removed and true positives lost compared with M1; calls per post, tokens, cost per post, latency. Show 3 inspectable examples per model, including Bajaj Finserv vs Bajaj Auto.

5. Two cheap extra checks on the best two models only: (a) anonymize candidate names (agent_1, agent_2) and rerun, to see whether decisions come from capabilities or brand names; (b) the injection post must not change the recipient list and the judge must return only the IDs given.

6. Sealed held-out set. I will provide current offers later. Do not look at them. Prompts and thresholds are frozen before they are run.

Teach as before. Checkpoint 3 after step 4 and 5. Variance trials only for the top two models, after I choose.
