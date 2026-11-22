# Council Q: would an analyst use poc-v118's library? (independent read; read-only; no edits, no model calls)

Alex was asked to read the served library himself for half an hour. His answer (2026-11-20): "dont' you take a look for me let the
council tak ea crack at it". You are the council's independent reader. Claude reads separately and has not shared its view.

## What you are reading
Hivemind keeps a library of investment questions on one company (NVIDIA). Each question is a bet an analyst would track; it has an
answer on a ladder of outcomes (for a number: bands; for an event: Yes/No), the reasoning behind the current answer, the evidence
filed under it (each a one-line summary with a quote and its source article), and its history (one judgement per day it changed).
The system built this library alone from 1,884 news articles, filings and company releases, 2026-07-01..09-20, reading them day by day.
What you read is its state on 2026-09-20, exactly as the page, the API and the MCP serve it.

## Materials (all read-only)
- `docs/research/2026-11-20-production-readiness/council-q/library-pack.md`: the library rendered as text. The list first; then each
  question with its ladder, current answer, latest reasoning, history of answer moves, evidence counts, the evidence the latest
  judgement cites, and a random sample of five uncited evidence items. Rendering only; nothing in it is a verdict.
- The full served JSON: `/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/api-library.json`
  (`views[*].judgements`, `views[*].evidence`, `groups`).
- The source articles: `sqlite3 -readonly poc/data/comparison-2026-11-17/items-comparison.sqlite "select title, publisher,
  publication_day, text from items where input_id = '<input id from the pack>'"`.

## Your task
Read it as a buy-side analyst who covers NVIDIA and is offered this as a daily tool. Do these, in order:
1. **The list.** Are these the bets an analyst covering NVIDIA would hold a card for? What big matter is missing? Which are duplicates
   of one bet, and which are too small to track?
2. **Big number questions.** Read v14 (FY2027 total revenue), v9 (FY2027 Data Center revenue), v5 and v6 (hyperscaler data-center
   capex, CY2026 and CY2027) and v28 (FY2027 gross margin) in full. Is each answer defensible from the evidence it cites? Is the
   arithmetic right and the scope right (which companies, which period, which measure)? Do the answer moves in its history look
   sensible? Of the evidence filed, how much would you actually want, and how much is noise?
3. **Event questions.** Read v4 (Vera Rubin shipping by 2026-12-31) and v34 and v43 (Hugging Face). Does the cited evidence support
   the answer? Open at least two source articles and check the quotes and the reading against them.
4. **Your own pick.** Search the list for China, export controls, gross margin, Blackwell, supply, competition. Does the library hold
   the questions an analyst would ask about them, and are the answers sensible?
5. **Facts.** Check at least eight specific claims (numbers, dates, who said it) against the source articles. Report each: right,
   wrong, or not checkable from the sources.

## Rules
- Judge against the source articles, never against your own memory of NVIDIA: these dates may be past what you know. A claim you can
  check only from memory is "not checked".
- You are a model reader; say so where your judgement of usefulness is a guess about a person's taste.
- Out of scope: the pipeline's internals, prompts, models, measuring rulers, cost, daily updates, the Idea feature. Name what is wrong
  in an analyst's words; do not propose prompt or code changes.

## Output (under 800 words)
First line: **USE**, **PARTLY** or **NO**, and for which job an analyst would use it. Then:
- the most useful point, with one question id as the example;
- the most unsatisfying point, with one question id as the example;
- the list review (missing big bets, duplicates, trivia), with ids;
- each question you read in step 2 and 3: answer defensible or not, and why, in one or two sentences;
- the facts table (claim, source input id, right / wrong / not checkable);
- what would have to change before an analyst used it every day, ranked by how much it matters to that analyst.
