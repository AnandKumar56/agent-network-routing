# Dataset review: checkpoint 1

Status: awaiting Anand's approval. No embeddings, routing evaluations or further paid calls have run.

Goal: spot-check five sourced posts and their business-action labels before using this dataset for experiments.

Done when: Anand checks the five sources below, accepts or corrects the label interpretations and explicitly approves the dataset, including the proposed hard-case 4 substitute.

## Inventory and validation

| Item | Count |
|---|---:|
| Real-company simulated profiles | 16 |
| Clearly fictional authors | 3 |
| Sourced simulated posts | 24 |
| Synthetic or derived fixtures | 6 |
| Reviewed sources | 20 |
| Documented positive labels | 14 |
| Inferred positive labels | 63 |
| Explicit negative labels | 493 |
| Hard-case specifications | 10 |

Every post and agent has `is_synthetic`. The exact and near reposts retain their real source, same author and `derived_from`; injection, spam and vague fixtures use fictional authors. Every positive and negative label has a reason and a `documented` or `inferred` basis.

`python3 scripts/validate_stage1_dataset.py` passed on November 15, 2026:

```text
PASS: 19 agents, 30 posts, 20 reviewed sources; all source hashes match.
PASS: 77 positive labels (14 documented), 493 explicit negatives; complete coverage.
PASS: all 10 hard-case specifications are present and consistent. Routing and near-duplicate cosine are NOT tested.
PASS: 22 notebook code cells compile and contain at most 25 lines; approval and model decisions remain pending.
```

This checks evidence-file integrity, annotations and policy consistency. It does not establish routing quality, cache savings, safety effectiveness or latency. No hard case has a measured routing pass yet.

## Five sourced samples

All five are sourced simulations with `is_synthetic: false`, not authenticated company posts. Each source has a visible-text snapshot and hash under `data/source_snapshots/`.

### 1. Flipkart mobile discounts with No Cost EMI

- Post: `p01_flipkart_mobile_emi`.
- Source: [ANI report published by Deccan Chronicle](https://www.deccanchronicle.com/business/companies/140518/bajaj-finserv-no-cost-emi-option-on-4-lakh-products-on-flipkart.html), May 14, 2018.
- Evaluation date: May 13, 2018. Documented sale window: May 13 to May 16, 2018.
- Post summary: discounted products including mobiles with Bajaj Finserv No Cost EMI. No numeric mobile discount is invented.
- **Documented recipient:** Bajaj Finserv, explicitly named as the financing partner through lending arm Bajaj Finance.
- **Inferred recipients:** TVS Credit, HDFC Bank, ICICI Bank and Axis Bank could propose eligible smartphone/appliance financing. Participation in this named sale is not verified.
- **Must not notify:** Bajaj Auto or TVS Motor. Manufacturing is not EMI financing, regardless of similar brand names.

### 2. Swiggy Diwali food coupons

- Post: `p02_swiggy_diwali`.
- Source: [official Swiggy Diwali Bonus terms](https://blog.swiggy.com/terms-and-conditions/diwali-bonus-engagement-emailer-tcs-12-11-2020/), November 11, 2020.
- Evaluation and validity date: November 12, 2020 only.
- Post summary: emailed answers unlock 70% off up to ₹201 for the first 50 users, 60% off up to ₹151 for the first 100, or 50% off up to ₹101 for the first 2000. Minimum order ₹150; food orders and first-come redemption only.
- **Documented recipient:** PhonePe, based on the [March 22, 2018 checkout partnership](https://www.phonepe.com/press/swiggy-and-phonepe-partner-to-grow-cashless-transactions/), not proof that the coupon stacks with PhonePe cashback.
- **Inferred recipients:** Google Pay, Paytm, HDFC Bank, ICICI Bank and Axis Bank could propose checkout incentives. These coupon terms do not specify a payment instrument or establish offer stacking.
- **Must not notify:** Zomato, a seeded competitor without a subscription; Bajaj Auto and TVS Motor, which have no complementary food-payment role.

### 3. Swiggy ICICI card-only food discount

- Post: `p03_swiggy_card_only_new`.
- Source: [official ICICI Bank offer terms](https://www.icici.bank.in/offers/swiggy-offer-food-order). October 3, 2025 is the documented offer start, not a verified page-publication timestamp.
- Evaluation date: October 3, 2025. Valid Fridays to Sundays through December 28, 2025.
- Post summary: ₹50 off a minimum ₹599 food order for eligible new/dormant ICICI-card users, defined by no ICICI-card Swiggy transaction in the preceding 60 days. Once per user, card and calendar month. Corporate cards, Amazon Pay ICICI cards, debit cards, UPI and net banking are excluded.
- **Documented recipient:** ICICI Bank, the named issuer.
- **Inferred recipients:** HDFC Bank and Axis Bank could propose their own card-funded food promotions. Their cards cannot redeem this specific ICICI discount.
- **Must not notify:** PhonePe, Google Pay and Paytm in their scoped UPI/wallet roles, because this post requires a credit-card role.
- The separate expiry specification evaluates this same post on December 29, 2025 and expects no routing and zero judge calls. It has not run yet.

### 4. PhonePe historical UPI and instant-cashback update

- Post: `p04_phonepe_upi_cashback_update`.
- Source: [official PhonePe Big Billion Days update](https://www.phonepe.com/press/phonepe-sees-a-150per-growth-in-transactions-during-flipkarts-big-billion-days/), October 22, 2018.
- Evaluation date: October 22, 2018. No promotional end date is supplied, so `valid_until` is null.
- Post summary: UPI accounted for over 55% of PhonePe payments during the historical sale; the source separately reports instant cashbacks without delays.
- **Inferred recipients:** Swiggy, Flipkart, Amazon India, Myntra and MakeMyTrip could act on the merchant-checkout/cashback model. All five labels are inferred action opportunities, not verified eligibility or partnership claims.
- **Must not notify:** HDFC Bank, ICICI Bank and Axis Bank under the scoped profiles, which declare card/EMI roles rather than a merchant-specific UPI campaign role.
- **Approval qualification:** the source describes a mixed-instrument campaign. It does not establish UPI-only cashback eligibility or a new broadly redeemable offer. This is a proposed market-update substitute for the plan's UPI cashback hard case, not a silently completed original case.

### 5. Bajaj Auto priced motorcycle launch

- Post: `p05_bajaj_motorcycle_purchase`.
- Source: [official Bajaj Auto Pulsar N250SS release](https://www.bajajauto.com/news-media/press-releases/bajaj-auto-introduces-the-new-pulsar-n250ss-with-a-4v-engine), October 21, 2026.
- Evaluation date: October 21, 2026. No offer expiry is supplied.
- Post summary: Pulsar N250SS at ₹1,59,406 ex-showroom Delhi, with a four-valve engine, six-speed gearbox and ETB ride modes. This is a launch, not a claimed discount or financing agreement.
- **Inferred recipients:** Bajaj Finserv and TVS Credit could finance eligible buyers through their two-wheeler lending roles. Neither exact manufacturer/dealer partnership is verified by this release.
- **Must not notify:** Swiggy or Zomato, which have no vehicle-financing action. Similarity of the Bajaj names is not the reason for accepting Bajaj Finserv.

## Qualifications requiring review

1. Approve or replace the qualified PhonePe market-update interpretation in sample 4. The original UPI-only promotional eligibility has not been verified.
2. Accept or revise the distinction between proposing a new card promotion and converting a named issuer's existing card balance. The latter labels only that issuer.
3. Accept the scoped payment roles. Apps can carry bank-issued cards and banks can provide UPI; omitting those roles here is a benchmark scope choice, not a factual denial.
4. Historical posts use `now = as_of`, but profiles are static simulations checked in November 2026. This is not a historical capability census. Unknown expiry is not evidence that a historical offer remains active today.
5. Some posts share sources and `series_id`; results must disclose their dependence. Near-repost cosine must be measured before claiming that fixture satisfies the 0.95 condition.

## Next action after approval

Arrange dataset access in Colab, then generate embeddings and M0/M1 results. A repository clone needs a remote URL; the supplied local folder cannot be cloned in Colab. A manual dataset transfer is an alternative, to be arranged separately without repeating granted secret or Drive permissions.

Stop again after M0/M1 for checkpoint 2. Model and threshold choices remain Anand's decisions. No FastAPI app, database, delivery worker or dashboard is authorized in this stage.

Original session start: `2026-11-15T03:59:03.629000+00:00`. Hard stop: `2026-11-15T07:19:03.629000+00:00`. The timer is not reset. Paid spend remains USD 0.00000066.
