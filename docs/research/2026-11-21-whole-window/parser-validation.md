# Parser validation for the primary line (`contradictions.py`; PAID-DESIGN.md §4; $0, stored v118 draws)

Two hand-read samples of the parser's output on old-1, old-2 and old-3 (`parser-validation.txt` holds the second; the first is the
first-amount version's sample, superseded):
- **First version (first amount in the band):** 2 misparses in about 30 rows: old-2 08-26 took an H2 figure ($212B) where the answer
  ends "approximately $419B for FY2027" (a missed contradiction); old-3 09-01 took FY2026 revenue ($215.9B) where the answer ends
  "about $415 billion for FY2027" (a false contradiction).
- **Second version (the last amount followed by "FY2027", else an opening amount, else the last amount, ambiguous when several):**
  40 rows read (every definite and ambiguous date of old-1 and old-3, every ambiguous date of old-2, five random others per draw). The
  "year" and opening rules read the stated annual forecast in every row but one: old-3 08-26, where the total's answer opens "Starting
  from the $396 billion FY2027 estimate" and concludes "approximately $444 billion": the rule took the starting reference, a false
  contradiction. The ambiguous rows are mostly rung boundaries quoted after the forecast ("roughly $380 billion. That is rung 2 ($350
  billion to below $400 billion)"), correctly set apart.
- Counts with the second version, 07-01..09-20: old-1 11 definite days (4 ambiguous), old-2 56 (5), old-3 1 (4; the one is the false
  contradiction above).

**Consequence for the design:** the parser is a lead, not the count. Every distinct flagged answer pair (definite or ambiguous) in all
six sequences is read by hand against both answers and classed definite, overlap, clear or misparse; unflagged pairs are read on a
random sample per sequence for missed contradictions, all of them read if the sample finds one.
