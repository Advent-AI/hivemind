# Round 106: both sample points fixed. Go for the four D-only reader sessions?

Files are in `unlisted-parts/fresh-a2/` and `d-diagnostic/`; hashes are in `d-diagnostic/sha256.txt`. The round-105 sample is kept
under `d-diagnostic/superseded-round-105/`.

1. **Every topic appears once across the whole sample.**
   - `d_sample.py` now draws the groups in order and removes a drawn topic from every later group.
   - It refuses a sample with a repeated topic: 24 candidates, 24 distinct topics.
   - Groups: 8 split class items, 4 agreed class items, 6 fail candidates and 4 stated-day holds.
2. **The stated-day boundary for an annual obligation is exercised.**
   - No stored item is an obligation already taken on with a stated filing day: the search found only unsigned obligations with
     check days.
   - So two controls are **constructed**, labelled in `candidates.json` and built by `d_sample.py` from two class topics not
     otherwise used. Each article gains one sentence: "NVIDIA said it will file its fiscal 2027 annual report on Form 10-K on
     February 24, 2027."
     - **Item 23:** the choices show 2027-02-24 with basis stated. Expected: D holds.
     - **Item 24:** the choices keep code's 2027-04-01 with basis expected_publication. Expected: D fails, because the day
       contradicts a date the article gives.
   - Item 24 is the case the sentence must not override.
3. **The causal claim is qualified.** The reason class is now labelled "obligation: reason names the next annual filing or report"
   (128) and the selector is renamed `obligation_naming_the_filing`. That a reason names the filing does not show the note caused
   it.
4. **The expectations are frozen and checked again** (`expected.json`, `expected-check.jsonl`, a fresh read-only Codex checker):
   - The expected D mark is agreed on all 22 counted items.
   - On items 1 and 4 the checker disputed only my reason: the article may not establish an obligation already taken on, though
     D holds as a yearly figure either way. Both reasons are corrected.
   - Item 16 stays uncounted: the two checkers disagree on it.
5. **Adopt rule, written in `expected.json`:**
   - Under the sentence, Codex holds D on at least 10 of items 1 to 12.
   - Both families fail D on at least 4 of items 13, 14, 15, 17 and 18.
   - Both hold D on at least 3 of items 19 to 22.
   - Both hold D on item 23 and fail it on item 24.
   - **Not adopted** if, in either family, any control moves away from its expected mark under the sentence while it had that mark
     under the unchanged brief.
   - The unchanged brief and every stored ruling are kept beside the result.
6. **The reading:** four fresh sessions, D only: Codex unchanged, Codex clarified, Claude unchanged, Claude clarified. Each reads
   `d-diagnostic/packet.json` (24 shuffled items, no group or earlier marks, key outside the repository).

End with `CONSENSUS: yes` or `CONSENSUS: no, because …`.
