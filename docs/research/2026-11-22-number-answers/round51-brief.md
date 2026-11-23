# Council round 51 (first of the two allowed by round 50): the exact wording and case list of the judging-v13 repair

You are an independent read-only reviewer. Round 50 (`codex-r50.md`) set a finish line:
- this round reviews the exact wording and corrected examples;
- one more round reviews the request the harness actually sends and the checks it runs;
- then the blind test runs once;
- a serious issue left after the second round goes back to Alex.

The design to review is `docs/research/2026-11-22-number-answers/REPAIR-DESIGN.md` (v2). It answers round 49 (`codex-r49.md`). Read
it against `calc_check.py`, `render_v13.py`, `paid_gate.py`, `gate.py`, `paid_rehearsal.py`, the request as sent (`paid-plan.json`)
and the stored answers in `poc/data/judging-v13-paid-gate-2026-11-22/`.

## Questions

1. **Coverage.** For every refusal template in `calc_check.py` (and the new ones in §3), name the sentence of §2 (or the enum or
   marker) that states it. List any refusal whose condition is still unstated or stated differently from what the code enforces. Pay
   special attention to:
   - C3's open-bound rule and compare periods;
   - C4's path and scenario rules;
   - C5's leaves ("speaker is not the system");
   - C6's band edges;
   - C8's per-unit and multiplier rules;
   - C9.
2. **Wording.**
   - Is any sentence in §2 wrong about what the code does, or does it contradict another sentence?
   - Does any example name the covered company or the gate's numbers (AGENTS §6)?
   - Does any sentence add a judging rule the standard does not hold (AGENTS §6, "The prompt carries the standard, not new rules")?
3. **The check changes in §3.** For 3.1 (signed period sets), 3.3, 3.4 (sign, trailing qualifiers, negation window), 3.5 (a null bound
   on a computed figure), 3.6 and 3.7: construct a wrong answer each lets through, or a right answer each refuses.
4. **The case list in §5.**
   - Are the registered inputs correct (thesis id, question, period, ladder)?
   - Are A1, A2 and A3 complete for the stop conditions?
   - Is any A1 form not expressible in the v13r shape as specified?
5. **Anything serious that would make the blind test unable to decide.** Report findings ranked by severity, with file and line.
   Say "nothing serious" if that is your finding.

Out of scope: the frozen ruler, `poc/config/poc-v118.json`, D725's pass lines, D731's harness rules, the system text's judging
sentences.
