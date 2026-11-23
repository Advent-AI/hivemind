The proposed sentence conflicts with the decisions: it can remove a part that the decisions say must remain visible as not judged, simply because the answer choices happen to settle it.

**Request sentences**

- **System, line 5:** “Judge the one the topic's outcome names as what is tracked.” **Consistent** with D397 and D420.
- **System, line 5:** “List every other part of the topic's description and outcome that the question leaves out, a second figure or event, a condition or a comparison, in not_judged, each with one sentence on why it is not the one tracked.” **Consistent** with D397.
- **System, line 5:** “A second side of the same bet, for example a market's tightness beside the volume shipped, a share beside the total it is part of, or capacity beside the demand it serves, stays in the one question as context: list it in not_judged.” **Consistent** with D436.
- **System, line 5:** “A second side is not by itself a reason to decline; decline only when no part is the main one, or when the main part itself meets a case below.” **Consistent** with D397 and D436; D417 supplies one relevant refusal case.
- **System, line 5:** “Never fold two things into one ladder: ‘Will the regulator approve the drug for a second use, and how many patients will take it in the first year?’ is judged on the approval when that is what its outcome names, and the patient count is listed; ‘How much will the carrier's fuel bill be next year, and will its pilots strike?’ is judged on the fuel bill when that is what its outcome names, and the strike is listed.” **Consistent** with D397.
- **System, line 13:** “A difference inside an outcome, such as an approval with conditions against one without, is not an outcome of its own; when the topic's description or outcome names it, list it in not_judged.” **Consistent** with D409.
- **Closing, line 1:** “Read the question back: does it ask one thing, the one the topic's outcome names, and is every other part of the topic's description and outcome listed in not_judged?” **Keeps wider** than D397 as written: it does not say “that the question leaves out,” so it can include wording already judged.
- **Schema, `not_judged` description, line 52:** “Every other part of the topic's description and outcome that the question leaves out (a second figure or event, a condition, a comparison); empty only when the question leaves nothing of either out.” **Consistent** with D397, but “leaves out” needs interpretation alongside D436’s instruction to list a second side retained as context.

The request leaves the model to guess whether a part is “left out” when the question mentions it as context, or when the answer choices settle it indirectly. It also does not define how to divide a partly settled entry.

**Proposed sentence**

Its removal test is **narrower** than D397 and D436: it removes some parts those decisions keep. It conflicts with the system’s explicit instruction to list a second side as context, and with the closing check’s instruction to list every other part. It also conflicts with the schema when the question leaves such a part out. For D409’s finer differences, it keeps them when an answer choice leaves the difference unsettled; D417 and D420 do not independently establish this removal test.

Two examples, assuming each answer range settles the comparison:

1. The question judges a factory’s annual output; the topic also asks whether output exceeded last year’s level. If every range lies wholly above or below that level, the proposed test removes the comparison, though D397 keeps it visible.
2. The question judges annual demand; the topic also asks whether fixed capacity kept pace with demand. If every range settles that comparison, the proposed test removes the second side, though D436 keeps it visible.