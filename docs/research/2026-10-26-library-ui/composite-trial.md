> Historical D185 trial. D188 makes this a default response capability; see [the current contract](default-composite.md).

# D185: Idea composite-history UI trial

Alex approved calculating the proposed composite and adding a thesis-style line chart to the Idea card to inspect the UI. This is a bounded trial of the current NVIDIA query, not activation of an automatic scorer for arbitrary ideas.

The existing response holds 10 chosen theses but no contribution directions or nonoverlapping representative selection. Therefore those semantics are explicit trial data, not inferred by frontend text matching. A dated optional build input selects two reviewed representatives already connected: v2 total revenue and v1 current-year top-five capex. Both direction +1; equal weight. Segment/product revenue and other capex/financing estimates are not counted separately. The input carries exact question text and as-of, so a local ID from another snapshot cannot silently select a different question. No model call or backend schema change.

Each point averages the available representatives' displayed scores times the supplied direction. Yes/No, when explicitly configured, map to +2/-2. No assessment is missing, never zero. Coverage accompanies each point. Use the last judgement at or before that day; never read later states. The current basket is applied retrospectively and labelled as a trial in the UI; this is not historical evidence that the Idea existed or was judged then. The current example calculates 0 through July 28, +0.5 on July 29, then 0 on August 10. Its lack of a quarterly consensus benchmark remains visible in analysis.

| State / event | Behaviour |
|---|---|
| No matching trial input | Existing Idea card, no invented composite |
| Exact query/as-of match | Validate the closed trial shape, unique connected IDs, directions and question identities; compute from stored histories |
| No available assessments | Null score and no chart point; coverage 0/N |
| Partial coverage | Average only available scores, report N/M |
| Replay / range change | Read composite at replay day; reuse thesis chart styling; preserve the earlier data cutoff |
| New request / error / new snapshot | Reset the response's trial; no cross-query or cross-snapshot ID merge |
| Open analysis | Show formula, representatives, directions, values, equal weights, exclusions and limitations |

| Value | Writer | Reader |
|---|---|---|
| Trial identity, drivers, signs and reasons | Optional dated JSON build input | Closed JS validator; rejected unless the question is actually connected |
| Numeric score/history | Pure composite calculator over canonical dataset | Idea card chart/header and analysis contribution table |
| Replay date/range | Existing canvas | Leading-card callback; neither recalculates model output nor mutates storage |

| New path | Existing checks retained / new proof |
|---|---|
| Optional build input | Defaults empty, safe JSON escaping; standard build remains supported |
| Composite calculator | Real-data July 29/August 10 values, direction inversion, missing/partial data, repeated IDs, identity mismatch, unrelated query, extra uncounted cards |
| Fractional chart | Shared axes/grid/step styling; no future points, no zero for missing, margin for latest dot |
| UI trial | Same card size, no footer; line instead of evidence subplot; full calculation in analysis |

D130 owns components; D138 owns chosen links; D184 owns returned analysis. D185 permits a manually specified read-only trial without changing those contracts. Future automatic direction/representative selection and persistent Idea-history versions remain separate work.
