# Linking related questions: the build design, version 5 (D694, D695; for council review before code)

Alex chose A (D694) and narrowed the first version (D695, "只连数字题"): a link joins a **newly opened number question** and an **open
number question it was shown**, in either reading direction; both are asset questions with five-rung ladders and typed bounds. No
theme, event or same-article pair is linked in this version. A chosen link leaves filing alone (D694 (a)). Version 1 of this document
was reviewed in council R round 4 (`codex-r4.md`, NOT READY), version 2 in round 5 (`codex-r5.md`, NOT READY), version 3 in round 6
(`codex-r6.md`, NOT READY), version 4 in round 7 (`codex-r7.md`, NOT READY); each finding is answered below (§10).

## 0. Versions and entry points

- `poc/config/poc-v119.json`: poc-v118 with `matching.engine` `jev-links` and `rejudging.prompt_version` `judging-v8`; nothing else.
- `poc/config/poc-v120.json` (D705): poc-v119 with `matching.link_questions` `links-v2`, version 2 of the READS and SIGN texts
  (`docs/research/2026-11-21-whole-window/WORDING-V2.md` §5); poc-v119 reads `links-v1` by default and is unchanged.
- `judging-v8.txt` is a byte copy of `judging-v7.txt`; only the code-built dependency block differs (§3). A request with no dependency is
  byte-equal under v7 and v8.
- `config.ENGINES` gains `jev-links`. Every place that tests `engine == 'jev'` (`round._match`, `scripts/replay.py`,
  `parallel_day.ParallelDay`, `budget_replay.py` defaults) treats `jev-links` as Jev; only `round.run` asks the link questions, and only
  under `jev-links`. Existing Jev requests are unchanged (`jev.request_for` holds model, state and questions only).
- **Who may run poc-v119 (an enforced boundary):** only the July harness (`TEST-PLAN.md`). `scripts/replay.py` and
  `budget_replay.py` refuse a configuration whose matching engine is `jev-links` ("not a product entry point in this version"). The
  harness holds `live_lock.acquire` on each sequence's store for the whole run, refuses a store whose last day is unfinished, and never
  resumes a sequence that stopped: a stopped sequence is final and reported as stopped. Each harness ledger is **marked harness-only**
  before the run (a table `harness_only` holding the harness's name and the date), and both ordinary writers refuse it under any
  configuration before routing an item (`scripts/replay.py`'s `refuse_harness_ledger`, called beside `refuse_seeded_ledger`, which
  `budget_replay.py` already calls); read-only inspection stays open. So the serial path's unchecked restarts (a
  sequence reused under another configuration or input, a second writer) cannot reach a v119 store. Making poc-v119 runnable from the
  product entry point is a later decision, with its own restart rules.
- **A store written by poc-v119 opened by poc-v118:** allowed; v118 writes no link, renders a stored link with today's v7 line, and
  filing skips it (filing reads the stored kind, not the configuration). A run is meant to keep one configuration; this is the defined
  outcome if it does not.
- Pins (`tests/test_frozen_questions_and_judgement.py`): the v7 pins stay; added: `judging-v8.txt`'s sha (equal to v7's), the two new
  question builders' output, judging-v8's schema (equal to v7's), and a request-level control: one ledger with a link rendered under v8
  (exact text) and under v7 (today's text), and one without a link, byte-equal under both.

## 1. Where selection runs: after matching has settled what opens

In `round.run`, under `jev-links` only, a new step **after the evidence-only second matching call returns and before the `matched`
success marker**, on the first call's `checked.outcomes` and lists:
1. From `checked.outcomes` take the candidates whose outcome is `new` or `succession`; `identity.batch_plan(handover.candidates,
   checked.outcomes)` gives their aliases; one canonical candidate per stored question. A candidate refused or not opened is not asked.
2. **Eligible pairs:** the canonical candidate C and each open thesis T on C's list (its search list plus the item's shown questions,
   `lists.candidate_lists[C] + shown`, the list its relation questions used), when both are **number questions**: asset kind; a
   measure outside `identity.EVENT_MEASURES` (C's own key, T's stored key); five rungs whose canonical labels run Strongly bullish to
   Strongly bearish or the reverse; a **typed direction** (§5). C's rungs are taken as the writer will store them
   (`writing.oriented_like` for a succession, which may reverse the whole ladder with its labels). A pair outside this set is not
   asked. Same-article pairs are not asked (D695).
3. **Stage 1, one Jev job per C:** state = `candidate_state(C)`; per eligible T the `READS` question (§2) with `thesis_text(T)`.
4. **Stage 2, one Jev job per C with a passing stage-1 answer:** the shared state stays `candidate_state(C)`; per such pair one of two
   sign questions, chosen by the stage-1 direction, each naming in its own instructions which question reads which (§2). One job can
   hold both directions.
5. **The graph check** (§4) on the whole proposed set of the article (every opening candidate's links) plus the stored reading
   relation; candidates are represented by their canonical ids until written.
6. The selection is recorded in a **new append-only table `link_selections`** (id, attempt_id, seq, input_id, config checksum, status,
   record_json). It is not a `match_records` row, so preflight and the trace grouping (which read `call_no`) are untouched; its readers
   are the July test and the tests that pin its shape. Per attempt (`attempt_id` = the article's input id and a counter):
   - **`proposed`**, inserted before the write savepoint, so a failed write does not roll it back (round.run's failure path commits
     the open transaction): every pair shown with its eligibility, each Jev call's call id and request sha, every answer's choice and
     probabilities, each correction with the rejected direction and its path, the links proposed with direction and sign;
   - **`committed`**, in the article's own commit: the rows written, each with its final label;
   - **`failed`**, after the rollback, in the transaction `round._fail` commits (alone, with the partial answers, when a Jev call fails
     before any proposal exists): the reason (persistent circle, write conflict, the
     waiting-row refusal) or, when `jev.ask` raised, the error and the computed request sha of the failing request (from
     `jev.request_for` and `model.request_identity`; a transport failure may leave no archive row), with what had been answered
     before it.
7. `writing.write` gains a keyword-only argument `proposed_links=None` (today's six-argument callers unchanged), carrying the canonical
   endpoints, direction and sign; the write resolves C's new id, computes the label from the stored rungs and writes (§4).

`jev.ask` failures (transport or answer shape) fail the article at the step `matched` as a matching failure does today: resumable, and
a resume re-asks only what the archive lacks.

## 2. The two questions

```
READS (choice), state = CANDIDATE (candidate_state), per THESIS:
 instructions: "Should one of these two questions be judged with the other's current conclusion in view? Use only the supplied text. THESIS:\n" + thesis_text(T)
 "candidate_reads_thesis": "the CANDIDATE should be judged with the THESIS's current conclusion in view, because the THESIS's answer bounds or drives the CANDIDATE's: a part read against its whole (one product line's sales against the company's total sales; one region's loan book against the bank's total loans), or a quantity read against another it depends on (a component supplier's revenue against its largest customer's capital spending; an airline's fuel bill against its fuel volume)"
 "thesis_reads_candidate": "the THESIS should be judged with the CANDIDATE's current conclusion in view, for the same reasons with the roles swapped"
 "neither": "neither answer bounds or drives the other: unrelated quantities (a retailer's gross margin and its store openings in another country), or the same quantity for the same period and scope; sharing a company, industry or topic is not enough"

SIGN, two builders with the same three classes; state = CANDIDATE (candidate_state), per pair:
 when the CANDIDATE reads the THESIS: "If the THESIS's answer turned out higher, which way would that move the CANDIDATE's most likely answer? Use only the supplied text. THESIS:\n" + thesis_text(T)
 when the THESIS reads the CANDIDATE: "If the CANDIDATE's answer turned out higher, which way would that move the THESIS's most likely answer? Use only the supplied text. THESIS:\n" + thesis_text(T)
 "together": "a higher answer to the question read makes a higher answer to the question reading it more likely (a company's total sales and one product line's sales, when that line's share of the total holds steady; a customer's capital spending and its component supplier's revenue)"
 "opposite": "a higher answer to the question read makes a lower answer to the question reading it more likely (an airline's fuel bill and its operating margin; a retailer's markdowns and its gross margin)"
 "no_clear_sign": "the question read only caps the other without moving its most likely answer (a regulator's cap on a bank's fees set far above what it charges), or the supplied text does not show which way it moves it"
```

Sources: PRD 06 ("B depending on A means B reads A's conclusion"; a numeric thesis reading another numeric thesis), D51 (chosen in the
matching step), D537 and council R (a part reads its whole), judging-v7 lines 4 and 9 ("a part cannot exceed its whole"; "consistent
with the conclusions of the theses it depends on"). Every class has an example from another industry (retail, banking, airlines,
components), all number questions of the kind D695 admits; none names a company. Same-quantity-same-period is excluded because such a pair is one question (D248); another period of the
same quantity may be linked. A link with no sign is not written: the existing label vocabulary cannot express it (council R round 2).

**Decision rule (code):** Jev's returned `choice` decides, accepted only when its probability is at least 0.5 (`THRESHOLD`, as every Jev
answer in `jev_matching` is read). Stage 1 `neither` or below 0.5: no link. Stage 2 `no_clear_sign` or below 0.5: no link. Every
outcome is in the selection record.

## 3. What the reader is shown (judging-v8)

```
- v14 (open; first_is_bullish) How much total revenue will NVIDIA report for FY2027?: now rung 3 Neutral, judged 2026-07-12
    Comparison point stated by that judgement: <reference, or "not stated">
    The system's forecast for it (our own judgement, not evidence): <implied_outcome, or "not stated">
    Reasons (excerpt): <reasons, first 600 characters>
```
Indented lines start with four spaces and a word, never "- v" or "[", so neither `evidence_shown_in`, `themes_shown_in` nor a block
header can read them; a value holding line breaks has each continuation line indented by eight spaces, so every physical line stays
inside its block. Not judged yet: "now not judged yet" and nothing more. `store.current_state` also returns `reference` and
`implied_outcome` (no v7 reader prints the whole dictionary). A change of the read question's comparison point alone, with its rung and
`changed` unchanged, reaches the reader at the reader's next judgement, not in the same round (the round queues on `changed`, as for
every dependency today).

## 4. The graph, the circle correction and the writer

- **Graph check (one owner, `links.check_graph`, run at selection and again inside the write savepoint):** the reading relation =
  every stored dependency row (all kinds) read at its **effective target** (`store.dependencies_of`'s `resolved_to`: a bound legacy
  wait counts through the question it is bound to) plus **every proposed link of the article**, the canonical candidates as nodes. Any circle
  in that whole graph is found, including one through two openings and no stored path (C1 → T1 → C2 → T2 → C1).
- **Waiting rows (admission):** under `jev-links` the link step refuses a store holding an unbound waiting row (a `dependencies` row
  with a waited year and no target), failing the article at `matched` with that reason; so no waiting row can bind in the same write
  and close a circle unseen. Product stores hold none (the three poc-v118 draws: 0 dependency rows); a test exercises the refusal.
- **Correction (PRD 06: "Refuse a cycle and ask the model to correct it; persistent cycles follow normal failure handling"):** for each
  proposed link on a circle, one correction request: the stage-1 question for that pair again, its instructions extended with "Reading
  this way would make <R> read itself through <path>; a question cannot read its own conclusion." and the offending direction removed
  from the criteria. Each corrected pair's answer replaces its original; a new direction goes through stage 2; the whole set is
  checked again. The rejected direction and its path are recorded. A circle that remains fails the article at `matched` ("persistent
  cycle"), resumable, as PRD 06 says.
- **Labels (code, §5)** are computed from the rungs as stored, inside the write, after C exists.
- **Writer:** a link C reads T is written in step 2 with C's other dependencies; a link T reads C after C is created. Each row: the
  article's seq, `direction` = the label, `kind = 'reads'`; T, when it is the reader, is added to the article's `changed` set, so the
  day's round judges it after C when T is eligible (open, evidence in force, D59); a new C without evidence in force stays unjudged
  and T reads it as "not judged yet". The plan is re-checked inside the write transaction (the graph, T still open); a mismatch raises
  `WriteConflict` as today (the article fails, resumable).
- **Store:** `dependencies.kind` (text). `ensure_writable_columns` adds it with default `''`; every existing row reads `''`.
- **Filing:** `store.direct_parents` skips `kind = 'reads'` (D694 (a)); rows with `''` narrow exactly as today. `research_context`
  reads dependency rows through an explicit column list (today `select *`), so its output keeps its shape.

## 5. The label

- **Typed direction** of a ladder (`links.typed_direction`): each rung is the interval [lo, hi) of its typed bounds; only the first
  and the last rung may leave one outer end open (None); every inner rung has both bounds with lo < hi; an interval with lo ≥ hi is
  invalid. The ladder runs −1 (values fall) when for every adjacent pair the next rung's hi is not above this rung's lo (touching
  allowed), +1 when for every adjacent pair the next rung's lo is not below this rung's hi; anything else, an open inner end, or a
  missing bound is None. Prose is not read (unlike `matching.ladder_direction`).
- **The favourable end** is the end whose stored label is Strongly bullish (position 1, or position 5 for a successor stored
  reversed). **Asset reader R reading T:** R's favourable end is its high end when that end is where R's values are high. T's end favourable to R: `together` → T's high end if R's favourable end is high, else
  T's low end; `opposite` → the reverse. Label `first_is_bullish` when that end is T's first rung (T's high end is its first rung when
  T's direction is −1), else `last_is_bullish`.
- Worked case (old-2 07-10): R = v9 (direction −1, Strongly bullish first: favourable end high), T = v14 (−1), `together` → T's high
  end = its first rung → `first_is_bullish`. Changing only the sign, only R's direction (its favourable end kept first), or only T's
  direction each gives `last_is_bullish`; R stored reversed with its labels (favourable end last, direction +1) keeps the favourable
  end high and gives `first_is_bullish`.
- Eligibility (§1) already requires both directions decided, so a label is always defined for an asked pair.

## 6. Table 1: state × event (C new in this article, T open and shown)

"Resumable" below is the product path's behaviour; for poc-v119, whose only entry point is the July harness, a stopped sequence is final
(§0).

| Event | Outcome |
|---|---|
| matching settles C as `new`/`succession`; the pair is eligible; READS and SIGN pass | link proposed; graph check; written in C's commit; reader judged in that day's round after the read question, if eligible (D59) |
| READS `neither` / below 0.5; SIGN `no_clear_sign` / below 0.5 | no link; recorded |
| C merges into an existing question, is skipped or not opened, or coalesces with another candidate | not asked, or asked once for the canonical candidate |
| a pair not eligible (theme, event, two-rung, untyped or shuffled bounds, same article) | not asked (D695) |
| a proposed link closes a circle (with stored links, or among the article's own proposals) | one correction request per link on it; a remaining circle fails the article at `matched`, resumable |
| the store holds an unbound waiting row | the link step refuses: the article fails at `matched` with that reason |
| `jev.ask` fails (transport, answer shape) | the article fails at `matched`, resumable; a resume re-asks what the archive lacks |
| the plan no longer fits at write time (T closed in between, a circle) | `WriteConflict`; the article fails, resumable |
| a crash after selection and before the write | resume re-runs matching and selection from the archive (no new send) and writes once |
| a crash after the write | the link is in the article's commit; a resumed day's round rebuilds its queue (`queued_by_ledger`) |
| T's conclusion changes in a round | its reader queued once, after it (`queued_by_change`) |
| T's comparison point changes with `changed=true` | the reader is queued in the same round and sees it |
| T's comparison point changes with `changed=false` | the reader sees it at its next judgement (§3) |
| T closes | the reader keeps reading T's closing conclusion marked "closed" (PRD 06's numeric branch) |
| the reader closes | not judged; the row stays as history |
| a later article shows C and T again | not asked: neither is new (two open questions are a later version) |
| an awaited (waiting) row in the store | this version writes none; the admission rule above refuses a store holding one |
| a second process writing the same store | refused: the harness holds `live_lock.acquire` on each sequence's store for the run, and v119 has no other entry point (§0) |
| a process dies after a provider attempt and before its answer reaches the archive | a death before settlement leaves the reservation counted against the ceiling (`SharedLedger.reserve`); a death after settlement leaves the settled charge counted; the sequence is stopped and final (§0), so no retry is free |
| a version switch between completed days | allowed: the store's links and kinds are read the same by either version (§0); the July test switches from poc-v118 to poc-v119 at 07-10 |
| a restart midway through a day (any configuration or input) | refused for v119: the harness refuses a store whose last day is unfinished and never resumes a stopped sequence (§0) |
| a v118 run on a v119 store | §0 |

## 7. Table 2: value × reader

| Value | Readers |
|---|---|
| `dependencies` row with `kind='reads'` | judging: `topological`, `upstream`, `build_prompt`, `check_answer`, `queued_by_change`, `queued_by_ledger`; `store.would_cycle`, `dependants_of`, `dependencies_of`; `links.check_graph`; the service (`dependencies`, `dependants`), `bundle`, `search` records, `research_context` (explicit columns), the idea route: all read "R depends on T". `store.direct_parents` (filing) skips it. |
| `kind=''` | every reader as today |
| the `link_selections` row | the July test's readers and its shape test; no product reader, not preflight, not the trace |
| T added to `changed` | `round.changed_views_of_day` → `judge_day` |
| `current_state.reference`, `.implied_outcome` | the judging-v8 block only |

## 8. Table 3: new path × old checks

| Check | Under poc-v119 |
|---|---|
| no-link requests byte-equal | proved at $0: poc-v119 over old-2's 07-01..07-09 with the link questions answered by a fixed `neither` transport equals the rebuilt v118 prefix (every other request from the archive) |
| filing under seed-style rows | unchanged (`kind ''`); the existing test stays green |
| filing with a `reads` row | no link removed: re-file old-2's stored readings after seq 148 with the link present (105 shared statements, `filing-exposure.md`) |
| `cites_views` only names shown dependencies | unchanged |
| dependencies judged first | unchanged |
| `matching.check` refusals fail the article | selection runs after it and never adds to its refusals |
| preflight and the trace (read `match_records` by `call_no`) | untouched: the selection is in `link_selections` |
| D59, the theme block | unchanged |
| frozen-piece pins | §0 |

## 9. Table 4: prior decisions

D51, D368 item 2 (the matching step chooses: a Jev question); D191 point 2 (an existing question gains a link when the read question
opens); D695 (number questions only, one new); D207, D265, D694 (a) (a link moves no statement); D260 (the reader sees the comparison
point and the forecast); D248 (same quantity and period is one question); PRD 06 (cycles corrected, then normal failure); D354, D359
(new versions); D542's five items: a circle through a waiting link cannot arise (no waiting link is written), closing as table 1,
theme twice and historical readers not reached (no theme link, no resolution row), `last_end` absent; the unbound-wait admission
rule (§4) as the guard for a waiting circle.

## 10. Round-4 findings and where they are answered

Round 7: 1 ordinary writers refuse a harness ledger: §0. 2 the serial item runner, sequence-bound authorization and post-commit
inspection: `TEST-PLAN.md`. Nonblocking: a Jev failure before any proposal writes `failed` alone (§1 step 6, §11 test 2); crash
accounting wording (§6); "resumable" rows read with §0 for v119.
Round 6: 1 writer and restart boundary: §0, §6. 2 durable selection and failure record: §1 step 6. 3 the July allow-list before
the budget transport, the out-of-pair stop at inspection: `TEST-PLAN.md`. Nonblocking: examples (§2), effective targets (§4), the
admission rule in Table 4 (§9), tests 2, 3 (§11).
Round 5: 1 sign batching: §1 step 4, §2. 2 the whole graph and waits: §4. 3 archive: `TEST-PLAN.md`. 4 placement, interface, record:
§1 steps 6–7. 5 reversed successors, event measures, intervals: §1 step 2, §5. 6 July dry run, extra links, budget: `TEST-PLAN.md`.
7 restart and judging rows: §6. Renderer continuation lines: §3.
Round 4: 1 final identity: §1 steps 1–2. 2 one graph, refusals recorded, PRD 06 correction: §1 step 6, §4. 3 lifecycle and theme boundary:
D695, §6. 4 July harness: `TEST-PLAN.md` (archive, sequences, dry run, unexpected links, budget). 5 question texts: §2. 6 typed
ladders: §5. 7 failure and restart rows: §6. Compatibility (current_state, research_context, mixing, pins, entry points): §0, §3, §4.

## 11. Tests (with the code; each names its row)

1. `typed_direction` and the label: the worked case, its three mirrors, a reversed stored successor, a shuffled middle, touching and
   overlapping bounds, an open inner end, prose-only bounds (None).
2. Selection under `jev-links` with a fake Jev transport: eligibility (theme, two-rung, same-article and merge cases not asked);
   stage 1 and 2 decisions; one sign job holding both reading directions; the canonical candidate asked once; under `jev` no question
   asked (mutant: asked); `link_selections` rows `proposed` then `committed`; `proposed` then `failed` on a write conflict; `failed`
   alone, with the partial answers and the failing request's sha, on a Jev error before any proposal.
3. Graph and correction: a circle with a stored path corrected; the four-link circle through two openings found and corrected; a
   persistent circle fails the article; a store with an unbound waiting row refused; a bound legacy wait passes the admission rule and
   takes part in the circle check through its bound target; no circle written.
4. Writer: T reads C written with `kind='reads'`, T in `changed`; WriteConflict when T closed.
5. Filing: `direct_parents` skips `reads` (mutant: it narrows); seed-style rows narrow (existing test).
6. judging-v8 block exact text, with a multi-line comparison point, forecast and reasons; v7 block byte-equal to today's; no-link
   request byte-equal under v7 and v8; a comparison-point change with `changed=true` queues the reader, with `changed=false` does not.
8. `link_selections` shape pinned; `writing.write`'s existing six-argument callers (`tests/test_identity_repair.py`) unchanged.
7. Entry points: `config.load` accepts `jev-links`; `round._match` and the parallel day treat it as Jev; `scripts/replay.py` and
   `budget_replay.py` refuse it (mutant: they accept it); the v118 CLI pointed at an unfinished harness-only ledger refuses before
   routing any item (mutant: it routes).
