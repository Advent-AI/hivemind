# Weighted Idea pipeline — D194/D195

The local default is `poc-v31-idea` with `idea-summary-v6`, the same Luna model and three-call flow. The model decides the participating theses and their impact percentages. The writer requires a complete per-ID JSON result and positive integer weights totaling 100; excluded connections carry zero. The UI displays the percentages in the Idea canvas's Thesis headers and calculates signed weighted history. The library's thesis records have no global weight.

The real cached Data Center example displays v3 60%, v1 40% and overlapping v9 0%. Its current score is `0 × 0.60 + 1 × 0.40 = +0.40`. The analysis drawer shows the model's allocation reasons and each contribution. Replay moves from 0.00 to +0.40 while keeping the same percentages. Both chart ranges work. [Cards](cards.png), [all weights](weights-overview.png), [calculation detail](analysis.png), [actual JSON](live-response.json).

## Checks

- 43 UI tests, lint and format pass. 163 Python tests pass.
- A real-storage test proves that the first two requests stay identical, returned weights survive archive replay, and no fourth call is added. The new configuration retains all five model-selected drivers in a separate case; legacy configurations keep their historical display cap.
- Invalid sums, range/type errors, positive excluded weights, unknown/missing IDs and empty reasons are refused. No normalization repairs the model's answer.
- Stored-input arithmetic proves 70/30 produces +0.30 rather than the former +0.50; the live 60/40 produces +0.40. A missing weighted state gives no composite rather than reallocating its weight. Negative direction and future-date cases pass.
- Three scratch mutants are caught: removed backend total validation, equal averaging in place of weights, and scoring with missing weighted states.
- Repository preflight: 754 extraction answers; 1,952 candidates/evidence judged, with the existing 451 refusals; 250 matching records with zero refusals; 159 prompt enum checks with zero missing values. Seven stored Idea schemas and the existing endpoint plan were separately replayed successfully.
- All three protected source database hashes are unchanged. The old service archive stays at seven rows. The local service uses a dated copy with one additional weighted answer, eight rows total; the index starts with zero embeddings and 90 unchanged records.

## Live model samples

The same Data Center context ran three fresh old-prompt controls and three weighted candidates. Every weighted answer has valid identities, directions and a 100% total. Percentages are discretionary and differ across fresh model responses, as Alex explicitly allowed in D195; no preferred allocation or fixed thesis count is imposed.

| Candidate | Data Center revenue | Cloud capex | Overlapping segment revenue | Composite |
|---|---:|---:|---:|---:|
| 1 | 60% | 40% | 0% | +0.40 |
| 2 | 0% | 100% | 0% | +1.00 |
| 3 | 100% | 0% | 0% | 0.00 |

The page uses the first completed weighted answer, not a retrospectively selected best sample. All raw answers are preserved. This is contract and calculation validation, not a claim of forecast calibration or stable allocations across regeneration.

System prompt length decreases from 1,760 to 1,748 characters. Measured request input tokens are 2,160 for controls and 2,231 for weighted candidates because the schema gains weight fields. Final-call latencies are 6.5/6.9/6.6s for controls and 9.8/9.4/12.9s for candidates; medians 6.6s and 9.8s. Six completed calls cost $0.002993 at repository list-rate estimates. One TLS handshake failed before HTTP transmission; the unissued sixth sample was recovered once without repeating the five completed answers. No spending ceiling changed.

## Scope and refresh

Weights are specific to the returned Idea plan. The chart replays that plan over old thesis states; it does not claim those weights were chosen on each historical date. Model allocations can vary on a fresh generation; a saved exact response and its arithmetic are deterministic. Missing required states remain unavailable. The score scale stays −2 to +2.

Reasoning refresh in PRD order: universe and classification inputs are unchanged; Config gains an immutable Idea version; dispatch, extraction and library writes are unchanged; final verdict, pull mode and human review are unchanged. The system's composite definition still applies. Current Idea/UI specifications, the default launch and current state now describe explicit impact percentages instead of equal weighting. Historical configurations and reports remain intact.
