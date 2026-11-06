Round 2 of the read-only review of the benchmark results reading. Your round-1 review: docs/research/2026-11-05-production-plan/r16/codex-review.out.
The reading is now revision 2: docs/research/2026-11-06-architecture-benchmark/results/results-reading.md. New since round 1:
- results/judgement-drops-reader.out: an independent reader on v9 and v10 (the design's required read);
- results/blind/hits-extras-reader.out: twenty hits and twenty extras of each arm read blind (keys kept outside the repository; the per-arm
  counts are in the reading);
- results/prompt-audit.md (Claude's audit of the failure classes) and results/prompt-audit-b-reader.out (a blind second reader's audit of B's
  whole request, results/b-request-dump.md);
- the ladder and due-day counts of new questions; the readers' reasons for the split questions the standard would not open.

For each of your seven round-1 findings say resolved / partly / not, with the line you read. Then judge the revised one recommendation and its one
test (reading §4) against AGENTS §6 and §7.3: is it written from the standard's line, does it avoid fitting the bench, is the test balanced and
able to refute the recommendation? Report any remaining blocker or serious finding (file, line, problem, fix), or say "No remaining blocker or
serious finding" and whether you agree with the reading and the recommendation. Out of scope as before.
