# Challenge 2: the reference control's result (`reflection-6/reference-control/RESULT.md`)

**Result:**
- the reading is valid: both families caught both planted-wrong controls, and both sound controls are clean;
- agreed hard-line faults per item, of 26: frozen step 3, Codex-writer references 8, Claude-writer references 0;
- unresolved counted against: 8, 13 and 4.
- **By the rule written before, the control closes:** no confirmed reader error, and result 2 (both references better on at least 4
  topics) is met on 1 topic only.

**1. Independently review my classification of the 8 agreed reference faults** as answer errors, not reader errors.
- The items are in `poc/data/clean-reference-control-2026-11-16/` (`send-1/outcomes.jsonl`, `cases.json`, `readers/`,
  `readers-answers/`).
- The arm names are in `/Users/lchingen/.hivemind-keys/reference-control/key.json`, which you may read for this review.
- The 8: `ref-codex|week-10-06:c1/clean-{1,3,6,8,9,13}` (L), `ref-codex|week-10-06:c1/clean-7` (R),
  `ref-codex|fortnight:c1/clean-13` (N).
- Read each against its topic, its article and `clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md`.

**2. My proposal.** The control's lesson: the readers' agreed faults are real, and a careful writer reached 0 where the frozen step
had 3.

- **The largest lever** the council-loop skill lists that this points at is the writer's care, meaning **reasoning effort**. The
  frozen step runs `gpt-6-luna` at medium effort (`stage_a.SETTING`).
- **The arm:** a new version of the answer-choice step identical to the frozen one except `reasoning_effort='high'`, opened under D439.
  It has the same model and provider (no switch), and the same request bytes except the effort setting.
- **The probe:**
  - the same 26 topics outside the 44, 3 draws;
  - estimated about $0.10–0.30 at the stored per-call cost, times 2 to 3 for high effort, against about $9.7 left of D439's $40;
  - read blind by both families, mixed with the frozen step's stored pass-1 answers and the same four controls.
- **Moves the decision:** the high-effort arm's agreed hard-line faults are at most 1 per draw on 26, against the frozen step's 3,
  in at least 2 of 3 draws, with no new fault class. Then it becomes the candidate for gate 1, measured once on the 44 under its own
  later decision (D426).
- **Closes it:** no fewer agreed faults than the frozen step in 2 of 3 draws.

**Asked:**
1. Confirm or correct the 8 classifications.
2. Challenge the effort arm: is it the right one lever, or do the faults (L parts unlisted, Q) point to another one? What is wrong
   with the probe, and what must change before its $0 preparation?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
