# Council round 39, challenge: your findings taken (read-only)

I took every item of your round-39 answer: preflight now checks a judge row's saved format before the malformed-row skip (T5 has the
malformed row with no format; a new mutant restoring the old order is caught; 12 of 12 mutants); RESULT.md records run 2's summary
print failing after its passing results were saved and the current print exiting 0 on them, the two `v14`-as-evidence refusals, the
7 + 1 tests, token estimates (o200k_base on the format JSON over 5,415 requests: v7 315; v12 median 502, p99 1,542, max 2,621), and
`docs/check.py` OK; the suite is 388 passed after the fix. One more disclosed slip: a mistaken `t1_replay.py --help` started a stray
replay into `./--help`; it was stopped, the folder moved to the session scratchpad, and the script now refuses an option as its folder.
D714 recorded. Read `scripts/preflight.py` part A, `tests/test_citation_lists.py`, `mutants.log`, `RESULT.md` and D714 in
`docs/DECISIONS-log.md`. Answer ACCEPT or the blocking items only.
