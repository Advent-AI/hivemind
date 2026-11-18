# Round 21: the source check is read; a $0 integration check ran. Review deeply; then one decision toward production.

1. **Source check** (`self-report/SOURCE-CHECK-RESULT.md`, `tally-source-check.txt`): by the frozen rule **unclear** (the Codex
   family marked the Sharon-to-Firmus scaling control `weak`, expected `comparable`; families differ on case-(1) membership in 9 of
   22). Reported, not a verdict: all 11 rejected are case (1) by both families, 2 of 11 accepted; the 9 differences are one
   disagreement (Codex rejects every Sharon-to-Firmus scaling, Claude accepts it); the narrower `none_shown` is given by both to 7 of
   11 rejected and 0 of 11 accepted, the families differing on it once in 22 (post hoc, my reading).
2. **Closing step on a new-system store** (`carried-run/INTEGRATION-CHECK.md`, last section), $0 on a copy: production's
   `pull.end_of_day` closed the six due questions with their frozen band and label, under the day's own sequence, no judgement
   changed; the page then lists them closed from that day and open before. Not built: the new system's daily loop never calls the
   closing step (it stops judging at the due day).

**My reflection.** The D520 line has now run three instruments (the judge's letter, my reading of its sentences, two reader
families' marks) and none gives a rule that holds across families: the families agree only on "no amount at all is shown", and
split on scaled comparables by threshold. By the loop's rule (two rounds moved nothing), this line stops: the record for Alex is
complete enough (a product choice; what can be told apart, what cannot). Meanwhile production integration has concrete, testable
work: gate 5 (D548) has had its first defect fixed today (the page) and now has a second, known gap (closing).

**Decision proposed (one, reversible):** (A) close the D520 line with the record above for Alex, no further reading; (B) build the
closing into the new system's daily loop at its writer, as production orders it (after the day's judging round, `pull.end_of_day`,
then `complete_day`), replacing nothing in the frozen pieces: `ladder_adapter.py` only (not frozen; the base adapter stays), a
test and mutants, the extension proof re-run (no judgement before a due day may change), full suite. A replay that ends before any
due day is byte-for-byte unaffected except for nothing: the closing writes only on days a question is due. Attack: is (B) a
product change that needs anything more (does the clean runner's `due_day_guard` already imply a closing semantics that differs
from production's "frozen at the last judgement"? does any reader of the views store treat a closed question differently?), and
is there a better next step toward production? End with `CONSENSUS: yes` or `CONSENSUS: no, because …`.
