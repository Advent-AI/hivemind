# Council round 43: independent read of a double-count diagnosis (read-only)

You are an independent reviewer for a hedge-fund research pipeline. Work read-only. Read the working rules first: `AGENTS.md`, §1
(diagnose), §2 (design) and §6 (writing prompts). Report in English.

## Background

The pipeline keeps forecast questions ("theses") with five-rung ladders. A model judge re-rates each question from its evidence and
from the conclusions of questions it depends on.
- In a paid pilot of a "linking" version, the total-revenue question (v14) read the stand-alone CPU question (v8). On 4 days it
  added v8's roughly $19.5B forecast on top of a total built from guidance, which moved its rung (D711, H4).
- Alex (the owner) opened the design of a fix (D720).
- Claude then counted the class on stored data and found that the frozen product, with no links, does the same thing through
  evidence filed under total revenue.

## Primary material

- The diagnosis: `docs/research/2026-11-22-whole-and-part/DIAGNOSIS.md`.
- Claude's reflection: `claude-r43.md` in the same folder.
- The candidate lister: `census_candidates.py`, same folder.
- The judge prompt: `src/hivemind/prompts/judging-v7.txt` (frozen product). `judging-v8.txt` has the same text.
- The request builder: `src/hivemind/views/judging.py`, `_lines_english` and `_dependency_lines_full`.
- Stores, read-only; open them with `?mode=ro`:
  - `poc/data/comparison-2026-11-17/run/old-{1,2,3}/prod/views.sqlite`: three draws of the product poc-v118, 07-01..09-20.
  - `/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/linked-1-copy/` and
    `control-1-copy/` (`views.sqlite`, `archive.sqlite`): the pilot arms. Only rows with `call_id > 8737` are fresh; earlier rows copy
    old-2.
  - Tables: `judgements` (`reasons`, `reference`, `implied_outcome`, `rung`, `cited_views_json`, `call_id`, `publication_day`),
    `views`, `rungs`, `evidence`, `evidence_links`, `dependencies`. The archive's `model_calls.request_json` holds each sent request.
- Decisions: `docs/DECISIONS-log.md` D702–D705 (link wording), D711, D719, D720.

## Part 1, before you read `readings-claude.json`: recount independently

For old-1 v4, old-3 v3, old-2 v14 (total revenue), linked-1 v14, v9 and v21 (fresh rows), and the total-CPU questions (old-1 v15,
old-2 v16, old-3 v14, control-1 and linked-1 v16), list every answer that adds a component's forecast or target into a whole's figure
when the basis (consensus, a guided run-rate, reported totals) already contains it. For each, say whether the addition decides the
rung by the answer's own arithmetic. Then compare with `readings-claude.json` and the table in DIAGNOSIS.md §1. Name every
disagreement with its call id and quoted text.

## Part 2: challenge

1. Is the class real and correctly bounded? Specifically:
   - Is the total-CPU sum (stand-alone Vera $20B plus Grace above $5B trailing twelve months) correctly set aside? Read the
     evidence quotes, e.g. old-2 `e2542`, `e897`, `e51`.
   - Is the share uplift correctly excluded?
2. Is the mechanism right? Check the two request sentences quoted in §2 against the full prompt, and look for any other sentence
   that drives the addition (for example "a figure no one states is derived from the accounting identities").
3. Is the judge text the right owner, rather than the link question, the request builder (for example a relation label in the
   dependency block) or filing?
4. Are the two candidate edits sourced and general (AGENTS §6: every company, no NVIDIA wording, cut as much as added)? Propose
   wording if you have better wording.
5. The cheapest proof in §4:
   - Are the cases, the controls, the old-text base rate and three draws enough?
   - What risk does it leave uncovered?
   - What result would stop the line?
6. Anything the diagnosis misses.

## Out of scope

The citation format (stopped by Alex, D719), the link-question wording (D705), the frozen ruler and gold files (never changed), and
modules outside judging. Do not propose building anything before Alex opens a version.

## Output

- A verdict line: DIAGNOSIS HOLDS, or DIAGNOSIS NEEDS CHANGES.
- Your Part 1 table.
- Findings, most serious first, each with the file or call id it rests on.
- Your one recommended next step and its test.
