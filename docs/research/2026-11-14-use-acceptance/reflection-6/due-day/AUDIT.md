The proposed change removes the instruction to use the annual filing date for a signed deal’s **completion**. The unchanged reader brief still applies that instruction, so it can mark the proposed answer as wrong.

**Request audit**

| Sentence or clause | Verdict against the cited standard |
|---|---|
| The question must be resolvable on its due date; the day must follow the item and be on or after the settling material’s publication. | **Consistent** with the [design table](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:285). |
| For a figure, use the stated publication date or `expected_publication` when the model estimates it. | **Contradicts** D414 as a complete instruction for an annual figure: D414 assigns the unstated day to code, although the request tells the model to estimate it. The reader brief describes the code-set day. |
| For an event, use a stated date or the named period’s last day, with fiscal year-end for an undated pending regulatory decision. | **Consistent** with D403. |
| Proposed binding-obligation clause: within 548 days; an **amount** already taken on uses the next annual filing; an unsigned obligation uses its signing-check day. | **Consistent** with D210 and D185, provided the signing-check day also satisfies D403’s stated-date or period-end rule. |
| Frozen clause: an **obligation** already taken on uses the next annual filing. | **Keeps wider** than D210: it also covers an event asking whether a signed deal completes. It conflicts with D403 when that event has a different stated date or period end. |
| System and schema refusal when an event has neither a date nor a period, except for the pending-regulatory case. | **Consistent** with D403. The schema’s figure exclusions are also consistent with D414’s limit on the annual-figure rule. |
| Schema `due_day_basis`: `stated` or `period_end` for events; `stated` or `expected_publication` for figures. | **Consistent** as labels, but it does not itself explain D414’s code-set day for annual figures. |
| Closing check: the event’s outcomes must be checkable on the due day, and the due day must follow the rules above. | **Consistent**, but it repeats the request’s rules and does not resolve the annual-figure inconsistency. |

The decisions are in [D185, D210, D403 and D414](/Users/lchingen/hivemind/docs/DECISIONS-log.md:2472).

**Cases**, assuming each date is after the item and within the 548-day limit:

- Signed acquisition, stated check date: **proposed:** stated date; **frozen:** annual filing clause competes with that date.
- Same acquisition, period only: **proposed:** period end; **frozen:** annual filing clause competes with period end.
- Purchase-commitment amount at the next annual filing: **both:** next annual filing; an unstated annual-figure date is subject to D414’s code rule.
- Unsigned deal’s signing: **both:** stated signing-check date or the named period’s end; neither permits an invented event date.
- Guarantee becoming final, stated date: **proposed:** stated date; **frozen:** if the obligation is already taken on, its annual-filing clause competes with that date.

No remaining proposed sentence directs signed-deal completion to the annual filing. The change leaves **no day-selection gap**: the general event rule supplies the stated date or period end, and an event with neither is declined. A date beyond 548 days creates a constraint conflict, not permission to invent another day.

The [reader brief’s D row](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md:98) still says **any** obligation already taken on is due at the next annual filing. Thus it can fail the proposed stated-date or period-end answer for signed-deal completion—and for an already-taken-on guarantee becoming final—when that day differs from the filing date.

NOT CONSISTENT: the unchanged reader brief applies the annual-filing rule more broadly than the proposed request, and the request’s annual-figure estimate instruction conflicts with D414.