**The record failed the prewritten usability line, but “not ready by one line” overstates how settled the rest of the result is.** The 75% margin was wrongly attributed to the CFO, and the line allowed no wrong statement. The separate fidelity verdict for the non-revenue sample remains unresolved; the comparison of the six answers also has gaps that need to be stated.

### 1. Verdict and fairness

The usability failure is clear. Both comparers marked Q4 wrong, and the record reader did say the CFO stated the 75% actual. The [view](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/record/record-view.md:50) presents the figure as “from” her. Yet [step 121, ev-5](/Users/lchingen/hivemind/poc/data/clean-lean-week-2026-11-14/week-r2/c1/step1/trace.sqlite) shows the author comparing the reported 75% with the CFO’s *forward* margin outlook. The frozen line permitted no unsupported statement, so it fails regardless of whether five other questions match. [Design](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/record/RECORD-TEST-DESIGN.md)

The non-revenue fidelity line is **undecided**, not a clean pass:

- Both families mark entry 22 wrong: the current earnings base is labelled an estimate.
- Entries 7 and 26 remain disputed even after another reader from each family: the article says analysts or gives a projection; the stored row says “consensus analysts.” If both are wrong, there are three wrong rows against the limit of two. Neither majority nor repetition settles whether “consensus” is supported.
- Entry 32 was also marked wrong by both settling readers, but their packet omitted the publisher shown to the model. That omission makes their stated reason insufficient; it does **not** by itself prove the attribution right. Re-read with the original request’s publisher and article, and distinguish an outlet reporting an estimate from authoring it.

The [tally](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/record/tally-record.txt) itself says the strata are undecided pending settlement. The result’s “met on settled marks” should not silently resolve the two continuing disagreements.

There are also usability-check limits:

- **Q1(c):** the comparers were not given the question’s wording. One says the article population cannot be checked; the other infers absence from both answers. “Neither has it” is therefore not established by that comparison.
- **Q2:** the comparers differ over the growth expectation omitted by the reference. This does not change the overall failure, but “five the same” is one reading, not settled agreement.
- **Q6:** the frozen question asks for **each pair**, but the reference includes acquisition prices outside the revenue-and-margin view, and the record reader lists other pairs the reference omits. Both comparers support those omissions as factual; reducing Q6 to the shared $406.05/$412 billion pair does not apply the “each pair” requirement as written. Its scope and completeness are unresolved. [Reader answers](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/record/claude-record-answers.jsonl) · [Reference](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/record/codex-reference.jsonl)

### 2. Defects and counts

The four listed issues are useful leads, but they do not all have the same evidentiary status.

1. **Shared attribution and date:** confirmed as a structural limitation and demonstrated in Q4. The counts—93 multi-figure statements, 15 with multiple kinds, and 9 actual rows carrying a non-company party—describe exposure, **not nine proven attribution errors**. Statement dates may similarly apply to one figure but not its neighbours; their error count is not established.
2. **Free-text measure and period:** the view’s 44 rows under 42 headings show fragmentation. They do not establish that every pair of similar-looking headings represents the same measure or period. The 52 missing periods need source-by-source classification before calling them all extraction defects.
3. **Reason elsewhere:** confirmed for the margin squeeze: the reader missed component costs that the articles describe. The design made the explanation optional, so this is a product limitation, not a failed required subpart.
4. **Publisher omitted from the packet:** a confirmed measurement defect, not a stored-record defect.

Two additional problems matter. First, entry 22’s **wrong kind** is a distinct stored-data error; treating every `actual` label as authoritative would not address a figure wrongly labelled `estimate`. Second, the **comparison packet and tally** did not faithfully exercise Q1(c) and the full Q6; the result should not claim all six questions were completely checked. The result’s claim that figures “hold what a reader needs” is too broad: the latest estimate was unexercised, the margin explanation was absent, and attribution failed.

### 3. Next step

I would **not implement A yet**. `actual` means a reported figure in the schema; it does not establish who reported it, whether the source actually names the company, or which date belongs to it. Replacing every stored party with “company reported” could hide a mixed-statement error or manufacture attribution. Showing the article and passage while explicitly saying *the figure’s speaker is not separately stored* is a possible display treatment, but its effect needs to be checked rather than assumed.

A general fiscal-period parser also needs a closed, source-backed boundary: “Q3 FY2027” and “third quarter of fiscal 2027” may be equivalent, while “last quarter,” “fourth quarter,” calendar years and different company fiscal calendars cannot safely be merged by spelling alone. The same six questions on another 40 articles would be useful only after fixing Q1/Q6, checking which parts the new articles actually exercise, and preserving a truly unread sample. Reusing questions and lines developed from the first sample remains a limitation, even with new readers.

**My recommendation is one smaller $0 test before A or B:** census and read the source passages for the 201 `actual` rows, starting with all 9 carrying a non-company party and the mixed-kind statements. For each, determine whether the company, another named speaker, or no speaker is actually established; whether the statement date applies to that figure; and whether a neutral display with the original passage preserves the distinction. Separately list the observed period forms and test proposed equivalences against their source context. Include known correct company-attributed rows as controls.

**Refutation:** if the neutral display still causes readers to infer a speaker or date unsupported for the figure, or the period forms cannot be grouped without inventing a year or scope, a view-only correction cannot safely solve this class. If it succeeds, it supports designing a bounded view test; it does not repair the stored per-figure attribution, justify a schema change, or authorize a product surface.

Council position: Keep the declared usability failure, but record non-revenue fidelity and parts of the answer comparison as unresolved. Before changing the view or frozen request, trace the actual-figure attribution and period classes against their sources; use that evidence to decide whether a neutral display is sufficient or the stored figure needs its own attribution.