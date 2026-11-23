# Review of the comparison's reading tools, round 3 (read-only, $0; D672's condition)

Rounds 1 and 2 said NOT READY (`tools-review-codex.md`, `tools-review-codex-2.md`; the Claude readers are summarised in D675). The fixes and
the written readings of the frozen rule are in D675. The tools in `stage0/` are:
- `score_comparison.py`
- `mapping.py`
- `mark_cards.py`
- `build_cards.py`
- `eligibility.py` (new)

Their tests are `test_score_comparison.py`, `test_mapping.py`, `test_mark_cards.py`, `test_build_cards.py` and `test_eligibility.py`. The in-memory mutants are
`mutants_reading_tools.py`, with its output in `mutants-reading-tools.txt`.

The rule is `stage0/verdict-rule.json`, the card is `stage0/card-spec.md`, and the plan is `RUN-PLAN-v12.md` §1.4.

**Check, citing file and line:**
1. Is every round-1 and round-2 finding fixed, or argued in D675 with a reason you accept? Name any you do not accept.
2. Did a fix break anything? Read each changed function against the rule. In particular:
   - the guardrail sample drawn from the system's own ids (`source_id`) while the cards carry neutral ids;
   - the redo store;
   - the debate's prior-round reading;
   - the plant pool.
3. Is anything left that a reader could see (system, key, another reader's mark), or a choice still open after outputs exist?

End with `READY TO READ` or `NOT READY: <the smallest changes>`. Under about 400 words. Do not open anything under `/private/tmp`,
`~/.codex/memories`, `~/.hivemind-keys` or `poc/data/comparison-2026-11-17/run`. Do not open `stage0/downloaded_files` (not ours).
