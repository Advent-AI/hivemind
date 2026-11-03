**The proposal list is still incomplete.** The clearest example is in §6.3: it makes every share-price reaction optional, while proposal 4 names only the covered company’s valuation, market value and unsupported target price. The signed standard makes **post-earnings** share-price reactions optional.

I reviewed [standard-v2.12.md](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.12.md:1), the file the request calls v2.4. No files were edited.

1. **Rules or examples without an adequate source or a listed proposal**

   - **Gold entries for rejected statements have no valid label in some cases.** [§8.2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.12.md:297) requires every sentence that looks like evidence but is rejected to be assigned to a row in §5.3: “看起来像证据但不留的句子各属于 §5.3 哪一行.” Yet [§5.3](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.12.md:197) says sentences outside that list must be judged under §5.1. An unrelated claim can therefore be rejected under the relevance rule without belonging to any §5.3 row. The signed standard does not impose this labelling requirement, and it is in neither top list.

   - **The optional share-price rule is broader than the listed proposal.** [§6.3, step 2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.12.md:260) says “估值倍数、市值、目标价、股价反应 → 可选.” It does not restrict price reactions to post-earnings reactions, or the other three items to the covered company. [Proposal 4](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.12.md:14) is narrower. The [signed standard §10.2](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard/standard.md:140) makes post-earnings reactions optional; it does not establish the broader rule.

2. **Contradictions**

   - **The proposed treatment of old forecasts conflicts with its own example table and the signed example.** [Proposal 6](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.12.md:16) says a restated forecast or plan that remains valid retains its original weight, while old actual results are optional. But the [§6.3 optional examples](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.12.md:269) list “看得出的旧事重提” without that distinction. Read literally, that includes a recognisable restatement of a still-valid forecast. The [signed standard §0](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard/standard.md:14) rates the restated cloud-spending forecast core.

   - **The source-tier table presents an unresolved priority as though it follows from the sources.** [§5.5](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.12.md:222) introduces the table as “按这两处的意思,” then places unnamed or unconfirmed reports above reported announcements and actual figures. This is now disclosed in proposal 9(a), which is an improvement. But [PRD 06](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/06-views.md:93) and the quoted role text do not themselves state a general first-match order for every overlap. The table should not read as an already-derived rule while the priority remains a proposal.

   - **The draft’s evidence-reading rule conflicts with the current PRD text.** [§7](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.12.md:281) correctly describes the limited set shown under [D198](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2558). [PRD 06, State](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/prd/06-views.md:80) still says to reconsider all evidence in force. D198 is the later decision, so this is a PRD inconsistency rather than an unsourced new proposal. The draft identifies a different PRD conflict over revisions in §10 B13, but does not identify this one.

3. **Wrong citations or quotations**

   - **The D209 owner quotation is not exact.** [Draft §9](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.12.md:337) ends the excerpt: “you got to pick it up. That’s the way to do proper evaluation.” [D209](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2643) says: “you got to pick it up. Again, that’s the way to do proper evaluation.” The signed standard already contains the same shortened quotation; copying it does not make it a verbatim D209 quote.

   - The two [§9 D241 excerpts](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/standard-v2.12.md:353) occur in [D241](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/DECISIONS.md:2914). D241 authorizes the drafting work; it does not approve the proposed grading thresholds.

4. **First-review findings**

   The [disposition log](/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/simulation-log.md:241) accounts for the four grouped findings:

   - Source-tier priority is now listed in proposal 9(a), but §5.5 still presents the resulting table too definitively, as described above.
   - The policy-step and share-price-news boundaries now send the statement through the relevance test. The prior automatic-retention problem is fixed.
   - The mechanical “current and next year” grading cutoff and the definition of question period have been removed. The 2030 shortage example no longer directly contradicts that cutoff. Proposal 1 now expressly describes distance as a matter of judgment.
   - The obligation quotation now identifies role-v29 and separately gives D238’s “stake” wording. The prior misattribution is fixed.

   The earlier fixes noted in the first review also remain present: the obligation exclusion is scoped to that opening reason, memo-derived questions are included, the unsigned-obligation date case is included, and the lease wording is no longer limited to offices and factories.

5. **Is the top proposal list complete?**

   **No.** At least the broader optional treatment in §6.3 is absent from proposal 4. Proposal 6 also needs to agree with the §6.3 example table before Alex can tell which treatment of restated forecasts he is being asked to approve. The §8.2 gold-labelling requirement is another unlisted requirement, though its immediate effect is on how the reference is recorded rather than necessarily on product behaviour.