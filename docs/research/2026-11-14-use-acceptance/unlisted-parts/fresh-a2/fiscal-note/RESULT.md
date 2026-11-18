# The shared fiscal-year note, audited (D607's step), 2026-11-16, $0

**Who reads the note** (`universe.fiscal_note`):

- production extraction's request (`src/hivemind/extraction.py:387`, frozen);
- the answer-choice step's payload (`clean-arch/step4-2026-11-10/stage_a/stage_a.py:144`, frozen as the ladder step, D426);
- the gate-1 readers' packets (`stage_a/build_reader_packets.py:35`).

For NVDA the note ends: "FY2027's full-year figures are published in the annual report around 2027-02; use that day as the due
date". The shared function is not edited.

**What the clause could reach in the answer-choice step:**

- **The shown day (`ladder_step.due_day_of`):** code replaces the model's day only when the model chose the basis
  `expected_publication` (D414: year-end plus 60 days for a company figure). A `stated` day is kept. So the clause could reach the
  product only through the model's choice of basis, or through the `stated` days it writes.
- **`basis_census.py`** → `basis-census-output.txt`: 202 distinct company-question answers from the frozen step (probe readings'
  control sends only):

  | Basis | The day falls in the note's month | Another day |
  |---|---|---|
  | `expected_publication` (code sets D414's day) | 23 | 102 |
  | `stated` (code keeps the answer's day) | 3 | 74 |

  - The 23 `expected_publication` answers in the note's month are model days that code replaces.
  - The 74 `stated` answers on another day are, as read, events and amounts with a deadline the question itself names: shipments by
    2026-12-31, the Hugging Face deal by 2028-03-24, a guarantee by 2027-12-31.
  - The 3 `stated` answers in the note's month are one matter: "Rubin volume ramp by January 31, 2027, shown by the fiscal Q4
    earnings release", dated 2027-02-24 or 2027-02-28, the release that settles it. That is defensible as stated, and not shown to
    come from the note.
- **Year:** the year mapping ("this year is FY2027 …") is in the note's other clauses, which no change proposed here would touch.
- **Refusal and rung:** nothing in the stored answers links either to the due-day clause.
- **The check before code's replacement (round 150):** for `expected_publication`, code first refuses a written day before the
  year's end (`ladder_step.py` check 5). The note's "around 2027-02" gives the model a day after the year-end. Removing the clause
  could therefore raise code refusals, so the clause is not inert. A change would need that measured.
- **The D split** (D590: Codex readers fail D on code-set days): the readers' packet shows the same note beside D414's day.
  - Removing the clause from the step's request would not change the packet.
  - Changing the packet is a change of the reading form, which D590 decided against.
  - **The cause of the split is not established:** the D-only diagnostic did not reproduce the split, so the packet's note is a
    candidate cause, not a shown one.

**Result by D607's criterion:**

- No product-visible effect is shown: the shown day is D414's or the question's own deadline.
- The reader split's cause is not established, so no gate-relevant effect of the request is shown.
- **Closed as a cleanup-only lead.** The step's request carries a due-day instruction that code overrides (AGENTS §3 and §6). No new
  version and no paid send follow.
