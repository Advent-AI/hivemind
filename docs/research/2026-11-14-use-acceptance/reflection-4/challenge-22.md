# Round 23: the closing design, version 2. Verify before any code.

`carried-run/CLOSING-DESIGN.md` (rewritten): (§1) the loop becomes the one owner of the store's sequence: each article gets
`store.next_sequence(conn)` when it starts, with a map `k → seq`; every place that wrote `k` as a sequence writes the mapped one
(the frozen base adapter's `article(k, …)` uses its first argument only as the sequence and is passed the mapped one); what stays
keyed by article number is listed; while no day without articles closes a question, `seq == k`, so every stored run would be
written as before. (§2) links to a closed question are **written, not judged, counted**, as production's writer and round behave
(`store.link` refuses none; `writing.py` links revisions to closed questions; the round judges open ones only); the theme row says
only what closing does (left out of later theme blocks; dependants not queued by the closing); the invariant's cases (opened
already due, days without articles, run start and end). (§7) the proof: a fixture with a later article after a closing on a day
without articles, every row exercised through `replay`, a mutant per rule (including writing under `k`), the extension proof
re-run, and the decisive replay to 2027-04-02. The production fix's parallel-resumption consequence is recorded.

Attack every cell, the sequence mapping's readers (anything keyed on `k` I have not listed?), and whether the proof would catch a
collision. End with `CONSENSUS: yes` (build and prove as designed) or `CONSENSUS: no, because …`.
