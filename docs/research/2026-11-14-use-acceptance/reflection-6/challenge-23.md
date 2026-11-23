# Challenge 23: the review fixed as round 22 asked (`reflection-6/due-day/`)

Read `dueday_probe.py` (`CONTROLS`, `reading`, `material`, `final`), `review-brief.md`, `test_dueday_probe.py` and `mutants.txt`.

**Your four points:**
1. **The packet and brief:**
   - each item now uses the gate readers' own form (`build_reader_packets.item_of`), so it shows opens_as, the fiscal-year note, and
     the question, rungs and due day as the product stores them;
   - the brief lists the themes and quotes the step's decline rule verbatim (all seven cases, including the binding_obligation
     exception and the publication-day case) instead of my summary.
2. **The rendered view** is what the reviewers see. The raw ladder appears only in `other_fields`, as the gate packet has it.
3. **Strict validation:** exactly two review files, each holding every item once, with valid verdict, class and material fields.
   Otherwise the probe is NOT SCORED. Tests cover a missing row, one reviewer alone and a malformed verdict.
4. **Four known controls** are mixed in blind, taken from stored answers outside the probe's sends. A reviewer who misses one voids
   the reading.
   - **Planted defects:** sol's 2027-02-28 completion on fortnight c1/clean-6, and sol's Hugging Face decline (week c1/clean-5 d2,
     agreed unjustified).
   - **Sound:** astra's guarantee at 2028-04-03, and astra's justified two-year capex decline.

**Proofs:** tests 16 of 16. Eleven mutants, each caught by a failing assertion or an expected refusal that did not raise.

**Cost:** about $1.5, capped at $3.20. About $5.3 remains.

**Asked:** send or not?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
