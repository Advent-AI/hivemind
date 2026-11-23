# Council round 1: Step 1 thesis library and noise (independent investigation)

You are Codex, the second member of a council with Claude Code. This is a read-only task: do not edit any file, do not run model
calls, do not start runs. Investigate independently first; Claude is investigating the same material in parallel, and you will
challenge each other afterwards.

## Objective (Alex, 2026-11-07)

Make the clean-architecture Step 1 meet this pass line on the 115 golden-v5 dev articles, run forward in publication order from an
empty library (one draw):
- at most 3 small or noisy theses in the final library;
- no fragmented bets (one bet tracked as several theses);
- helpful matters kept at least 190 of 234, scored by the frozen scorer's matching (`score_gold.py`'s `same_matter`).
Also reduce noise: items matching a not-kept gold span (currently 50; frozen production 30–34).

Alex explicitly opened the solution space: prompt restructuring, pipeline-structure changes, other models (DeepSeek flash or
v4-pro are callable; there is no Anthropic key), and different reasoning effort. He wants approaches not tried before, not small
wording tweaks.

## Constraints you must respect

- Alex's decided contract for Step 1: Luna reads the item and all open theses for the entity; it returns thesis–evidence pairs;
  evidence and thesis always come together; an existing thesis is reused (never a duplicate); a new thesis comes with evidence;
  there is no separate thesis-routing stage (Alex, 2026-11-06: "thesis routing is not necessary"); Step 2 later compares evidence
  with stored history (search + Jev); a thesis carries entity, question, outcome to track, period when known.
- Alex's granularity rule (AGENTS.md §8): only big matters become theses ("不要搜集一堆鸡毛蒜皮的事情，要看重要的大事"); one bet = one
  question; a topic may open without a date (Alex: "no need to be very strict in opening ... just don't open 'noisy' thesis").
- The frozen ruler (AGENTS.md §7.1) is not changed; the frozen production configuration and its prompt files are not edited.
- Out of scope: Step 2–4 implementation, the source-cleaning track, the UI.

## Primary materials

- Current candidate K5: `clean-arch/takeover-2026-11-07/k5-system.txt` (system) and `k5-closing.txt` (appended at the end of the user
  message after the JSON payload); schema in `clean-arch/PRD.md` §12 "Proposed structured-output schema"; runner
  `clean-arch/step1/runner.py`.
- The full K5 forward run over 115 gold articles, exported readably:
  `poc/data/clean-step1-takeover-2026-11-07/council-trace-gold-k5.json` (per article: text, open theses before, new theses, evidence
  with links and relevance). Raw trace: `poc/data/clean-step1-takeover-2026-11-07/gold-k5/trace.sqlite`.
- Scores and misses on the frozen gold: `poc/data/clean-step1-takeover-2026-11-07/gold-scores-final.json` (runs `k5`, `k2`,
  `clean-control`, production draws); gold: `docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json` (its `items` with
  weights and `not_kept` with reject rows); scorer `docs/research/2026-10-29-ledger-standard/score_gold.py`.
- Frozen production's prompt for comparison: `src/hivemind/prompts/role-v74i.txt`, `review-v74i.txt`; its opening reasons and
  "do not propose" list are in role-v74i.
- The takeover log with every round so far and its regressions: `clean-arch/takeover-2026-11-07/LOG.md` (read §§1–10).
- Codex's own earlier Step 1 experiments (yours, 2026-11-06/07): `clean-arch/STEP1-RUN-LOG.md` and the `clean-arch/STEP1-*.md` files.
- The standard: `docs/prd/05-extraction-standard.html` (Chinese), AGENTS.md §6–§8.

## What to deliver

1. **Mechanism of small theses.** Read the articles where K5 opened theses that a senior analyst would not hold a card for (for
   example the executive transition, Omniverse made free, DLSS in games, RTX 50 SUPER, Beersheva R&D, orbital data centres, lidar
   policy, the company's own debt raise) and the fragmented families (customer financing / backstops; competing chips). For each,
   what in the request led there? Cite the article number and the request text.
2. **Mechanism of the remaining noise** (the 50 items matching not-kept spans; 46 of them are filed under big theses).
3. **Approaches, ranked by expected effect on the pass line**, including at least two not tried before (structural, payload,
   model or effort changes, not only wording). For each: the mechanism it targets, what it could break (recall, core items,
   linking), the cheapest decisive check (which stored articles, how many draws), and how it fits Alex's contract.
4. Facts versus hypotheses, kept apart. Cite files and article numbers.

Return a concise report (under 1,500 words).
