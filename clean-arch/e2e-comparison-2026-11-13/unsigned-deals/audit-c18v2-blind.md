**The revision addresses the three concerns from the first audit, but it still has two meaningful wording risks:** it can be read as preventing *any* new question about a small or signed deal, and it says the deal’s statements inform the total without checking each statement’s relevance. It also does not carry D389’s size test.

For example, a large unsigned aircraft order may deserve its own signing question alongside a question about total purchase commitments. But a separate open question might already cover that order under different wording, and not every statement about the order necessarily tells us something about the total.

I ran the requested diffs. The only system-text change is the addition at [c18-system.txt:101](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c18-system.txt:101); the closing check is unchanged. The c18 and c8 schemas are also identical.

**Sentence-by-sentence assessment**

1. **“An unsigned single deal … keeps its own signing thesis beside an open thesis on that total, unless an open thesis already asks whether that deal is signed; its statements also inform the total.”**

   **Consistent with D388 in its intended case, with two qualifications.** D388 says: “A material unsigned obligation that merits a separate investment judgment keeps its own yes/no question … beside an open question on the total of the same kind.” The added words “an analyst would judge apart” restore that separate-judgment requirement. The exception for an already open signing question also follows the standard’s requirement that “库里没有问题在问同一件事” — no existing question asks the same thing. [D388](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4172), [standard §4](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:308).

   - **Keeps wider than D389 on size:** “could change those” gives no 5%-of-recent-annual-profit anchor. D389 says a stated amount must be “about 5% or more,” with unstated amounts judged qualitatively; it explicitly leaves loss-making companies open. D389’s stated scope is the focused D388 step under test, so this omission matters if c18 is meant to implement that decision; it is not a change to the frozen standard. [D389](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4185).
   - **Keeps wider on linking:** “its statements also inform the total” states relevance for all the deal’s statements. D388 establishes the separate question, but does not say every statement necessarily informs the total. The existing request instead links each statement to questions it actually informs.

2. **“A small one, or one signed under a programme tracked by its amount, opens no thesis, and its statements inform the total when kept.”**

   **Keeps narrower if read literally.** D388 says such a deal “stays evidence for the total.” In context, that supports not opening a *separate obligation question for that deal*. But “opens no thesis” is broader: it could prevent a separately justified question raised by the same material under another opening reason. The standard explicitly says items excluded as obligations can still be judged under another opening reason. [Standard §4](/Users/lchingen/hivemind/docs/prd/05-extraction-standard.html:327).

   The words “when kept” correctly preserve the separate evidence decision. As in the first sentence, however, “its statements inform the total” assumes relevance rather than judging it statement by statement.

**Consistency with the rest of the request**

- **Small matters:** The first sentence’s “could change” and “judge apart” generally agree with “Open only matters an analyst would bet on separately.” The conflict is with D389’s more specific size test, which is absent.
- **An existing question:** The explicit exception reduces the duplicate risk. It is narrower in wording than the request’s broader same-question test: an existing question may already track the signing without literally asking “whether that deal is signed.” The unchanged closing check does cover the same underlying question, subject and scope. [Closing check](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c18-closing.txt:14).
- **Separate outcomes:** “Judge apart” is compatible with the requirement that answers can move apart, but it does not explicitly require that they *can* move apart. The later instruction and closing check still require it. Thus there is a potential reading tension, rather than a direct contradiction.
- **Linking:** The new language encourages linking to the total, but its unconditional wording conflicts with “to none that its own relevance says it does not inform” and the same check at the end. It does not override the explicit instruction to link to *every* relevant question.
- **Date:** There is no direct contradiction. The earlier definition supplies a check date within 18 months, and the example says “by the check date.” The example alone does not state the limit, so it relies on that earlier sentence.

**Examples and schema**

The examples name an airline and a supplier prepayment, not a covered company, named product or number. Their principle can apply across industries. The large aircraft order is a plausible D388 example **if** it is an unsigned obligation in the company’s own name, is large enough under the applicable size test, and warrants a separate investment judgment. “Large” alone does not establish those facts. The small prepayment example illustrates the intended no-separate-question case, but does not itself say whether it is already signed or show why it is small.

The [schema](/Users/lchingen/hivemind/clean-arch/step1-unfiled-2026-11-08/arms/c18-schema.json:1) can express the proposed signing question, its date, the reason for separate tracking, and links to both the new question and the total. It does not itself establish materiality, enforce the 18-month limit, or decide whether a statement informs the total.

**Specific failure risks**

- **Duplicate question:** Possible if “already asks whether that deal is signed” is read literally and the existing question tracks the same event in different words. The closing check mitigates this.
- **Small deal gets a signing question:** Possible because “could change those” and “large” are qualitative, while D389’s 5% test is missing. The explicit “small one … opens no thesis” pushes against it, but does not define small.
- **Deal statements stop linking to the total:** The addition points in the opposite direction: “also inform the total” expressly asks for the link. A model could nevertheless omit it; this text alone cannot prove behavior. The more direct wording risk is an **unwarranted link** for a statement that does not inform the total.
- **Other openings are suppressed:** Yes. “A small one, or one signed under a programme … opens no thesis” can be read as a blanket prohibition, even when the article also raises a distinct question that passes another opening reason.

This is a text audit, not a measurement of model behavior. No files were changed.

