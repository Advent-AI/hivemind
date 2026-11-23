You are an independent reviewer, read-only. Do not run model calls or start runs. You have not seen this work before; form
your own view from the files, then answer. Be specific: cite files, judgement numbers and sentences.

**Context.** Repository `/Users/lchingen/hivemind`, branch `clean-arch`. Working rules: `AGENTS.md` (read §5, §7.1 "Measure
the stick before using it", §7.3). Step 4 of the clean path is a "ladder step" plus production's frozen judge
(`clean-arch/step4-2026-11-10/DESIGN.md`; read "Where it stands" near the top and §8 from "### Stage B" to the end of the
section). Alex's decision D426 (`docs/DECISIONS-log.md`, search "## D426") opens the *preparation* of Stage B, its $0
baseline reading first. Nothing paid is sent.

**What to review: the baseline reading, before any reader starts.**
- The plan: `clean-arch/step4-2026-11-10/stage_b/BASELINE.md`.
- The form the readers get: `clean-arch/step4-2026-11-10/ladder/stage-b-reader-brief.md`; the third reader's:
  `clean-arch/step4-2026-11-10/ladder/stage-b-third-reader-brief.md`.
- The code: `clean-arch/step4-2026-11-10/stage_b/stored_judgements.py` (what a judgement is given with),
  `build_baseline.py` (chunks, the six planted answers `PLANTED`, the three repeats, placement, the key),
  `baseline_count.py` (the count, written before any row).
- A trial build to inspect (not the readers' copy):
  `/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/baseline-trial/readers/packet-*.json`
  and its key `/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/.held/baseline-trial-key.json`.
- The stored runs: `poc/data/clean-unseeded-2026-11-10/draw-d1|d2|d3/judged/` (finished; open read-only).

**Questions.**
1. **Does the plan do what the design's §8 "Baseline" and its lines 4 and 5 need**, and nothing the design or Alex did not
   ask for? Name anything missing, anything added, and any number in `BASELINE.md` that the code does not produce.
2. **The six planted answers.** For each (open its packet in the trial build and read the request as sent): is it plainly
   UNSUPPORTED by the form's tests, on the request alone? Could a careful reader defensibly call it SUPPORTED or
   INSUFFICIENT? Is the planted text told apart from a stored answer by its form (length, style, a missing field, an
   inconsistency with the request's "previous conclusion") rather than by its substance? Planted 5 and 6 are first
   judgements; planted 3 and 4 claim `changed` true against a previous conclusion in the request: check each for a tell.
3. **`not_shown`** (`stored_judgements.not_shown_of`): is "linked at or before the judgement's sequence number, not replaced
   by then, not listed in the request" the right reading of "evidence in force that the request did not show" against
   production's `store.evidence_in_force` and `judging.evidence_shown_in` (`src/hivemind/views/`)? Check one judgement by
   hand (for example draw d2, view v18, a late judgement).
4. **`baseline_count.py`**: does it compute what `BASELINE.md` says, and are the stop and void conditions the design's? Any
   case it gets wrong (a judgement both families call INSUFFICIENT; a third reader's row missing; the repeats)?
5. **The packets**: up to about 210,000 characters and 7 judgements in one. Is anything in a packet that a reader should not
   see (ids of the run, the stored rung of a planted answer, a hint of which item is a control)? Is one control a packet,
   always of another question, itself a tell?
6. **What would make this reading misleading as a baseline** even if every step runs as written?

End with one line: **Ready** (readers may start), or **Not ready**, with the changes needed, most serious first.
