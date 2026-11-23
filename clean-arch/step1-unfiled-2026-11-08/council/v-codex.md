**Steps 1 and 2 are built and investigated, but neither has passed its latest acceptance check.** A useful example is quarterly results: Step 1 can read the figures, yet discard them because no existing view takes them. The proposed remedy preserved more figures, but also kept figures Alex said to discard and left relevant margins disconnected.

**Step 1.** Alex chose K6b with DeepSeek Flash. On 115 development articles, two forward draws kept 205/234 and 197/234 helpful matters and met the thesis-size line after source-backed review. On 26 eligible test articles, one draw kept **32/42**, below the proportional target of 35; it matched 8 not-kept spans versus 4 in the production comparison. Seven of the ten missed helpful matters had been extracted but were dropped without a thesis link; three were not extracted. The test articles had prior exposure, and the proportional target was not separately confirmed. The chosen configuration is not production acceptance. The later conditions experiment, c1, is not carried forward. [Step 1 close-out](clean-arch/takeover-2026-11-07/LOG.md), [conditions investigation](clean-arch/step1-unfiled-2026-11-08/LOG.md).

**Step 2.** The isolated comparison and grouping path ran on 282 Step 1 records and produced 178 groups. In one fresh comparison draw, search found a group containing a known counterpart in **112/113** cases; readers found **3 clearly wrong merges out of 104**, above Alex’s 2% limit; and the grouped view retained **28/36** later details versus **27.5/36** without merging. Thus the recorded search and detail checks met their lines, while wrong merges failed. The search denominator contains known labelled counterparts, not all real repeats. The tested comparison also truncates passages at 600 characters; 44/282 stored items exceed that length, so unseen qualifications may affect comparison. [Step 2 results](clean-arch/step2-validation-2026-11-07/LOG.md), [comparison code](clean-arch/step2/compare.py), [conditions design §15](clean-arch/STEP1-CONDITIONS-DESIGN.md).

**What produced the results**

1. **Useful facts can be lost after extraction.** K6b requires a home in a view. Its own instructions discourage opening a view for a quarter’s figures, so the model can find revenue and then discard it. In the stored test, retaining all unfiled items would raise the helpful match count from 32 to 38, but also raise not-kept matches from 8 to 12. Keeping everything is not the answer. [Unfiled census and model accounts](clean-arch/step1-unfiled-2026-11-08/LOG.md).

2. **c1 broadened retention and narrowed linking at the same time.** It told the model to keep company financial figures, omitting Alex’s “useful” qualification, and to link them only where they inform a view’s *reason*. In the saved answers, cash was retained in all three relevant draws despite Alex’s contrary ruling, while margin linked to the revenue view fell from 5/6 to 1/6. The model’s accounts cite those instructions. [Saved answers](poc/data/clean-step1-unfiled-2026-11-08/probe-r4/merged.json), [accounts](poc/data/clean-step1-unfiled-2026-11-08/probe-r4/accounts.json), [c1 instruction](clean-arch/step1-unfiled-2026-11-08/arms/c1-system.txt).

3. **A correct structural idea was tested with conflicting wording.** c1 eliminated four figure-only views and retained the EPS forecast in 6/6 draws versus 3/6, but produced seven additional views absent from the gold’s requested set. The explanation for the networking and supply-commitment cases remains disputed; the model’s accounts do not establish that c1 caused each one.

4. **Merging sources alone erased later detail.** Keeping each report’s own text in a group restored detail in the selected reader exercise. But grouping does not make a wrong association right: two of the three clear wrong merges involved a bundled original, and one involved different analyst figures. [Step 2 log §§10–12](clean-arch/step2-validation-2026-11-07/LOG.md).

5. **The process itself allowed avoidable drift.** c1 combined three changes and went out without the required full prompt audit. Its apparently successful design review did not check the actual request against Alex’s rulings clause by clause. [Conditions investigation §20](clean-arch/step1-unfiled-2026-11-08/LOG.md).

**Conclusions weaker than they look**

The development pass is not a general accuracy claim: the material was heavily exposed, the two draws differed, and matching a passage does not establish correct meaning or linkage. The 112/113 search result cannot establish recall across unknown repeats, and five hits had a counterpart in the group but not in the original shown to the comparator. The grouped-reader result tests selected questions about later details; it does not establish safety when readers encounter wrong groups without being pointed to them.

**Remaining problems, by product impact**

1. Useful information is discarded or disconnected from the view it informs.
2. Wrong grouping and incomplete comparison text can associate different statements; retained text reduces loss but does not eliminate misleading placement.
3. Source meaning, speaker, dates and qualifications can drift, with consequences for both steps.
4. Extra, overly broad or fragmented views and residual noise make the library harder to use; the observed size varies with readers and draws.

**One next angle:** continue the conditions direction in its smallest form: preserve a **useful company financial figure** when no view takes it, retain ordinary links whenever it informs an existing view, and require a supported reason for a new view. Do not introduce a list of approved figures or treat every figure as useful. First audit the complete proposed request against Alex’s rulings and the signed standard; then, when authorized, use the existing saved cases and read the answers by hand, including cash, margin, EPS and empty-library cases.

The idea is falsified as a usable fix if it cannot simultaneously retain the useful unfiled figure, discard the ruled-out cash example, preserve the margin link, and avoid figure-only views across the repeated cases. A successful small check would justify the broader forward measurement; it would not by itself establish acceptance. Step 2’s wrong merges remain open and should be addressed within the same Steps 1–2 boundary.

