You are an independent reviewer, read-only. Do not run model calls, start runs, or write files. You have not seen this work
before. Cite files and lines.

**Context.** Repository `/Users/lchingen/hivemind`, branch `clean-arch`; rules in `AGENTS.md` (§1 "When one mechanism draws
findings round after round, stop answering findings: propose one structural rule", §4, §5, §7.1 "Measure the stick", §7.2).
Stage B (the production's frozen judge over the clean path's own questions) has run: three draws complete, 236 judgements
(`poc/data/clean-stage-b-2026-11-11/`; read-only). No reader has read any verdict yet. The reading's lines are Alex's (D428,
D430 in `docs/DECISIONS-log.md`); the baseline it compares with was read the same way
(`clean-arch/step4-2026-11-10/stage_b/BASELINE.md`, `RESULT.md`, `baseline_count.py`). Stage A has not passed.

Three earlier reviews said **Not ready**: `clean-arch/step1-unfiled-2026-11-08/council/kv-codex.md`, `kw-codex.md`,
`kx-codex.md`. Each judged one or two planted answers open to a good-faith other verdict. The plan now answers that with one
rule (`STAGE_B_READING.md`, "The trial decides which planted answers are clear"): the trial, as in the baseline, uses only the
planted answers both reader families call UNSUPPORTED with the stored rung named, and the reading waits until each of the
form's three tests keeps one. The third review also found two versions of one matter could share a packet (the draws word one
matter differently), and an unresolved material dispute was reported as a confirmed miss, and two row-value gaps.

**What to review now:** the plan `clean-arch/step4-2026-11-10/stage_b/STAGE_B_READING.md`; the tools `stage_b/build_stage_b.py`
(`PLANTED`, `TRIAL_PACKETS`, one-draw packets in `stage_b_packets`), `stage_b/stage_b_trial.py`, `stage_b/stage_b_count.py`,
`stage_b/control_theses.py`, `stage_b/control-reader-brief.md`, `stage_b/check_stage_b_count.py`, `stage_b/count_mutants.py`
with `count_mutants.output.txt`, `stage_b/run_codex_readers.py`; reused `stage_b/build_baseline.py`, `stage_b/baseline_count.py`;
the form `ladder/stage-b-reader-brief.md` (unchanged); the trial packets
`poc/data/clean-stage-b-reading-2026-11-12/validation/packet-1.json`, `packet-2.json`; the control packets
`controls/control-packet-1..4.json`. Keys and control facts are outside the repository in
`/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/.held/`.

**Questions.**
1. Is the trial rule sound as the answer to the recurring finding, and is it enforced by the code as written? Is any finding of
   `kx-codex.md` still open?
2. Is each planted error real (the step it takes is one the form's test names), and does any planted answer still give itself
   away by form, or share a packet with another version of its matter?
3. Any case the trial, the count or the control count accepts that it should refuse, or refuses that it should accept?
4. Anything else that would make the reading misleading even if every step runs as written?

End with one line: **Ready** (the trial may start, then the reading), or **Not ready**, with the changes needed, most serious
first. Findings about wording only are listed as such and do not make it Not ready.
