Read-only check, following your round-24 review (docs/research/2026-11-05-production-plan/r24/codex-review.out). Every one of the 225 not-kept
matches in the 12 sends (212 unique record/entry pairs) went to a blind independent reader: docs/research/2026-11-06-architecture-benchmark/screen/
notkept-check-packet.json, notkept-check.prompt.md, notkept-check-reader.out (yes 197, no 10, unsure 5). Condition 2 was recomputed from the
confirmed matches for every version and for S_n: screen/recount_condition2.py, output screen/recount.txt. (The occurrence key mapping sends to pairs
is kept outside the repository; spot-check the per-send totals against sends.json with the counting aid minus the reader's "no" pairs if you can.)
Result: revised 22.67 against a bound of 21.67 with unsure counted as kept; 22.00 against 21.33 without. Condition 2 fails both ways; the self-check
holds. The missing 70th article is a dispatch-level merged copy with no extraction request in any arm, excluded from all versions alike (reported
as 69).
Check the reader's verdicts on a sample (do they apply the standard's unit: the summary's statement?), the recount, and the handling of the 69. Then
say "No remaining blocker or serious finding" and whether you agree that the revision is not adopted, or name what remains.
