# Steps 3 and 4: compare, then place and merge (design before code, D201)

Alex's three answers (D201): Jev gives an opinion only; the library keeps the source records and, per question, a
research argument that is updated; a new question needs an independent investment judgement. His method: a written
gold first (`gold.md`, 24 cases, 3 held out), one small scope, quantified against a fresh control, every failure traced
to its raw answer and mechanism before any test or change.

Example: NVIDIA tells Tom's Hardware "our roadmap is intact" the day SemiAnalysis reports the Kyber delay (gold G09).
Today the product replaces SemiAnalysis's report with the denial: the contrary report leaves what the judgement reads.
The new path keeps both as sources, records the denial as opposing the report on the Data Center argument, and the
judgement reads an argument that says "delay reported, denied without detail".

## What runs today and what the gold found

Step 3 today: `matching.build_lists` finds up to ten old pieces by word overlap on the linked questions; Jev scores
each incoming piece against them (same_statement / revision / different) and the writer acts on the top score: repeat
(add a source to the old piece), replace (retire the old piece), new (store the piece). Step 4 does not exist: no record
says what a question's argument is, what the new piece added, or whether two pieces are independent; the judgement
reads the flat list of pieces in view (D198).

The gold (`gold.md`) scores the stored product decisions on 24 cases: 14 right, 7 wrong, 3 half. The wrong ones are
one class with two faces: (1) `replace` retired a different statement three times, once a contrary report (G07, G08,
G09); (2) a restatement of a held claim was stored as a new, independent-looking piece four times (G11, G12, G13,
G15). Both come from the same design: the only relation Jev can state is between two pieces, and the writer's only
moves are keep / retire / add. Nothing holds the argument the pieces bear on, so "same claim, new outlet" and "contrary
claim, same topic" have no place to go but "new" or "replace".

## The contract to build and measure

Stage boundaries (numbers as on the review page, `docs/research/2026-10-27-pipeline-review/index.html`, main branch):

| step | owner | input | output |
|---|---|---|---|
| 1 source | extraction v18 (`poc-v34`, D200) | the item | pieces S with quote, one_line, speaker, tier, event_time, links |
| 2a catalog | `research_context.Reader.catalog` (port from main) | object ids, config themes, before_seq | every open question in scope with rungs, key, dependencies |
| 2b expand | `Reader.expand(ids)` | question ids chosen in step 3 | every active piece of those questions with sources, replaced predecessors, latest judgement |
| 3 compare | Jev (`jev-1.14.0`) | S + the pieces of 2b | opinion R: per question {direct, lead, background, unrelated, uncertain}; per old piece {same, revision, different}; each with a score |
| 4 place and merge | gpt-6-luna, one call | S + 2b + R + the question's current argument | update U (below) |
| 5 commit | writer (code) | U + S + the ledger version it read | the source stored immutable; the argument stored as a new version; links; a change list |
| 6 assess | judging (`judging-v5` + argument block) | the argument, its sources, the latest judgement | unchanged contract, new input |

The update U (the closed set the analysis model fills; code enforces the enum and the id references):

```
action:            update_existing | propose_new | background_only | unresolved
question_ids:      ids from the catalog (update_existing / background_only)
same_as:           old piece ids this piece restates (same original source)      -> source added, no new support
revises:           old piece ids whose value or status this piece updates         -> both kept; the argument cites the later
opposes:           old piece ids this piece contradicts                           -> both kept, marked opposing
independent:       true | false, with original_source (who first said it)
new_information:   one sentence, or ""                                            -> "" with same_as nonempty is the duplicate case
argument:          the question's argument, rewritten in full (statement, support ids, opposing ids, limitations)
new_question:      only with propose_new: the candidate as the admission contract requires, plus `independent_judgement`:
                   one sentence saying what view this question carries that no catalog question does
reason:            short
```

Rules the code holds, not the prompt: `replaces` as a writer move no longer exists (D167's replacement becomes
`revises`: both pieces stay, the argument says which is current); `same_as` adds a source to the argument's support
count only when `independent` is true; `propose_new` without `independent_judgement`, or naming a question in
`folds_into`-like relation to an open one, is refused by the writer (Alex's third answer); an id not in the catalog or
the expansion is refused; the argument text is stored as a new version with the version it was read from (one writer).

## State × event

| state | event | written / transition |
|---|---|---|
| piece extracted, not compared | catalog read, Jev answers | R stored with the piece's input id and before_seq; nothing else written |
| R in hand | Jev refuses / HTTP error / malformed | no R; step 4 runs without R (R is an opinion) and says so in `reason`; no retry |
| R in hand | analysis answers U that passes code checks | sources stored; argument version n+1 per touched question; links; change list; all in one transaction |
| R in hand | U refused (bad id, propose_new without judgement, enum) | nothing written; the refusal recorded with the raw answer; the piece stays "not placed" (a counted class, not retried) |
| mid-transaction | crash | the transaction rolls back; the piece is "not compared" again; the archive keeps the answers, so the rerun sends nothing |
| placed | a later piece on the same question | reads argument version n+1; writes n+2; the predecessor is never edited |
| placed | the configuration changes between runs | a new config checksum on the next version; old versions keep theirs |
| placed | two scopes (asset question and a theme question) | one U, both question ids, one argument version each |
| any read | ordering | by dispatch sequence and before_seq only; no wall clock (D12, D13, D31) |
| any | an input corrected and re-sent | a new piece id and a new source record; the old argument version stands as history |

## Value × reader

| value | writer | readers | sources it can come from |
|---|---|---|---|
| R (opinion) | Jev via step 3 | step 4 only; stored for audit | Jev answer; absent on refusal |
| same_as / revises / opposes | step 4 | writer (support count, current value, opposing list), judging (through the argument), UI later | model answer, checked against the expansion ids |
| independent + original_source | step 4 | writer (support count), judging | model answer; the source record's speaker fields are the check |
| argument version | writer from U | judging block (new), library UI (later), the next step 4 call | U.argument |
| new_question + independent_judgement | step 4 | writer (admission contract check), collision judge (D190) | model answer |
| source record | writer from S | everything that reads evidence today (unchanged shape) | extraction v18 |

Every present reader of `evidence`, `evidence_links`, `evidence_sources`, `replacements` keeps working: no row of theirs
changes shape; `replacements` stops gaining rows under the new path (it is read as history).

## New path × old checks

- Judging reads evidence in view (D198): still does; the argument block is added, not substituted, so every D198 test
  passes unchanged; a new test proves the block is present and names the argument version.
- The collision judge (D190) and the shared-quantity rule (D197) run on `propose_new` as before; G21 (merge by key)
  must still merge, and the argument must keep the population label.
- The writer's checks (`matching.check`): ids in scope, no future reads, replacement rules → the replacement rule is
  retired with D167's census re-read; the rest stand.
- Preflight (`scripts/preflight.py`) gains check F: every stored U replayed through the writer's checks; cases judged
  and refused with reasons.

## Prior decisions searched

D62 (no voting across answers: each case one send; three sends measure variance, never vote), D162 ("no new product
data layer": superseded by D201's second answer for the argument record, recorded there), D167/D168 (the writer owns
replacement and succession: replacement becomes `revises`, succession unchanged), D169 (Jev is the matcher: stays, as
the opinion), D190 (collision judge: unchanged), D197 (shared quantity: unchanged), D198 (evidence in view: unchanged,
plus the argument block), D42 (unlinked pieces dropped at extraction: unchanged; the cold-start loss is D199's open
item, not this slice).

## Measurement, small scope first

1. $0 first: the 24 cases' control scores are in `gold.md`. The new path's request for each case is built from stored
   data (S from the handover, 2a/2b from the reader at before_seq) and checked offline: ids resolve, sizes within the
   reader's budgets, enum words present in the prompt (preflight D).
2. One send per case, all 24, Jev then Luna (two concurrent), under a $1.00 cap, no retry, no vote: read every raw
   answer beside its gold row before scoring. Score the exact fields (action, same_as/revises/opposes ids,
   independent, step-3 relations) and read the text fields.
3. A case that fails is traced to its mechanism (the request as the model reads it, the model's own account on the
   stored conversation, D245-style) before any change. One change per arm, tested on the cases that failed plus
   G09 as the regression; the three held-out cases are scored once per arm and never used to pick the change.
4. Three sends on the cases where arm and gold disagree, to tell a flip from a miss.
5. Only when the 24 cases are right does the writer/reader change (steps 5/6) get built, with its own gold: the
   argument the judgement reads for v5 at seq 1085 (Vera) against what it reads today.

Budget: Jev about $0.0004 and Luna about $0.003 per case at the measured request sizes (the Vera run's 39,641 input
tokens is the upper end); 24 cases × one send ≈ $0.10; the full plan under $1.00. Nothing here resumes a long run or
changes a production default.
