# Checkpoint 2 failing posts

DEV labels, not held-out truth. Diagnostic thresholds are 0.65 for raw/filtered M0 and 0.75 for M1. These are stateless pair predictions, not a completed delivery pipeline. Source data and label reasons remain unchanged.

## M0 raw: 26 failing posts

Every real post, `p01` through `p24`, plus `p26_exact_repost` and `p29_near_repost`, has at least one missed or extra recipient. Total TP/FP/FN: 48/84/29.

## M0 filtered: 25 failing posts

The same list except `p04_phonepe_upi_cashback_update`, which now has exactly its expected recipients. Total TP/FP/FN: 48/47/29. Filters removed 19 competitor and 18 instrument errors, but did not recover any positive.

## M1: 14 failing posts

Total TP/FP/FN: 73/50/4. All four missed positives belong to one HDFC online-card-rewards post. The other 13 failing posts have only extra recipients.

| Failing post | Missed recipients | Extra recipients |
|---|---|---|
| `p04_phonepe_upi_cashback_update` | none | zomato |
| `p08_phonepe_swiggy_first_cashback` | none | zomato, flipkart, amazon_india, myntra, makemytrip, hdfc_bank, icici_bank, axis_bank |
| `p09_phonepe_swiggy_repeat_cashback` | none | zomato, flipkart, amazon_india, myntra, makemytrip, hdfc_bank, icici_bank, axis_bank |
| `p11_swiggy_hdfc_cobrand` | none | icici_bank, axis_bank |
| `p12_hdfc_online_card_rewards` | flipkart, amazon_india, myntra, makemytrip | swiggy |
| `p13_axis_myntra_cashback` | none | flipkart |
| `p14_flipkart_axis_card_emi` | none | hdfc_bank, icici_bank, bajaj_finserv, tvs_credit |
| `p15_amazon_prime_card_rewards` | none | hdfc_bank, axis_bank |
| `p17_amazon_icici_no_cost_emi` | none | hdfc_bank, axis_bank, bajaj_finserv, tvs_credit |
| `p18_bajaj_finserv_bike_finance` | none | amazon_india, makemytrip, hdfc_bank, icici_bank, axis_bank |
| `p19_tvs_credit_bike_finance` | none | hdfc_bank, icici_bank, axis_bank |
| `p20_tvs_credit_durable_finance` | none | hdfc_bank, icici_bank, axis_bank |
| `p21_tvs_credit_mobile_finance` | none | hdfc_bank, icici_bank, axis_bank |
| `p26_exact_repost` | none | hdfc_bank, icici_bank, axis_bank, bajaj_finserv, tvs_credit |

The `p04` slug is legacy: this is the approved historical **market update**, not a verified UPI cashback promotion. Zomato is an extra under the current DEV label policy, not independently proved irrelevant. Generic merchant relevance and narrower campaign scope remain a trade-off for Anand to review; no label was changed to improve a score.

The exact-repost error is a missing notification-deduplication stage. A high near-repost cosine does not prove suppression of already-notified agents. No full hard-case pass count or quarantine guarantee is claimed.

`docs/checkpoint2_snapshot.json` stores label and recipient bitsets for all 540 pairs, so every method's missed/extra pairs can be reconstructed after a runtime reset. Bit `j` corresponds to `agent_order[j]`. For a post, missed bits are `(documented | silver) & ~predicted`; extra bits are `negative & predicted`. Counts use Python's `int.bit_count()`.
