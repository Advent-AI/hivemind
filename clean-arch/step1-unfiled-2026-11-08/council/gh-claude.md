# Council gh: Claude's own reflection on the handoff of 2026-11-10 (written before reading any other member)

Read first: AGENTS.md, `docs/CURRENT_STATE.md`, `clean-arch/HANDOFF-2026-11-10.md`, the round log §§47–68, D38, D186, D368, D391–D396,
`docs/prd/11-production-experiments-from-split.md` (E3, E4), the Step 4 design, `gg-codex.md`, and the code the design leans on
(`role-v74i.txt`, `extraction.py`, `views/writing.py`, `views/judging.py`, `views/store.py`, `e2e-2026-11-09/adapter.py`).
Counted at $0: the 34 theses of the three unseeded draws, joined to the model's stored answers in each trace.

## 1. Lessons at mechanism level (§§47–68)

1. **One call doing several jobs moves cases it did not target.** c9, c10a, c10b and c11 each moved 4–5 untargeted cases while c8
   matched itself on 31 of 32 (§53). A separate call that left c8's bytes alone reached its target 36 of 36 (§58). What stopped it was
   not the structure: each round met a boundary the standard does not define (how big is big, when a programme is undertaken), and
   every fix was tuned on the same 32 cases.
2. **The model holds knowledge it does not apply unprompted.** Capex from two cash-flow figures: 3 of 3 when pointed at them, 0 of 3
   from a general instruction, in wording (c12) and in placement (c13) (§§64–65). A general sentence does not buy a recall step.
3. **With the question present, delivery decides the answer.** q10 and q16 account for the whole +5 of Stage 2, and delivery matched
   outcome in all six draws (§63). The frozen judge reasons onward once it holds the facts.
4. **From an empty library the gap is the question's shape.** All nine subset misses are a question not opened as the ruler asks it
   (§67). The judge agreed 16 of 16, but on the ruler's wording, ladder and deadline.
5. **The frozen judge stops runs.** A theme shown under D191 is written into `cites_views`; two refusals stop a draw (§62; E4 counts
   18 of 25 refusal errors as this class).
6. **Process.** A fix found by reading a probe is a new arm; reviews check a rule's text, not how the model applies it; a set that
   tuned six arms cannot accept a seventh.

## 2. Conclusions weaker than they are stated

- "Once a question is opened, the evidence is enough to judge it right" (the question put to Alex for D396). The 16 answers cover
  seven distinct questions, ten of them yes/no, each on the ruler's own ladder and deadline. Nothing yet shows an answer on a ladder
  the system wrote.
- Stage 2's +5 is two questions. The threshold is exploratory and c8 was tuned on 115 of the 243 items.
- The design's "about $1" assumed the mapped-ruler judging counts. With the system's own themes in the store, a changed theme queues
  every open asset thesis (`judging.queued_by_change`), so the count of judgements is not the count of views with a new link.

## 3. What the Step 4 design missed (each checked in the files)

1. **Prior art it does not quote (AGENTS §2, "Prior decisions").**
   - The split experiment already ran a separate call that wrote new questions with their ladders, and was sealed as failed (D378).
     Its record for ladders (PRD 11, E3): whether a new question got a ladder at all was "a coin flip on the same request (21 of 44)";
     ladders came out inverted; a "within 5%" band missed its own bounds; a rung held no value; "a reworded reference sentence lost two
     control ladders. Checks, not wording, are the part to port."
   - D186 with D368 item 1: Alex decided that asset rungs state the outcome against guidance, each thesis naming its favourable end,
     "built in the next extraction version" ("这个你记住，我们要做"). A new call that writes ladders with v74i's bullish-to-bearish
     sentences builds the thing D186 replaces. Whether the new call is that "next version" is his to say.
   - E4: the refusal class of lesson 5 is recorded with a proposed judging version only Alex opens.
2. **D38's "a view looks at one thing".** "A question that needs a number and an event is two views … a question whose parts can
   move in opposite directions is two views." 13 of the 34 stored theses are compound by wording ("Will NVIDIA sign … — and at what
   amount", "conclude its investigation … and will it impose remedies or fines", "How far will the crackdown escalate — will …"). A
   ladder call must pick one thing, split, or refuse. Picking changes the question the system opened; the design says nothing.
3. **The inputs the design names are not where it says.** The library state of a thesis holds only description, entity, id, outcome
   and period. `opens_as` and `settled_by` exist only in the Step 1 answer stored in the trace (`trace.result`), keyed by a local id.
4. **Periods are prose.** 29 of 34 periods carry no ISO date ("NVIDIA's next annual report (FY2027 Form 10-K), expected early 2027";
   "12 months from the item (by ~mid-2027)"); 5 carry one; none is null. The due day must be derived, and a check must refuse a due day
   on or before the opening article's day.
5. **Theme against asset decides more than labels.** `judging.themes_in_force` keys on the view's `object_kind`. The seeds carry seven
   theme views under theme objects such as `chip-export-controls`. The clean path has no theme object: 21 of the 34 theses opened as
   `shared_quantity` (13) or `policy_stage` (8). Stored as themes they bring the theme block, the re-queue rule and the refusal class
   of lesson 5; stored under the company they do not. That is a choice about what the system does (D191, D195).
6. **Dependencies.** A clean thesis has none, and production's default path gives an article-opened thesis none either (CURRENT_STATE,
   open defect 4; D368 item 2, to be built). With none stored, any id in `cites_views` is refused.
7. **Thresholds need a reference.** v74i asks for "the neutral comparison in its condition" and "no ladder whose thresholds depend on
   an unspecified future target". An opening article often states no consensus or guidance (HBM capacity, the CPU-to-GPU ratio). A
   five-rung ladder is then a set of invented bands, and an answer on it can be well supported and still say nothing.

## 4. Remaining problems by product impact

1. **No answer exists for any question the system opens itself.** 0 of 34. AGENTS §5: the product runs end to end before anything
   else is built. Everything measured so far borrowed the ruler's ladders.
2. **Opening shape:** the second year of an annual quantity (3 of 9 misses), the memory question (3), Ohio (2), one check date (1).
   Tuning on these cases is ruled out (council gf).
3. **The frozen judge's stop on a theme cited as a dependency** (E4). It will meet the clean system's own themes.
4. q12 (D394); link clutter; unverified passages; one company, fourteen days.

## 5. My position

**Step 4 is the right next step, and the first thing to build inside it is the ladder step alone.**
- The judge is frozen and measured. The only new and unmeasured part is the ladder. The split's record says the ladder is where a
  separate call failed before.
- So the order is: (a) the ladder call with its checks and writer mapping; (b) the frozen judge over the system's own laddered views
  through the adapter; (c) the reader test on the judgements. Stage (b) runs only when (a) meets its frozen line.

**The first test, in two stages, on the three stored unseeded draws.**
- **Stage A, ladders (34 calls, cents).** Denominator: all 34 opened theses. Each ends in one of: refused by code (count, reason);
  written and judged sound by two blind readers against the thesis and its opening article; written and unsound, by class (not the
  thesis's question; not one thing; not a partition; due day unsupported; neutral rung with no stated reference; inverted direction).
- **Stage B, judgements.** Denominator: every judgement of every laddered thesis over the window, not only the last. Each is
  SUPPORTED, UNSUPPORTED or INSUFFICIENT EVIDENCE against all evidence linked by that day, with arithmetic and the D260 fields checked
  apart. Refused judgements, unjudged theses and stopped draws are counted.
- **A known-answer control inside the test.** 16 of the 34 theses were matched SAME to a ruler question by the frozen MATCHING-v2
  reading (`mapping-runs.json`), and their ruler-ladder answers agreed with the gold 16 of 16. On those 16 the answer on the system's
  own ladder can be read against reader B's range. A test with this control cannot pass empty, and a ladder that bends its question
  shows up as a disagreement where the ruler ladder agreed.

**For Alex, after the design is clean:** one recommendation (build the ladder step, run Stage A, then B), and these product choices
if the decisions do not settle them:
1. whether this ladder call carries D186 now, or v74i's labels first with D186 as its own later slice (my lean: v74i's labels first;
   the frozen checks and the ruler's ladders use them, and one lever at a time);
2. whether the system's own shared-quantity and policy questions are stored as themes, with D191's block (my lean: yes, as the
   decisions in force say, with the refusal class counted);
3. what happens to a compound thesis (my lean: the ladder call writes the ladder for the one thing the thesis's `outcome` and
   `settled_by` name, says what it left out, and readers judge whether the question survived; no split in this version).

## 6. What would change my mind

- A cold reader showing that a cheaper change than a ladder call gives the system's questions an answer a reader can check.
- Evidence that ladders at opening cannot be anchored for most theses, which would argue for writing the ladder when the first
  reference figure arrives, against D38's "set when the view is created".
- Evidence that the 16 matched theses are too few or too easy (ten yes/no) to serve as the control.
