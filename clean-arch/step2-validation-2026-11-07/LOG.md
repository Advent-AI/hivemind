# Step 2 validation: retrieval and comparison (council loop, from 2026-11-07)

Alex, 2026-11-07: "好开始；我觉得这几次的循环很有效的逼近问题我觉得应该把他写成一个skill 你思考下怎么construct 然后跑这个skill". Run
with the `council-loop` skill (`.claude/skills/council-loop/SKILL.md`). This is a validation of Step 2, not an end-to-end claim:
there is no Step 4.

## 0. Frame

- **Objective.** On stored Step 1 output, measure whether Step 2 finds the earlier statement a new evidence item repeats or revises,
  and whether the comparison labels the pair correctly. Then read what the deduplicated dossier of three investment questions looks
  like.
- **Alex's decided contract (PRD §§5–6, Codex thread [16]–[21], answers on 2026-11-06):**
  - a search engine over the evidence returns the top 10 for {thesis, evidence};
  - the search covers the entity's evidence across theses (choice B);
  - Jev labels each candidate repeat, revision or different;
  - a repeat adds its new source, and any missing thesis link, to the existing record;
  - a revision keeps both records, linked.
- **Proposed pass line (not confirmed by Alex):**
  - retrieval: at least 90% of true repeats and revisions have their earlier counterpart in the top 10;
  - comparison: at least 90% of found true pairs labelled correctly;
  - wrong merges of different parties' statements: at most 2% of comparisons.
- **Reference system.** Production's Step 2: word-overlap ranking within one thesis, top 10 (`views/matching.rank_evidence`), with
  the existing Jev piece question (`views/jev_matching.PIECES`).
- **Ruler.** The frozen golden-v5 does not measure Step 2 (AGENTS §7.1, "what it does not measure"). The pair ground truth built
  here is an exploratory reference by independent readers. It is not a frozen ruler until Alex signs it, and it is labelled as such
  in every result.
- **Data.** The Flash K6b draw-1 forward run over 115 gold articles (`poc/data/clean-step1-takeover-2026-11-07/gold-k6b-flash/`):
  282 kept items with summaries, passages, party, dates, tier and thesis links, in forward order.
- **Out of scope.** Step 3's writer, Step 4, the UI, frozen production files.
- **Budget.** Embeddings (`text-embedding-3-small`) and Jev ($0.042 per M input tokens). Calls and cost are counted before any send.

## 1. Council A (independent design, then one challenge round)

The fresh Codex session is `01a1b870…`; its records are `council/a-handoff.md`, `a-codex.md`, `a-claude.md` and `b-*.md`. Agreed
design:

- **Reference pairs (exploratory, model-authored, labelled as such).**
  - Population: ordered pairs (earlier item, later item) from different articles, with availability set by forward article order.
    Same-article pairs are excluded. An item linked to two theses is one item, queried once per {thesis, evidence} association.
  - Candidate pairs come from routes that do not use the embedding search under test:
    - shared figures;
    - shared parties and named entities;
    - summary-word Jaccard;
    - same-thesis lexical rank.
  - Readers do not see which route found a pair, nor any search or model output.
  - Labels:
    - repeat;
    - revision;
    - same quantity, different party (a subtype of different);
    - different;
    - insufficient information;
    - and, for repeats, whether the later item is richer or qualified (D204's risk).

    Two blind readers label each pair with the same full source context; disagreements are kept, then adjudicated with the source.
- **Generator-miss control.**
  - Sample: 30 incoming items, drawn uniformly within three time strata (articles 1–40, 41–80, 81–115) with a fixed seed. Inclusion
    probabilities are recorded and the estimate weighted.
  - Scan: the reader reads the incoming item's full passages, then every earlier summary.
  - Audit: a random sample of unflagged pairs is re-checked with full context.
  - Expected to be inconclusive if positives are few; expand rather than claim.
- **Retrieval arms.**
  - R0: production as written, word overlap within the linked thesis, top 10; a new thesis has no candidates.
  - R0e: entity-wide word overlap.
  - R1: embedding of summary, verified passages, party, time and period; query of thesis description, outcome and period plus the
    incoming summary and passages; entity-wide; top 10.
  - R2: R1 without the thesis in the query.
  - Strict forward availability throughout.
- **Comparison.** Jev with the cross-thesis wording and full fields, tested first on the labelled pairs, apart from retrieval, then on
  the retrieved candidates. An uncertainty option is open; an uncertain pair is never silently called different.
- **Metrics.**
  - recall at 10 by type and by cross-thesis status;
  - the Jev confusion matrix;
  - false repeats by cause, over true-different and over predicted repeats;
  - the combined path (right target and right label);
  - the dossier per thesis before and after dedup, labelled a simulation.

  The 90% figures are discussion targets until Alex agrees.
- **Open for Alex:** what is saved when one item is a repeat of one candidate and a revision of another, or a repeat of several.

**Dossiers fixed before retrieval** (Flash d1 thesis ids):
1. Customer financing and backstops: clean-1, the revenue-sharing and credit-support model.
2. Competition: clean-18 (custom silicon and AMD) and clean-24 (inference-chip challengers).
3. Product roadmap: clean-11 (Vera Rubin volume shipping) and clean-17 (Kyber).

## 2. Reference (2026-11-07/08)

- **v1** (`reference.json`, kept as history): 573 pairs, from 488 triage-possible pairs, 66 scan-flagged pairs and a 60-pair audit.
  - Two blind readers agreed on 94.9%; a third settled 29 disputes.
  - Readers marked 313 of 397 "repeats" as richer. A hand-check of 6 found 2 that were not repeats.
- **v2** (`reference-v2.json`, council round 1): two fresh readers answered two separate questions, the relation and the material the
  later item adds, over 497 pairs (all v1 positives, 60 sampled negatives, 6 insufficient).
  - Relation agreement 93.4%; 24 of the 33 disputes were between same statement and different fact of the same matter.
  - Result: same_statement 333, different_fact_same_matter 105, revision 25, same quantity other party 8, different 24, insufficient 2.
  - All 60 v1 "repeats" were relabelled as different facts.
  - My hand-read of 18 same_statement pairs: 2 clearly wrong (NVL144 against NVL576), 2 arguable.
- **v3 additions** (`v3-answer-E/F-*`): the 48 never-labelled pairs Jev called repeats on the product path or in the forward
  simulation, two readers.
  - 24 same statement, 17 different fact, 1 other party, 6 disputed.
  - So the reference had missed about half of those pairs, and Jev was wrong on the other half.

## 3. Search: recall at 10 (`score_retrieval_v2.py`, forward simulation)

| Query | Per association, raw history (391) | Deduplicated history | Forward simulation, real Jev decisions |
|---|---|---|---|
| R0, production, within thesis | 82.1% | | |
| R0e, word overlap, entity-wide | 78.5% | | |
| R1, thesis + evidence (agreed) | 90.0% | 125/125 | 112/113 |
| R2, evidence only | 95.9% | 113/113 | |

- Revisions: R1 found 22 of 25.
- Cross-thesis positives: only 3, so no conclusion can be drawn on cross-thesis search.
- The raw-history misses come from many copies of the same story crowding the top 10; merging removes that crowding.
- 112/113 counts only known matches, from one Jev draw.

## 4. Comparison (Jev)

**Pair level on the labelled pairs** (`score_jev.py`):

| Arm | Agreement | Wrong merges |
|---|---|---|
| J0, production question | 82.4% | 30 (9.4%; 14 from one bundle record) |
| J1, cross-thesis wording | 80.8% | 22 (7.5%) |

Pair level is not the verdict. A record is saved or discarded whole, and one true match is enough.

**Product path, per incoming record** (`score_product_path.py`; J0 over the R1 top 10):

| Arm | Merged into a true same statement | No true match | Duplicates kept |
|---|---|---|---|
| J0 | 106 | 6 | 4 |
| J1 | 97 | 2 | 13 |

**Forward simulation** (`forward_sim.py`, J0, article order, the library each decision would see): 282 items become 180 records.
- 102 merged.
- Both loss readers say 93 of those have a true same-statement home. 9 do not: by my read, 3 clear (Sharon AI into Firmus; analysts' 82%
  and 41% into the analysts' revenue-doubling record; NVL576 into NVL144) and 6 arguable.
- 10 cite the incoming source on an extra record that the incoming record does not state.
- 14 true repeats in the results were left unmerged.

## 5. What merging loses (`loss-answer-G/H-*`, all 102 merged items, two readers)

- Both readers say a material fact is lost that no other record holds in 66 of 102 (agreement 93/102). The readers over-flag.
- My hand-read of a random 12 of the 66:
  - 3 material: Q1 net income, EPS and margin; Q2 guidance "±2%, assumes no China data-centre revenue"; the Taiwan raid on Supermicro
    bundled into a Singapore record;
  - 3 moderate;
  - 6 trivial.
- A random 4 of the no-loss items: 4 had no loss.
- This is a small diagnostic sample, not a population estimate.
- **Mechanism:**
  - Step 1 records carry one matter, often several facts.
  - Later articles retell a statement and add figures or qualifications.
  - The current rule keeps only the earlier text and adds the source, so those additions are discarded.

**Probe J2** (`jev-J2-merges.json`, $0.004): same_statement only when the incoming record adds nothing an analyst would keep.
- Merges fell from 102 to 22 on the same 102 merges. This is not a new forward run.
- All 3 material and all 3 moderate losses were kept, but so were 5 of 6 trivial and 3 of 4 no-loss items.
- Jev cannot separate trivial from material additions any better than the readers can, so a materiality gate either loses facts or
  undoes most of the merging.

## 6. Council B (rounds 1–3: `council/c-*`, `d-*`, `e-*`)

- Round 1: re-label with two separate questions, and score per association.
- Round 2: do not claim that search passes or that detection is close. Run a forward simulation and read every merged record against the
  dossier.
- Round 3: grouping preserves text, but has not been shown to be understood by the judge.
  - Say "same statement", not "same story".
  - J2's 22 is not a forward run.
  - Group membership with several matches still needs a rule.

## 7. Verdict and the question for Alex (2026-11-08)

The hypothesis "top-10 search plus Jev repeat/revision/different, then source-only merging" is contradicted on the merge action, so the
line stops (D355).

- Search is not the bottleneck.
- Detection is near but not at the proposed line: 3 to 9 wrong merges in 102, and 14 duplicates in 113.
- Source-only merging discards facts in a noticeable share of merges.

Question for Alex: when a later article repeats a stored statement with more detail, what does the library do?
- **(A) Recommended:** keep the later record's text and source inside the stored record's group. The original is not rewritten, and the
  judge reads the group as one statement.
- **(B)** Merge only exact retellings.
- **(C)** Keep source-only merging.

The proposed pass lines and the conflict rule for several matches are still not confirmed.

**Next test if (A):** build the groups on the forward history, show the judge's input for the three predeclared dossiers before and
after, and check that grouped details are visible and that nothing is counted twice. The Kyber group of 14 retellings is the size case.
Then take the next class: wrong groups and missed repeats.

**Cost:** Jev about $0.19 in all (labelled $0.021, product path $0.116, forward $0.054, J2 $0.004, at the listed rate). Embeddings
earlier. Readers were Codex read-only sessions.

## 8. Log rows

| Arm | Hypothesis | Change | Result | Kept |
|---|---|---|---|---|
| R1 against R0 | An entity-wide embedding finds cross-thesis repeats | Embedding query with thesis + evidence | 90.0% against 82.1% per association; 112/113 in the forward run | yes (agreed design) |
| J1 against J0 | Removing the "same thesis" premise reduces wrong merges | Cross-thesis wording | Fewer wrong merges (2 against 6 per record), more duplicates (13 against 4) | open |
| J2 | A stricter repeat removes the loss | same_statement requires nothing new | Loss removed; merges 102 → 22; trivial retellings kept | no: refuted as a gate; it motivates grouping |

## 9. Alex's decision (2026-11-08)

On the question in §7, Alex replied: "A 继续；跑council loop 开始做". **Decided:** each repeat's own text and source are kept inside the
stored record's group, and the original is not rewritten. Recorded in the clean PRD, §5 repeat handoff and §6. Still not confirmed:
the Step 2 pass lines, and the rule for several matches.

## 10. Grouping round (2026-11-08, council loop)

**Frame.** Alex chose A (§9).
- Goal: build grouping and test whether readers notice what later reports add, without double counting or being misled, compared with
  source-only merging and with no merging (the full-information control).
- No model judge exists (PRD §7), so blind readers act as the dossier's readers.

**Council A** (`council/group/a-*`, `b-*`).
- Agreed:
  - the group contract: the original is never rewritten; members keep their own id, text, fields and source; links carry their
    provenance; revisions are links; a replay is idempotent; one unit per item; distinct articles are counted;
  - the dossier view;
  - three views built from one stored history;
  - a key written by independent readers before any view is read;
  - one view per reader.
- Settled in the challenge:
  - several matches (15 items): kept as their own entry with `also_matches` references in both merged views. This is a **test
    convention only**; the product rule stays Alex's.
  - What was built: the isolated library with only the decided rows, refusing a failed comparison and several targets.

**Built.**
- `clean-arch/step3/library.py`: groups, members, links, revisions, refusals and the dossier text.
- `test_library.py`: 12 tests, one per table row. All 5 mutants were caught (the original rewritten, a replay appended, articles not
  distinct, a failed comparison saved, several targets joined).
- `build_views.py` replays the forward simulation's 282 stored decisions through the library: 195 groups, 0 refused. This is a
  fixed-decision reconstruction, not a new forward run.

**Reader test** (`reader-test/`).
- Questions and scoring rules were frozen first (`FROZEN.sha256`, checked by the scorer): 39 questions over three dossiers.
- Key: two readers; a third settled the 16 questions where the drafts differed.
- 18 masked view readers; 3 blind graders. Tally: `score_reader_test.py`, 234 grades.

| Dossier | Detail: none / source / group (out of 12) | Unsupported claims: none / source / group | Characters: none / source / group |
|---|---|---|---|
| financing | 7.0 / 1.0 / 6.5 | 0 / 4 / 0 | 43.7k / 23.0k / 42.5k |
| competition | 7.5 / 2.0 / 8.0 | 2 / 2 / 2 | 18.1k / 15.2k / 22.5k |
| roadmap | 10.5 / 0.0 / 10.5 | 2 / 0 / 0 | 62.9k / 40.2k / 65.9k |

- Detail in total: none 25, source 3, group 25, out of 36.
- Double counting: 0 in every view, on 4 independence questions.
- Controls, comparison and independence scores are about equal; group is slightly ahead on comparison (9 against 8 against 6).
- No frozen falsifier fired. Detail: group trails none in financing by 0.25 question per reader, under the 1-question threshold. The
  wrong-group questions scored the same in every view.

**Traces read.**
- C3: group readers saw both Lisa Su accounts, but read the ambiguous sentence as covering MI450 only. That is a judgement point, not a
  missed detail.
- R5: group readers put "orders" and "sales" side by side, while none readers added an inferred year.
- F1 is partial everywhere because grading was strict.

**Council B** (`council/group/c-*`).
- The test supports preserving later text. It does not prove equivalence with no merging, overall dossier quality (the questions were
  chosen for added details), or wrong-group safety (the questions pointed readers at the facts).
- Size is about no merging, up to 25% more in competition: groups bring members whose own links point elsewhere. Grouping gives
  structure, not compression.
- Next class: wrong groups.

**Wrong-group census ($0; the 9 no-home merges, read against exactly what Jev saw):**
- M2, Sharon AI into Firmus: the incoming record's quote is the whole paragraph, Firmus sentence included, so Jev matched on the quote.
  Step 1 bundle on the incoming side.
- M57, NVL576 into NVL144: the stored record's own summary also states the NVL576 claim, so the merge is defensible. Step 1 bundle on
  the stored side.
- M30, analysts' 82% and 41% into the analysts' revenue path: different figures. A Jev error.
- 6 arguable (the same announcement, the same figure, or a relayed report): under grouping both texts sit side by side.
- So 2 real wrong groups out of 102, and their texts survive.

**Open for Alex:**
- the several-match rule (pending, best match, or own entry with references);
- the Step 2 pass lines.

## 11. Log rows

| Arm | Hypothesis | Change | Result | Kept |
|---|---|---|---|---|
| Grouping (A) | Keeping each repeat's text keeps added details noticeable without double counting | Isolated library and group view | Detail 25/36, the same as no merging, against 3/36 source-only; 0 double counting; size about the same as no merging | yes (Alex's decision; tested) |

## 12. Close-out (2026-11-08)

**Alex's decisions (2026-11-08):**
- a record that is a repeat of several groups joins only the one Jev judges it most like (the highest same_statement probability; ties
  go to the earliest group);
- the Step 2 lines: (1) search at least 90%; (2) clear wrong merges at most 2%; (3) grouped dossiers keep no fewer later details than
  no merging.

Both are recorded in PRD §5.

**Built.**
- `clean-arch/step2/compare.py`: search, Jev comparison, the outcome with best match, forward order, and a failed comparison refused and
  reported. `test_compare.py`: 6 tests; all 4 mutants caught.
- `run_forward.py` reads a stored Step 1 trace directly.
- **Run** (`poc/data/clean-step2-forward-2026-11-08/`, a fresh Jev draw): 282 records made 178 groups.
  - 104 repeats, 3 revisions, 0 refused; 16 records had several same_statement answers.
  - The cached embedding texts were verified identical: 282 of 282 documents, 313 of 313 queries.

**Council A** (`council/group/d-*`):
- report search as recall over known labelled counterparts;
- blind-review every merge, previously labelled positives included;
- verify the cache texts;
- re-run the reader test on the new views.

| Line | Result | Met |
|---|---|---|
| 1. Search | 112/113 known labelled counterparts had a holding group among the candidates (99.1%). For 107 of them the group's original, which is what Jev saw, is itself a counterpart. This is not recall over all real repeats. | yes |
| 2. Clear wrong merges | 104 merges read by two blind readers; 85 accepted by both; the 19 rejected by either went to a third reader: acceptable 1, overlap 15, **wrong 3** = 2.9% | **no** (missed by one merge) |
| 3. Later details | Reader test re-run on the rebuilt views with the frozen questions and key: detail none 27.5, source 3, group **28** of 36; unsupported claims 3 / 2 / 2; double counting 0 | yes |

**Line 2 detail.**
- The 3 wrong merges:
  - NVL576 into the NVL144 group, twice. The group's original Step 1 record states both claims.
  - Analysts' 82% and 41% growth into the analysts' revenue-path record: different figures, a Jev error.
- 15 overlaps, which the third reader called imperfect but not misleading to a reader of the record's own text. Among them:
  - orders against sales ($1tn);
  - expected revenue against committed off-take (Firmus);
  - bundled records: the business model into the Sharon group, the Kyber delay report into the backup-rack group, the Taiwan raid
    alongside the Singapore mansion.
- My own reading had 5 wrong (Sharon AI into Firmus, and the business-model bundle into the Sharon group, both overlap to the third
  reader). Both readings miss the line.

**Council B** (`council/group/e-*`):
- do not offer the result as a pass;
- report 3 wrong, 15 overlap and 1 acceptable after dispute;
- a later look at bundled records would explain only part of it;
- stop and report.

**Verdict.** Step 2 meets lines 1 and 3 and misses line 2 by one merge, in one Jev draw. Per Alex's instruction, the work stops here,
and the census goes to him.

**Not done:** the unprompted wrong-group reading test, and a fix for line 2.
