# Design: a thesis the ladder refuses is not open (fix 1 of PATH-TO-PASS; $0 design, nothing built)

**The defect** (census C)
- Step 1 runs over the whole window before the ladder, so a thesis the ladder later refuses stays in Step 1's open-thesis state.
- Later items file their evidence under it and never open a well-formed thesis.
- In the two new draws, capex, DRAM, Groq and the neocloud matters were lost this way.

**The rule, owned by code (identity, not judgement):** a thesis is open only once the ladder has accepted it.

**Where it goes:** in Step 1's item loop (`clean-arch/step1/runner.py` `run`), after an answer is checked. Each new thesis of that answer is
laddered at once, with the frozen ladder request (astra-frozen, pass 1, the same thesis and item fields `build_cases` writes).
- **Accepted:** the thesis enters `theses`, which is the next item's open list. Its pass-1 ladder is stored with the trace row.
- **Refused:** the thesis does not enter `theses`.
  - The evidence the answer linked only to it is kept unlinked (D383), so the later-linking step can file it.
  - The refusal and its reason are recorded on the trace row.
- **The pipeline's ladder component reads the stored pass-1 ladders** and runs passes 2 and 3 as now, for D400's checks.

## State × event
| State | Event | Transition and what is written |
|---|---|---|
| Item answered, new thesis proposed | Ladder accepts | The thesis is added to `theses`; the ladder is stored on the row; the next item sees it |
| Same | Ladder refuses (one refusal note and one resend, stage_a's rule) | Not added; the refusal and its reason are on the row; evidence linked only to it goes unlinked |
| Same | Ladder transport failure after its retries | The row is failed with its reason; the run continues; the thesis is not opened. Recorded beside D449: a format or transport failure at the ladder is not a refusal |
| Same | Crash midway (the row is in flight) | As now: the run stops; a relaunch finds the row in flight |
| A thesis already open | A later item proposes the same bet | As now (Step 1 links to the open thesis); the ladder is not run again |
| Refused thesis | A later item raises the same matter, well formed | Proposed anew, laddered, opened if accepted. The earlier unlinked evidence is found by later linking |
| Configuration changed between days | — | Refused by the launcher's identity check, as now |
| End of the run | — | Every open thesis has a pass-1 ladder; `build_cases` counts the opened theses from the states. Its count rule is unchanged: refused theses never enter a state |

## Value × reader
- **`theses`, the open state:** read by the next item's request (`open_theses`), by `build_cases` (`opened_count`, from the states) and
  by Step 2 (links). All of them now see accepted theses only.
- **The pass-1 ladder:** stored with the trace row. It is read by the ladder component, which must not re-send pass 1, and by the judge's
  inputs.
- **Evidence linked only to a refused thesis:** unlinked, read by Step 2 and by later linking (D383, D513).

## New path × old checks
- **`build_cases`'s count check:** it holds, because states contain accepted theses only.
- **The ladder's pass-1 archive:** it moves into the Step 1 folder. The judge's input path changes (`judge-inputs.json` names it).
- **The D400 three-pass checks:** pass 1 is stored at opening, passes 2 and 3 are sent as now, and the fingerprints are unchanged.
- **Cost:** about one ladder call per opened thesis, the same calls the ladder component makes now, moved earlier.

## Prior decisions
| Decision | What it says | How the design stands |
|---|---|---|
| D383 | A kept statement no thesis takes is kept and linked later | Holds |
| D397 / D436 | A second side of the same bet is one question | Unchanged; the ladder still decides |
| D432 | The no-ladder theses were diagnosed | This acts on their consequence, not their wording |
| D493 | No further Step 1 request change | No request text changes; the loop's control flow does |
| D427 | Clean Step 2 is frozen | Untouched |
| D448 / D449 | The wiring and the redo | The ladder's failure policy is listed above for review |

**Not decided here:** the ladder's own refusal of a deal's completion and size (fix 3), and D505 (fix 4).

**The test, after Alex's word:** a cents probe that replays new-2's July–September items over the capex, DRAM and Groq matters with the
rule. Measured: whether a well-formed thesis opens and is accepted for M02, M03, M16 and M25.

## Blind review, round 1 (`council-e-codex.md`): NOT READY. Gaps to close in the next revision
1. **The failure taxonomy.**
   - Separate a valid decline, two invalid answers, a transport failure and a budget stop.
   - Stage A stops an incomplete run today; keep that behaviour, and do not inherit Step 1's whole-step redo.
   - Say what commits when a crash follows one acceptance in an item with several new theses.
2. **The link contract.**
   - Remove the refused thesis's links from the saved result, so frozen Step 2 sees no unresolved link.
   - Keep the valid links, including those to a co-proposed accepted thesis.
   - Keep the raw answer for audit.
3. **File locations and populations.**
   - The judge and the release checks expect the pass-1 files under the ladder component.
   - D400's three-pass population needs an explicit contract once only accepted theses are counted.
4. **A PRD change.** The PRD places the ladder after Step 3 and keeps unjudged theses (`clean-arch/PRD.md` around line 370). This design
   changes both. That is a recorded decision, and Alex's to make, since the PRD's design is his.
