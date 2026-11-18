# Step 2 validation: retrieval and comparison (council loop, from 2026-11-07)

**Status (2026-11-11): closed and frozen (D427, §19).** The open defects carried with it are in §17.

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

## 13. Embedding score to Jev: interrupted exploratory probe (2026-11-09)

Alex asked whether giving Jev the retrieval similarity score helps and authorized a small council test. The frozen candidate lists were
replayed in an isolated probe, comparing the original Jev request with one adding the real cosine scores and query-type labels. This
is not a production change or a new acceptance measurement. The [design, source-backed blind reviews and full result](../../reports/step2-score-council-2026-11-08/RESULTS.md)
remain separate from the Step 1 work.

- The planned sample was 11 selected cases, 3 same-day sends per arm. **36 of 66 calls completed:** 6 cases; the next request ended
  in a connection reset after dispatch and its outcome is unknown. The remaining 29 calls were not sent. The predeclared stop held;
  no automatic resend or resume occurred.
- On the six completed cases, all 46 candidate choices, the selected groups and revision links were the same in both arms, in all
  draws. Two blind readers agreed on all 46: 3 same, 42 different and 1 overlap. The overlap was grouped as a repeat in both arms;
  it is not treated as an unambiguously correct or incorrect merge. The score changed some returned probabilities, not decisions.
- The known wrong merge and the selected revision-bearing case were not reached. **No decision improvement was observed, but the
  interrupted, selected sample cannot establish equivalence, precision, recall or revision quality.** The effect of scores remains
  unresolved; neither the prompt nor the configuration was changed. Recorded successful call cost was $0.005742; billing for the
  interrupted request is unknown.

## 14. Jev revision-target procedure: failed isolated probe (2026-11-09)

Alex asked the Codex–Claude council to select and execute the next small Step 2 test. The candidate asked Jev to identify the statement addressed before applying the existing revision definition, preserving the three existing choices. A full-request audit, blind second read and isolated-sender review preceded the send. Seven archived full-candidate requests were sent under the original and candidate criteria three times each: 42/42 completed. In the predeclared wrong-revision controls, the original and candidate both kept the C036 backup and interconnect links in all three draws; C057's target left revision once in the candidate, below the required two-draw advantage, and its new `same_statement` answer was not supported by the two source readers. The selected correct revision and repeat controls retained their labels in all draws. The predeclared improvement condition failed; **do not adopt this candidate or tune another variant on these cases**. The remaining source disputes, particularly C059, are not silently resolved. This selected small probe does not measure overall precision, recall or final investment judgment.

Reported input: 200,067 tokens (original 99,918; candidate 100,149). The dated repository Jev rate gives an estimated $0.0084, not an invoice; conservative reservation was $0.0739053. V108 preflight included 2 historical schema refusals and 2 skipped matching rows and did not exercise clean Step 2; the clean Jev request bytes and archived answers were separately verified. No production prompt, frozen ruler or runtime dataset changed. The [protocol, raw results, independent source review and council exchange](../../reports/step2-next-action-2026-11-09/) are retained with the event journal.

## 15. One unsupported revision relation traced to the judge (2026-11-10)

Alex handed the Step 2 work over with the council's conclusion of 2026-11-09 (stop tuning Jev's wording; test whether one wrong
relation changes a later judgement). The test was carried out as that council wrote it. [Result](../step2-edge-effect-2026-11-10/RESULT.md),
[protocol](../step2-edge-effect-2026-11-10/PROTOCOL.md). No change to Jev, a prompt, a rule, the frozen judge or a saved run.

**Frame.** Saved D392 clean draw 1, judged by the frozen judge through the experimental adapter. The case: an NVIDIA spokesperson's
"Our roadmap is intact" (record `70:e4`), an answer to a report that the Kyber rack is delayed, read by Jev as a later version of
"NVIDIA plans to sell more racks of the existing form" (`69:e5`). The adapter gives a record the question links of the record it
revises, so the Kyber answer was shown under the FY2027 Blackwell and Rubin revenue question (v20).

**At no cost** (`edge_replay.py`, every request answered from the saved archive):
- The untouched run replays: 239 of 239 judge requests equal a saved one; ledger, recorded requests and counts equal the saved run's.
- With that one relation removed, the first changed request is v20's on 2026-07-06: the Kyber answer is gone, nothing else.
- With the relation removed and its link kept, all 14 days are identical: this relation reaches the judge only through the link.
- The class (`inheritance_census.py`): links that exist only because a revision relation carried them are 5 of 700 in draw 1, 11
  of 725 and 8 of 730 in draws 2 and 3 (relations of every kind). By the readers' labels of draw 1: 2 of the 5 come from relations
  that join different statements, 1 from an unclear one, 2 from repeats. A relation also prints one "later version" line under
  the new record: 6 records carry a line from a relation the readers call different, 4 of them shown to the judge (55 of 4,575
  showings); the saved reasons use those statements for what they say and never as a later version of the piece named.
- Step 1 never filed the roadmap statement under v20 (0 of 28 copies in three draws); a blind reader of the article placed it as
  context that should not move the FY2027 estimate.

**Paid, $0.0126:** v20's request of 2026-07-06 sent as saved and with the record removed, three times each, after four read-only
sender reviews (none ended "ready"; each serious finding and what was done is in the protocol; sent on my reading). The reading
rule was fixed before the send.

| Arm | Rungs | Implied revenue | The Kyber answer |
|---|---|---|---|
| As saved | 2, 2, 2 | about $335, $330 and $340 billion | cited and marked as pushing up in all three; not used in the reasons |
| Record removed | 2, 2, 2 | about $340, $350 to $370 and $335 billion | absent |

By the rule: no difference in the conclusion in these samples. All six answers give the same cause for the move from rung 3 to
rung 2 that day: the Data Center question it depends on had moved to about $390 billion.

**Council on the result** (`council/result-challenge-codex.md`): agrees with leaving Jev unchanged; the defect stays open, and the
size is given by the labelled counts, not by "about 1%".

**Verdict.** The relation changed what the judge read on one question and not what it concluded there. It is one case and one day
of one draw; it does not show the record had no influence, and it says nothing of the other relations or the later days.

**Recommendation to Alex.** Stop work on Jev's revision relation now and keep the defect open with these counts; no change to
Step 2 or the adapter. The clean PRD's §6 does not say a revision gives the new record the earlier record's thesis links (the rule
is the adapter's, from production's writer); that is a product rule to put to him when Steps 3 and 4 are joined.

| Arm | Hypothesis | Change | Result | Kept |
|---|---|---|---|---|
| Relation removed (one case) | An unsupported revision relation changes a later judgement | The one relation taken out of a copy of the library; v20's request of 2026-07-06 sent both ways, 3 times each | Input changed (one record under one question); rung 2 in 6 of 6; the cause given unchanged | no change made; Jev's revision relation stays an open defect |

## 16. What a "later version" relation may file: a council round, and a withdrawn fix (2026-11-10)

Alex, on §15's recommendation and its open point: "okay take your suggestion what is the fix and how to measure get your council
skill ready to propose" (D423). The round is in [its own log](../step2-revision-links-2026-11-10/LOG.md). No code of the writer, no PRD
rule and no test changed.

- **Census, three saved draws:** the rule wrote 24 links (5 of 700, 11 of 725, 8 of 730). Nineteen are NVIDIA's answer to the Kyber
  report carried to revenue questions (10) and the Rubin shipping question (9); three belong to records Step 1 filed under a thesis
  the seeded test does not judge; two to records Step 1 filed nowhere.
- **Exact:** the writer's own code with judging off reproduces the three saved ledgers row for row; "never carry" leaves out exactly
  those 24 links and changes no other row.
- **Two blind reader families, with controls of both kinds:** 19 context by both, 3 evidence by both, 2 split. Nothing a program
  can read separates the two kinds.
- **Two links judged both ways:** the context one (§15) made no difference in six answers; the evidence one (NVIDIA's answer beside
  four delay reports under FY2028 revenue, draw 3) gave rung 2, 2, 2 with it and 2, 3, 2 without: not decided by the rule fixed
  beforehand, $0.0109.
- **Council (Codex independent, two challenge rounds):** the rule is not changed now; that it is the better rule is not shown.
- **Verdict:** "never carry", which §15 recommended on draw 1 alone, is withdrawn by its author. Alex on the proposal: "好根据你的建议，
  下一步": the rule stays (D424). Not decided: whether a company's answer to a report must sit under every question the report
  is filed under.

| Arm | Hypothesis | Change | Result | Kept |
|---|---|---|---|---|
| Never carry | A relation should not file a record under the older record's questions | Simulated on three draws; 24 links read blind; two judged both ways | 19 context, 3 evidence, 2 split; the evidence link: 2, 2, 2 against 2, 3, 2 | no: withdrawn |

## 17. Step 2 stops here (2026-11-10)

Alex asked for the next step after D424. Two independent views, written apart, and one challenge round
(`../step2-revision-links-2026-11-10/council/d-claude.md`, `d-codex.md`, `e-challenge.md`, `e-codex.md`) reach one recommendation:
**Step 2 stops here with its known problems recorded, and no new test now.** It is a recommendation on priority, not confirmed by
Alex, and not a claim that Step 2 is free of risk.

**Why.**
- Its three lines (D381) were met at the acceptance of D386 on 50 fresh articles, one draw: search 141 of 143; clear wrong merges
  1 of 57, plus 2 overlaps; later details kept. The first forward run's 3 of 104 (§12) is the older measurement. The fresh set barely
  exercised "later version" relations.
- In the seeded end-to-end test (D392) the clean system agreed with the ruler on 18, 18 and 17 questions against production's 17,
  15 and 16. Its misses: capital spending in all three draws (a known Step 1 gap, D394); the Ohio guarantee question not covered
  in two draws (Step 1's first open defect); the China share question in draw 3 and the FY2028 revenue question in draw 2, once
  each. None has been traced to Step 2; the last two have not been traced to a cause. A lead, not a finding: in draw 2 the FY2028
  question holds one report of the Kyber delay and no answer from NVIDIA, and it sits on a rung boundary in every draw.
- Checked and set aside: of the items the judge was shown, a second or later copy of a statement already in the same request is
  31% to 34% in the three clean draws and 26% to 31% in the three complete production control draws. The copies are a trait of
  the frozen judge's input in production too (D204, D358), not something clean Step 2 added; a test of them is not this step's.

**Recorded as open.**
1. Jev's "later version" relation: 9 of 30 relations join different statements in draw 1 (two source readers); work stopped (D423).
2. The links that relation carries: 19 of 24 are context by two reader families; the rule is kept (D424).
3. Wrong groups: at the line on one draw of fresh articles; the unprompted wrong-group reading test was never run.
4. The "Unverified quote" mark is not shown to Jev (3 of 188 fresh records).
5. Not decided: whether a company's answer to a report must sit under every question the report is filed under.

**What reopens it.** Step 4 yields judged views on the clean path and an end-to-end miss, or something a reader of a thesis sees,
traces to one of the five; or the joining of Steps 3 and 4 has to settle point 5.

## 18. The reopen condition checked (2026-11-11)

The two untraced misses of the seeded end-to-end test were diagnosed ([round log](../e2e-misses-2026-11-11/LOG.md)). Neither traces to
Step 2: one is the judge's own variation at a rung line, the other a difference in what Step 1 filed under the question. Step 2 stays
closed.

## 19. Closed and frozen (2026-11-11, D427)

Asked whether Jev could be closed and put into production, I answered not yet and offered two ways: (A) freeze it and take it to
production with the whole clean path once Step 4 meets its lines, through one end-to-end comparison against production on the frozen
ruler, with Step 2's three lines checked on that run (recommended); (B) transplant it into the current production pipeline now, as a
new version measured against it. Alex: "饿、好jev 收尾冻结": option A.

- Frozen at the committed state (cc2fdf2), each file unchanged since: `step2/compare.py`, `step2/run_forward.py`, `step3/library.py`
  and their tests (13 and 20 pass). `tests/test_frozen_clean_step2.py` holds their sha256 and fails the suite when one moves; a scratch
  copy with `library.py` changed fails it, the unchanged copy passes.
- Not frozen here: the writer between the library and the judge (`e2e-2026-11-09/adapter.py`), measurement code that Step 4's design
  extends; its revision-link rule (D424) stays pinned by `test_adapter.py`.
- Carried with the freeze: the five open defects of §17.
