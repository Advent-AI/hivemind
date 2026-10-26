# Final same-row score placement — October 26, 2026

D193 restores the score pill beside “AI score” on the same row, superseding D192. The shared title renderer restores its right-aligned pill; the extra row, plot translation and canvas height increase are removed. The pill shape and 11px text remain.

Browser verification: all 90 library cards place the pill to the right of the title, vertically aligned and at the same font size. The cached Idea and its three connected Thesis cards pass the same placement check. Home/End replay still changes the displayed scores. [Final screenshot](score-beside-final.png).

40 UI tests, lint and formatting pass. 160 Python tests pass. The final build contains 155,465 JavaScript bytes and validated 90 theses in 27.6ms in the recorded sample. All three source hashes remain unchanged; the model archive contains seven rows and the browser reuses cached responses.

Reasoning refresh in PRD order: research universe, classification, Config, dispatch, extraction, thesis library, final verdict, pull mode, human review and system overview retain their input/output contracts, examples and acceptance rules. The current UI specification and current-state paragraph now describe D193 instead of D192. No probability model, schema or formula has changed.
