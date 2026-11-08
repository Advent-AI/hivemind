Blind prompt audit, read-only. Repository /Users/lchingen/hivemind. Read AGENTS.md §6 and `.claude/skills/prompt-audit/SKILL.md` first.

Scope: the candidate Step 1 request "c2" only. Do NOT read `clean-arch/STEP1-CONDITIONS-DESIGN.md` §16 (the author's own audit) before you finish yours; you may read it afterwards to compare.

The request as the model reads it: `clean-arch/step1-unfiled-2026-11-08/arms/c2-system.txt` (system), `c2-closing.txt` (appended after the item), `c2-schema.json` (stated in the system text). The control is `clean-arch/takeover-2026-11-07/k6b-*` (diff them).

The standard and Alex's decisions to audit against:
- the signed extraction standard `docs/prd/05-extraction-standard.html` (frozen; its keep rule, reject rows, opening tests, §4.3);
- D209 and D371 in `docs/DECISIONS-log.md`;
- Alex's four rulings and his reframe: `clean-arch/step1-unfiled-2026-11-08/LOG.md` §§11, 16, 17 (cash drop; margin kept under the existing revenue thesis, no separate margin thesis; keep the analysts' EPS forecast, drop the author's target price; drop a small supplier's step; a thesis is a view with a reason; a useful company figure no view takes is kept as a condition);
- AGENTS §6 principles (general hedge-fund brain, no bench-fitted example, closed set with examples, no growth without reason).

Deliver, in English, under 700 words:
1. Every clause of c2 that decides keep, reject, link, open, or a figure/condition, with a verdict: consistent, contradicts, keeps wider, keeps narrower, or no source — citing the standard line or Alex's words. Include clauses c2 left unchanged from K6b if they now conflict with the new clauses (for example the closing check's sentences about unfiled items, the evidence test, the do-not-open list, the "valuation is kept" row).
2. Walk each of Alex's four rulings and the reframe through c2 and predict what the model will do, naming the clause that decides it and any clause pulling the other way.
3. Any example that is bench-fitted or one-industry, and any abstract clause that will be a coin flip.
4. The fixes you would make before a send, smallest first. End with one line: READY TO SEND (motivating cases, a few cents) or NOT READY (the blocking clause).
