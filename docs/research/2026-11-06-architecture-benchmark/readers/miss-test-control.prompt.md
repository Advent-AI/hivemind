You are an independent reader for an extraction benchmark. You built neither system. Read-only: do not edit any file.

Read first: docs/prd/05-extraction-standard.html (the signed extraction standard, version 5; the frozen ruler), and AGENTS.md §7.1-§7.2 for how a
miss is read. The gold is frozen and is never corrected here; a disagreement with it is reported, not acted on (D373).

Input: docs/research/2026-11-06-architecture-benchmark/results/traces-test-control.json (golden-v5 test articles, extraction stage only: "written" means handed over), a JSON list. Each entry is one helpful gold matter (core or supporting) that the arm "control" missed in at least one of its three
draws. It holds the gold entry (span, meaning, weight, the standard's line), the source paragraph, and per draw: whether the matter was handed over
by the extraction stage and whether it was written to the ledger, the item's processing steps, every archived extraction-stage answer in full, the
full checked handover (statements, candidates, drops), and the written records. An item marked UNREAD lacks an answer it should have; say so.

For every entry and every draw in which it was missed ("written": false), put the miss down as exactly one of:
- MODEL_NOT_WRITTEN: no answer of the extraction stage states this matter (quote what the answers say instead, or that they are silent);
- DROPPED_BY_CHECK: an answer states it but a code check dropped it (quote the drop reason from the handover);
- PRESENT_OTHER_WORDS: the matter is in the handover or the written records in other words, so the counting aid missed it (quote the record);
- NOT_PROCESSED: the item was merged as a copy of another item or never extracted (quote the step);
- GOLD_QUESTION: the gold entry is not in the source as written, or reads it differently from the standard (quote the source; this is reported
  beside the score, never applied).
Return, as your final message, a JSON array only (no prose before it): [{"matter": ..., "draw": "d1", "verdict": ..., "reason": "<one sentence quoting the evidence>"}], one row per missed draw.
After the array, one line with the counts per verdict.
