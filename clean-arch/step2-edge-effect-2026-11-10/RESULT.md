# One unsupported revision relation: what it changed for the judge

**Since (2026-11-11):** work on Jev's revision relation stopped (D423); the rule that a revision takes the earlier record's questions was measured and kept (D424, [round log](../step2-revision-links-2026-11-10/LOG.md)); Step 2 is frozen (D427).

2026-11-10. The test the council of 2026-11-09 recommended, carried out as written in [PROTOCOL.md](PROTOCOL.md). Saved D392 clean draw 1,
the frozen judge through the experimental adapter. No change to Jev, a prompt, a rule, the frozen judge or a saved run. Cost: $0.0126.

**Result: removing the relation changes what the judge reads on one question, and not what it concludes there, in these samples.**

## The case in one picture

An NVIDIA spokesperson answers a report that the Kyber rack is delayed: "Our roadmap is intact." Step 1 filed that under the Kyber
shipping question. Jev read it as a later version of another statement (NVIDIA plans to sell more racks of the existing form), which
is filed under the FY2027 revenue question. Because the adapter gives a record every question link of the record it revises, the
Kyber answer was also shown under the revenue question, on 2026-07-06 and on every later day.

## What was found

| Step | Finding |
|---|---|
| Replay the saved run untouched, no send | Reproduced: 239 of 239 judge requests equal a saved one and took its saved answer; the 23 ledger tables (less each judgement's archive row number), the recorded requests and the counts equal the saved run's. |
| Remove the one relation, no send | Five days identical. On 2026-07-06 the revenue question's request loses the Kyber answer (4 lines; 28 items for 29); the 14 other requests of that level are identical. The replay stops there. |
| Remove the relation, keep the link, no send | All 14 days identical. For this relation the judge's input changes only through the carried link. |
| Send that one request both ways, 3 times each | Six accepted answers, **all on rung 2** ($320 to below $400 billion): by the rule fixed beforehand, no difference in the conclusion in these samples. |

The six answers, read one by one (`poc/data/clean-step2-edge-effect-2026-11-10/judge-probe-1/`):

| Arm | Implied revenue | What moved the rung from 3 to 2, in the answer's words | The Kyber answer |
|---|---|---|---|
| With it, 1 | about $335 billion | the Data Center question's forecast of about $390 billion, times a share of about 86% | cited, marked as pushing up, not used in the reasons |
| With it, 2 | about $330 billion | the same, about 85% | cited, marked as pushing up, not used in the reasons |
| With it, 3 | about $340 billion | the same, about 87% | cited, marked as pushing up, not used in the reasons |
| Without it, 1 | about $340 billion | the same forecast, "most, but not all" | absent |
| Without it, 2 | about $350 to $370 billion | the same forecast, discounted | absent |
| Without it, 3 | about $335 billion | the same, about 86% | absent |

The saved run moved this question from rung 3 to rung 2 on that day. Every one of the six answers gives the same cause: the
question it depends on (Data Center revenue) had moved to about $390 billion. None names the roadmap statement.

What the record does leave behind when it is there: in all three answers it appears among the cited evidence with the mark "pushes
toward the top rung". A reader of the revenue question would see a statement about a later product generation listed as support.

## How big the class is (counted on the saved ledgers, no cost)

A revision relation reaches the judge in two ways.

1. **It carries the new record into the old record's questions.** Links that exist only for that reason:

   | Draw | Links in the ledger | Carried only by a relation, right or wrong | Of all evidence shown to the judge |
   |---|---|---|---|
   | 1 | 700 | 5 | 42 of 4,575 showings |
   | 2 | 725 | 11 | 69 of 4,913 |
   | 3 (its completed run, `judged-2`) | 730 | 8 | 52 of 4,921 |

   This is every relation-carried link, about 1% of the links: an upper bound on the wrong ones, not their count. Only draw 1 has
   the source readers' labels: **2 of its 700 links** come from relations the readers call different statements (the Kyber answer
   into the revenue question; a second Kyber denial into the Rubin shipping question), 1 from an unclear relation, 2 from relations
   that are really repeats. Draws 2 and 3 are not labelled.
2. **It prints one line under the new record** ("the matcher read it as a later version of …", marked as an unverified opinion).
   Draw 1: 20 records carry the line; for 6 of them the printed relation is one the readers call different statements. Two of the
   six were never shown to the judge; the other four were shown 55 times (of 4,575 showings) under four questions. The paid probe
   did not test that line: the relation removed here was not the one printed. Read at no cost instead: in the saved reasons of
   those judgements, every sentence that speaks of a revision, a denial, a replacement or the roadmap (located by those words, then
   read) uses the new statement for what it says itself ("NVIDIA's unsized denial is counterevidence but does not provide a
   delivery date"); none treats it as a later version of the piece the line names. That is a reading of the stated reasons, not a
   test of the line's influence.

Two more facts at no cost:
- Step 1 itself never filed the "roadmap is intact" statement under the revenue question: 0 of 28 copies in the three draws.
- A blind reader given the article and the revenue question, and not told of the relation, placed the statement as context that
  should not move the FY2027 estimate (`council/relevance-codex.md`).

## What this does and does not show

- Shown: this relation changed the judge's input; in three answers each way it did not change the rung or the cause given. The
  implied figures overlap: about $330 to $340 billion with the record; about $335, $340 and $350 to $370 billion without it.
- Not shown: that the record had no influence (the three answers that saw it cite it and mark it as pushing up; stated reasons do
  not prove what moved an answer, and three answers an arm cannot rule out a shift in the figure, in either direction); anything
  about the other relations, another kind of question (this one is led by a figure it depends on), the later days (2026-07-07 to
  07-14 would rest on new answers), the influence of the printed "later version" line, the clean Step 4 (not built), or Step 2's
  overall accuracy.
- The bytes of the saved run's request cannot be read back from the archive; the stand-in is in the protocol.
- **A point the clean PRD leaves open.** PRD §6 saves a revision as "the new evidence and its source, linked to the earlier
  statement"; it does not say the new record takes the earlier record's question links. That rule is the adapter's, taken from
  production's writer. It is the only way a wrong relation moved a record into another question here.

## Recommendation

Leave Jev as it is and stop working on its revision relation now. The defect stays open on the list with what was measured: in
draw 1, 9 of 30 relations join different statements by the readers; they put 2 of 700 links under a question the record was not
filed under and print a wrong "later version" line on 4 records the judge saw; in the one case traced to a judgement the
conclusion did not change. No further wording arm on Jev, and no change to Step 2 or the adapter. Whether a revision carries
question links is a product rule to put to Alex when Steps 3 and 4 are joined on the clean path.

**The challenge round** (`council/result-challenge-codex.md`, a new Codex session reading the raw answers and the saved run): agrees
with leaving Jev unchanged; asked that the line not be called closed, that "about 1%" not be given as the size of the wrong
relations, and that the printed line be read in the saved reasons. All three are taken above.

## Files

- `edge_replay.py` (control and counterfactual replays), `inheritance_census.py` (the count), `judge_probe.py` (check, send, read),
  `PROTOCOL.md`, `preflight.log`, `council/` (four sender reviews, the blind relevance reading, the challenge of this result).
- `poc/data/clean-step2-edge-effect-2026-11-10/`: `control/`, `remove-relation/`, `remove-relation-keep-link/`,
  `inheritance-census.json`, `judge-probe-1/` (registration, raw bodies, the six answers, `reading.json`).
