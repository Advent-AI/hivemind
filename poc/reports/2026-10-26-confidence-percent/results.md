# Idea confidence percentage — D197

The Idea card now displays AI confidence on a 0–100% scale. `confidence = 50 + 25 × aggregate` maps −2 / −1 / 0 / +1 / +2 to 0 / 25 / 50 / 75 / 100%. The existing model-selected weights and thesis scores remain the inputs. This is the defined confidence index, not a fitted outcome-probability model.

The actual cached three-thesis response gives 61.25%, displayed as 61% on the compact card. The chart uses percentage ticks and the same conversion for every history point; missing history remains unavailable. Analysis shows effects in percentage points from 50%. Individual Thesis scores retain their original scale.

Verification: 46 UI tests, lint/format, and 165 product Python tests pass. The live browser shows 61%, 0–100% chart ticks and 61.25% in analysis; Home replay reached 50%, End returned to 61%. The raw-score mutation fails the conversion assertion. No model call or source-database change. All three baseline source hashes match, and the active model archive remains at nine rows.

[Analysis screenshot](analysis.png). D198/D199's subsequent presentation changes and final build measurements are in [the final UI report](../2026-10-26-weight-order/results.md).

Reasoning refresh: research universe, classification, Config, dispatch, extraction, library, final verdict, pull mode and human review retain their contracts and examples. The system glossary, Idea specification and UI specification now agree on confidence display. No backend state or score calculation changed.
