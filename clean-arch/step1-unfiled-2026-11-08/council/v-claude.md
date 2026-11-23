# Reflection council v: Claude's own reflection, written before reading Codex's (2026-11-08)

## Status
- **Step 1.** The configuration is K6b on DeepSeek Flash, high effort; Alex confirmed it.
  - Dev passed the line: 205/234 helpful over 115 gold articles, forward from empty.
  - The test set missed by 3: 32/42 against a proportional line of 35, one draw, exposed. Noise was twice production's (8 against 4).
    7 of the 10 misses were extracted but left unfiled and dropped (takeover LOG §16).
- **The unfiled round** (LOG §§0–17, about $5.6):
  - The D371 wording moved nothing measurable. The reader families disagreed, 15 against 6.
  - Alex ruled four boundary cases and reframed: a thesis is a view with a reason, and a useful company figure no view takes is kept as
    a condition ("好").
  - The conditions design passed eight review rounds. They found a latent Step 2 defect: a 600-character passage cut affecting 16% of
    items, not yet fixed in code.
  - The runner keeps a valid condition with empty links (3 tests, 4 mutants).
  - **Probe 4 (c1) was mixed** (LOG §20). Wins: theses that only restate a figure fell from 4 to 0, and EPS was kept 6/6. Losses:
    margin under the revenue view fell from 5/6 to 1/6; cash was kept against Alex's ruling; 7 extra theses; gold not-kept rose from
    13 to 23. Stopped (D355).
- **Step 2.** Lines 1 and 3 met; line 2 missed by one merge (3/104 wrong, 2.9% against 2%), one Jev draw. Not done: the line-2 fix,
  and the conditions design's Step 2 changes (full passages, a no-thesis search, backfill).
- Nothing is committed.

## Lessons at mechanism level
1. **Structural outlets move the model a lot; wording does not.**
   - The "unfiled" outlet in K6b and the "condition" outlet in c1 each changed behaviour strongly.
   - Sentence-level D371 wording (u1) moved nothing, and its length-neutral cuts did.
   - A structural lever must therefore pass the prompt audit before the send. I skipped it for c1, and all three regressions are
     clauses an audit flags.
2. **Alex's rulings are concrete cases, and they are the only ruler for the new record.** The frozen gold marks most figures optional
   (neutral), so it cannot see conditions. c1 was written from the design's abstractions ("only the reason it informs") rather than
   checked against the four rulings sentence by sentence. **Lesson:** walk each ruling through the changed request at $0 before any
   send.
3. **Broad linking was already right.** K6b's "link to every thesis it informs" put the margin under the revenue view 5/6, as Alex
   wants. Narrowing it to "the reason it informs" sounded principled and broke his ruling.
4. **My own trace reading had an instrument defect.** The printer truncated summaries to 120 characters, so I missed the margin inside
   combined items and called the control 0/6; Codex caught it. Read an anchor by searching passages and summaries for the figure, not
   by eye on truncated lines.
5. **The design gate and the prompt audit are different gates.** Eight design rounds reviewed the record shape and the downstream
   isolation. None read the c1 request against the rulings.
6. **Possible cross-step link (hypothesis):** 15 of Step 2's overlaps and 2 of its 3 wrong merges come from bundled Step 1 records,
   and c1 split figures into single items. More atomic items might help Step 2's line 2. Untested.

## Conclusions weaker than they look
- The dev pass is one draw on articles the prompts were tuned on; the test missed.
- Probe 4's "4 → 0" rests on two empty-state cases. The 4 sit in two control draws of one case.
- Step 2 line 1 (99.1%) is recall over labelled counterparts, not over all repeats. Line 3 is one Jev draw.
- "c1's own sentences caused it" is supported for cash and margin (the accounts quote the sentences). For networking and supply it is
  not established.

## Remaining problems by product impact
1. **Step 1 recall in thin libraries:** 7 of the test's 10 misses were unfiled. Conditions plus backfill target this directly; a quarter's revenue, a cash-return plan and a cash-flow forecast are figures.
2. Step 1 noise, twice production's on the test.
3. Step 2 wrong merges: bundles and one Jev figure error.
4. Small suppliers opening theses: 3/3 in both arms.
5. Out of scope (Alex: stop at Steps 1–2): whether conditions help Step 4 at all.

## Next angle, with its falsifier
**c2: K6b plus the conditions outlet, minimal.**
- **Unchanged:** K6b's linking and big-matter wording.
- **Added:**
  - the `condition` field;
  - one CONDITION bullet: a useful company figure is judged in context, with Alex's cash case as the boundary (a backward cash or
    balance figure that no question turns on is not kept; forward plans and estimates are, per D371);
  - the do-not-open row "a measure's level, growth or guidance with no reason (it is a condition)", which is Alex's reframe;
  - none of c1's "a measure with a reason is a view" or "big matters include a reason".
- **Before any send:** the prompt audit with a blind second reader, and each of the four rulings walked through at $0.
- **Then:** the motivating cases one draw each (a few cents), then 16 × 3 against the same control.
- **Falsified if any of these holds:**
  - margin under the revenue view below 4/6;
  - cash dropped below 2/3;
  - more than 1 extra thesis;
  - gold not-kept above the control + 3;
  - any figure-only thesis in empty-40 or empty-57;
  - EPS kept below 5/6.
- **If the minimal arm keeps figure-only theses in empty states,** the view-definition lever is needed, and it is isolated as its own
  arm.
