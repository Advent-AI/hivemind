# Council round 54: review the v13s implementation and its $0 rehearsal before the blind test

You are an independent read-only reviewer. **Scope (Alex, D737; build rule D738):** report a finding only when it does one of these:
- (a) lets one of the five defects through **where the calculation's own structure decides it** (D738). An indirect form (a multiplier
  of one, a relabelled basis, an estimate's judgement) is recorded for readers, not refused, and is not a finding;
- (b) breaks structure;
- (c) refuses a right answer;
- (d) makes code differ from the rule the request states;
- (e) makes the blind test unable to decide.

All the files are in `docs/research/2026-11-22-number-answers/`.

**What was built (D738):**
- `calc_small.py`: the checks S1–S8, `from_answer` and `publish_decision`;
- `render_v13.py`: `v13s_schema` and `v13s_header`; v13's request bytes are unchanged;
- `judging-v13s.txt`: the system text, with one sentence changed;
- `paid_gate.py`: format selection through `item`, `build_plan('v13s')`, `Gate.attempt`, `summarise`/`merge`, `card_lines`/`card_view`.

**Its checks:**
- `small_cases.py` (`small-cases.log`: 80 of 80 cases);
- `small_mutants.py` (`small-mutants.log`: 28 mutants caught, control passes);
- `small_rehearsal.py` (`small-rehearsal.log`: 13 of 13, including the old run's `results.json` reproduced byte for byte);
- the old harness unchanged: `paid_rehearsal.py` 63 of 63 and `gate.py` 87 of 87.

**The design it implements:** `SMALL-DESIGN.md` §2 [52], §3 [52], and the D738 entry in `docs/DECISIONS-log.md`.

You may build the v13s plan in memory to read the exact request:

```python
import sys; sys.path[:0] = ['docs/research/2026-11-22-number-answers', 'src']
import paid_gate as pg
p = pg.build_plan('v13s')
```

## Questions

1. **Code against the stated rules (d).** For each of S1–S8, does `calc_small.py` enforce exactly what the request's sentences say?
   Read the schema descriptions and the header. Name every gap, with the code line and the sentence.
2. **Right answers refused (c).** Using the gate's twelve requests (`pg.build_plan('v13s')`) and the stored first answers in
   `poc/data/judging-v13-paid-gate-2026-11-22/answers.jsonl`, find right calculations an analyst would write that the code refuses.
   Encode each in v13s and run it through `model.check_schema`, `calc_small.from_answer` and `calc_small.check` in memory. Look in
   particular at:
   - S1's parser and qualifier window on real quotes;
   - S8's period algebra;
   - S4 on the separate arm after `merge`.
3. **Structure (b) and decidable defects (a).** Crashes, unhandled shapes, or a decidable defect the cases miss.
4. **The cases and mutants.** Is any registered case wrong, any assertion too weak, or any mutant caught for the wrong reason?
5. **Readiness (e).** Can the blind test (`SMALL-DESIGN.md` §5 with its [52] reader changes) start on this code? Answer "ready" or
   list the blocking items.

Report findings ranked by severity, tagged (a)–(e), with file and line. Out of scope: the frozen ruler, `poc-v118`, D725's lines,
D731's harness rules.
