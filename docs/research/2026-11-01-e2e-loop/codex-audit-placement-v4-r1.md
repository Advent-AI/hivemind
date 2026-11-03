The rewrite has three serious findings: it makes the code-written filing rules authoritative even where they admit material D207 excludes, adds an unsupported cross-period rule, and gives conflicting directions for news about named matters.

For example, a supplier’s quantified capacity increase could be filed under a total-revenue question as a “direct driver,” even though D207 restricts that question to the company’s own figures, guidance and management statements.

1. **Unsourced rules**

   - **Serious:** “The period in a takes line tells apart questions about the same quantity for different periods; it does not bar a figure or driver from an earlier or later period when no open question covers that period.” D240 says missing information alone is not a reason to discard meaningful evidence; it does not establish that a figure for a *known different period* belongs under the only open question. D248 explicitly permits a calendar-year estimate as evidence for a fiscal-year question, but does not state this general rule for all earlier and later periods. [D240 and D248](docs/DECISIONS.md).
   - **Serious:** “News about a customer, supplier, competitor, product, policy or deal goes under the question that names that matter (an event, a policy process, a theme).” D209 requires a statement to bear on an open question, and D207 chooses the narrowest qualifying question. Naming the matter alone is not the stated test; this sentence can direct filing even when that question’s takes line does not cover the news. [D207 and D209](docs/DECISIONS.md).

2. **Conflicts with takes lines or ambiguous wording**

   - **Serious:** “Each open question is a bet with a file, and its 'takes' line is the one rule for what belongs in that file.” The code writes “figures, guidance, estimates and revisions for … over …, and the direct drivers of that figure stated with a size.” For a company-wide figure, D207 instead says “company-wide figure questions take only their own figures, guidance and management statements.” Making the broader takes line authoritative permits sized drivers that D207’s restriction does not. See [placement.py](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/placement.py:42) and [D207](docs/DECISIONS.md).
   - **Serious:** “News about a customer, supplier, competitor, product, policy or deal goes under the question that names that matter (an event, a policy process, a theme).” A reader can treat this as an instruction to file **any** such news under a question naming the matter, even if its takes line covers only particular events or figures. That conflicts with “A statement that no takes line covers is filed under none” and with the generated takes lines’ limits.
   - **Serious:** “A statement a takes line covers belongs in the file whoever says it … and even when it gives no period, basis or exact amount.” The condition “a takes line covers” can be read as requiring a match to the generated “over [period]” text before the missing-period exception applies, or as allowing a missing period in that matching decision. The latter follows D240; the former can drop a relevant statement solely because its period is absent. Also, “no … exact amount” is unclear beside the takes line’s requirement that a driver be “stated with a size”: an approximate size and no size at all are different cases. [D240](docs/DECISIONS.md).
   - **Wording:** “when no open question covers that period” could mean no question about **the same quantity** covers it, or no open question of any kind covers it. The sentence does not specify which.

3. **The revenue sink**

   **Serious: it reopens a limited version of the sink.** The enabling sentence is: “Each open question is a bet with a file, and its 'takes' line is the one rule for what belongs in that file.” The takes line then admits “the direct drivers of that figure stated with a size,” including a quantified business development that is not the company’s own figure, guidance or management statement.

   “File a statement under the narrowest question whose takes line covers it” does not prevent this when the revenue or segment question is the only question whose takes line covers the sized driver. It does not make *all* general business news eligible: the code’s “direct” and “stated with a size” limits still apply. D207’s narrower company-wide figure rule is the governing restriction. [D207](docs/DECISIONS.md).

4. **Company or industry specificity**

   **No finding.** None of the v4 sentences names a particular company, product or industry; the examples of speakers and business relationships are general.

5. **The period sentence**

   **Serious.** “The period in a takes line tells apart questions about the same quantity for different periods; it does not bar a figure or driver from an earlier or later period when no open question covers that period.”

   - **D240:** It is not sourced by D240’s missing-information rule. A known earlier fiscal year is different from an unstated period.
   - **D248:** It does not necessarily conflict with the rule that separate outcomes can be separate questions: one period’s evidence can bear on another question. But D248’s explicit cross-period permission concerns a calendar-year estimate filed under the fiscal-year question; it does not authorize every earlier or later period.
   - **D207:** It overrides the generated takes line’s “over [period]” boundary without requiring the earlier figure to bear on the later question. For a company-wide figure, D207 also limits the kind of material the file takes.
   - **Earlier fiscal year, only later year open:** The prompt tells the model that the earlier year **does not bar filing**. Read with the instruction that a statement covered by the takes line belongs in the file, it can file the earlier-year figure under the later-year question even when the figure does not make that later answer more or less likely. The sentence does not independently require the model to establish that connection.

The quoted prompt is [placement-narrow-v4.txt](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/placement-narrow-v4.txt); the decisions are in [DECISIONS.md](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md).