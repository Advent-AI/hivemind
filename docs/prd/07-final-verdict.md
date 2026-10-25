# Final verdict

> Status: earlier draft, to be redesigned with pull mode. Due-date state freezing is decided (D54). English edition: October 25, 2026 (D163).
> The earlier draft uses the pre-D38 library. Its verification conditions, confirmation/falsification, premises, seven-day fallback, same-tier-disagreement escalation and waiting rules no longer apply.
> Design page: `docs/system-design.html` → New → Final verdict → Details. Recorded decisions take precedence.

## Current decision

Pull mode freezes a thesis at its current rung and closes it when due. Whether a separate final-verdict step is still needed remains open. The earlier draft used a complete model review before closure.

- A thesis has one state and no separate settlement judgement. Decisive information, such as annual results or an official action, enters normally as evidence and can move the state.
- Freeze the current rung on the due date and close the thesis. Dependencies read its closing state and reasons.
- Pull mode runs at day-end or scheduled intervals without an additional wait.
- Example: NVDA FY2027 China results move the thesis to “down at least 80%”. Day-end pull freezes that rung and closes it.

## Open question

The original rationale was to review all evidence before closure. Rejudgement now already reads all evidence still in force. Claude proposed handling closure in pull mode without a separate step; this is not approved. Retain final-verdict Config settings until the decision.

## Earlier draft (D29): no longer the current contract

Before closure, the model reads the thesis, all evidence, premise states and trigger, then closes it as confirmed, falsified or expired, or keeps it open.

### Original rationale

Alex requested a complete review before closure. A single condition or evidence item shows only part of the picture. As with predeclared investment exit criteria, the earlier draft required predefined verification conditions and factual evidence; a larger number of opinions was insufficient.

### Triggers

<!-- generated: triggers -->
| Trigger | Detected by |
|---|---|
| Confirmation or falsification condition met | Code |
| Deadline reached | Pull mode, after all items published no later than the deadline have been processed |
| Premise status changes: falsified, expired, confirmed, superseded or no longer tracked | Code, immediately |
| Premise weakened | At the subject's next item, or within seven days via pull mode |
| Weakening evidence arrives in the fact tier | Code |
| Disagreement: independent sources within one tier support and weaken the thesis | Code |
| A revised source item removes the thesis's basis | Code |
<!-- /generated: triggers -->

### Outcomes

<!-- generated: verdict -->
```
Final verdict | Does this thesis still hold? (The model reads the thesis, all evidence, premise states and trigger)
├─ Confirmation condition met with factual evidence → Close: confirmed (Identify the evidence used)
├─ Falsification condition met with factual evidence → Close: falsified (Identify the evidence used)
├─ Deadline reached without decisive evidence → Close: expired (Record “no data to verify”, neither success nor failure)
└─ Other cases → Keep open (May remove or replace premises and add verification conditions specifying decisive facts and when they can be known)
```
<!-- /generated: verdict -->

### Rules

<!-- generated: rules -->
1. The model reviews the thesis, all evidence, current premises and trigger in one judgement.
2. Only verification conditions plus factual evidence can establish confirmation or falsification. Third-party views and rumours alone cannot. Expiry is not a correctness judgement.
3. Write a new thesis version citing evidence and sources. Retain closed theses for historical lookup.
4. Closing a thesis sends each thesis that uses it as a premise to another final verdict.
5. Pass “now” into pull mode: real time in production, replay time in tests. The system owns no clock.
<!-- /generated: rules -->

### Example

In August 2025, reported Commerce issuance of H20 licences meets the old falsification condition for a tightening-controls thesis. Code sends it for a complete review, and the model closes it as falsified, citing the official-action report.

Its dependent NVDA thesis about China data-centre revenue approaching zero is then reviewed. Reported Chinese procurement restrictions still prevent revenue recovery, so that thesis remains with a new premise.

### Earlier acceptance criteria

- No closure without a final verdict.
- Third-party views and rumours alone cannot confirm or falsify a thesis.
- At expiry without decisive evidence, record “no data to verify”, neither success nor failure.
- Write a new version with evidence, sources and Config version.
- Wait until all items published no later than the deadline are processed before an expiry verdict.
- Closing a thesis sends every premise-dependent thesis for another review.

### Earlier open questions

- Judge multiple triggered theses for one subject separately or in one call.
- Validate the provisional seven-day fallback interval on data.

## Related decisions

- D14: pull mode owns scheduled and expiry work.
- D29: earlier pre-closure review, superseded by D54 state freezing.
- D30/D31: earlier contradictory-statement and premise-change rules, superseded by D38 dependencies.
- D54: freeze and close at the due date without a separate result or extra wait; decide the separate step later.
- D55/D56: label obsolete rules and their historical decision references explicitly.
