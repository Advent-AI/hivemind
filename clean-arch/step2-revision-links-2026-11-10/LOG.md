# Step 2 to Step 3: what a "later version" relation may file (council loop, 2026-11-10)

**Status (2026-11-11):** the rule stays (D424); Step 2 is frozen (D427). The measurement kit of this round (`simulate_rule.py`, `build_packets.py`, `tally_readers.py`, `edge_replay.py --uncarry`, `judge_probe.py --case`) is how a later change to the rule is measured.

Run with the `council-loop` skill. This round ends at a proposal for Alex: the fix and how it is measured. Nothing is built into the
writer and nothing is sent before his word.

## 0. Frame

- **Alex's words (2026-11-10)**, after [the traced case](../step2-edge-effect-2026-11-10/RESULT.md) and the question "when B is judged a
  later version of A, should B automatically be put under every question A is under? Not automatically (my suggestion) / keep it":
  "okay take your suggestion what is the fix and how to measure get your council skill ready to propose".
- **Objective.** One proposal: the rule that replaces the automatic carrying of question links on a "later version" relation, where it
  lives, and the measurement that accepts or stops it.
- **Pass line.** None set by Alex. The line in §6 is proposed, not confirmed.
- **Reference system.** The writer as it is: `clean-arch/e2e-2026-11-09/adapter.py`, which gives a record every question link of the
  record it revises (D202's rule, taken from production's `writing.py`).
- **Ruler.** The frozen ruler does not measure whether evidence is filed under the right question (AGENTS §7.1). The readers' labels
  here are an exploratory reference by independent readers, not a ruler, and are labelled so wherever they are quoted.
- **Constraints.** Production, the frozen judge and the ruler do not change. Jev's wording is not tuned (council of 2026-11-09,
  accepted). Code decides identity, never importance; no probability cut, no hand list. No new model call in the product.
- **Out of scope.** Step 1's own filing, the ladder step of Step 4, the judge's quality.
- **Budget.** This round: no model call by the product's code. Readers are Codex and Claude sessions. A paid check, if the proposal
  needs one, is priced in §6 and waits for Alex.

## 1. Census on the saved draws (no model call by the product; `census.py`, `simulate_rule.py`)

The class is every link the judge's ledger holds only because a "later version" relation carried it: the record's own Step 1 links
and Step 3's later links do not include that question.

| Draw | Links | Relations | Carried only by a relation | Showings of them to the judge | Question-days judged only for a carried link |
|---|---|---|---|---|---|
| 1 | 700 | 30 | 5 | 42 of 4,575 | 0 |
| 2 | 725 | 21 | 11 | 69 of 4,913 | 2 |
| 3 (`judged-2`) | 730 | 27 | 8 | 52 of 4,921 | 2 |

The three draws are three extractions of the same 243 articles, so they are not three independent samples of news.

**Split by a fact code can read: where did Step 1 itself file the record?**

| Step 1 filed the record | Links | What they are |
|---|---|---|
| under a question the seeded test judges | 19 | All NVIDIA's answer to the Kyber delay report ("Our roadmap is intact", "on schedule"), carried from the Kyber question to revenue questions (10: v20 seven, v1, v2, v22) and to the Rubin shipping question (9: v7) |
| only under a thesis the clean system opened itself, which the seeded test does not judge | 3 | The tally of blocked data-center projects (filed under "total AI infrastructure capital expenditures in 2026") carried into Data Center revenue and hyperscaler spending; a US approval for ZTE to buy H200 (filed under an export-licence thesis) carried into the China share question |
| under no thesis at all | 2 | New charges in a Singapore case into the China share question; the RTX 50 Super refresh shelved into Blackwell and Rubin revenue |

The second row is an effect of the seeded test, not of the product: those records have a home in the clean library, and the test
judges only the 22 seed questions.

**The exact effect of each candidate rule** (`simulate_rule.py`: the adapter's own writing code over each draw, judging off; under the
present rule the written ledger equals the saved one row for row in all three draws):

| Rule | Links not written (draws 1, 2, 3) | Anything else changed |
|---|---|---|
| never carry | 5, 11, 8: exactly the census's 24 | no other row of any table; the remaining links in the same order |
| carry only for a record Step 1 filed under no thesis | 5, 9, 8: the 22 links of records Step 1 filed somewhere | none |

## 2. Mechanism

- **Code.** `e2e-2026-11-09/adapter.py`, `Adapter.article`, lines 222 to 230: after `store.revise(old, new, …)`, every question
  `store.views_linked_to(old)` returns gets a link from the new record. The relation comes from Jev's `supersedes` answer on one
  draw (`step2/compare.py`), with no further check.
- **Origin.** D202 (2026-10-27): "A `replace` decision stores the incoming piece, links it wherever the target is linked, and records
  the pair in a new `revisions` table (old, new, said day, seq); both pieces stay in force." Before D202 the new piece took the old
  piece's place; after it both stay, and the carrying of links stayed with them.
- **The need it serves.** A question that holds statement A must also see A's later version.
- **Decided beside it.** D203: "D202's census: 19 of 37 recorded revisions carry a wrong label", so the judge's line reads "Opinion,
  not verified". D204, for repeats: "the old piece gains no source row and no new link (the new piece carries the outlet and the
  links; a link written on a one-draw label is a write like any other)". The relation is treated as an opinion where it is shown and
  as a fact where it files.
- **On over-filing.** Alex on filing (D207): "要么挂不到，要么挂多". D355's first open defect: news is filed under the company's
  revenue questions, and "the total-revenue question holds about a quarter of all links". Ten of the 24 carried links land on revenue
  questions.
- **The clean contract.** PRD §6 saves a revision as "the new evidence and its source, linked to the earlier statement as a
  revision" and says nothing of thesis links. D383 keeps a statement no thesis takes without a link, to be linked when a thesis
  opens. The carrying is the adapter's alone on the clean path, and Step 4's design has Stage B write "as the Stage 2 adapter
  writes them".
- **Two properties of the rule found while tracing it.** It depends on order: the new record takes the links the older record has
  at that moment, and none it gets later. It spreads: a record that revises a record with a carried link takes that link too.

## 3. Blind readers over all 24 carried links (two families; `build_packets.py`, `tally_readers.py`, `readers/`)

The readers' labels are an exploratory reference, not a ruler. Two families (a Codex session and a Claude session for each task),
each blind to how a case came about; the key was kept outside the repository.

**Filing: would a careful analyst file this statement as evidence under this question?** 56 cases: the 24 carried links mixed with
15 records under a question Step 1 itself filed them under and 17 records under a question no record of their article was filed
under.

| Cases | Codex | Claude |
|---|---|---|
| filed there by Step 1 (15) | evidence 14, context 1 | evidence 13, context 2 |
| nothing of the article filed there (17) | evidence 1, context 9, unrelated 7 | evidence 1, context 1, unrelated 15 |
| **carried by a relation (24)** | evidence 5, context 19 | evidence 3, context 21 |

On the carried links the two families agree on 22 of 24: **19 context by both** ("related enough to note, should not move the
answer"), **3 evidence by both**, 2 split. Neither family called a carried link unrelated.

| The 3 both would file | What it is | In the saved judgements |
|---|---|---|
| draw 3, `70:e4` into v22 (FY2028 total revenue) | NVIDIA's answer, beside four SemiAnalysis reports Step 1 filed under that question | shown 9 days, cited 9, marked as pushing up 9 |
| draw 3, `238:e1` into v17 (China share) | a US approval for ZTE to buy H200; the same news is already there through another record | shown 1, cited 1 |
| draw 2, `239:e5` into v20 (FY2027 Blackwell and Rubin revenue) | the record also says Blackwell Ultra is ramping and Rubin is on track | shown 1 (the last day), cited 0 |

The 2 split: the data-center tally into Data Center revenue (draw 1; cited 6 of 10 showings) and the RTX 50 Super shelved into
Blackwell and Rubin revenue (draw 2; cited 0 of 3).

**Relation: is the incoming statement a later version of the stored one?** 31 pairs: the 23 carrying relations and 8 relations two
source readers labelled on 2026-11-09. Each family agrees with the earlier labels on 9 of the 12 labelled pairs. Of the 23 carrying
relations the families agree on 16: different 11, repeat 2, revision 2, uncertain 1; on the other 7 Codex says uncertain where
Claude says revision (6), and revision where Claude says different (1). A link carried by a relation both call a later version: 2
of 24, both context by both families.

**What separates the links worth keeping from the rest: nothing a program can read.** The same record (`70:e4`) is context under
FY2027 revenue in draw 1 and evidence under FY2028 revenue in draw 3; both came through relations both families call different
statements. The split by where Step 1 filed the record does not separate them either: all 3 both-evidence links belong to records
Step 1 had filed somewhere.

## 3a. Two carried links traced to a judgement, one of each kind

| | The link | Sends | With the carried record | Without it | By the rule fixed beforehand |
|---|---|---|---|---|---|
| Context by both families | draw 1, NVIDIA's answer under FY2027 Blackwell and Rubin revenue, 2026-07-06 ([result](../step2-edge-effect-2026-11-10/RESULT.md)) | 6, $0.0126 | rung 2, 2, 2; the reasons never use it | rung 2, 2, 2 | no difference in these samples |
| Evidence by both families | draw 3, the same answer under FY2028 total revenue, 2026-07-06 ([protocol](PROBE-v22.md); `poc/data/clean-step2-revision-links-2026-11-10/judge-probe-v22/`) | 6, $0.0109 | rung 2, 2, 2 at about $553 to $554 billion; all three reasons set it against the four reports | rung 2, **3**, 2: about $553, **about $545**, about $553 to $554 billion | **not decided** (mixed) |

In the second case the question then shows four reports of delays and no answer from the company. One answer of three "would shade
that forecast below the $550 billion boundary"; none did with the answer shown. The previous conclusion sat $4 billion above that
boundary, so three answers an arm cannot separate the record's effect from the judge's own spread: it is a direction, not a result.

**The four question-days judged only because a carried link arrived** (draws 2 and 3, the Rubin shipping question on 2026-07-07 and
07-13), read in the saved runs: the rung is 1 on every day of the window in both draws, none of the four judgements changed it or
used the carried record in its stated change, and the question was judged again the next day in all four. Nothing was at stake
there.

## 4. Design of the rule that was considered, "never carry" (the tables of AGENTS §2; withdrawn in §6)

Written before the readers and the second traced case; kept as the design that was weighed.

**The rule.** A "later version" relation is recorded and shown as it is now. It writes no thesis link. A record is filed where Step 1
filed it, and where Step 3's later linking files it.

**Where it lives.** One place: the writer between the library and the judge (`adapter.py`, the three lines of the carrying loop), as an
explicit setting of a run, so that the saved D392 and D395 runs stay reproducible under the old setting. PRD §6 states the rule;
Step 4's design sentence "written as the Stage 2 adapter writes them" names the setting. Production is not touched.

**Table 1. State and event** (a record R that Step 2 judged a later version of the record A; A is under question Q)

| State of R | Event | Now | Proposed |
|---|---|---|---|
| Step 1 filed R under some thesis | R is written, with its relation to A | R is also linked to Q and to every other question of A | R keeps its own links; the relation row is written |
| Step 1 filed R under no thesis | R is written, with its relation to A | R is linked to A's questions | R has no link (D383) and stays eligible for later linking; the relation row is written |
| either | R has relations to two older records | links from both | none from either |
| either | A gets a new link on a later day | R does not get it (the carrying happened once) | no difference between the two days |
| either | a later record R2 is judged a later version of R | R2 takes R's links, carried ones included | R2 keeps its own |
| either | a thesis opens later | Step 3's later linking judges unlinked groups against it; it does not read the writer's links | the same |
| either | the day's judging round | Q is judged that day when the carried link is its only new link (2 and 2 question-days in draws 2 and 3) | Q is not judged that day for that reason |
| either | R has no verified passage | the record and its relation are dropped and counted | the same |
| either | the draw is replayed | the same rows | the same rows |

**Table 2. The value removed (a link from R to Q) and every reader of it**

| Reader | What changes |
|---|---|
| `judging.evidence_in_view` (what the judge is shown for Q) | R is not shown under Q; it is still shown under its own questions |
| the day's changed set, `round_of_judgements` | see the judging row above |
| `store.views_linked_to` (the carrying loop) | not read for carrying any more |
| the judge's "later version" line (`store.revision_of`) | unchanged: printed wherever R is still shown |
| the judgement scorer | reads judgements only; no direct change |
| Step 3's library and later linking | do not read the writer's links |
| a page that lists evidence under a thesis | R is no longer listed under Q |

**Table 3. Checks written for the present path**

| Check | Under the proposed setting |
|---|---|
| `test_adapter.py`, "the new piece inherits the old piece's seed links" | It states the present rule. It changes with the decision, recorded first: under the new setting the new piece holds only its own links; a mutant that carries must fail it |
| the adapter's leakage checks and `load_draw` | unaffected |
| `simulate_rule.py` | must pass on the built setting as it passes on the simulated one |
| `edge_replay.py control` | must still reproduce draw 1 under the old setting |

**Table 4. Prior decisions**

| Decision | What it says | Relation to the rule |
|---|---|---|
| D202 | "links it wherever the target is linked" | The rule amends this on the clean path; production keeps it |
| D203 | the relation is printed as "Opinion, not verified" | kept |
| D204 | "a link written on a one-draw label is a write like any other" | the rule applies this to a revision |
| D168 | an official's confirmation or denial of a report is a revision | kept: the relation is still recorded |
| D383 | a statement no thesis takes is kept unlinked and linked later | the state of an R that Step 1 filed nowhere |
| D207, D355 | over-filing, and filing under revenue questions, are known harms | 10 of the 24 carried links land on revenue questions |

## 5. Council A (independent, then two challenge rounds; `council/`)

- **Independent** (`a-codex.md`, `a-claude.md`, each written before reading the other): both leaned to "never carry", with the same
  measurement shape (exact on stored data, blind readers, a paid check only for a named case).
- **Round 2** (`b-challenge.md`, `b-codex.md`), after the readers and the draw 3 case: Codex withdrew "never carry". Agreed: the
  draw 3 link is useful and came by a lucky path; no rule a program can apply files a company's answer where the report it answers
  is filed without a reliable pairing; "carry only when Step 1 filed the record nowhere" misses that link. Codex's limits on the
  probe: six answers cannot decide the rule either way.
- **The probe** was reviewed once more before it was sent (`probe-review-codex.md`: one serious finding, the reader not bound to its
  case; closed and shown) and sent on my reading that it was closed.
- **Round 3** (`c-challenge.md`, `c-codex.md`), after the probe. **Consensus:** do not change the rule now, and take the new
  evidence back to Alex, since he accepted "not automatically" on my reading of draw 1 alone. **Not agreed as proven:** that the
  present rule is better (two cases; 19 context links do not show 19 harmless links; "about 1%" is every carried showing, useful ones
  included). Codex against a test of all 24 links both ways (144 calls, about $0.30): one link removed at a time is not the rule
  removed, and three answers an arm would leave many cases undecided; it asked instead for the four question-days of §3a, read
  at no cost: done.
- **Left open for Alex, as a product rule not yet decided:** whether a company's answer to a report must sit under every question
  the report is filed under.

## 6. Verdict and the proposal

**Alex on this proposal (2026-11-10): "好根据你的建议，下一步". The rule stays (D424); point 2 below is not decided.**

**Verdict: stop this fix. The rule stays as it is.** "Never carry", the suggestion Alex accepted, is withdrawn by its author: on the
three draws it would take away 19 links two reader families call context and 3 they would keep, and in the one kept link traced to a
judgement the company's answer is the only thing set against four reports.

**What is proposed to Alex**

1. **Keep the writer's rule unchanged.** No code, PRD rule or test changes. The carried context links (19 of the 24, in these three
   draws all one story) stay a recorded defect: they are shown and cited, and in the one traced case they did not move a
   conclusion.
2. **One product rule for him to decide, when he wants it:** a company's answer to a report is filed under every question the
   report is filed under. Today only the carried link does this, through Jev's relation, and it over-reaches to neighbours of the
   same story. A cleaner version needs the pairing of an answer with the report it answers to be right, which is the part of Jev
   the council of 2026-11-09 stopped tuning. If he decides the rule, this round's 24 links with both families' labels and the two
   traced judgements are its first test set.
3. **How any later change to this rule is measured** (built and used in this round, all on stored data):
   - exactly which links a rule writes, by the writer's own code with judging off (`simulate_rule.py`; under the present rule it
     reproduces the three saved ledgers row for row);
   - two blind reader families over every link the change adds or removes, mixed with controls of both kinds (`build_packets.py`,
     `tally_readers.py`);
   - for a link both families would keep, or that the saved judgements cite, the question's judgement on that day both ways, three
     answers each, about one cent a case (`edge_replay.py --uncarry`, `judge_probe.py --case`).
   Proposed line for such a change, not confirmed: it removes no link both families file as evidence unless that link's judgement
   shows no difference both ways, and at least 9 controls in 10 are read as expected.

**Not shown by this round:** anything beyond three extractions of the same 243 articles and one story; the effect of the 18 other
context links on a judgement; later days; the clean Step 4.

| Arm | Hypothesis | Change | Result | Kept |
|---|---|---|---|---|
| Never carry | A "later version" relation should not file a record under the older record's questions | Simulated on the three saved draws; 24 links read blind by two families; one context link and one evidence link judged both ways | 19 context, 3 evidence, 2 split; context link: no difference; evidence link: 2, 2, 2 with it and 2, 3, 2 without | no: withdrawn, the rule stays |
| Carry only when Step 1 filed the record nowhere | The rule is needed only as a home for unfiled records | Simulated | keeps 2 links (context by both; split) and drops the 3 both families would keep | no |

## 7. After Alex's word: the next step (2026-11-10)

Alex: "好根据你的建议，下一步" (D424). Asked what comes next for Step 2, the council ran once more: two views written apart (`council/d-claude.md`,
`d-codex.md`) and one challenge round (`e-challenge.md`, `e-codex.md`). **Consensus: Step 2 stops here, no new test.** The reasons, the
five open items and what reopens the step are in the [Step 2 log](../step2-validation-2026-11-07/LOG.md) §17. Corrected in the round:
Codex's first view cited the first forward run's 3 of 104 wrong merges; the acceptance on fresh articles is 1 of 57. Dropped in the
round: my lean to a sizing probe of repeated copies in the judge's input, after the same share was found in production's control
draws.
