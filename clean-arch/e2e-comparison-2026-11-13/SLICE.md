# The one-day slice (D443), 2026-11-13

Run `poc/data/clean-e2e-comparison-2026-11-13/slice/` (manifest with sha256s; `poc-v118`/4f2aad7d25dae54d, provider openai, no seed),
2026-07-01 only, run cap $0.25, under the shared ledger (ceiling $5.00).

- **Completed:** 13 items, 13 extracted, 0 failed; 7 evidence; 2 new views, both judged; 23 calls; ledger spent $0.0211, nothing left
  reserved, no refusal, no overrun.
- **Its own views** (`opened-slice.json`, `extract_opened_prod.py`: no seeded view): v1 "By NVIDIA's FY2027 annual report, what amount
  of credit-support obligations will NVIDIA report for its AI cloud infrastructure programme?" (five numeric rungs with bands, due
  2027-02-28, judged rung 3 on 2026-07-01); v2 "Will NVIDIA sign a financial guarantee for OpenAI's Ohio data-center lease by
  2027-12-31?" (Yes/No rungs, due 2027-12-31, judged rung 1 on 2026-07-01).
- **The readers read it:** `prod_records.outcome` reads rungs with bands and yes/no labels and the last judgement by day;
  `prod_records.shown_evidence` returns the evidence listed in each view's judge requests (v1: e1–e5, e7; v2: e6). The shape matches what
  the comparison reads.
- **Cost check:** about $0.0016 a processed item on this day; the stored seeded runs averaged $0.0027 an extracted item over 14 days
  (with 22 more views judged). Three 14-day draws should cost well under the $1.00 run caps.
