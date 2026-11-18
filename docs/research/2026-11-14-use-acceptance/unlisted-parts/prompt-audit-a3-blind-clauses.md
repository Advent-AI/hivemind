The added sentence conflicts with the request’s existing instruction to list **every** omitted part. I found no decision that explicitly settles whether a restatement of an event’s own outcomes must be listed. D397’s literal “every other part” can be read to include it; D409 supplies those outcomes as the answer itself.

| Location and short quote | Decision | Verdict |
|---|---|---|
| System opening: “senior hedge-fund analyst”; “write in English”; “written once … never rewritten” | None found | No source |
| Question: “one figure … or one event”; “write a question”; resolvable on due date; figure names period and settling material | D397; D403 | Consistent |
| Question: “outcome names what is tracked”; list other parts with reasons | D397 | Consistent |
| Question: “second side … stays … as context”; list it; do not decline solely for it | D436, D397 | Consistent |
| Question: “never fold two things into one ladder”; approval/patients and fuel/strike examples | D397 | Consistent |
| Refusal: no main part; nothing checkable on a date; regulatory exception | D397, D403 | Consistent |
| Refusal: quarter or half-year; past year; beyond next year except obligation; do not rewrite as event | None found in D397–D437 | No source |
| Refusal: non-year period without publication day | D417 | Consistent |
| Refusal and object: another company or uncovered matter; name it | None found | No source |
| Object: company’s own figure, progress or obligations; world events belong to themes | D418 supports the regulatory subset | No source for the general rule |
| Object: regulator’s permission or ban belongs to theme; company sales and proceedings against company belong to company | D418 | Consistent |
| Ladder: concrete conditions; no unknown future target; no gaps or overlaps | D398, D409 | Consistent |
| Event: happened, ruled out, neither; finer differences listed | D409 | Consistent |
| Event: identify decision-maker and decision; deadline passing or continued waiting is neither; null only if no decision can rule it out | D409, D416, D420 | Consistent |
| Event: decision after item day; happened wins if both apply; merger example | D409, D416 | No source for these additional details |
| Event: investigation conclusion published, abandoned without conclusion, or still ongoing; safety-agency example | D420 | Consistent |
| Figure: five ranges; units and year forms; inclusive/exclusive bounds; full amounts and percentage convention | D398 supports ranges against reference; D409 concerns events | No source for the specific figure format |
| Ladder: exactly one of event and figure | None found | No source |
| Reference: item’s own words; consensus, guidance, plan or deadline; no invented value | D398, D405 | Consistent, but the prompt’s “own words” is **wider** than D405’s required unbroken passage |
| Reference: last reported same quantity only when no expectation; never call it expectation; carry range | D411 | Consistent |
| Reference: middle range contains the value or stated range; without a valued reference, estimate outcomes | D398, D411 | Consistent |
| Favourable end: higher/lower with reason; amount owed or committed defaults lower when unsettled; topic says more is good → higher; examples | D398, D413 | Consistent |
| Favourable end: theme figure is “n/a” | None found | No source |
| Due day: after item and on or after settling material’s publication | D403, D414 | Consistent in principle |
| Due day: model sets “expected publication”; fiscal-year conversion | D414 | **Contradicts** D414 for an estimated annual figure: code sets fiscal year-end + 60 days or calendar year-end + 90 days |
| Due day: event uses stated date or period end; pending regulatory exception | D403 | Consistent |
| Due day: binding obligation at most 548 days; next filing or signing check | None found | No source |
| Schema `no_ladder`, `question`, `object`, `not_judged` descriptions | Same decisions as corresponding system clauses | Same verdicts; “every other part” also **contradicts** the proposed exception |
| Schema `event`, `happened`, `ruled_out`, `by_whom`, `decision` | D409, D416 | Consistent; “after the item’s day” has no source found |
| Schema `figure`, `unit`, `year`, `ranges`, `lo`, `hi`, `favourable_end`, `favourable_why` | D398, D413 | Same verdicts as figure and direction clauses above |
| Schema `reference.words`, `kind`, `value`, `value_to` | D405, D411 | Consistent except “own words” is **wider** than D405’s unbroken-passage requirement |
| Schema `due_day_basis`: stated/expected publication or stated/period end | D403, D414 | **Contradicts** D414 if expected publication is set by the model |
| Closing check: one tracked thing; every other part listed | D397 | Consistent with D397’s literal wording; **contradicts** the proposed exception |
| **Added sentence:** remove restatements of happened, ruled out or waiting; keep separate consequences and finer cases | D397, D409 | **Contradicts** the existing “every other part” instructions. D409 supports keeping finer cases; no explicit source found for removing restatements |
| Closing check: contiguous figure ranges; event conditions and checkability | D409, D416, D420 | Consistent |
| Closing check: reference kind/value, middle range, fixed bounds and due-day rules; obligation direction | D398, D411, D413, D414 | Consistent except it repeats the conflicting estimated-date rule |
| Closing check: “check it once … correct” | D425 | Consistent: D425 retains a check in the same call |
| Payload `company`, `themes`, topic `id`, `description`, `outcome`, `opens_as`, `settled_by`; item date, publisher, title and text | D397, D398, D403 | Consistent as inputs; their particular contents are not decisions |
| Payload `fiscal_year_note`: FY conversion and “use [February 2027] as the due date” | D414 | **Contradicts** D414 if February is an estimate: code sets the day 60 days after fiscal year-end |
| Payload topic `period`: “24 March 2028 … set per section 3” | D403; 548-day rule: none found | Consistent as a stated event date; no source found for the 548-day rationale |
| Settings: model, strict JSON schema, token limit, reasoning effort | None found | No source |

For the added sentence’s two boundary cases:

- **Could remove something kept:** A topic explicitly contrasts completion with termination. Under a literal reading of D397, “termination” is another part of the topic’s wording; the sentence removes it as the event being ruled out. D409 itself treats that as an answer outcome, so the decisions do not expressly resolve this overlap.
- **Could keep something removed:** I found no such case in D397, D409 or D436. An approval with conditions remains listed under both the added sentence and D409; a separate consequence or second side remains listed under D397/D436.