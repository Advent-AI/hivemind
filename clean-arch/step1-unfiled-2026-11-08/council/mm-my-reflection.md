# My reflection on the census and the next repair, written before the council (2026-11-13)

- **The census** (`clean-arch/e2e-comparison-2026-11-13/RESULT.md`): both systems agree with reader B on 1–2 graded questions a draw
  (production 3 in all, clean 4; 2 unresolved each); every eligible judgement agrees; every loss is at opening. So the judging step is
  not where the product loses on the ruler; how questions are opened is.
- **The largest class, read against the frozen standard** (`docs/prd/05-extraction-standard.html`, §3 and §4): event deadlines.
  - q08 (China H200): the standard says a pending regulatory decision with no date takes the current fiscal year-end (role-v12: "A
    pending regulatory decision may lack a date; use the current fiscal year-end as its due date"): 2027-01-31, the ruler's day.
    Production used 2026-12-31 (and narrowed to AI firms). A breach of the standard.
  - q18 (Kyber): D248 boundary 2: "同一件事的不同截止日：早的那题开着时，晚的截止日是它的证据"; product nodes ask the step that brings
    revenue, "下一代机架系统能否在 2027 年底前开始出货". Production asked "by 2028" (the reported slip) in all three draws. A breach.
  - q23 (Ohio): the standard lets an unsigned obligation take a check date "文章后 18 个月以内"; the ruler chose 2027-06-30, production
    2027-07-01 and 2027-12-31, all inside the standard's range. D430 requires the same deadline, so a one-day difference makes the answer
    ineligible though it agrees. A measuring-stick concern, recorded apart under D373, scoring unchanged.
  - Beside it: q05 (memory, 2027 against 2026) opened by neither system in six draws; q04/q13 production splits the years in 2 of 3,
    the clean path did not (and c15yc's fix moved the memory question, D441).
- **My lean for the next repair:** on the clean path (the production candidate), set event deadlines by the standard's own rules in
  code where the rule is identity, as D414 did for figure due days (18 of 34 → 33 of 33): a pending regulatory decision → the company's
  current fiscal year-end; a product node → the planned date, a reported later date filed as evidence (D248 boundary 2); an unsigned
  obligation → the model's date within 18 months, unchanged (the standard leaves it open). Test: the stored clean theses and the census's
  matched views at $0 (how many event questions the code rule would move onto the ruler's deadline, and how many it would move wrongly),
  then a small probe. Strongest argument against: it is fitted to three graded questions; the census also says the clean path is level
  with production, so the gap that matters for D427 is not here but in Step 4's failed lines.
