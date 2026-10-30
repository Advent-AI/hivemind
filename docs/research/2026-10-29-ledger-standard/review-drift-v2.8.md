**The proposal list is not complete, and v2.8 still has rules that conflict with the signed standard or the decisions.** For example, it adds company-charter matters to the “do not open” list while citing a source that does not include them.

I reviewed [standard-v2.8.md](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.8.md:1), the named rewrite. The request also calls it “v2.4”; my findings concern **v2.8**, not the separate v2.4 file. No files were edited.

### 1. Rules or examples without an adequate source or proposal

- **Company-charter matters are added to the “do not open” list.** Draft §4.3 says “高管任免、股东投票、**章程**、回购授权” cannot open a question and cites signed standard §6. That section lists appointments, votes and buyback authorization, but not charters. A charter matter could therefore be rejected under a new categorical rule that is not in the proposal list. [Draft §4.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.8.md:130); [signed standard §6](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard/standard.md:92).

- **The grading procedure treats some irrelevant comparisons as supporting evidence.** Draft §6.3 step 1 sends competitor comparisons past the reject list; steps 2–3 then assign “辅助” to everything that does not meet the core test. Unlike §5.3, those steps do not send the comparison through §5.1’s relevance judgment. Thus an irrelevant comparison can receive a supporting grade. Neither the signed standard’s specific AMD ruling nor proposal 1 establishes that rule. [Draft §§5.3 and 6.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.8.md:180).

- **The handling of the unrelated-statement metric is asserted as a decision, but the citation is narrower.** Draft §8.3 says “**‘无关陈述’的计数要用按本标准重建的金标重算**,” and §10 B9 repeats it. D240 removes the target based on reference-v2 pages marked “keep nothing”; it does not say to rebuild the entire unrelated-statement count under this draft. This can change the signed acceptance measure and is not separately listed for Alex. [Draft §8.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.8.md:313); [D240](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2901).

### 2. Contradictions

- **Proposal 1 conflicts with an accepted case, and its detailed procedure does not consistently apply the proposal.** The top list says another company’s own operating figures, including revenue and backlog, are “**算辅助**.” The signed standard treats the Google Cloud revenue, growth and backlog figures as one item, and D229 says the reference keeps Alex’s revenue-growth classification as **core**. Separately, §6.3 step 3 says a material, quantified statement touching a key judgment is core; it does not include proposal 1(c)’s exception for another company’s operating figures. A large customer’s reported backlog can therefore be core under the steps and supporting under the top list and §6.3’s example. The proposed change is disclosed, but its consequences and execution are inconsistent. [Proposal 1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.8.md:11); [draft §6.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.8.md:249); [signed standard §§2 and 8](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard/standard.md:30); [D229](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2826).

- **Proposal 9 changes the recorded treatment of reported announcements.** Draft §5.5 says an announcement of a future action is a party statement, and an account with no identifiable source is a rumour. D238 states that a reported announcement is a fact, and the adopted v29 prompt says an announcement reported by the item is a fact even when the reporter names no source. Proposal 9 is listed, but its introduction says PRD 06 only defines the tiers; it does not identify this conflict with the adopted rule. [Draft §5.5](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.8.md:215); [D238–D239](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2879); [role-v29](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/role-v29.txt:10).

- **§6.2 omits an extraction responsibility.** It says “**抽取的模型只决定留不留、怎么写**” (“the extraction model only decides what to keep and how to write it”). Signed standard §1 also assigns it the production of candidate questions. Other sections of the draft describe question opening, so this is also an internal contradiction. [Draft §6.2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.8.md:245); [signed standard §1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard/standard.md:23).

### 3. Wrong citations or quotations

- **§4.3’s citation to signed standard §6 does not support the added charter exclusion**, as described above.

- **§8.3’s attribution to D240 does not support the broader instruction to recalculate all unrelated-statement counts**, as described above.

- **The date fix still leaves an unsupported restriction in §4.2.** It now correctly quotes the review’s requirement that a researcher-set check date be marked, but also says the “**时间依据能在原文找到**” and says an unrepairable failure prevents opening. §3.1 E allows an undated pending regulatory decision to use fiscal year-end. If the article gives no time basis, the draft does not say that the researcher-set date satisfies or overrides §4.2; the case can still be rejected. The cited review permits a marked researcher-set check date. [Draft §§3.1 and 4.2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.8.md:91); [research review §1](/Users/lchingen/hivemind/research_notes/对冲基金论点粒度与金标/codex-challenger.md:12).

I found **no material misquotation of Alex** in the owner quotations I checked against the signed standard and decisions. In particular, the two D241 excerpts in §9 are present in [D241](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2914). D241 authorizes the drafting and review work; it does not itself approve proposal 1’s thresholds.

### 4. Status of the v2.7 review findings

The [disposition log](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/simulation-log.md:220) lists seven changes. The unqualified graphics-card price-cut example was removed; Singapore’s optional status was moved into the boundary column; the regulatory examples were changed to match the cited theme/asset distinction; and the `other` exception was added in both shared-quantity locations.

The remaining fixes are incomplete:

- The competitor-comparison boundary now calls for relevance judgment in §5.3, but §6.3’s grading steps bypass that judgment and can still grade an irrelevant comparison as supporting.
- The exception-routing change in §6.3 no longer automatically excludes the named required exceptions, but it introduces the comparison problem above.
- The date wording now acknowledges researcher-set check dates, but §4.2 still requires a time basis in the source without resolving the undated case allowed by §3.1 E.

### 5. Is the proposal list complete?

**No.** At least the charter exclusion and the instruction to recalculate the unrelated-statement count are behavior-changing additions outside the list. The grading steps also apply a broader comparison rule than proposal 1 states. Proposal 9 is listed, but does not disclose its conflict with D238 and the adopted v29 announcement rule.