**Keep the unlinked-evidence decision and stable article numbering; revise the valuation, retry, splitting, matching and measurement changes before relying on their results.** The clearest example is valuation: Alex rejected one target price, but the new prompt rejects *all* valuations, including calculated valuations the signed standard says to keep.

The code directories are untracked, so Git cannot show their previous versions. I compared the current code with the recorded changes and compared the prompt files directly.

1. **Changes**

- **c4 unlinked evidence — keep.** Alex explicitly chose to keep useful statements without a home and link them later; rejecting an unwanted cash statement instead of returning it follows that choice. This is general, and the Dell laptop example shows why it matters. The later-linking implementation still needs verification. [Decision and consequences]( /Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:961), [prompt]( /Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c4-closing.txt:15).

- **c4 blanket valuation rejection — revise.** Alex said to keep the EPS forecast and drop the particular target price; that does not establish a ban on every valuation. The signed standard keeps conditional valuations with derivation. The prompt’s wider ban drops a test item the gold marks helpful. Preserve the specific ruling and resolve the broader conflict with Alex. [His ruling]( /Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:318), [standard]( /Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:196), [observed miss]( /Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1042).

- **c5 and c6 splitting — revert c5; revise c6.** The standard supports one statement per item, but does not establish that every other party’s comment deserves its own item. c5 increased test not-kept matches from 4 to 11; the log identifies extra remarks. c6 restores the keep test and is more general, but its two-draw checks do not establish that it preserves useful combined context or fixes the whole class. [Standard]( /Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:248), [regression and revision]( /Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1200).

- **64k output cap — keep provisionally.** The 32k cap cut one article twice; it completed at 37,210 tokens with 64k. This addresses a general length limit, but one completion does not establish a sufficient cap for all inputs. [Evidence]( /Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1220).

- **Cut-answer retry and changed test — revise.** Alex authorized one retry for non-JSON or schema failures, and stopping for other failures. The code treats every `finish_reason=length` as a format failure *before parsing*; an existing test supplies syntactically valid JSON with that finish reason. A cut response can be incomplete even when JSON parses, but the claim that every cut answer “is not JSON” is false. Clarify that boundary against Alex’s decision rather than treating the old test as proven wrong. [Decision]( /Users/lchingen/hivemind/clean-arch/takeover-2026-11-07/LOG.md:763), [code]( /Users/lchingen/hivemind/clean-arch/step1/runner.py:300), [test]( /Users/lchingen/hivemind/clean-arch/step1/test_runner.py:366).

- **Step 2 criteria — revise provisionally.** “Main statement” follows the recorded merge test and is general in wording, but the reported improvement was assessed on the same cases that prompted it. The later-link criteria address five observed wrong links, yet also removed a borderline link and were not checked for missed links across all rejected candidates. The downstream reader test was not repeated. [Criteria]( /Users/lchingen/hivemind/clean-arch/step2/compare.py:54), [linking results]( /Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1116), [missing check]( /Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1166).

- **Manifest numbering — keep; reference mapping — revise.** Manifest position prevents a failed article from shifting later IDs. Mapping by input ID is preferable to shifted positions, but shared passage text does not prove two records express the same statement: the mapper selects the greatest overlap, including when one passage contains multiple statements. Its mapped-only search score cannot establish performance on unmapped cases. [Numbering]( /Users/lchingen/hivemind/clean-arch/step2/run_forward.py:31), [mapping]( /Users/lchingen/hivemind/clean-arch/step2-validation-2026-11-07/map_reference.py:36).

2. **Results and cheapest credible checks**

The c2–c7 test results are **exploratory, not held-out acceptance**: test articles were previously exposed, and test misses and scores informed subsequent choices. Scoring once *per configuration* does not undo selection across five configurations. Freeze one final configuration and assess it on fresh, independently prepared articles.

The c4 merge improvement reuses verdicts for 95 identical pairs, which is reasonable for the same pair and criterion, but does not make the 13 new, case-motivated pairs independent evidence. Blindly check a fresh set, including missed counterparts. The question comparison has one reader per run; independently re-read the consequential disagreements with source text. All forward totals are one draw; do not claim small differences are stable without repeated final and control draws. [Exposure]( /Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:908), [carried verdicts]( /Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1159), [question measure]( /Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/LOG.md:1369).

3. **Process errors, ranked**

1. **Test-set selection:** reserve a fresh set until the configuration and acceptance criteria are frozen.
2. **Decision widened beyond its source:** trace every changed sentence to the exact ruling and test the signed boundaries in both directions.
3. **Changes sent without independent challenge:** require the council to review the change, controls and stopping condition before each send.
4. **Judging a fix on its motivating cases:** include untouched cases and inspect both false merges and missed links.

4. **Next step**

Before any run, conduct one independent, source-backed review of the **complete proposed final request and its downstream checks**, including valuation, split statements, retry classification and linking. Use stored cases and record each contradiction and unresolved decision; only then choose what to change. This review establishes what the final configuration actually is before spending on another measurement.