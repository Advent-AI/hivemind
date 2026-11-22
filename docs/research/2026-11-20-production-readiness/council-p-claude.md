# Council P: Claude's position, written before reading Codex's

## The system (poc-v118), end to end
1. **Sources.** A batch harvest toolchain (`poc/corpus/README.md`; `poc/corpus/scripts/harvest_*.py`: Google News, GDELT, EDGAR,
   official notices, company blogs) → `assemble.py` → `freeze_window.sh` → `clean_pages.py` (D351). It is run by hand per window;
   there is no scheduler. The last harvested window is NVDA 07-01..10-27 (`items-nvda-2026-07-01-10-27.sqlite`).
2. **Dispatch** (`dispatch.py`): each item validated, numbered and routed, in order.
3. **Extraction** (`extraction.py`, `gpt-6-luna`, v74i, low effort; one call per article): reads the questions open at day start,
   files quoted evidence under them, proposes new questions.
4. **Matching and writing** (`views/jev_matching.py`, Jev 1.14 with the collision judge; `views/writing.py`): open, merge or skip a
   candidate; repeat, replacement or new for evidence; append-only SQLite.
5. **Judging** (`views/judging.py`, judging-v7): once a day, the questions whose evidence changed get a rung on their ladder, with
   citations.
6. **Pull mode** (`pull.py`): a question closes at its rung on its due day.
7. **Driver** (`scripts/replay.py`): days in order over a frozen items database; it resumes after a store's last completed day
   (`src/hivemind/replay.py:62`), so a store can be extended.
8. **Serving:** HTTP API, MCP server, the page (Thesis Library, Explore Ideas) and the Idea call (`poc-v118-idea`, three calls). They
   serve the sealed `served-2026-10-28-v34-nvda-3m-through-0828` ledger, built by the older `poc-v34` (README, "Local requirements";
   DECISIONS §13). **No analyst has seen poc-v118's own output on the page.**

## Performance (measured)
- **Release comparison** (07-01..09-20, 82 days, about 1,884 articles, 3 draws; `2026-11-17-product-comparison/RUN-LOG.md:32-41`):
  old serves 10 of 32 key matters ("served" = a covering question rated worth tracking and supported, plan v12 item 5); the new
  system 2–3. Each old draw cost $8.60–$9.83 (about $0.11 a day) and took under three hours of wall clock for 82 days; no stop.
- **Answer quality:** among worth-tracking questions in the 5 stored draws, 24 answers were rejected by both blind readers
  (`2026-11-20-hybrid/census/CENSUS.md`): overlapping amounts added, a figure of another scope taken as the answer, unsupported
  adjustments, talks taken as likely completion. About 16 of 24 step off a reference rung the judge itself named.
- **Frozen ruler** (14 days, judgement at 07-14): poc-v116 53/57 against poc-v108 45/57, three draws (`CURRENT_STATE.md:134`).
  poc-v118 itself cannot be scored by the seeded scorer (README, "Run the pipeline").
- **Never measured:** a second company; live latency; a window past 09-20 for poc-v118; a human analyst's read of its output (the
  pilot deck has waited on Alex since D560); evidence growth over months (open defect 7, D358 stopped the v34 run on bloat).

## Readiness for a production test
| Requirement | State | Evidence |
|---|---|---|
| New articles each day | Partly: tools exist, run by hand per window, no schedule; corpus ends 10-27 | `poc/corpus/README.md` |
| The pipeline run each day on a continuing store | Partly: replay resumes a store; a daily wrapper and an items database that grows are not built | `src/hivemind/replay.py:62` |
| Its store served to the page, API and MCP | Partly: one-edit swap documented; serving-while-writing proofs were built for the new system's writer (D594–D603), and a restart is Alex's | README "Switching the served data"; `OPERATING-CONTRACT.md` |
| Cost cap and monitoring | Partly: `--cap` per run, not hard; cost is small (about $0.11/day for one company) | README "Run the pipeline" |
| Quality accepted | No: not accepted end to end; 10 of 32 matters; no human read | `CURRENT_STATE.md:133` |
| Hosting | Host only: Docker has no outbound model calls under the VPN | AGENTS §9 |

**Verdict: NOT READY for a live production test today; READY for a shadow forward test now.** The pipeline is complete and stable
over 82 days, cheap, and has never stopped; what is missing is (a) a daily feed and wrapper, engineering of a few days, and (b) any
human read of what it gives an analyst.

**Recommendation and one test.** Run poc-v118 forward from one old draw's 09-20 store over the unseen 09-21..10-27 articles (already
harvested; about $3 for one draw at old's rate, Alex's money since D439 has $0), serve that store locally on the page, and have Alex
read it for half an hour: is this something an analyst would use? It tests the two things never tested (fresh articles after the
design's window, and the product page showing poc-v118's output) and decides whether the daily-feed engineering is worth building.
