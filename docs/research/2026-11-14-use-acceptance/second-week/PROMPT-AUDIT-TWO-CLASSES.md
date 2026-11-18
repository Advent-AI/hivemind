# Prompt audit of the two classes that are the answer-choice step's own (D557, under D439), 2026-11-15, $0 of provider calls

By the prompt-audit procedure: the whole request read as the model reads it (the 23 lines of
`clean-arch/step4-2026-11-10/ladder/candidate-system.txt`, the closing check, the schema's descriptions, a stored user message),
each class mapped to the sentences that decide it, against the decisions (D397, D411, D436, D547) and the reading form. Two
reads made apart: Claude's, written first (`proofs/audit-own-read-before-the-second-reader.md`), and a fresh read-only Codex
session that was given the same material and not Claude's verdicts (`AUDIT-BRIEF.md`, `proofs/audit-second-reader.md`). Cases:
`proofs/audit-cases.json`. No candidate text is written here. The reader sessions' dollar cost is not known.

## The verdicts

| Class | The request's words | The decision or the form on the same case | Verdict (both reads) | Does a later reader see it? |
|---|---|---|---|---|
| An event's reference left empty, where the article states a plan with a time ("could begin shipping later this year"; "volume shipments expected later this quarter"; "China plans to allow ...") | line 16: the kind is expected "when the item states what the market expects: a consensus, the company's guidance, the stated plan or deadline ... Otherwise reference is null" | form, XR: "quotes what the article states the market expects"; "an event's is null whenever the article states no expectation" | **misread**: the sentence covers a stated plan, and the step quotes it in some attempts and not in others of the same topic (Vera Rubin: quoted in 2 of 3, 1 of 3 and 0 of 3 attempts on three topics; the two others in 2 of 3) | not in the judge's view as built: `ladder_step.py` writes a reference into it only for a figure that has a value. What a later product view will show is not settled by this |
| An event's reference left empty, where the article gives a third party's statement of progress ("its antitrust investigation is nearing a conclusion"), or an expectation about another measure (a revenue share beside a ramp) | the same line: neither a plan nor a deadline is plainly stated | the form does not say whether a progress report is an expectation | **abstract**, in the request and in the form alike; and for the marks, **not the prompt**: the same sentence with the same empty reference was failed in all nine July attempts and held in two of three attempts of the earlier reading | no |
| A part of the topic left out of the question and not listed (this week: two further figures the `outcome` names, on two topics) | line 5: "Judge the one the topic's outcome names as what is tracked. List every other part of the topic's wording that the question leaves out"; the schema and the closing check repeat "the topic's wording" | D397: every other part of its wording is listed and shown beside the answer as not judged; D436: a second side of one bet is shown as not judged | **missing**: nothing in the request says which of the topic's five fields "the topic's wording" is | not in the judge's view as built, and nothing yet built shows it; D397 decides that the product shows it beside the answer, so it matters to the product as intended |

## What the two reads found beyond the verdicts

- **The event reference is two things under one mark.** Nine of July's fourteen event marks are the one sentence about the
  French inquiry, which the step never quoted (0 of 12 attempts over four topics) and which the readers of another reading
  mostly held. The other five, with two in Alex's topics and one this week, are chance omissions of a plainly stated plan.
- **Counterexamples a repair would have to leave alone:** the many events with no stated expectation, held empty by both
  families (24 of 27 in Alex's topics, 15 of 29 in July, 6 of 8 this week); the quotations already made; and it must not turn
  a figure about another measure (a 20% revenue share) into the reference of a ramp.
- **The unlisted parts: D547's finding holds, its count does not carry over.** The request leaves the field undefined; that
  much is the same on the new cases. But where a part "sits" depends on the reading: by the second reader's sorting, parts
  named only in the `outcome` were listed in between one and three attempts of three, and so were parts of the `description`
  (the 25% clause of topic 8 once in three; the signing of topic 11 once in three). The pattern "the description always, the
  outcome sometimes", which Claude's own read repeated from D547, is not established on this week.
- **A correction to Claude's own read:** it said the product shows the list beside the answer. That is what D397 decides; no
  product view of the new system exists yet, and the judge is not shown the list.

## Is a general, product-relevant repair worth designing?

The two reads do not say the same here, and the difference is kept.

- **The event reference.** The second reader: worth considering only for consistent recording; the judge gains nothing
  until it can see the reference; a repair could wrongly equate a revenue share with a ramp or erase a valid plan. Claude:
  no. The council's judgement (D558): no repair now; it stays recorded as a matter of the reading form, beside the due-day
  conflict.
- **The unlisted parts.** The second reader: worth designing, because readers should see what an answer leaves out (D397);
  it could clutter an answer with context or cut one bet into fragments. Claude and the council: deferred, not dismissed.
  Today nothing reads the list, the step is frozen (D426), and the count the first read leaned on did not hold up; it is a
  candidate for the day the list has a reader or the day Alex wants this gate pursued as written. That a single defining
  clause would be enough is a guess, not a finding of this audit.
- By the procedure's own stop: where the request states the rule plainly and the cause stays uncertain (the chance omissions
  of a stated plan), the next thing would be the model's own account, which is a paid call and a later decision.
- What the audit supports as a whole: no bounded, product-relevant repair is ready on the present record. It does not show
  that every remaining miss is a rule working as intended: the map also holds wrong questions, doubtful answer choices,
  disputed readings and refusals both third readers call unjustified.
