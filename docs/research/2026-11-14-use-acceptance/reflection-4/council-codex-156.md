Version 2 is closer, but I would not build it yet. Two cases in particular remain undefined: **how to identify a refused yearly view**, and **what the surviving view says when its sibling was never written**.

1. **Give every yearly attempt an identity, even without a view.** A `(thesis_id, view_id)` key cannot reliably distinguish two refused years when both have `view_id = NULL`; SQLite permits multiple `NULL` values in a composite primary key. Use a non-null attempt identity or year, and specify how ordinary unsplit and refused rows remain unique. The existing [control reader](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/control_theses.py:72) fetches one row per thesis, so listing it is not enough: specify what it and every other reader should do with two.

2. **Make the “not judged” rule depend on the result.** If the 2026 view is written and the 2027 attempt refuses, omitting 2027 because “its sibling judges it” misleads the reader. Specify the list when both succeed, only one succeeds, or neither succeeds, including what becomes visible when. Test those states in the bundle and page.

3. **Define the transaction and recovery boundary.** The current loop commits article writes before judging; it is not day-atomic. [Replay](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:489) Specify where the model calls and their archived results sit relative to the transaction, what survives a crash after either call or after the view commit, and whether recovery can duplicate a paid call or a view. The assertion that a crash leaves none needs a real-path proof.

4. **Make the reading rule decisive.** The brief says readers use the gate marks, but the verdict only vetoes a base-year question or lost qualification. It could call a lead when a child has a wrong question or overlapping ranges. Specify which settled marks veto, and how unresolved points, missing rulings, refused children and missed plants affect both countings. The control rule should also report controls whose frozen sends disagree as unexercised for outcome-kind regression.

The title’s statement that D397 remains unchanged also conflicts with §1’s correctly named departure. Fix that wording and record the proposed D439 decision before any build.

The typed case remains a behavior change. A year pair is only a structural check; the model’s judgment that both years are independently asked is the boundary the controls must exercise. The planned design should also state a spend bound that includes parent calls, child calls and retries.

CONSENSUS: no, because the partial-result representation, recovery path and verdict are not yet complete enough to build.