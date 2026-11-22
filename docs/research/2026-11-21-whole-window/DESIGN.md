# The whole-window measurement of the linking version: design, version 1 (D699; for council review before any send)

Alex chose A (D699, "continue"): measure poc-v119 over the whole release window (2026-07-01..09-20, 1,884 articles) against poc-v118,
the measurement designed with the council at $0 first; the paid send waits for the council's pass and a ceiling Alex names. He was told
the measurement would answer four questions, in his order:
1. over the whole window, do related number questions still contradict each other;
2. which questions did the matching step link, and is any link wrong;
3. does the self-made market reference (the system's own figure presented as the market's, `self-reference/RESULT.md`) become rarer;
4. does any other question get worse.

## 1. The shape: old-2 continued with links

Every request the linking version builds byte-equal to a request old-2 sent is answered with old-2's answer (each sequence works on its
own copy of old-2's archive); only the requests the links change are bought: the link questions (Jev) and the judgements of a question
that reads a linked question. This is the July test's method (`../2026-11-20-production-readiness/dependency-design/TEST-PLAN.md`)
over the whole window.

Why this shape and not an independent forward run:
- **Question 4 is answered by construction and checked by code.** No other request carries a judgement of another question:
  the extraction request shows open questions with their takes lines (`placement.question_lines`, `placement.takes`: key and group
  only); Jev's matching state and thesis text show the question, its ladder and its first two pieces of evidence
  (`jev_matching.candidate_state`, `thesis_text`, `matching.describe_view`); a judgement shows its own evidence, its own previous
  conclusion, the theme block and its dependencies (`judging.build_prompt`). Linking writes only asset-to-asset rows (D695), so a
  changed judgement reaches only the questions that read it. The July test confirmed it: three days, 39 bought calls, every other
  request answered from the archive. The code check: every judgement of a question outside the reading chains is equal, row for row,
  to old-2's.
- **The links' effect is not buried in sampling noise.** A fresh run re-samples 1,884 extractions and about 1,600 judgements; the
  questions opened and their evidence would differ from old-2's for reasons that have nothing to do with links.
- **Cost:** only the readers' judgements and the link questions are bought (section 6), not the ~$9 of a fresh run.

What this shape cannot show, stated with the result (round 13): it is a comparison **conditional on old-2's questions and evidence**;
how the link step behaves on question sets another draw would open (only old-2's openings are asked); a fresh run's cost and timing;
the idea routes (they read judged positions and reasons, `idea.py`, and the daily replay does not call them: outside this measurement).
The equality check compares nine projections (`rebuild_control.compare`), and unrelated judgements are compared by question and day,
since extra reader judgements shift row ids. The archive matches a request by its canonical identity (sorted keys), as production's
archive does.

## 2. The $0 proof that nothing else changes: the `neither` pass

`window_test.py neither`: poc-v119 from an empty ledger over the whole window, every link question answered "neither" by a fake Jev,
every other request from old-2's archive, anything else stops the pass. An answer old-2's own run refused (the archive keeps it under a
`:refused:` suffix, four judge answers) is given back once, so the code refuses it again and the stored retry follows; without that,
the first pass stopped at 07-13 (v7, whose 07-13 judgement was a retry). The pass must end equal to old-2's finished store on views,
keys, rungs, evidence, links, judgements, switches, successions and dependencies (`rebuild_control.compare`), and it lists every
opening with the pairs shown and which are eligible under D695.

Result (`neither.log`, `neither-census.json`; 375 seconds): **equal to old-2 in every table** (43 questions, 5,102 evidence items,
6,306 evidence links, 1,616 judgements, 137 rungs, 44 switches, 2 successions, 0 dependencies; last completed seq 1884 in both); the
four refusals met again and none left unmet. The version asks link questions at **14 openings** (every new number question from v2 at
seq 8 to v36 at seq 1262), **105 eligible pairs** in 14 jobs: each new number question against every earlier open number question of
the company (1, 2, ... 14 pairs; themes and yes/no questions are not eligible, D695). Openings with pairs:

| seq | new question | pairs |
|---|---|---|
| 8 | v2 commitments for customer and cloud-provider guarantees, FY2027 | 1 |
| 49 | v8 stand-alone CPU revenue FY2027 | 2 |
| 62 | v9 Data Center revenue FY2027 | 3 |
| 148 | v14 total revenue FY2027 | 4 |
| 206 | v15 supply commitments, FY2027 report | 5 |
| 265 | v16 total CPU revenue FY2027 | 6 |
| 321 | v17 total revenue growth FY2028 | 7 |
| 534 | v21 total revenue growth FY2027 | 8 |
| 746 | v28 gross margin FY2027 | 9 |
| 821 | v29 equity investment commitments, FY2027 report | 10 |
| 1029 | v32 Poolside licence payment commitment | 11 |
| 1102 | v33 gross margin FY2028 | 12 |
| 1238 | v35 total revenue FY2028 | 13 |
| 1262 | v36 MediaTek convertible-bond investment | 14 |

## 3. Before any judgement is bought: the link decisions over the window

**The July answers were close to a coin flip.** In each linked sequence Jev answered the 07-10 opening of v14 (total revenue FY2027)
against v9 (Data Center FY2027): "v9 reads v14" 0.52, 0.54, 0.51; "v14 reads v9" 0.47, 0.45, 0.48. The rule takes Jev's choice at
0.5 or more (`links.THRESHOLD`), so a shift of 0.02 gives no link or the opposite link. The same opening's v14–v8 (stand-alone CPU)
pair: "v14 reads v8" 0.47, 0.46, 0.44 (below the line), "neither" ~0.40. JULY-RESULT.md reported the link "chosen in 3 of 3" without
these margins; this is added to it.

**Mechanism (prompt audit, `links.READS_CRITERIA`):** "candidate_reads_thesis" covers "a part read against its whole ... or a
quantity read against another it depends on"; for a total against its own segment, both readings fit: the segment is a part of the
total, and the total depends on the segment. D537 names the one sourced case for a new link: Data Center revenue reading total
revenue; PRD 06 line 134 and D368 describe the historical seed arrows and give no rule for a newly chosen link (round 13). Verdict:
**abstract** (the criterion admits both directions for a part against its whole).

**The census** (`window_test.py census`, Jev only): the same whole-window pass with each link job sent to Jev as poc-v119 builds it
and the writer handed no link, so no row is written and every later request stays old-2's (checked by the same equality). Three draws
share one reservation ledger, ceiling $0.10 (Alex, D700; Jev reserved at its published 64K limit for each of its three attempts, as in
July). In draw n the two seq-148 jobs are answered by July's linked-n answers (the same requests, sha 6dcb7664… and d118a387…), not
bought again (round 14); `census-reuse-dry` proved it at $0 (both reused, v9 reads v14 together proposed, complete, equal to old-2,
`census-reuse-dry.log`). Round 15: the July answers are refused unless they are exactly the two pinned requests, and a link job at seq
148 whose request is not pinned stops the pass before the paid transport (`reuse-refusals.log`).
Its $0 checks: `census-dry` (every eligible pair answered "the THESIS reads the CANDIDATE", sign together: 28 jobs, 105 links
proposed, 0 written, equal to old-2 in every table, `census-dry.log`); the mutant (the same fake answers with links written) stops on
07-01 at the first reader judgement, which misses the archive (`census-mutant.log`). Cost: 14 READS jobs of 1 to 14 questions per
draw plus the SIGN jobs of what passes; Jev input at $0.042 per million tokens.
Read for every eligible pair: the answer and its probabilities in each draw; whether the chosen direction and sign are right under
the criterion's own examples; whether the decision is the same in 3 of 3 draws.

**The registered reading (rounds 13–14: a gate needs a known positive, registered before any answer is read):** `expected_links.py`
→ `expected-links.md` / `.json` classes each of the 105 pairs from its scopes and the evidence each question was shown with: **R**,
the known positive only, v9 reads v14 with the sign together (D537's clear case; the criterion's own first example); **W**, any link
wrong: the shown material names no connection (equity investment, licence and convertible-bond amounts against revenue, growth or
margin; two financing amounts of different kinds): 38 pairs; **O**, defensible either way and reported only: 66 pairs (credit support
against revenue or margin, since its shown evidence says NVIDIA earns product revenue and a share of cloud revenue on the supported
capacity and may buy back unsold capacity; supply commitments against revenue, margin or the capacity backstops; CPU parts against
totals far above them; growth against its amount; another period). Round 14 moved the CPU-to-total and credit-support-to-revenue pairs
out of R and W; round 15 moved supply commitments against backstops (206:v2) and credit support against gross margin (746:v1, 746:v2;
the same reasoning moved 1102:v1 and 1102:v2, FY2028 margin) to O. The seq-148 pairs were seen before the
registration (the July answers), disclosed with every score.

**Scoring** (`read_census.py`): it refuses unless given exactly draws 1, 2 and 3, each with a `draw.json` saying it was counted, and
unless every registered pair has a READS answer in every draw. It refuses a draw whose `draw.json` does not say `transport: paid`, so a dry draw cannot be scored as a census draw (round 15). Per
pair and draw: the READS and SIGN answers and the product's decision
(a reading direction at 0.5 or more and a sign of together or opposite at 0.5 or more); R right only with the registered direction and
the sign together, missed with no link, wrong otherwise; W wrong if linked; a margin below 0.10 on a linked or required pair flagged
fragile, not a gate. $0 checks (`scorer-checks.log`): no draws and folders without `draw.json` refused; a missing READS answer
refused; the fake "reads" answers give 114 wrong links and gate FAIL; a control with only the known positive linked passes; the known
positive with the sign opposite, or reversed, fails.

**Gate:** no wrong link in any draw, and the known positive right in every draw. Pass: the paid design goes to its own council round on
the current wording, with the misses, the O links and the fragile pairs disclosed. Fail: the wrong-link class goes to the council; a
wording that fixes the part-and-whole direction changes what the system does and goes to Alex with options and a recommendation before
any judgement is bought. Already known: the known positive's July margins are 0.05, 0.09 and 0.03 (fragile).

**A draw counts only when complete** (`window_test.complete`): its READS answers are exactly the registered pairs, every READS answer
that passed has its SIGN answer, every job was answered, the pass ends equal to old-2 with no link row, and the ledger never stopped
or overran. Mutants on the dry record: a dropped READS answer, a dropped SIGN answer and a failed job are each caught.

**Budget:** each draw registers its launcher with the shared ledger (`claim_launcher`, so the stop gate stops every draw when one
dies); the ledger is created with the ceiling Alex names and the harness refuses any other, a non-finite one, or one above $0.10
(checked: NaN, 0 and 0.2 refused). The store is marked harness-only and held under its lock for the pass. Priced from the dry pass's
28 jobs: the ledger settles a Jev call at three times its reported input (`budget_replay`), so a draw settles about $0.022 at most
(tokens 0.37 of the request's bytes, the larger July ratio; every SIGN job included); three draws $0.066; the largest reservation
$0.0084. The draws run one after another, so the live headroom is one reservation (round 14: $0.066 + $0.0084 = about $0.074 under $0.10); a
budget stop leaves the census incomplete. Preflight over old-2's whole-window archive and ledger (`preflight-window.log`): extraction
1,884 rows replayed, 6,817 statements judged, 69 dropped (as stored); matching 1,277 records judged, 3 refused and 10 skipped: the
three refusals are artefacts of reading the final state (v28 and v14 "already have a successor", v40 "closed": the successions and the
closing came later); the 10 skipped are D197 shared-quantity records the preflight lookup cannot identify (round 15); enum names 46, none missing; 42 keyed open views, no
duplicate key. The `neither` pass, which replays every request with the state of its time, met every request in the archive.

## 4. The paid run (after the census, the council and Alex's ceiling)

- **Linked, three sequences:** poc-v119, each on its own copy of old-2's archive and an empty ledger, the whole window. Jev's link
  answers are not byte-stable (the July probabilities moved by up to 0.03), so the three may choose different links; each is read.
- **Control, three sequences:** poc-v118 on its own archive copy with the judge rows of every reader of the linked sequences (their
  union) retired from the seq of that reader's first link, so their judgements are fresh samples of the same requests old-2 sent.
- **old-2's stored path** is a fourth control path, labelled: v9's self-made reference was found on it, so it is not a neutral draw.
- Order: the three linked sequences first (they decide the readers), then the three controls. One shared reservation ledger under the
  ceiling Alex names; a refused reservation or a stop makes the comparison inconclusive.
- Each sequence uses the comparison runs' budget transport with July's settlement (cache writes at 1.25x), and an allow-list before
  it: a sequence may buy only link questions and the judgements of its readers (linked) or of the retired readers (control); any other
  request that misses the archive stops that sequence (July's latch).

Round 13's points for the paid design's own round (not built yet): pair each control with its linked sequence and retire that
reader's original and retry requests from its first affected judgement, not the union; keep old-2 a labelled baseline outside the
fresh-control mean; run the fresh calls together; report linked-only judgement days apart; record link choices that differ from the
census.

## 5. Reading rule (to be frozen before the paid send)

Round 13's points, to be taken into this rule before its own round: part–whole contradiction only on matching scope and period, a
definite contradiction kept apart from overlapping ranges, a remainder floor only where the evidence establishes it; a sign gives no
bound; a self-made reference traced to an outside statement of the right scope (the text scan clears a figure copied from the linked
forecast); July's arithmetic-and-assumption check kept; rates on common question-pair dates, the three whole trajectories as the
independent repeats, pass, fail and inconclusive defined for zero links and too few dates, and the halving rule checked control
against control.

Per linked pair (reader R reads T), over every day R is judged; scored by Claude first, then by a blind reader under shuffled labels.
- **A, the links:** each link committed in a linked sequence, read with both questions and ladders: right or wrong (relation,
  direction, sign).
- **B, contradiction:** for a part read against its whole, R's implied outcome above T's implied outcome, or leaving less for the rest
  than the reported rest of the latest quarter carried over the remaining quarters (July's rule C generalised); for another relation,
  R's implied outcome on the side of its ladder that T's conclusion and the sign rule out, stated as such in the reasons.
- **C, self-made reference:** `self-reference/reference_census.py`'s three measures on every reader judgement, linked against controls.
- **D, harm:** a reader calling T's forecast a market figure or evidence (grounding error); first-attempt refusals; failed articles;
  any judgement outside the reading chains differing from old-2's (code).
- **Pass line (proposed, for the council):** every committed link right by both readers; B: linked days in contradiction at most half
  the controls' mean, with the controls showing at least two (else "not tested"); C: linked at most the controls' mean; D: no
  grounding error and no failed article in the linked arm, refusals at most the controls' plus two, every other judgement equal to
  old-2's.

## 6. Cost (estimate, to be priced from the census)

Link questions: Jev input at $0.042 per million tokens, July's two jobs cost under $0.001. Reader judgements: old-2's stored v9
judgements cost about $0.003 each at published rates (July's `price`); a reader judged about 70 times over the window, plus the days a
changed T queues it. Priced from the census's readers and old-2's stored judgement tokens before the ceiling question.

## 7. State × event (the harness; the product path's rows are DESIGN.md §6 of the dependency design)

| Event | Outcome |
|---|---|
| a request outside the allow-list misses the archive | the sequence stops (latch), final, reported; the comparison is inconclusive if any sequence stops |
| a request old-2's run refused | its stored answer is given back once; the check refuses it again; the stored retry follows |
| a fresh reader answer is refused twice | the article or the day fails as in the product; the sequence stops; reported |
| a link closes a circle | one correction per link (product path); a persistent circle fails the article: the sequence stops |
| a reservation would pass the ceiling | refused, the ledger stops, every sequence stops: inconclusive |
| a process dies | the sequence is final (never resumed); the reservation stays counted |
| two sequences at once | separate folders and archive copies; one shared ledger under its lock |

## 8. Prior decisions

D694 (A), D695 (number questions only), D696 (reservation from request size), D697/D698 (the July proof and result), D699 (A for the
whole window), D537 (part reads whole) and PRD 06 line 134 (D368/D208: root reads drivers), D677 (no paid work unless Alex funds a run
with a written path to passing: D699 is that funding; this document is the path), D667 (three draws for totals; D431's same-day rule
does not apply: every sequence reads the same stored articles), D449 (a crash stops the run).
