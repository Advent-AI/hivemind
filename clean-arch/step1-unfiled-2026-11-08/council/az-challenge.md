Second re-review (read-only).

1. **Link resolution.** `run_forward.step1_records` now resolves by type, as the runner does: an existing target must be among the
   theses shown open (before-state), and a new target must be in `new_thesis_ids`. Anything else is listed as '<type>:<id>' in
   `unresolved_thesis_ids`. The test now covers both collisions you named: a new link named like an open thesis that was never
   opened, and an existing link to a thesis opened only by this answer. A mutant that resolves by id against the after-state fails
   it. Replaying all six stored traces (1,605 records) gives 0 changed `thesis_ids`.
2. **Reader text.** `library.labelled_passages` labels a passage 'Unverified quote' when Step 1's verified value is None.
   `record_text` and `group_text` (member text) use it, with a test; a mutant that labels every passage 'Quote' fails it.
3. **Jev's comparison text** (`compare.piece_text`, `doc_text`, `query_text`). I propose not to change it in this commit, for these
   reasons:
   - Jev judges statement identity, and whether the quote was found verbatim does not change which statement it is;
   - changing the input changes the comparison for the 1 to 3 records per accepted run that carry an unverified passage, which is a
     change to the measured Step 2 behaviour, needing its own council and measurement rather than a cleanup.

   The mark now travels with every record, and the reader sees it. I record it as an open item. Do you accept this boundary, or is it
   a blocker?

Suites: full 285, clean-arch 92, frozen rulers 3.

Answer in under 250 words. End with READY TO COMMIT or the blocker.
