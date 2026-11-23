# judging-v13s blind test, third run after D742: result (SMALL-DESIGN.md §5 [D742])

**STOP on one registered line, as written** (council round 57 confirms): "an accepted reply with a named defect (marked by both readers …)".
- **R01 (S, Claude writer).** Both readers marked "broken structure" on F14: the outcome is a range of $679.25–745B, and rung 4
  ($700–800B) does not hold all of it.
- **Both adjudicators reject that mark.** The schema the writer was given says the rung is "for a range outcome, a band it overlaps,
  with the reason in reasons". The answer gives that reason: "the midpoint and most of the range lie in rung 4". The code (S6) checks
  overlap.
- **The cause is my reader brief.** Its definition of broken structure reads "a rung whose band does not hold the outcome", without the
  schema's range clause. Both readers applied the brief as written. No earlier run had a range that crossed a rung edge, so the gap was
  not exercised before.

Everything else in the run is clean:
- **Writers:** 12 of 12 schema-valid, 12 of 12 accepted, 0 refusals, so there was no refusal review.
- **Readers and adjudicators:** six packets drew a disagreement. Every disputed mark was settled, and every one was rejected by both
  adjudicators. No defect was upheld, and no split remains.
- **Every case has a usable reply.** The joint case has both forecasts supported in one reply (R02 and R11).
- **The D742 rule was followed by every P-family writer.** All six recorded the Q4 pace as an estimate naming its benchmark, then
  computed Q4 from it. None computed a guidance rate straight into the calculation.

**Run:** `poc/data/judging-v13s-blind3-2026-11-22/`, $0 at the provider. All Codex writers read only `system.txt`, `user.txt` and
`schema.json`. The tally is in `TALLY.json`.

## 1. Writers' first answers (`CHECKED.json`)

| Case | Claude writer | Codex writer |
|---|---|---|
| P (joint) | v4 416.3, v8 386.1, both rung 2 | v4 420.9, v8 391.0, both rung 2 |
| P-v4 | 419.3, rung 2 | 416.3, rung 2 |
| P-v8 | 387.4, rung 2 | 388.1, rung 2 |
| S (CY2026) | 679.25–745, rung 4 | 670.5, rung 3 |
| O | 9–20, rung 1 | 16, rung 1 |
| E | 37, rung 3 | 34, rung 3 |

## 2. Readers and adjudicators (`TALLY.json`)

**Settled as not defects (both adjudicators reject):**
- R01 broken structure (both readers' marks), explained above;
- R01 "two forecasts" (Microsoft backed out of the four-company tallies, a reader matter through `rests_on`);
- two "plus or minus 2%" midpoint marks (R02, R09) and a rounding difference within tolerance (R08). In all, both adjudicators
  rejected 8 marks covering 7 distinct allegations (F14 was marked twice);
- R06's "number misread" claims on the $18B schedule and the Lancium tranche.

**Support:**
- **R07 (S, Codex writer) is settled "not supported".** Its rung rests on a 90% data-center share, while the passages put the share near
  100%:
  - e1947: more than $730B "on AI infrastructure" against $720–745B of capex;
  - e2759 and e5376: NVIDIA's "nearly $800 billion" for the top five, written both as capex and as data-center capex;
  - Meta's own figures: about 96%.
  At 94% or more, the same $745B gives rung 4. The reply is accepted and publishable, but its rung does not follow from the evidence.
  This is not a registered stop line (usable is counted per case, and S has R01). It is a real judgement error in an answer that would
  publish.
- **R06 (O, Claude writer) is split again** on the $18B reading: Codex says not supported, Claude says supported. This is the same
  passage as in both earlier runs.
- Every other forecast is supported by both readers or both adjudicators.

## 3. What the test shows

- **The writer-side contract holds.** In three runs, the request has moved from 11 of 12 accepted with a checker error (run 1), to 11 of
  12 with a request contradiction (run 2), to 12 of 12 with no refusal (run 3). D742's rule was followed by all six writers it applies
  to.
- **The stop this time is in the measuring instrument.** The reader brief's definition is narrower than the format the writer was
  given. Both adjudicators corrected it from the format rule.
- **The readers did their job on substance.** They found the one reply whose decisive assumption is unsupported (R07). That is the
  kind of error the paid re-send is meant to measure in gpt-6-luna.
- **Council round 57 found two more points** (`codex-r57.md`):
  - R01, the only usable S reply, marks Zacks's $720–745B of *total* capex as the market reference for *data-center* capex. Claude's
    reader noticed it in its ground but filed no named defect.
  - R11's prose offers "$138 billion in Q4" as reaching rung 1, but it gives $428.32B against the $431.2B edge. The forecast itself
    sits in rung 2.
- **Open disclosures:**
  - O's $18B reading (split three runs running);
  - wrong numbers in prose, which this run's adjudications did not raise;
  - R07's unsupported share.

## 4. The blinded re-read (D743, Alex: "补上那条，重读一遍"; `reread-packets/`, `reread-adjudication/`, `REREAD-TALLY.json`)

Fresh readers re-read the same 12 replies under the corrected range rule. Two controls were mixed in, under a fresh shuffle Q01–Q14.

- **The range repair works.**
  - C-disjoint was marked broken structure by both readers.
  - C-overlap was marked by neither.
  - R01 (now Q07), the range across a rung edge, was not marked broken structure by either reader.
- **STOP again, as written: Q10 (P-v8, Codex writer).**
  - Both readers marked "number misread" on F6: "$108.0 billion, plus or minus 2%" given as its midpoint, 108.
  - Both adjudicators rejected it. The schema the writer was given says "'$4.5 billion, plus or minus 3%' in full, given as low and high
    or its midpoint as value".
  - The same mark has been raised about 12 times across the four readings, by single readers until now. Every adjudication rejected it.
- **The class.** The readers' packet carries the user text and the answer, but not the format rules the writer was given. The
  adjudication packet carries them and its definitions say "allowing what the format rules permit". Both stops caused by the instrument
  (the range, the midpoint) come from this one gap.
- **C-overlap's other mark is my error.** Both readers marked "two forecasts" on C-overlap because my control kept E's original text
  ("85% … $37 billion") beside the new range. The readers were right to flag the inconsistency. It does not touch the range rule the
  control tests.
- **Judgement noise:**
  - S's Codex reply (90% share) was settled "not supported" by both adjudicators in the first reading, and is "supported" by both fresh
    readers now.
  - S's Claude reply (Q07) is split at both levels this time: Codex says not supported and upholds two marks; Claude rejects them.
  - O's Claude reply (Q09) is split again.
- **No settled defect.** Every adjudicated mark on Q09, Q10 and Q14 was rejected by both adjudicators. Q07's two marks split.

## 5. The second blinded re-read (D744, Alex: "批准再重读一次"; `reread2-packets/`, `reread2-adjudication/`, `REREAD2-TALLY.json`)

Readers now get the same rule text as adjudicators (`blind_rules.py`). There were five clean controls, under a fresh shuffle T01–T17.

- **The instrument is calibrated.**
  - All five controls passed: K-midpoint was not marked; K-misread was marked by both readers; K-overlap was not marked; K-disjoint was
    marked by both; K-unsupported was "not supported" by both.
  - On the 12 replies, no defect was marked by both readers. The class from §4 (format-permitted forms marked) did not recur.
- **STOP on two registered lines, as written.**
  1. **A settled defect on an accepted reply: T10 (S, Claude writer), F11.** e1416 writes "an estimated $750 billion". The writer
     recorded qualifier "none", and both adjudicators upheld "number misread". But "estimated" is not in the qualifier list the schema
     enumerates (`calc_small.QUALIFIERS`), so "none" was the only value the format allowed. The descriptions the adjudicators saw say
     "the qualifier the quote writes just before the number" and do not list the allowed values. This is a format gap: the closed list
     and the description disagree.
  2. **A case with zero usable first replies: S.**
     - S's Codex reply is "not supported" by both readers. Its 90% data-center share decides rung 3, and the passages do not size the
       share.
     - S's Claude reply is split at both levels. Its 95–100% share sets the range, and Codex says the passages do not support 95% as
       the low end.
     - Both writers met D741 ruling 3's letter (a stated deduction), but not its "supported" part. That is a judgement weakness of the
       writers on this question, caught by the readers, not an instrument error.
- **Other settled support:**
  - E's Codex reply is now "not supported" by both readers. Its 15% cut from the guided $40B floor decides rung 3 without passage
    support. Earlier readers had supported it, and the two-step brief (name the evidence for the band-setting assumption) made readers
    stricter on such cuts.
  - O's Codex reply is supported after adjudication; O's Claude reply is split again.
- **Usable replies per case:**

  | Case | Usable replies |
  |---|---|
  | P | both writers |
  | P-v4 | both writers |
  | P-v8 | both writers |
  | O | Codex |
  | E | Claude |
  | S | none |
