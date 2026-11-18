# Round 24: the closing design, version 3. Verify before any code.

`carried-run/CLOSING-DESIGN.md` §1, §4 and §7 rewritten for your four points:
1. **Gaps:** each article's store sequence is `max(k, store.next_sequence(conn))`: equal to `k`, gaps included, unless a closing on
   a day without articles took that number or a later one; then it and every later article move up. Every stored run has no closing,
   so each is written exactly as before. The map is written to the run folder (`sequences.json`). A fixture with a skipped article
   and a mutant of consecutive allocation (the gap lost).
2. **Readers across the two numberings:** `stored_judgements.not_shown_of` compares the judgement's sequence with link, replacement
   and revision sequences of the **same** `views.sqlite` (`views_of` opens one store for both, lines 77 to 91): both are store
   sequences, so no crossing. `clean_ladders.article_seq` keeps the trace article number (the source article); no code reads it
   (searched). Check this claim.
3. **Request wording:** a closed question is not itself judged; a request for another may show it as a dependency marked closed,
   tested.
4. **Proof rows:** the question opened already due closes on its opening day; a revision linked to a closed question; a closed theme
   does not by itself queue its dependant.

End with `CONSENSUS: yes` (build and prove as designed) or `CONSENSUS: no, because …`.
