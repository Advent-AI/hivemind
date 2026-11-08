Blind prompt audit, read-only, fresh session. Repository /Users/lchingen/hivemind. Read AGENTS.md §6 and
`.claude/skills/prompt-audit/SKILL.md`. Do not read any file under `clean-arch/step1-unfiled-2026-11-08/council/` until your answer is
written.

Scope: two complete requests.
- c10a: `arms/c10a-system.txt`, `c10a-closing.txt`, `c10a-schema.json`;
- c10b: `arms/c10b-system.txt`, `c10b-closing.txt`, `c10b-schema.json` (with the `unsigned_obligation` field description).

Both are in `clean-arch/step1-unfiled-2026-11-08/`. References: the signed standard `docs/prd/05-extraction-standard.html` §§3–5;
D248, D380–D388 in `docs/DECISIONS-log.md`.

Deliver in English, under 600 words:
1. Every clause that decides **opening** a thesis, with a verdict for each (consistent / contradicts / keeps wider / keeps narrower /
   no source), in particular the closing's final read-back. Name any line of D388 or D248 the requests fail to carry.
2. Any clause pulling against the read-back, in particular "drop the thesis if … an open thesis exists and its answer cannot move
   apart from it", the §3 "another estimate, source or wording of what an open thesis tracks", and "If the two cannot move apart". Is
   the precedence clear?
3. For c10b: does the field's definition agree with the read-back and the standard?

End with READY or NOT READY (the blocking clause), for each arm.
