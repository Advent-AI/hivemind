# Closing due questions in the new system's daily loop: design version 3 for the council (rounds 22 to 24), 2026-11-16, $0

**Goal (gate 5, D548: integration).** The new system's store is read by production's page and closed by production's closing
step (`pull.end_of_day`; D54, D356: at the end of a day passed in, every open question whose due day has come is frozen at its
last answer, or closed "no data to verify" if never judged). The copy check (`INTEGRATION-CHECK.md`) showed the closing works on a
new-system store; the new loop does not call it and instead refuses to run past a due day (`ladder_adapter.LadderAdapter.due_day_guard`).
One owner: the closing rule stays in `pull.py`; the new loop calls it in production's order (`replay.py`: the day's items, the
day's judging round, `pull.end_of_day`, `complete_day`). Nothing frozen changes (the base adapter, Step 1, Step 2, the ladder
step, the judge); only `clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py`.

**Found on the way, fixed in production's own loop (same slice, AGENTS §1):** on a day without items, a closing takes its own
sequence, but `replay.py` completed the day at the sequence before it, so the next day's items were shown the closed question as
open (`views_open_at_day_start`). Census: 5 closings by the closing step in 139 stored stores, none on a day without items (0 of
5). Fix: the day is completed at the last sequence it wrote (`store.next_sequence(conn) - 1` after the closing). Test
`tests/test_closing_on_a_day_without_items.py` through `replay.run` failed on the old line at its decisive assertion and passes;
`test_pull`, `test_sequential_replay`, `test_no_seed_replay` pass. The parallel day path runs inside `replay.run` and takes the
same line. Consequence recorded (council round 22): a parallel day's manifest hashes every package `.py` file, so a parallel day
started before this change refuses to resume after it (runtime mismatch); none is unfinished now.

## 1. One owner of the store's sequence (council rounds 22 and 23)

Today the new loop writes each article under its trace article number `k` as the store's sequence. A closing on a day without
articles takes `store.next_sequence(conn)`, which can be the next article's `k`: the two would share a sequence, and the page
dates a sequence by its earliest day (`service.seq_day_map`), so the later article would show on the closing day. **The loop
becomes the one owner:** each article's store sequence is `max(k, store.next_sequence(conn))`, taken when the article starts and
kept in the map `k → seq` (written to the run folder as `sequences.json`). It equals `k`, gaps included (trace article numbers skip
an article Step 1 did not complete, `adapter.trace_articles`), unless a closing on a day without articles took that number or a
later one; then the article moves up past it, and so may later ones, until a gap in the trace numbers lets `max` return to `k`. Every stored run so far has no closing, so each would be written
exactly as before. Where the mapped sequence goes: views opened (`views.created_seq`), evidence, sources, links, same claims and
revisions (the frozen base adapter's `article(k, …)` uses its first argument only as the sequence and is passed the mapped one),
the processing record, the judging round's sequence (the day's last article's mapped sequence), the day's completion and
`leakage_check`. What stays the trace article number: the trace's records, openings, the later-linking log, the article's input
id (`article_inputs`) and `clean_ladders.article_seq` (the source article; no code reads it). **Readers that compare sequences:**
`stored_judgements.not_shown_of` compares a judgement's sequence with link, replacement and revision sequences of the same store,
both store sequences (`views_of` opens one `views.sqlite` for both): no crossing. The page, `day_start_seq` and the closing step
read store sequences only.

## 2. State × event (the new loop, after the change)

| State of a question \ event | A day with articles | A day without articles | Its due day | A link from the trace (an article's own or the later-linking log) | A revision of a statement linked to it | Run ends |
|---|---|---|---|---|---|---|
| Open, never judged | links written; judged in the day's round if changed | nothing; the day completed | judged that day if changed, then closed at the day's end, "no data to verify" if still never judged | written; queued | written; queued | stays open |
| Open, judged | as above | nothing; the day completed | judged if changed, then frozen at its last answer | written; queued | written; queued | stays open |
| Opened already due (its due day on or before its opening day) | opened, linked, judged if changed, closed at that day's end (production's order) | (not opened: openings come with articles) | the same day | written that day | written | closed |
| Closed | **written, not judged** (`store.link` refuses no link; production's round judges open questions only); counted as "links to a closed question" | nothing | not closed again (`pull.end_of_day` closes open questions only) | written, not judged, counted | written, not judged (production's writer does the same, `writing.py`) | closed |
| A theme closed | left out of later theme blocks by production's judging; closing does not by itself queue its dependants | — | — | as for any closed question | as for any closed question | — |

Production's reading step is never shown a closed question, so a direct link to one does not arise there; in the new system it
arises only because Step 1's library does not learn closings (§6). Writing it keeps the fact's home and changes no judgement;
the count shows the size of that upstream gap.

**Days.** The loop walks every calendar day from the first article's day to the run's end day (the last article's day unless an
end day is passed): a day without articles has no article work and no judging round, then the closing and the day's completion
at the last sequence written. A judge store is written new from the first article day each run (`mkdir(exist_ok=False)`), so a
run never starts between article days. **The guard** becomes an invariant checked at each day's start: no open question is due
before that day. It holds by construction (every earlier day ran its closing; a question opened already due is closed at the end
of its opening day); a breach refuses the run.

## 3. Value × reader

| Value written | Readers (searched) | Effect |
|---|---|---|
| `view_switches` closed rows (`pull.close_view`) | `service.is_open_as_of`, `service.views`, `bundle`, `judging.round_of_judgements` (open only), `store.views_open_at_day_start` (production's reading step only), `pull.end_of_day` (no second closing) | the page shows the question closed from its due day; no later judging |
| the closing's processing record on a day without articles (`pull.closing_sequence`) | `service.seq_day_map`, `store.next_sequence` | the closing dated on its day; the next article's sequence after it |
| article sequences from the loop's allocation | every table the loop writes, `service.seq_day_map`, `leakage_check`, the judge's recorded requests (`sent[].seq`) | equal to `k` unless a closing on a day without articles took that number; then higher until a gap lets it return to `k` |
| `days_completed` for every calendar day, at the last sequence written | `service.default_as_of`, `bundle`, `store.day_start_seq` | the page's default day is the run's end day |
| the count of links to closed questions | the run's counts | read by the run's reader |

## 4. New path × old checks

- `leakage_check(day, seq)` takes the day's last mapped sequence; the closing writes none of the tables it reads.
- The extension proof's 19 checks: the fortnight has articles every day and no due day, so every sequence equals `k` and every
  request and judgement must be unchanged.
- The judge's request check (`watching`): a closed question is not itself judged (production's round takes open questions only);
  a request for another question may still show it as a dependency marked closed, as production presents one (`judging.py`).

## 5. Prior decisions

D54, D356 (pull mode freezes at the due day; no final review); D251 (day-start state); D12, D13, D31 (no wall clock; only pull
mode acts on time, with its day passed in); D403 (an event's due day); D426 (the ladder step frozen; untouched); D427 (Step 2
frozen; untouched). No decision bounds closing in the new system; the runner's guard was a stop written when closing was out of
scope ("closing is pull mode's, not run here").

## 6. Not covered, recorded

Step 1's library does not learn that a question closed: it can still file a later fact under that topic; the store links it to
the closed question (written, not judged, counted). Teaching Step 1 closings would change its input, a frozen piece (D387): not
proposed here.

## 7. Proof plan ($0)

1. Tests in `test_ladder_adapter.py`, through `replay` as the runner calls it, on a fixture with: an article day; an article Step 1
   did not complete (a gap in `k`) followed by a completed one; a question due on a day without articles, the closing taking the next completed article's `k`
   (so the collision is exercised); a later article after it; a question due on a day with articles; a never-judged question; a question opened already due; a link from the trace to a
   closed question; a revision of a statement linked to a closed question; a closed theme with an open dependant. Assertions: each
   sequence equal to `k` until the closing, the gap kept; the later article's sequence after the closing's and dated on its own day
   by the page; each question closed on its due day (frozen, or "no data to verify"), the one opened already due closed on its
   opening day; the page before and after each due day; the link and the revision to the closed question written, not judged,
   counted; the day after a closing the round leaves the closed question out; the closed theme absent from the dependant's theme
   block and the dependant not queued by the closing alone; a dependency shown as closed when a judged question depends on a
   closed one. A mutant per rule: no closing; articles written under `k` (the collision); consecutive allocation that ignores `k`
   (the gap lost); days without articles skipped; the day completed before the closing; the invariant removed.
2. The extension proof re-run: 19 of 19, every request and judgement unchanged, every sequence equal to `k`.
3. The decisive replay through the real loop: the extension proof's draw run on to an end day of 2027-04-02 with no further
   articles: the six due questions closed on their own due days at their last answers, `v6` open, no model call; the page on the
   day before and the day of each due day.
