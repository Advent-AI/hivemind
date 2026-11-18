# Prompt audit of one failure class: a clause left out of the question and not listed (D546), 2026-11-15

Scope: the six attempts of the fresh week that both readers failed on line 2 (and a seventh the blind reader failed), in the step
that writes a question's answer choices (`clean-arch/step4-2026-11-10/ladder/candidate-system.txt`, `candidate-closing.txt`,
`candidate-schema.json`, frozen by D426). The whole request was read as the model reads it (system text, the topic as it is given,
the answer form's descriptions, the closing check), against Alex's decision (D397), his line (D400) and the reading form. Then
the model's own account on four stored attempts (`model_accounts.py`, `accounts.json`: $0.0022 of a $0.05 ceiling). Nothing was
changed.

## The verdict

**A term the request never defines, and marks that were stricter than the reading already ruled on.** The request tells the
model to list "every other part of the topic's wording" and never says which text "the topic's wording" is; every failed
attempt concerns a clause that sits only in the topic's `outcome` field. My first conclusion from that, that such clauses need
never be listed, was refused by the council and is withdrawn (section 6): D436 has a second side of a bet, which can sit in the
outcome, shown as not judged. The recount of section 7 settles more: in the July reading the third readers of both families
ruled an unlisted comparison with the reference a pass, twice; two of the fresh week's six failures are that case. **After the
recount no omission recurs on two questions under an agreed reading, so no prompt change is designed (D547).** The undefined
term stays recorded.

## 1. What the request says, in every place

| Where | The sentence |
|---|---|
| system text, "What the question asks" | "A topic's wording may ask about more than one thing. Judge the one the topic's outcome names as what is tracked. List every other part of the topic's wording that the question leaves out, a second figure or event, a condition or a comparison, in not_judged, each with one sentence on why it is not the one tracked." Two examples follow, both a second question joined by "and" (a patient count; a strike) |
| system text, "The ladder" | "A difference inside an outcome, such as an approval with conditions against one without, is not an outcome of its own; when the topic's wording names it, list it in not_judged." |
| the answer form, `not_judged` | "Every other part of the topic's wording that the question leaves out (a second figure or event, a condition, a comparison); empty only when the question leaves nothing of the wording out." |
| the closing check | "does it ask one thing, the one the topic's outcome names, and is every other part of the topic's wording listed in not_judged?" |
| the topic as the model receives it | a JSON object with the fields `description`, `outcome`, `period`, `opens_as`, `settled_by`. No field is called "wording". The first step's own answer form defines `description` as "The proposed research question" and `outcome` as "The outcome or event being tracked by this thesis" |

## 2. What the standard says

- **D397** (Alex: "只判主要那件"), asked about topics where "一题问了两件事" (his example: will the guarantee be signed, and for how much):
  "a thesis gets at most one judged question: the part its `outcome` names. Every other part of its wording is listed and shown
  beside the answer as not judged."
- **D400**, line 2: no ladder "leaves a part unlisted".
- **The reading form** defines the fields: "`description` (the topic's wording), `outcome` (what is tracked)"; its mark asks that
  "every other part of the thesis's wording that the question leaves out (a second figure or event, a condition, a comparison)
  is listed". It also notes that the question's focus line (the `outcome`) "also names parts listed in `not_judged`".

So the decision speaks of a topic that asks two things and of "its wording"; the form calls the `description` the wording and
yet expects parts named in the `outcome` to be listed. The standard does not settle a clause that appears only in `outcome`.

## 3. Every left-out clause of the seven questions, by the field it sits in

| Question | The clause | Field | Listed in how many of 3 attempts |
|---|---|---|---|
| Vera Rubin shipments | "which the company says has entered full production" | `description` | 3 |
| the Chinese permission | "allowing those sales to proceed" | `description` (and its twin in `outcome`) | 3 |
| credit support | "versus the equity investments it has made" | `outcome` only | 3 |
| purchase commitments | "versus the prior year" | `outcome` only | 3 |
| the Hugging Face closing | "versus being repriced ..." | `outcome` only | 2 |
| Blackwell to China | "so that China data-center revenue can resume" | `outcome` only | 1 |
| the cloud companies' spending | "compared with the nearly $800 billion the article says they will spend this year" | `outcome` only | 1 |
| the Chinese permission | "(versus blocking, delaying or capping quantities)" | `outcome` only | 1 |

A clause in the `description` was listed in every attempt. A clause only in the `outcome` was listed in 11 of 18. The three kinds
that went unlisted (a consequence, a comparison with the reference, a difference inside an outcome) are one case, not three.
For the $800 billion: the figure is carried as the reference in all three attempts; what two of them lack is its listing.

## 4. The model's own account (four stored attempts; the question names the clause and can lead the reply)

| Attempt | Listed the clause | Sentence it quotes | What it took "the topic's wording" to be |
|---|---|---|---|
| cloud spending, attempt 1 | no | the sentence of the first row above | "the thesis description alone" |
| cloud spending, attempt 3 | yes | the same | "the thesis's description and outcome fields" |
| Blackwell to China, attempt 1 | no | the same | "the thesis's `description` field alone" |
| Blackwell to China, attempt 2 | yes | the same | "the thesis `description` field, not the `outcome` field. On that interpretation, I should not have listed the revenue phrase" |

All four name the same sentence. Three of four read the wording as the description alone; one of those listed the clause
anyway. (Two replies add that the wording "should include the outcome field too": that follows the question's lead and is not
evidence of what the rule is.)

## 5. Verdict by the audit's classes

| Class | The request's sentence | The standard | Verdict |
|---|---|---|---|
| a clause that sits only in the `outcome` field is listed in some attempts and not in others (7 of 18) | "every other part of the topic's wording", with no field named | D397 speaks of a topic that asks two things; the reading form calls the `description` the wording | **missing**: no sentence decides the case, in the request or in the standard; the model guesses, and so did the readers |

What this audit does not find: a contradiction between two sentences; a rule for another case; an instruction that forces the
fault. And it designs nothing.

## 6. The two readings put to the council, and its ruling (round 6 of the cold thread)

The council refused the first reading below and took a limited form of the second: a part can need disclosure even when it sits
only in the outcome (D436: "a second side of the same bet ... stays as context in that question and is shown as not judged";
one of that decision's cases asks about memory demand in its description while its outcome adds whether capacity keeps pace);
not every outcome-only clause must be listed; the question is whether the clause is a distinct part the answer leaves unjudged.
The four accounts are prompted with the disputed clause and do not prove the undefined term caused every omission. The original
marks are preserved. The two readings as first written:

- **The wording is the topic's question (its `description`).** This is what D397's words and the reading form's own definition
  say. A clause Step 1 wrote only into `outcome` describes the tracked thing and is not another thing asked; listing it is
  harmless, leaving it out is no fault. Then the six attempts meet Alex's line, the two readers marked too strictly, and on the
  fresh week's seven questions no attempt fails line 2. Nothing in the frozen step changes.
- **The wording is the description and the outcome.** Then the request lacks one defining sentence. That is a new version of
  the frozen step, reviewed before any send and tested on theses that are neither Alex's 44 nor these seven; or the same rule
  owned upstream, in what the first step may write into `outcome`.

The judge is not shown the list (the reading form: "what the step recorded beside the ladder and the judge does not see"), so
neither reading changes a judgement; the list is what a reader of the thesis sees beside the answer.

## 7. The recount against D397, D436 and the rulings of the July reading (`july_line2_recount.py`, `july-line2-sheet.json`), $0

The July full run's reading (40 fresh theses, three attempts each, 91 ladders read by two families, differing marks ruled by a
third reader of each family) is the calibrated one. What it did with each kind of left-out clause:

| Kind | July: attempts that left it unlisted, and the marks | The fresh week's failed attempts of that kind |
|---|---|---|
| a comparison with the reference figure, in the outcome ("versus the roughly $650 billion they are reported to plan"; "versus the $119 billion cited in this item") | 9 attempts on 4 theses: 7 passed by both first readers; in the other 2 the Codex first reader failed it and **both third readers ruled it a pass** | the cloud companies' spending, attempts 1 and 2 ("compared with the nearly $800 billion"; the figure is carried as the reference): **a pass under the July rulings**; both fresh-week readers were stricter |
| a consequence or a remark on why it matters, in the outcome ("which would raise write-down or utilisation risk"; "as a demand pool for Nvidia's AI accelerators") | 2 attempts, both passed by both first readers; no third-reader ruling | Blackwell to China, attempts 1 and 3 ("so that China data-center revenue can resume"): **disputed**. Under D436 the company's revenue could be a second side of the bet; the July first readers passed the like |
| a difference inside an outcome, named in the outcome ("(behavioral remedies, commitments or fines)"; the scale of permitted purchases) | never left unlisted in July | the Chinese permission, attempts 1 and 3 ("capping quantities"): **stands**, by the request's own sentence |
| a second figure or event named in the topic's question | the July failures of this line: the DeepSeek investigation (a conclusion and penalties asked, a finding accepted, nothing listed: ruled a failure) and graphics-memory prices beside commodity DRAM (failed by both first readers on one attempt, split on another) | none |

So, with the original marks kept as they are: of the fresh week's six failures of line 2, two are a case the July third readers
passed, two are disputed, two stand, on one question. July's own failures of the line are a different thing (a second figure
or event of the question left out), 2 or 3 of 91 ladders.

Sensitivity only (the historical verdicts do not change): the fresh week's line 2 fails on 6 attempts as marked, on 2 to 4 under
the July rulings; its questions right in two of three attempts are 4 of 7 as marked, 5 or 6 of 7 under the July rulings.

**No omission recurs on two distinct questions under an agreed reading; no prompt change is designed.**

