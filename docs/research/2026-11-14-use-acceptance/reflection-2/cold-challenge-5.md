# The prompt audit of line 2 is done ($0.0022 of the $0.05). It finds an undefined term, not a varying step. Challenge it, and rule on the reading.

D546 records the last round with your correction of the boundaries. Audit:
`docs/research/2026-11-14-use-acceptance/fresh-ladders/PROMPT-AUDIT-LINE-2.md`; the model's accounts in `accounts.json` (four stored
attempts continued once each; the script `model_accounts.py`). You are the independent reader of this audit: check it against
`clean-arch/step4-2026-11-10/ladder/candidate-system.txt`, `candidate-closing.txt`, `candidate-schema.json`, the stored requests and
D397's record before answering.

## What the audit found

1. The request says "List every other part of the topic's wording that the question leaves out" (system text, the answer form,
   the closing check, and once more for a difference inside an outcome). The topic reaches the model as a JSON object with the
   fields `description`, `outcome`, `period`, `opens_as`, `settled_by`. **No sentence says which of these is "the topic's
   wording".**
2. Every one of the seven failed attempts concerns a clause that sits **only in the `outcome` field**. Over the seven questions:
   a left-out clause in the `description` was listed in every attempt (6 of 6); a clause only in the `outcome` in 11 of 18. The
   three kinds I told you about last round (a consequence, a comparison with the reference, a difference inside an outcome) are
   one case.
3. The model's accounts, on two questions with an attempt each way: all four quote that same sentence; three read "the topic's
   wording" as the description alone, one as description and outcome; one that read it as the description alone had listed the
   clause anyway and says that on its own reading it should not have.
4. **The standard does not settle it either.** D397 (Alex: "只判主要那件") was asked about topics where "一题问了两件事" and decides:
   "the part its `outcome` names. Every other part of its wording is listed". The reading form defines "`description` (the topic's
   wording), `outcome` (what is tracked)" and still expects parts named in the focus line (the outcome) to be listed. Both
   readers, I among them, failed the six attempts by treating an outcome-only clause as a part of the wording.
5. Verdict by the audit's classes: **missing** (no sentence decides the case). Not a contradiction, not the step's variation on
   a clear rule.

## What I ask you to rule on, under D439

The audit shows two readings. I recommend the first.

- **A. The wording is the topic's question (its `description`).** Source: D397's own words (a topic that asks two things; "every
  other part of its wording") and the reading form's own definition. A clause the first step wrote only into `outcome` describes
  the tracked thing; listing it is harmless and leaving it out is no fault. Consequence: the six attempts meet Alex's line; the
  two readings were too strict on this mark; on the fresh week's seven questions no attempt fails line 2, and by my marks none
  fails any of the six lines (the blind reader's remaining marks: the due day of the two commitment questions, which D414
  settles as code's day; the Hugging Face check date, a real conflict between "the day the topic gives" and "an obligation
  already taken on is due at its next annual filing" that comes from the first step's period; two single attempts on line 3).
  Nothing in the frozen step changes. It is a reading of Alex's line recorded as the council's, not as his words.
- **B. The wording is description and outcome.** Then one defining sentence is missing from the request: a new version of the
  frozen step, reviewed before any send, tested on theses that are neither the 44 nor these seven.

Why A: it is what the decision says; it changes nothing that is frozen; the judge never sees the list, so no judgement depends
on it; and B would spend a new version on telling a reader that a description of the tracked thing is "not judged".

What A would not mean: that the step has passed anything. Seven questions are a diagnostic sample; Stage A's lines were read on
44 theses and on 40 fresh ones and missed; this audit explains one class of those readings and says the earlier readings of
line 2 may hold the same over-strict marks. If you take A, the natural next $0 step is to count that: in the stored readings of
the July full run (40 fresh theses, three attempts each), how many of the failures of line 2 are outcome-only clauses, and what
lines 2 and 5 become under reading A. That tells us how far the step really is from Alex's lines before anything is changed.

Say whether the audit holds against the files, which reading you take and why, and whether the recount is the next step.
End with: "Position: <...>".
