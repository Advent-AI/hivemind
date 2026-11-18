# Claude's own audit, written before the independent read was opened (2026-11-15)

**A. The reference of an event.**
- Request, line 16: "Its kind is expected when the item states what the market expects: a consensus, the company's guidance, the
  stated plan or deadline. ... Otherwise reference is null." Schema: `words`, "the item's own words for what the figure or event
  is measured against". Form, row XR: "quotes what the article states the market expects ... an event's is null whenever the
  article states no expectation". Neither says what counts as an expectation for an event beyond "the stated plan or deadline".
- Two different things sit under the one mark. (i) "its antitrust investigation is nearing a conclusion" (one article, four
  topics in four runs): the step never quoted it (0 of 12 attempts); July's third readers failed all nine, the reading of Alex's
  44 topics held two attempts and left one open. The same words, marked differently by reading: `abstract`, in the request and
  in the form alike (a third party's statement of progress is neither plan nor deadline nor plainly "what the market expects").
  (ii) a plan stated with a time ("could begin shipping later this year", "volume shipments expected later this quarter",
  "China plans to allow ..."): the step quoted it in some attempts and left it empty in others of the same topic (Vera Rubin: 3
  of 9 quoted; the two others 2 of 3); readers fail every empty one. The sentence covers it ("the stated plan"): `misread`, or
  the sampler; by the audit's rule a change would first need the model's own account.
- No later reader: `ladder_step.py` writes a reference into the judge's view only for a figure with a value. An event's
  reference is seen by the readers of this form and by no one else.
- Worth a repair: no. Nothing a reader of the product or the judge sees would change; nine of July's fourteen marks rest on a
  reading that another reading of the same words did not make.

**B. The unlisted parts.**
- Request, line 5: "Judge the one the topic's outcome names as what is tracked. List every other part of the topic's wording
  that the question leaves out"; schema and closing check repeat "the topic's wording". Nothing says which fields that is.
- This week: parts named in the `description` were listed in every attempt (topics 2, 5, 9, 11: 12 of 12); parts named only in
  the `outcome` in 13 of 16 attempts (topics 1, 3, 6, 7, 8, 13); the three misses are the three agreed faults. D547 found 6 of
  6 and 11 of 18 on the fresh week. Its finding holds on the new cases: the same place in the request, three distinct
  questions over two weeks.
- Verdict: `missing` (no sentence says the `outcome` field is part of the wording to be listed from).
- Seen later: yes, the product shows the list beside the answer (D397).
- Worth a repair: a small one, yes: one defining clause. It must leave alone a comparison with the reference figure that the
  reference already carries (the July third readers passed those unlisted, D547's recount), and it is a change to a frozen
  piece, so a decision and a test of its own.
