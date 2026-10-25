# Dispatch

> Status: first version frozen, October 18, 2026. English edition: October 25, 2026 (D163).
> Design page: `docs/system-design.html` → New → Dispatch. Recorded decisions take precedence over this PRD.

## Purpose

The system's only entry point asks three questions in sequence to determine each item's destination.

The old system spread routing across daily steps, channel-specific text/table rules, filename-based model routing and category lists in nine modules. This design gives that decision one tree.

## Scope

Check completeness, previous processing and classification. Give categorised items a sequence number and send them to extraction. Send issues to human review.

Do not inspect subjects, filter categories already selected by the universe, choose research scope or perform date-based work.

## Decision tree

<!-- generated: tree -->
- An item arrives → **Question: Is the item complete?** (Check author, publication day, classification result and upstream ID.)
  - Incomplete → **Return**: This is an upstream problem; also place it in the human review pool.
  - Complete → Check processing records, **Question: Has it been processed?** (Use the upstream ID. An updated version is a new item with its own ID.)
    - Already processed → **Skip**: Do not pay again when upstream resends an item or a test reruns.
    - Not processed → Read classification, **Question: What is the classification result?**
      - Invalid → **Do not process**: Record the reason; unresolved lookup entries go to the human review pool.
      - Not source material → **Do not process**: For example, derived indicators we can calculate ourselves, or a file listing.
      - Duplicate item → **Merge with the original item**: Record another source for the original item; do not process it again.
      - Assigned to a category → **Send to extraction**: Include its category and sequence number; extraction reads each category differently.
<!-- /generated: tree -->

## Notes

<!-- generated: notes -->
- Grey boxes stop processing. The black box sends the item to extraction.
- Do not filter by subject here. Incoming items are already within the research universe, so dispatch does not decide which categories to process.
- Every category goes to extraction with its category-specific reading method; no manual selection. Extraction defines what each category yields.
- An unregistered publication series does not stop processing; also record it in the human review pool.
- Assign sequence numbers in arrival order, without using the computer clock. All later steps use that order.
- Processed means completed. Resume unfinished work from its recorded step rather than treating it as completed.
<!-- /generated: notes -->

## Examples

| Input | Destination |
|---|---|
| Resent Reuters item with a completed upstream ID | Skip |
| Updated version of that report, with a new ID | Process normally |
| News without publication time | Return and record in human review |
| Vendor-calculated P/E ratio | Do not process: not source material |
| FOMC statement | Extract under T11 |
| Reuters report | Extract under T7 |
| Unregistered publication series | Classify using author rules, process normally and record in human review |

## Acceptance

- Every item has exactly one destination.
- A completed upstream ID is skipped on redelivery without another model call. An updated version has its own ID. Unfinished work resumes from its recorded step.
- Every categorised item reaches extraction with its category and sequence number. Sequence follows arrival order, not the computer clock.
- Routing does not read related subjects.
- Incomplete items are returned and appear in human review.
- Without an incoming item, dispatch does nothing.

## Open question

How returned items notify upstream; decide with upstream.

## Related decisions

- D4/D18: no subject or category filtering here. D7: processing records determine prior completion.
- D10/D17: dispatch is the system's sole entry. D16: issues go to human review.
- D19/D37: first-version freeze; changes need a decision.
- D25: one extraction module; dispatch no longer branches on text/table form.
- D31: assign the sequence passed through every later step.
