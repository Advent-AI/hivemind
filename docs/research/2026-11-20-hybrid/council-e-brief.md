# Council A, round 5 (read-only, $0)

Your round 4 is `council-d-codex.md` (DISAGREE). Fixed in `judge_probe.py`:

**1. Invalid rungs.**
- An invalid-rung answer is kept in the key's `invalid` list with its production refusals.
- `probescore()` counts it as refused and not supported. It refuses to score unless every arm × case × repeat is accounted for. It
  applies the locked rule (a), (b) and (d) against v7's re-send, and reports the plants.

**2. Queue.**
- `prodpath` now starts each day from production's own queue, `round.changed_views_of_day(conn, day)` on the copy, and reports what the
  round added and whether the judged set equals old's.
- Replay result:
  - 09-17: starts with 13, the round adds 23, 36 judged;
  - 09-18: starts with 18, the round adds 18, 36 judged;
  - both days give the same set as old's, with 72/72 requests byte-identical.

If nothing serious remains, answer `CONSENSUS: send J2a and J2b (probe and gold, 3 repeats), score coverage and refusals, read the
complete deck, then the production-path check under v7 and the passing arm`. Otherwise name what blocks. Under 150 words.
