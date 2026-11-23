# Council round 38: the citation-only judge version, design review (read-only)

Alex opened a new judge version whose only change is the answer format's id fields (D712; his words in `docs/DECISIONS-log.md` D712).
Review `docs/research/2026-11-21-citation-lists/DESIGN.md` before any code is written (AGENTS §2: a blank or wrong cell means not
ready). Governing code: `src/hivemind/views/judging.py` (`schema_for`, `evidence_shown_in`, `themes_shown_in`, `check_answer`,
`round_of_judgements`, `_lines_english` closing line), `src/hivemind/model.py` (`build_request`, `request_identity`, `call`),
`src/hivemind/config.py`, `scripts/preflight.py`, `tests/test_frozen_questions_and_judgement.py`, the harnesses in
`docs/research/2026-11-21-whole-window/` and `docs/research/2026-11-20-production-readiness/dependency-design/`. Data: the stored runs
`poc/data/comparison-2026-11-17/run/old-{1,2,3}/prod/`, the pilot copies under
`/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/{control-1-copy,linked-1-copy}/`
(read-only; the scripts `enum_size_census.py`, `id_typo_census.py` are in that scratchpad folder).

Out of scope: the frozen ruler, the prompt text, the rung field, the link direction (a separate design), every module but judging's
answer format and what reads it. No paid call. Your report is a lead; cite what you read.

Questions:
1. Is every table cell right and complete? Find a state, event, reader or old check the design misses, with a concrete case.
2. Representation (§3): plain enum per field, a shared `$defs` enum, or a pattern alternation? Which is safest under the provider's
   limits and the stored sizes, and what would you verify first?
3. The lists read from the sent text versus from the store objects that rendered it: is reading the text right? Does
   `check_answer`'s dependency set (store `dependencies_of` resolved ids) equal the ids the text lists in both shapes (v7 and v8)? Any
   case where they differ?
4. Versions as two names (judging-v9/v10) versus a config field: which, and why? Should v10 be built now?
5. Is the $0 test (§5) sufficient and exact, and can T1 be run with the existing replay machinery (old-2 replayed with a transport that
   matches system and user bytes)? What would make it pass while the product is wrong?
6. Anything in the design that adds a mechanism for an unnamed case, or departs from D711/D712's scope?
