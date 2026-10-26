# PRD index

Each module has one Markdown specification. Select a module on `docs/system-design.html`, then open its PRD link. The system PRD link at the top opens the overview.

| File | Module | Status |
|---|---|---|
| 00-system.md | System overview | Main flow defined |
| 01-universe.md | Research universe | First version frozen; specific themes remain a draft |
| 02-classification.md | Upstream classification | First version frozen |
| 03-config.md | Config | First version frozen |
| 04-dispatch.md | Dispatch | First version frozen |
| 05-extraction.md | Extraction (read-only) | Foundation frozen; D149 grouping requirement integrated by D165; category prompts still need validation |
| 06-views.md | Thesis library and matching records | Foundation frozen; D149 group handoff and storage integrated by D165; other open items are in the PRD |
| 07-final-verdict.md | Final verdict | Earlier draft, to be reconsidered with pull mode; due-date freezing is decided |
| 08-pull-mode.md | Pull mode | Earlier draft; day-end/scheduled work and due-date freezing are decided |
| 09-review-pool.md | Human review pool | First version frozen; intake defined, output deferred |

## Maintenance rules

Authority: Alex's instructions, then `docs/DECISIONS.md`, then the PRDs and design page. If a PRD contradicts a decision, correct the PRD.

After **every change**, reason through every module in this order: research universe → classification → Config → dispatch → extraction → thesis library → final verdict → pull mode → human review pool → system overview. Compare each with the decisions and ask:

1. Does this change affect the module?
2. Do its page and PRD describe the same behaviour?
3. Do the examples still work?
4. Do the acceptance criteria or open questions need to change?

Correct inconsistencies and list what changed and why. Update decisions and current state in the same slice.

Run `python3 docs/check.py` **last**. It compares generated PRD blocks with page data, rebuilds the bundle used when the page opens from disk, runs the classification simulation and checks rendering. It reports mismatches rather than correcting their meaning. A pass is a mechanical result, not the reasoning review.
