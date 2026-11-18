# The typed-unit audit contract (D446), fixed before any case is read against it, 2026-11-13

A proposed representation of a Step 1 thesis's unit, to audit on stored data ($0): not established facts, and no permission for code to
decide which questions matter (the model still decides whether to open and what is worth tracking; AGENTS §2). Agreed in council round
mm-4 (`clean-arch/step1-unfiled-2026-11-08/council/mm-codex-4.md`).

**Fields.**
- `kind`: quantity or event.
- For a quantity: `measure` (what is counted), `scope` (whose, which parts), `period`: one calendar year, one fiscal year, or a comparison of
  exactly two named years.
- For an event: `event` (what happens).
- For both: `check_date` and its `basis`: a date the item gives; a date derived from a publication (the release of a period's figure, the
  next annual report); an event's resolvable milestone; or a rule of the standard (a pending regulatory decision with no date: the current
  fiscal year-end; an unsigned obligation: a day within 18 months of the item on which signing can be checked; an undertaken obligation's
  amount: the next annual report). A valid event date need not be printed in the article.
- For an obligation: `signed` (yes, no, unknown) and `undertaken` (yes, no, unknown), which may both hold; an unsigned obligation's
  signing is an event, an undertaken obligation's amount a quantity.

**Values.** Read from the stored thesis and its answer only. A missing thesis, a field the answer does not supply, or contradictory text
is recorded as unknown or unavailable, never reconstructed from the ruler.

**For each case** (the 16 losses, the unresolved cases, the correct controls: the clean draws' agreeing and eligible theses and the sound
Stage A theses; and the D441 memory and capex neighbours): the field values; whether code could detect the error from those values alone;
whether detection would only refuse or could recover the missing question; which correct theses the check would reject and what each
rejection costs the final judgement. Stage A's declines are classed by DIAGNOSIS.md (two of the three "two figures" declines are Step 4's
wrong refusals).

**Stop the typed-unit line** if a catch needs invented values, if it mostly refuses without a path to recover the question, or if it cannot
tell a correct comparison or related evidence from an invalid combination. The audit shows feasibility and risk only, not how a model
would fill a new schema or the effect on final judgements.
