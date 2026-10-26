# Positive-weight Idea associations — D196

The default is `poc-v32-idea` with `idea-summary-v7`. The model chooses a variable-length list and assigns positive weights totaling 100. The raw JSON has no excluded or zero-weight branch. Omitted candidates are absent from final associations, part links, bundles, related cards and score inputs. Retrieval candidates remain search trace only.

The prior v6 schema required every candidate to be represented, including zero-weight exclusions. All three measured v6 answers contained exclusions (five zero-weight entries total), while the graph still used the larger pre-assessment list. This was a response-contract and association-projection problem, not a card-style problem.

## Proof and validation

- A real-storage test supplies three candidates and returns one model-selected thesis. The API returns exactly that one chosen ID and bundle, no automatic related edges, and no orphan numeric claim. The first two discovery requests remain unchanged and archive replay retains the adopted result.
- Zero weight, invalid total, duplicate/foreign ID and invalid endpoint are rejected. An empty list has no associations or composite score. No post-hoc zero filter repairs an invalid model answer.
- A scratch mutant that retains the pre-assessment candidate list fails the exact adopted-ID test (three IDs instead of one). The normal control passes.
- The browser uses the real endpoint. Cards and calculation show the same three adopted theses at 55%, 20%, 25%, totaling 100. The current score is +0.45. Replay reaches 0.00 with the same weights; Full and Last 30 days retain the plan. The analysis has no zero-weight/excluded section.
- 165 Python tests and 44 UI tests pass; lint/format and the documentation check pass. Final JavaScript is 157,559 bytes; the recorded build validates 90 theses in 24.6ms.
- All three protected source database hashes remain unchanged. The active service uses a dated copied archive containing nine rows; earlier seven- and eight-row service archives are unchanged. Startup embeds zero new records and reuses 90 indexed theses.

[Actual response with matching bundles](live-response.json), [card screenshot](cards.png), [analysis screenshot](analysis.png).

## Fresh model samples

Three v6 controls and three v7 candidates used the same stored candidate context. All three new raw answers contain only positive weights totaling 100. No preferred allocation or thesis count was imposed.

| Sample | Data Center revenue | Compute & Networking revenue | Cloud capex | Composite |
|---|---:|---:|---:|---:|
| 1 | 55% | 20% | 25% | +0.45 |
| 2 | 60% | 20% | 20% | +0.40 |
| 3 | 60% | 15% | 25% | +0.40 |

The page uses the first completed candidate. System prompt size decreases from 1,748 to 1,221 characters; measured input tokens decrease from 2,239 to 1,899. New final-call times are 9.5, 10.7 and 9.8 seconds, versus 7.6, 7.0 and 9.5 seconds for controls. Six completed calls cost an estimated $0.003327. Together with the prior weighted experiment's $0.002993 this remains below the unchanged $0.035 allocation ceiling. Browser verification used cached answers.

## Limits and reasoning refresh

Model choices can differ on regeneration. Saved choices and weighted arithmetic remain deterministic. The curve applies today's adopted plan to past thesis states; it is not a record of earlier allocation decisions or a calibrated probability. No extraction/grouping or source-ledger behavior changed.

PRD order reviewed: universe, classification, Config, dispatch, extraction, thesis library, final verdict, pull mode, human review, system overview. Config gains an immutable Idea version; Idea association semantics change under D196. Other module contracts/examples remain unchanged. The Idea/UI specifications, current-state paragraph and default launch now agree on positive-only adoption. Historical versions and measurements remain intact.
