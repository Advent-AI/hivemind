# Step 1 evidence-reading order: comparison results

**Result: do not adopt this candidate as a fix.** On one selected article the candidate returned the reported Kyber delay and company denial once, while all three same-day controls omitted both. The other two candidate answers also omitted them, and the one that returned them stored the report, company denial and reporter's 2027 expectation under one NVIDIA party/tier. On another article two candidate answers linked a planned cloud-gaming server to an AI-infrastructure-spending question without a source-supported connection; neither control did. Other fidelity problems remained in both arms. These are three-draw observations on known articles, not general rates or proof of cause.

## What was tested

The candidate moved the existing evidence-reading definition and four bullets before the thesis-opening examples, changing no other prompt wording, input article, open-thesis state, schema, model or setting. Both system prompts measured 13,427 characters and 2,697 `o200k_base` tokens locally. The assembled complete requests were also counted, and their token counts matched for each pair; these are local counts, not provider measurements. The placement does not prove the model separately identifies facts before deciding which thesis they inform.

Nine selected, previously examined articles were sent three times per arm in mixed order: 54/54 responses completed. Each article used its recorded pre-item thesis state; the comparison did not advance the state or write a production ledger. The exact input request, response and validation observations for each call are preserved. This is an exploratory diagnostic, not an end-to-end production acceptance or an independent unseen sample.

Before comparison, nine saved requests and answers were verified against their originating traces and current clean checks. Historical preflight judged 243 extraction answers and reported its previously observed 12 quote/merge losses in 726 handover items; it does not exercise the clean path. Independent readers reviewed the complete source and pre-state without inspecting this comparison's answers, and then inspected all 54 anonymized answers against their source and open theses. Their findings were recorded before the arm key was opened. The frozen ruler and gold were unchanged.

## Source-backed outcomes

| Source | Same-day control | Candidate | What it means |
|---|---|---|---|
| Article 34: reported possible Kyber delay and company denial | Returned in 0/3 answers | Returned in 1/3 answers | The recovered answer links to the existing Kyber thesis, but mixes the third-party report, company denial and journalist's 2027 expectation into one party-statement record. This is a partial selected-case observation, not reliable recovery or proof that prompt placement caused it. |
| Article 34: Q2 revenue and margin guidance | Returned in 2/3 answers | Returned in 1/3 answers | The source includes a no-China-compute assumption; returned guidance must preserve that condition. A Kyber gain did not mean the other relevant matter was also consistently retained. |
| Article 27: Toronto GeForce NOW cloud-gaming server | No control linked it to the existing AI-spending thesis | 2/3 answers linked it to the AI-spending thesis | The source describes a gaming-service expansion and does not establish an AI-spending connection. One candidate explanation expressly admits the source offers no evidence relevant to growth. |
| Article 10: Kyber report and company response | All 3 returned the facts and proposed a distinct roadmap thesis | All 3 returned the facts; 2/3 did not propose a distinct roadmap thesis | The library contained no existing Kyber question. Whether to open a separate topic requires judgment, but these two answers filed the material only to broader questions. |
| Article 14: Hygon and Cambricon product evaluations | Named evaluations omitted in 3/3 | Omitted in 2/3 | The source says the products were being evaluated, not adopted. Naming Hygon as an expected beneficiary is not the same signal as recording both product evaluations. |
| Article 8: vendor benchmark versus IBM preview | 3/3 included self-benchmark details and retained the IBM integration/preview | 3/3 included self-benchmark details and retained the IBM integration/preview | Neither arm consistently followed the standard's vendor-benchmark exclusion. Preview availability is not customer adoption. One candidate passage was not located verbatim because it omitted a word. |
| Article 36: management's roughly $1tn revenue visibility | Returned in 3/3 | Returned in 3/3 | All identify management's stated visibility, not booked revenue. One candidate links a Marvell mention to a specific inference-chip-partnership thesis without a source-established connection. |

The blind readers found other uncertainty and errors in individual outputs, including date attribution, an exact revenue threshold made into an exact value, and citations missing adjacent context. Full findings and labels are in the three independent reviews linked below. A reported issue is not automatically a general error rate; some relevance and opening judgments are explicitly unresolved.

## Why exact citations are not enough

In article 41, a control answer's `e6` says Lightmatter executive Roy Kim predicted high-volume optical scale-up in 2028. Its cited passage actually attributes that prediction to Ayar Labs executive Vishal Chandrasekar, and the same evidence record's `original_party` identifies Chandrasekar. The citation is located exactly; the standalone summary names the wrong person. The candidate also misattributes a separate reporter-described 72-to-576 processor plan to an executive in one answer. Both show that a located source passage and a valid schema cannot establish that the summary preserves who said what.

Across this selected comparison, all 54 returned responses passed schema and clean runner handling. One candidate quotation remained explicitly unverified; no unresolved thesis references were recorded. The 27 controls returned 111 evidence items and 22 new-thesis proposals; the 27 candidates returned 106 evidence items and 15 new-thesis proposals. These are descriptive output counts, not quality scores, and no item was written to the production evidence database.

## Conclusion and next investigation

The ordering change is not established as a fix and is not inserted into the active clean prompt. It partly recovers one known missed case while introducing unsupported gaming-to-AI links and failing to retain a potentially distinct product-roadmap topic in other answers. The raw output continues to omit or misstate important source information in both arms. The model's internal reason for those decisions remains unknown; these results do not identify prompt ordering as the mechanism.

The next useful investigation is to trace **source meaning and speaker preservation** on the actual records before proposing another prompt change: compare the complete source, cited passages, standalone summary, speaker/date/tier fields and linked question, including the article 41 wrong-speaker example and the article 34 mixed report and denial. Assess their frequency on stored data and what the existing writer and reader actually preserve. A further change must address the observed class rather than a one-example rule; no new source-identity or importance gate is adopted by this result.

## Review materials

- [Interactive article-by-article comparison](../poc/data/clean-step1-coverage-order-2026-11-06/review.html) shows each source, before-state, six outputs, links and passages.
- [Source-only diagnostic map](../poc/data/clean-step1-coverage-order-2026-11-06/SOURCE-REVIEW.md) and blind reviews for [articles 4, 8, 27](../poc/data/clean-step1-coverage-order-2026-11-06/review-04-08-27.md), [10, 14, 41](../poc/data/clean-step1-coverage-order-2026-11-06/review-10-14-41.md), and [12, 34, 36](../poc/data/clean-step1-coverage-order-2026-11-06/review-34-36-12.md) retain each reader's reasoning and uncertainty.
- [Prompt audit and exact experiment](../poc/data/clean-step1-coverage-order-2026-11-06/AUDIT.md) records the independent prompt review, candidate diff, preflight and fixed comparison design. The prompt diff, predictions, frozen schedule, individual raw responses and blind key are retained in that directory.
