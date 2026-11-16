# Working agreement

These owner instructions override earlier workflow instructions. They apply to the rest of this session and every later step.

The confirmed Colab secret name is `AICREDITS_KEY`. Notebook permission was already granted. Never print or save its value.

1. Run one small cell at a time. Each cell does one thing and contains at most about 25 lines. Never chain risky steps.
2. After each cell runs, write 2 to 3 lines in chat: what the output shows, anything surprising, and what will run next and why. Do not paste long code into chat.
3. Human-blocking actions, including Drive mounts, secret permission prompts and browser authentication, get their own cells. Ask the owner to perform the action by hand first, then verify with a fast, bounded check. Do not ask again for a permission already granted.
4. Every network call has a timeout and reports elapsed seconds using `time.perf_counter`. If a cell runs longer than 60 seconds, interrupt and report. An MCP request timeout does not prove the kernel stopped. If no interrupt tool is exposed, ask the owner to stop execution before running anything else.
5. No unbounded loops. Every paid call requires known prices, a `max_tokens` cap and a usage log row.
6. Stop at every plan checkpoint and wait for the owner's reply.

## Step 1, redone as small cells

- 1a: Secret check only. Report whether `AICREDITS_KEY` can be read. On failure show `False` and the exception class name, never the secret value.
- 1b: Drive check only. Check whether `/content/drive/MyDrive` is present. If not, ask the owner to mount Drive by hand and wait. Only after an explicit decline may the cache use `/content/cache`, with a warning that a runtime reset removes it.
- 1c: Define cache helpers only. Defining them must not perform file I/O.
- 1d: Build the OpenAI-compatible client and call `models.list()` once, with a timeout and timing. Show only the model count and elapsed seconds.
- 1e: Write the catalogue to the cache, then show a small provisional shortlist and whether pricing fields exist.

## References checked

- OpenCode MCP skill and documentation: https://opencode.ai/docs/mcp-servers
- Installed official Colab MCP release: https://github.com/googlecolab/colab-mcp/tree/b85ab6ec5206e06fdd289ff4ff3f9c4ee767b422
- Official Colab secret API source: https://github.com/googlecolab/colabtools/blob/main/google/colab/userdata.py

The documented `userdata.get` request has a 10-second timeout. The exposed notebook tools do not include an interrupt operation. Do not treat a browser-proxy connection as proof that a runtime operation succeeded.

## Latest owner overrides

- The 3h20m allocation is now a planning guide, not a hard stop. Preserve the original start and elapsed-time record. Report progress around Sunday November 15, 2026, 17:30 IST; Anand decides whether to continue. The real submission deadline is Monday November 16, 2026, 10:00 AM IST.
- Use the existing Colab notebook and runtime. Do not create another notebook or repeat installation, secret authorization, Drive mounting or client setup.
- Read the DEV data from `/content/drive/MyDrive/agent-network-experiments/data`. No clone URL is needed.
- Follow the seven DEV conditions recorded verbatim in `docs/PLAN_AMENDMENTS.md`. This is not a held-out benchmark.
- Before each phase, explain what is tested and why in three short lines. After each result, explain it in plain words and show two or three inspectable examples, especially failures and the Bajaj Finserv/Bajaj Auto distinction.
- Maintain `docs/LEARNING_NOTES.md`, with an empty `My notes` section after each explained step. Preserve Anand's later notes.
- Investigate surprising results. Present alternatives with their trade-offs and let Anand decide; do not silently choose final models or thresholds.

## Latest execution override: experiments, not more setup

- Stop notebook/output audits and setup reruns. Reuse the working runtime, client, packages and authorized key.
- DEV input is the owner-uploaded `/content/data.zip`, extracted to `/content/data`. Persistent Drive caching is no longer required; this replaces earlier DEV condition 5.
- Do not reconcile ledgers or use reservations. Append a row for each new paid call to `/content/usage.csv`, including model, tokens and cost. Prior spend is below USD 0.01; keep the total below USD 1.50. No new guard cells.
- Ignore catalogue-count changes. Confirm only the original three trial models and prices, then add one or two haiku/flash/mini mid-tier candidates and smoke-test JSON mode with 32 output tokens each.
- Run BGE-small embeddings, the M0 threshold sweep and M1 with dated relationships and the instrument gate. Stop at checkpoint 2 with documented/silver metrics, failing posts and the Bajaj Finserv/Bajaj Auto comparison.
- Retain short teaching explanations before and after each step. No separate setup/status reports before checkpoint 2. Preserve owner notes in `docs/LEARNING_NOTES.md`.
- Save checkpoint tables locally in `docs/experiments_draft.md`, since the runtime can reset. All other DEV conditions and the original elapsed-time record remain in force.
