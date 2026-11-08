# Step 1: source-passage field-order comparison

## Result

Moving the source-passage field before the summary changed the emitted field order, but **did not establish a reliable fix** for missing support, changed meaning, or missed relevant material. It is not adopted. The existing prompt, production configuration and databases remain unchanged. The [article replay](../poc/data/clean-step1-citation-first-2026-11-07/review.html) shows all 66 outputs, the text and open theses sent, citations, links and review observations.

The experiment compared the existing clean request with one change to JSON Schema property order: `source_passages` immediately precedes `summary`. There were three independent answers per condition for each of 11 previously inspected articles, 66 completed calls total. Each used the same saved article and pre-article thesis state; state was not advanced. The model returned passages before summaries in all 94 candidate evidence items, and after summaries in all 112 control items. These are output counts, not quality scores. No causal claim about internal reasoning follows from output order.

Readers assessed all six responses for each article against its source and thesis context with condition labels hidden; their article-specific findings were saved before the condition mapping was opened. Reviewers knew the selected articles and their historical issues, so the exercise was not blind to the cases. One reader assessed each response; independently checked examples below are identified by their source text and saved outputs. The [review judgments](../poc/data/clean-step1-citation-first-2026-11-07/blind-judgments.json), [condition mapping](../poc/data/clean-step1-citation-first-2026-11-07/blind-key.json), [prewritten plan](../poc/data/clean-step1-citation-first-2026-11-07/predictions.md), complete requests and raw responses are retained. There is no held-out sample, and three draws do not establish a general rate or why a change occurred.

## Source-backed observations

Each count is answers out of three for that article and condition, not evidence records. Findings overlap and must not be added. Concerns are explicitly marked; they are not confirmed errors.

| Article and observation | Existing order | Passages first | Interpretation |
|---|---:|---:|---|
| 11: $1bn financing stated in summary but opening sentence giving the amount omitted from attached passages | 3/3 | 3/3 | The amount exists in the supplied article, but the attached passages do not establish it. The ordering change did not resolve this example. |
| 34: reported Kyber delay and company denial both absent | 3/3 | 3/3 | Both are present in the supplied article; the omission persists. Whether guidance should be kept was recorded separately as a concern. |
| 28: a Phi model mentioned as an example stated as the proposed system's actual choice | 2/3 | 1/3 | A source-supported quotation can still accompany a summary that removes a qualification. One further control answer was ambiguous. |
| 29: stock-market investment described as actual infrastructure investment | 0/3 | 1/3 | The source says money is flowing into infrastructure stocks; the candidate answer describes infrastructure investment. This is a regression observed in one draw, not proof of a general effect. |
| 6: quotation substitutes “Nvidia” for the source's “The GPU giant” | 3/3 | 1/3 | The candidate has fewer of this specific changed-quote issue in this small sample; literal quote checks do not establish meaning or relevance. |
| 3: unrelated recommendation described as a Firmus builder or listing | 1/3 | 3/3 | The captured page identifies another story, but its teaser was in the supplied text. This exposes source contamination and its interpretation, not a clean test of the article alone. |
| 35: no thesis–evidence pair returned | 3/3 | 3/3 | A legitimate empty result for the selected trading-card source; it is a useful negative control. |

Additional reviewed cases: article 16 preserved planned deployment in all three candidate answers and two controls; one control was ambiguous, and relevant original-page material had already been omitted from the input. Article 25 had a questionable financing-thesis link in one answer per condition, while the announced integration had valid indirect links. Article 41 placed a forecast horizon in a statement-date field once per condition; two candidate raw quotes were repaired by validation, which is distinct from semantic correctness. Article 42 had an unverified quote from a whitespace change in one candidate answer and repeated claims in one control answer; several speaker and link judgments remain concerns. Article 29 omitted the article's easing-GPU-shortage context in two answers per condition; article 34's guidance omission is a recency-dependent concern rather than a settled error.

The model-visible source is not always the full captured article: article 16 lacks some original-page material, and article 3 contains an unrelated recommendation. Neither should be scored as if the model saw a clean complete article. Article 28's source says the Phi model is an example. Article 11's opening sentence establishes the $1bn figure; its later $11bn valuation passage alone does not.

## Implication for the next investigation

Do not switch the prompt or schema based on this comparison. The trace supports investigating source preparation, whole-article coverage, source support and faithful interpretation as separate issues; it does not show one common mechanism or prove that ordering fixes them. In particular, the earlier full-article versus Kyber-paragraph comparison changed the input in several ways and was not a production solution. Select the next investigation from the concrete source-to-output failures, preserve useful indirect links and paired thesis–evidence output, and measure both omissions and new errors. Do not introduce a hard-coded importance gate.

Independent per-article reviews: [3, 6, 11 and 16](../poc/data/clean-step1-citation-first-2026-11-07/review-03-06-11-16.md); [25, 28 and 29](../poc/data/clean-step1-citation-first-2026-11-07/review-25-28-29.md); [34, 35, 41 and 42](../poc/data/clean-step1-citation-first-2026-11-07/review-34-35-41-42.md).
