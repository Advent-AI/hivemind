# Council A: Claude's own reflection, written before reading Codex's

2026-11-10. Written after building the census of the three draws (`census.py`) and before the blind readers returned and before
opening `a-codex.md`.

## Mechanism

- Code: `clean-arch/e2e-2026-11-09/adapter.py`, `Adapter.article`, the loop after `store.revise` (lines 222 to 230): for each relation
  a record brings, every question the older record is linked to gets a link from the new record.
- Whose decision: Jev's `supersedes` answer on one draw (`step2/compare.py`), with no further check. Production's writer applies
  three conditions the adapter does not (`writing.revision_refused`: a stated day, a tier not below the old piece's, the same
  party for a view or a rumour); none of them would stop the Kyber cases (a company statement may revise a third party's report).
- Origin: D202 (2026-10-27), "a `replace` decision stores the incoming piece, links it wherever the target is linked". It was chosen
  when the new piece took the old piece's place. After D202 both pieces stay in force, and the link carrying stayed.
- The need it serves: a question that holds statement A must also see A's later version.
- A principle already decided next to it: D204 (2026-10-28), for repeats, "the old piece gains no source row and no new link … a
  link written on a one-draw label is a write like any other". D203 recorded that 19 of 37 recorded revisions carried a wrong label
  and made the judge's note say "Opinion, not verified". So the relation is already treated as an opinion when it is shown, and
  still as a fact when it files.
- The clean PRD §6 saves a revision as a link between two records and is silent on question links.

## What the rule did in the three saved draws (by code)

| Draw | Links | Carried only by a relation | Showings of them |
|---|---|---|---|
| 1 | 700 | 5 | 42 of 4,575 |
| 2 | 725 | 11 | 69 of 4,913 |
| 3 | 730 | 8 | 52 of 4,921 |

Two classes, split by a fact code can read:

1. **The record has a question of its own from Step 1: 19 links.** All 19 are NVIDIA's answer to the Kyber delay report, carried
   to revenue questions (10: v20, v1, v2, v22) and to the Rubin shipping question (9: v7).
2. **The record has no question of its own (Step 1 kept it unlinked): 5 links, 4 records.** A tally of blocked data-center projects
   into Data Center revenue and hyperscaler spending (draw 1); new charges in a Singapore case into the China share question; the
   RTX 50 Super shelved into Blackwell and Rubin revenue (draw 2); a US approval for ZTE into the China share question (draw 3).

Also by code: for 5 of the 24, another copy of the same statement (same Step 3 group) is already under the question by its own
link; in draws 2 and 3, two question-days each were judged only because of a carried link.

My own reading of the 24, before the readers: class 1 is noise where the target is a revenue question and at best a duplicate
where it is the shipping question. Class 2 is the only place the rule can help: the tally with "$130 billion" was used by the
hyperscaler-spending judgement's reasons in draw 1, the ZTE approval looks like the same news as the older record, the other two
look weak.

## Candidate fixes

| | What is written | What it could lose | Fit |
|---|---|---|---|
| F1. Never carry | The relation and its printed note stay; no link is written on it | A record of class 2 is under no question until a thesis opens (D383's designed state for an unlinked record). Concrete: the $130 billion tally | Finishes D204's principle; amends D202 on the clean path; code decides nothing |
| F2. Carry only for a record with no question of its own | 19 links go, 5 stay | Still files on Jev's one-draw label, for a record that would otherwise be nowhere; a second way of giving an unlinked record a home, beside Step 3's later linking | A product choice: is a wrong home better than no home? |
| F3. Keep | as now | nothing; keeps about 1% of links of mixed worth | — |
| F4. Show the later version under the old record, file nothing | a note in the judge's request | — | Changes the frozen judge's text: out |
| F5. Apply production's three conditions | fewer relations | — | Would not stop the Kyber cases: not a fix for this class |

My lean: F1, unless the readers find class 2's links are needed updates; then F1 against F2 is a product choice for Alex with the
readers' counts.

## How to measure

1. **Exact, free.** With the rule changed, the adapter must write the same evidence, relations and every other link; the removed
   links must be exactly the census's set. A replay of each draw's writes, ledger compared table by table; and the first judging
   round that differs, from the saved archive.
2. **Readers, no API cost.** Every removed link, blind and mixed with controls, by two reader families: would an analyst file it
   there (evidence, context, unrelated); and is the carrying relation a later version (revision, repeat, different, uncertain).
   Each link then falls into: gain (does not belong), neutral (the statement is already there), loss (belongs, not otherwise there,
   a true later version). Disagreements go to a third reader with the sources.
3. **Paid, only where the readers find a loss.** That question's judgement on that day, both ways, three answers each (about
   $0.013 a case), as for the Kyber answer. Not a whole-window rerun: the class is about 1% of what the judge reads, and two fresh
   runs differ by more than that from the judge's own sampling; six judge passes would cost about $2.90 and could not attribute a
   difference.

Proposed line (not confirmed): adopt if the exact check shows only the census links change; the readers place the controls as
expected in at least 9 of 10; and no removed link is a loss, or each loss shows no difference in the conclusion in its paid check.
Stop and return to Alex if a loss case changes a conclusion.
