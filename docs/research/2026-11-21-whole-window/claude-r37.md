# Claude's own position, round 37 (written before reading Codex's)

## Verdict as registered
Pilot pair 1 is inconclusive (control double refusal, §4 (2)), unless linked-1 double-refuses (then fail, §4 (1)). Nothing else can
change it under the registered rules.

## Mechanism
One-character copy errors of listed evidence ids (e3620 -> e362; e3110 -> e3111), refused by `check_answer`, the retry repeats the
class. Same class as 5 of 7 refusals on the three stored v118 runs (none of their retries refused). A defect of the frozen judge,
independent of the links (the control runs poc-v118, which has no links).

## Recommendation: C, with the rule written before linked-1's P rows are read
- Rule for every remaining sequence, both arms: a double refusal resumes the day once in the same store, as the product does
  (`replay.run` resumes after the last completed day; the day's items route as skipped; `judge_day` re-runs at the same sequence;
  views already judged at that sequence are not judged twice; the refused rows stay retired so the failing question is re-sampled).
  A second double refusal on the same day is terminal under the old precedence. Every refusal still counts in H1.
- Why it is not selection: the stop fell on v21, which feeds neither P question in the control (no dependencies in poc-v118; none of
  the 118 fresh v9/v14 requests mentions v21). The resumed days 09-08..09-20 are fresh samples, as any re-run would draw. Against B
  (a full re-draw), C keeps a control whose lead (28 definite of 60) is below old-2's 50: choosing C over B does not favour the linked
  arm; a re-draw could only move the control nearer old-2's higher count.
- The symmetric cost: a linked double refusal no longer fails on its own; it fails only if it recurs on the resumed day. That matches
  the product (a resumable day), not a product failure.
- Cost: about 13 days x 3-4 reader calls, about $0.15, inside the $2.50 ceiling (about $1.6 spent when linked-1 ends).

## Harness work it needs (at $0, before the send)
- A `resume` command: only a sequence whose terminal outcome is `double refusal`, only once (a marker file); no `prepare`; the same
  admission and latch; segment 1's summary kept as `summary-segment1.json`; the combined summary in the same schema.
- Freshness across segments: a reader judgement is fresh when its call lies in its own day's window in either segment (segment 1's
  windows read back from its dated judge rows).
- H1 over both segments' dated rows; H2 and the calendar over the whole store; the terminal record keeps the first double refusal.
- Checks: the dry double-refusal control resumed with the plain fake judge must be accepted (positive control); mutants: a second
  resume refused; a resume of a sequence that did not stop on a double refusal refused; segment 1's windows ignored must fail
  freshness.

## Product finding for Alex (not built)
The judge copies long id lists; a one-character slip refuses the whole answer. One structural rule candidate: evidence cited by its
list position, which code maps back to the id (code owns identity). A new version of the frozen judge, Alex's to open.
