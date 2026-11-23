# The self-report diagnostic: result (D565), 2026-11-16, $0.0346

Replies and spend: `poc/data/clean-self-report-2026-11-16/` (`accounts.json`, `reply-*.json`, `spend.json`); score: `score.txt`.
45 calls, 45 replies, no error, no unresolved reply, no E; $0.0346 at the published rates (bound $0.403, ceiling $0.45).

## By the rule frozen before the send: does not separate

| | Letters | Warnings (C or D) |
|---|---|---|
| Failed (22: settled too little or unsupported) | C 20, D 2 | 22 (misses 0) |
| Passed (23: both first readers passed, same paths) | C 21, B 1, A 1 | 21 (false alarms 21) |

False alarms 21 of 23 (the rule: 12 or more closes it), the same as D520's keyword rule on these cases (17 of 22, 21 of 23).
Per path every failed answer warns and almost every passed one does too (`score.txt`). **This wording's self-report route to a
label is closed.** No second wording is sent on this result (the design's rule).

## What Claude read in all 45 sentences (a hand reading after the score; it changes no count)

The judge's sentences are specific and agree with its stored answers; none contradicts its letter. The letter C held two
different things:
- **Failed answers:** 21 of 22 sentences say the total or the chosen band is not stated or calculated by anything shown ("my own
  estimate", "no evidence item states or calculates that total"; some name an unquantified figure, e.g. Trainium's "multi-billion-
  dollar business"); the 22nd applies an unstated scaling to a stated $119bn.
- **Passed answers (corrected count, council round 17):** 19 of 23 describe an unstated assumption (a scaling, an execution
  discount) applied to amounts the evidence states (Sharon AI's $4.88bn backstop, Broadcom's $26.8bn); 2 say the combined total is
  not stated or calculated; 1 describes a calculation from stated figures (its stored answer does scale one partner's figure to
  another); 1 says a stated $119bn places it.

The sentences are what the judge says afterward and can rationalise an answer (`u3-v1-21`); they are not an independent account of
what the evidence supports. With that limit, the split resembles D520's own: (1) nothing sizes the amount, (2) an estimate built on stated figures with a step of
the judge's own. The question's option C, as revised in council round 14, put "a calculation in which such an assumption decides
the band" in C, which merged case (2) into case (1). This reading is post hoc and by the author of the design: a lead, not a
result. It does not establish that case (1) is exactly the readers' failure class: D519 records three failed answers decided by an
unsupported step, and two passed answers here say no total was stated or calculated.

## What it shows and does not

- Shows: asked this closed question after the fact, the frozen judge says its own assumption or estimate decided the band in 41
  of 45 answers, passed and failed alike; the letter cannot tell the readers' failed answers from their passed ones.
- Does not show: that a label distinguishing "nothing stated sizes it" from "an estimate built on stated figures" would work live
  (untested; the lead above is one author's reading of one sample of related days, mostly two matters), or anything about Alex's
  choice between A, B and C.
