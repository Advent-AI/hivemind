# Council R, round 1 (independent): a build-ready design for linking related questions in the product, or what blocks it

You are a read-only reviewer of the Hivemind repository (`/Users/lchingen/hivemind`). Read `AGENTS.md` first: it governs. Read the
primary material yourself; this brief points at it and states no preferred answer. Write your answer as a Markdown document.

## Why this review exists

The product is the configuration `poc/config/poc-v118.json` (D690). It opens questions from news about NVIDIA and judges each one every
day. Council Q (`docs/research/2026-11-20-production-readiness/council-q/RESULT.md`) found that its number answers contradict each other
in all three stored draws (for example the Data Center segment's Q4 near or above the whole company's Q4), because no question reads
another's conclusion: the stores hold no dependency row. Alex chose (D691, `docs/DECISIONS-log.md`): no daily wrapper yet; link related
questions first, a $0 check then a few cents.

The few-cents probe passed (D692; `docs/research/2026-11-20-production-readiness/dependency-probe/RESULT.md`, `claude-marks.md`,
`render-check.json`): on one draw-day, with the total-revenue question's conclusion shown through one dependency row rendered by
production code, 2 of 3 Data Center answers reconciled against 0 of 3 unchanged. Read its "What it does not show" section.

The decided next step (D692) is this review, at $0, before anything is built or sent, and then Alex. An earlier stretch already worked on
the subject and closed with a design that is **not sound for build** (D533–D542, `docs/DECISIONS-log.md` from "## D533" to "## D543";
`docs/research/2026-11-14-use-acceptance/dependency-selection/SEPARATION-DESIGN.md`, read it whole). D542 lists what a reopened review
must settle before any build.

## The question

For the product as it runs (poc-v118: no preset questions, so no seed edges; the Jev matcher; judging-v7), is there a design that links
related number questions so that their answers can agree, that is complete under AGENTS §2's four tables and consistent with the
decisions in force? If yes, state it. If not, state exactly what blocks it and which choices only Alex can make.

Settle each of these, citing the file and line or the decision you rely on:

1. **Who chooses an edge, and which way it reads.** D51 and D368 item 2 (Alex) say the matching call chooses a new question's
   dependencies; the Jev matcher returns none (`src/hivemind/views/jev_matching.py`, the candidate loop near lines 260–355). Material:
   - `selection-census.md` in this folder (`selection_census.py`): the matcher's stored "part_of" answers (its criterion is "in either
     direction", `jev_matching.RELATIONS`) and the typed keys code already stores for every number question (`view_keys`).
   - the old matching prompt's dependency step (`src/hivemind/prompts/matching-v3.txt` line 10–11) and schema (`views/matching.py`).
   - AGENTS §2 "Code owns identity, never importance"; SEPARATION-DESIGN §2.5's ownership table.
   - The reading direction: PRD 06 (`docs/prd/06-views.md` lines 114–140) and D537 support "the segment reads the total"; D368 item 4
     says, for seed edges, "the supported (root) question reads the supporting questions' conclusions"; council Q quoted D368 item 4 for
     the product; the probe used the segment reading the total. Say which applies to which kind of pair, and on what source.
   - The direction label the judge is shown (`first_is_bullish` and so on: matching-v3 line 11; `judging.py` near line 148).
2. **What the dependency line carries.** `views/judging.py` `_lines_english` prints the dependency's reasons cut at 600 characters, not
   its implied outcome; `render-check.json` shows the decisive figure lost in two of three draws. The judge's prompt file is frozen
   (`tests/test_frozen_questions_and_judgement.py`); the line is code.
3. **Filing.** Every edge in the product would be a chosen (`reads`) edge. `extraction.narrowest_links` (D265) treats every row as "the
   reader is the narrower home" and, in D538's proof, removed seven total-revenue links (`EDGE-PROOF-RESULT.md`). SEPARATION-DESIGN §2.1
   proposes not applying it to a chosen edge. Settle it for the product.
4. **D542's five items, as they apply to the product:** a circle through an awaited question at creation (`views/writing.py`
   `resolve_waiting`); closing (PRD 06's "historical only" has a reader and no writer); a theme shown twice (theme block and line); the
   historical readers (service, bundle, search, research context, idea route); the label's meaning (the seed label `last_end` exists
   only on seeded stores; say whether anything of it remains for the product).
5. **Order, propagation and cost in the daily round:** `judging.topological`, `queued_by_change`; how many extra judge calls a day a
   linked pair costs (rates in `hivemind.model.PRICES`).
6. **What changes and who opens it:** which frozen pieces a build touches (AGENTS "Where to look first", D354), and the smallest test
   on the product's own path that would show the build makes the answers agree without making them wrong (note SEPARATION-DESIGN §9:
   a fixed-state probe is not the sequence a live judge produces). Give its cost from the published rates.

## Out of scope (do not report on these)

Seeded configurations and the seed label beyond item 4; the daily wrapper; the "self-made market reference" defect (traced
separately); council Q's other findings (duplicates, small bets, missing bets); the reading (extraction) prompt; the frozen ruler; any
paid send. Do not propose new mechanisms for cases no one has named (AGENTS "Authority and scope").

## What to return

Per item: your answer, its sources, and whether it is decided by existing decisions, open for the council under D439-style reasoning,
or Alex's choice (a change to what the system does or to a frozen piece). Then: is a build-ready contract reachable now (yes / no /
yes after named choices), the list of Alex's choices with your recommendation for each, and the one test. Label estimates as estimates.
