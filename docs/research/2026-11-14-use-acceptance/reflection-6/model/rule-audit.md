**The sources do not give a general rule for finding the main part when several parts are named.** They support judging one part and showing the rest, but they do not say when the topic’s description, a first-mentioned part, a later milestone, or a closely related second figure makes one part primary.

For example, the CPO topic asks about **2027 shipments** in its description, but its outcome names shipments from **Q4 2026 through 2027**. Treating the full-year figure as primary is reasonable; treating the whole named span as the tracked figure is also consistent with the sources.

1. **What the decisions say**

   - [D397]( /Users/lchingen/hivemind/docs/DECISIONS-log.md:4326) records Alex’s choice: “只判主要那件.” It says to judge “the part its `outcome` names,” show the other parts as not judged, and give no question when there is “no main part.” It does not explain how to choose when the outcome names several candidates.
   - [D436]( /Users/lchingen/hivemind/docs/DECISIONS-log.md:4847) says “a second side of the same bet” stays as context and is “shown as not judged.” Its examples include shortage beside shipments. It does not say how to identify the main side in every multi-part topic.
   - [D417]( /Users/lchingen/hivemind/docs/DECISIONS-log.md:4606) declines a figure covering “a period which is not one fiscal or calendar year” when neither text gives a publication day. It does not say which period to select when the topic names several.

   The [reader form]( /Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md:95) checks that the question asks what the outcome names, omitted parts are shown, and a refusal’s stated reason applies. It supplies no further selection rule.

2. **The 24 declines**, grouped where all draws have the same source-level verdict. “Silent” means the available standard does not settle the disputed selection; it is not a finding that the decline is wrong.

| Topic and sol draws | Main part and verdict |
|---|---|
| Fortnight **13**, d1–d3 | **Silent.** Full-year 2027 shipments may be main, with earlier checkpoints left out; alternatively the outcome tracks the Q4 2026–2027 span. D417 applies only if that span is the selected figure and has no publication day. |
| Fortnight **3**, d1–d3 | **Silent.** US authorization may be main, with Chinese restrictions as another condition; alternatively both authorities’ actions are separately tracked with neither main. |
| Fortnight **8**, d2–d3 | **Justified on the recorded theme finding.** The main figure is 2026 physical-AI venture funding; the refusal is about no matching theme, not multiple parts. Both readers held it. The case file itself does not contain the request’s theme list, so that finding rests on the recorded trace. |
| Week **11**, d1–d3 | **Silent.** Signing may be main, with closing and terms left out; alternatively signing and closing are distinct tracked events with neither selected. |
| Week **12**, d1–d3 | **Justified.** 2026 and 2027 global AI spending are presented together, with neither singled out. They are separate annual figures; choosing one would require an additional rule. |
| Week **13**, d1–d3 | **Silent.** Remaining commitments may be main, with cash paid and changes left out; alternatively these are separately tracked figures with none selected. |
| Week **3**, d1–d3 | **Silent.** Contract-price change may be main, with selling prices and margins left out; alternatively the named measures compete. Even if price change is main, the separate HBM-versus-DRAM series question remains. |
| Week **4**, d1–d3 | **Justified.** 2026 and 2027 hyperscaler spending are presented together, with neither singled out; they are separate annual figures. |
| Week **5**, d2 | **Unjustified.** Closing the already signed acquisition is the named event; termination is an alternative outcome, while consideration and regulatory conditions are other parts to show. Both readers rejected the refusal. |

The reader disagreements and matched answers are in the [refusal trace]( /Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-6/model/refusal-trace.txt:1). These verdicts are about the stated refusal reasons; they do not certify that a proposed answer would meet every other requirement.

3. **Wording and boundary cases**

The strongest sourced wording is already in the [request]( /Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/candidate-system.txt:5): “Judge the one the topic’s outcome names as what is tracked,” and list every other part. D436 adds “a second side of the same bet” as context. Applied to all nine topics above, that wording supports the week 5 correction, preserves the two two-year refusals and the separate theme refusal, and leaves the other five topics unresolved. It does **not** tell the model how to resolve those five; the stored trace also cannot establish that repeating it would change any model response.

A ruling would need these boundaries, with both readings shown:

- **CPO shipments:** description’s full-year figure is main / the outcome’s multi-period span is tracked.
- **China restrictions:** US approval is main and Chinese acceptance is a condition / the two authorities’ decisions are separate candidates.
- **Reflection acquisition:** signing is main and closing follows / signing and closing are separate candidates.
- **Commitments:** remaining balance is main and funding/change are context / all are separate candidate figures.
- **Memory:** contract-price change is main and company prices/margins are context / the figures compete; separately, whether HBM/DRAM denotes one usable figure or requires a series choice.

These are the same unresolved distinctions identified by the [earlier rule review]( /Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/unlisted-parts/rule-review.md:1). Neither “use the description” nor “use the first part” is sourced as a general tie-breaker.

SOURCES SILENT: OWNER RULING NEEDED