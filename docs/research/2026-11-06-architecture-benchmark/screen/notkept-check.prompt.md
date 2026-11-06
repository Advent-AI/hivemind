You are a blind independent reader. You did not write either system, the gold, or the counting code. Read-only: do not edit any file.
Read first: docs/prd/05-extraction-standard.html (version 5), §5.1 (one evidence item records one statement; that statement is what is judged), §5.3
(the not-kept list).
Input: docs/research/2026-11-06-architecture-benchmark/screen/notkept-check-packet.json. Each entry pairs an evidence record (its quote and its summary,
which says what statement the record keeps) with a gold entry the standard does not keep (excluded_matter, with its standard_row). A counting aid
matched them because the record's quote overlaps the excluded sentence.
For each entry decide: recorded = "yes" if the record keeps the excluded matter as its statement (its summary, or the quote read as the record's one
statement, states that matter); "no" if the excluded sentence only sits beside another statement in the quote while the summary records something
else; "unsure" otherwise. Give a one-sentence reason quoting the summary.
Return, as your final message, a JSON array only: [{"id": "N001", "recorded": ..., "reason": ...}], then one line of counts.
