# The second-look test: result (2026-11-10; D422)

**The second look does not pass the conditions written before the send.** Of the 18 answers with a fault the readers had
agreed on, it mended 6 (the page asks for 9). Of the 30 answers no reader had faulted, 3 count against it (the page fails
at 3). Whether the step takes a second look is Alex's decision (D422); this page gives him the count, not a choice made.

One picture. The thesis on the Hugging Face purchase had a wrong ruling out ("restructures the acquisition" counted as the
deal being off). Sent back, the model took "restructures" out, and the readers now fault the same answer for something
else: the thesis names a restructuring and the answer no longer says what happens to it. And the thesis on Vera Rubin's
first shipments, which no reader had faulted, came back twice with its reference ("could begin shipping later this year")
removed; both readers fault that.

## What was done

76 answers of the fourth Stage A, each sent back once in its own conversation with one sentence that names no fault
(`REGISTERED.md`). 49 came back unchanged, 27 changed; code refused one of the 27 and kept its first answer. $0.1176
(cap $0.20). One blind reading round: 102 items (the 76 first answers and the 26 kept second answers, shuffled, none
saying which it is), two reader families with the unchanged form; where they differed, two third readers (54 points).
`compare.py` and `reader_repeat.py` print every number below; `result/compare.txt`, `result/reader-repeat.txt`.

## The count the page registered

| | passes | fails | counted |
|---|---|---|---|
| the 18 with an agreed fault | 9 mended, none with a new agreed fault | 5 or fewer | **6 mended**, none of the six with a new fault; a seventh send carries a new one. In between |
| the 30 no reader faulted | at most 1 | 3 or more | **3**: one refused by code, one turned from a decline into a ladder and faulted, one faulted. Fails |

The round faults again, as agreed, 14 of the 18 first answers (the page needs 12 for the first row to be read).

## The same count, read field by field (my read, one reader)

Every "mended" and every "new" was read against what the second look changed in the answer.

| send | counted as | what the second look changed | the fault concerns | so |
|---|---|---|---|---|
| u2/clean-7 send 3 | mended | the theme alone | the question, untouched: a reader named "the four companies may not report this figure" on the first copy and nobody named it on the second | not the second look's doing |
| u2/clean-9 send 2 | a new fault | the ruling out and the list of what is left out | the reference, empty in both copies: held on the first copy, failed on the second | not the second look's doing |
| u3/clean-5 send 3 (unfaulted group) | mended | the ruling out | the question, untouched | not the second look's doing |

Without them: 5 mended of the 18 (the page fails at 5), 2 of the 30 against (in between). **Neither reading passes either
row, and each reading fails one.** The registered count stands as the result; the field read is beside it because three of
its entries come from the readers marking two copies of one untouched field differently.

## What the second look did, over the 26 answers it changed and code kept

- **Mended, 6** (field read): three wrong refusals turned into ladders (acc/clean-9 send 2, u3/clean-11 sends 1 and 3:
  every refusal the fourth run's readers agreed was wrong); the 105 billion ceiling taken out of a reference (acc/clean-3
  send 1); a missing reference added (u1/clean-11 send 2); a missing unit added to a question (acc/clean-10 send 3).
- **Broke, 3:** a correct reference removed, twice (u1/clean-3 sends 1 and 2); a correct refusal for "no listed theme"
  turned into a ladder with no reference (u3/clean-2 send 2).
- **Traded one fault for another, 2:** "restructures" out of the ruling out, and now neither judged nor listed
  (acc/clean-2 sends 1 and 3).
- **Refused by code, 1:** a quarter, rightly declined, came back as a ladder (acc/clean-5 send 3). The first answer stayed.
- **Changed without mending:** the two Kyber answers that ask about 2027 and fall due at the end of 2028 (u1/clean-6 sends
  1 and 2: the wording moved, the fault stayed); the lidar ban under the export-controls theme (u1/clean-10 send 3).
- **Left alone, with the fault agreed again:** u1/clean-8 send 3, u3/clean-3 send 2, u3/clean-7 sends 1 and 3.
- The other changes add a line to the list of what is left out or reword a ruling out; no reader faults them.

The pattern: it mends what one rule states and one field shows (a refusal with a main figure, a ceiling as a reference, a
missing unit). It does not mend what needs the thesis read against the question (which year is asked). And asked to check
"each rule", it also acts on answers that were right: of the ten correct refusals in the sample, two came back as ladders.

## What the round says about the readers (`result/reader-repeat.txt`)

The same 76 first answers were read in the fourth Stage A and again here, by fresh readers of the same two families.

| the fourth run's reading | answers | an agreed fault again | a disputed fault only | no fault |
|---|---|---|---|---|
| a fault both sides agreed | 18 | 14 (13 on the same mark) | 2 | 2 |
| a fault the third readers parted on | 18 | 2 | 10 | 6 |
| a mark one reader failed, both third readers held | 10 | 1 | 3 | 6 |
| no fault from either first reader | 30 | 2 | 1 | 27 |

The two third readers rule alike on 22 of 54 points. What this supports: most agreed faults of the fourth run are found
again (the wrong refusals, the rulings out, the Kyber year, the lidar theme are real; "the same mark" is loose where the
mark is a fault named outside the form, since those all share one letter); and 2 of 30 answers a round called clean draw
an agreed fault in the next, in this chosen sample, one draw. **What it does not support** (the council's correction,
`council/ke-codex.md`, to a sentence I had written here): that a line of "none" on a wrong question, an unlisted part, a
ruling out or a refusal can be missed by a step that makes no such fault. Both clean-to-faulted answers carry faults named
outside the form, none of those four marks; the readers' own movement on each line has not been measured.

The Kyber answers are the ladder step's own fault, not the thesis's shape: the step turned "in 2027 or delayed to 2028"
into "by the end of 2028", which cannot tell the two apart (the council's read; mine had left it open).

## The council's read (`council/ke-codex.md`) and the consensus

The count is right and the change to `compare.py` is faithful to the registered page. The registered 6 and 3 stand as the
result; the field read (5 and 2) stays beside it as the author's interpretation, since the script tells faults apart by
mark and cannot itself show that the same fault went away. A second look kept to refusals is a subgroup chosen after the
result and is not the next test. **Consensus:** the second look is not adopted on this evidence; Alex is asked to permit
the preparation of Stage B on the step as it ran in the fourth Stage A, despite its missed lines, the one test being the
planned $0 blind reading of the 159 stored judgements, reported with its reader controls before any paid Stage B send.
That is a recommendation to measure what the remaining ladder faults cost the judgement; it is not evidence that Stage A
passed, and the record does not show it is the step with the largest effect: question opening without seeds stays below
its seeded score (4.0 against 6.33, D395) and the capital-spending gap is open (D394).

## What it cannot show

That the six lines would be met with a second look in the step: only a run of the 44 theses could. Nothing here is a
fifth Stage A, and none is sent without Alex's word.

## Corrections to my own read, kept

- Before the readers I counted 7 of 18 mended and called the two removed references "lose a reference in words alone";
  the readers fault both, rightly (`result/own-read-of-the-pairs.md`).
- `compare.py`, written before any reader's row, summed kinds of damage; the registered page counts sends. Changed before
  the third readers' rows existed, to count a send once (u3/clean-2 send 2 is two kinds).
- The cost estimate was eight cents; the model reasons before it answers, and it cost twelve.
