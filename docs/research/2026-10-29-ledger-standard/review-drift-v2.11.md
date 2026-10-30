**The proposal list is not complete.** The draft adds a rule for choosing evidence source tiers without listing it for Alex, and one proposed grading rule conflicts with both its own example and an accepted example.

For example, an article can give an actual number without saying where it came from. The draft now calls it a fact; the cited sources do not settle that overlap in the way the draft claims.

This review concerns [standard-v2.11.md](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.11.md:1), although the request also calls it v2.4. No files were edited.

## 1. Rules without an adequate source or a listed proposal

- **Source-tier priority.** [Draft §5.5](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.11.md:222) says “从上到下第一个符合的就是” (“take the first matching row”). It makes an unnamed-source claim a rumour even when it reports an announcement, and makes an unattributed published actual figure a fact. [PRD 06, Four evidence tiers](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/06-views.md:93) lists both published figures as facts and unattributed statements as rumours; it does not provide this order for overlaps. [Role-v29](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/role-v29.txt:10) likewise names the categories but does not state the draft’s first-match rule. Proposal 9 covers *mixed statements*, not this priority for a single statement.

- **Automatically keeping all news behind a share-price reaction and all announced policy steps.** [Draft §5.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.11.md:186) says “股价反应的那条新闻本身要留” and “官员宣布的政策步骤要留.” Its [§0 flowchart](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.11.md:40) sends an item marked “要留” straight to retention. The [signed standard §2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard/standard.md:29) makes relevance to an investment question the retention rule; its policy examples do not say every such step is relevant. Neither general exemption appears in the proposal list.

## 2. Contradictions and rule conflicts

- **The proposed horizon rule rejects an accepted core example.** [Draft §6.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.11.md:261) says that a quantity or forecast beyond the current and next year is supporting, regardless of whether it has a number. Yet its core examples include “内存厂说短缺持续到 2030” in a 2026 context. The [signed standard §4](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard/standard.md:73) also lists the shortage through 2030 as core, and [D215](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2727) records Alex’s core judgment. Proposal 1 discloses a grading change, but its rule and example cannot both be applied as written.

- **“Question period” is replaced by an allowable opening window.** The same [§6.3 rule](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.11.md:261) defines “问题期限” as the current *and* next fiscal or calendar year, or 18 months for obligations. [PRD 06, Ladder rule 5](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/06-views.md:76) gives the years in which **separate questions may be opened**, not the period of one question or a rule for grading evidence. A statement about next year can therefore pass the draft’s horizon even when the actual question is about this year. The definition also does not say what period to use for an event question. This leaves the first review’s multiple-question problem unresolved.

- **The policy and share-price exemptions conflict with the draft’s own relevance rule.** [§5.1](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.11.md:168) requires an analyst to have reason to record the statement. As described above, §5.3 and the §0 flowchart instead make those two classes automatic keeps, even when unrelated to the company’s investment questions.

## 3. Wrong citations or quotations

- **D238 is quoted with words it does not contain.** [Draft §3.1 C](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.11.md:90) labels this as “D238 原文”: “Its own borrowing, its own leases and a completed or unsized investment are not obligations.” That sentence appears in [role-v29](/Users/lchingen/hivemind-extraction-quality-2026-10-28/src/hivemind/prompts/role-v29.txt:14), not in [D238](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2879). D238 describes a “completed or unsized **stake**,” not “investment.” The citation should identify the actual source; the wording difference also matters when deciding how broadly the exclusion applies.

- **The citations for the first-match source-tier rule do not establish that rule.** The specific gap is described in section 1 above. The draft presents the ordering as the meaning of PRD 06 and role-v29, but neither source states that ordering.

- I found **no material misquote of Alex** in the owner quotations checked against the signed standard and decisions. In particular, the two [§9 D241 excerpts](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.11.md:353) occur in [D241](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2914). D241 requests the work; it does not approve the draft’s grading thresholds.

## 4. First-review findings

The [disposition log](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/simulation-log.md:229) lists the changes. Four specific fixes are present:

- The general ban on opening questions about own borrowing, leases and certain investments is narrowed to the **binding-obligation reason**.
- The user-memo route is added to the question origins.
- The undated unsigned-obligation case is added beside the regulatory-date exception.
- The own-lease wording no longer narrows the exclusion to offices and factories.

Two fixes remain incomplete or introduce a problem:

- **Source-tier overlap:** the table now has a priority order, so the rows produce one answer, but the new priority is not sourced or listed as a proposal. It also changes the treatment of overlapping unattributed figures and announcements.
- **EPS and question period:** the new exception prevents a far-future EPS forecast from qualifying as core merely because it has a number. But the replacement definition uses the two-year opening window rather than a particular question’s period, and the same rule conflicts with the 2030 shortage example.

## 5. Proposal-list completeness

**No.** At least the source-tier priority and the automatic retention of the news and policy classes described above can change results and are absent from the top list. The proposed grading horizon is listed, but its conflict with the accepted 2030 example and its use of an opening window as a question period need to be made clear for Alex’s decision.