# Claude's own round-1 findings on the traces (written while the Codex reviewers ran)

Each finding cites the trace (`traces/split-v2-confirm-first100-2026-11-05/<seq>.json` and `_ledger.json`).

## J1. The part-period ladder reference leads the frozen judge to count growth twice (serious; caused by my change)

- v79 "What total revenue will TSMC report for fiscal 2026?" (created 1240). Ladder neutral: around NT$4.8 trillion, "the annualized Q2 2026
  pace". Judgements 08-29 and 08-30: rung 1; reason: "Carrying the reported 36% year-over-year growth forward implies about NT$6.53 trillion
  (NT$4.8T × 1.36)". The year-over-year growth is already inside the Q2 level; applying it again to an annualised current quarter counts it
  twice. The seven months reported (NT$2.872 trillion, item 1275 in the final run) point to roughly NT$5 trillion for the year.
- v84 ACIE revenue: "Carrying the reported 25% sequential growth forward gives an implied FY2027 total of about $185.9 billion" (rung 1),
  compounding one quarter's sequential growth.
- PRD 06 (ladder rule 2, and the judging row, D260): the neutral rung states its comparison, and the judgement forecasts against "what the
  market expects (consensus, guidance, the stated plan or deadline)"; its own example compares with the prior year ("FY2027 China revenue versus
  FY2026"). A run-rate derived from one quarter is none of these. Judging is frozen (D354), so the ladder must not invite this error.
- Candidate fix to settle in review: the reference is guidance or consensus when given; otherwise the prior year's reported figure (growth
  bands, as PRD 06's example); a part-period figure is evidence, not the reference; no reference of these kinds → no ladder. To prove on the
  stored record-preparation requests and then on the stored judgements (re-sent with the new ladder) of v79, v84, v75, v78, v85.

## J2. Questions whose period is a month (minor)

- v86 "What will the year-over-year U.S. headline PCE price-index inflation rate be in December 2026?" (1271). The standard's D class is a
  quantity "for this or next calendar year"; a single month's reading is a point in a series. Its judgement reasons from July's monthly
  change annualised. Count across the three runs before any change.

## B1. B misses a schedule that belongs to an open question (minor)

- 1210: "Of this total, $92 billion is due in the remainder of fiscal 2027, followed by $87 billion and $88 billion across fiscal 2028 and
  2029" not written, although v70 (supply commitments) was open; the headline $279 billion passage was written to v70.

## A1. A opens the next-year revenue question late (minor)

- 1210 carries "Kress spoke about 70% total revenue growth in fiscal 2028"; no FY2028 revenue question was open and A proposed none; v72
  "What total revenue will NVIDIA report for FY2028?" opened at 1213. A recall miss on one item; the evidence at 1210 was dropped with it.

## Production observations

- P1. `parallel_day` (D183) prepares requests ahead; D375 requires each item to read the questions committed before it. In the three v2 runs,
  13–22 questions opened over 76 items: every such item changes every later item's request.
- P2. The research runner keeps its own subject table (`poc_subjects`), its own resume records and a reuse path from an earlier run; none of
  these exist in the production path.
- P3. Acceptance on the frozen ruler needs the 22 seeds as the starting library (the judgement scorer refuses other seeds), which D370 retired
  as product behaviour.
