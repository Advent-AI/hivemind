# Step 1: source-unit ID observations

**Status: offline examination of one proposed representation; no schema or prompt has changed.** A council proposal would let the model identify supporting source units by ID and have code retrieve the original text. This could avoid model copying changes, but an ID cannot establish that the selected text supports the summary, belongs to the target article, or includes all needed context. The earlier [citation audit](STEP1-CITATION-SUPPORT-AUDIT.md) also describes a different, untested claim-to-passage mapping hypothesis; the two are not the same change.

## Existing boundary heuristic

The existing `_SENTENCE_END` in `src/hivemind/extraction.py` is used for quote repair. It is not a validated article sentence splitter. For example, on the saved Quartz article, it cuts after `U.S.` in “a handful of U.S. data centers”; a saved financial article also breaks at `Jan.` in a date. Full-page inputs include headings, tables, code and navigation, and can be one long line. Exact byte reconstruction is possible if every offset and whitespace character is retained; that alone does not make the resulting units meaningful sentences.

An independent [offline census](../poc/data/clean-step1-citation-completeness-2026-11-07/segment-census.py) applied this heuristic to all 6,463 candidate captured-page article inputs. Concatenating the units reproduced every input. The median page had 234 units, the 99th percentile 794 and the maximum 3,288; 31 pages had over 1,000. The maximum unit was 5,250 characters. These counts describe the heuristic and saved page text, not useful article content or a safe limit.

Applying the same boundaries to saved located quotations also shows a projection issue. In the [overlap check](../poc/data/clean-step1-citation-completeness-2026-11-07/segment-passage-overlap.py), 116 of 248 located passages in the 49-article forward run span at least two units. Selecting every overlapping whole unit adds some surrounding characters to 240 passages, usually boundary whitespace; one adds 276 characters, including a discussion beyond the shorter original quote. The other overlapping samples are reported separately in the linked output. Returning a larger verbatim source slice is not the same as reproducing the model's original quotation or proving the added context supports its claim.

## Request size and metadata

For the four source-control pages, a literal JSON list of `{id, text}` objects encoded with `o200k_base` required 5,401, 14,224, 2,403 and 2,253 source-only tokens, compared with 2,719, 8,593, 912 and 598 respectively for the corresponding plain JSON strings. This is a measurement of one verbose representation, not the complete model request, actual billing or a claim about a more compact notation. Numbering can therefore shift cost from output to input and needs a real request-size comparison.

Source metadata and article text are different inputs. In 49 completed forward requests, 10 titles appeared as exact strings in the text and 39 did not; this is not a semantic assessment. A text-only ID cannot automatically cite a metadata title. In a wrong-page capture the target title can be unrelated to the page text; merging their provenance would be misleading. Duplicate identical text can also appear at multiple offsets or in different page roles. IDs must be scoped to the exact sent input and preserve offsets and source type if this direction is tested.

## What remains open

Neither source-unit IDs nor claim-to-passage associations guarantee that the model selects the right material, retains every qualifier or extracts an unmentioned matter. A model can link a whole multi-claim summary to the same incomplete excerpt. A source-grounded inference or caution need not be literally stated in a quotation. Unknown IDs and missing source material must remain visible rather than becoming fabricated quotations or an added stream-stopping rule. Any isolated candidate would need a reviewed projection back to the current thesis–evidence pair shape and separate writer/reader compatibility work. No source-unit version is adopted.
