# Council mx, challenge round 3 (D493): the record test's result, and the next step

Read `docs/research/2026-11-14-use-acceptance/record/RECORD-TEST-RESULT.md`, `tally-record.txt`, `record-view.md`, the reader files beside
them (`claude-record-answers.jsonl`, `codex-reference.jsonl`, `codex-compare.jsonl`, `claude-compare.jsonl`, `codex-fidelity.jsonl`,
`claude-fidelity.jsonl`, the two `*-fidelity-settle.jsonl`), and the design `RECORD-TEST-DESIGN.md`. The stored statement behind the wrong
attribution is step 121, `ev-5`, in `poc/data/clean-lean-week-2026-11-14/week-r2/c1/step1/trace.sqlite`.

Challenge:
1. **The verdict.** "Not ready, by one line": is it the frozen lines applied as written? Is the stratum-O reading fair (one row wrong by both
   families; two rows on which the families differ twice over "Consensus analysts"; one mark traced to the packet lacking the publisher)?
2. **The defects.** Are the four the right ones, and counted right? Is anything in the answers a defect the result does not name?
3. **The next step.** Claude's candidates, in its order of preference:
   - (A) Fix what code can at the view, then test on unread articles at $0: a row of kind "actual" is shown as the company's reported
     figure, with its statement's speaker as the one citing it, never as its source (from the schema's own definition of the kinds); a
     general parser of fiscal periods (quarter and year forms) so equal periods group; no hand list of measures. Then the same six
     questions and lines on a second sample of 40 articles of the week (a new seed, none of the first 40), new readers, the publisher in
     their packets. A pass would show the record usable on stored data; the product choice of showing it stays Alex's.
   - (B) Give each figure its own party and a typed period in Step 1's schema: a new version of the frozen request, which only Alex opens,
     and a change inside the one call again, though to a field and not to an opening rule.
   - (C) Report to Alex now with the result and ask whether he wants this record as a product surface before more work.
   Is (A) a fix at the right layer or a view that hides a defect of the stored record? Does the re-test guard against fitting the first
   sample? Is there a smaller or better step?
End with: "Council position: <...>".
