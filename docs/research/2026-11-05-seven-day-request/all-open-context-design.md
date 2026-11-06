# All open questions before each item

Alex, after being offered the existing article-subjects-plus-themes rule and the recommended all-open rule with the five-case context cost: “改 work on it”. This is taken as approval of the recommended all-open rule. The stopped seven-day run stays stopped; this slice changes the experimental split path and the design, not the frozen production replay or the ruler.

The prior lookup silently omitted 13 new `research:` company questions from every later saved A/B snapshot, even when the article directly described the same investment or product. The exact subject-recognition defect is recorded in `subject-context-investigation.zh.md`. Showing all open questions prevents visibility from depending on subject names, ticker aliases or incoming tags; it does not repair wrongly stored issuer identities and does not itself prove that the model makes the correct use of context. It supersedes D264's subject selection for this design and preserves D375's per-item timing.

## State × event

| State/event | Read, transition and write |
| --- | --- |
| First item | All questions open immediately before its dispatch sequence, including prior-period starting questions. |
| Earlier article commits a new company, unknown company or theme question | It is included before the next item, irrespective of that item's tags. |
| A and B for the same item | Both get the identical immutable pre-item snapshot; A finds new questions and B links evidence. |
| Question opened at current/later sequence | Excluded until a later item. |
| Question closed at/before the prior sequence | Excluded; a later close must not leak into an earlier snapshot. |
| Refusal, model failure, partial write, crash or restart | Existing runner records/recovers the stage; no new snapshot is fabricated. The manifest pins the code and requests; a changed configuration cannot reuse an old request. |
| Concurrent/other writer, configuration/input correction | Dispatch sequence and committed state govern visibility; an old snapshot/request must not be reused as current. The experiment processes one item at a time. |
| No open questions | Both calls receive an empty list; no question ID is invented. |

## Value × reader / new path × checks

`latest_library` supplies one ordered snapshot to A, B, B's permitted-ID pattern, matching, and the archived request/`shown.json`. The stored rows keep their original object, dates and evidence; model subject classification is not silently rewritten. Every row must exist by the preceding sequence and have an open switch at that sequence. The current question list is checked against source-backed real snapshots, A/B request builders, question-link checks, and the real writer-to-next-article path. All-open changes the model request, so cached answers from the subject-only configuration cannot establish its quality. No cap, company list or importance gate is introduced. Larger payloads can affect model behavior and provider limits and must be measured; five historical A+B requests had an estimated additional 4,954–24,562 text tokens.

## Proof

Replay all saved article snapshots with the new selector and count open questions gained and any prior questions lost. On a temporary real ledger, prove open/closed and same-sequence boundaries, show that an untagged unknown-company question reaches both A and B and a later source-backed B record is written to it. Replay at least the Fed, NVIDIA investment, and RTX Spark saved snapshots (the three named hidden cases). Mutate the selector back to subject-only on a scratch copy: the decisive test must fail. Run touched tests and standing checks, then a small real A/B probe on a source and its actual pre-item library to inspect what the model does. A paid probe is a few calls, not a resumed seven-day run; no run starts without a new request.

## Results

The split selector now includes every open question as of the preceding dispatch sequence. On 118 saved A snapshots, 99 gained questions (2,435 additional question appearances total); none of the 8,415 previously shown question appearances disappeared. The three named previously hidden questions v82, v105 and v109 are included in their later relevant article snapshots. These are exposure counts, not counts of helpful questions.

The real-writer test created an unknown IREN company question, then built A and B requests for a later actual article whose upstream labels omit IREN; both requests contained the new question and a source-backed fake B answer was written to it. Separate tests covered close/reopen and same-sequence boundaries. A scratch mutation restoring the old subject filter failed at the missing-question assertion. The existing same-day write, restart and split request checks passed. Full suite: 241 passed, 61 skipped; PRD/page structural check passed.

The original 1285 article's A and B request bytes were rebuilt exactly from its saved inputs, then re-sent with only the expanded pre-item question snapshot. Previously v105 (the NVIDIA–MediaTek investment) was absent from 92 shown questions, A proposed it again, and B did not link to it. In the new single draw, all 104 questions including v105 were shown; A proposed no new question. B still did not extract the article's opening description of the investment for v105. The latter is a separate existing-question evidence miss and remains open; the context change alone is not accepted as evidence-quality improvement. The three B records in that draw passed the quote check. Raw requests and provider answers are in `poc/data/all-open-context-probe-2026-11-05/`.
