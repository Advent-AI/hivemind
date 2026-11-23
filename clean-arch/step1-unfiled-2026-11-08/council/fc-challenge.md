Your blocker (fb-codex.md) was checked against the code and fixed. Re-read the changed files and confirm or name what is still wrong
(under 300 words). Read-only.

1. **Revisions.** You were right (library.py:72-74 stores `{'group': revised, 'by': record}` on the revising group). The adapter now
   writes, when the `by` record is written, one revisions row from the revised group's original to the `by` record's evidence, and
   inherits the old piece's links. Several revisions are several rows, and the judge shows the latest (store.revision_of), as production
   does. A new test checks all 11 stored revisions; a scratch mutant with the direction swapped fails it.
2. **Order and verified passages.** Records now come from run_forward.step1_records in Step 1 order, with verified passages; the stored
   library lacks them. The adapter refuses a library whose records differ from the trace's.
3. **Request check.** It is now an ordered list compare against the selection recorded at prompt build. Docstring argument: the prompt
   is built by frozen code from a database already checked to hold nothing past the seq (views, evidence, sources, links, same_claims,
   revisions), so text and nested content follow.
4. **q23.** This follows plan v4 (en-claude.md:40-41, 149). `adapter.py candidates` lists clean-opened theses matching the scorer's own
   rule. A reader who did not write the code confirms equivalence to q23's question before `--q23` is passed. The view gets a yes/no
   ladder from its opening article.
5. **Bounds.**
   - Judging is capped at $3 per draw, priced from tokens; a mutant ignoring the cap fails a test.
   - A live replay writes only under poc/data/clean-e2e-2026-11-09.
   - Step 1 limits are scaled to 243 items at at-or-above published rates.
   - `run_clean_draw.sh` pins the Step 1 invocation with no candidate files, checks the PRD request is c8 (test_runner.py) and checks
     the frozen hashes.
   - Step 2 (embeddings plus Jev) has no cap: priced at the stored dev run's scale, it is under $0.10 per draw.

**Files:** clean-arch/e2e-2026-11-09/adapter.py, test_adapter.py, run_clean_draw.sh, stage2-frozen.md and stage2-limits.json.

End with SEND (clean arm, pending the control harness) or BLOCKER.
