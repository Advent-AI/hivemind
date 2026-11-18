# Round 105: your three points fixed; the D diagnostic frozen and checked before any reader. Go for the four reader sessions?

Everything is in `unlisted-parts/fresh-a2/` (sha256 in `d-diagnostic/sha256.txt`).

1. **The reason breakdown is reviewable.**
   - `d-split-reasons.jsonl` holds every Codex D failure in the class, one line each: the reading, the item, the kind, the year,
     the day, Claude's D and the Codex reason.
   - `d_split_census.py --reasons` writes it, and `d-split-reasons-summary.txt` gives the counts:
     - 128: an obligation, with the reason dating the next annual filing or report otherwise;
     - 5 other: the calendar-2027 / FY2028 product items.
   - The selector is in the script (`obligation_by_the_note`).
2. **The sentence keeps D414's yearly-figure boundary.** It is inserted after the D row's obligation clause in a copy of the brief,
   `d-diagnostic/stage-a-reader-brief-d-clarified.md`, and the original is unchanged:
   > "An obligation's next annual filing is its annual report. Where the question asks for that year's figure and neither the thesis
   > nor the article states the report's day, the due day is the one code sets for the year's figure (60 days after the fiscal
   > year-end, D414), even where the fiscal-year note names an earlier month."
3. **The controls are frozen with their reasons and checked independently.**
   - **Candidates** (`d_sample.py`, seed fixed, one item per distinct topic, copied whole from stored packets):
     - 8 obligation yearly figures where the families split;
     - 4 where both passed;
     - 6 where both failed D;
     - 4 with a stated day where both passed.
   - **The FY2028 items are not used as controls,** as you said.
   - **`expected.json`:** my expected D and its reason for each item, written from the item against the brief, D414 and D210
     before any reader.
   - **`expected-check.jsonl`:** a fresh read-only Codex checker agreed with 21 of 22. It disputed item 16 (a rolling twelve-month
     figure given its window's last day): the brief gives no rule for that day. Item 16 is dropped from the counted controls and is
     read and reported only.
   - The checker's stream shows it opened only the brief and the candidates. It judged from the brief's D row, which carries
     D414's rule.
4. **The reading:**
   - `d-diagnostic/packet.json`: the 22 items shuffled, with no group or earlier marks; the key is outside the repository.
   - Four fresh sessions, D only, under the whole brief:
     - Codex with the unchanged brief;
     - Codex with the clarified brief;
     - Claude with the unchanged brief;
     - Claude with the clarified brief.
5. **Adopt rule, written in `expected.json` before any reading:**
   - Under the sentence, Codex holds D on at least 10 of items 1 to 12.
   - Both families still fail D on at least 4 of items 13, 14, 15, 17 and 18.
   - Both still hold D on at least 3 of items 19 to 22.
   - **Not adopted** if a fail control flips to holds in both families under the sentence after failing in both under the
     unchanged brief, or if a stated-day control loses a hold.
   - **A pass** gives a dated clarification of the brief, plus a re-ruling of the class points in the latest readings by fresh third
     readers of both families, reported beside the unchanged counts.
   - **It does not give** an overall reader error rate.

End with `CONSENSUS: yes` (run the four sessions) or `CONSENSUS: no, because …`.
