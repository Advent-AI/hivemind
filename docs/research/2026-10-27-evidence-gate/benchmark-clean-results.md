# Five-send benchmark on the cleaned text (D256), 2026-10-27 evening

The stored request of the paused run (poc-v30, T*-v12) with only its [Item] text replaced by the cleaned database text (`benchmark_clean.py`), sent five times at reasoning_effort low. Same prompt, theses, groups and schema as the stored request. A piece is the same when its quote is the same text. Whole-page baseline: `benchmark-results.md`.

| article | text chars page → clean | pieces per sample | reasoning tokens | distinct pieces | pieces in every sample | seconds |
|---|---|---|---|---|---|---|
| gnews:011203b517e045ffe773b1fb | 15,298 → 2,993 | [7, 0, 7, 0, 3] | [508, 321, 450, 236, 382] | 10 | 0 | [20.7, 7.2, 17.6, 4.8, 10.9] |
| gnews:dadd84590540a466aea01b3c | 12,574 → 5,264 | [11, 8, 11, 3, 2] | [485, 529, 361, 797, 600] | 19 | 1 | [23.3, 16.8, 19.4, 16.4, 13.3] |
| gnews:01a49ffd41f6abe24538da65 | 8,252 → 6,833 | [5, 1, 7, 7, 5] | [512, 326, 286, 338, 414] | 13 | 0 | [12.5, 8.9, 11.7, 12.0, 11.6] |

total USD 0.0102

Reading: the cleaned text did not stabilise the single call. CoreWeave returned nothing on two of five sends and seven pieces on two others; Motley 2 to 11; Rest of World 1 to 7. Pieces present in all five sends: 0, 1, 0 (whole page: 0, 0, 2). The mechanism is the task shape, not the page junk; the two-call design proceeds.
