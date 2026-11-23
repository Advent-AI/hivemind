Blind whole-request prompt audit, read-only. Repository /Users/lchingen/hivemind. Read AGENTS.md §6 and `.claude/skills/prompt-audit/SKILL.md`. Do NOT read `council/ah-claude.md` until your answer is written.

Scope: the complete request c8 as the model reads it: `clean-arch/step1-unfiled-2026-11-08/arms/c8-system.txt` (system), `c8-closing.txt` (appended after the item), `c8-schema.json` (stated in the system text, every field description included).
References: the signed standard `docs/prd/05-extraction-standard.html` (§§2–5); Alex's decisions D380–D386 in `docs/DECISIONS-log.md` (figures are conditions; material no-home statements kept unlinked and linked later; theses only for the standard's four reasons, class A excluded by D382; target prices and valuation conclusions not kept); AGENTS §6 principles (general hedge-fund brain, examples from varied domains, no bench-fitted example, closed set with examples, growth needs a reason).

Read the request top to bottom once, then deliver in English, under 900 words:
1. Every clause that decides keep, reject, link, open, or a figure: verdict (consistent / contradicts / keeps wider / keeps narrower / no source), quoting the clause and the source line. Both directions: also list any line of the standard or decision the request fails to carry.
2. Any two clauses of the request that pull against each other (including old K6b text beside the new text), and any wording a model could read as the opposite of the decision (for example "unfiled" now meaning kept).
3. Bench-fitted or one-industry examples; abstract clauses with no example.
4. Size: characters per file and whether each addition carries a decision; anything redundant to cut.
5. The smallest fixes before freezing. End with READY TO FREEZE or NOT READY (the blocking clause).
