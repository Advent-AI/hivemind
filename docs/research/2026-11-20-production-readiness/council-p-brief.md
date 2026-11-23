# Council P: is the production system ready for a production test? (read-only; no model calls; no edits)

## Alex's question (2026-11-20, his words)
"describe to me what the end-to-end system looks like. What are the components, how it's done, and what is the current performance?
Are we ready to actually start to push this to production for testing?"

"This" is the system Alex just confirmed as the product: the replay default `poc/config/poc-v118.json` ("the old system"; D689,
D690 in `docs/DECISIONS-log.md`). The hybrid, the judge fix, the c8 reading and the opening changes are closed (D689, D690) and are
out of scope: do not propose improvements to them.

## What I need from you, independently and from primary sources
1. **The system, end to end.** From a source article to what an analyst sees (the page, the HTTP API, the MCP server, the Idea call).
   For each component: what it does, the code that runs it, the model and settings, and whether it exists in code, is only designed,
   or is not built. Include what sits outside the pipeline: where articles come from (upstream supply), what starts each day's run,
   which store the service serves today and which pipeline built it.
2. **Measured performance,** each number with its scope, draws and source file:
   - quality: the frozen ruler (AGENTS.md §7.1) where it applies to this configuration, and the release comparison's 32 matters
     (`docs/research/2026-11-17-product-comparison/`);
   - stability across draws, cost per day or per run (priced from tokens, AGENTS §7.2), run time, refusals and failures;
   - what has never been measured (for example a window longer than the one measured, a second company).
3. **Readiness for a production test.** Define the smallest honest "production test" for this product: for example, new articles
   arriving daily for one company, the pipeline run each day, its store served to the page, API and MCP, with a cost cap and
   monitoring. For each requirement: exists, partly, or missing, with file:line evidence. Rank the blockers by impact. Say which
   blockers are engineering and which are product choices only Alex can make.
4. **One recommendation and one test** of it, with its cost if it costs money.

## Where to look
`README.md`; `docs/CURRENT_STATE.md` ("What runs", "Open defects", and the blocks from D563 and from D665 onward);
`docs/poc/pipeline-plan.md`; `docs/poc/service.md`; `docs/prd/README.md` and `docs/prd/10-filing-phase.md`;
`docs/research/2026-11-17-product-comparison/RUN-LOG.md` and `RUN-PLAN-v12.md`;
`docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md` and `DECISION-PAGE-2026-11-16.md`; `scripts/`;
`src/hivemind/`; `poc/config/`.

## Constraints
- Read-only. No model or network calls. Do not open any database under `poc/data/` that a run may be writing (none is live today,
  per `CURRENT_STATE.md`); reading files and the code is enough.
- Do not read credentials (`~/.config/hivemind/`), settings files, `.mcp.json` or `~/.claude.json`.
- The frozen ruler never changes. Nothing is deployed, pushed or committed.
- A claim without a file you read behind it is labelled as an inference.

Answer in under 700 words with file:line citations. End with one of READY, READY WITH CONDITIONS or NOT READY, and the shortest path
to a production test.
