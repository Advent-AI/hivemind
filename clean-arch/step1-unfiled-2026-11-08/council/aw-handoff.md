Code review for check-in, read-only, fresh session. Repository /Users/lchingen/hivemind, branch clean-arch. Read AGENTS.md §§3–4
(code and test rules) first.

The branch will commit the clean-architecture work that is currently untracked or modified:
- `src/hivemind/model.py`: see `git diff src/hivemind/model.py` (`openai_transport` gains `max_attempts` and keeps response bodies on
  failure);
- `clean-arch/step1/*.py`: runner, live transport, launchers, source materialisation, quote lookup, renderers, and their tests;
- `clean-arch/step2/compare.py`, `run_forward.py` and `test_compare.py`;
- `clean-arch/step3/library.py` and `test_library.py`;
- `clean-arch/render.mjs` (diff);
- the measurement scripts in `clean-arch/step1-unfiled-2026-11-08/*.py`, `clean-arch/takeover-2026-11-07/*.py` and
  `clean-arch/step2-validation-2026-11-07/*.py`. These are experiment harnesses; review them more lightly.

Out of scope: the production pipeline outside `model.py`, the frozen ruler, and prompt wording (already audited).

Find, ranked by severity, with file:line and the concrete failure:
1. **Correctness bugs.** Wrong results, silent failures (a warning where a refusal is needed), a race, a resource leak, or a wrong
   default in production code (`model.py`: does the default path keep production's behaviour exactly, including the sleep and retry
   counts?).
2. **AGENTS §3 violations.** A branch taken on an environment variable; wall-clock ordering; a credential in an argument, a log or
   stored data; non-descriptive names; duplicate implementations of one rule; a comment that states history rather than behaviour.
3. **Tests that trace to no requirement**, test the wrong thing, or would pass on a broken implementation.
4. **Dead or superseded code:** scripts nothing calls; files that should not be committed (raw `*.jsonl` event streams, `*.stderr`,
   `*.pid`, scratch outputs); any secret or key material. Check by grepping.
5. **Cleanup that would make the commit reviewable,** without changing behaviour.

Run nothing that writes. Under 1,000 words. End with: BLOCKERS (must fix before commit), SHOULD FIX, NITS.
