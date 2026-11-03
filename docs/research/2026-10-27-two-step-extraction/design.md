# Two-call extraction: read the article once, then link its statements to the theses

Design v2, 2026-10-27 evening, after a blind review of v1 (17 findings; the 8 blocking ones are resolved below and
named where they changed a row). Nothing built. Alex: "做，先拆两步，深度思考怎么设计" and, after the page cleaning
(main repo D256), "你用我们的新数据库来好好看抽取问题". Numbers come from `census.py` over the cleaned window
`poc/data/items-nvda-2026-07-01-10-27.sqlite` (3,643 fed NVDA items) unless a source is named.

## 1. The problem, measured

One model call reads the page, holds the objects' 16–29 theses and up to 18 research groups in view, and at once
decides which sentences to quote, how to cut them, their tier, which thesis each bears on, whether a candidate opens,
and its groups. On the whole pages of the paused run, byte-identical requests returned 6, 4, 3, 5, 3 pieces on five
sends, and 0, 0 and 2 pieces were present in all five sends of three articles (`../2026-10-27-evidence-gate/
benchmark-results.md`); 363 items the run extracted twice differ by three or more pieces in 87 pairs. The provider
offers no determinism. Medium reasoning does not narrow it (D243 agrees: an analyst prompt and curated reporting-only
text, five sends each, "no overall stability improvement").

The pages are now cleaned (D256: median 44% of a page's characters kept, 4% junk left). The same five-send benchmark
on the cleaned text, same request otherwise (`../2026-10-27-evidence-gate/benchmark-clean-results.md`): 7, 0, 7, 0, 3
pieces for CoreWeave, 11, 8, 11, 3, 2 for Motley Fool, 5, 1, 7, 7, 5 for Rest of World; present in all five sends 0, 1, 0.
The junk was not the mechanism; the task shape is. §8 reads these sends as the control.

Codex's research today measured the half of this design that reads the article in its own call: with a required
answer per paragraph and quotes copied by code, the 18 labelled core claims of three articles were present in all 54
repeat chances (D244) and the record counts per send held (15/15/14, 36/35/38, 40/43/38 against the single call's
5/6/3, 5/10/6, 6/6/8). Routing to theses stayed unstable (links empty in 3 of 5 sends; the same claim to v37, to
nothing, to v6), speaker and time fields varied, and one reference that differed by a hyphen refused a whole answer
(3 of 582 references blocked 63 records; D255). D162 (2026-10-25) was an earlier two-call experiment that failed on
other grounds and barred a new product data layer. This design takes the measured half, keeps the reading inside
the handover row, and makes the second call a closed decision per statement, enforced by the schema.

## 2. The shape

Two model calls per item from extraction version 16 (`SPLIT_FROM = 16`; versions below 16 run exactly as today).

### Segmentation (code, before any call)

A paragraph is one non-blank line of the cleaned text, `p0001 … pNNNN` (four digits; max 1,061 lines in the window).
Sentences inside a paragraph are split at `. ! ?` followed by space and a capital or opening quote, except after a
closed list of abbreviations (U.S., U.K., Inc., Corp., Co., Ltd., Mr., Mrs., Ms., Dr., Jr., Sr., vs., e.g., i.e., No.,
St., Fig., month abbreviations): 553 false splits avoided over 156k sentences. A span never crosses a paragraph; 79
pages (2.2%) hold a sentence broken across lines by the page, which then quotes as two statements (accepted, counted).
A paragraph is mandatory when it holds a digit, a month name or 120+ characters (median 14 per item, p90 32, p99 94,
max 931 in one 10-K). Mandatory paragraphs are grouped into reading chunks of at most 40 (`READ_CHUNK`), in page order,
each chunk carrying every paragraph from its first mandatory one to its last; 256 items need more than one chunk, p99
is 3, the 10-K 24. Every chunk's request is a pure function of the page, the category and the setting.

### Call 1, reading (`read-v16.txt`, purpose `read`, one call per chunk)

In: the category's "what it is" and "what to read out" blocks (`categories-v16.json`), the objects (`[Subjects]`, no
themes, no fiscal note, no ledger), the item header, the chunk's paragraphs as `pNNNN` blocks with `sNN` sentence
lines, and the list of mandatory ids. Nothing from the ledger: the bytes never change for an item, so the archive
answers every later re-extraction at no cost, and the parallel day never sends a reading twice (a shared in-flight
future per request sha; review finding 2).

Out (strict JSON): an object `paragraphs` whose keys are the chunk's mandatory ids, every one required
(`additionalProperties: false`; the provider enforces completeness, review finding 3; at most 40 keys, no enums), and
an array `extra` for statements from non-mandatory paragraphs. A paragraph entry is either `{"statements": [...]}`
with one or more statements or `{"skip": "boilerplate|navigation|repeat|no_claim"}` (an `anyOf` of the two object
shapes; the provider enforces it, and `sift_reading` re-checks it because `model.check_schema` has no `minItems`).
A statement: `first_sentence`, `last_sentence` (pattern `^s\d{2}$`, checked by code against the paragraph),
`one_line`, `speaker`, `original_who`, `original_day`, `tier` (enum), `event_time`: the evidence fields every reader
uses today, nothing new. The quote is `text[first.start:last.end]`, copied by code; the model never retypes a quote,
so "quote not in item" (92 drops in the NVDA ledger) and the punctuation refusals cannot occur. Two statements may
share a span when their speakers differ (D244, D245, D250: "同句不同说话者各留一条"); a same-span statement with the
same speaker is dropped as a repeat. A statement whose sentence ids do not exist or run backward is dropped with a
reason; the rest of the chunk stands (a span check is mechanical, unlike D250's reference check; §6 puts the choice
to Alex). Only a shape the schema cannot express and code refuses (a key outside the chunk, a statement in `extra`
citing a mandatory paragraph) refuses the chunk: `archive.retire`, one re-send, then `extracted` fails.

Statements get ids `e1, e2 …` in page order across chunks. A chunk whose answer is cut off by the output cap is a
provider malformed answer today (`:malformed:`, `SchemaError`, `extraction_failed`); at one statement per mandatory
line a chunk is about 4,200 output tokens including a reasoning allowance, under the lowest cap (8,000 at T7/T8); the
estimate is checked in §8 with the longest pages per category in the trial (review finding 1).

### Call 2, linking (`role-v16.txt`, purpose `extract`)

In: what the current request carries about the ledger (`[Subjects]` with themes and the fiscal note, `[Research
reference]`, `[Existing theses of these objects]`, `[Research groups]`), the item header, and a `[Statements]` block:
one line per statement, `e7 | tier | speaker | original_who | original_day | event_time | one_line | "quote"` (review
finding 12). The page is not re-sent (D162's rule: the second call cannot add facts the first did not read; D46 item
16 and D149 assumed the whole document in view when a candidate is written: here every quoted sentence is in view,
the unread page is not; §6).

Out: today's candidate and group shape (`candidates` with the admission fields, `new_groups`, `group_refs`) without
`evidence_ids`, plus `decisions`: an object whose keys are the statement ids, every one required by the schema, each
`{"links": [...]}` with items matching the pattern of shown thesis ids and this answer's candidate ids (a pattern,
not an enum, so the budget never grows; review finding 10). An empty list means the statement bears on no shown
thesis and opens nothing: dropped with the reason `no thesis`. Code re-checks the key set and refuses a mismatch
(retire; no re-send, the schema already rules it out: review finding 14). `evidence_ids` are derived by code from
the decisions that name a candidate. Then the existing `sift_with_groups` runs unchanged on `{evidence, candidates,
new_groups}`: the link filter, ladder, year, due-day, admission, bounds and group checks as today. The same-quote
merge in `sift` is gated from v16 to merge only when the speakers are equal (§6). The admission enum for v16 is v12's
(`industry_aggregate`), gated explicitly, so the v12 control and the v16 arm share the candidate contract (review
finding 5; `role-v15.txt` has this defect and `poc-v31.json` is not to be run).

### Handover and ledger

`Handover` keeps its positional fields and appends, with defaults, `read_call_ids`, `read_request_sha256s`,
`read_cached`; `cost_usd` sums every call, `cached` is true when all were archived. `round.run` stores
`reading: {statements, skips, dropped}` beside `evidence, candidates, dropped, new_groups` in the same `handovers`
row: the record of what the page was read into, read by `trace_items` and the audit (`proof.py`); no new table
(D162). A linking-only re-send (ledger changed) reuses the archived reading at no cost.

## 3. State × event

| State | Event | Transition and what is written |
|---|---|---|
| Item dispatched, nothing read | every reading chunk answered and checked | statements in memory; linking sent |
| | a chunk answer refused by code (shape the schema cannot express) | retire the row; one re-send; a second refusal → `extracted` failed `extraction_failed`; day resumable; the item's cost so far counted |
| | a chunk's statements partly dropped (bad span, same span same speaker) | dropped entries recorded in `reading.dropped`; the chunk stands |
| | a chunk cut off at the output cap | provider malformed: `:malformed:` row with tokens 0 (an existing defect of `model.call`, noted), `SchemaError`, `extracted` failed; a resume re-sends the same chunk; §8 sizes the chunk so the p99 page fits |
| | malformed / schema (provider) | as today |
| | transport failure | 3 attempts as today; then failed |
| | crash between calls | nothing in the ledger; resume at `extracted` re-runs: readings from the archive ($0), linking sent |
| | an archived chunk that changed code now refuses | retire, re-send once (review note 18) |
| Statements in memory | linking succeeds, keys complete | sift as today; `handovers` row with `reading`; `extracted` ok |
| | linking keys ≠ statement ids (code re-check) | retire; `extracted` failed; no re-send |
| | zero statements and the publisher is not `self` | no linking; empty handover bound to the reading shas; `handed_over` "nothing to match" |
| | zero statements and the publisher is `self` (a memo) | linking still runs: candidates may carry no evidence (PRD 05:36; review note 11) |
| `extracted` ok | resume | the stored handover as today; `reading` ignored by the resume |
| Parallel day, item waiting | a commit changes shown theses or groups | preparation key changes → stale → re-prepared; readings come from the archive or from the in-flight shared future, never sent twice (review finding 2); only the linking is re-sent (today 439 of 1,553 calls were whole re-sends) |
| | two preparations of one item overlap | `model.call` keeps one future per request sha per process; the second caller waits for the first; `insert or ignore` never sees two answers for one sha |
| | its turn, key equal | validate: the prepared answer's reading shas equal the chunks built now and its `request_sha256` equals the linking request rebuilt from the archived readings ($0); zero statements: reading shas only |
| | its turn, answer arrived but the rebuilt linking request differs (ledger changed after preparation) | v16: re-extract at the turn (today's code raises; changed for v16, review finding 2) |
| Any | version < 16 ↔ ≥ 16 between runs | `environment_key` differs; a half-done parallel day refuses; serial finish |
| Any | code or prompt files changed | `runtime_key` differs; same rule as today |
| Any | an input corrected while waiting | `item_key`/text check refuses as today |
| Any | spend cap | checked per committed item as today; in-flight overshoot bound is 2–4 × workers' calls (review note 9) |
| Preflight | stored `read` rows | replayed through `sift_reading`; refusals and drops by reason |
| Preflight | stored v16 `extract` rows | paired with their readings by the statements block; decision keys checked, then `sift` |

## 4. Value × reader

| Value | Writer | Readers, and what changes |
|---|---|---|
| `statements[].quote` (whole sentences) | code, from offsets | `writing.write`, Jev `piece_state` (quote[:600]), `matching.decide` (quote[:300]), judge (quote[:400]), UI: shape unchanged; the cut-offs now meet whole sentences (today quotes are median 171, p90 294 characters; a span of one sentence is similar, two sentences may pass 300: measured in §8) |
| `one_line, speaker, original_who, original_day, tier, event_time` | reading | same readers; `original_day` still falls back to the publication day in the writer and Jev (unchanged, open defect) |
| `statements[].id` | code | linking request, decisions, derived `evidence_ids`, aliases in `sift` |
| `decisions[id].links` | linking | `sift` link filter → `evidence.links` → matching lists, writer links; empty → dropped `no thesis` |
| `candidates[].evidence_ids` | code | `jev_matching.candidate_state`, `sift`, writer: unchanged |
| `handover_json.reading` | `round.run` | `trace_items` (shows it), `proof.py` (audit), `compare_ledgers` (byte compare: fine); preflight C parses by key |
| `Handover.read_*` | `extract` | `parallel_day.accepted_extraction`; `round.run` cost/cached; `round.py:110` and ~25 test sites build `Handover` positionally: new fields come last with defaults |
| archive rows, purpose `read` | `model.call` | `cost_report` (new line); `trace_items.pick_call` (unchanged, picks `extract`; its cost line must add the readings); `preflight` A maps `read` to the reading schema and B replays it |
| `extraction_key` | `parallel_day` | v16: identity of (reading request shas, linking context = the linking request minus its statements block, the schema skeleton); `proof.handover_errors` is extended to rebuild both and compare (review finding 7) |
| `request_for` | `extraction` | callers `parallel_day:47`, `proof.py:60`, tests: v16 adds `requests_for` returning the reading requests and the linking builder; `request_for` keeps its contract for < 16 |
| config `T*-v16` | `poc-v32.json` (next free replay number; `poc-v32-idea.json` is the Idea config, a different kind) | `config._prompt_files` accepts `read-<v>.txt`; the setting's model, effort and output cap serve both calls |
| prompt files | this slice | `runtime_key` changes: the paused run's half day 2026-08-25 is finished with `--workers 1` (already required) |
| `scripts/preflight.py` D | this slice | checks `read-v16.txt` for the tier and skip enums, `role-v16.txt` for the admission reasons (review finding 5) |

## 5. New path × old checks

| Check today | v16 reading | v16 linking |
|---|---|---|
| strict schema at the provider | per-chunk schema (required mandatory keys, anyOf entry, patterns) | per-item schema (required statement keys, link pattern, fold/group patterns) |
| `model.check_schema` locally (no minItems/$ref) | `sift_reading` enforces statements-xor-skip and non-empty statements | code re-checks the key set |
| quote in item; quote ≥ 8 characters | by construction; a one-sentence span is longer than 8 | n/a |
| links to shown ids or kept candidates | n/a | as today on decisions |
| same-quote merge | same span + same speaker dropped at reading | merge only when speakers equal (gated ≥ 16) |
| candidate ladder, quarterly, year, due day, admission, bounds, groups | n/a | unchanged |
| candidate without surviving evidence | n/a | unchanged, derived `evidence_ids` |
| silent drop of a piece whose links died (`extraction.py:520-522`) | n/a | unchanged (named, not this slice) |
| preflight B (`sift` on every `extract` row) | B gains a reading pass | B branches on `decisions` in the answer (a v16 row would otherwise crash at `extraction.py:515`, review note 9) |
| preflight D (enums in `role-*.txt`) | D reads `read-*.txt` for tiers and skips | D reads admission reasons |
| `test_admission`, `test_groups`, `test_keyed_views`, `test_shared_quantity` (v12 transports keyed on schema name) | untouched | untouched |
| `test_concurrency` request identity and audit | v16 tests: stale on a theses change; reused when unchanged; both shas validated; the shared future sends one reading for two preparations; `proof.handover_errors` passes on a v16 day | |
| `test_sequential_replay` | v16: crash between calls resumes with archived readings and one new linking | |
| output budget | chunk ≈ 4,200 tokens at one statement per mandatory line, under 8,000; the trial sends the longest T7, T8 and T6 pages and records tokens and finish reasons | decisions ≈ 12 tokens each |

## 6. Prior decisions

- D37 froze extraction; D42 "One read hands over two things"; PRD 05-extraction :36 "One reading returns …", :156
  "without a separate clustering call". This design makes it a reading and a linking: recorded as D199 in this tree
  with Alex's words ("做，先拆两步"); the PRD sentences change in the same slice. (`poc-v31.json` cites a D199 that was
  never recorded; its note is corrected to "unrecorded draft".)
- D62 "Extraction variance is fixed in the prompt, not by sampling several times"; D193, D243: no sampling, no
  voting. Each call samples once; nothing votes.
- D162: two calls in an isolated experiment; "不增加产品数据层". The reading lives in the handover row.
- D46 item 16 / D149: a candidate is written with the whole document in view. Departure: the linking sees every
  quoted sentence, not the unread page.
- D244 "Three same-quote merges erase distinct summaries"; D245 "相同 quote 不合并"; D250 "同句不同说话者各留一条". Kept:
  same span with different speakers stays; `sift`'s merge is gated. D250 also says "禁止部分通过" and D255 "not
  permission to relax the writer": those govern model-retyped references, which this design removes (code copies the
  quote). Dropping a statement with an impossible span while keeping the chunk is a choice for Alex: the alternative
  is refusing the chunk and re-sending once (D255's amplification class). Lean: drop the statement, count it.
- D44/D155 identity with matching and code: unchanged. D184–D190 admission and collision judge: unchanged (v12 enum).
- D197 shared quantity: the key rule runs on the candidate as today.
- D198: the judge's evidence in view unchanged; its "extraction links wide" defect (`role-v15.txt`) is not folded in.
- D27 whole page: the reading gets the whole cleaned page (D256).
- D181/D183 parallel day: `proof.py` is the audit behind them; extended, not bypassed.

## 7. Prompts

`role-v12.txt` is 7,458 characters. `read-v16.txt` takes "How to write evidence" (one_line, speaker, original
speaker and day, tier) plus the coverage contract (every listed paragraph gets statements or a skip reason; one
claimant per statement; reporter background apart from a quoted claim; no inferred dates; a headline repeated in the
body is a repeat) and drops the quote-copying instruction. `role-v16.txt` keeps the candidate, link, group and identity
sections and replaces "How to write evidence" with the decision rule. Target: both ≤ 8,000 characters together;
measured and reported before the first paid call, with prompt tokens.

## 8. Measurement before any production switch

$0 first: the unit tests above; `scripts/preflight.py` over the production archive is unaffected (no v16 rows).

Control, done: the single call (v12, cleaned text, same request otherwise) sent five times at low on the three
benchmark articles (`../2026-10-27-evidence-gate/benchmark-clean-results.md`, $0.0102); two more run articles get the
same five sends in the trial. The fresh article
(`gnews:a85f1634a6bf9b3ed5fc96aa`, Tom's Hardware, 2026-10-20, 3,667 characters, used by no trial) gets its own five
single-call sends as control and a reference list of statements written before any v16 send (assistant-authored).

Arm: on the same five articles (three benchmark, two more from the run chosen by `measure.py`), five readings each and, on reading 1, five linkings each; plus one reading of the
longest T7, T8 and T6 pages in the window for the output budget (tokens, finish reason). About 60 calls, estimated
under $0.10 at the measured single-call rates (7,055 input / 694 output tokens median); the script reports the actual.

Bars, all computed by `measure.py` on both arms with the same splitter (review finding 6):
- span identity = (paragraph id, first sentence, last sentence); a control piece maps to the span covering its quote;
- reading stability: per article, the share of distinct spans present in all 5 sends and the mean pairwise Jaccard;
  pass when the arm's all-5 share is at least twice the control's and the Jaccard ≥ 0.8 on every article;
- linking stability: on a fixed reading, the share of statements whose link set is identical across the 5 sends;
  reported beside the control's per-piece link agreement (pieces matched by span);
- end to end: the set of (span, links) after `sift` per send, same two numbers, arm against control;
- the fresh article: reference statements present in every reading;
- seconds and tokens per call; the longest pages' finish reasons.
A miss means the mechanism is elsewhere: no prompt rounds on these articles (D255); report and stop.

Then Alex decides: `poc-v32` as the default for the paused run from 2026-08-25 (finish the half day serially).

## 9. Out of scope, named

The evidence gate wording (D198's open defect; next arm on v16); speaker pronouns, time fields that are not times,
invented fiscal anchors (D255's real defects: a later class on the reading prompt); the `original_day` fallback; the
silent drop in `sift`; `model.call` archiving a cut-off answer with tokens 0; further page cleaning (D256 covers the
experiments).
