# Existing-question IDs in the split POC

2026-11-05. The previous seven-day run failed at sequence 1289 because B returned three subject identifiers as question links. On all 85 saved B answers, 195 evidence records carried 208 links; three links, all at 1289, were not shown question IDs. Each was instead the subject ID displayed beside exactly one shown question: `research:1174ba36750a7b35ddb6` beside v97, `research:ab064a706a0bdd95ddfc` beside v94, and `research:a43bbd7b5828e9dfa90b` beside v95. The request said to return question IDs but its schema accepted any string. Source and answer are retained in the failed run's item directory. The symptom is an identity-contract defect; this does not establish whether the evidence is substantively relevant.

The B request's link items use an anchored pattern made from the actual IDs of the questions shown to that request. Empty links remain allowed. When no question is shown the existing unconstrained string schema remains and the writer's existing check still refuses any invented link. This does not decide which evidence matters or infer a relationship from a subject ID. The separate code check remains at the writer boundary. No frozen ruler or production extraction prompt changes.

| State or event | Result |
| --- | --- |
| Questions shown | Each nonempty link must equal a shown question ID; B decides which, or returns empty. |
| No questions shown | Existing prompt asks for empty links and the writer refuses any nonempty link. |
| Unknown/subject ID or model/schema failure | Request is refused; nothing is written for that item. |
| New item after a write | Rebuild the allowed IDs from that item's latest committed snapshot. |
| Retry or restart | The existing exact request/provider-answer check applies; changed schema prevents reuse of an old request. |

Reader contract: the B request builder sends the ID schema; model schema validation and `build_handover` both check it; A and the candidate matcher are unchanged. A saved-answer sweep must keep all 205 valid links and refuse the three bad links. A real re-send of the complete saved 1289 request with only this schema change must use shown question IDs without losing source text before the seven-day start. This is a one-request functional proof, not an extraction quality measurement. The first prototype used an enum and passed the real request; it was replaced by a dynamic pattern to avoid introducing a fixed enum-size limit as the library grows. No question list is truncated.

Verification of the enum prototype: the saved sweep judged 85 answers, 195 evidence records and 208 links; the only refusals were the three subject IDs above. The real saved request, re-sent with only the enum added, returned six evidence records with six source-backed quotes and links `[v97]`, `[v94]`, `[v10]`, `[v2]`, `[v95]`, `[v98]`; it passed both provider-schema and exact request/answer checks. This is one draw. The stored output is `poc/data/b-question-id-probe-2026-11-05/`.

The final pattern passed the same sweep (85 answers, 208 links; exactly the same three refused), and a separate real resend returned six source-backed evidence records with the same six question IDs, all accepted by the exact request/answer and schema checks. The stored output is `poc/data/b-question-id-pattern-probe-2026-11-05/`. These draws verify the ID contract on this case, not evidence quality.
