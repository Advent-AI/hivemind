# Council round 52: the judging-v13 small format (v13s), before any code

You are an independent read-only reviewer.

**Alex's decision D737** (in `docs/DECISIONS-log.md`): shrink judging-v13's format.
- Code refuses an answer only for five defects:
  - a number misread;
  - wrong arithmetic;
  - a part above its whole, or added into it;
  - two forecasts of one quarter;
  - an own estimate passed off as the market's.
- It also refuses broken structure.
- Each rule is written in one or two sentences beside its field. Everything else is shown to readers, never refused.

**Review scope (binding, D737):** report a finding only when it does one of these:
- (a) lets one of the five defects through the rules as written;
- (b) breaks structure (a link, a cycle, a missing or doubled answer, an outcome not of the question's quantity, a rung not holding
  the outcome);
- (c) refuses a right answer;
- (d) states a rule differently from how the design says code will enforce it;
- (e) makes the blind test unable to decide.

A wrong answer outside the five defects is a reader's matter. It is not a finding. Earlier rounds kept finding such cases, and Alex
chose to stop enforcing them.

**The design:** `docs/research/2026-11-22-number-answers/SMALL-DESIGN.md`.

**Background in the same folder:**
- `PAID-GATE-RESULT.md`;
- `REPAIR-DESIGN.md` §5, the blind test this design carries over;
- `codex-r49.md` and `codex-r51.md`, the earlier rounds;
- `calc_check.py`, today's checker, kept for the old run;
- `render_v13.py` and `paid_gate.py`, the harness;
- `paid-plan.json`, the request as sent;
- the stored answers in `poc/data/judging-v13-paid-gate-2026-11-22/`.

## Questions

1. **Coverage of the five defects.** For each defect, construct the strongest answer that commits it and passes S1–S8 as written. For
   example:
   - for S8, Data Center added into company revenue through an estimate, or through a product with a multiplier of 1;
   - for S4, a second forecast hidden as an estimate or a computed figure without basis forecast;
   - for S5, a reference computed from a reported figure and an estimate relabelled reported.
   For each case, say whether the request could state a closing rule in one or two sentences, and give the sentence.
2. **Right answers refused.** Construct right answers the rules refuse, within the formats an analyst needs for the six registered
   cases, the gate's twelve requests and the stored answers. Look in particular at:
   - S1's number parser (currency forms, "US$", "bn", ranges, "twice");
   - S8's period algebra;
   - S2's range arithmetic;
   - S3's paired ends.
3. **Wording.** Does any sentence in §3 contradict another or §2, or name the covered company? Does any sentence add a judging rule
   (AGENTS §6)?
4. **The build (§4).** Does every reader of the decoded answer get the shape it needs? Does the old run stay reproducible? Is anything
   missing for the rehearsal?
5. **The blind test (§5).** Are A1, A2 and A3 sufficient for the stop conditions? Are the registered inputs right? Can the
   reader protocol decide "usable" without bias?

Report findings ranked by severity, each tagged (a) to (e), with file and line. Say "nothing serious" if that is your finding.
Out of scope: the frozen ruler, `poc/config/poc-v118.json`, D725's pass lines, D731's harness rules.
