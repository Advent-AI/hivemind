> D186 historical implementation contract. D188 extends the final assessment with the default composite plan; see [the current contract](default-composite.md).

# D186 implementation contract

A completed Idea card opens analysis on click or Enter/Space. The summary in its JSON response reads like a portfolio manager's short assessment of the idea. For example, an annual revenue outlook can inform an earnings-beat idea without proving next quarter beats expectations.

## Final design and prior decisions

D135/D145's decomposition and mapping requests remain unchanged. D184's detail drawer and D185's explicit composite trial remain. D186 adds an optional, versioned `idea_summary` setting after code validates the mapping and evaluates the claim. It receives selected theses' dated conditions and reasons, mapped coverage and the validated claim result. Its strict JSON allows only `summary`. That replaces `reading.summary`; it cannot return IDs, weights or scores. Default `poc-v26-idea` uses the same model/provider with 800 output tokens. Old configs retain two calls. The extra serial call is the stated cost of isolating the tasks; it does not meet the old whole-flow latency target by itself.

## State × event

| State/event | Transition and writes |
|---|---|
| Completed card, click / Enter / Space | Open existing analysis; no model call or ledger write |
| Pending/failed card or canvas drag | No analysis action |
| No recorded coverage | Existing null response, zero calls |
| Mapping complete, summary configured | Read chosen states at request as_of, archive final JSON, return it |
| No chosen thesis | Summarize coverage gap with an empty state list; do not invent evidence |
| Summary not configured | Original mapping summary; two-call compatibility |
| Model refusal, transport/schema failure | Existing error path; no locally invented fallback |
| English slip | Shared English retry; all calls counted |
| Exact retry / later library date / another reader | Exact-request archive hit, or new date-specific request; request-owned read connections |
| Close/reopen/new submission | Shared drawer motion and focus; new submission closes old detail |

## Value × reader

| Written value / source | Readers |
|---|---|
| Versioned idea_summary setting | Config validation, prompt resolution, model accounting and API startup |
| Dated state condition, day and reasons | Summary-only request; mapping briefs unchanged |
| Model summary string | Existing API JSON, Idea preview and first drawer section |
| Chosen IDs, claims, parts and relations | Existing readers; no write by summarizer |
| Composite trial | Existing explicit trial; omit when required representative is not connected |

## New path × existing checks

The summary uses the existing model JSON validation, request hashing, archive, English handling and cost accounting. Config refuses a summary without a mapping setting or a missing prompt. Test original request equality, unchanged selected IDs/claims/relations, exact summary forwarding, selected-only state context, historical cutoff and three-call accounting. Existing legacy configs and corpus tests remain.

## Audit and measured outcome

The old prompt requires reporting “judged” states and gives only labels. Its 16 unique candidate records do not include state conditions/dates/reasons. Two combined-prompt development arms improved phrasing but changed matches; they are not enabled. The final summary-only call preserves the original two requests and all ten selected IDs on the stored example. Three fresh controls and three isolated summaries were read; all results, limitations, tokens, latency, costs and rejected arms are in [the report](../../../poc/reports/2026-10-26-analyst-tldr/results.md).

## D22 reasoning refresh

Reviewed in order: universe (no scope/category change); classification (no input change); Config (explicit optional versioned setting, missing references refuse); dispatch (no arrival/order change); extraction (no prompt or handoff change); thesis library (reads existing state at as_of, no writes/grouping/scoring change); final verdict (untouched); pull mode (untouched, no new clock); human review (untouched); system overview (thesis/evidence/group distinction intact). Their page/PRD examples and acceptance rules still agree. The inconsistent current statements were the Idea service default, two-call-only API description and separate View analysis action; these were corrected in their owners and linked summaries. No frozen module's business rule changes.
