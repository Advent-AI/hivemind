**PARTLY** — I’d use it to find source documents and verify milestones. I’d keep my own earnings forecast.

**Most useful — v4.** The earnings call gives the August Vera Rubin shipping date, the 10-Q confirms the fiscal quarter, and a customer deployment corroborates it.

**Most unsatisfying — v9.** It forecasts $146B of Q4 Data Center revenue while v14 forecasts $127B for all of NVIDIA. I’d have to rebuild the forecast before using either number.

### The list

Keep revenue (v9/v14), margin (v28/v33), customer spending (v5/v6), Rubin (v4), and customer financing (v1/v2). The biggest missing bets are how much Blackwell can ship through the Rubin transition and how much business AMD and customers’ own chips could take. v3/v22 and v30/v31 are exact duplicates. v1/v2 substantially overlap, and v14/v21 and v35/v17 express the same revenue bets in dollars and growth rates. I’d drop standalone cards for the Fed meeting (v41) and one Virginia site’s utility terms (v42).

### Big numbers

- **v14 — Defensible at $400–450B.** Reported first-half sales, a historical guidance beat and an assumed 12% Q4 increase sum to $418.6B. The August drop and rebound follow identifiable changes in Q3 estimates. The Q4 increase is an assumption.
- **v9 — $410B is unsupported as presented.** The $164B first half and roughly $100B Q3 are sound anchors, but $146B in Q4 means 46% sequential growth and exceeds v14’s company-wide forecast. The September 20 upgrade reused July’s SemiAnalysis estimate, already used in August, with its underlying forecast unspecified.
- **v5 — $700–800B is unsupported for data centers.** The four are Amazon, Alphabet, Microsoft and Meta, but the $720–760B figures cover total capex. The five moves around $700B repeatedly switch between spending measures.
- **v6 — $1.1–1.2T is unsupported.** The August move has a clear trigger and the arithmetic works: $1.3T × 730/800 ≈ $1.19T. The ratio mixes spending measures and assumes the same four companies retain their share in 2027.
- **v28 — Defensible at 73–76%.** Revenue-weighting the quarterly margins at their midpoints gives about 73.6%. August’s lower Q4 outlook pulled the estimate down within the same band.

I’m a model reader. My estimate of analyst usefulness is that **4 of the 25 sampled uncited items** add something worth keeping alongside the citations. The rest mostly repeat known figures or lack a usable link to the forecast. That’s a sample judgment.

### Events and other bets

- **v4 — Yes, confirmed.** The call and 10-Q say production shipments began, and TechTarget reports seven CoreWeave racks in production.
- **v34 — Yes, confirmed.** The 8-K records signing on September 2. The answer stayed Yes as talks became a signed agreement.
- **v43 — Yes is a tentative management case.** The filing makes closing conditional on approvals. The cited article reports filing requirements and potential objections. Clearance timing remains unverified.

**China, supply and competition.** v10’s Yes is plausible for selective H200 permissions. The 10-Q describes small shipments under U.S. licenses and continuing Chinese restrictions. I’d want a China revenue range that accounts for both governments’ rules. v15’s $187B remaining supply commitment before additions is a reasonable starting point, but the extra $28B is thinly supported. v28/v33 cover margin. Blackwell shipments and competitive losses still lack their own forecasts.

### Facts checked

| Claim | Source input ID | Result |
|---|---|---|
| Rubin production shipments began in August | `truenorth:transcript:NVDA:2026-08-26` | Right |
| CoreWeave had seven racks and 504 GPUs in production | `gnews:8392653145e1e67a11ab3654` | Right |
| Hugging Face agreement signed September 2 | `edgar:NVDA:0001045810-26-000078:nvda-20260902.htm` | Right |
| $12.9B was the purchase price | `edgar:NVDA:0001045810-26-000078:nvda-20260902.htm` | Wrong. $11.9B plus up to $1B in retention awards |
| Both clearances will arrive by June 30 | `gnews:7a5002df93385ecef12a2cd8` | Not checkable |
| Q2 revenue was $96.2B, including $89B Data Center | `nvidianews:nvidia-announces-financial-results-for-second-quarter-fiscal-2027` | Right |
| Q3 guide was $108B ±2%, excluding China Data Center compute | `nvidianews:nvidia-announces-financial-results-for-second-quarter-fiscal-2027` | Right |
| The four’s $760B was specifically data-center capex | `gnews:c8ea23246edff9fbbc981992` | Not checkable. The article says capex |
| The $1.3T estimate was for five hyperscalers in 2027 | `truenorth:transcript:NVDA:2026-08-26` | Right |
| Q4 margin outlook was 71–72% | `truenorth:transcript:NVDA:2026-08-26` | Right |

### Before daily use

1. Reconcile forecasts across cards and show which assumptions move them.
2. Track Blackwell volumes, competitive losses and China revenue exposure.
3. Merge duplicate bets, retire settled milestones and put the decisive sources first.