# Reflection council "my", round 14: the $0 check is done and the stop conditions do not hold; review the revised probe design before any send

D522 recorded round 13. Nothing was sent.

## The $0 check (`docs/research/2026-11-14-use-acceptance/duplicates/historical_check.py`, `historical-check.json`)

- **Historical state:** for all four cases the production code (`extraction.shown_views`, `extraction.request_for`,
  `model.build_request`) rebuilds the stored reading request from the stored article and the run's store read at the day's start,
  with the stored archive key. The list "committed before the article" comes from the same code with the store read at the
  article's sequence minus one (groups, other names and parents as of that sequence); no line is typed by hand. As you warned, it
  differs by more than one question: the Rubin article's list gains two questions and another question's line changes.
- **Checks in isolation:** each stored answer through `sift_with_groups` and `file_reading` on the day-start list gives exactly the
  stored handover (four of four). A synthetic answer linking the statements to the earlier question is kept under it on the
  per-article list and not on the day-start list.
- **A third same-day case:** the fresh week's third agreed duplicate pair (fiscal 2028 amount and growth, `v3` and `v5`) was also
  opened by two articles of one day (11 and 22 of 09-22); my candidate list had missed it because those questions share no research
  group. So all three pairs both teams called duplicates are same-day cases.

By your stop rule: the earlier question can be reconstructed at the tested sequence; the checks can be exercised without the final
store's later state; the cases that support the expected duplicate treatment are the three fresh-week pairs. The July pairs are
left out as unsettled.

## The revised design (`duplicates/VISIBILITY-PROBE-DESIGN.md`; script `visibility_probe.py`, run dry; the changed request of one case in `changed-request-rtx.txt`)

Against your five points:
1. Named an isolated visibility probe, not a D375 replay; the changed arm is the production code's own list at the article's
   sequence; the heading's "at the start of <day>" wording is disclosed.
2. The control is rebuilt by production code and matched to the archived key before anything else; the empty-list case needs no
   hand edit (the code prints the list).
3. Every answer goes through the production checks and filing on its own arm's list.
4. Outcomes fixed before the send on source-backed statements: the passages the stored answer filed under the question it opened
   (kept, and under which question), a second question on the matter (two marks, one blind), everything else printed. Two
   separate controls that should still open their questions when shown an unrelated earlier same-day question (the article that
   opened fiscal 2027 and 2028 revenue after the financing question; the article that opened gross margin after Rubin shipping).
5. The rule names "exercised", "supports", "does not support" and "inconclusive", reports all three sends of each arm, and bars
   reading a failed probe as a finding about the comparison step.

Cost sized on the rebuilt requests: 30 calls, $0.159 if every call used its whole 8,000-token allowance; ceiling $0.25.

Review it as the independent read before a first send: the full changed request against the frozen prompt and D375; the case and
control definitions; the rule; anything that would make the result unreadable. Say "send" only if you find nothing serious; else
name what must change. If you hold that this probe should not be sent at all while Alex is away, say so and why.

End with: "Council position: <...>".
