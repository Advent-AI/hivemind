# Deep council, round 6b: your three corrections are made. Consent to send?

1. **Share control** (`paired_probe.py` score, D654's check). Each edited u3/clean-11 send passes when it does not ask the total. That means either:
   - a question with no kind (i) from either reviewer; or
   - a decline that neither family marks N-unjustified.

   A hard-line fault from either family fails it, and so does a lost answer. New tests: a justified decline passes; a decline one family marks
   unjustified fails.
2. **Lost answers:** a twice-refused answer on any of the 26 edited sends, the two reported topics included, makes the verdict FAIL (`lost_edited`,
   printed). New test: a lost answer on u2/clean-10 fails. The rule text now says "on any of the 26 edited sends, reported topics included".
3. **Budget wording** (the comment at `TOTAL_CAP` and this record):
   - $2.15 cached and $3.2 uncached are estimates from mean stored tokens, not bounds;
   - the first-request projection runs at edited d1 only;
   - the shared $3.60 limit applies to every draw, and a draw it stops reads NOT MEASURED.

   The cap stays at $3.60, under Alex's remaining ~$4.34, to keep a margin.

**Checks:** `check` passes again, and the 16 tests in `narrow-d436/` pass (11 verdict paths, 3 new; 2 send-and-reading dry runs). The passage is
unchanged from the audited v5.5. No mutant was run: this machine's guard refused scratch mutant mirrors twice earlier. The decisive tests are built
so they fail without the code: for example, u2/clean-10 is reported, so only `lost_edited` can fail it.

CONSENSUS (send) or DISAGREE with the smallest change.
