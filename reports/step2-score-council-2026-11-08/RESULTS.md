# Jev retrieval score probe: interrupted; partial result

Alex requested a small council test of whether supplying embedding scores helps Jev. The isolated probe used fixed archived c8 inputs, 11 selected cases, two arms (original control, and real cosine metadata plus query type), 3 same-day draws per arm. It was not a new acceptance measurement, was not a forward run, and cannot measure a change in retrieval recall. The design, frozen manifest and hashes, preflight and source-blind review are in this folder. Frozen rulers, production and the concurrent Step 1 configuration did not change.

## Status

The seventh case's first dispatch (`18:e2`, treatment draw 1) failed with `ConnectionResetError` after 36 successful answers. Whether that request reached the service is unknown. Per the predeclared single-attempt stop rule it was not retried; 29 further planned calls were not sent. Six cases have all six answers; five cases have no complete paired result. In particular the known wrong merge (`22:ev-11`) and revision-bearing example (`19:ev-guidance-70`) were not reached. Six completed cases carry 46 candidate comparisons; control and treatment each have three decisions per candidate. Logged successful input tokens 136,590, logged cost $0.005742; the ambiguous request's actual billing is unknown.

## Observed outcome

Every one of the 46 candidate relation choices was identical in all six draws. The resulting groups and revision links were also identical in all six: 3:e1 repeat of 1:e3; 5:e1 new; 9:e1 new; 9:e6 repeat of 7:E1; 13:e11 repeat of 6:e1; 14:e3 repeat of 7:E4. No revision links occurred. For 5 of the 46 candidate comparisons, the mean reported same-statement probability differed across the arms; one example was 9:e6 against 7:E1, control 0.77/0.74/0.79, treatment 0.84/0.84/0.86. Probabilities do not establish accuracy or explain a cause.

Two independent blind readers each read source materials and all 46 candidates for these cases, and agreed: 3 same, 42 different, 1 overlap. In particular 13:e11 groups a three-cloud growth record into an AWS-only record; both blind readers call it an overlap. Do not count that as unambiguously right or wrong. The other three repeat targets were both called same, and both new cases had no candidates called same or revision. Later details remain preserved as member text; the score does not fix the overlap.

## Interpretation and stop

No visible decision benefit or harm in the six completed selected cases. This is not evidence of equivalence or a measured precision/recall change. The wrong-merge case central to the prediction and the revision-bearing case were not run. The score input also adds query-type metadata and can encode thesis/period content missing from the comparator; an effect could not be attributed to numerical similarity alone. Complete result and two source-backed reviews do not exist for the intended 11 cases. Stop and report the interruption, no automatic resumption or replacement of the ambiguous call. The independent Codex partial review is `partial-review.out`; independent Claude follow-up is `partial-claude.jsonl`. No adoption or product change is justified by these results.

Council post-read: Codex and Claude independently agreed on the six completed outcomes and their limits. Claude's partial review says 106 total candidates across eleven cases; the frozen packet and complete blind annotations contain 96, so 106 is a counting error and is not used. The three reader disagreements lie in unfinished cases. The connection reset's cause is not established; the logged exception is its type only.
