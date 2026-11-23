# Answer choices that leave a part of the question unlisted (line 2): census (D576, 2026-11-16, $0)

**Answer: a pattern supports one hypothesis; it is not a proven cause.** Every failing send of the two readings read here (10 sends,
7 topic instances) leaves out a clause that sits in the topic's `outcome` field and not in its `description`. In all seven, another
attempt of the same topic lists that clause. The request never says that the outcome's clauses belong to "the topic's wording", and
in the same sentence it names the outcome as the thing to judge. The hypothesis: the undefined term makes listing an outcome-only
part a coin flip. The other attempts list the same clauses without any definition, and the earlier accounts were prompted with the
disputed clause. So only sends can show whether a definition changes the rate.

**Why it matters now:** since D570 the product's page shows each question's list of parts not judged beside its answer. An empty
list on a topic that compares with last year tells a reader nothing was left out, when the comparison was.

## The cases

Scripts: `line2_census.py` (each send either first reader marks failing: the topic as the ladder step was given it, the send's own
list, both readers' reasons, the topic's other sends' lists). Outputs: `fortnight.txt` (09-22 to 10-05, D563), `second-week.txt`
(the week of 10-06, D550 and D551). The fresh week's six (09-22 to 09-28) are D547's record (`fresh-ladders/PROMPT-AUDIT-LINE-2.md`: "every
failed attempt of the fresh week concerns a clause that sits only in the `outcome` field").

| Reading | Topic | Sends failing (both first readers) | The unlisted part, in the outcome only | Other sends of the topic that list it |
|---|---|---|---|---|
| fortnight | clean-2, purchase commitments | p1 | "versus the prior year" | p2, p3 |
| fortnight | clean-3, Blackwell to China | p2 | "so that China data-center revenue can resume" | p1, p3 |
| fortnight | clean-6, Hugging Face deal | p3 | the price "being repriced" | p1, p2 |
| fortnight | clean-7, MIIT approval | p2, p3 | "capping quantities" | p1 |
| fortnight | clean-13, CPO shipments | p1, p2 | the Q4 2026 (15,000) and early-2027 (16,000) checkpoints | p3 |
| second week | clean-1, Ohio lease guarantee | p2, p3 | "any amounts paid or accrued", "the remaining term" | p1 |
| second week | clean-3, memory prices | p2 | "the memory makers' reported average selling prices and memory gross margins" | p1, p3 |
| fresh week | three topics | six sends as marked (2 to 4 under July's rulings, D547) | outcome-only clauses | D547: an outcome-only clause listed 11 of 18 times |

In clean-7 and clean-13 the failing sends do list the description's own extra part (the description's "allowing those sales to
proceed"; the 30,000-unit checkpoint), and leave out the outcome's.

**Marked by one first reader only (not settled; read beside):** fortnight clean-5 p2 and p3 ("compared with the nearly $800 billion",
outcome only; no send of the topic lists it), clean-9 p2 (the $1.3 trillion comparison, outcome only; p1 and p3 list it); second
week clean-8 p1 (the description's "up to 25% of the loss", the only description-only part in this census; p3 lists it). So a
description part can be missed too (and July's two failures are description parts: the table by kind below).

## The request, as the model reads it

The topic arrives as fields: `"description": …, "outcome": …, "period": …`. The request's sentences on the list (the ladder step's
`candidate-system.txt`, `candidate-closing.txt`, `candidate-schema.json`):

- System: "A topic's wording may ask about more than one thing. Judge the one the topic's outcome names as what is tracked. List
  every other part of the topic's wording that the question leaves out, a second figure or event, a condition or a comparison, in
  not_judged …"
- Schema, `not_judged`: "Every other part of the topic's wording that the question leaves out (a second figure or event, a condition,
  a comparison); empty only when the question leaves nothing of the wording out."
- Closing check: "does it ask one thing, the one the topic's outcome names, and is every other part of the topic's wording listed in
  not_judged?"

"The topic's wording" is never tied to a field. The outcome is named as the source of the one thing judged. A reader of the request
can take the wording to be the description, with the outcome only telling which part of it to judge. That is the reading D547's
stored accounts gave ("mostly reads the wording as the description alone"). Verdict (prompt audit): **missing**, the term undefined;
the clauses missed are of the kind the request names (a comparison, a condition, a second figure).

## By kind, across all four stored readings (the readers' original marks kept)

The readings disagree on two kinds; on one kind they agree. Rows count failing attempts. "Matters" counts distinct matters: the
fortnight re-opened the fresh week's articles with another Step 1 run, so its cloud-spending, Blackwell and Chinese-permission topics
are the fresh week's matters again.

| Kind | July (91 ladders, calibrated by third readers) | Fresh week (D547) | Week of 10-06 | Fortnight | Where it sits | Standing |
|---|---|---|---|---|---|---|
| **A second figure or event, or a difference inside an outcome, left unlisted** | 2 (the DeepSeek inquiry's penalties; graphics memory beside DRAM) + 1 disputed (Vera CPU shipments and first revenue; one first reader) | 2 (capping quantities) | 3 (amounts paid and the remaining term; makers' prices and margins) + 1 disputed (the 25% loss cap) | 5 (repricing; capping quantities ×2; two earlier checkpoints ×2) | July: the description; since: the outcome (one disputed in the description) | failed in every reading where it occurred: **12 attempts on 7 matters**, plus 2 disputed |
| A comparison with the reference figure or the prior year | 9 attempts left it unlisted; 7 passed by both first readers, 2 ruled passed by both third readers | 2 ($800 billion) | 0 | 1 (versus the prior year) + 3 disputed ($800 billion ×2, $1.3 trillion) | the outcome | July passes it; later readings fail it |
| A consequence ("so that … can resume") | 2, passed by both first readers | 2 (Blackwell revenue) | 0 | 1 (the same matter) | the outcome | July passes it; later readings fail it |

The row groups several omissions (a second figure, a second event, a cap inside an approval); each reading failed the ones it met,
which is not the same as every reading judging every one of them alike. It is also the kind the request names ("a second figure or event, a condition or a comparison"). Ten of its
twelve attempts are outcome-only clauses. The two July cases sit in the description, so the defect is not only about the field. On
the two disputed kinds the readers' threshold differs; a prompt change aimed at them would be tuning to one reading's rule.

**Harm side, not yet counted:** attempts that list something that is not a part (how the answer is settled, or a distinction the
answer choices already judge). No reader marks that, so this census cannot count it. One example from the fortnight: clean-6 pass 2
lists "Whether the acquisition is repriced, delayed past the check date, or terminated as separate outcomes". Delay and termination
are judged by its Still open and Ruled out choices; only the repricing is a part.

## Prior decisions on this class

- **D547** refused ruling that the wording is the description alone. D397 judges the main part and shows the rest as not judged.
  D436 keeps a second side of the same bet, found in the outcome, "as context in that question … shown as not judged". So the
  direction the record supports is the other one: the wording is both fields.
- **D558** deferred a repair "for the day the list has a reader" (now, D570). It also warned that a single defining clause may not
  be enough. D558 recorded misses on both fields in the week of 10-06; this census finds only the one disputed description case
  there.
- **D426** forbids tuning the step further on Alex's 44 topics; none of the cases above is one of them.

## What it does not show

- That a definition would make the model list these parts. The other sends of the same topics list them without one, so the miss
  is a coin flip per send; only sends can show the change.
- That listing every outcome clause is harmless. An outcome also names how the answer is settled ("as reflected in … disclosures")
  and the event's own alternatives ("versus being … delayed past the check date or terminated"), which the answer choices already
  judge. Neither is a part to list; no reader in this census asked for either.
