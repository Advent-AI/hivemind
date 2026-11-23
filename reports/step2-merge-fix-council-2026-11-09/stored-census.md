# c8 stored merge census, 2026-11-09

Read-only count of decision outcome `kind == repeat`, linked by exact record ids to `merge-key.json`, `merge-answer-MA-*`, `merge-answer-MB-*` and `merge-third-answer.json`. All 363 selected pairs were identifiable and each had two first-reader judgments; all disputes carried their third-reader verdict. This is one fresh draw and three draws over the same 115-article dev set, not 363 independent events.

| Saved run | merges | clearly wrong | overlap | accepted by both or adjudicator |
|---|---:|---:|---:|---:|
| Fresh | 57 | 1 | 2 | 54 |
| Dev draw 1 | 100 | 1 | 14 | 85 |
| Dev draw 2 | 100 | 1 | 12 | 87 |
| Dev draw 3 | 106 | 1 | 15 | 90 |

Four wrong merge instances by recorded readers comprise 3 different source-pair classes (one repeats in 2 dev draws): (1) production/20% forecast vs August customer deliveries, Jev 0.49; (2) analyst revenue-level forecasts vs growth rate forecasts, 0.53; (3) cloud providers' revenue share vs developers' sales share, 0.84 and 0.51. These have shared topic but distinct claims according to the readers; X22 was also called overlap by an independent blind Claude, so classification uncertainty remains. The developer-sales case has additional source-fidelity ambiguity: it is not proven that the media report accurately represented its source. See saved `library.json` group original and member and `decisions.json` at each run; see prior X22 council report.

## 0.5 threshold counterexample

Among the 363 merges, six selected same-statement scores are below 0.5: fresh X22 (0.49, wrong), fresh X47 (0.47, accepted by both), dev1 X33 (0.47, overlap), dev2 X27 (0.41, accepted by both), dev3 X26 (0.41, accepted by both), dev3 X28 (0.49, accepted by both). Rejecting these merges on a 0.5 floor would remove 1 of the 4 wrong instances, while splitting 4 accepted and 1 overlap instance. These are fixed archived outcomes; the statement is conditional on this isolated transformation and neither estimates behavior of a forward run nor argues any threshold is appropriate.

The overlap rows are not silently reclassified as errors. Their counts are listed, but their reader-defined acceptability and product impact need source-backed review. Exact historical log and verdicts: `clean-arch/step1-unfiled-2026-11-08/LOG.md` §§43–44 and each `poc/data/clean-{acceptance-2026-11-09/step2,step1-c8-dev-d1-2026-11-09/step2,step1-c8-dev-d2-2026-11-09/step2,step1-c8-dev-d3-2026-11-09/step2}/merge-third-answer.json`.
