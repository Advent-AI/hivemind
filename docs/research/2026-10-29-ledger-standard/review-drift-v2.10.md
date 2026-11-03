**The proposal list is not complete.** The named draft still contains rules that are broader or narrower than their cited sources, and two fixes from the v2.9 review leave the draft internally inconsistent.

For example, the draft says a proposed guarantee with no stated date cannot open a question unless it is a regulatory matter. But D210 permits a question about an unsigned obligation with a researcher-chosen check date within 18 months. That restriction is not listed for Alex to decide.

I reviewed the named [standard-v2.10.md](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.10.md:1). The request also calls it v2.4; the findings below concern **v2.10**. No files were edited.

## 1. Rules without an adequate source or listed proposal

- **A general ban on opening questions about a company’s own borrowing, leases and certain investments.** [Draft §4.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.10.md:141) lists “公司自己借钱、自己的租约、已完成或没写规模的投资” under “不开的.” Its cited [D238](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2879) says these **are not binding obligations**. It does not say they cannot be relevant to a question opened under another reason. The broader ban is not in the proposal list.

- **Only two ways for a question to enter the ledger.** [Draft §2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.10.md:73) says a question is “要么由文章里的候选问题开出来，要么是……种下的驱动问题.” [PRD 06, State](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/06-views.md:85) also describes a thesis from a user’s memo. The draft’s closed “either/or” omits that route; no proposal lists its removal.

## 2. Contradictions and unresolved rule conflicts

- **The date exception is too narrow for unsigned obligations.** [Draft §4.2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.10.md:129) says the **only** exception to finding the time basis in the source is an undated pending regulatory decision. [D210](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2663) also permits an unsigned obligation to have a check date after the article, within 18 months. It does not require the article to supply that date. An article reporting guarantee negotiations without a deadline therefore meets D210’s form but fails the draft’s new universal check.

- **The source-tier table assigns some statements to two tiers.** [Draft §5.5](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.10.md:224) assigns “公布的实际数字” to fact, but assigns any unsourced statement that is not a reported announcement or completed deal to rumour. An unattributed published actual figure can satisfy both rows. Likewise, an article can report an announcement while attributing the claim to unnamed sources. The table does not say which row wins. This matters because only facts can establish the final outcome under [PRD 06, Four evidence tiers](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/06-views.md:93). Proposal 9 addresses mixed statements, not this overlap for one statement.

- **The proposed grading rule still does not consistently produce its EPS example.** [Draft §6.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.10.md:260) says a key profit judgment with **a quantity**, a definite state, **or** a forecast with a period is core, subject to the listed exceptions. The FY2028 EPS forecast has a quantity—12.76—and is about profit. The new exclusion for a forecast beyond the question’s period is attached to the forecast branch, but the same statement can qualify through the quantity branch. The table nevertheless calls it supporting. The [signed standard §0](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard/standard.md:15) also calls this example supporting.

  The exception also depends on “问题期限,” but the draft grades evidence even when no question has a home, and extraction does not see the library. It does not say which question period to use in that case or when a statement relates to more than one question.

- **The description of own leases is inconsistent.** [Draft §3.1 C](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.10.md:90) excludes a company’s own office and factory leases while saying purchases of capacity or services count. [D238](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2879) excludes the company’s **own leases** from the obligation category without that office/factory qualification. A company leasing capacity is left between the two descriptions.

## 3. Wrong citations or quotations

- **The citation to D238 in §4.3 does not support the broader ban** described in section 1. D238 limits the *binding-obligation reason*; the draft places the items in a general “do not open” list.

- **The citation for §4.2 does not support “唯一的例外.”** The cited [research review §1](/Users/lchingen/hivemind/research_notes/对冲基金论点粒度与金标/codex-challenger.md:15) asks for a time basis in the source and says a researcher-set check date must be marked. It does not establish that the regulatory case is the sole permitted researcher-set date. D210 supplies another applicable case.

- I found **no material misquote of Alex** among the owner quotations checked against the signed standard and decisions. In particular, both [draft §9 D241 excerpts](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.10.md:352) occur in [D241](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2914). D241 requests the work; it does not approve the draft’s proposed grading thresholds.

## 4. Disposition of the v2.9 findings

The [disposition log](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/simulation-log.md:216) lists the first-review findings. The changes are present, but two do not fully resolve their findings:

- **EPS grading:** an exception was added, but the quantity branch and undefined question period leave the conflict described above.
- **Missing unattributed-source category:** a rumour row was added, but it overlaps the fact row described above.

The regulatory-date fix removes the previous broad permission to substitute a researcher-set date, but introduces the opposite problem: its “only exception” excludes the D210 obligation case.

The remaining fixes are present in the specific respects raised: the $600 billion discussion is disclosed as core; optional cases are handled before the relevance pre-check; the bylaws exclusion and its role-v29 source are restored; and the stale B16 pointer is corrected. The first review’s correction about Google Cloud also stands: the accepted [gold check](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard/gold-check.md:31) calls it supporting.

## 5. Proposal-list completeness

**No.** At least these behavior changes are absent from the top list:

1. Treating borrowing, own leases and completed or unsized investments as a general bar to opening a question, rather than a limit on the binding-obligation reason.
2. Excluding the memo-origin route from the draft’s closed list of ways to create a question.
3. Making an undated regulatory decision the only exception to the source-time-basis requirement, thereby restricting the D210 unsigned-obligation case.

The source-tier overlap and EPS grading conflict also need a defined resolution before the proposal list can describe their effects reliably.