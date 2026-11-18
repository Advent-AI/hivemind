You are an independent reviewer, read-only. Do not run model calls, start runs, or write files. You have not seen this work
before. Cite files and lines.

**Context.** Repository `/Users/lchingen/hivemind`, branch `clean-arch`; rules in `AGENTS.md` (§4, §5, §7.1 "Measure the stick",
§7.2). Stage B (the production's frozen judge over the clean path's own questions) has run: three draws complete, 236
judgements, $0.42 (`poc/data/clean-stage-b-2026-11-11/run.json` and the draws' folders; read-only, the run is over). No reader has
read any verdict yet. The reading's lines are Alex's (D428, D430 in `docs/DECISIONS-log.md`); the baseline it compares with was
read the same way (`clean-arch/step4-2026-11-10/stage_b/BASELINE.md`, `RESULT.md`, `baseline_count.py`). Stage A has not passed.

A previous review said **Not ready** (`council/kv-codex.md`). Its findings were: the planted answers were identifiable (two-rung
events, questions no Stage B judgement has); the control count accepted incomplete or invalid rows and rulings, trusted its facts,
marked material as one answer instead of item by item, skipped a missing decisive item silently, and did not report the literal
reading's result or the days of the compared answers; the facts file sat beside the control readers' packets; the count did not
refuse a zero denominator; the count dropped the baseline's reports of repeats and of the stored rung named on planted answers;
the control brief described reader B favourably.

**What to review now:**
- the plan: `clean-arch/step4-2026-11-10/stage_b/STAGE_B_READING.md`;
- the tools: `stage_b/build_stage_b.py` (new planted answers in `PLANTED`, the trial packets, the reading packets),
  `stage_b/stage_b_count.py`, `stage_b/control_theses.py`, `stage_b/control-reader-brief.md`, `stage_b/check_stage_b_count.py`,
  `stage_b/count_mutants.py` and `count_mutants.output.txt`; reused: `stage_b/build_baseline.py`, `stage_b/baseline_count.py`,
  `stage_b/plant_trial.py`, `stage_b/stored_judgements.py`; the judgement form `ladder/stage-b-reader-brief.md` (unchanged);
- the built packets: `poc/data/clean-stage-b-reading-2026-11-12/validation/packet-1.json` and `packet-2.json` (the trial: six
  planted answers among six stored judgements), `controls/control-packet-1..4.json`. The keys and the control facts are outside
  the repository, in `/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/.held/`
  (`stage-b-trial-key.json`, `stage-b-control-facts.json`). The reading packets are built only after the trial.

**Questions.**
1. Is each finding of `kv-codex.md` closed? Name any that is not, with the line.
2. The six new planted answers: is each unambiguously wrong under the form's test it is filed under, with the stored rung the
   rung the rules lead to (read each against its request in the trial packets)? Could a careful reader call any of them
   SUPPORTED or INSUFFICIENT in good faith? Does any still differ in form from a real judge answer in a way a reader could spot
   without judging it (wording, length, fields, the request's previous-conclusion block)?
3. The count and the control count: any case still accepted that should be refused, or refused that should be accepted? Is
   each line computed as D428 and D430 say? Is excluding the Ohio question from line 3 what the design §8 says
   (`clean-arch/step4-2026-11-10/DESIGN.md`, "Control with a known answer")?
4. Anything else that would make the reading misleading even if every step runs as written?

End with one line: **Ready** (the trial may start, then the reading), or **Not ready**, with the changes needed, most serious first.
