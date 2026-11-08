# Step 1: reasoning setting and source fidelity

## Result

Medium reasoning improved some of these selected outputs, but it **did not fix the recurring loss of source qualifications** and introduced or retained other concerns. It is not adopted as a production setting. [Open the 36-answer replay](../poc/data/clean-step1-reasoning-fidelity-2026-11-07/review.html) to inspect the source, open theses, summaries, links and quotations.

Six previously inspected articles were sent three times at low and three times at medium reasoning. Each article used the same prepared source, saved pre-item thesis state, prompt, model, schema, metadata and output-token cap; the request changed only `reasoning_effort`. All 36 requests completed. Independent readers examined anonymous answers against the actual prepared text and captured page before the setting key was opened; output content can still reveal a condition. The article-28 example wording received an additional independent recheck before unblinding. No state advanced and no frozen production configuration changed.

## Source-backed observations

Each cell is answers out of three for the named article. These cases were selected after previous inspection; they are not an unseen sample or a general error rate. Findings overlap and three draws cannot prove the cause of a difference.

| Article and observation | Low | Medium | Interpretation |
|---|---:|---:|---|
| 28: example model stated as if used in the proposed system | 3/3 | 3/3 | The source says models **such as** Phi-4; all six quote the qualified source while describing the model more definitively in their summaries. Neither setting solved this known qualification issue. |
| 28: source's use-case condition for partial cloud replacement omitted from benefit summary | 0/3 | 3/3 | Reviewers marked this as a context concern. The answers do not necessarily claim universal replacement or realized savings. |
| 29: stock-market flows blurred into infrastructure spending in a summary or link | 3/3 | 0/3 | The source discusses investment in infrastructure **stocks**, which does not establish capital spending. Medium answers also did not retain the stock-flow statement, so the lower error count does not prove better handling of that statement. |
| 16: $1bn SambaNova funding returned | 1/3 | 2/3 | The financing paragraph was present in all six inputs. Whether and where the financing should be paired remains an analyst judgment; this small difference does not prove improved coverage. |
| 6: joint-system quotation altered | 2/3 | 0/3 | The preserved original quotation and source location were checked. Other questions about company versus CEO attribution remain in both conditions. |
| 35: unrelated trading-card giveaway linked to Shield TV while the link explanation says it does not inform that thesis | 1/3 | 0/3 | The other five answers returned no pairs; empty output was evaluated against the page, not enforced as a rule. |
| 3: separate $15.5bn valuation assigned a currency not explicit in the captured article | 1/3 | 2/3 | This is a source-qualification concern; the captured page itself appears incomplete. All six retained the reported NVIDIA investment. |

In article 29 the reviewers also flagged attribution of the journalist's custom-chip claims to the interviewee in some answers; in article 16 they noted concerns about the deployment GPU's unspecified identity and the journalist's cooling comparison. For article 28, all answers kept the collaboration and did not claim completed vehicle adoption, but some reporter and tier fields blurred the issuer, host or status of company claims. These observations must be read with their source-specific notes and are not a single numerical score.

The provider reported 89,454 input tokens for each setting across 18 answers. It reported 22,036 completion tokens for low, including 5,094 reasoning tokens, and 49,190 for medium, including 30,213 reasoning tokens. These are usage totals for this diagnostic, not a production throughput or billing estimate.

## What remains open

The model's later response to a targeted follow-up correctly recognized that “such as” did not establish model selection, but also said it could not know its earlier reasoning. That retrospective answer does not establish that adding a self-check will work: earlier source-check placement and separate review attempts had mixed results. This comparison likewise cannot prove that reasoning effort caused a particular error, or rule out a different setting, prompt, representation or process. The source-role selector remains provisional; multi-passage storage and downstream reader integration are not verified. The council is reviewing the results before choosing the next focused action.

## Records

- [Interactive comparison](../poc/data/clean-step1-reasoning-fidelity-2026-11-07/review.html) and independent reviews for [articles 3 and 6](../poc/data/clean-step1-reasoning-fidelity-2026-11-07/review-03-06.md), [16 and 28](../poc/data/clean-step1-reasoning-fidelity-2026-11-07/review-16-28.md), and [29 and 35](../poc/data/clean-step1-reasoning-fidelity-2026-11-07/review-29-35.md).
- [Design and pre-send controls](../poc/data/clean-step1-reasoning-fidelity-2026-11-07/design.md), [request manifest](../poc/data/clean-step1-reasoning-fidelity-2026-11-07/manifest.json), [condition-hidden judgments](../poc/data/clean-step1-reasoning-fidelity-2026-11-07/blind-judgments.json), [separate qualification recheck](../poc/data/clean-step1-reasoning-fidelity-2026-11-07/adjudications.json) and [setting mapping](../poc/data/clean-step1-reasoning-fidelity-2026-11-07/blind-key.json). Every request, response, validation outcome and usage record remains in the experiment folder.
