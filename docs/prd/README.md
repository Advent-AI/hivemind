# PRD index

Each module has one Markdown specification. Select a module on `docs/system-design.html`, then open its PRD link. The system PRD link at the top opens the overview.

| File | Module | Status |
|---|---|---|
| 00-system.md | System overview | Main flow defined |
| 01-universe.md | Research universe | First version frozen; specific themes remain a draft |
| 02-classification.md | Upstream classification | First version frozen |
| 03-config.md | Config | First version frozen |
| 04-dispatch.md | Dispatch | First version frozen |
| 05-extraction.md | Extraction (read-only), and the coverage-start reading | Foundation frozen; groups declared during extraction in the default pipeline (D165); the production prompt frozen at v74i (D274); coverage-start reading built (D364), accepted and in the replay default (D366) |
| 05-extraction-standard.html | Extraction standard: ledger records, question types and opening, evidence and weight, golden set, prompt measurement | Signed (D243), open it in a browser; the one measuring standard for extraction, replacing `docs/research/2026-10-29-analyst-standard/standard.md` (D229) |
| 05-extraction-standard-corrections.md | Dated corrections to the frozen standard page: the statements later decisions changed, read with the page and never merged into it | Three records, 2026-11-05 (D368) |
| 06-views.md | Thesis library and matching records | Foundation frozen; group handoff and storage in the default pipeline (D165); other open items are in the PRD |
| 07-final-verdict.md | Closing at the due day (the final verdict retired, D356) | Decided and built (D54, D356) |
| 08-pull-mode.md | Pull mode | Decided and built (D54, D356) |
| 09-review-pool.md | Human review pool | First version frozen; intake defined, output deferred |
| 10-filing-phase.md | Current phase: filing that links facts the way an analyst does (in English since D368) | In progress since 2026-11-04; read before every step |
| 11-production-experiments-from-split.md | Production experiments drawn from the failed split extraction: what to try on production, the evidence for each, and what not to repeat | Proposed 2026-11-06 (D378); each experiment opens only on Alex's word |

## Maintenance rules

Authority: Alex's instructions, then `docs/DECISIONS.md`, then the PRDs and design page. If a PRD contradicts a decision, correct the PRD.

After **every change**, reason through every module in this order: research universe → classification → Config → dispatch → extraction → thesis library → closing at the due day → pull mode → human review pool → system overview. Compare each with the decisions and ask:

1. Does this change affect the module?
2. Do its page and PRD describe the same behaviour?
3. Do the examples still work?
4. Do the acceptance criteria or open questions need to change?

Correct inconsistencies and list what changed and why. Update decisions and current state in the same slice.

Run `python3 docs/check.py` **last**. It compares generated PRD blocks with page data, rebuilds the bundle used when the page opens from disk, runs the classification simulation and checks rendering. It reports mismatches rather than correcting their meaning. A pass is a mechanical result, not the reasoning review.
