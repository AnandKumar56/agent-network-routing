# AICredits price snapshot

Checked on November 15, 2026 using the authenticated `GET https://aicredits.in/v1/models` response. The free catalogue request returned 454 entries in 1.774 seconds. Its complete response is cached on Drive under `agent-network-experiments/cache/model_catalogue/`.

The gateway supplies per-token rates. The table multiplies those rates by 1,000,000. INR rates come directly from the catalogue, not an invented exchange rate. Dashboard billing has not been independently reconciled.

| Provisional trial model | USD input / million | USD output / million | INR input / million | INR output / million |
|---|---:|---:|---:|---:|
| `mistralai/mistral-nemo` | 0.020000 | 0.030000 | 1.979504 | 2.969255 |
| `google/gemma-3-4b-it` | 0.040000 | 0.080000 | 3.959007 | 7.918014 |
| `meta-llama/llama-3.1-8b-instruct` | 0.050000 | 0.080000 | 4.948759 | 7.918014 |

This is a limited pool of established general instruction/chat models, not a global cheapest-model ranking. ScaleDown task utilities and roleplay merges were excluded from this trial. Prices alone do not establish judge quality or strict decision-schema support. The final model remains decision D1 for Anand.

## Model documentation checked

- Mistral's model card: https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407
- Google's Gemma 3 model card: https://ai.google.dev/gemma/docs/core/model_card_3
- Meta's Llama 3.1 model card: https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md
- Lunaris author's roleplay/generalist merge description: https://huggingface.co/Sao10K/L3-8B-Lunaris-v1
- Pinned SDK timeout/retry documentation: https://github.com/openai/openai-python/blob/v1.109.1/README.md

## Measured connectivity test

| Setting or result | Value |
|---|---|
| Model | `mistralai/mistral-nemo` |
| Temperature / JSON mode | `0` / `json_object` |
| Output token cap | 32 |
| Request timeout / automatic retries | 20 seconds / 0 |
| Elapsed request time | 2.662 seconds |
| Reported input / output tokens | 24 / 6 |
| Estimated cost | USD 0.00000066; INR approximately 0.000065 |
| Validation | Exactly `{"ok": true}` |

The original run completed one paid request. Anand's later manual execution completed a second NeMo smoke request in 2.374 seconds, again with 24 input and 6 output tokens and estimated USD 0.00000066. Both passed the same JSON check. Known cumulative estimated spend is USD 0.00000132. Gemma and Llama compatibility, judge quality, variance, routing thresholds and per-post routing cost are still untested.

The later catalogue returned 452 entries in 5.629 seconds, with finite prices for 398 chat entries. The three displayed trial models and their rates are unchanged. Unlike the original Drive cache, the later live cache cell enables temporary `/content/cache`: its ledger began at zero and currently accounts only for the second smoke request. The two ledgers must be reconciled without overwriting history before more paid calls. See `docs/COLAB_OUTPUT_REVIEW.md`.

## Guards

- Original session ledger: `stage1-20261115-035903`, persisted on Drive. The later temporary ledger uses the same tag in a different location; it is not a complete session history.
- Budget: USD 1.50, with a maximum of 240 paid requests, known finite rates and an output cap on every call.
- Response cache keys include the complete request and `trial_id`. The amended semantic judge key must also be applied before judge experiments.
- Unresolved requests retain conservative reservations and block automatic replay. Missing usage retains the reservation instead of assuming zero cost.
- Original session start: `2026-11-15T03:59:03.629000+00:00`. Original planning stop: `2026-11-15T07:19:03.629000+00:00`, retained as history, not enforced. The owner replaced it with a soft Sunday 17:30 IST progress checkpoint. The real deadline is Monday November 16, 2026, 10:00 AM IST. Elapsed time and spend must not be reset.

## Latest owner override and mid-tier trial additions

The ledger reconciliation and reservation requirements above are superseded. Earlier spend is owner-confirmed below USD 0.01. Each new paid call appends to `/content/usage.csv`; the budget check includes a conservative USD 0.01 allowance for earlier spend and stops before the USD 1.50 ceiling. Persistent Drive caching is no longer required. No catalogue request or successful setup step was repeated.

The cached catalogue confirms that all three original models remain present at unchanged prices. Two mid-tier candidates were added for comparison, not selected as final models:

| Additional trial model | USD input / million | USD output / million | JSON result at 32-token cap | Seconds | Input / output tokens | Estimated USD cost |
|---|---:|---:|---|---:|---:|---:|
| `google/gemini-2.5-flash` | 0.30 | 2.50 | Failed: returned `Here is` | 2.066 | 12 / 2 | 0.00000860 |
| `openai/gpt-4.1-mini` | 0.40 | 1.60 | Passed: exactly `{"ok": true}` | 1.937 | 22 / 5 | 0.00001680 |

Both used the existing OpenAI-compatible client, `temperature=0`, `response_format={"type":"json_object"}`, a 20-second request timeout and zero automatic retries. Costs use the gateway's reported usage and cached per-token prices. New-call total is USD 0.00002540; conservative cumulative upper bound is USD 0.01002540. The Gemini failure cause remains unconfirmed. A tiny JSON pass is not a routing-quality result.
