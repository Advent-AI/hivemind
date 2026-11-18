# Why the fresh topics miss line 5 (D604's trace), 2026-11-16, $0

`line5_trace.py` → `line5-trace-output.txt`. It reads the stored fresh reading (`poc/data/clean-fresh-a2-2026-11-16/choices/reading`)
with the gate-1 scorer's own functions, for the control arm (the frozen step). It reproduces the recorded line 5: 2 of 5 right with
unresolved points counted for the answer, 1 of 5 with them counted against.

## Topic by topic

| Topic (kind) | What blocks it, counted for / against | How settled | Reaches what a reader of the product sees? | Existing record |
|---|---|---|---|---|
| clean-14 (theme figure) | XR / XR | Passes 1 and 3: both third readers fail XR (the reference: IDC's "19% growth" forecast for a unit count). Pass 2 split. | **Not in these cases** (corrected in round 146, see below). | Event reference has no bounded repair (D557, D558); "what counts as an expectation" is an open form issue. |
| clean-15 (theme figure) | L, XR / L, XR | L: pass 1 both first readers; pass 2 both third readers; pass 3 split. XR: pass 1 both first readers. | **Yes, for L:** a part the question leaves out, now shown in the card's list of parts not judged. XR: the same visible choice either way (below). | Line 2's class; no sourced main-part rule (D580); tuning stopped (D586, D391). |
| clean-16 (AI bill) | none / none: three justified refusals | Both families: N holds. | Right. | |
| clean-17 (event) | R, XR / R, XR | R: pass 3 both third readers (the wait-as-ruling-out class); pass 1 split. XR: all three passes, both first readers. | **Yes, for R:** the Ruled-out rung's words. XR: no (the judge never sees an event's reference, D557). | The postponement boundary, on Alex's page (D591). |
| clean-18 (company figure) | none / D | D split on all three passes (Codex fails, Claude holds). | **Yes,** the due day is shown, and it is code's D414 day, 60 days after year-end. Readers who fail it read the request's fiscal-year note ("around 2027-02; use that day"), which contradicts code. | The reader discrepancy (D590): read alone, both families hold D on the class. The request-and-code contradiction (`universe.py:136` against D414) is recorded and not changed. |

## What this gives

- **On fresh topics, line 5's misses reduce to four recorded things:**
  - reference choices (XR, on 3 of 4 written topics, and the only blocker of clean-14). In these cases a rule-following answer would
    produce the same answer choices; see the section below;
  - a stopped class (L);
  - an unresolved policy boundary (R, Alex's);
  - a reader discrepancy on Alex's own rule (D).
- **No common, sourced product mechanism is found.** By D604's rule this closes the route to a candidate. The gate stays unmet; a
  later candidate is not excluded.
- **A diagnostic recount of the stored marks, not a gate result and not a change of any line.** Without XR, line 5 on the fresh
  topics would read 3 of 5 (unresolved for) or 2 of 5 (against). The development map's 9 or 7 of 13 (`gate1-stick/RESULT.md`) was
  counted without both L and XR, not without XR alone.
- **Limits:** one week, one draw, 5 topics, control arm only.

## Corrected in round 146, and the source-backed reading (D604's unfinished part)

**My error.** I wrote that no product reader sees the ladder's reference. That is wrong for figures. `ladder_step.write_view` puts the
reference into the middle answer choice's words, which the judge is shown and the page carries:
- with a stated number, "(the reference when the question opened: "…")";
- with a last reported amount, "(the amount last reported …)";
- otherwise "(no reference figure when the question opened)".

An event's reference is used by no rung. I had relied on an older finding and a search for the word in `bundle.py`, without following
the writer.

**Each XR failure, read beside its article.** The articles are in `cases/cases.json`; the readers' reasons are in
`choices/reading/third-reader` and `readers-answers`.

| Topic, passes | What the article states | The answer's reference | Readers | What the judge and page see |
|---|---|---|---|---|
| clean-14, all three | "China's broader AI accelerator market reached about 2.008 million units in the first half … IDC expects total accelerator shipments to grow 19% in 2026". No full-year 2025 count, so no expected count is stated. | null | Claude: the 19% is an expectation for this very quantity, so it should be quoted (kind `expected`, no number). Codex: a growth rate, not a count, so null holds in packet 1 and fails in packet 2. | **The same either way.** With no number in the figure's unit, a quoted words-only reference gives the same middle choice as null: "(no reference figure when the question opened)". |
| clean-15, pass 1 | Microsoft: "Starting next calendar year, we will scale our Maia family to multi-gigawatt deployments". | null | Both first readers fail, so it was settled without a third reader. On passes 2 and 3, and on the A2 arm, both families' third readers rule that a null reference is right, because it is one company's plan, not an expectation for the combined capacity. | The same either way, since no number. The fail is a reading inconsistency across passes. |
| clean-17, all three (event) | "Taiwan will tighten export controls on high-end AI processors and servers, mirroring U.S. rules". | null | Both first readers fail: an expected event belongs in the reference. | **Nothing:** an event's reference is used by no rung. |

**What it gives:**

- **Every XR failure on these topics leaves what the judge and the page are shown unchanged.** An answer that followed the rule
  exactly would produce the same answer choices: a words-only reference for clean-14 and clean-17, or null for clean-15.
  - The rule allows "no number the article does not state".
  - None of these articles states a number in the figure's unit.
  - An event's reference never reaches a rung.
- **The disputes are about the rule's reach:** whether a growth rate counts as an expectation for a unit count, and whether one
  company's plan does for a combined figure. "What counts as an expectation" is the open form issue already recorded.
- **The narrower claim (round 147):** this checks the writer's behaviour on the stored answers; it is not a test that a new model
  request would leave every other field unchanged.
- **Under D604 and round 146's criterion this closes the route.** It found disputed reference choices with no product consequence and
  no sourced general mechanism. The gate stays unmet; no paid work follows without a new candidate.
- **Observation, outside the line marks:**
  - A Claude first reader's G remark on clean-14: the middle range (3.5 to 4.0 million) sits below the first half's annual rate
    (about 4.0 million) and below what IDC's growth implies.
  - G is not one of the line marks.
  - The ranges are product-visible, but one reader of one family on one topic is a lead, not a class.
