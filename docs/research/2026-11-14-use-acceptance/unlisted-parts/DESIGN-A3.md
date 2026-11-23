# Arm A3: A2 plus one check of an event's not-judged list (design for the council, 2026-11-16, version 11, council rounds 80 to 89; nothing sent)

## Why, from the record

- **A2** (`RESULT-A2.md`, D583):
  - It removed the unlisted parts on the motivating topics (control 6 topics, A2 0) with no refusal.
  - It kept every refusal control.
  - It was negative under the fixed rule.
- **Its one harm traced to the change is over-listing** (`OVERLIST-AUDIT.md`). 9 of 137 entries are not parts, against 1 of 71 in the
  control:
  - the outcomes an event's choices decide (a delay, a termination);
  - the material the answer is read from;
  - one comparison with the reference, which the control lists too.
- **The model's account** (`listing-accounts-output.txt`): it lists termination while saying "Formal termination is covered by
  'ruled_out'". Nothing in the request asks it to check an entry against its own outcomes.
- **The prompt audit** (`PROMPT-AUDIT-A3.md`, with a blind reader):
  - The closing check asks only whether something is missing from the list, never whether a listed entry is already decided.
  - The blind reader showed that a check written for every shape would remove, from a figure, a comparison or a second side that the
    ranges happen to settle. D397 and D436 keep those visible, and they are the kind the families split on (`DECLINE-AUDIT.md` §5:
    "not written into any arm").

## The change: one sentence, for an event only, added to A2's closing check after "…listed in not_judged?"

> *For an event, an entry that only restates one of its outcomes, the event itself happening, its being ruled out without naming
> how, or its still being awaited on the due day, is not a part the question leaves out: remove it. Keep every other entry, including
> a named way the event could be ruled out, a separate matter that would follow from an outcome, and a finer case inside one.*

**Why "a named way" is kept (round 86).** As the judge is shown it, Ruled out always reads "…. This rung holds when that, or any other
decision against the event of rung 1 …" (item 112). It therefore never says which decision it was.
- A termination by the parties, or a regulator's block, is a finer case inside Ruled out, and D409 lists such cases ("更细的区别
  列为'不判'").
- What the sentence removes is only an exact restatement of one of the three outcomes.

**The source, stated as an interpretation:**
- D409 (Alex: "发生了 / 明确落空（被否决、被放弃）/ 到期还没结果 … 保住了'否决'和'还在等'的区别；更细的区别列为'不判'") makes the
  three outcomes the answer.
- D397 shows the other parts as not judged.
- Together they support removing an exact restatement of an outcome, and keeping everything finer.

**Worked cases, against the complete choices as shown** (`PROMPT-AUDIT-A3.md` §9):

| Entry (stored) | Choices as shown | Sentence |
|---|---|---|
| "A delay past March 24, 2028" | Yes: closed by 2028-03-24; Ruled out: the parties terminate or abandon, or any other decision against; Still open: neither | removed: still awaited on the due day. A delay counts as still awaited only when the entry names no decision to defer; a formal decision to defer is a named way of ruling out, and an entry that does not say which is `cannot tell` |
| "Termination of the acquisition" | the same | kept: a named way of ruling out |
| "Whether the acquisition is repriced, delayed past the check date, or terminated" | the same | the repricing and the termination kept, the delay removed |
| "Whether MIIT blocks or delays the purchases" | Ruled out: MIIT formally denies, or any other decision against | the block kept, the delay removed |
| "The investigation's conclusion as a separate procedural milestone" | Yes: the Department publishes its decision or conclusion | removed: the event itself happening |
| "The investigation being formally concluded without a finding" | Ruled out: the Department formally abandons it without a conclusion, or any other decision against | kept: a named way |
| a payment due automatically at closing; Chinese restrictions on H200; a cap on the approval | — | kept: a separate matter; a second side; a finer case |

| Part | Source |
|---|---|
| an exact restatement of one of the three outcomes is judged, so it is not "not judged" (an interpretation) | D409, D397 |
| a named way of ruling out is kept | D409 ("更细的区别列为'不判'"); the shown Ruled out adds "or any other decision against" |
| a separate matter that follows from an outcome is kept | D436 |
| a finer case inside an outcome is kept | D409: "finer differences are listed as not judged"; system line 13 ("A difference inside an outcome … list it in not_judged") and its merger example, where Ruled out groups the regulator's block and the parties' withdrawal |
| events only; figures untouched | the blind reader's two counterexamples; DECLINE-AUDIT §5 |
| no example | round 79: a delay can be Still open or, decided formally, Ruled out; the actual outcomes decide |

**What is dropped, and why:**
- **The source-only clause.** No decision covers it.
- The census of the 66 stored topics finds no topic where a disclosure is itself a side part, so the distinction round 83 asked to
  exercise cannot be exercised.
- The 4 such entries in A2 stay a reported residual.

**Size:** about 300 characters; the closing check grows from 1,342 to about 1,645.

## The test: three arms on A2's 28 topics, three sends each (252 sends, about $0.23; caps $0.25 an arm)

- **The arms:** the frozen request (control), A2 and A3, all sent the same day and read blind together, with the same readers, plants,
  third readers and scorer as A2.
- **What the A2 arm gives:** an estimate, on this sample, of the sentence's own effect: A3 against A2. It does not isolate the cause.

**The stored population, classed by v8's kinds** (A2's run, the four event topics; my reading, one reader):

| Topic | A2 arm: restating entries or parts | named ways | cannot tell | control: restating |
|---|---|---|---|---|
| acquisition (fortnight clean-6) | 3 whole entries (the delay, p1 to p3) | 2 (termination, p1 and p3) | 0 | 1 part (the delay in p2's mixed entry) |
| purchase approval (fortnight clean-7) | 2 parts ("delays" in p2's and p3's mixed entries) | 2 ("blocks", same entries) | 0 | 2 parts |
| investigation (July c1/clean-5) | 0 | 2 ("concluded without a finding", p1 and p2) | 1 ("formally concluded as a separate milestone", p3) | 0 |
| export approval (fortnight clean-3) | 0 | 0 | 0 | 0 |
| **all** | **5 (3 whole, 2 parts)** | **6** | **1** | 3 parts |

The exercise threshold (at least 3 restating entries or parts in the A2 arm, as the blind classer counts them) is met on the stored run
with 5.

**The predicted verdict, written before the send:**
- **The first readers mark named ways `already_judged`:** termination twice, and "concluded without a finding". v8 keeps them by
  design.
- **Without adjudication:** motivating H counting unresolved points for the answer would then be the two untouched source-material
  sends plus about two termination sends, against 0. That is above control + 2, so **negative by construction, whatever A3 does with
  restatements**.
- **What a send can decide:** only through the adjudication below.

### The decision, written now (a diagnostic on preselected topics; any lead needs fresh material before a repair is claimed)

**A3 against the control:** A2's rules 1, 3 and 4, under both countings:
- no unlisted part or refusal on the motivating topics beyond one topic and one send;
- every exercised refusal control kept;
- a recovery gain of three correct written answers.

**A3 against A2: the sentence's effect, on the four event topics** (fortnight clean-6, clean-7, July c1/clean-5 and regression-watch
fortnight clean-3):

**The entries are classed blind.** Before the key is joined, a reader who sees neither the arm nor this design's predictions puts
each entry listed on the four event topics, from the reading packets, in one kind:
- restates happening;
- restates being ruled out without naming how;
- restates still awaited;
- a named way of ruling out;
- other;
- cannot tell.

A mixed entry is classed by its parts. A `cannot tell` part is printed in both arms, and the removal check is taken over its range
(r: restating parts; u: `cannot tell` parts; 2 for A2, 3 for A3):
- **passes:** even at worst, with every one of A3's `cannot tell` parts restating and none of A2's: r3 + u3 ≤ r2 / 2;
- **fails:** even at best, with none of A3's and all of A2's: r3 > (r2 + u2) / 2;
- **inconclusive:** anything between, and whenever r2 < 3.

**Two readings, both printed with their verdicts:**
- **Reading A (unchanged)** is the existing scorer as it is. Where both first readers agree, that settles the point, and only disputed
  points go to the third readers.
- **Reading B (diagnostic, new, pre-registered)** adds one step, applied to all three arms blind, before the key is joined.
  - **Which entries:** every entry the classer finds a named way in goes to the two third readers, one of each family, whatever the
    first readers marked. The readers get the reading form's own test quoted ("a rung decides a part only when holding that rung says
    whether the part happened"), the choices as shown, and no arm.
  - **What they rule:** each part of the entry, as the classer split it, with the H brief's four values.
  - **A part, from its two rulings:**
    - both `part`: holds;
    - both `already_judged`: fails;
    - both `settlement`: fails;
    - any disagreement, or any `cannot_tell`: unresolved, counted for the answer in one counting and against it in the other.
  - **The entry:** it holds only when every part holds. It fails when any part fails. Otherwise it is unresolved.
  - **An entry with no named way** keeps Reading A's settled mark.
  - **The send:** it fails H when any entry fails, exactly as Reading A counts it. A mixed entry whose named-way part holds still fails
    through another part that fails.
  - It is a separate function in the scorer, with its own tests:
    - matching `settlement` fails;
    - a disagreement is unresolved in both countings;
    - an agreed first-reader `already_judged` is overturned to `part`;
    - a mixed entry whose named-way part holds and whose other part fails, fails.
  - Reading A's verdict is printed first in every case, a diagnostic lead included.
  - **Outcome mapping:**
    - Reading A's verdict is the verdict on the reading as it stands.
    - When Reading A is negative only through named-way marks and Reading B is a lead, the result is "diagnostic lead", and it goes to
      the council before any next step.
    - When Reading B is negative, the result is negative.

**H stays per send, as the scorer counts it.** A send fails H when any one of its entries is settled other than `part`. Settling a
named-way entry as `part` never clears a different failing entry on the same send. A test holds this case.

| Check | Expected | Fails when |
|---|---|---|
| exact restatements removed | the three restating kinds, over the `cannot tell` range above; every entry printed | the range rule says fails |
| named ways of ruling out kept | listed in 2 of A3's 3 sends wherever A2 lists one in 2 of 3 | fewer |
| parts kept | every entry settled `part` in 2 of A2's 3 sends of a topic (the cap, the repricing, H200's permission) listed in 2 of A3's 3 | fewer |
| motivating H against the control | at most the control's plus 2 (exploratory), counting unresolved points both ways, on the reading after adjudication | above it, in either counting |

**Diagnostic, reported and not scored: a grouped outcome.**
- **When it is exercised:** a send whose Ruled out names two or more cases joined by "or", or two parties, where the topic names one
  case as a part.
- **What is reported:** whether A3 keeps that case, with the readers' marks.
- **Fewer than 2 exercised sends:** the distinction is reported as untested, and no lead claims it.
- **Where the readers mark a kept case `already_judged`:** that is reported as a disagreement with this reading of D409, with both
  scores shown. It is not a bias.

**Every other mark:**
- Reported per group, in both countings, for A3 against the control and A3 against A2.
- Each failure above the control is read and put in a class:
  - **consistent with the sentence:** the entry the sentence removes or keeps (A3 against A2). This counts against A3; it is not proof
    of cause;
  - **present in A2:** the same fault in the A2 arm's sends of the topic. Both arms' sends are shown. This is not proof that A2's
    definition caused it, or that A3 left its frequency unchanged;
  - **pre-existing:** the same fault in the control's sends of the topic. This is not proof that the change left it unaffected;
  - **uncertain:** anything else.
- **Outcomes:**
  - any failure consistent with the sentence is negative;
  - all rules met with no uncertain failure is a lead;
  - all rules met with uncertain failures is "lead, uncertain harms", which goes back to the council before any next step.

**The disputed comparison with the reference:** each comparison A3 adds or removes against A2 and against the control is printed
beside the decision with the readers' marks.

## Built and checked ($0; council round 90: "Go for the $0 build and checks")

- **Arm files** (`make_arm3.py` → `arm-a3/`):
  - the system and schema are byte-identical to A2's;
  - the closing check grows from 1,326 to 1,724 characters, the one sentence (+398 with its space);
  - the frozen files are read, never written.
- **`probe.py --arm a3 check`** (`check-output-a3.txt`), three arms (control, A2, A3) on the 28 topics:
  - every control equals its stored first request;
  - the A2 arm equals the control plus A2's replacements, and A3 equals the control plus A3's;
  - 18 stored written answers are accepted;
  - a synthetic answer is accepted, and a mutant is refused;
  - 252 sends; each arm is held to $0.25 by reservation.
  - Re-run, A2's own check output is unchanged.
- **Synthetic answers following A3** (`synthetic-a3-output.txt`): a restated delay removed (two acquisition answers) and a mixed entry
  reduced to its named way (the approval). The step's code checks accept all three.
- **The readings:**
  - `a3_reading.py` builds the classer's packet from the first readers' packets (the topic, the choices as shown, the entry, the
    matters; no arm).
  - A dry run on a scratch copy of A2's stored reading gave 48 entries in one packet (`classer-packet-dry-run.txt`). Its first entry
    shows Ruled out with "or any other decision against the event of rung 1".
  - The named-way packet is built from the classer's answers. The briefs are `a3-class-brief.md` and `a3-named-way-brief.md`, and
    `run_readers.py` runs both kinds.
- **The scorer** (`probe_score_a3.py`):
  - Reading A is `probe_score`'s settling, unchanged; its loading was moved into `load_reading()`, and A2's score output is
    byte-identical after the move.
  - Reading B and the checks are implemented as written above.
- **Round 91's three corrections, built:**
  - The final result is "diagnostic lead" only when Reading B leads in both countings and Reading A, wherever it is not a lead, is
    negative only through motivating H. Reading A inconclusive, or negative through another check, gives inconclusive.
  - The named-way check now counts each named way by the classer's matter. A3 listing a different named way does not keep the one A2
    listed.
  - The trace review is part of the decision. The scorer lists every (group, mark) where A3 fails more sends than the control, with
    A3's sends, under both readings and countings. A lead stays PROVISIONAL until `reading/a3/trace-review.json` classes each listed
    send as one of: consistent with the sentence, present in A2, pre-existing, uncertain.
    - Any failure consistent with the sentence makes the result negative.
    - Any uncertain failure makes it "lead, uncertain harms".
    - A review that misses a listed send, or uses another class, is refused.
- **Round 92's two distinctions, built:**
  - **A named way outside the matter list** (the classer's `other`) has no identity to match it by. When A2 lists one in 2 of 3 sends
    of a topic, the named-way check for that topic is unresolved, and the result is inconclusive unless another check fails. Two
    different such named ways are never counted as one.
  - **A diagnostic lead** also needs Reading B not to raise the control's motivating H count in any counting where Reading A is
    negative. The two readings settle only named-way entries differently, so Reading B can then pass only by clearing A3's named-way
    marks.
- **Tests:**
  - `test_probe_score_a3.py` has 22 (18 below, plus a different named way on one topic, the trace review, two unmatched named ways,
    and a Reading B that raises the control), covering Reading B's four required cases, the removal range (six cases), named ways kept, parts
    kept, the H bar at 2 and 3, an unexercised removal check, the outcome mapping, a mismatched A2 arm refused by the check, and the
    whole three-arm pipeline through a fake transport.
  - The 27 earlier probe tests still pass.
- **Mutants** (`a3-mutants.txt`): all 18 are caught, each by its own test. Unmutated, all 22 pass. The 27 earlier tests pass.
- **Preflight** (`preflight-output-a3.txt`): as for A and A2, the ladder archive holds no extraction rows, so sections A and B judge
  none. The ladder's answers are replayed by `probe.py check` instead.
- **Cost:** about $0.23 (A2's two arms cost $0.15). The spend so far is about $26.33 of D439's $40.
