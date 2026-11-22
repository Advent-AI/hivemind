# Is poc-v118 ready for a production test? (council P, 2026-11-20, consensus; $0)

Alex asked, after choosing A (D690): "describe to me what the end-to-end system looks like. What are the components, how it's done,
and what is the current performance? Are we ready to actually start to push this to production for testing?"

Record: `council-p-brief.md`; Claude's position, written first: `council-p-claude.md`; Codex round 1: `council-p-codex.md` (thread
`01a1fb07-9dc1-7560-ba64-999178d52831`, read-only, memories off); round 2: `council-p-round2-brief.md`, `council-p2-codex.md`, CONSENSUS.

## Answer
**NOT READY for a daily production test; ready for a $0 read of its output.** Every pipeline piece is built and ran 82 days three times
without a stop. Three pieces of operation are missing, and no person has read poc-v118's own output on the product page.

## The system
| Step | What it does | Code | State |
|---|---|---|---|
| Sources | Harvest news, filings and company releases; assemble, freeze a window, clean | `poc/corpus/scripts/` | Built, run by hand per window; no schedule; NVDA corpus ends 10-27 |
| Dispatch | Validate, number and route each item in order | `dispatch.py` | Built |
| Extraction | One `gpt-6-luna` call per article (v74i, low): files quoted evidence under the questions open at day start, proposes questions | `extraction.py` | Built, frozen |
| Matching and writing | Jev 1.14 with the collision judge; append-only SQLite | `views/jev_matching.py`, `views/writing.py` | Built, frozen |
| Judging | Once a day, judging-v7 (medium) re-judges changed questions to a rung, with citations | `views/judging.py` | Built, frozen |
| Pull mode | Closes a question at its rung on its due day | `pull.py` | Built |
| Driver | Days in order; resumes after a store's last completed day | `scripts/replay.py`, `src/hivemind/replay.py:62` | Built; no daily wrapper |
| Serving | HTTP API, MCP, the page, the Idea call (`poc-v118-idea`) | `scripts/hivemind_api.py`, `scripts/hivemind_mcp.py`, `poc/ui/` | Built; serves the v34 ledger through 08-28, not poc-v118's output |

## Performance (measured)
- **Stability:** three 82-day draws (07-01..09-20, 1,884 articles each) completed in about 2 h 45 min each, opened 47, 43 and 49
  questions, and had 1, 4 and 2 refused judgements, all recovered, with no terminal failure (`run/old-*/prod/replay.log`).
- **Cost:** $7.40, $6.72 and $6.85 of model usage priced from tokens, about $0.08–0.09 a day; the spending guard booked $9.83, $8.60
  and $8.83 because it charges three attempts for every Jev response (council P round 2).
- **Coverage:** a supported, worth-tracking answer on 10 of 32 key matters in at least two of three draws (release comparison,
  diagnostic).
- **Frozen window (07-01..07-14):** 1/1/1 settled agreements on the 7 graded ruler questions (2/2/2 with disputed points); no
  eligible judgement disagreed; every loss was a question not opened in the ruler's shape
  (`clean-arch/e2e-comparison-2026-11-13/CENSUS-FULL-RESULT.md`).
- **Answer errors:** 24 answers rejected by both blind readers across the comparison's five stored draws: overlapping amounts added,
  another scope's figure taken, unsupported steps off a reference (`2026-11-20-hybrid/census/CENSUS.md`).
- **Never measured:** a person reading poc-v118's output (the pilot deck has waited since D560); a second company; live arrival and
  late articles; a window past 09-20 for poc-v118; the Idea call on a poc-v118 store.

## Missing for a daily production test
1. A daily feed and start (the harvest tools exist; no schedule; the gap after 10-27 needs a plan).
2. Publishing each finished day to the page, API and MCP together, keeping the last good copy on a failed day.
3. Spend, stale-data and failed-day alerts; the replay's `--cap` can overshoot.

Alex's to decide: where it runs (Docker has no outbound model calls under the VPN on this Mac), who tests, and the spend ceiling.

## Recommendation and one test (consensus)
1. **$0 first:** serve a copy of old-2's finished 09-20 store (43 questions, 42 open) with its articles locally on the page, API and
   MCP, confirm all three show the same day and source links (the page silently keeps its embedded v34 copy if its fetch fails), and
   Alex reads it for half an hour: would an analyst use this? Codex read the store through the shared reader (`bundle.py:225`): it
   returns 09-20 and all 43 questions.
2. **Only if he says yes:** build the daily wrapper (harvest → clean → append → replay one day → snapshot → publish) with its alerts,
   rehearse it one day at a time over the harvested 09-21..09-27 with one deliberately failed day (about $0.60 at the measured rate),
   then plan the gap after 10-27 and switch to real days.

## Step 1 done (2026-11-20)
Alex: "做". A copy of old-2's 09-20 store is served on the host: the page at http://127.0.0.1:8792/index.html, the API on 8790 and MCP
on 8791 (`poc/data/review-v118-old2-0920-2026-11-20/README.md`). Checked: the page fetched `/library` from 8790 (HTTP 200); the API's
`/library` and MCP's `thesis_library` are byte-identical (09-20, 43 questions, 42 open); a question's detail shows its answer,
reasoning, quotes and source links. $0. Waiting on Alex's read.

## Step 1 read by the council (2026-11-20)
Alex: "dont' you take a look for me let the council tak ea crack at it". Council Q (Codex and Claude, consensus in round 2, $0;
`council-q/RESULT.md`): **PARTLY**. An analyst would use it to find sources and check milestones, not for its number answers:
linked number questions contradict each other in all three draws (old-2: Data Center Q4 about $146B against a total Q4 of about
$127B), because each question is judged alone; the dependencies that would link them are decided (D368 item 2) and not built.
Recommended to Alex: do not build the daily wrapper yet; open a judging version with the decided dependencies, tested first at $0
on the exact request text, then a few cents on the three draws' revenue questions.
