Council A on a design before any code. Read-only, fresh reader, under 450 words. Repository /Users/lchingen/hivemind.

**Context:** Alex chose (D396 in docs/DECISIONS-log.md): "设计新系统自己的“判断”环节". The design is
`clean-arch/step4-2026-11-10/DESIGN.md`.

**Also read:**
- `clean-arch/PRD.md` §§2, 4–7 (the clean architecture; Step 4 is left open);
- `src/hivemind/prompts/role-v74i.txt`, the ladder lines;
- `src/hivemind/extraction.py` (`check_ladder`, `normalise_ladder`, `check_bounds`);
- `src/hivemind/views/writing.py` (`_create_view`);
- `src/hivemind/views/judging.py` and `round.py`;
- `clean-arch/e2e-2026-11-09/adapter.py`;
- D38, D354, D359, D364 and D370 in docs/DECISIONS-log.md;
- AGENTS.md §2 (design tables) and §§6–7.

**Check:**
1. **Is option B (a separate ladder call at opening) right against A and C?** Is reusing production's frozen ladder text and checks
   sound, or does it import production-specific fields (object, measure, scope keys, groups) the clean system does not have?
2. **Are the tables complete (AGENTS §2)?** Name any missing state or event, value or reader, or old check. Examples to consider:
   duplicate theses; a later restatement; a due date already past; theme against asset; dependencies (the judge reads
   `dependencies_of`); themes in force.
3. **Is the first test sound and decidable without a gold?** Two reader families plus an adjudicator, and the lines in §8. Does it
   answer Alex's question: are the system's answers to its own questions well supported?
4. **What decision must Alex make before a build?** For example, the new ladder prompt under D359 and D364.

**Out of scope:** changing frozen prompts, c8 or the ruler.

End with READY or NOT READY and the blocking items.
