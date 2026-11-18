# Review round 19, confirmation only (read-only, $0)

Round 18 (`tools-review-codex-18.md`) showed that a well-formed but edited readings file could flip a verdict. The structural rule is now
in place (`git log -1`, D675's last entry):
- `score_comparison.score(mapping out, marks folder)` builds the readings with their one writer, `mark_cards.build_readings`, from the
  named inputs, and scores what it built;
- it refuses a `readings.json` that differs from what it built;
- the command line and the chain dry run use this entry;
- the deck key now also decides each card's answered flag and opening day;
- every draw keeps a card map, empty when the draw opened no question.

Check, citing file and line:
1. Through the command-line entry, can any change to a file other than the readers' own marks (rounds 0–2), the mapping output's
   readers' answers, or the frozen inputs change a verdict or a printed value? Give the change.
2. Does a writer fixture with an empty draw now reach `too small`?
3. Is any value or verdict changed for well-formed readings?

End with `READY` or `NOT READY: <the smallest changes>`. Keep it under about 200 words. Report only a case of kind 1, 2 or 3.

Do not open:
- anything under `/private/tmp`, `~/.codex/memories`, `~/.hivemind-keys` or `stage0/downloaded_files`;
- anything under `poc/data/comparison-2026-11-17/run`.
