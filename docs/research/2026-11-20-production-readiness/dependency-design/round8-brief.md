# Council R, round 8: version 5

Your round 7 (`codex-r7.md`, two blockers) is answered: (1) each harness ledger is marked harness-only and both ordinary writers
refuse it under any configuration before routing (DESIGN §0, test 7); (2) the harness runs `replay.run` with a serial item runner as its
`day_runner`, binding an item-scope transport to each item's own sequence (link questions pass only at seq 148, linked arm) and
inspecting the committed links after seq 148 returns, before the next item or the day's judging; judging gets its own scope
(TEST-PLAN, "The sequences", the allow-list, the out-of-pair stop, dry-run step 3). Nonblocking items taken (DESIGN §1 step 6, §6,
§11).

Check against `replay.py` (the `day_runner` seam), `round.run`, `jev.ask`, `scripts/replay.py` and `budget_replay.py`. End with READY
TO BUILD, or NOT READY with the exact changes; list nonblocking items separately.
