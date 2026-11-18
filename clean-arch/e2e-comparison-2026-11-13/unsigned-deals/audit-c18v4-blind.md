**Version 4 resolves the main wording problems found in the earlier audits, but it still does not implement D389’s size test.** I found no direct contradiction between the two new sentences and the rest of the request. The remaining risks are mainly that the model may read the exception too literally, or treat “could change” as enough to open a deal that fails D389’s test.

For example, a major unsigned aircraft order can warrant its own question alongside a question about total purchase commitments. If an existing question already asks about that same order with a different deadline, however, the candidate’s phrase “asks whether that deal is signed” must be read together with the standard’s rule for different deadlines; otherwise it could open a duplicate.

I ran both diffs. The system prompt adds **two sentences** at [c18-system.txt:101](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c18-system.txt:101). The closing check has no changes.

### Sentence-by-sentence assessment

1. **“An unsigned single deal that alone could change those, and that an analyst would judge apart from the total of its kind, keeps its own signing thesis beside an open thesis on that total, unless an open thesis already asks whether that deal is signed; a statement about it is linked to the total too when it informs it.”**

   **Consistent with D388, subject to the D389 qualification below.** D388 says: “A material unsigned obligation that merits a separate investment judgment keeps its own yes/no question … beside an open question on the total of the same kind.” The signed standard likewise says an unsigned deal’s signing question can remain separate from a plan’s amount question. [D388](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4172), [standard §4](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:343).

   The explicit exception for an existing signing question and “when it informs it” are consistent with the standard’s duplicate test and the request’s relevance-based linking rule. “Judge apart” also restores the requirement for an independent investment judgment.

   **Keeps wider than D389 on deal size, if this candidate is meant to implement D389.** D389 specifies that a stated amount must be “about 5% or more of the company’s most recent annual profit”; an unstated amount is judged qualitatively, and a loss-making company is left open. “Could change those” does not express that test, and the request does not supply the recent-profit input D389 calls for. D389 limits itself to the focused step under test; it does not amend the frozen standard. [D389](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4185).

2. **“A small one, or one signed under a programme tracked by its amount, opens no signing thesis of its own, and a statement about it is evidence for the total when it informs it.”**

   **Consistent with D388.** D388 says: “A small unsigned obligation, or a deal already signed under a plan tracked by amount, stays evidence for the total.” The standard also says small individual deals do not warrant an obligation question and that whether their statements are kept is judged separately. [D388](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4172), [standard §3](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:278).

   “No **signing** thesis” is appropriately narrower than the previous version’s “no thesis”: it does not expressly forbid another independently justified question. “When it informs it” avoids asserting that every statement about the deal belongs under the total.

### Relationship to the rest of the request

- **Small matters and separate bets:** The new requirement that the deal “alone could change” the business and be judged apart is consistent with “Open only matters an analyst would bet on separately; small matters open no thesis.” The missing D389 threshold leaves the model to decide what counts as small.
- **An already tracked deal:** The exception is consistent with “another estimate, source or wording of what an open thesis tracks.” The remaining ambiguity is that “already asks whether that deal is signed” might be read literally rather than by underlying event. The unchanged closing check says to compare the same underlying question, subject and scope. The standard also says a later deadline for the same event is evidence while the earlier question remains open. [Standard §4](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:343).
- **Answers that cannot move apart:** “An analyst would judge apart” is compatible with, but does not itself spell out, the requirement that the answers can move apart. The later instruction and closing check still explicitly require that test.
- **Date:** There is no direct conflict. The existing definition and date rule require a check date within 18 months of the item for an unsigned obligation; the new sentence does not replace that rule. The aircraft example says “by the check date,” relying on the earlier instruction for the limit.
- **Evidence links:** The new wording agrees with linking each statement to every question it informs. It expressly preserves a link to the total when relevant; it does not say that the statement must link to the total regardless of relevance.

### Earlier audit findings

| Earlier concern | Version 4 assessment |
|---|---|
| Separate investment judgment was missing | **Resolved:** “an analyst would judge apart” states it; the separate-outcome test remains later in the request. |
| Possible duplicate signing question | **Improved, not fully eliminated:** the explicit exception now names an existing signing question, but could be read too literally. |
| Major deal might not be linked to the total | **Addressed in the text:** it now explicitly links the statement to the total when relevant. Actual model behavior remains untested. |
| Every deal statement was presumed to inform the total | **Resolved:** both sentences now say “when it informs it.” |
| “Opens no thesis” could suppress other kinds of question | **Resolved as written:** it now says “opens no signing thesis.” |
| Example omitted a check date | **Resolved in part:** it says “by the check date”; the 18-month limit remains in the surrounding definition. |
| D389 size test and recent-profit input missing | **Unresolved:** neither appears in the added text or request input. |
| Signed programme deal could suppress another independent opening | **Reduced:** the prohibition now targets its own signing question, rather than every question. |

### Examples and schema

The examples name no covered company, named product, or number. An aircraft order and a supplier prepayment are industry-specific illustrations of a distinction that can apply across industries.

The aircraft-order example is consistent with D388 **if** the order is an unsigned obligation taken on by the company, is sufficiently material, merits a separate judgment, and is not already covered by a signing question. The example says “large” but does not establish those facts or D389’s threshold. The small prepayment illustrates the no-separate-signing-question case if it is an obligation in the programme and informs its total.

The [schema](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c18-schema.json:1) can express a signing question, its check date, the reason for separate tracking, and links to both the new question and the total. It does not itself decide materiality or enforce D389’s size test.

### Specific risks

- **A duplicate deal question:** Possible if “unless an open thesis already asks whether that deal is signed” is interpreted as requiring those exact words, or fails to recognize the same event with another deadline. The broader duplicate and deadline rules work against that reading.
- **A signing question for a small deal:** Possible under “alone could change those” and the example’s “large,” because neither gives D389’s stated-amount test. “A small one … opens no signing thesis” pushes the other way.
- **Failure to link a deal statement to the total:** The new words explicitly request that link **when relevant**. They do not instruct the model to stop linking; an omission is still possible model behavior, but this text audit cannot establish that it will occur.
- **Suppression of another opening:** The earlier blanket wording has been fixed. A model could still overread “one signed under a programme … opens no signing thesis of its own” as a broader prohibition, but the sentence itself limits the prohibition to a signing question.

These are wording assessments, not observed model results. No files were changed and no model calls were run.

