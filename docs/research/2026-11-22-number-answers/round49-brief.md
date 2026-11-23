# Council round 49: review the judging-v13 repair design before any code

You are an independent read-only reviewer. Alex chose one bounded repair of judging-v13's request and checks, then a $0 blind
conformance test (D734 in `docs/DECISIONS-log.md`; the failure it answers is D733 and
`docs/research/2026-11-22-number-answers/PAID-GATE-RESULT.md`; round 48's reviews are `codex-r48.md` and `claude-r48.md` there).

The design to review: `docs/research/2026-11-22-number-answers/REPAIR-DESIGN.md`.

Read against the code it changes:
- `calc_check.py` (the checks);
- `render_v13.py` (`v13_schema`, `render`, `strict`, `without_nulls`);
- `paid_gate.py` (`item`, `strip`, `Gate.attempt`, `summarise`, `merge`, `packets`, `card_view`, `normalise`);
- `gate.py` (the $0 gate's fixtures);
- `paid_rehearsal.py` (stub answers in the schema's shape);
- the request as sent, `paid-plan.json`;
- the stored answers, `poc/data/judging-v13-paid-gate-2026-11-22/answers.jsonl` and `retries.jsonl`.

Working rules: AGENTS.md §2 (design tables before code), §3 (code over prose; one owner), §6 (the request never asks for what a check
refuses; a field's definition beside the field; never grow a prompt without a written reason), §7.3.

## Questions

1. **Completeness of §2.** Walk every refusal message `calc_check.py` can emit. For each, is its rule stated in the repaired schema as
   §1 and §2 describe it (or held by an enum)? List every rule still unstated, with its line in `calc_check.py`. Include the rules on
   `what` keys (the outcome key match, C3/C4's shared quantities and periods, `compare_periods`), scenarios, `range` summaries,
   `basis` × `kind` combinations, C5's reference graph, C6's rung semantics for a range outcome, C9/C10, and the per-unit identity.
2. **The shape changes in §1.** Do the `outcome_for` and `reference_for` markers on figures cover every case the old fields allowed
   (a range summary as outcome, a shared figure, an unresolved member, a computed reference)? Does the scenario enum
   `base/low/high/range` lose a case DESIGN.md §2 allows? Is `from_answer` the right single owner, and does every reader of the
   answer get the converted shape?
3. **The check changes in §3.** For each change, construct a wrong answer it would now let through, if one exists. Especially:
   - 3.2's "<later> vs <earlier>" growth period. Does it let a sequential rate pass as year over year when the label is the
     model's own?
   - 3.4's containment rule: an expression that contains one extracted expression but changes its meaning, or a qualifier outside the
     extracted span.
   - 3.3's refusal of `%` in `product`: does any correct form need it?
4. **The blind test in §5.**
   - Are the six fresh requests fresh enough? Measure their evidence overlap with the gate's requests if you can.
   - Are A1 and A2 sufficient? Name missing forms and defects.
   - Is the classification of refusals (i)/(ii)/(iii) decidable without bias? Who decides, and against what?
   - Is "fewer than 6 of 12 passing" the right warning?
   - Does a stronger writer than gpt-6-luna make the test too lenient? If so, what would close that gap at $0?
5. **Anything serious the design misses**, including size and prompt growth, the internal fixtures, the plan rebuild, and the old
   plan's record.

Out of scope: the frozen ruler (AGENTS §7.1), `poc/config/poc-v118.json`, D725's pass lines, D731's harness rules, the system text's
judging sentences. Report findings ranked by severity, each with the file and line you read. Say "nothing serious" if that is your
finding.
