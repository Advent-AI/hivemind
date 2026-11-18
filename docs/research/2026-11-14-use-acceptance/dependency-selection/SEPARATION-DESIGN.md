# Design for the council's review: the two uses of a dependency edge, read apart (D538, under D439), 2026-11-15, $0

Status: **closed as a provisional research candidate, not sound for build** (council rounds 30 to 33, D542), on paper, with two
proofs on stored data; not a finished product rule. If the slice is reopened, its review must settle section 7 before any build. Nothing is built, nothing was sent, no
package, configuration or frozen file changed. It does not decide the stored representation, does not change D368's direction,
and does not design the selection call itself (who chooses, what it is shown): those are listed in section 7. Revised after
round 30: the reading of D265 is stated as a proposed interpretation with its cost (2.1); the duplicate and circle rule is
explicit (2.2); rows written before a kind was stored have one versioned reading (2.3); the one-home requirement is stated as
unresolved for questions opened from articles (2.4); the reader table is completed (4); a second proof exercises the production
writers and a whole week (9).

## 1. The defect, in one picture

One stored row, `dependencies(view_id, depends_on, direction, ...)`, has two readers:

| Reader | Where | What it takes the row to mean |
|---|---|---|
| judging | `store.dependencies_of`, `store.dependants_of`, `store.would_cycle` (the request's block, the order of a round, the citations allowed, what a changed conclusion queues, the cycle check) | "this question reads that question's conclusion" |
| filing | `store.direct_parents` → `extraction.narrowest_links` (D265) | "this question is the narrower home: a statement linked to both keeps this one only" |

and two kinds of writer mean different things by it:

| Writer | What the row states | Judging as coded | Filing as coded |
|---|---|---|---|
| a seed file (`seeding.seed_views`; D208: "each driver declaring the root it feeds") | the driver **supports** the root | wrong way: the driver reads the root (D368 item 4; traced 2026-11-03, `../../2026-11-04-filing-end-to-end/core-problem.md`) | right: the driver is the narrower home |
| the matching call for a new question (D51, PRD 06; not asked on the default path today) | the new question **reads** the other's conclusion | right | not stated by the row, yet applied: the reader is treated as the narrower home (`EDGE-PROOF-RESULT.md`: seven statements lose their total-revenue link) |

## 2. The rule

Each edge carries its kind, set by its writer and by nothing else: `supports` or `reads`. Each reader reads one derived relation.

- **Reading relation** (judging): for a `reads` edge (B, A), B reads A's conclusion. For a `supports` edge (D, R), R reads D's.
- **Narrower relation** (filing): for a `supports` edge (D, R), D is the narrower home than R. A `reads` edge states none.

Sources: D368 item 4 ("For filing, the supporting (driver) question is the narrower one ... For judging, the supported (root)
question reads the supporting questions' conclusions ... The fix separates the two uses of the edge"), which speaks of seed
edges; PRD 06 ("B depending on A means B reads A's conclusion"; "A statement about A is A's evidence ... B learns it through A's
conclusion").

### 2.1 What the rule changes in a decision's reading, and what it costs

D265 says: "a statement linked to a question and to a question that question depends on (the ledger's `dependencies`, the seeds'
root-and-driver pairs, transitively) keeps the narrower one only". The rule keeps this for `supports` edges and **does not apply
it to `reads` edges**. That is a proposed interpretation, not something D368 settles: D368 separates the two uses for seed edges
and does not say that a dependency chosen by the matching call has no filing meaning. The council may take the interpretation
under D439; it is recorded as one.

Its cost, measured on the one real case: with the `reads` edge "data-center revenue reads total revenue", the seven statements the
reading step linked to both questions keep both homes, as they do today without any edge. Four of them belong under total revenue
(the company-wide outlook; three sentences holding its own reported figure); three are about the segment's competition and D207's
narrowest home would be data-center revenue alone. So the interpretation preserves the four and leaves the three filed twice.
The literal reading of D265 does the opposite: it moves the three rightly and strips the four wrongly, one of them a statement
a total-revenue judgement cites.

### 2.2 Duplicates and circles, on the reading relation

An edge is proposed with its kind; the writer looks at the reading pair it would add (who would read whom).

| The reading relation already holds | The proposed edge adds | Outcome |
|---|---|---|
| B reads A (from `reads` (B, A)) | B reads A again, the same direction label | a duplicate: not written |
| B reads A (from `reads` (B, A)) | B reads A again, **another direction label** | **a conflict, refused and recorded, never dropped as a duplicate** (PRD 06: "A dependency has one direction"; within one answer the existing check already refuses "same-key dependency direction conflicts") |
| B reads A (from `reads` (B, A)) | A reads B (`reads` (A, B)) | refused as a circle |
| R reads D (from `supports` (D, R)) | D reads R (`reads` (D, R)) | refused as a circle |
| R reads D (from `supports` (D, R)) | R reads D again (`reads` (R, D), any label) | **not resolvable here: returned to the council.** The seed edge's label is `last_end`, written as a constant by the seeding module; no decision, design page, seed file or prompt defines it, so "the same direction" and "a conflicting one" cannot be told apart without inventing its meaning. The proof writes nothing and reports "label undefined" |
| a longer path from the read question back to the reader, through edges of either kind | any edge that closes it | refused as a circle (PRD 06: "Before adding an edge ... code checks for cycles") |

The production writer has the circle check and a duplicate check within one write; the conflict across articles and the handling
of a pair already given by the other kind would be the builder's.

### 2.3 Rows written before a kind was stored

A writer stores the kind when it writes the edge, and a reader never infers it from equal values. For rows already in stored
ledgers there is one versioned reading, by marks (`edge_inventory.py`, `edge-inventory.json`). The package's history shows two
writers of the table (the seeding module, D253; the writer step from a matching answer). What was counted, and no more: the 158
SQLite files under `poc/data` whose name contains "views" (snapshot folders included); 99 hold rows. **1,138** rows carry the
seeding module's marks (sequence 0, direction `last_end`, on a question created from a seed file) and are read as `supports`;
**395** sit on a question opened from an article, at the very article that opened it, with a direction label of the matching
vocabulary (its English form or the earlier Chinese one), and are read as `reads`, the meaning judging has always given them;
none waits for a year; **none** is anything else. The count classes rows by their marks; it does not identify a writer beyond
them and says nothing of a ledger kept elsewhere. A build refuses a row with neither set of marks and no stored kind (it raises
and names the row; exercised), and rewrites no stored ledger.

### 2.4 The one-home requirement: what is represented, and what is left unresolved

A hierarchy between two questions is represented by a `supports` edge and by nothing else; only the seeding module writes one.
For questions opened from articles no decided writer states a hierarchy, with or without this design, so a statement the reading
step links to two such questions keeps both homes. In the fresh week 60 of 385 stored records have more than one home; that
sizes such records and is **not** a count of breaches: D360 itself stores a sentence that gives a figure for each of two
questions as one record linked to both (corrected after the council's round 31).

### 2.5 The filing contract, case by case (`filing_contract.py`, `filing-contract.json`)

Each case: what the reading step linked (from the stored raw answer), what the code's rule leaves with and without a stated
hierarchy between the two questions, and the homes the existing decisions call for. The expected homes are written from the
decisions by hand; no code decides them.

| Case | The reading step linked | No stated hierarchy (today for article-opened questions; a `reads` edge) | A stated hierarchy (a `supports` edge; D265 read literally on a `reads` edge) | Expected, and by which words |
|---|---|---|---|---|
| the company-wide outlook excluding China | both | both: no | data-center only: no | total revenue only. D207: "company-wide figure questions take only their own figures, guidance and management statements" |
| the quarter's total and segment revenue in one sentence (three outlets) | both, as one item | both: yes | data-center only: no | both. D360: "a statement giving a separate figure for each of two questions is written as two evidence items, one under each" |
| a competitor's segment revenue; a customer buying capacity elsewhere; the same customer designing its own chips | both | both: no | data-center only: yes | data-center only. D207, and the frozen link rule: "compare the specific questions before a company-wide revenue or margin question and take that one only" |
| seeded draw: one matter of the driver (the spot price of GPU time) | both | both: no | data-center only: yes | data-center only (D207, D259) |
| seeded draw: the quarter's total and segment revenue in one sentence | both, as one item | both: yes | data-center only: no (the cost PRD 10 §3 records) | both (D360) |
| a two-figure sentence written as two items, one link each (D360's own form; synthetic) | one item under each | both: yes | both: yes | both (D360) |
| the unrelated pair (Hugging Face commitments; financing commitments) | no statement is under both | unchanged | unchanged | n/a |

Five of the ten cases come out as expected under each state, and a different five. **No reading of an edge yields the expected
homes**, because in every real case the reading step wrote one item linked to both questions, and telling the whole's own
statement from a driver's is a judgement about what the statement is, not an identity code can hold (AGENTS §2). Who owns what:

| Decision | Kind | Owner |
|---|---|---|
| which question a statement bears on, and which it measures most directly | judgement | the reading step, under the frozen link rule |
| one item or two for a sentence that holds a figure for each of two questions | judgement | the reading step (D360; its sentence is not in the frozen reading prompt, whose version carrying it failed its test, D361) |
| whether two questions are a driver and its root | identity | the writer of a `supports` edge (the seed file's author today) |
| of two linked questions with a stated hierarchy, keep the narrower | identity, given the hierarchy | code (D265), with the recorded cost when the reading step links the root's own figure to both |
| whether a question reads another's conclusion | judgement | the matching call for a new question (D51); code checks circles, duplicates and conflicts only |

So the contract this design can state for filing is narrow: **a `reads` edge moves no statement; a `supports` edge keeps D265's
rule and its recorded cost; the one home for the cases above is the reading step's to write.** The design adds no rule to make
code produce those homes, and none is proposed here.

### 2.6 The unseeded path: what can happen to a dependency chosen at creation, and who already handles it (round 32)

Today's default holds no seed edge (D370), so only `reads` edges written when a question is created (D51) are in play. For each
event: whether it can occur at creation, what the decisions say, what the code does today, and what exercised it under the
separated reading (`seam_plugin.py` runs the package's own 287 tests with the seam installed; `old_rows_readers.py`).

| Event | At creation? | Decision | Code today | Under the candidate | Exercised |
|---|---|---|---|---|---|
| an edge chosen for a new question | yes | D51, PRD 06 | `matching.check`, then `writing.write` in the article's commit | unchanged; the writer stores `reads` | the whole week (section 9, W2) |
| the answer names a question not shown, itself, or a candidate that is not opened | yes | PRD 06: "Choose only among ..." | `matching.check` refuses; the article is retried once (one attempt on the Jev engine) and then fails, resumable | unchanged | the suite under the seam |
| a circle among the candidates of one answer; conflicting directions between same-key candidates | yes | PRD 06: "Refuse a cycle and ask the model to correct it; persistent cycles follow normal failure handling"; "A dependency has one direction" | `matching.check` and `identity.batch_plan` refuse; the refusal is in the match record | unchanged | the suite under the seam (`test_coalesced_dependency_is_refused_before_matching_retry_ends`) |
| a circle against edges already stored | **yes, in one way** (corrected after round 33): nothing reads a question that is being created, except an existing question that was waiting for it. If the new question names that waiting question as its dependency, binding the waiting edge would close a circle; `resolve_waiting` checks and leaves the edge unbound, without a record | PRD 06, as above | `writing.write` drops the edge with a note in the article's record. **This differs from PRD 06 (refuse and ask for a correction)**; the difference predates this design and can only matter for a later addition | the cycle check walks the reading relation | proofs 1 and 2 (the check itself) |
| a second edge for the same pair at a later article (a duplicate, or another direction) | **no**: only the later addition (D191 point 2, unbuilt) can produce it | "A dependency has one direction"; **what happens to a later conflicting proposal is not written in any decision** | no code path | 2.2 states the outcomes; the conflict's handling is recorded for the council, not decided here | the seam's outcomes (section 9, X) |
| the read question closes, gains a successor, or its awaited year is created | yes | PRD 06's tree (read the closing conclusion; read the successor and judge once; wait and bind) | the request marks "closed" or "historical only"; resolution rows; `resolve_waiting` with the cycle check | unchanged: `reads` rows pass through the same functions | the suite under the seam (the awaited year; resolutions in the bundle and the research context). No test covers "historical only", and no code in the package writes that resolution (the request can print the mark; nothing sets it): PRD 06's branch for a question closed without a successor has a reader and no writer |
| the question named is a theme | yes | PRD 06's own example reads an event question; D195 also shows every theme to every company question | for a company question both are printed: the conclusion appears twice; a theme is not shown the theme block | unchanged (it predates this design) | not exercised. The census holds three theme-to-theme pairs both readers grant (next year's market spending reading this year's, strongly; the two Chinese-permission questions and the U.S. authorization, weakly, both ways) and no company question reading a theme that both grant |
| a crash after the article's commit; a round that dies midway | yes | D63 | the edge is in the commit or absent; a resumed round rebuilds its queue through the dependants | the queue reads the reading relation | the suite under the seam with one fixture's row restated as a chosen dependency: the resume test passes |
| a row written before a kind was stored, read by the pages, the search records and the idea route | n/a | PRD 06 | `service.dependencies` and `service.dependants` read the stored row | for a `reads` row the service shows exactly what the candidate reads | all 399 questions with an edge in the 28 ledgers that hold such rows |

The package's suite under the seam: 285 of 287 pass as they are. The two that do not both write a row by hand with the seed
label at an article's sequence, which neither writer produces: the resume test (it passes once that row is restated as a chosen
dependency: 286) and `test_a_statement_filed_under_a_driver_and_its_root_keeps_the_driver_only`, which holds D265 in its literal
reading over such rows and would state `supports` for them under the candidate.

So on the unseeded path the events that can occur at creation are handled by code the candidate does not touch, and most were
exercised; **not exercised**: a theme named by a company question, a question closed without a successor, and the circle through
an awaited question. The suite under the seam is evidence of compatibility, not a proof of every event; the old rows were read
through the service at one far date, not at every historical day. What the candidate leaves undetermined: the later addition
(its conflict and its cycle handling), and everything that touches a seed edge (the label, 2.2; the seeded pages, where the
service shows the stored direction or, for most seed rows, nothing).

## 3. Table 1: state of a pair by event

"Seq" is dispatch's sequence number of the article (or 0 for a seed file); no cell reads the clock.

| Event | No edge | `reads` edge (B, A) | `supports` edge (D, R) |
|---|---|---|---|
| a question B is created and the matching call names A (D51) | cycle check on the reading relation, then the edge is written with kind `reads` at the article's seq, in the same commit as B (`writing.write` and the "written" record are one commit); B's first judgement that evening reads A's conclusion | the writer's own duplicate check writes nothing twice (a resumed article) | a new B has no edge yet: not reachable |
| a later article names a dependency for an existing question (D191 point 2; decided, unbuilt) | cycle check, then a `reads` edge at that article's seq; the question is judged once in that day's round (its inputs changed, PRD 06) | nothing written | the same pair the other way round: a circle, refused (next row) |
| the proposed edge would close a circle in the reading relation | refused: nothing written, a note in the article's record ("dropped: cycle", as `writing.py` does today); the question opens without it | as left | as left |
| the read question's conclusion changes (its judgement says so) | nothing | B is queued in the same round, after A | D changes: R is queued after D. R changes: D is **not** queued (today it is) |
| the read question closes | nothing | with a successor: a resolution row to the successor, B judged once; without: B reads the closing conclusion marked "historical only" (PRD 06, as today) | R reads D's closing conclusion as "historical only"; seed edges have no successor rule. Unexercised: no stored draw closes a question |
| the awaited year's question is created (a waiting `reads` edge) | nothing | bound by `resolve_waiting` after the cycle check; B judged once (as today) | a seed edge carries no awaited year: not reachable |
| the reading step links one statement to both questions | both links stay (today) | both links stay: the edge states no hierarchy | D's link stays, R's is removed (D265), from the first day whose day-start list holds the edge (its seq at or before the list's) |
| a crash between writing the question and the day's judging; a resume | nothing | the edge is in the article's commit or not at all; a resumed round rebuilds its queue from the committed judgements through the same reading relation (`queued_by_ledger`) | the same |
| a later run on a later day on the same store | nothing | the kind is stored with the edge: read the same under any configuration | the same |
| a row written before a kind was stored (2.3) | nothing | a row at an article's seq, on a question opened from an article, with a matching direction label: `reads`, as judging has always read it | a row with the seeding module's marks: `supports`. A row with neither writer's marks: refused |
| a second edge between the same two questions (2.2) | n/a | the same reading pair again: not written; the opposite pair: a circle, refused | `reads` (R, D), the pair the edge already gives: not written; `reads` (D, R): a circle, refused |
| the reading question closes | nothing | a closed question is not judged (as today); the edge stays as history | the same |
| work in flight when a run ends, a second writer, two objects at once | nothing | only the writer step writes edges, one article at a time in sequence order (`dispatch`); the parallel day prepares requests only | the same |

## 4. Table 2: each value by its readers

Readers found by searching the package for the table and the three store functions.

| Reader | Today | Under the rule |
|---|---|---|
| `judging.topological`, `upstream` (order of a round) | the stored row: the row's question after the question it names | the reading relation |
| `judging.build_prompt` (the block "Current conclusions of the theses it depends on") | the stored row | the reading relation: for a `supports` edge the root is shown its drivers, a driver is not shown its root |
| `judging.check_answer` (`cites_views` may name only what was shown) | the stored row | the reading relation, so the closed set equals what the request showed |
| `judging.queued_by_change`, `queued_by_ledger` | the stored row reversed | the reading relation reversed |
| `store.would_cycle` (`writing.write`, `resolve_waiting`) | walks the stored rows | walks the reading relation, across both kinds |
| `matching.check` and `identity.batch_plan` (dependencies among the candidates of one answer: named only among what was shown, not on itself, no circle, no conflicting direction between same-key candidates) | the candidates' proposed rows | unchanged in what they check: a candidate's chosen dependencies are `reads` edges; the circle among candidates is on the reading relation |
| `extraction.shown_views` → `file_reading` → `narrowest_links` | every row is a hierarchy | the narrower relation: `supports` edges only |
| `writing.resolve_waiting` (awaited years, successors) | rows with waiting fields | unchanged: only `reads` edges carry them |
| `store.views_for_prompt` (a list "with who depends on whom") | no caller in the package or the scripts | must not be revived without reading the kind |
| `service.dependencies`, `service.dependants`, `bundle`, `search` (the result records), `research_context`, and the idea route (`idea.py` walks "upstream" and "downstream" through the service) | read the stored rows as "depends on" and "depended on by" | they expose the meaning, not a label: each must read the reading relation (and show the kind), or the product shows a `supports` edge the wrong way round and the idea route walks it backwards. **Part of any build, not a later step** |
| writers: `seeding.seed_views` (retired from the default by D370; each stored seeded draw holds 17 such rows); `writing.write` from the matching answer (`jev_matching` returns `'dependencies': []` today) | write the row without a kind | each writes its kind: the seeding module `supports`, the matching writer `reads`. Kind is never inferred from equal values (AGENTS §3, Identity) |

The stored unseeded default runs hold no edge at all (the fresh week: 0 rows), so under the rule both relations are empty there
and every request and every filing of today's default is unchanged.

## 5. Table 3: the new reading against the checks the old one passes

| Check | Held by | Under the rule |
|---|---|---|
| today's default: every reading, matching and judging request | the frozen-piece tests; `scripts/preflight.py` | unchanged: no edge exists (section 4) |
| a statement under a driver and its root keeps the driver (`test_a_statement_filed_under_a_driver_and_its_root_keeps_the_driver_only`) | seed-style rows | unchanged for `supports` edges. Its fixture inserts rows by hand: it would state their kind |
| the stored seeded draw's filing | the stored handovers | reproduced: 243 of 243 (section 8, B) |
| a cycle is refused | `store.would_cycle` | refused across both kinds (section 8, C) |
| `cites_views` only names what was shown | `judging.check_answer`, `test_the_request_names_the_closed_set_for_cites_views_when_no_dependency_is_listed` | holds: the same relation feeds the block and the check (section 8, A and B) |
| dependencies are judged first; a dependant reads this round's conclusion | `round_of_judgements` | holds on the reading relation (section 8, A: total revenue before data-center revenue; B: 11 and 13 pairs) |
| a waiting dependency binds when its year's question is created (`test_waiting_dependency_resolves_across_year_spellings`) | `resolve_waiting` | unchanged (`reads` edges only) |
| a question with no evidence in force is not judged, whatever it reads (D59) | `round_of_judgements` (`eligible`) | unchanged |
| every theme reaches every company question without an edge (D191, D195) | the theme block | unchanged |
| the store only appends | the store's triggers | a kind is written with the edge, never updated |
| the judgements of a seeded store | stored requests | **change, by D368 item 4's intent** (a root gains the block, a driver loses it): "it changes judgements, so it is measured before it enters the default". Not built or measured here (D536) |

## 6. Table 4: prior decisions

| Decision | Its words | Here |
|---|---|---|
| D51 (Alex, 2026-10-21) | "dependencies chosen in the matching call"; a question "reads its own evidence and the conclusions (state and reasons) of the views it depends on" | a chosen dependency is a `reads` edge |
| PRD 06, Dependencies | "B depending on A means B reads A's conclusion"; "A statement about A is A's evidence"; "Choose only among searched theses, extraction block-5 theses and candidates opened from the same item"; cycles refused | the reading relation; no hierarchy from a `reads` edge |
| D191 (Alex, 2026-10-26) | themes: "这个 1 to all mapping 比较 make sense"; "A dependency may be added to an existing thesis by a later item (可以)"; "The `feeds` field of the design is withdrawn for themes" | themes need no edge; the later addition is a row of table 1, unbuilt |
| D207 (Alex, 2026-10-28) | "one home, the narrowest question; company-wide figure questions take only their own figures, guidance and management statements" | the narrower relation serves it where a hierarchy is stated; it is not manufactured from a `reads` edge |
| D208 (Alex, 2026-10-28, design) | "each driver declaring the root it feeds through `dependencies`"; "Root judgements read driver and theme conclusions, not their evidence" | a `supports` edge, in both its uses |
| D259 (Alex, 2026-11-02) | "先放款take 吧，辅助反正就是个中间地带我们给点leeway"; the sink "bounded by the narrowest-question rule and the driver questions" | unchanged |
| D260 | the prompt's "a component cannot exceed its whole" | a part reading its whole stays expressible as a `reads` edge |
| D265 (2026-11-02) | "a statement linked to a question and to a question that question depends on (the ledger's `dependencies`, the seeds' root-and-driver pairs, transitively) keeps the narrower one only" | kept for `supports` edges. For a `reads` edge the words "depends on" no longer imply "narrower": the one place this design reads a decision more narrowly than its text; it rests on D368 item 4 and PRD 06, and is put to the council as such |
| D360 (Alex: "go") | "a statement giving a separate figure for each of two questions is written as two evidence items, one under each" | not in the frozen reading prompt (its version failed its test, D361). Under a `supports` edge the root still loses a two-figure sentence (PRD 10 §3: "0–2 of the facts it needs" a draw): unchanged here, listed in section 7 |
| D368 (2026-11-05) | item 2, Alex: "做" (the matching step chooses a new question's dependencies; a later item may add one); item 4, settled by Claude on his delegation ("好你来定"): the two sentences quoted in section 2 | item 4's direction is kept as recorded, not measured (D536); this design is its "fix separates the two uses", extended to chosen edges (D538) |
| D354, D370, D427 | judging, matching and the reading prompt are frozen as they run; preset questions are retired from the default | nothing here changes a frozen piece; a build is a new version the council or Alex opens |
| The independent review of 2026-11-03 (`review-core-codex.md`, point 6) | six contracts a fix must settle: filing's use, cycles across kinds, article-opened questions' edges keeping their meaning, the direction label, citations, the 600-character cut | the first, second, third and fifth are answered by the rule and section 8; the fourth and sixth are open (section 7) |

## 7. What this design leaves open (for the council; nothing here is assumed)

1. **The representation**: a kind on the row, or two tables. The proof derives the kind from the writer's marks for stored
   edges; a build would store it where the edge is written.
2. **The direction label of a `supports` edge when the root reads the driver: a blocker for any seeded build.** Seed rows carry
   `last_end`, outside the matching vocabulary (`first_is_bullish`, `last_is_bullish`, `same`, `opposite`); the request prints
   the label as stored, and what it tells the new reader has not been established.
3. **What the line carries**: the conclusion's first 600 characters and its band, not the implied outcome; a root might get a
   band without the calculation behind it.
4. **A theme named by a `reads` edge** would be shown twice (the theme block and the line). The census found no such pair
   that both readers grant.
5. **The strongest relations of the fresh week are not reachable at creation** (the Rubin shipping questions against the
   revenue questions opened before them). Two decided or possible routes, neither built: the later addition (D191 point 2), or
   letting a new question declare that it supports an existing one, which is D208's sentence for seeds and beyond D51's words
   for article-opened questions. A choice, not assumed here.
6. **The known cost of the narrowest rule under a `supports` edge** (the root's own figure in a sentence that also holds the
   driver's) is unchanged by this design.
7. **The selection itself**: which call is asked, what it is shown (the matching engine already stores a closed relation for
   every compared pair, "part of" among them), its prompt audit and its measurement. A separate design.
8. **D368 item 4's direction** stays recorded and unmeasured; a measurement needs a seeded configuration the default no longer
   runs (D536).
9. **Cells of table 1 no proof exercises**, which a build-ready contract must fill: a `supports` edge whose driver closes, with or
   without a successor (a stored kind affects resolution); the later addition (D191 point 2); a stored ledger with `reads` rows
   read through today's pages (the 395 rows are read here only by their marks).
10. **The one home for the cases of 2.5**: the reading step's, the filing phase's subject (PRD 10); no rule for code is proposed.
11. **Where decisions and code part, or decisions are silent** (2.6): a cycling edge is dropped with a note where PRD 06 says
    refuse and ask for a correction; an awaited edge that would close a circle is left unbound without a record; "historical
    only" has a reader and no writer; no decision says what happens to a later proposal with another direction.
12. **The seed edge's label `last_end`**: undefined anywhere; it blocks both a seeded build (item 2) and the comparison of a
    proposed edge with a `supports` edge in the same reading direction (2.2). Returned to the council; its meaning is not
    invented here.

## 8. The first proof on stored data (`separation_proof.py`, `separated_edges.py`), $0

The seam replaces three functions of the store for the life of the proof (what judging reads, what a change queues, what
filing reads); no package file changes. 35 registered expectations hold; the script exits with an error otherwise.

- **A. The unseeded fresh week with the `reads` edge "data-center revenue reads total revenue".** Every one of the 235 stored
  readings filed again by the production entry point equals the stored filing: the company-wide outlook (`e22`) and the six
  other statements keep their total-revenue home. From the stored state before the last day's round (rebuilt, equal to the
  stored run): total revenue is judged before data-center revenue; the data-center request is the stored one plus the block
  with total revenue's conclusion of that round and the closing sentence; every other judgement equals the stored one, the
  unrelated pair included; the judge's check accepts the citation; the reverse edge is refused as a cycle.
- **B. A stored seeded draw (17 `supports` edges).** Every one of its 243 stored readings filed again equals the stored filing
  (the narrowest rule reads the edges as before). The last day's round, dry with labelled fakes, 14 calls when no conclusion
  changes and 18 when all do: each supporter is judged before the question it supports and shown there; no question is shown
  one it supports.
- **C. Circles across the two kinds**, on the seeded state: a `reads` edge that would let data-center revenue and total revenue
  read each other is refused; one that closes no circle (the Vera CPU question reading the Rubin shipping question) is written,
  ordered before the questions that read it, gives filing no narrower home, and its opposite is then refused.

Positive controls: with the edge read as the code reads it today, 13 expectations fail (the seven filings among them); with
every edge taken as `reads`, 12 fail (the seeded filing, the seeded order, the circle).

This first proof inserts its edges with a helper and derives the kind from the writers' marks; it shows the labelled examples
A, B and C and nothing about a stored kind.

## 9. The second proof (`separation_proof_2.py`), $0: the production writers, a whole week, the edge combinations, old rows

20 registered expectations hold. The two production writers are wrapped so that each stores the kind of the edges it writes
(in a side table on the scratch store); the readers read the stored kind.

- **W1. The seeding module** on an empty store writes 17 edges, each stored as `supports`; filing reads them as the code does
  today for every question; judging reads them the other way.
- **W2. The unseeded fresh week, whole, with one change, and the data-center question's stored answers forced back**: at the
  article that opened the data-center revenue question the matching answer names total revenue as a dependency. The production
  check accepts it and the production writer writes the edge, stored as `reads`. The week then replays from its stored answers:
  every reading and matching answer comes from the archive; questions, statements, the 449 links and all 235 filings equal the
  stored run; every judgement of every other question equals the stored one. The only requests the archive does not hold are
  the data-center question's seven judgements; each is the stored request of that day plus the block with total revenue's
  conclusion of the same round (its first 600 characters) and the closing sentence, with total revenue judged first each day.
  Those seven are answered by handing back the stored answer of the day. **These are not the seven requests a live judge would
  produce**: a changed first answer changes the next day's previous conclusion, the statements carried forward and the change
  flag. A real test would run each arm as a sequence from its own earlier answers; isolated sends of these seven requests would
  answer another question (council round 31).
- **X. The combinations of 2.2** on the seeded state: `reads` (total revenue, data-center revenue) on top of the `supports` edge
  that already gives that reading is not written and is reported as a label that cannot be compared; `reads` (data-center
  revenue, total revenue) is refused as a circle; a `reads` edge that closes no circle is written with its kind, its opposite
  refused, its repeat with the same label not written, the same pair with another label refused as a conflict; filing's
  reading is the same after all of it.
- **M. Old rows**: the inventory of 2.3; a row of neither writer without a stored kind is refused.

Positive controls: with the edge read as the code reads it today the week stops on 2026-09-23 at the first article whose
statement loses its total-revenue link (a matching request the archive does not hold); with duplicates written three
expectations fail; with the writers storing no kind four fail.

What the two proofs do not show: what a judge does with the line (no model was asked); a stored-kind implementation in the
package (the kind lives in a side table of the harness); closing, successors and the later addition; the pages and the idea
route under the rule; anything about how a dependency would be chosen, or any benefit to an answer.
