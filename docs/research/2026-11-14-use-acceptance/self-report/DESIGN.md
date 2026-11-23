# Can the frozen judge say what sized its band? The self-report diagnostic (council rounds 13 and 14, under D439), frozen before any send

**What it can decide.** D520 left Alex a choice for answers where nothing sizes the amount: A leave it, B show the band with a plain
label of what it rests on, C show no band. B needs a judge that can tell, of its own answer, whether the evidence sized the band.
This test asks whether the frozen judge's own after-the-fact account separates answers two reader families settled as resting on
too little (or unsupported) from answers they passed on the same question paths. A positive result justifies investigating a
label (it does not show the live judge can emit one, that the page carries it, or that it survives to the next day); a negative
result closes this question and this wording, not every label design. Nothing in either system changes.

**Cases** (`prepare_cases.py` → `cases.json`, $0): the Stage B reading (the frozen judge on the new system's own questions, July
window, three draws, every day's answer read by two families). Failed: the 22 figure answers settled INSUFFICIENT (19) or
UNSUPPORTED (3), on 6 question paths. Passed: the 23 figure answers both first readers passed on those same paths (one path, u3 v10,
has none). Days of one path are not independent: results are reported per path.

**The send** (`self_report.py`, a copy of D519's `judge_account.py` with these cases and this question): each stored request is
rebuilt by `model.build_request` with the frozen judge's setting and schema and refused unless its archive identity (the sorted-key
hash of `model.request_identity`) equals the stored key: this proves the same content, not the original wire bytes or key order
(45 of 45 match, dry run). The stored answer is given back as the judge's turn (its stored JSON, serialised again; the model's
hidden reasoning is not stored) and one fixed question is asked; the structured answer form is dropped. This is a retrospective
follow-up, not the live call and not a test of a label emitted inside the call. Model, effort and output allowance kept; one
attempt; eight calls at a time; cost at published rates. **Bound $0.403** (a conservative bound under the stated token and framing assumptions; a breach inside a batch is caught only after it): per call the original call's recorded input tokens
(the provider's count for the same content), the added messages at one token a byte (a token holds at least one byte) plus 50
each for framing, the whole 16,000-token output allowance, no cache discount; the script refuses a ceiling below the sum. A call
whose usage lacks either token count is charged at its bound; an output count above the allowance is a breach. After each batch of
eight the script stops if any call cost more than its bound or if the spend plus the remaining bounds would pass the ceiling.
Ceiling $0.45.

> In the answer you just gave, what places the amount in the band you chose? Begin your reply with a first line of exactly
> "LETTER: " and one letter, then one sentence naming the evidence ids or the assumption. A: a figure stated in the evidence shown
> places it in that band. B: a calculation that uses only figures stated in the evidence shown places it there. C: an assumption
> or estimate of your own, which the evidence shown does not state, decides the band, including a calculation in which such an
> assumption decides the band. D: nothing in the evidence shown sizes the amount. E: mixed, or you cannot tell.

**Scoring** (`score_self_report.py`, self-test 11 of 11 before any send): the letter is read only from a first non-empty line of
the form "LETTER: X"; anything else (no such line, a refusal, a transport failure, a case missing from the records) is unresolved
and kept in the denominators; unknown or duplicated cases make the scorer refuse. A warning is C or D. E (mixed, cannot tell) is
counted with the unresolved and reported apart. Misses = failed answers without a warning; false alarms = passed answers with one.
Every count is printed twice: unresolved and E as no warning, and as a warning (checked at $0 on made-up accounts: C on every failed
and E on every passed case gives 23 unresolved, so unclear, and 23 false alarms under the second counting). Claude reads every reply's
sentence against its stored answer and request and records, by hand, any letter its own sentence contradicts (reported beside the
counts; the counts are not changed by it).

**Baseline on exactly these cases:** D520's keyword rule warns on 17 of 22 failed and 21 of 23 passed (misses 5, false alarms 21).

**Decision rule, written before the send** (the five paths holding both sets are related days of six matters, not independent
tests; every path's counts are reported, and the path with no passed answer is not compared):
- **Separates** (a label is worth investigating): under both countings of unresolved replies, misses at most 7 of 22 and false
  alarms at most 7 of 23.
- **Does not separate** (this wording's self-report route is closed; not every label design): under both countings, false alarms
  12 or more of 23, or misses 12 or more of 22.
- Anything else, or more than 4 unresolved or E replies, is **unclear**, reported as such; no second wording is sent on this result.
- Whatever the result, it does not show that the live judge can emit a label, that the page carries it, or that it survives to
  the next day, and it does not settle Alex's choice.
