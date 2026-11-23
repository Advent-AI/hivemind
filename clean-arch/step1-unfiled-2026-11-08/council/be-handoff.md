Blind whole-request prompt audit, read-only, fresh session. Repository /Users/lchingen/hivemind. Read AGENTS.md §6 and
`.claude/skills/prompt-audit/SKILL.md`. Do not read any file under `clean-arch/step1-unfiled-2026-11-08/council/` until your answer is
written.

Scope: the complete request c9 as the model reads it:
- `clean-arch/step1-unfiled-2026-11-08/arms/c9-system.txt` (the system text);
- `c9-closing.txt` (appended after the item);
- `c9-schema.json` (every field description).

References:
- the signed standard `docs/prd/05-extraction-standard.html` §§2–5;
- D248, D380–D387 in `docs/DECISIONS-log.md`;
- the AGENTS §6 principles: a general hedge-fund brain; examples from varied domains; no bench-fitted example; a closed set with
  examples; growth needs a reason.

Read it top to bottom once, then deliver in English, under 700 words:
1. Every clause that decides **link** or **open**, with a verdict for each (consistent / contradicts / keeps wider / keeps narrower /
   no source), quoting the clause and the source line. Work in both directions: also name any line of the standard or decisions the
   request fails to carry on linking or opening.
2. Any two clauses that pull against each other on linking or opening, and any wording a model could read as the opposite.
3. Bench-fitted or one-industry examples.

End with READY or NOT READY (the blocking clause).
