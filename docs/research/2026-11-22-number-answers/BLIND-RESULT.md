# judging-v13s blind conformance test: result (SMALL-DESIGN.md §5; D737–D739)

**STOP**, on two registered stop conditions.
1. A check refused a right answer. E's Claude writer copied "$35 billion" from "from $35 billion to $170 billion", the CPU market's
   2026 value in a grow-from-to sentence, and S1 read the sentence as a range.
2. An accepted reply carries a named defect. P-v4's Codex writer used two values for company Q3 revenue: the $108B guidance to set a
   growth benchmark, and its own $113.6B forecast as the base for Q4. Both readers and both adjudicators marked it.

What passed:
- All 12 first answers were schema-valid, with none refused by the schema.
- 11 of 12 passed every code check.
- One refusal is disputed on whether the request states its condition. The two reviewers split on that, and agree the refused
  amount is right.

**Run:** `poc/data/judging-v13s-blind-2026-11-22/`. It cost $0 at the provider: the writers, readers and adjudicators were fresh Claude
subagents and fresh read-only Codex sessions. Every Codex writer's stream shows it read only `system.txt`, `user.txt` and
`schema.json`.

## 1. Writers' first answers (`CHECKED.json`)

| Case | Claude writer | Codex writer |
|---|---|---|
| P (joint) | publish: v4 416.3, v8 384.9, both rung 2 | publish: v4 417.4, v8 386.5, both rung 2 |
| P-v4 | publish: 417.4, rung 2 | publish: 419.8, rung 2 |
| P-v8 | publish: 385.9, rung 2 | publish: 387.1, rung 2 |
| S (CY2026) | publish: 705–735, rung 4 | publish: 715, rung 4 |
| O | publish: 8–24, rung 1 | publish: 16, rung 1 |
| E | **refused (S1)**: "$35 billion" read as part of "$35 billion to $170 billion" | publish: 36, rung 3 |

**The refusal review** (`refusal-review/`):
- Both reviewers say the refused figure is right: $35B is the 2026 value, and $170B is the 2030 value of the same market.
- On whether the request states the condition, the Claude reviewer says no and the Codex reviewer says yes.
- **The mechanism is mine.** Round 54's change added "X to Y" as a range form so that "$195 billion to $205 billion" would pass. The
  old checker had excluded "to" for exactly this ambiguity. Its comment reads: "'to' is ambiguous ('from $253 billion to $392
  billion')".

## 2. Readers and adjudicators (`reader-packets/`, `adjudication/`, `TALLY.json`)

Each reply had two blind readers, a Claude subagent and a Codex session. Each saw the whole request and the whole reply, and nothing
of the writer or the checker. Where the two disagreed, two adjudicators, one per family, settled each point against the passages and
the format rules. A point counts as settled when both adjudicators agree.

**Settled defects on accepted replies.**
- **R06 (P-v4, Codex writer), two forecasts of one quarter.** Both readers and both adjudicators marked it.
  - F7 = growth(Q2, F4) takes Q3 from the $108B guidance outside the Q3 forecast F6 ($113.6B). It reaches the outcome through an
    estimate's `rests_on` (F8, which rests on F7), so S4's walk, which follows `inputs` only, did not see it. Under D738 this is an
    indirect form, recorded for readers.
  - The effect is about $6B on Q4, and the rung is unchanged.

**Settled as not defects (both adjudicators reject):**
- every "number misread" claim. These were a "plus or minus" expression given as its midpoint, which the format permits; "up to",
  which in e1919's quote belongs to the $3B total and not to the $1B tranche; and "about $70 billion", which was kept;
- both "wrong arithmetic" claims:
  - R09 declared the midpoint of a computed range, which the format permits;
  - R02 summed "more than $42 billion" and $25 billion as 67, keeping the qualifier on its source;
- R12's two-forecast claim (guidance used as a benchmark beneath an estimate, with one Q3 value in the outcome chain).

**Unsettled: the two families split** (the Codex adjudicator upholds, the Claude adjudicator rejects).
- **A computed market reference.**
  - The cases:
    - consensus company revenue ($411B) × the reported Q2 Data Center share (92.5%) gives a Data Center reference of about $380B
      (R05, R08, R12);
    - the reported $25B balance − the $18B "committed to equity investments for the rest of its fiscal year" gives $7B (R02).
  - **The Codex adjudicator's view:** applying a quarter's share to a full year, or netting the schedule, is the writer's assumption,
    so it is not the market's reference.
  - **The Claude adjudicator's view:** the rule allows a figure computed only from consensus, guidance and reported figures.
  - The original design took the Claude view: DESIGN.md C5 passes q02's "$392B consensus × 92% reported mix" as a reference.
- **A label that changes the quantity (R09, S's Claude writer).** Company-wide capex was labelled "data-center capex".
  - The Codex adjudicator calls it not supported (an outcome not of the question's quantity).
  - The Claude adjudicator calls it supported: the passages use the two terms interchangeably (e5376 against e5081).
  - Round 55 notes that those two articles describe five companies, while R09 answers for four.

**Support.** Every forecast is supported by both adjudicators, except R09, where the families split as above.

## 3. What the test shows

- **The request now states its rules.**
  - Twelve first answers from two writer families produced no schema refusal and no refusal on an unstated rule.
  - The one code refusal was a checker error.
  - Compare the paid gate (D733), where 0 of 90 outcomes named a figure.
- **The checker still holds one error of mine:** the "from … to …" range.
- **The indirect route through an estimate's `rests_on` let one real inconsistency through.** D738 chose to record such routes for
  readers. The readers caught it, and the registered stop rule counts their catch.
- **The two reader families apply different thresholds** to a computed market reference and to a relabelled quantity. These are ruler
  questions. By the council-loop rule "Model readers carry their family's threshold … take a balanced set of boundary cases to Alex;
  his rulings are the ruler", they go to Alex.
- **The joint and separate answers in P agree closely.** v4 is 416–420 and v8 385–387, all rung 2. This is one draw each, a strong
  writer, and not gpt-6-luna. It is no evidence for D725's joint-versus-separate question.

## 4. Council B (round 55, `codex-r55.md`)

- **STOP is correct as registered**, and every count reconciles. Three wordings above are corrected.
- **R06 and R12 use the same method.** Each derives a guidance-implied Q3 growth benchmark of about 12.25%, chooses 13% for Q4, and
  applies it to its own higher Q3 forecast. Only one Q3 dollar figure enters the revenue calculation. The adjudicators upheld one and
  rejected the other on reasoning that fits both, so the readers' boundary is unstable. It goes to Alex.
- **Questions for Alex**, with the council's recommendations:
  - (1) May a guidance-implied growth benchmark inform a growth estimate, when one Q3 forecast supplies the revenue calculation? The
    council recommends allowing it.
  - (2) May "consensus total × last quarter's segment share" be called the market's segment estimate? The council recommends no: call
    it our comparison estimate unless an outside source gives the full-year share or segment figure.
  - (3) May total capex stand in for data-center capex? The council recommends requiring a stated deduction or a supported bound.
- **The next step:**
  - fix the S1 "from … to …" range;
  - apply Alex's rulings in the reader brief, and in code only where the structure decides them (D738);
  - check that both reader families apply the rulings the same way to the stored boundary replies;
  - run the registered blind test once with fresh writers and readers. A clean result is the basis for the paid re-send request.

## 5. Not measured

Whether gpt-6-luna at medium effort follows the format: only the paid re-send measures that. Readers' quality judgements beyond the
five defects were not graded.
