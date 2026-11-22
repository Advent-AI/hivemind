# A sharpened link question, version 2 (D703; for council review before its cents probe)

Alex chose to probe a sharpened wording before the paid run (D703): keep Data Center reads total revenue and the 38 negatives, remove
unsupported links including the base effect, no blanket ban on a whole reading its part. The probe is harness-only: `window_test.py
probe-v2` replaces the READS and SIGN criteria texts in memory for its pass; no product file changes until a version is chosen.

## 1. Prompt audit (the census's failure classes against the request sentences; AGENTS §6)

| Failure class (census, `CENSUS-RESULT.md`) | The request sentence that produced it | The standard or decision on the case | Verdict |
|---|---|---|---|
| Part against whole, direction unsettled: v9–v14 at margins 0.03–0.09; v21–v9 flips between draws; whole-to-part and part-to-whole both occur | READS `candidate_reads_thesis`: "a part read against its whole (...), or a quantity read against another it depends on (...)": the second clause lets a whole "depend on" its part; no sentence says which reads when both fit | D537: the total carried the year's consensus and guidance that the segment's requests lacked; D260: a judgement is made against what the market expects (consensus, guidance, the stated plan) | **abstract** (two clauses, both directions, no tie-break) |
| Across periods with an unsupported sign: v17 (FY2028 growth) reads v16 (FY2027 CPU), together, 3 of 3; v35 (FY2028 total) reads v9 (FY2027 Data Center), 1 of 3 | no READS sentence on periods (`neither` covers only "the same quantity for the same period and scope"); every SIGN example is within one period | the arithmetic of a growth rate (a higher base lowers next year's growth at a given level); the dependency design §2: another period of the same quantity "may be linked" | **missing** |

## 2. The wording (changes marked; every example from another industry, none names the covered company)

READS, `candidate_reads_thesis`, appended sentence:
> When either question could be judged with the other in view, the one whose answer the supplied text anchors less (no guidance,
> consensus or reported figure for the quantity and full period the question asks about) is the one judged with the other's conclusion
> in view.

READS, `neither`, appended clause (before "sharing a company ..."):
> or quantities of different periods when the supplied text does not state how one period's answer moves the other's (a retailer's
> sales this year and its sales growth next year, when the text only names both)

SIGN, `opposite`, added example:
> ...; one year's sales and the next year's sales growth at a given next-year level, since a higher base lowers the growth

`thesis_reads_candidate` ("for the same reasons with the roles swapped") and the instructions are unchanged, so the tie-break applies
both ways: a part with guidance and a whole without would have the whole read the part. No direction is banned.

Sources (round 18 made the distinction explicit): the general tie-break and the periods clause are proposals this probe is authorized
to test by D703, not rules already decided; D537 decided only the concrete case (Data Center revenue reading total revenue, the total
carrying the year's consensus), and D260 explains why guidance and consensus anchor a judgement (it governs judging, not linking). The
base-effect example is the arithmetic of a growth rate with the next-year level held fixed. The periods clause narrows the dependency
design §2 ("another period of the same quantity may be linked") to "when the supplied text states how": a link across periods still
exists when the text gives the bridge (v35 reads v14: the FY2028 outlook translates growth into a level through the FY2027 base).
Round 18 read the seq-148 request (dry archive, call 8744): the total carries Bloomberg's $393B FY2027 estimate, Data Center a Q1
figure of $75.25B (92% of the quarter): a full-year anchor against a partial-year one, so the tie-break gives v9 reads v14. Growth: 595
characters across the three criteria texts (READS `candidate_reads_thesis` +269, `neither` +209, SIGN `opposite` +117; the READS
criteria repeat in every pair of a job, about 120 tokens a pair); written reason: the audit shows a missing case and an abstract clause, and nothing in the current texts
duplicates them to cut.

## 3. What the probe decides (registered before its answers: `expected-links-v2.json`)

The census's registration (R 1, W 38, O 66) with, for version 2 only (`expected-links-v2.json`): **W** for any link across periods
whose shown text gives no bridge, the two unsupported links council R named (321:v16, v17 FY2028 growth against v16 FY2027 CPU; 1238:v9,
v35 FY2028 total against v9 FY2027 Data Center; round 18 showed the gate passing without this); **F**, the base-effect sign, a growth
rate reading an earlier period's revenue amount with the sign together (321:v8, 321:v9, 321:v14). Version 2: R 1, W 40, O 61, F 3;
1238:v14 stays O and is reported. Gate: the known positive right in 3 of 3 draws, no W link, no F link. $0 checks on the stored census
answers (`scorer-checks.log`): as stored, FAIL on 321:v16 and 1238:v9; with 321:v16 made "neither" and 1238:v9 kept, FAIL; with both
made "neither", PASS; 321:v16 linked with the sign opposite, FAIL; 321:v14 linked together, FAIL. Reported beside: every O pair
against the census, and the margins.
- **Pass:** version 2 becomes the candidate for the paid design (a product version built and reviewed first).
- **Fail on the known positive or a W link:** the current wording stays the candidate with its measured risks (D702).
- **Fail on F only:** the base-effect sentence did not take; reported, the current wording's risk stands.
- **A ceiling stop before draw 3 completes:** an incomplete probe, no verdict (round 18: the observed job shapes price at about $0.034
  for three draws; the all-SIGN stress shape at 0.37 tokens a byte at about $0.074 against $0.0734 left).

## 4. The probe

`window_test.py probe-v2 <scratch> <draw> <ledger> 0.10`: the census pass with the version-2 texts patched into `links.READS` and
`links.SIGN` for the pass; every link job is new (the July answers do not match the new texts), so the seq-148 jobs are bought. Three
draws on D700's ledger (spent $0.0266, $0.0734 left); priced as the census (a draw settles about $0.009 at the ledger's rule; the READS
requests grow by about 120 tokens a pair). The completeness check, equality with old-2 and the paid-transport record apply as in the
census; `draw.json` records the wording.

## 5. The product version (D705: version 2 as a separately versioned, reviewed configuration)

- **Config:** the matching setting gains `link_questions` (`config.Setting.link_questions`; allowed `links-v1`, `links-v2`), accepted
  only with the engine `jev-links` (any other engine naming it is refused) and defaulting to `links-v1` there, so `poc-v119.json` is
  unchanged in bytes, checksum and requests. `poc/config/poc-v120.json` = poc-v119 with `"link_questions": "links-v2"`.
- **Code:** `links.py` holds both question sets as literal texts (`READS`, `SIGN` for links-v1; `READS_V2`, `SIGN_V2` for links-v2,
  byte-equal to the probe's `window_test.wording_v2()`); `reads_question` and `sign_question` take the version; `choose`, `_signed` and
  `_corrected` pass `cfg.matching.link_questions`. Nothing else reads the field.
- **Entry points:** unchanged: the ordinary launchers refuse the engine `jev-links` under any question version (D694 §0); poc-v120 runs
  only in the measurement harness.

| Table | Rows |
|---|---|
| Value × reader | `Setting.link_questions`: read by `links.choose`, `_signed`, `_corrected` (searched); indirectly by `parallel_day.environment_key`, which serializes the whole configuration, so a manifest written before the field existed no longer matches and the parallel day refuses it (its existing guard; round 21); `model.build_request` and every other step ignore it. The two text sets: read by the two builders only. Config rule (round 21): named only in matching under `jev-links`, as one of the exact strings; a null or another section is refused; unnamed under `jev-links`, `links-v1`. The harness's `probe-v2` entry points are retired (the builders read `QUESTION_SETS`, so the old patch no longer changes a request). |
| New path × old checks | poc-v119's link requests byte-equal (the v1 pin `LINK_QUESTIONS_SHA` unchanged; `poc-v119.json` untouched); the v2 texts pinned (`LINK_QUESTIONS_V2_SHA`) and equal to the probe's; poc-v120 over the whole window with the probe's own answers replayed by request hash meets every link job of the probe (READS and SIGN) and ends equal to old-2 (`window_test.py v120-replay`); config refuses an unknown question version and the field on another engine. |
| State × event | a run keeps one configuration (as for v118/v119, DESIGN.md §0); a store written under poc-v120 and opened under poc-v119 or poc-v118 is read the same (the written rows do not carry the question version; the selection record carries the config checksum); a configuration changed between days is the defined outcome of D694 §0, not a supported mode. |
| Prior decisions | D359 (a configuration naming a version the code does not build is refused), D694 §0 (entry points), D695, D703, D705. |
