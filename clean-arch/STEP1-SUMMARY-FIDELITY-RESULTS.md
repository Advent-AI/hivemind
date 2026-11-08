# Step 1: summary-field wording diagnostic

## Result

The tested field-description clarification did **not** show the intended improvement on the selected source-qualification case. It is not adopted. Both the original and candidate descriptions returned the article-28 example model as part of the proposed system in all three answers, without retaining the source's “such as” qualification. Neither group claimed that the system had already been deployed. [Open the 36-answer comparison](../poc/data/clean-step1-summary-fidelity-2026-11-07/review.html) to see the source, open theses, every output and its cited passages.

The study used six previously inspected articles, three fresh low-setting responses per condition, the same saved prepared text and before-state, and the same system message, schema shape and other fields. The candidate changed only the `summary` schema description. All 36 calls completed. Independent readers compared each anonymous answer to its source before the condition mapping was opened; answer content may nevertheless reveal its condition. A second reader specifically rechecked the article-28 example wording before unblinding. No thesis state or production data was changed.

The tested description grew from 101 characters / 15 `o200k_base` tokens to 183 characters / 29 tokens. The change was a diagnostic of field-local wording, not an approved enlargement of the canonical prompt. The system message already asks for conditions and uncertainty to be preserved; the test does not establish that the field description caused the error.

## Selected source-backed observations

Each count is answers out of three for that article and condition. The categories overlap. The known cases and three draws are not a general accuracy estimate, a production acceptance, or proof of why the model made a choice.

| Article and observation | Original | Candidate | Interpretation |
|---|---:|---:|---|
| 28: the source's example model described as used in the proposed approach | 3/3 | 3/3 | The release says models “such as” the named model. Every answer omitted that qualification; none asserted exclusive selection or completed deployment. |
| 3: separate $15.5bn valuation given an explicit US-dollar currency | 2/3 | 2/3 | The captured article does not explicitly label that valuation's currency, although it labels the investment and fundraise amounts. The capture may be incomplete. |
| 35: promotional trading-card giveaway attached to a thesis the link itself says it does not inform | 1/3 | 1/3 | The two answers choose different unrelated theses; the other four outputs are empty. The page's relevance, not a mandatory empty output, determines the judgment. |
| 16: $1bn financing mentioned | 1/3 | 0/3 | The financing paragraph was present in all inputs. Whether it deserves a new topic or link is an analyst judgment; the difference does not establish why it was omitted. |
| 25: announced deployment and split between hardware roles retained | 3/3 | 3/3 | Relevant multi-part facts and a legitimate indirect context remained in these cases; this does not establish all cross-paragraph handling is safe. |
| 29: quote lacks nearby text identifying the H100 rental-price chart | 1/3 | 2/3 | The missing identification exists elsewhere in the supplied article. This is a citation-support issue, not an assertion that all summaries or links are wrong. |

Other independent observations include potentially over-specific memory-price labels in two candidate article-29 answers, absent reporter identity or date fields in some answers, and a candidate article-25 citation that lacks a hardware-life detail present elsewhere on the page. Some interpretations and indirect links are explicitly marked as concerns rather than definite errors in the detailed reviews.

## Implications

The candidate is a source-general clarification, but the result does not justify changing the prompt: the main repeated qualification issue remained, and meaningful information or supporting context was not consistently retained. Nor does the result prove that no different wording, representation, reasoning setting or model process could help. The source-role selection itself remains experimental; missing source capture, actor attribution, quote support and downstream storage are separate unresolved problems. The council is reviewing the outputs and prior attempts before choosing the next focused action.

The [request audit](STEP1-FIDELITY-PROMPT-AUDIT.md) maps each observed class to the whole saved request and the signed standard, explains the candidate and its risks, and records the independent request-only audit. The prompt and frozen ruler have not changed.

## Records

- [Interactive replay](../poc/data/clean-step1-summary-fidelity-2026-11-07/review.html), [articles 3 and 16 review](../poc/data/clean-step1-summary-fidelity-2026-11-07/review-03-16.md), [25 and 28 review](../poc/data/clean-step1-summary-fidelity-2026-11-07/review-25-28.md), and [29 and 35 review](../poc/data/clean-step1-summary-fidelity-2026-11-07/review-29-35.md).
- [Pre-send design](../poc/data/clean-step1-summary-fidelity-2026-11-07/design.md), [exact-request manifest](../poc/data/clean-step1-summary-fidelity-2026-11-07/manifest.json), [condition-hidden findings](../poc/data/clean-step1-summary-fidelity-2026-11-07/blind-judgments.json), [separate example-qualification recheck](../poc/data/clean-step1-summary-fidelity-2026-11-07/adjudications.json), and [condition mapping](../poc/data/clean-step1-summary-fidelity-2026-11-07/blind-key.json). Individual raw requests, responses, validation outcomes and usage remain in the experiment directory.
