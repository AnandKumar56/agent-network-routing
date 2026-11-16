# Submission

## Published link

Design package (the submission artifact):
- `README.md` — what the system is and the one hard problem (business complementarity).
- `docs/DESIGN.md` — full architecture, pipeline, delivery, trust/safety, feedback loop, data model, API.
- `docs/RESULTS.md` — measured DEV results with honest caveats.
- `docs/LIMITS.md` — known limits, stated plainly.
- `EXTRAS.md` — additions beyond the brief with quality bars.

No hosted/deployed build was produced today; the design package on GitHub is the published artifact.

## GitHub link

- Repository: local project `problem1-agent-network/` (owner to provide the remote URL for push; no remote was configured in this session).
- Not committed/pushed during this session because no GitHub remote was provided.
- The build runs locally with `python3 -m pytest tests/ -q` (requires `pip install fastembed pytest`; first run downloads the BGE model, then results are cached).

## Screen recording

**Not produced today.** The session was time-boxed to design, measured experiments and the minimal build; no screen recording was captured.

## Anything else

**What was added beyond the brief**
- Deduplication measured *before* routing (owner amendment): exact reposts stop with zero routing calls and zero notifications; near reposts suppress already-notified recipients without touching relevance labels.
- An owner error-review CSV with all 50 original false-alert pairs and 4 misses, measured similarities, rule/edge IDs and blank verdict fields, plus a reproducible, overwrite-protected exporter.
- A frozen, unexecuted five-model judge-stage configuration (strict JSON, opaque IDs, request-specific cache keys, anonymization and injection controls).
- A working routing-core package (`agent_network/`) with a pytest suite that reproduces the measured DEV numbers from the approved fixtures (7 passing tests, ~0.1 s with cached embeddings).

**Quality bars (real numbers)**
- Dataset: 19 agents, 30 posts, 21 reviewed sources with matching hashes, 77 positives (14 documented / 63 inferred), 463 negatives, all ten hard-case specifications.
- Routing on 540 non-self pairs: raw M0@0.65 = 48/84/29; filtered M0 = 48/47/29; M1@0.75 = 73/50/4 (F1 0.730); after exact-repost dedup = 73/45/4 (F1 0.749). Total paid spend upper bound USD 0.01004150.

**Honest status**
- M2 (LLM judge stage) was designed, frozen and **never executed** — no paid M2 call, no model selection.
- Documented recall is partly circular (labels and dated edges share sources); M1's 0.75/0.80 plateau is driven by rules and edges, not similarity; all scores are DEV, never held-out.
- The PhonePe near-repost facet collision is disclosed, not silently patched.
- Not built today: API service, database, webhook delivery worker, dashboard; not measured: quarantine pass, notification-suppression stress test, variance trials, held-out evaluation (offers remain sealed).
