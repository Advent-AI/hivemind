# Current state

**Clean Steps 1–3, current (2026-11-11).** Records: Step 1, [round log](../clean-arch/step1-unfiled-2026-11-08/LOG.md) §§16–47; Step 2, [Step 2 log](../clean-arch/step2-validation-2026-11-07/LOG.md) §§12–19.
- **Step 1 configuration: c8, adopted by Alex (D387).** It runs DeepSeek Flash at high effort, with a 64,000-token output cap; a
  format failure or a cut answer is resent once (D380). It carries Alex's decisions D382–D385:
  - figures are conditions;
  - material statements with no thesis are kept without links;
  - only big matters open a thesis;
  - no target prices.

  [PRD §12](../clean-arch/PRD.md) holds its system prompt, closing check and schema; a run with no candidate files sends exactly the
  accepted request.
- **Acceptance (D386, [protocol](../clean-arch/step1-unfiled-2026-11-08/ACCEPTANCE-PROTOCOL.md)).** 50 fresh articles that no run,
  old or new, had used: news from 2026-09-05 to 09-07, a holiday weekend with no NVIDIA posts. One draw; two readers and a third on
  disputes.
  - helpful 132/139 (core 83/83);
  - wrongly opened theses 1 of 10;
  - search 141/143 available repeat pairs, or 141/145 for the whole system (one 11-article story supplies 55 pairs, and revisions are
    barely exercised);
  - clear wrong merges 1/57, plus 2 overlaps;
  - detail retention 22 = 22. This is a storage comparison: every record keeps its own text. It is not a usability test.

  Dev ×3 on the frozen golden-v5 (a lead): helpful 214, 211 and 212 of 234; search 98.9–100%; clear wrong merges about 1%. Step 1
  cost for the fresh set plus dev ×3: $4.20 at published rates.
- **Steps 2 and 3** are built in isolation (`clean-arch/step2`, `clean-arch/step3`): search, comparison, grouping and later linking.
  They are not integrated with production storage. **Step 4 (judging) has not passed** on the clean path: its ladder step is built and
  measured (four Stage A runs, lines missed by 1 to 3 answers; D426), so nothing yet shows the clean system can judge an investment
  view on its own questions.
- **Step 2 is closed and frozen (Alex, D427, 2026-11-11;** [Step 2 log](../clean-arch/step2-validation-2026-11-07/LOG.md) §§14–19**).** It goes
  to production only with the whole clean path, after Step 4 meets its lines; `tests/test_frozen_clean_step2.py` guards its files. Its three lines were met at the acceptance above (one draw; "later version"
  relations barely exercised), and no miss of the seeded end-to-end test (clean 18, 18, 17 against production 17, 15, 16) has
  been traced to it (the two single-draw misses were diagnosed on 2026-11-11, below: neither traces to Step 2). What happened since the close-out of 2026-11-08:
  - A change to Jev's wording for "later version" relations failed its line (42 calls, 2026-11-09) and tuning stopped.
  - One wrong relation was traced to the judge: it put NVIDIA's answer to the Kyber report under the FY2027 revenue question;
    sent both ways, the conclusion did not differ ([result](../clean-arch/step2-edge-effect-2026-11-10/RESULT.md)).
  - Alex stopped work on that relation (D423) and asked for a fix to the rule that gives a "later version" the older record's
    questions. Measured on the three saved draws ([round log](../clean-arch/step2-revision-links-2026-11-10/LOG.md)), removing the
    rule was withdrawn: of the 24 links it wrote, two blind reader families call 19 context and 3 evidence, and one of the 3 is a
    company's answer that would otherwise be missing beside four reports (with it rung 2, 2, 2; without it 2, 3, 2). **The rule
    stays (D424).**
  - **Open, recorded:** Jev's "later version" relation (9 of 30 join different statements in draw 1); the context links it carries
    (19 of 24); wrong groups (at the line on one draw; the unprompted reading test never run); the "Unverified quote" mark not
    shown to Jev (3 of 188); not decided, whether a company's answer must sit under every question its report is filed under.
  - **Reopens when** Step 4 yields judged views on the clean path and a miss, or something a reader of a thesis sees, traces to
    one of these. The round's measurement kit (replay of a saved draw, exact simulation of a writer rule, blind packets with
    controls, a judgement sent both ways) is kept in the two folders above.
- **The clean system's untraced end-to-end misses, diagnosed (2026-11-11;** [round log](../clean-arch/e2e-misses-2026-11-11/LOG.md)**).**
  The China share question in draw 3 and the FY2028 revenue question in draw 2 (seeded test, D392). Both estimates sit on a rung
  line. China: the same window-end request, re-sent, gives the miss twice and the right answer once (the judge's own variation at the
  1% line); no H200 price is in any request. FY2028: draw 2's window-end request gives the miss 3 of 3 and draw 3's the right answer 3
  of 3; draw 2's lacks records draw 3's holds (a "41% in calendar 2027" figure Step 1 filed under FY2027 only, "$1 trillion of
  Blackwell and Rubin visibility", five infrastructure-demand records), not isolated which matters; FY2028 is the question whose filed
  statements differ most between draws (47% shared, median 74%). Neither traces to Step 2. Refuted on the way: that a refused answer
  re-asked caused the China miss. Observed defect of the frozen judge: it names the export-controls theme as a dependency of the China
  question, 42 of 65 refusals in six draws, and the re-ask changed the rung 8 times (PRD 11, E4). No change proposed; 18 sends, $0.043.
- **Open defects, by product impact** (reflection council, `council/av-codex.md`):
  1. **The Ohio-guarantee yes/no question is never covered** in the three dev draws; a broader credit-support amount thesis opens
     instead. Diagnosed (round log §48): the model folds the unsigned guarantee into the open aggregate thesis because the request
     uses "covers" both for "is evidence for" and for "already asks this question". The same clause sits under link clutter.
  2. **A revenue-share thesis was opened** (Vera Rubin's share of data-center revenue), the class-A boundary of D382.
  3. **Link clutter.** A blind recheck of the 34 disputed fresh links found 19 weak and 2 wrong; 10 accepted links mixed in as controls were all useful; the other 49 links were not rechecked.
     The model's own account names topic or theme overlap and inference chains, and c8's closing check never reads back a link. This is
     a likely cause, with no fix proven. Alex approved designing a protected link check through the council; a first draft was stopped
     because it would drop founding premises and contrary facts.
  4. **Unverified passages:** 3 of 188 fresh records and 1–3 per dev draw. The mark now travels into Step 2's records, and a reader sees the found source text or an "Unverified quote" label. Jev's comparison input still carries the model's text without the mark; changing it changes measured Step 2 behaviour and needs its own measurement.
  5. **The lidar policy thesis** recurs at the boundary (one dev draw in three).
- **History.** These earlier states are superseded:
  - the 2026-11-07 takeover (K5 → K6b; [takeover log](../clean-arch/takeover-2026-11-07/LOG.md));
  - the 2026-11-08 close-out (K6b test 32/42; Step 2 first lines; [Step 2 log](../clean-arch/step2-validation-2026-11-07/LOG.md) §12);
  - the unfiled fix round and the c1–c7 arms (round log §§1–39).
- **No run is live.** The branch is committed through the D388 line (round log §§48–59).

**Clean Step 1 source investigation (2026-11-07):** A [source-loss census](../clean-arch/STEP1-SOURCE-LOSS-CENSUS.md) traces two separate losses in the historical cleaner and records reproducible corpus observations. Offline candidate comparisons expose both recovered content and source-identity or contamination risks. A subsequent [full-page diagnostic](../clean-arch/STEP1-FULL-PAGE-RESULTS.md) completed 102 calls on 17 selected articles and independent source-backed review. It exposes examples of both missing or misattributed source text and model errors that persist despite the right text being present. A Codex–Claude council is reviewing the results and earlier attempts; no source-cleaning candidate is adopted, and the source corpus and production defaults are unchanged.

Alex has authorized correcting the test-source cleaner and test data when their defects are confirmed, while the frozen production configuration and ruler remain intact. The cleaner switched 615 originally fed articles off; a replay reproduces all 615, and direct inspection confirms an actual article excluded because its 9,874-character body was flattened to one line. Other examples include a wrong-site shell, paywall and long challenge code, so the false-exclusion count and a general article-identification repair remain to be established. The [council regroup](../clean-arch/STEP1-SOURCE-REGROUP-COUNCIL.md) and [source-preservation design](../clean-arch/STEP1-SOURCE-PRESERVATION-DESIGN.md) describe an isolated candidate checked against all 34,084 records, with a fake-answer actual-runner handoff and provenance display in the replay renderer. The [five source-control calls](../clean-arch/STEP1-CAPTURE-CONTROLS-RESULTS.md) completed and were source-reviewed; two items contain summary details absent from their attached quotations, and one source-visible risk explanation was not returned. This is selected-case evidence, not a general quality result. Broader source-quality comparison, citation completeness and actual writer integration remain open.

**Clean architecture Step 1 (2026-11-06, isolated work on `clean-arch`):** Alex reopened work with the clean architecture. An experimental prepared-source handoff now preserves the archived page, prior cleaned text, source-role decisions and selected-line mapping without changing the original database; quotations for prepared items must also occur contiguously in the original captured page. Two seven-item runs are available in the [clean architecture PRD](../clean-arch/PRD.md), one in the earlier selection order and one in recorded page-timestamp order. The source selector is not a production service and source ordering is not established event-arrival ordering. The runs expose unresolved semantic problems: citations can omit supporting facts despite an exact location match; model output can change a benchmark into a deployment, reverse a backup relation, omit a named customer or assign an unstated currency. A blinded 84-call check-placement/wording comparison and a 27-call same-article citation-completion diagnostic did not give a clean semantic fix and are not adopted. The latter missed an omitted connectivity condition and a reversed backup relationship, and left six expected evidence reviews unaddressed. A further five-round Codex–Claude council produced a narrowly scoped Step 1 link candidate, independently checked for prompt-contract drift. A six-article, 36-call blind comparison completed; the candidate still produced an explicitly self-contradictory link and both arms consistently omitted the same Kyber report and company response. It is not adopted and has not changed the active PRD prompt. A trace confirms that both the Kyber report and open Kyber thesis were supplied, and the raw model answers omitted the report and denial; the reason is not established. See ../poc/data/clean-step1-kyber-trace-2026-11-06/TRACE.md. An isolated six-call comparison showed that hiding the Kyber thesis did not recover the report or denial in any draw. A second six-call comparison returned them in 3/3 draws with the original Kyber paragraph alone and 0/3 with the full article; length, position and surrounding content changed together, so the reason is not isolated. Excerpt outputs have source-attribution limitations. Neither experiment changed state or established a production fix. (Superseded: the next task then was a whole-article coverage approach; the current next task is under "One next task".) See ../clean-arch/STEP1-IMPLEMENTATION-COUNCIL.md. The earlier four-round council agreed that no tested semantic fix is ready; its next investigation is a source-backed review of the 49-item historical run and its 160 evidence records, with overlapping issue flags and separate article-level omissions, then a separate comparison of the seven-item replays. See ../clean-arch/STEP1-COUNCIL-REVIEW.md. Preserve relevant evidence while identifying the next intervention; production/frozen history remains as described below. See [Step 1 run log](../clean-arch/STEP1-RUN-LOG.md) and [English reading page](../clean-arch/architecture.html).

**Sealed (D379, 2026-11-06):** Alex asked to clean up and seal this version while he re-plans the system design. Work stops here and is sealed as it is: main's working tree is committed on branch `seal/2026-11-06` (tag `sealed-2026-11-06`) and merged into `main` on Alex's word (PR #10); the sealed split and two side experiments are pushed on their own branches (D379). No PRD 11 experiment is open, and the E1 next task below is withdrawn. The next task is Alex's re-planned system design.

**E1 diagnosed (2026-11-06, Alex chose E1):** of 57 helpful matters frozen production wrote and then dropped, two readers agree on 17 link misses (4 core), 3 opening misses (1 core) and 24 small matters the standard itself drops; 10 are disputed on the fallback clause and 3 were quote refusals. Opening is not the experiment. The core of the link misses is the model reading a question's period, population or named configuration as a boundary; only 8 of the 13 window draws it dropped were lost to the product. No production change; $0.02 of probes. My recommendation was to fold that narrow change into the next extraction version; withdrawn by the seal (D379). Details: `docs/research/2026-11-06-e1-no-home-drops/README.md`, PRD 11 E1.

**Split extraction sealed as a failed experiment (D378, 2026-11-06):** the split (a new-question call, an evidence call and record preparation) was benchmarked against the frozen poc-v108 and failed. Its stop line fired: helpful matters 156, 156, 159 against 166, 170, 162, with about 15% higher cost. One screened revision kept more noise than production. It is sealed in the worktree `hivemind-no-preseed-evidence-review` (tag `split-extraction-failed-sealed-2026-11-06`), and nothing of it is in main. What it taught is written as proposed production experiments in `docs/prd/11-production-experiments-from-split.md`: E1 no-home helpful drops, E2 duplicate questions, E3 ladder checks with D186, E4 judge refusals, E5 D203's revision day, E6 the measurement kit. Each opens only on Alex's word.

**Question-catalog limit removed (D377, 2026-11-05):** Alex also directed removal of the separate 150 KB catalog rejection. The research reader in this worktree now has neither the catalog nor evidence byte limit; it retains full scoped questions, historical boundaries, dependencies and evidence. A portable 326,996-byte catalog test returns all 400 new questions and expands evidence both after reading the catalog and directly; the old 150 KB guard fails the same test in a scratch copy. The saved 69-question pilot catalog and all 69 saved evidence expansions match their original content hashes. Details: `docs/research/2026-11-05-catalog-limit/`. The full suite remains pending until the paid seven-day run no longer competes for resources. The run remains in its isolated worktree and does not call this research reader.

**Evidence reader limit removed (D376, 2026-11-05):** Alex directed removal of the reader's 1 MB evidence-expansion rejection. In this worktree, `research_context.Reader.expand` now returns the entire evidence payload without that cap, while the catalog's separate limit remained at that checkpoint; D377 subsequently removed it. On the saved pilot ledger, all 69 individual question expansions, the four-question 1,931,225-byte pilot request and the entire 3,454,076-byte catalog produce the exact same content as the pre-change high-limit baseline; the portable oversized-ledger test passes and fails when the old cap is restored in a scratch copy. Details and snapshot-specific measurements are in `docs/research/2026-11-05-reader-limit/`. The seven-day diagnostic runs in `/Users/lchingen/hivemind-no-preseed-evidence-review/poc/data/split-fresh-seven-day-2026-11-05-v2/` with its pinned code; it does not call this research reader. Read its status through its `snapshot.sh`; do not edit its package code while it is live. This change is not an acceptance of seven-day extraction or judgement quality.

**Start-state correction (2026-11-05):** Alex requires a research library established from real material available before the test start, then extraction against that state. The prior empty-library diagnostic cannot represent this case. Our own mistakes and the current 68-question provenance audit are in `../hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/own-mistakes-2026-11-05.zh.md`. Two new A-only calls were run on 2026-08-29 articles using the 68-question prior-day snapshot; both proposed the same aggregate supply-commitments topic. A source/context review judged it distinct from the existing specific SK Hynix question. A third A-only call on an author-body excerpt about DLSS 5, already tracked by v22, passed; the prompt also restricts software updates, so the reason is not established. No writer or dedup ran; source-history completeness remains unverified, and this is not scored acceptance. Details: ../hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/start-state-diagnostic-2026-11-05.zh.md.

**Measurement correction (2026-11-05):** Alex clarified that a gold-worthy topic already in the supplied library should not open again; an absent worthy topic should open. The earlier simple-A claim of a "missed" new topic was not scored against that rule and is withdrawn as a correctness conclusion. In the actual experiment, a Kyber topic was shown and passing follows Alex's topic-level rule; whether its exact release question captures the shipping milestone remains unverified. The experimental pre-article snapshots differ from the replay's day-start snapshots; 9 of 10 inspected examples differ. The current uncommitted replay default does not build a cold-start library; committed main HEAD still uses the old seed and startup filing path. Historical lexical coverage has a confirmed unrelated-topic match. The frozen gold and past scores remain unchanged. Audit: `../hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/measurement-context-scrub-2026-11-05.zh.md`.

**Simple new-question diagnostic (2026-11-05):** At Alex's direction, an isolated prompt returned new questions plus article evidence without asking for product database fields. Four previously seen real dev articles each ran once: three returned one candidate, one returned none, all four quotes matched their source, and the gold-listed GPU backstop amount question was not proposed. Whether that omission is a new-topic miss depends on whether the existing library covers the topic. Two other candidates require source and independent-significance review; the actual experimental snapshot already had a Kyber topic, so its pass follows Alex's topic-level rule; whether its exact release question captures the shipping milestone remains unverified. This is not a production or full-pipeline acceptance. Details: `../hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/simple-new-question-results.zh.md`.

**Split prompt structure v3 read diagnostic (2026-11-05):** One real reading-stage call on a previously seen article found the revenue/margin guidance and Trainium scale but omitted the gold China revenue/market-loss matter. The prewritten stop condition was triggered and the linking call was not sent. This is one draw and not a production or end-to-end result. See `../hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/structure-v3-read-result.zh.md`. D374 removes the model sampling field from active settings and default configs; historical config files and archives retain their original bytes.

**Split prompt structure v2 small test (2026-11-05):** Thirty calls on two previously seen golden-v5 dev articles completed in `../hivemind-no-preseed-evidence-review`. The blind model reader found complete helpful matters in the fresh control versus new A+B of 6/19 vs 10/19, 11/19 vs 7/19, and 9/19 vs 12/19. The new arm also retained more gold not-kept matters in each draw; B missed useful margin guidance and one answer reused IDs, with a demonstrated matching collision. This is not a production acceptance. See `../hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/structure-v2-results.zh.md` and `reports/2026-11-05-parallel-structure-v2.html`.

**Split extraction small test (2026-11-05):** At Alex's request, the isolated `hivemind-no-preseed-evidence-review` worktree ran two real golden-v5 articles once through each split lane. An independent model reader found 7 of 19 helpful gold matters fully retained, two partial, two written then dropped, eight missed, and one retained gold not-kept matter. Three saved v108 draws on these articles retained 7, 9 and 12 of 19, but used 22 seeded questions while the new test used 8/10-question snapshots; these are not directly comparable. The experiment remains unaccepted; see `../hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/small-scored-test-20261105.md` and `reports/2026-11-05-split-small-test.html`.

As of November 5, 2026; decisions through D374. [Decisions](DECISIONS.md) holds what is decided now; the [design page](system-design.html) and the [module PRDs](prd/README.md) hold what the code must do; the [README](../README.md) holds startup, build and run instructions.

## Future evidence scoring (D372)

Alex decided future gold scoring should measure helpful versus not helpful evidence without requiring separate scores for core and supporting. Use frozen golden-v5 as-is: combine core and supporting as helpful, treat not-kept as unhelpful, and keep optional entries neutral. A counting report has not yet been implemented. Historical scores retain their original definitions. D373 removes the stop caused by a separate concern about three question-gold entries: keep the gold unchanged, continue scoring and disclose the concern; see `../hivemind-no-preseed-evidence-review/docs/research/2026-11-05-parallel-refinement/ruler-conflict-2026-11-05.zh.md`.

## Latest decision (D369)

Alex decided in D369 to capture core and supporting evidence without a strict boundary and in D370 to remove the 22 preset starting questions and separate earnings-report import. The replay entry now defaults to `poc-v118` (D374), refuses old seeded ledgers and baseline configurations, and continues to read existing non-seeded questions; earnings releases remain normal source items. This change has local contract tests but has not passed end-to-end product acceptance. The frozen historical rulers and results remain unchanged.

The small 2026-11-05 study used three archived NVDA articles and an 8/28 historical 68-question snapshot: without versus with an appended report, independent AI review found 14/27 versus 13/27 complete matters. This measured appended extraction context, not the distinct former coverage-start step; D370 removes both by Alex's decision. Full traces and limitations are in the separate `hivemind-no-preseed-evidence-review` worktree under `docs/research/2026-11-05-real-input-evidence/existing-library-results-2026-11-05.md`.


**One-day smoke completed (2026-11-05 UTC):** Alex requested a quick 1–2 day end-to-end test. One day, 2026-08-29, ran in `/Users/lchingen/hivemind-no-preseed-evidence-review/poc/data/v117-one-day-smoke-2026-11-05/`: config v117, an 8/28 historical library, 40 extraction calls, 93 evidence records written, four new questions, 54 judged and zero terminal failures. Two judgement attempts were refused and corrected. A Microsoft revenue forecast of $391.1bn was assigned to a rung whose upper bound excludes $391.1bn; the same article's actual quarterly revenue and next-quarter guidance were dropped with no home. Some source dates and bodies are not verified, and an independent 14-article sample review was incomplete due to truncated text. This is not semantic or production acceptance. Findings and scope: `docs/research/2026-11-05-real-input-evidence/one-day-v117-smoke-2026-11-05.zh.md` in that worktree. The clean source-text comparison and its condition-hidden review are complete; council discussion of next steps is ongoing.

**D371, in progress:** Alex directed that present and forward-looking revenue and financial information should be tracked. Diagnose the same-day extraction and filing losses before designing a general change. No new financial tracking implementation has been accepted yet. The old frozen standard and gold are unchanged. The original prompt-only pilot failed design review. The user approved an exact prompt addition for an experiment; it is not a production implementation. Four paired real-article diagnostic calls per arm completed for the exact approved sentence: v74i versus experimental role-d371-pilot. Microsoft next-quarter guidance and NVIDIA FY2028 guidance still dropped in the treatment; a single draw is not acceptance or proof of causation. Details: docs/research/2026-11-05-real-input-evidence/d371-prompt-pilot-results.zh.md (isolated worktree). The requested full prompt audit and restructure were drafted experimentally; five real-article paired diagnostic requests per arm completed. Microsoft revenue guidance was missed in both arms, and the draft produced unsupported original dates, a quote refusal and suspect links. No production prompt change or acceptance; see restructure-pilot-results.zh.md in the isolated worktree.

**Clean Step 1 coverage council (2026-11-06):** Codex and Claude Code independently reviewed the existing attempts and completed three discussion rounds. The proposed next research candidate moves the existing evidence-reading block ahead of the thesis-opening block while preserving the article, open-thesis state and paired output. It is a hypothesis, not an implemented or validated fix. A complete prompt/contract audit and independent review precede any controlled Luna comparison. Historical paragraph-based and source-first experiments, their noise and attribution problems, and the rejected overlap-based merge are recorded in [the council review](../clean-arch/STEP1-COVERAGE-COUNCIL.md). No new Luna experiment was run in the council.

**Clean Step 1 coverage order result (2026-11-07):** The isolated 54-call clean comparison completed and all answers were reviewed blind. Moving the evidence-reading block recovered a known Kyber report and denial in one of three candidate answers against none in three controls, with attribution blur; it also produced unsupported gaming-to-AI links in two candidate answers and no controls. It is not adopted. A separate exact-quote example misattributes an executive's prediction in the standalone summary. [Results and replay](../clean-arch/STEP1-COVERAGE-ORDER-RESULTS.md) record all selected cases, uncertainties and source-fidelity work; no production ledger was written.

**Clean Step 1 fidelity council (2026-11-07):** Codex and Claude Code completed five rounds on source attribution, conditions, dates and meaning. No tested fix or root cause is established. The agreed source-to-record review of 49 articles / 160 evidence items and the subsequent isolated field-order comparison are complete; the later 54-answer / 217-record repeated sample remains separate. Prior source-first, quote-first and follow-up-review experiments and their limits are recorded in [the fidelity council](../clean-arch/STEP1-FIDELITY-COUNCIL.md). No Luna experiment or production change was made in this council.

**Clean Step 1 fidelity review (2026-11-07):** All 49 saved source packets and 160 original evidence items have received a source-and-record review; focused independent cross-checks cover the findings and selected controls. The [review and article replay](../clean-arch/STEP1-FIDELITY-REVIEW.md) distinguish source contamination and missing source material from model meaning, citation, date and link issues. The [isolated schema property-order diagnostic](../clean-arch/STEP1-CITATION-ORDER-RESULTS.md) completed all 66 calls and condition-blinded article reviews. Several omissions and semantic errors persisted; it did not establish a fix and is not adopted. It used saved articles and before-states without changing production.

**Clean Step 1 source handoff council (2026-11-07):** The ongoing [council and offline checks](../clean-arch/STEP1-SOURCE-HANDOFF-COUNCIL.md) reconstructed 16 matching article-34 controls, all omitting a Kyber report and denial; the cause remains unknown. The 20-article saved source-role overlap review distinguished previously cited AI-generated summary lines and an unrelated recommendation from authored body. The clean runner does not send the saved source-role labels; the council chose to first compare original and previously selected source text on ten known articles. The isolated 60-call source-text comparison and condition-hidden review are complete; [results](../clean-arch/STEP1-SOURCE-TEXT-RESULTS.md) show specific contamination reductions alongside persistent omissions and changed meaning. It did not advance state or write production. The isolated six-article low-versus-medium source-fidelity diagnostic completed 36/36 calls and condition-hidden review. [Results](../clean-arch/STEP1-REASONING-FIDELITY-RESULTS.md) show partial improvements alongside persistent source-qualification and attribution concerns; no production setting is changed. The [prompt audit](../clean-arch/STEP1-FIDELITY-PROMPT-AUDIT.md) maps the observed failures to the full request and signed standard. The six-article isolated schema-description comparison completed 36/36 calls and condition-hidden review; the candidate did not preserve the repeated example qualification and is not adopted. [Results](../clean-arch/STEP1-SUMMARY-FIDELITY-RESULTS.md). A further six-article 36-call low-versus-medium comparison used corpus-cleaned sources outside the original 49-item clean replay and a fixed exploratory context; results were mixed, including unsupported links and incorrect attribution/date fields. [Results and replay](../clean-arch/STEP1-ADDITIONAL-SOURCES-RESULTS.md). The structured-claims candidate was not sent after review revealed scope and complexity concerns. Council review of the next action is ongoing. The date-text schema-description diagnostic completed 48/48 calls on eight known cases, with mixed results; the candidate is not adopted. A selected-run census found twelve literal "null" strings in date-text fields, but no production writer impact is established. [Results and replay](../clean-arch/STEP1-DATE-DESCRIPTION-RESULTS.md). A further preregistered eight-source date comparison completed 48/48 calls; the candidate lost a supported company-article statement date in all three draws on one source and is not adopted. [Results and replay](../clean-arch/STEP1-DATE-NEW-SOURCES-RESULTS.md). A bounded corpus census confirmed 163 source pages across three explicit generated-summary structures whose labels were removed while some summary text was retained; two NVIDIA cases were reproduced through the cleaner. [Source provenance investigation](../clean-arch/STEP1-SOURCE-PROVENANCE-CENSUS.md). A read-only source-lineage replay reproduced 363/363 cleaned pages with current inputs, preserved ambiguous original-line locations, and surfaced the generated-summary label loss for review. [Source investigation and lineage replay](../clean-arch/STEP1-SOURCE-PROVENANCE-CENSUS.md). An offline neighboring-context observation exposed only 144 or 149 of 163 known labels and introduced many other page lines; it is not adopted as a general source fix. [Observations and viewer](../clean-arch/STEP1-SOURCE-CONTEXT-OBSERVATIONS.md). A new [saved-quote integrity investigation](../clean-arch/STEP1-QUOTE-INTEGRITY-CENSUS.md) reconstructed 360 saved answers across eight overlapping cohorts, including 78 prepared-source calls. Five saved unverified passage instances were complete matches under the existing normalization; an in-memory candidate recovered their original slices, while ten others remained unverified. The normalized source-slice lookup is now installed only in the isolated clean Step 1 runner; saved-answer and entry-point checks are recorded there. Page provenance, Unicode completeness, production resource budgets and writer integration remain open. The existing writer stores only one quote, whereas 63 of 160 evidence items in the 49-article exploratory trace have multiple passages. A [source-first 49-article coverage review](../clean-arch/STEP1-COVERAGE-CENSUS.md) separates material missing from the model input from source-visible omissions in the saved answers, with uncertain matter boundaries labeled. (Superseded: the next investigation then was why supplied material is missed; the current next task is under "One next task".) The canonical prompt and production configuration remain unchanged. Adding fallible role annotations remains a separate untested candidate. Council streams and handoffs are in `poc/data/clean-step1-ongoing-council-2026-11-07/`.

## What runs

- **Nothing is live.** The two-week run of D563 finished on 2026-11-16 at 01:23 local (`poc/data/clean-carried-run-2026-11-16/`, draw
  complete, ledger $3.476 of $6.00); its readings are recorded (D564, [result](research/2026-11-14-use-acceptance/carried-run/RESULT.md));
  the six contested last answers are being traced at $0 (`docs/research/2026-11-14-use-acceptance/contested-six/`).
- **Pipeline (replay default `poc/config/poc-v118.json`, D370, D374).** Every item reads the relevant open questions from the library at the start of its day, then extraction v74i on `gpt-6-luna` proposes evidence and questions; Jev matching with the collision judge matches them; code writes the records; judging-v7 judges changes once a day; pull mode closes due questions. There is no separate seed or coverage-start report import, and reports as source items remain eligible. This default has not completed end-to-end acceptance. The [pipeline guide](poc/pipeline-plan.md) maps stages to code.
- **Measured:** one company (NVDA) over one 14-day window (2026-07-01 to 07-14), the judgement scored at the window end on the frozen ruler (AGENTS §7.1). Three draws of `poc-v116` against three of `poc-v108` run in the same hours: 53 against 45 agreements of 57; operating margin and capex agree in 3 of 3 draws, never judged without the coverage-start reading ([acceptance](research/2026-11-04-filing-end-to-end/acceptance-design.md)).
- **Served data:** the service, the MCP server and the standalone page serve the sealed three-month ledger `served-2026-10-28-v34-nvda-3m-through-0828` (68 theses, 34 groups; D358), built by the earlier `poc-v34` pipeline, not by the replay default. HTTP `/library`, MCP `thesis_library` and the standalone page share the dated bundle writer.
- **Idea API:** `poc-v118-idea` (D290, D335, D374): two discovery calls and one adoption and weighting assessment; only adopted theses with positive weights appear, and nonempty plans total 100%. The [Idea contract](poc/idea-card.md) owns its fields and the limits of its scores.
- **Interface:** the Thesis Library and Explore Ideas workspaces, with the confidence Trigger and an Action preview (no wallet connection or order execution). The [UI specification](poc/thesis-ui.md) and the [integration guide](../poc/ui/README.md) own its behaviour.
- **Repository:** `main` holds the product, the frozen ruler and the research records; run databases, logs and model archives stay on disk (D353), located by the [data manifest](research/2026-10-25-english/data-manifest.md). Worktrees: `/Users/lchingen/hivemind` is the main checkout, where slice branches are cut from `main`; `/Users/lchingen/hivemind-extraction-quality-2026-10-28` (the extraction branch, merged on 2026-11-03) keeps in its ignored folders the stored end-to-end runs of `poc-v91` to `poc-v95` that later comparisons read (D359); `/Users/lchingen/hivemind-run-v109-2026-11-04` is the finished judging-v8 run's worktree. Older branches stay in Git without worktrees (D359); none is merged work in progress. The clean source-text comparison and its condition-hidden review are complete; council discussion of next steps is ongoing.

## Open defects

1. **Competitor and customer news is filed under the company's revenue questions** instead of the share, capital-spending or custom-chip question it informs (D355; filing is otherwise about 85% right). Share facts are often not written at all, an extraction recall miss. The total-revenue question holds about a quarter of all links (D354).
2. **One bet opened twice** about one encounter in five: the collision judge splits a seed question from an identical candidate on a fine detail (D354).
3. **A question the standard rules out** (the lidar legislation) was proposed by the extraction and opened in one draw of three (D354).
4. **A thesis opened from an article gets no dependency of its own**: the default Jev matching asks for none (`views/jev_matching.py`), although D51 has the matching call choose them; themes still reach every company thesis through the theme block (D191, D195). Found in the 2026-11-05 consolidation; building it is decided (D368).
5. **Historical coverage-start reading, retired by D370** (D364–D366): the capital-spending line is missed in about one read in six (the question is then left as it was); a labelled guidance figure is written with the fact tier; later reports reach the questions only through the daily stream; `scripts/preflight.py` does not replay the reading's check.
6. **Measured on one company and one 14-day window**, the judgement scored at the window end only; no version of the current pipeline has completed a longer window (a 60-day run of `poc-v108` was stopped at Alex's word after 2026-07-15, [log row 8](research/2026-11-04-argument-record/log.md)). The China-share question (v17) swings between draws (0 of 3 in the acceptance, 2 of 3 in its control, 1 of 3 in the frozen draws): two readers found the starting figures did not cause the acceptance's drop, and the byte-identical extraction request kept a "share fell to zero" sentence in two candidate draws and dropped it in two control draws. One acceptance draw judged nothing on v16; its cause is not established.
7. **What a judgement reads grows with the window** (D358). Argument records (D201) were measured as the remedy on 2026-11-04 and not built: judging-v8 agreed 12 of 17 against 15 of 17, judging-v9's card added little at about half again the judging cost; their code was removed at Alex's request ([log rows 4–11](research/2026-11-04-argument-record/log.md)).
8. **Seen once, not traced.** A judgement named a shown theme as a dependency and the check refused it twice, stopping a draw for a day (2026-11-02, D266). The sealed run's review recorded that a succession's opening evidence is not linked to the new question (D358), not yet checked against today's code.
9. **Earlier defects, unchanged.** Matching (build log row 49): another document's copy of a figure can be treated as new evidence; one matter can occupy several groups; same-answer candidate references caused seven chain or duplication decisions of the generative matcher; empty `original_who` values can count as the same party; different names for one population cause two of nine Jev merge misses. Nine 2026 aggregate-spending theses under `ai-capex` each have a different population; whether to combine them is a product choice. Extraction's instructions remain narrower than the PRD's important-question rule and omit the personal-memo exception, and extraction can change a quantity's meaning before matching (a guarantee amount against financing provided). Classification keeps its [recorded simulation defects](research/2026-10-25-english/classification-existing-defects.txt). The corpus audit recorded 97 official notices with 56 body and file-name collisions, to re-fetch before relying on a rebuilt corpus. An older intermittent search-test failure is untraced. Fresh Idea allocations vary while saved weights do not; the confidence chart applies the current plan to past states and is not a calibrated probability; broad analyst-prose quality and fresh Idea stability remain unaccepted (the [Idea contract](poc/idea-card.md) lists its limits); generative matching dependencies await `matching-v4`. The readers' doubts about the frozen standard, listed in the [extraction branch's state page](research/2026-11-01-e2e-loop/current-state-extraction-branch-2026-11-03.md), remain for Alex.

Upstream supply and the human review pool's output remain deferred.

10. **A new-system store being written serves its first day in progress** (D573, D574; `docs/research/2026-11-14-use-acceptance/page-contract/LIVE-READ-DESIGN.md`, B):
   before any day completes, the service's default date falls back to the latest judgement's day. Not built: a correct guard needs one
   snapshot for the check and the read, MCP's start and the streamed Idea response handled; 0 of 143 stores are in that state and no
   new-system store is served live today.

## One next task

**Where the lean path stands (2026-11-15; D489 to D542).** Alex is not active (D509); D439 is in force: choices go to the
council (an independent Codex review and Claude) until consensus, recorded citing D439; nothing is pushed, deployed, published or
committed; paid calls stay within D439's $40 ceiling (about $18.42 recorded; $0.0134 sent in this period, the ten judge calls of
D511 and D519; the lean path $8.34 in all). Every stretch below is closed; its full record is in the decision log and in
`research/2026-11-14-use-acceptance/LEAN-LOG.md` (sections 1 to 43).

- **The choice between the systems is not made.** The fresh week did not separate them (D489, "not clear"; nothing since ranks
  them). The comparison that could choose by measurement was sized and not sent: at the proposed size it may miss differences
  that matter ([sizing](research/2026-11-14-use-acceptance/comparison/COMPARISON-SIZING.md), D517). **Production stays the default
  and both systems stay (D518).** Alex's product choice on the company's financial figures stands (D505: evidence for related
  questions, no table and no questions of their own; D382 and D384 stand).
- **For Alex:** the [decision page](research/2026-11-14-use-acceptance/DECISION-PAGE-2026-11-15.md) (its section 7 is the one list
  of what is his to choose, what he has decided and awaits building, and the defects with their evidence), the
  [side-by-side week](research/2026-11-14-use-acceptance/side-by-side/SIDE-BY-SIDE-WEEK.md) and the
  [judge note](research/2026-11-14-use-acceptance/unsupported/DESIGN-NOTE.md) with its one choice.

**Open defects found on this path, each with its evidence; nothing is built on any of them:**
1. **The new system's delivery gap** (D506, D508, D513, D514): a kept fact that bears on a question by a step of reasoning may be
   linked to another question or to none, and so never reach that question's judge; the later-linking step skips a group whose
   original statement arrived under another question. Three confirmed fact-and-question pairs in the fresh week, 23 unresolved
   ([census](research/2026-11-14-use-acceptance/delivery-class/CLASS-CENSUS-RESULT.md)); one six-call test of its effect was
   inconclusive ([result](research/2026-11-14-use-acceptance/effect/EFFECT-TEST-RESULT.md), D511). Paused.
2. **The judge, shared by both systems** (D519, D520): on a question that asks for an amount it names a band when nothing shown
   sizes the amount, or closes the last gap with a number of its own (36 of 438 stored readings, many of them the same
   question read on successive days: a failure pattern on a few question paths, not an error rate;
   [census](research/2026-11-14-use-acceptance/unsupported/UNSUPPORTED-CENSUS.md)). Three of the ten settled unsupported answers
   coincided with a figure the system held and had not delivered to that question
   ([result](research/2026-11-14-use-acceptance/missing-input/MISSING-INPUT-RESULT.md), D530 to D532). What the product shows is
   Alex's choice (the judge note).
3. **The old system's duplicate questions** (D520 to D523): three pairs in the fresh week; one second question was never compared
   with the first, the others were compared and kept apart
   ([result](research/2026-11-14-use-acceptance/duplicates/DUPLICATES-RESULT.md)).
4. **The old system's filing under the broader question** (D529 to D531): the data-center revenue question never received the
   next quarter's guidance or a consensus for the year, filed under total revenue only
   ([cases](research/2026-11-14-use-acceptance/d375-measure/SAME-DAY-CASES-RESULT.md),
   [trace](research/2026-11-14-use-acceptance/missing-input/FILING-TRACE-RESULT.md)). The relation `docs/prd/10-filing-phase.md` §2 names.
5. **Where decisions and code part on dependencies** (D541, D542): `writing.write` drops an edge that would close a circle with a
   note where PRD 06 says refuse and ask for a correction; PRD 06's "historical only" branch has a reader and no writer; the
   label the seeding module writes on every seed edge (`last_end`) is defined nowhere; no decision says what happens to a later
   proposal with another direction for a pair already read.

**Decided by Alex, awaiting implementation and acceptance (not asked again):**
- **D375, each article sees the questions committed before it.** A passed, bounded serial proof with labelled fake answers
  ([result](research/2026-11-14-use-acceptance/duplicates/D375-PROOF-RESULT.md), D526, D528); the eligible same-day cases of the
  fresh week read (D529). A real measurement needs a new version of the reading request and a paid run; not opened.
- **D368 item 2, the matching step chooses a new question's dependencies.** In the unseeded fresh week one clear case among 97
  pairs (data-center revenue reading total revenue;
  [census](research/2026-11-14-use-acceptance/dependency-selection/DEPENDENCY-SELECTION-CENSUS.md), D537). As the code stands
  one stored edge has two readers (whose conclusion to read; which of two homes is the narrower): the same edge would remove
  seven filing links ([proof](research/2026-11-14-use-acceptance/dependency-selection/EDGE-PROOF-RESULT.md), D538). A design that
  reads the two uses apart is recorded as **a provisional candidate, not sound for build**
  ([design](research/2026-11-14-use-acceptance/dependency-selection/SEPARATION-DESIGN.md), D539 to D542): two proofs on stored
  data, the package's suite run under it, every stored dependency row classed. If the slice is reopened, its review must first
  settle the cycle through an awaited question at creation, closing behaviour, a theme shown twice, the historical readers and
  the label. A statement's home is not something an edge can decide (its section 2.5): the reading step's, the filing phase's
  subject. No selection call is designed; nothing was sent.
- **D368 item 4, the reading direction for preset questions** (settled by Claude on Alex's delegation): not measured (D536); the
  stored seeded draws already agree with the frozen reference on 15, 15 and 16 of 17 questions; the rebuild and dry-run harness
  is kept ([page](research/2026-11-14-use-acceptance/dependency-channel/CHANNEL-ASSESSMENT.md)).

**The choice is made by the council under D439 (D544, 2026-11-15): the work toward production carries forward on the new
system; the old system stays the running default until the new one passes its gates; both remain.** Nothing that runs is
switched, deleted or deployed. It is not a finding that the new system's answers are better: the cold reflection (D543) found
nothing that ranks the two systems' answers, and the first consensus left the choice to Alex; that deferral was withdrawn the
same day, because his words in D439 give the council the job of taking a course. Reasons: he had reopened work on the rebuild
and D439's scope names its steps; it follows the product rule on financial figures he last confirmed (D505); the fresh week
gives no demonstrated reason to abandon it and shows fewer trivial or duplicate questions in that one run. Kept in view: its
answer-choice step has not met its lines, Stage B did not pass, integration is undone, and its cost and time to production are
unknown. **Alex's word overrides this at any time**; it is also reconsidered on a change of his product rule, a sound comparison
on shared subjects that favours the old system, or the rebuild failing its unchanged gates within a bound agreed later. A first
checkpoint: $5 of further spending without a candidate that passes its prewritten small test returns the direction to the
council.

**Since the choice (D545 to D550, all under D439):**

- **The fresh week's answer choices, read and traced (D545 to D547).** Of 21 attempts on seven questions, one agreed fault of
  Alex's lines (a condition of the topic left out of the choices, six attempts); ranges written with no figure were overrun by
  the first filed amount on two questions (the old system shares this). A census of 49 amount questions and an audit of the
  request found an undefined term ("the topic's wording") and no mechanism general enough to design for; no prompt change
  ([result](research/2026-11-14-use-acceptance/fresh-ladders/FRESH-LADDERS-RESULT.md),
  [audit](research/2026-11-14-use-acceptance/fresh-ladders/PROMPT-AUDIT-LINE-2.md)).
- **The gates the new system must pass (D548), in order:** the answer-choice step on Alex's lines (D400), not passed; the
  judge on the system's own questions (D428), not passed; the end-to-end comparison with Step 2's checks (D427, D431), still
  owed, "beats" not yet defined in numbers; use on unseen news (D484), its lines proposed and not his; integration and
  release, not written ([frame](research/2026-11-14-use-acceptance/NEW-SYSTEM-FRAME.md)).
- **The first blocker (D549):** the step declines some worthwhile questions. From the July refusal review, no general,
  permitted change recovers them: no candidate.

**The one-week diagnostic of the answer choices is run and read (D550 to D554, 2026-11-15): not clean.** Nothing is live. The
new system read the 272 articles of 2026-10-06 to 10-12 in two parts (the first part stalled when the laptop slept with a call
in flight; it was ended and continued from the library after article 120, D551, D552); only the topics and the answer choices
were then run (the matching and the judge are recorded as not run, D553; they can be run later from the merged trace by a
decision of their own). Result ([page](research/2026-11-14-use-acceptance/second-week/RESULT.md)): 13 topics; of 39 attempts at
answer choices 9 were declined, on 4 topics, two of them in all three attempts; three of the zero-fault lines are missed on
faults both reader families agree on; the count by written choices is missed (6 of 12 against 8). The fresh week's picture (no
refusal) did not repeat. It is evidence, not a gate: it passes nothing and reverses nothing. Traced at $0: the largest reason
for declining over every stored run (22 of 37 refusals) is a topic that asks two things (two years, or two figures), which the
step declines by Alex's own rule (D397), a known open defect "until splitting is built"; it starts in the first step's field
for what a topic tracks. Ledger $3.67 of the run's $3.95; paid calls under D439 about $22.10 of $40 (Claude's ceiling). D544's
$5 checkpoint is reached for further weeks, so the direction is back with the council.

**Changed in the code (D552):** each call of the new system's first step waits at most 600 seconds on a silent connection
(`clean-arch/step1/live.py`, `CALL_WAIT_SECONDS`; five tests). Before it, a machine that slept during a call stopped the run for
good; with it, the second part survived eight lost attempts and a second sleep.

**Open defects found on the way:** (1) a lost attempt is charged its whole reservation on the ledger (about $0.12 against a
cent for an answered call): eight of them used up the room for the matching and the judge; the rule is the design's and was
not changed. (2) The note given to the answer-choice step and to the readers says a year's figures are "published around
2027-02; use that day", while code sets the due day 60 days after the fiscal year-end (D414): the two reader families read the
due day apart on 23 points. (3) Reader sessions' dollar cost is not known and is outside every ledger.

**After the diagnostic (D555 to D558, all at $0):** the council refused a rule that would take the first-named figure as a
topic's main one (D397, D469, D470); a study of the "no main part" refusals found no candidate
([study](research/2026-11-14-use-acceptance/second-week/NO-MAIN-BOUNDARY-STUDY.md)); a map of all four stored readings, reconciled
to their reports, shows agreed faults on the zero-fault lines in every reading (6 to 8 marks, of kinds that change) and no
bounded way on the record to bring the four to zero together ([map](research/2026-11-14-use-acceptance/second-week/FIRST-GATE-MAP.md));
an audit of the two classes that are the step's own (an event's reference; unlisted parts) with an independent second read
finds no bounded, product-relevant repair ready ([audit](research/2026-11-14-use-acceptance/second-week/PROMPT-AUDIT-TWO-CLASSES.md)).
**The first gate is recorded as not met; Alex's lines (D400) stay as written; no pass is claimed.**

**The core-problem council (D559, 2026-11-15; asked by Alex after the week's result, his words in the decision log), all at $0:** the product
problem is forming answerable questions: a worthwhile matter is left without an answerable question, or a delivered question
asks a materially different or potentially unresolvable thing; no single cause is proven. Over July's three runs two reader
families found 18 matters: the same judged question in every run that opened it on 3 (a fourth disputed), delivered but
different on 3, a question in one run and a refusal in another on 4, refused in both on 1, opened by one run of three on 6.
The clean measurements examined (July, the weeks of 09-22 and 10-06) each start from empty, which the start-state correction
of 2026-11-05 above says does not represent the test with an existing research library; that record had no decision number
and was not carried into D466 or D469. In the two later weeks, by two families with the articles, 18 of 20 opened topics were
standing matters, 16 of 20 were opened from an article that mentions the matter in passing, and 10 of 20 were on a matter an
earlier-dated library already held a question on. These classify 20 selected topics; they are not a rate, and nothing shows
yet that a carried library prevents the failures ([council](research/2026-11-14-use-acceptance/reflection-3/cold-codex-5.md),
[round log](research/2026-11-14-use-acceptance/LEAN-LOG.md) §51).

**The reflection council (D560, 2026-11-15, asked by Alex; his words in the decision log), all at $0:** the goal is a
continuing research library in which an analyst finds the important questions, the facts for and against, and a present
answer whose reasons are visible; the record carries four goals at once and no single number for "ready". The measuring
method is a major part of the impasse, beside demonstrated product defects, and the present sticks cannot apportion the two:
the first gate has substantial reader disagreement, nothing on record clears it and it has no measured link to the final
answer; the July end-to-end reference could not rank the systems at that size; the conditions measured were not the
product's. The next step is a pilot of Alex's own product-level review on the stored fresh week (sixteen cards, three hidden
repeats, controls, three completeness sheets), beside the frozen reference and the gates, replacing and ranking nothing;
then D559's comparison. The role of the six answer-choice lines is put to him after the pilot. No gate, line or frozen piece
changes ([council](research/2026-11-14-use-acceptance/reflection-4/council-codex-3.md), [round log](research/2026-11-14-use-acceptance/LEAN-LOG.md) §52).

**The small comparison ran on Alex's "go" (D561, D562; $0.43):** with the week of 09-22's library the first step re-opened none
of the four questions it held and filed their facts under them (4 questions opened against 16 from empty, none duplicating the
library); it did not open the equity-commitments question the empty read opened and lost a DOJ/FTC question on the Groq deal;
by the rule written before the run, between its two outcomes ([result](research/2026-11-14-use-acceptance/carried-library/RESULT.md)).

**Where it stands (2026-11-16; D563 to D567; Alex not active, D439 in force; about $26.07 of D439's $40 spent):**
- **The two-week product-condition run (D563, D564):** read in five ways; gate 1 (Alex's six lines) is not met there either (7 or
  5 of 13 topics right); no last answer is unsupported by both reader families and 6 of 12 are contested, for too little
  evidence to choose a band and for question forms, not for undelivered facts ([result](research/2026-11-14-use-acceptance/carried-run/RESULT.md),
  [the six](research/2026-11-14-use-acceptance/contested-six/RESULT.md)).
- **The judge naming a band where nothing sizes it (D519, D520):** closed for Alex with its record (D565, D566): the judge's own
  account does not separate failed from passed answers; reader families agree only when no amount is the starting point. The
  choice (leave the band, label it, show none) stays his ([self-report](research/2026-11-14-use-acceptance/self-report/RESULT.md),
  [source check](research/2026-11-14-use-acceptance/self-report/SOURCE-CHECK-RESULT.md)).
- **Integration (gate 5) moved twice:** the product's page reads the new system's store (D564); the new system's daily loop now
  closes due questions with production's closing step, walks calendar days and owns its sequence (D567,
  [design](research/2026-11-14-use-acceptance/carried-run/CLOSING-DESIGN.md)). A production defect found on the way is fixed: a
  closing on a day without items was invisible at the next day's start (`src/hivemind/replay.py`, D566).
- **Waiting on Alex (D560, unchanged):** his half hour on the pilot's cards
  ([the deck](research/2026-11-14-use-acceptance/pilot-deck-1/deck-1.html); his marks tallied by `tally_deck.py` against the key in
  `~/.hivemind-keys/pilot-deck-1/`), then the six lines' role, then D559's wider question.

- **Gate 1's reading repeated (D568, D569):** the same 39 sends read again from identical packets give the same line verdicts; line 2's
  failing sends are identical (reproduced by the method, not proved right). The parts a question does not judge (L) were shown nowhere.
- **The product page now reads the new system (D570 to D573):** the page shows D397's "Not judged" parts beside the answer; it reads the
  new system's events, theme ranges and unrecorded shapes without inventing a direction (neutral, named, no Idea composite); the API
  serves a new-system store, closings included, and the page renders it ([result](research/2026-11-14-use-acceptance/page-contract/RESULT.md),
  [serving](research/2026-11-14-use-acceptance/page-contract/SERVE-RESULT.md)). Listed for Alex, not changed: production's Yes/No colours
  and its inferred theme scores state a direction the question may not hold.

- **Serving while writing (D574):** no partial day leaks into the completed-day view; a freshly opened page now shows the served
  library's latest completed day. The first day of a live store is open defect 10.

- **Alex's page (D575, D576):** `docs/research/2026-11-14-use-acceptance/DECISION-PAGE-2026-11-16.md`, six choices in order, checked
  against the records. The live-service design is paused (D575). Stage B's control line cannot be exercised by re-sending the judge (D576).

- **The unlisted parts (D576, D577):** the request never ties "the topic's wording" to a field. 12 failing attempts on 7 matters leave
  out a second figure, event or cap; 10 of them sit only in the topic's outcome. Arm A defines the wording in all four places. The
  probe (18 stored requests, unchanged and changed ×3, about $0.15) was sent 2026-11-16 to `poc/data/clean-unlisted-probe-2026-11-16/`
  (`docs/research/2026-11-14-use-acceptance/unlisted-parts/DESIGN.md`).

- **The unlisted-parts probe (D578 to D580):** negative under the rule fixed before the send. The changed written answers left no part
  unlisted, against 4 or 5 control topics; but the change declined twice where both readers said it should not. The two accounts
  apply line 6's decline rules to the outcome's words. No sourced rule for the main part of a multi-part topic survived review
  (`unlisted-parts/DECLINE-AUDIT.md`, `rule-review.md`). Arm A is stopped.
- **The Idea planner (D580, D581):** a new-system three-choice event is shown to it as Yes and Still open. The design is parked as
  recorded input (`idea-planner/`).

- **The hold lifted, arm A2 (D582, D583):** Alex's standing instruction to keep going outranks D581's hold. A2 adds D436's rule for a
  second side of the same bet to arm A. It is negative under the rule fixed before the send.
  - **What it fixed:** no part left unlisted and no refusal on the motivating topics (the control left parts out on 6 topics); every
    refusal control kept.
  - **What it broke:** it lists an event's own outcomes, and the source the answer is read from, as not judged (9 of 137 entries,
    against 1 of 71).
  - **The bar itself:** run against itself, the unchanged request already breaks the "+1" bar on 5 marks (`unlisted-parts/RESULT-A2.md`,
    `control-vs-control.txt`).
- **Arm A3 (D584):** A2 plus one closed-set sentence that removes, for an event only, an entry that merely restates one of its outcomes
  (D409, D397). It was built at $0 through council rounds 78 to 93 (`unlisted-parts/DESIGN-A3.md` v11).
  - The three arms (control, A2, A3) are sent on the same 28 topics.
  - They are read with the existing reading and a pre-registered diagnostic one.
  - A lead stays provisional until a trace review classes every failure above the control.

- **A3 and the edge (D585, D586):** A3 is negative under its fixed rule.
  - Two of its failing checks were measurement errors (`unlisted-parts/RESULT-A3.md`).
  - Its real side effect: on another event it lists the Ruled-out rung's own named decision as not judged.
  - Tuning of the not-judged list's edge stops (D391). A2 stays an unaccepted candidate.
- **A fresh comparison of A2 (D587 to D589):** no stored topic set is held out. So the frozen first step ran on the unread week of
  10-13 (383 articles), starting from the 10-06 week's library (`poc/data/clean-fresh-a2-2026-11-16/`).
  - **The run:** complete, $3.45, 5 topics opened.
  - **The populations:** population (a) has all 5. Population (b), classed blind, has 3 different matters, under the minimum of 5,
    so the comparison gives no verdict (D589).
  - **The council's choice (round 102):** send and read the 5 topics as registered, then close the comparison. Pooling the corpus's
    last week was refused.

- **The fresh reading (D590):** the frozen step on 5 fresh topics misses lines 2, 3 and 5 and meets line 4. A2 is better or equal,
  with no verdict; the comparison is closed (`unlisted-parts/RESULT-FRESH-A2.md`).
- **The due-day mark's split (D590):** Codex first readers fail D on 133 company figures with code's day, Claude on none. A D-only
  diagnostic held all 12 class items in both families, so it is noted as a reader discrepancy and the brief is unchanged
  (`fresh-a2/d-diagnostic/RESULT.md`).

- **Ruled-out rungs that catch a postponement (D591):** in 296 frozen-step event answers there are 37 company delays on deadline
  questions and 1 authority case (Taiwan p3). No decision settles whether "not by the due day" rules an event out. The step and the
  form are unchanged, both readings are recorded, and the 38 answers are listed beside gate counts as candidates affected. The
  question is on Alex's page (`fresh-a2/postponement/BOUNDARY-CASES.md`).

- **The final-answer test's control line (D592):** an unchanged re-send stays at 4 comparable controls of 8, and delivering three
  facts reaches at most 7. It is not pursued for the line's sake (`stage-b-controls/DESIGN-SHORTFALL.md`).
- **The live store's operating contract (D593):** version 9 is agreed after nine council rounds for a $0 proof build on test stores
  (`live-service/OPERATING-CONTRACT.md`). Live operation is not authorized. P1, the exception to AGENTS §9 for the product's own
  readers, is only proposed.

- **The live store's proof build (D594 to D597; nothing deployed, no service restarted):**
  - **Slice 1:** one owner for every upper date bound. A future date is refused, and the served product store's half-processed
    2026-08-29 is no longer returned.
  - **Slice 2:** one pinned read transaction per API request and per MCP call, and MCP connections per call.
  - **Slice 3:** search ranks and embeds only what a request may see.
  - **Slice 4a:** the writer's WAL store, its stops and its orderly end.
  - **Slice 4b (D598, corrected in D599 and D600):** one writer per store by an operating-system lock, preflight's one locked copy, the
    snapshot route, every reader opening a store by its own path, and the writer leaving WAL mode on every exit. The
    filesystem-full proof was run separately.
  - The suite passes (341), and so do the new system's folders (190).

**The live-store contract's proofs are all built at $0 on test stores (D594 to D603):**

- the resolver;
- pinned reads, through one opener that names the store on failure;
- visible-only search;
- the writer's WAL store, stops, lock and end;
- preflight's locked copy and the snapshot route;
- serving while the built writer runs (proof 10);
- the page's day reaching the Idea call (2f);
- the crash, disk and busy proofs.

The suite passes (346), and so do the new system's folders (192). Nothing is deployed or restarted. P1 (the AGENTS §9 exception for
the product's own readers) stays only proposed, and the running service picks up the new behaviour only on a restart, which is
Alex's.

**This session's investigations, all at $0, closed with evidence (D604 to D612):**

- line 5's fresh misses (D605);
- the postponement repair, with D606's provisional reading reversed (D607);
- the shared fiscal-year note (D608);
- delivery of the company's own figures on the carried fortnight (D609, D610: 5 bearing statements undelivered on 3 questions, none
  predicted to move an answer by a blind second reader);
- a same-news comparison from established libraries (D611: underpowered, and no unread week left).

The council's reversible decisions on Alex's page are recorded in D606 and D607.

**The merge test (D678–D680, 2026-11-19): closed; the registered test did not pass.** The old system opens questions, clean Step 1 reads
and files under them, and the frozen judge answers. It ran on 70 articles × old-2 and old-3, with a hybrid arm and a control arm, for
$2.13 ([result](research/2026-11-19-merge-council/RESULT.md)).
- **Held:**
  - delivery: the decisive statements reached the judge on 4/4 primary questions in both draws;
  - talks stayed talks;
  - both blind readers supported all 4 hybrid answers;
  - no five-company or 2027 figure was taken as the answer;
  - c8 proposed no NVIDIA-figure question.
- **Missed:**
  - P2's proxy clause: total capex is used for data-center capex without being named a proxy, which old also misses;
  - V: the rebuilt control's v47 was unsupported, and a reconstruction effect is not ruled out.
- **Not shown:** that the merge answers better. The old answers were already supported, and the capex band was set by 09-06 history.
- **Next:** superseded by D681, below.

**The one next task: none open (D689, D690, 2026-11-20).** poc-v118 is the product (Alex chose A, D690), and the research line
rests until his new direction. The hybrid's release line is paused, and the judge and c8 lines are closed for now. A line reopens only
on its condition below. No paid send is open, and D439 has $0 available without Alex's word.
- **D689 (Alex chose option 1; council N closed both lines; record:
  [council-n-codex.md](research/2026-11-20-hybrid/council-n-codex.md), [council-n2-codex.md](research/2026-11-20-hybrid/council-n2-codex.md)).**
  - **Judge.** The carried previous conclusion holds rejected forecasts: on full evidence, 0 of 13 move with it and 8 of 13 without it,
    with 0 of 8 controls moving.
    - The readers jointly support 4 net repairs against the 5 required, including M14 in two of three old draws.
    - The frozen gold reads 44.3 against 45.0, with China share regressed.
    - It reopens on eight eligible failures on fresh questions, which the design never read and are counted once across draws, with
      matched controls and a source-checked summary of the omitted facts (D198 option 2). Then the D198 choice and its price go to
      Alex.
  - **c8.** It showed no improvement in the final answers tested, and adds about $24 to old's about $9 over 82 days. It reopens on a
    traced decisive fact that old missed, c8 delivers, and that could change a named final answer.
  - **Spend (an error of mine).** "Inside D439's $40" was written in D679, D682 and D684 with no tally. D439 stands at about $39.65 or
    $44.42 under the two readings. Phase 1's ledger is $2.64, not $2.4.
- **History of this line (D681–D688)** follows. Alex opened the hybrid's build and
test, and asked that problems not be found only at the end (his words are in the D681 record). Plan: [PLAN.md](research/2026-11-20-hybrid/PLAN.md). Design:
[DESIGN-J2.md](research/2026-11-20-hybrid/DESIGN-J2.md).
- **Where old loses on the 32 matters:**
  - it never opens 17;
  - it opened M08 and M14 in 3/3 draws, but the judge reasoned wrongly: amounts that overlap were added, and a figure of another scope
    was taken as the answer.
- **Census:** 24 answers rejected by both readers ([CENSUS.md](research/2026-11-20-hybrid/census/CENSUS.md)).
- **Found at $0:** the judge writes the rung first and its reference and derivation last (`schema_for` appends the stance fields to
  the end of `properties`).
- **Arms:**
  - J2a, the schema order only;
  - J2b, J2a plus an overlap and scope check.
- **The probe and its rule** are written before any J2 send. Its regression guard is the frozen judgement gold: the stored v7 requests
  give 15/17, 15/17 and 16/17, and are rebuilt byte for byte.
- **Status (D685):**
  - **The judge line is paused within D198.** Four angles have failed:
    - J2a and J2b fail the locked blind reading;
    - removing the previous conclusion misses its screen by one, and the frozen gold reads 44.3 against 45.0;
    - H1, the heading only, gives 0 net repairs against 2 in council J's blind diagnostic.
  - The carried derivation holds the rejected rungs. Every remaining lever changes D198.
  - **No fresh test exists on this corpus.** The judge's errors sit in about ten numeric bets the design has read; 27 fresh bets gave
    1 target against 8 needed.
- **Opening census (D686):** [OPENING-CENSUS.md](research/2026-11-20-hybrid/OPENING-CENSUS.md). Of the 16 matters old never opens:
  - 6 are merged into a held question, because the scoring list is finer than D197 and D248;
  - 5 fall outside the library's NVIDIA-only subject;
  - 5, plus M05, are never proposed, though D248 allows them; a fix needs a new extraction version (D274).
- **D382 answered (D687; his words are in the record):** in the hybrid, a company's own material figure keeps its own question, as
  old's opening does.
- **Attainable check (D688, council M):** [OPENING-CENSUS.md](research/2026-11-20-hybrid/OPENING-CENSUS.md), last two sections.
  - The census found no credible path to a D665 lead through opening changes alone.
  - The concrete misses within Alex's rules are M20 (a $125B unsigned obligation, D388) and M05. M09, M30 and M25 are coin flips.
  - Noise costs about 1.4.
  - What binds: the list counts finer than D248/D388 on 9 matters, the NVIDIA-only subject on 5, and D198 on 2.
  - No opening test is sent.
- **D688's recommendation, answered by D689:** keep poc-v118 as production and pause the hybrid's release line. Questions on other
  research-list companies' key figures are offered only for their own value. Spend: phase 1 $2.64 of $3 (ledger); `phase1b` $0.36 of
  $2.

**Earlier next task, closed by D676 and D677 (D665–D675): read the release comparison's six draws when they finish, with the council-reviewed tools**
(`docs/research/2026-11-17-product-comparison/RUN-PLAN-v12.md` §1.4–§1.6; `DESIGN-1.6.md` v7; D675).

- **Done:**
  - stage 0 and slice 2;
  - the full run, six draws, launched together at 22:36 on 2026-11-17 under `poc/data/comparison-2026-11-17/run/`;
  - every reading instrument built and passed by the council before any output was read: reading tools in round 5, the §1.6 tools in
    round 10; the scorer hardened through Codex rounds 11–21 (D675); 101 stage0 tests, 75 mutants on the reading tools.
- **Result, 2026-11-19 (diagnostic, 5 draws; Alex stopped new-1).** The new system loses on the release comparison.
  - Of 32 key matters, the new system serves 2–3 and the old one 10 (a = 0, b = 7–8). The controls pass.
  - Even a perfect new-1 could not reverse it.
  - The new libraries miss the core revenue, margin and capex matters.
  - Details: `docs/research/2026-11-17-product-comparison/RUN-LOG.md`, `poc/data/comparison-2026-11-17/reading-diagnostic/`.
  - **Diagnosed (D676, council):** D382's figure exclusion plus the Step 1→ladder bundled-question loss (D432). Even repaired, the new system ties at best. The old system stays; no further comparison run.
  - **The goal loop is closed (D677, council).** The old system stays and no paid work continues. It reopens only if Alex reverses D505
    or funds a full run, with a written path to passing first.
  - **The one-outcome probe failed its line 1** (`docs/research/2026-11-19-one-outcome-probe/RESULT.md`): it fixes the period bundles
    but not the deal bundles.
  - **What a pass would take** ($0 arithmetic on the frozen list; pass = a − b ≥ 5 and a ≥ 2b):
    - **Under D382:** the old system keeps 4 figure matters the new one can never take, so b ≥ 4. The new system would need at least 9
      matters only it serves, out of the 14 its rules allow that the old system misses: 6 shared quantities, 5 obligations and 3
      policy steps. Today it serves 0–1 of them.
    - **With D382 reversed:** at least 5 of 17, the 14 plus 3 figures the old system misses, provided it also matches the old system on
      the rest.
    - **Either way:** passing needs much broader opening, not a wording fix.
- **(Superseded) When all six draws end, in this order:**
  1. `eligibility.py`: six complete draws, launched within 1 h, sends within 72 h.
  2. `mapping.py export`, then `read`, `third`, `result`.
  3. `mark_cards.py deck`, then `mark`, `debate 1`, `debate 2`, `readings`.
  4. `score_comparison.py <run root> <mapping out> <marks folder>`: rebuilds every derived file from the primary data (refuses any that
     differs, the readings record included) and gives the verdict and the printed-beside quantities on the rebuilt snapshot.
  5. `d400_code_check.py` and `step2_lines.py`: the hard checks and the release status.
  6. `d400_reader_lines.py` and `d431_reading.py`: printed beside.
  7. A council loop on the result, and a row in `TRIES.md`.
- **If a draw stops:** no release verdict; a diagnostic export (plan §1.4 item 10).
- **If the verdict is not a practical lead:** the council-loop skill on the traces, and the next try from another angle (D674).
- **Monitored** in `RUN-LOG.md`. Out-of-scope findings go to `FINDINGS.md`.
- **Held** (D662): answer-choice changes, model trials, and live-store, planner and integration work. D658 waits (D664).
- **Open:** D661 (past Codex readers ran with memories on); D656's listing omission; the 589 uncommitted paths (his call).

**After D638:** the stop hook rejected the hold, so the council opened D612's fourth condition with a new candidate, astra with arm A2
(D436's second-side sentences; D639).
- **Two readings,** both VOID by their planted listing controls (D640, D641).
- **Descriptive only:**
  - A2 wrote H20 2 of 2 where the frozen arm declined 2 of 2, unflagged by both product reviewers;
  - memory is disputed;
  - agreed hard-line failures frozen 2 against A2 0;
  - the listing harm is unmeasured.
- **Its status:** astra with A2 stays provisional and unadopted, and the route stops.

**The state, measured today** (`reflection-6/`, D623 to D637):
- **The readers are valid** (D625).
- **Higher effort and a required field are closed** (D626), and so is a paired gate-3 comparison (D628).
- **Sol** fails 9 of 78 sends on the 26 topics outside the 44. **Astra**, on the unchanged request, fails 4 of 78, all main-part
  declines (D633, D634).
- **The main-part choice is unsourced** (D631). Two rule candidates closed (D631, D635). Six cases are on Alex's page.
- **A source-backed review of astra's 51 written questions** finds 11 material defects that gate 1 does not count (D636).
- **A one-clause correction** (`due-day/candidate-system-v2.txt`, the binding-obligation day narrowed to amounts per D210 and D403)
  fixes the signed-deal completion date in its probe, 4 of 4 against 0 of 4, with no control moved.
  - Its verdict is inconclusive on one unrelated listing split (D637).
  - It is kept beside the frozen request, unadopted.
- **Two leads closed at $0:** the MIIT listing (request-independent) and the purchase-commitment ranges (the recorded fixed-range
  limitation).
- **A third lead closed (D638):** Rubin's widened window follows the topic's own period field, which contradicts its description. It
  is an opening-step wording defect, recorded and not taken up.
- **Council round 28:** "the record stands; no further step is supported on the present evidence". Work reopens on D612's conditions,
  including a new concrete reversible candidate.

**On Alex's page** (`DECISION-PAGE-2026-11-16.md`, item 2):
- the six main-part cases;
- the measurements, kept separate;
- the v2 correction;
- D403's consequence for events proven after their day;
- the reader brief's D row.

The gate-1 measurement on his 44 topics, and any adoption, are his (D426).

D612's four reopening conditions govern paid work again.

Alex's page (`DECISION-PAGE-2026-11-16.md`) is kept current.

The paragraphs below are the record of where the clean path's Step 4 stood on 2026-11-12.

**Clean Step 4 (D396–D430):** the ladder step was measured four times and has not passed Alex's lines; it is frozen as it ran
in the fourth measurement (D426). The frozen judge's baseline on the ruler's ladders is read (3% unsupported, all in figure
questions). **Stage B (the judge on the ladder step's own questions) ran and does not pass** (2026-11-12,
[result](../clean-arch/step4-2026-11-10/stage_b/STAGE_B_RESULT.md)): the control line is unexercised (4 controls comparable with
reader B's material shown, 8 needed; all 4 agree); the judgement lines are met except the last-judgement line on its strictest
reading (3 of 24). Next: the diagnosis of how Step 1 cuts a matter into theses (D432), including council B's $0 trace of the 8
controls excluded on the question and the 3 with missing material; the end-to-end gate is against production as it now runs,
with no preset questions (D431). Where the whole clean path stands, read by the council:
[progress](../clean-arch/step4-2026-11-10/PROGRESS-2026-11-12.md), [consensus](../clean-arch/step1-unfiled-2026-11-08/council/kr-consensus.md).

- **What Step 4 is:** the first thing built and tested is the **ladder step alone**: the call that turns a thesis Step 1 opened
  into one judged question with its answer ladder and due day, or declines. The frozen judge follows only when the ladder step
  meets its lines (Stage B, run 2026-11-12: does not pass).
- **Alex's decisions in force (2026-11-10):** one judged question a thesis, the other parts shown as not judged (D397); the step
  carries D186 in full (D398); the request may teach how to build an event's five states (D399); Stage A is read against his six
  fixed lines with no paid control arm (D400); build and send Stage A capped at $3, a missed line stops and goes to him (D401);
  an event's due day is a stated date or the period's last day (D403); a theme's state is never named with a company label
  (D404); a reference's words are the article's own, else the answer is sent back once (D405); the build uses the request as
  first sent, and code refuses and sends back the faults of writing (D407).
- **How the build was reached:** twenty single reviews and five rounds by angle did not reach zero findings (15, 9, 15, 11, 11);
  four small sends ($0.105) then showed that sentence changes to the request corrected the writing and lowered the declining of
  topics with no main thing (`clean-arch/step4-2026-11-10/probe-2026-11-10/READING-claude.md`).
- **The build** (`clean-arch/step4-2026-11-10/ladder/`, `stage_a/`): the step, its model caller, the Stage A runner with one
  spending limit and an on-disk ledger, the accounting, the readers' packets and the collection of readings; 109 tests, with a
  mutant for each check (40, 11 and 16, all caught).
- **Stage A, sent 2026-11-10** (44 stored theses, three sends each; $0.17 of the $3): 111 ladders, 17 declined, 4 refused twice
  by code. Two reader families and a third reader on the 73 marks where they differ:

  | line | as ruled | whoever reads |
  |---|---|---|
  | 1. no ladder asks another question | missed, 11 of 111 | 0 failed by both families |
  | 2. no ladder leaves a part unlisted | missed, 4 | 0 failed by both |
  | 3. no outcome with no rung or two | missed, 16 | missed, 7 failed by both |
  | 4. no refusal without a justified reason | missed, 2 of 17 | missed, 1 failed by both |
  | 5. 35 of 44 theses right in two of three sends, 28 by a ladder | missed, 21 and 16 | 36 and 30 if every differing mark held |
  | 6. the three sends agree | missed: the favourable end differs in 2 of 8 theses, the due day in 11 of 32 | by code |

  The two families read the form at different strictness (47 against 84 of 111 ladders sound) and the third reader is of the
  stricter one, so the count as ruled is the strict reading. The 25 ladders both families fault are the firm set: five states
  for the company in 10 of 17, yes/no in 2 of 24, figures in 12 of 67.
- **The classes** (result page): an event's five states (gaps, overlaps, labels, the object); a Yes that needs a confirmation
  the No does not; a reported amount carried as the market's expectation, and an expected range the field cannot hold; a
  figure's due day estimated anew in each send; the direction of a commitment's amount; a company's quarterly figure laddered; a
  group named and not listed, which the families read differently.
- **Stage A does not compare the step with production** (D400). The reference reading of 36 production ladders, other
  questions, held every firm mark on 19 and on 25 by two readers.

- **Open defects of the ladder step:**
  - it misses its lines in both measurements; the event answers are changed (D409) and their class is smaller, not closed; a
    figure's due day, the reference (D411), a company's quarterly figure and the direction of a commitment's amount are not
    yet changed;
  - the readers' two families differ at every level (first readers 60 against 90 of 114 ladders sound; third readers agree on
    21 of 70 points), so a line's verdict can turn on the reader;
  - check 6 sets a footnote marker aside, one thing more than D405's record names: reported to Alex, not confirmed;
  - the check on pointing at the item misses "at the item date" (one instance in 111 ladders); mark Q owns the rule;
  - the design lost its block on the outcomes of a send, the lines and the accounting at version 29 and had it put back at
    version 31; the fourth and fifth review rounds read the design without it.
- **Alex decided on the result (2026-11-10):** stay at this step, change the event answers first, check at no cost and have it
  reviewed, then run the same Stage A once more within the $3; the other classes one at a time; no Stage B (D408). An event is
  answered in at most three outcomes, it happened, it is ruled out, or neither, the last written by code (D409, superseding
  D399). A group named and not listed is not a fault of a question (D410). An amount already reported may be a figure's
  baseline when named as that, built after the event answers (D411).
- **Done since, at no cost** (design version 32, §5.2.1): the request, the schema, the checks and the view writer answer an event
  in three outcomes; eight stored theses whose first answers had a gap are answered by hand and pass every check, each former
  gap in one rung; the form carries D410 and the event rules; a differing mark goes to two third readers, one of each family,
  and an unresolved point is counted both ways.
- **Reviewed, probed and sent again (2026-11-10).** Three council rounds on the change did not say "ready"; what they found was
  closed by one structural rule (code writes the scope of a ruling out: new, whole and standing) and read by two families on
  stated facts (20 of 20 alike, then 21 of 23). A small send (26 theses, $0.03) showed the model writing the new shape; a
  decline check beside a fresh control showed 8 against 9 of 15. The second Stage A was sent on my reading that the council's
  two conditions were met, not on its clearance ($0.15; 114 ladders, 16 declined, 2 refused twice).
- **Alex's instruction (D412):** every round is reflected on in the council to a recorded consensus, then the next test goes
  straight ahead on the PRD and its numbers, with every trace read by Claude itself.
- **The reflection council's consensus (round log §69, `council/ja-*`, `jb-*`):** no change to the request, the checks or the
  form until the second result is read in full and reported; then one next step (if the event class is not closed, report
  it, and fix at this step only where the cause is found and no decided rule changes; if it is closed and the lines are still
  missed on due day or direction, diagnose the figure's due day over its whole class first); the next stage is not asked for
  in advance. Alex decides: any change to what the product does; an important part of a thesis that three outcomes cannot
  carry; whether an event undone counts as happened; the footnote marker; the next stage.
- **Second Stage A, read (2026-11-10;** [result](../clean-arch/step4-2026-11-10/stage_a/result-2/RESULT.md)**).** The six lines are
  still missed. Regression: the due day is the same across sends in 18 of 34 theses, against 21 of 32. On what both first
  readers fail, against the first run: R on 4 ladders (7), N on 0 refusals of 16 (1 of 17), 37 theses right and 32 by a ladder
  (36 and 30), event ladders with a fault 8 of 43 (13 of 44), theses whose three sends differ in shape 1 (7). On the two third
  readers' agreed rulings: Q fails on 2 ladders, L on 1, R on 5; 34 theses right and 29 by a ladder, against the 35 and 28 asked.
  The favourable end still differs in the same two theses. The two third readers, one of each family, agree on 21 of 70 points,
  so every line is reported under both countings, and how many ladders are sound cannot be said from readers alone.
- **The council's consensus on what follows (round log §69, `council/jc-*`):** the event class is smaller and not closed, so
  it is diagnosed in full first, at no cost (the model's own ruled-out sentence not bound to a decision after the article; a
  question and an answer with different periods; a 2027 question judged in 2028; the object of a regulator's decision); then
  the figure's due day over its whole class, with D411's reference checked on its own; the changes and a plan go to an
  independent review; a third Stage A needs Alex's word. Reading disagreements a document settles are settled; the few that
  need a decision go to Alex.
- **Done since, at no cost (round log §69, council `jd`):** the event class counted on the second run (a ruled-out sentence with
  "after": R held by both readers on 27 of 31; without: failed or disputed on 9 of 11); one clause of code's sentence changed
  so that the scope governs the model's own sentence; proved on six real answers shown with the sentence as it was and as it
  is (`dryrun14/`): both reader families place an earlier decision in "ruled out" 6 of 6 before and in "still open" 6 of 6
  after, 36 of 36 placements alike and as fixed beforehand. The proof is of six sets of stated facts, not of the judge, and
  the event class is not called fixed (a question and an answer with different periods; a missing ruled-out rung; the object
  of a regulator's decision). A figure's due day counted on both runs and a candidate rule replayed
  (`stage_a/due_day_rule_replay.py`): agreement 18 to 32 of 34, with three figures set months late; no rule is recommended yet.
- **D411's reference, built, reviewed and probed (design §5.2.2; round log §69, councils `je`, `jf`):** the reference carries its
  kind (expected, or last reported for a figure) and a range by its two ends; the judge's middle rung says "the amount last
  reported" for a reported amount. Two council rounds corrected it before any send (a range is spanned end to end by the
  middle range; "the same quantity" is defined against a part, a ceiling and another quantity). A small send on 18 theses
  ($0.016, one draw) filled the field as written beforehand in all seven reference cases, kept the declines for no main thing,
  and sent back no first answer for its quotation (the second run: 68 of 132), which is not claimed until a full run shows it.
- **After the reference change: what else moves, and line 6** (round log §69; councils `jg` to `jj`;
  `clean-arch/step4-2026-11-10/probe-direction-2026-11-10/RESULT.md`). Read by hand, the small send also showed three company
  figures called "higher is good" and two events with a worse ruling out. A three-arm probe registered before its send (the
  request as the second run sent it; the working request; the working request with `unclear` allowed for a company figure's
  favourable end; 96 first answers, $0.074) found no signal that the reference change caused either: the old request sent in
  the same run shows both. It also showed the quotation refused in 15 of 34 first answers of the old request against 5 of 35.
  Line 6's two halves were counted at no cost: the favourable end differs within a thesis on two obligation theses in both
  full runs, and the model's own account says the texts do not settle it; two independent readers of the texts alone find
  "lower" settled in none of seven obligation theses, where the working request says "lower" in 19 of 21 answers. Letting the
  model answer `unclear` moved the wobble to two other theses (not shown to work by the registered test). The due day is the
  same in 18 of 34 theses and would be in 32 of 34 with a day set by code from the year.
- **Alex's choices (D413, D414, D415; 2026-11-10):** where the texts do not settle it, an amount the company owes or
  guarantees is registered with the lower end favourable; code sets the due day of a year's figure whose day would be an
  estimate (the fiscal year-end plus 60 days; a calendar year-end plus 90); the third Stage A is sent without asking again
  once each change is proved small and reviewed, and a change that does not pass stops and goes to him. Both rules are built
  (design §5.2.4). D414 replayed at no cost on the second run's stored ladders: one due day in 31 of the 33 theses still
  whole (18 of 34 as sent), the new refusal firing only on the three theses that are not a year's figure.
- **The third Stage A (2026-11-10; `clean-arch/step4-2026-11-10/stage_a/result-3/RESULT.md`):** sent under D415 after two
  small sends proved D413 and D414 (a sentence first added to the request with D414 was refuted by the first small send and
  removed; `probe-d413-d414-2026-11-10/RESULT.md`). 132 sends, 108 ladders, 24 declined, none refused twice; $0.11. **Line 6
  is met on both halves** (the favourable end the same in 9 of 9 company-figure theses; one due day in 34 of 35). Lines 4
  and 5 are met on the two readings that favour the answer (37 theses right, 29 by a ladder) and missed on the strict one.
  **Lines 1 to 3 are missed on every reading**, by 1, 1 and 3 ladders that both first readers fail (a survey question re-cut
  to a calendar year; a part not listed; three events that write the wait as the ruling out). The two third readers agree on
  21 of 70 points. Spent under D401's $3: $0.755.
- **Alex's answers after the third Stage A (D416 to D419; 2026-11-10):** the six lines stay; the ruling out of an event is
  tried as a typed answer (who decides, what they decide) and proved small first; a rolling twelve months with no
  publication day is declined; a government's permission or ban on a class of products belongs to the theme; the fourth
  Stage A is sent without asking again once each change is proved small and reviewed. The largest thing both readers fail
  was diagnosed first: a wait written as the ruling out, 7 of 140 stored event answers read in full, six on product-deadline
  theses (`stage_a/result-3/wait-as-ruling-out-hand-read.md`).
- **After the third Stage A: four rules of Alex's, each tested alone, then the fourth Stage A (D416 to D421; design §5.2.5;
  `clean-arch/step4-2026-11-10/stage_a/result-4/RESULT.md`).** D417 (a rolling twelve months with no publication day
  declined), D420 (an authority's proceeding always has a ruling out), D418 narrowed (a tracked government decision is the
  theme's) and D416 (an event's ruling out as who decides and what they decide) each passed a small send of its own; the
  typed ruling out failed its first trial and passed its second, after D420. The fourth Stage A: 132 sends, 104 ladders, 27
  declined, 1 refused twice; $0.11. **Lines 2 and 6 are met under every reading** (the favourable end the same in 9 of 9;
  one due day in 33 of 33 theses whose three sends are ladders). Line 5 is met on the two readings that favour the answer
  (40 right, 31 by a ladder) and missed on the strict one (34 and 25). **Lines 1, 3 and 4 are missed**, by 1, 2 and 3
  answers on the third readers' agreed rulings (0, 1 and 2 on what both first readers fail): a Kyber question that both
  branches of its thesis answer Yes; a question and a Yes condition on different periods; a "restructuring" counted as a
  ruling out; three declines for "two figures, none the main one" that no earlier run had. The third readers agree on 29
  of 53 points. Spent under D401's $3: $1.136.
- **The second-look test (D422; `clean-arch/step4-2026-11-10/probe-second-look-2026-11-10/RESULT.md`): it did not pass.**
  76 answers of the fourth Stage A, each sent back once with one instruction that names no fault ($0.12); one blind
  reading round of 102 items. Of the 18 answers with an agreed fault, 6 mended (9 needed); of the 30 unfaulted, 3 counted
  against it (the page fails at 3). It mends what one rule and one field show (the three wrong refusals, a ceiling as a
  reference, a missing unit); it removed two correct references, turned a correct refusal into a ladder and traded one
  fault for another twice. The round also re-read the fourth run's answers: 14 of its 18 agreed faults are agreed again;
  the two third readers rule alike on 22 of 54 points. Spent under D401's $3: about $1.25.
- **Alex's answers (D425, D426):** the second look is not adopted; the ladder step is not tuned further on the 44 theses and
  no fifth Stage A is sent. **Stage A has not passed** (lines 1, 3 and 4 missed by 1 to 3 answers of 131). By his word the
  preparation of Stage B opens on the step as it ran in the fourth Stage A; no paid Stage B send without his word again.
- **The Stage B baseline reading (`clean-arch/step4-2026-11-10/stage_b/RESULT.md`):** the frozen judge on the ruler's
  hand-written ladders, 159 stored judgements read by Codex and Claude Opus 5.5 after seven reviews of the plan: 4 of 151
  decided judgements UNSUPPORTED (3%), all in figure questions (4 of 52, 8%; yes/no 0 of 99), 7 INSUFFICIENT, 16 of 16
  questions end the window SUPPORTED. Every fault is in three figure questions before a sized amount is in view. Controls:
  6 of 6 planted caught by both families. The lines' chance behaviour is measured (`line_chance.py`). Council B consensus
  (`km`, `kn`): put Stage B's lines and the paid send to Alex.
- **Stage B (2026-11-12, `clean-arch/step4-2026-11-10/stage_b/STAGE_B_RESULT.md`): does not pass.** Three draws, 236
  judgements, $0.42; the reading plan reviewed five times; trial 6 of 6; both families caught 6 of 6 planted answers. Line 3
  unexercised (eligible 7, material shown 4, all agreeing). Lines 1 and 2 met (26 of 26); figure 3.4/3.2/10.5% against
  12.7/12.5/14.4%, yes/no 0.9/0.8/4.9% against 5%: met; last judgements missed 3 of 24 on the strictest reading. The families
  differ on 22 of 236 and the third readers split on 12 (9 along family lines). Patterns: three-outcome events kept at "Still
  open" because nothing is settled yet (Kyber); figure questions with no reference figure the evidence cannot size (19
  INSUFFICIENT); a figure carried forward. Council B (`council/la-codex.md`): stands with corrections, applied.
- **The control trace (done, `stage_b/CONTROL_TRACE.md`):** most of the 8 question differences are already in the Step 1
  thesis (the article's angle: a programme inside a total, the reported date, a later milestone); two missing items are stored
  with no link to any thesis though the capex thesis was open; leads, not an attribution.
- **The Step 1 diagnosis (D432, `clean-arch/step1-diagnosis-2026-11-12/DIAGNOSIS.md`, version 8; seven council rounds):** c8 states
  "one quantity for one period, or one event", but its merge rules carry neither D38's year boundary nor D388's signing exception;
  the second year of an annual quantity is never opened (3 graded misses). Proposed to Alex: carry D38's year boundary into two
  merge sentences (+151 characters), first tested on stored articles with a c8 arm. Recorded, not proposed: outcomes with a second
  thing in them (under most of Stage A's ladder faults, a class to investigate); rolling periods and small matters against c8; a
  contract gap between c8's shared_quantity and the ladder step's object and theme rules.
- **c14 (D433), stage 1 (`clean-arch/step1-diagnosis-2026-11-12/STAGE1-RESULT.md`): does not pass.** Both years of hyperscaler
  capex opened apart in 7 of 9 sends against a line of 8 (c8 0 of 9); one send lost the capex question (c8 never); $0.24. The
  misses: the model choosing one year as the bet, and c8's "a customer expanding capacity … is not a thesis of its own" colliding
  with shared_quantity. Stage 2 not sent; c8 stays in force.
- **Gate 1 done** (`clean-arch/step1-diagnosis-2026-11-12/gate1/`, D435, D436): change 2 (the capacity counterexample scoped) passes
  G1-b; changes 1 and 2 together fail G1-a, separating the two years of hyperscaler capex in 5 of 9 sends against a line of 8 (c8: 0 of
  9; 20 of 26 over every year-wording send on that article). The misses decline the second year as too much. c8 stays in force.
- **Alex carried changes 1 and 2 to gate 2 (D437).** Gate 2 (`clean-arch/step1-diagnosis-2026-11-12/GATE2.md`, version 11) passed
  its review in round 11 (`council/mi-codex.md`): c15yc against c8 on seven stored neighbours in three draws, 126 sends, about $1.8,
  ceiling $2.2.
- **Authority (D439, 2026-11-13):** Alex is not active; every choice goes to the council (Codex + Claude) until consensus, recorded
  citing D439. Paid spending in this period: $0.83 (gate 1) of a $40 ceiling (Claude's setting); gate 2 sent on Alex's word (D438).
- **Step 1's combined candidate stopped (D441).** Gate 2 failed on the memory article; the council's memory diagnostic (D440) found
  c15yc opens a memory-price question less often (17 against 28 of 54, interval -34.6 to -4.8) and pushes it from the ruler's
  2027-against-2026 shape to 2026; c8 stays. Spend so far $4.77 of the $40 D439 ceiling.
- **The next step (D442–D444): an exploratory end-to-end census.** The clean path's stored chain (unseeded draws 2026-11-10, Stage A
  run-4 ladders, Stage B judgements) against fresh production draws (`poc-v118`, no seeded questions), on the frozen judgement ruler by one
  method (`clean-arch/e2e-comparison-2026-11-13/DESIGN.md` v4). The first three draws stopped at an over-conservative ledger (D444; kept
  as records); three fresh 14-day draws completed 2026-11-13 03:46 (`poc/data/clean-e2e-comparison-2026-11-13/draw-q1..q3`: 243 items
  each, 0 failed, 13, 12 and 15 own views; recorded $0.43, $0.46, $0.46). D442's same-day comparison stays owed for D427.
- **The census result** (`clean-arch/e2e-comparison-2026-11-13/RESULT.md`): on the seven graded questions both systems agree with
  reader B on one or two a draw (production 1/1/1, clean 1/2/1; two unresolved each); no eligible judgement disagrees in either; every
  loss is at opening (event deadlines against the standard's rules, the memory comparison never opened, scope). A measuring-stick concern
  (D430's same deadline against the standard's 18-month range for q23) is recorded apart (D373), scoring unchanged.
- **After the census (D445–D447):** the trace of the clean path's 17 graded opening losses found no single mechanism; a typed-unit
  audit found identity fields detect 2 of 16 and recover none, so that line stopped.
- **The wiring (D447, D448), built and proved at $0** (`clean-arch/e2e-comparison-2026-11-13/WIRING-DESIGN.md` v4; round log §81): one
  shared spending ledger over every paid call (Step 1, Step 2's embeddings and Jev, the ladder step, the judge, production), the
  ladder step's and the judge's inputs as arguments, a per-draw orchestrator (`run_fresh.py`). The $0 proof passed: Stage B's three
  databases rebuilt row for row through the new inputs; Step 1 (one day), Step 2 (a whole draw, byte for byte), Stage A run 4 (every
  outcome of three passes), the judge and production (one day) each sent every network call under a ledger reservation; a ledger
  refusal stops every component; bypass mutants are caught. Full suite 287 passed.
- **The code review (D449):** eight defects found and closed by four structural rules (stops shared and read before every actual send;
  launcher liveness by its lock registered on the ledger; one reservation bound and settlement rule; the proof through the real
  orchestrator). `proof_end_to_end.py`: one day through `run_fresh.py` (5 child processes, 55 calls, all reserved), a killed child and a
  killed orchestrator handled; full suite 287 passed. Redo of Step 1, Step 2 and production only by a reasoned relaunch; a crash stops
  the run.
- **The slice (D450) ran and the wiring works live** (`clean-arch/e2e-comparison-2026-11-13/SLICE-RESULT.md`): both draws complete in 8
  minutes, every component with real sends on one ledger, every ledger line attributed; $0.159 of ledger (about $0.15 at the published
  rates). Every answer read.
- **The full run (D451) completed** (`poc/data/clean-e2e-full-2026-11-13/`, 05:44–08:33; c2's Step 1 redone after a dropped response,
  D453): ledger $11.43, every line attributed (`spend-by-component.json`). Clean 15/10/15 theses, 69/72/92 judgements; production 12/13/14
  views, 92/80/104 judgements, 0 failed. First read in the round log §84.
- **The full run, read (D452–D455):** Stage A on the 40 fresh theses misses lines 1–5 and meets line 6 (`STAGE-A-FULL-RESULT.md`); the
  census (`CENSUS-FULL-RESULT.md`): settled agreements on the seven graded questions clean 2/1/0, production 1/1/1 (2/2/1 and 2/2/2 with
  unresolved points counted), no eligible judgement disagrees, every loss at opening; the clean path kept 51 of 55 decisive facts of its lost
  questions, production 39 and left kept Kyber and Ohio facts unlinked; Stage B line 3 unexercised (0 settled, at most 4 of 8), its judgement
  reading stopped (D455).
- **Traced since (D456–D458), all at $0:** production's kept-but-unlinked facts cost no final answer in this window (three mechanisms,
  `unlinked-trace/UNLINKED-TRACE-RESULT.md`); the opening losses hold few shown breaches of the standard, spread over small mechanisms, and
  their largest classes are choices the standard leaves open (`opening-review/OPENING-REVIEW.md`); no opening phase is opened.
- **Since (D458–D460):** Stage A's first-pass faults form no class (`stage-a-trace/STAGE-A-TRACE-RESULT.md`); the model's accounts make
  two opening mechanisms strong leads, the unsigned Ohio guarantee folded into the programme's amount (seven draws, both systems) and the
  next year's capex folded into this year's question (five of six clean draws), and show the standard's keep-apart line for unsigned deals
  missing from the clean Step 1 request (`opening-review/D459-RESULT.md`).
- **Since (D460–D462):** the whole-request audit of clean Step 1 (two readers apart, `step1-audit/AUDIT.md`) finds the standard's identity
  boundaries missing from its request (the unsigned deal beside a plan's amount; another year of a shared quantity) and one date sentence
  narrower than the standard (F6); F6 decided only one or two of 26 memory declines (`step1-audit/f6/`) and is recorded, not tested alone.
  The status report for Alex, reviewed by the council for accuracy: `clean-arch/e2e-comparison-2026-11-13/STATUS-FOR-ALEX-2026-11-13.md`.
- **Since (D463–D464):** the identity lever is a prompt clause first; candidate c16 (version 5, four blind audits) and a case-specific
  diagnostic on fresh articles (one story per target boundary is all this window holds), 7 merge and 9 negative stories and the stored guards
  (`clean-arch/e2e-comparison-2026-11-13/identity-probe/v2/PROBE-DESIGN-v2.md`).
- **Since (D465–D466):** the identity diagnostic moved its error (c16 not adopted, c8 stays; `identity-probe/v2/RESULT.md`, $4.49); a deep
  reflection council (Alex's request) agreed the second half of the day circled and reset the plan.
- **Since (D467–D473):** the ladder-cost proofs are kept as tools (`ladder-cost/`); the ladder-refusal candidate stopped on a contested
  "main figure" boundary; the 41 Stage A reader splits recorded, none changing its verdict; the ten right-by-refusal theses traced; the period
  candidate c17 failed its frozen lines (memory and federal openings suppressed; `period-probe/RESULT.md`). Step 1 sentence changes on these
  articles stop (D473). Provisional choices under D439 (D469): empty-start measurement; the three open shapes stay concerns; the written-ladder
  line stands (D471). Alex's answer overrides any of them.
- **Since (D474–D477):** the unsigned-deal candidate c18 was not adopted (`unsigned-deals/RESULT.md`). The source check of the eleven
  first-pass refusals (`reachability/RESULT.md`): six right, four reachable only on paper, one split. **D477:** Stage A not passed; no theme or
  ladder change for the H100 boundary; no more Step 1 sentence changes on these articles; production stays the default; the clean path's
  three product choices are written for Alex (`clean-arch/e2e-comparison-2026-11-13/CHOICES-FOR-ALEX-2026-11-13.md`).
- **Since (D478–D482), under D439:** choice 2 tested and failed (c19); choice 3 taken (production stays the default); production's price
  rule (D191.4) tested and failed (`docs/research/2026-11-13-shared-quantity-price/`); no further paid test on the frozen ruler (D482).
- **Alex active again (2026-11-14).** D483–D486: a use-oriented acceptance was designed and its $0 trial read
  (`docs/research/2026-11-14-use-acceptance/TRIAL-RESULT.md`); Alex asked for a leaner path (small steps, each run fast). D487: step 1 built nothing (the
  "dated after the article" statements are correct dates against items stored a day early); step 2 runs one fresh week (2026-09-22..28, 235
  items proved identical for both systems), one draw a system, a one-day slice first, readings A and B, the decision rule written before
  reading (`LEAN-LOG.md` §2). Slice passed; production's week draw complete; the clean draw stopped twice on dropped connections, root-caused and fixed (D488: Step 1 resends a
  network loss, each attempt on the ledger). The clean week draw completed from empty (`poc/data/clean-lean-week-2026-11-14/week-r2/`, $2.52; both ledgers $4.69). **Result (D489,
  `docs/research/2026-11-14-use-acceptance/week/WEEK-RESULT.md`):** not clear by the rule written before reading; no system chosen. Production
  covers 4 of the 5 big matters two blind reader families listed, the clean path 2 (it lacks revenue and margin by D382/D384); judgement
  support does not rank them at this size. The question then put to Alex (whether the new system holds questions on the company's main
  numbers) was answered by him on 2026-11-15 (D505; see "One next task").
  Recorded spend under D439 at that point: about $18.4 of $40 (about $7.26 before the run; the run's ledger $11.43, somewhat above its cost at the
  published rates); the current figure is in "One next task". (An earlier line here gave "about $29.2" as tracked spend; no decision or
  log records that figure and it is withdrawn.)
- **Open defects recorded by this review:** the frozen judge retried 10, 16 and 18 judgements in the seeded clean draws, 38 of 51
  reasons a theme cited as a dependency (PRD 11, E4), and its stored path holds the 2026-07-05 fault above (frozen; findings for
  Alex); the same matter takes different shapes between draws (Kyber due end-2027 in one draw and end-2028 in another); under D397
  the second bet of a topic that holds two has no answer; five-state event ladders failed by hand three times before a construction now in the request
  produced ones that pass a reader; in Stage A the model's own are faulted by both reader families in 10 of 17 for the company.
- **The unseeded measurement (D395):** graded subset 4.0 against 6.33 seeded. Every miss is a question not opened in the ruler's shape.
  Judged answers 16 of 16, on the ruler's wording and ladder; the system's own questions have never met a judge.
- **Stage 2 of D392:** clean 18, 18, 17 against v108 17, 15, 16, inconclusive on q12.
- **Known gap (D394):** capital spending (q12).

No long job is running.
