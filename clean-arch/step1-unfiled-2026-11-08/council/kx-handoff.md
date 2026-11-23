You are an independent reviewer, read-only. Do not run model calls, start runs, or write files. You have not seen this work
before. Cite files and lines.

**Context.** Repository `/Users/lchingen/hivemind`, branch `clean-arch`; rules in `AGENTS.md` (§4, §5, §7.1 "Measure the stick",
§7.2). Stage B (the production's frozen judge over the clean path's own questions) has run: three draws complete, 236
judgements, $0.42 (`poc/data/clean-stage-b-2026-11-11/`; read-only, the run is over). No reader has read any verdict yet. The
reading's lines are Alex's (D428, D430 in `docs/DECISIONS-log.md`); the baseline it compares with was read the same way
(`clean-arch/step4-2026-11-10/stage_b/BASELINE.md`, `RESULT.md`, `baseline_count.py`). Stage A has not passed.

Two earlier reviews said **Not ready**: `clean-arch/step1-unfiled-2026-11-08/council/kv-codex.md` and `kw-codex.md` (both
readable at those paths). The second asked for: the trial's result enforced (no duplicate rows, complete rows, packets rebuilt,
all three tests covered, the count refusing an in-use file that is not the trial's result); the control readers to search every
judge request through 2026-07-14, not only the last; complete reader rows and a written reason on every third ruling; and the
planted answers rewritten where they were identifiable (a shared generic sentence) or open to a good-faith other verdict.

**What to review now:**
- the plan: `clean-arch/step4-2026-11-10/stage_b/STAGE_B_READING.md`;
- the tools: `stage_b/build_stage_b.py` (`PLANTED`, the trial and reading packets), `stage_b/stage_b_trial.py` (new),
  `stage_b/stage_b_count.py`, `stage_b/control_theses.py`, `stage_b/control-reader-brief.md`, `stage_b/check_stage_b_count.py`,
  `stage_b/count_mutants.py` and `count_mutants.output.txt`, `stage_b/run_codex_readers.py` (the `trial` and `controls` kinds);
  reused: `stage_b/build_baseline.py`, `stage_b/baseline_count.py`, `stage_b/stored_judgements.py`; the judgement form
  `ladder/stage-b-reader-brief.md` (unchanged);
- the built packets: `poc/data/clean-stage-b-reading-2026-11-12/validation/packet-1.json`, `packet-2.json` (the trial),
  `controls/control-packet-1..4.json`. The keys and control facts are outside the repository in
  `/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/.held/`
  (`stage-b-trial-key.json`, `stage-b-control-facts.json`).

**Questions.**
1. Is each finding of `kw-codex.md` (and any of `kv-codex.md` it left open) closed? Name any that is not, with the line.
2. The six planted answers, read against their requests in the trial packets: is each unambiguously wrong under the test it is
   filed under, with the stored rung the rung the rules lead to? Could a careful reader in good faith call any SUPPORTED or
   INSUFFICIENT, or name another rung? Can any be spotted by form without judging it?
3. Any case the count, the trial or the control count accepts that it should refuse, or refuses that it should accept?
4. Anything else that would make the reading misleading even if every step runs as written?

End with one line: **Ready** (the trial may start, then the reading), or **Not ready**, with the changes needed, most serious first.
Findings about wording only are listed as such and do not make it Not ready.
