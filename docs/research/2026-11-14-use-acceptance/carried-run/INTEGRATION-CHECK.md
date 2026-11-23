# Can the product's page server read the new system's library? Not as it is stored (2026-11-16, $0)

**Answer: no. The existing page server, given the new system's stored week (a copy of
`poc/data/clean-lean-week-2026-11-14/week-r2/c1/judge/draw-c1/views.sqlite`), returns an empty library: `/library` → `"views": []`,
`/views?object=NVDA` → `[]`, `/views/v1` → not found, `/days` → no first or last day. Only `/views/v1/history` answers (the
judgements of one question).**

**Why (read in the code):** the product's read side places every question in time through the record of completed days
(`src/hivemind/views/store.py`, `day_start_seq`: "the seq of the last completed day before it, or 0 before the first completed
day"; `bundle.py` lists days from `days_completed`). The new system's store, written by the judging adapter, holds no completed
day (`days_completed`: 0 rows), so every question sits after the cut-off and is hidden.

**What it means:** gate 5 of `NEW-SYSTEM-FRAME.md` (integration with production storage and the pages) is not started, and this
is its first concrete defect: the adapter writes the questions and judgements but not the days. The fix belongs to the writer
(AGENTS §3, one owner: where the data is written). Not changed now: a run is live and no package code is edited while it
runs; and integration is not this step's work (D563). Recorded as an open defect for the integration step.

Server started on port 8791 for this check and stopped after it; the store was a copy.


## The cause, corrected, and the fix (2026-11-16, $0)

**The first diagnosis was incomplete.** On a copy of the fortnight's store, recording the completed days alone made `/days` answer
but left the library empty. The page maps every sequence number to a day through the processing record
(`src/hivemind/service.py`, `seq_day_map`: "sequence number → the publication day of the item or daily round written under it",
read from `processing_steps`), which the new system's store does not hold either (0 rows). With both recorded on the copy (one
processing step per article, its sequence and day; one completed day per day, its last sequence), the page lists all 12 judged
questions with their present answers and details.

**The fix, at the writer** (`clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py`, the judge step of the live clean path):
`LadderAdapter.record_article` writes the article's processing step (`store.mark_step`, step `handed_over`, the day as its time
field: no clock) after its records are written (corrected below); `LadderAdapter.complete_day` writes the day's end (`store.complete_day`) after its round of
judgements. Neither table is read by the judging code or either adapter (searched). The base adapter
(`clean-arch/e2e-2026-11-09/adapter.py`) is frozen with the unseeded measurement (`clean-arch/unseeded-2026-11-10/unseeded-frozen.sha256`;
the runner refuses to start when it changes, which is how the first attempt to put the methods there was caught); it is
unchanged, and its own day loop, which only that measurement's harness uses, does not record them.

**Proved:**
- a test (`test_ladder_adapter.py::test_the_page_can_place_every_judged_view_in_time`): every completed article has its step at its
  own sequence and day, every day its end at its last sequence, and the page's own listing (`service.views`) shows every judged
  view; 28 of 28 tests of the file pass; two mutants on a scratch mirror (no completed day; no processing step) each fail it;
- the extension proof re-run with the change (`extension_proof.py`): 19 of 19, every judge request and every judgement equal to
  the stored week's; the draw it writes holds 235 steps and 7 days, and the page lists its 7 judged questions.

Not yet: the stores already written (the fortnight's draw and earlier ones) do not hold the records; a page over them needs the
draw re-run, or a separate back-fill that would be its own change. Integration as a whole (gate 5) is more than this: the page
was built for the old system's questions and has not been read by anyone over the new system's.


## Every reader of the two records, and the failure states (council round 10; 2026-11-16, $0)

Searched in `src/`, `scripts/` and `clean-arch/` (tests aside). Readers of `processing_steps` and `days_completed`:

| Reader | What it reads | On the new system's store |
|---|---|---|
| `service.py` (`seq_day_map`, `default_as_of`, the day's items), `bundle.py` | sequence → day; the last completed day; the handed-over items of a day | the page: what the records are for |
| `pull.py` (closing at the due day) | sequence → day; `next_sequence` for its own closing records | needed by the closing step, which has never run on a new-system store; without the records it could not place sequences |
| `dispatch.py`, `replay.py`, `parallel_day.py` | `is_processed` (`handed_over` / `ok`), `last_step`, `next_sequence`; resumption | production's own pipeline over its own store; never run on a new-system store. If it were, `handed_over` / `ok` says what is true: the article's statements are written |
| `store.day_start_seq` / `views_open_at_day_start` | the last completed day before a day | production's extraction; not called by the judging code or either adapter (searched) |
| `baseline.py` | steps of the retired coverage-start reading (D370) | not used |

**Order and failure states.** Production marks `handed_over` after an item's records are written and completes a day after its
round (`replay.py`); the writer now does the same (`record_article` moved after `article`). The judge step writes a new store
each time (`output.mkdir(exist_ok=False)`); a crash leaves a partial store that is never resumed: the runner relaunches into a new
folder. In such a partial store the days end at the last day whose round finished, and the page's default day is that one. **Not
tested, and an exception:** when no day has finished (a crash in the first day's round), the page's default day falls back to the
latest judgement's day (`service.default_as_of`) and a judgement committed during that round would show. The conclusion holds
for completed replays only.

**Evidence after the final change:** `proof-output-after-writer-change.txt` (19 of 19; on its draw 235 steps, 7 days, the page
lists 7 of 7 judged views), `mutants-after-writer-change.txt` (control passes; both mutants fail), `full-suite-after-writer-change.txt`
(287 passed); the adapter's own file 28 of 28.

## Production's closing step on a new-system store (2026-11-16, $0, on a copy)

On a copy of the extension proof's store (7 questions; the writer as fixed), `pull.end_of_day(conn, '2027-04-02', last seq)`
closed the six questions due by then (v6, due 2028-03-24, stayed open): each closing record names the frozen band with its label
("due 2027-01-31, frozen on 2027-04-02 at rung 1 Yes"; "... at rung 3 from 775,000,000,000 USD to below 825,000,000,000 USD"),
under a new sequence the closing step recorded as that day's own; no judgement changed. After the day was completed the page's
default day was 2027-04-02 with 1 question open and 7 listed with the closed; as of 2026-10-05 all 7 were open. **Not built:** the
new system's daily loop does not call the closing step (the runner stops judging a question at its due day, `due_day_guard`);
production calls it after each day's round and before completing the day (`replay.py`). **Built and accepted since (D567):**
the new loop calls it in production's order (`CLOSING-DESIGN.md`).
