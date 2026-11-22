# Council Q, round 3: the dependency probe's design, before any send (read-only; no edits, no model calls)

## Alex's word
Asked to choose after council Q (A: no daily wrapper yet, link the related questions first, a $0 check then a few cents; B: build
the daily wrapper and warn testers; C: stop), Alex answered "A" (2026-11-20).

## What I found since round 2 (read these)
- **The dependency stretch already ran (D533–D542).** `docs/research/2026-11-14-use-acceptance/dependency-selection/`:
  - `DEPENDENCY-SELECTION-CENSUS.md` (D537): in the unseeded fresh week the one clear useful pair was "data-center revenue FY2027
    ← total revenue FY2027" (the part reading the whole), useful and source-backed; "total revenue growth FY2028 ← data-center
    revenue FY2027" was a risk ("a dependency would pass an assumed number on"). Readers marked DC/total both ways (a circle risk).
  - D538: one stored edge has two readers: judging (whose conclusion to read) and filing (`narrowest_links`: the reader becomes the
    narrower home; seven statements would lose their total-revenue link).
  - `SEPARATION-DESIGN.md` (D539–D542): `reads` vs `supports` edges; closed as a provisional candidate, **not sound for build**; a
    reopened slice must first settle a cycle through an awaited question, closing, a theme shown twice, historical readers, the label.
  - So round 2's "decided and not built" was incomplete: decided (D368 item 2), worked on, not ready to build. I will tell Alex.
- **Direction.** Your round-2 point read D368 item 4 (seed edges: the root reads its drivers). PRD 06 line 134: for a question opened
  from an article, matching "chooses a new thesis's dependencies, stating which conclusions it relies on"; `reads` edges in
  SEPARATION-DESIGN §2. The census's useful case is the part reading the whole. The probe therefore tests Data Center reading total
  revenue; it does not test the root reading its drivers.
- **$0 check done** (`render_check.py`, `render-check.json`; `check.txt`):
  - The block production renders shows the total's rung and its reasons cut at 600 characters. old-2: $411B reference, $419B,
    Q3 $113.5B, Q4 $127B all shown. old-1: $411B and $404B shown; its reasons never state Q4. old-3: $419B, Q3, Q4 $127B shown, but
    the final "$446 billion" is cut (the rung "Strongly bullish", at least $431.2B, is shown).
  - `probe.py check`: each draw's scratch copy rolled back to before the Data Center question's 09-20 judgement (that row and any
    later one removed) rebuilds the stored request **byte-equal** (sha256) through `judging.build_prompt` and `model.build_request`
    in all three draws; the changed request adds 682–764 characters (the block, and the closing sentence's `cites_views` clause).

## The probe (`probe.py send`)
- Per draw (old-1 v8←v4, old-2 v9←v14, old-3 v35←v3): control = the stored 09-20 request re-sent unchanged; changed = the same
  state plus one dependency row (`first_is_bullish`), rendered by production code with its 600-character cut. Three samples each,
  each in its own empty archive (fresh samples), a refused answer retried once with production's note. 18 sends, about $0.006 each
  (18k input, 7.6k output at luna's $0.10/$0.50), cap $0.40.
- The total's conclusion shown is its same-round 09-20 judgement (production judges dependencies first).

## Reading, written before any answer
For every answer, I and a blind reader (you, given answers under shuffled labels with the total's shown conclusion and the evidence
the request lists) record: the FY2027 Data Center estimate; any Q4 Data Center figure; whether each figure of its arithmetic traces to
evidence or to the dependency; whether it relates its figure to the total.
- **Reconciles:** FY Data Center below the total's shown FY figure; a stated Q4 Data Center below the total's shown Q4 (when shown);
  no unsupported step (a figure with no source in the request).
- **Pass:** changed reconciles in at least 2 of 3 samples in each draw; control reconciles in at most 1 of 3 in at least two draws
  (else the stored contradiction is a coin flip the probe cannot separate: inconclusive); no added refusal; no new unsupported step.
- **What it decides:** pass → the next step is the build design (D542's five open items and the `reads`/`supports` separation),
  back to the council and Alex; fail → linking alone does not reconcile; the cause is the judge's own arithmetic, back to the
  council; inconclusive → report as such.

## Questions
- (a) Is this probe sound? What would make it misleading (the 600-character cut, old-1's missing Q4, the same-round total, the
  reading rule)?
- (b) Is "Data Center reads total" the right first direction given D368 item 4, PRD 06 and D537?
- (c) Anything to change before the send?

End with CONSENSUS or DISAGREE. Under 400 words.
