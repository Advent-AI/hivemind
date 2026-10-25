# D162 verification

- Targeted tests: 23 passed (`test_source_first.py`, `test_ohio_sequence.py`).
- Full Python suite: 227 passed, run from a temporary working directory; see `tests-full.txt`.
- Stored-answer replay: all 18 D161 answers round-trip, retaining the same 11 candidates and 66 accepted evidence items. The previous quote refusal remains a refusal.
- Source-preservation and missing-disposition mutants fail the intended assertions (`mutant-changed_quote.txt`, `mutant-silent_omission.txt`). Artifact-audit mutant changes the selected quote on a scratch copy and fails `Selected content changed or silently omitted` (`audit-mutant.txt`). No stored original was changed.
- Final audit: 18 completed inputs; 11 raw/kept candidates; 103 raw evidence items, 102 accepted by sift; 10 memberships; 94 source writes; 17 prior member appearances. The eight-item difference after sift is the first `grouped-3` question rejected for an empty object, not a missing database write.
- Prompt/model acceptance: failed; details in `results.md`. No default promotion.

## D22 reasoning refresh, in order

Each module was reread for impact, agreement between page and PRD, examples, and acceptance/open items. No product contract or generated page block was changed in D162.

| Module | Impact and consistency conclusion |
|---|---|
| 01 Research universe | Same reference lists, identifiers and admission rules; no new object is silently admitted. The empty-object failure is reported. Examples and acceptance unchanged. |
| 02 Classification | Same three input records and upstream categories/dates. Source selection does not reclassify input. Examples and acceptance unchanged. |
| 03 Config | Both internal calls use the original category setting; both calls are archived and costed. Only the isolated manifest selects this experiment. No product settings change. |
| 04 Dispatch | Same sequence and resend behavior; a complete item precedes the next. No resume was attempted in the measured experiment. |
| 05 Extraction | D162 authorizes an isolated two-call alternative inside extraction. Final evidence remains linked to a question; no standalone product evidence store is added. The failed experiment does not replace the frozen default design. |
| 06 Views | Existing matching and atomic writing remain unchanged. Actual missing ownership, the event-period override, and wrong semantic membership are reported, not declared successful because the IDs exist. Examples and acceptance unchanged. |
| 07 Final verdict | Not exercised or changed; remains a separate future design. |
| 08 Pull | Not exercised or changed; the stream uses no new clock. |
| 09 Review pool | No new product route; experiment errors remain in its isolated records. |
| 00 System | Product boundary and glossary unchanged; grouping remains required but not enabled by default. |

Stale current-status text was replaced in CURRENT_STATE, pipeline-plan, and grouping-improvement-plan. DECISIONS records D162's failure and D163's subsequent language request. The frozen D162 plan and historical D161 results remain untouched. New report text is English under Alex's latest instruction.

The mechanical documentation check runs after this refresh; its complete output is `docs-check.txt`.
