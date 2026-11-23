Council read before Stage 2 of D392 sends money: the v108 control harness. Read-only, fresh reader. Repository /Users/lchingen/hivemind.

**Read:** `clean-arch/e2e-2026-11-09/control_v108.py` and `test_control_v108.py`; plan `clean-arch/step1-unfiled-2026-11-08/council/en-claude.md` ('Control harness' and 'Qualifications': the byte proof checks the request as sent, dict and key order as built, AGENTS.md §5); D392 in `docs/DECISIONS-log.md`; `src/hivemind/replay.py` (run), `src/hivemind/model.py` (build_request, call, Archive, openai_transport) and `src/hivemind/jev.py`; the reference run `poc/data/e2e-r9-frozen-v108-2026-11-03/d1` (manifest.json, manifests/, replay.log).

**Claims to check, from the author's report** (a lead, not a fact):
- `prove` replays the whole window through `hivemind.replay.run` with poc-v108 on a seeded ledger, against the 11-03 archive. 1018 of 1018 requests matched in canonical form, with no unused rows.
- Because the archive keeps only sorted keys, the bytes as sent are proved by replaying commit a907eba's `src/hivemind` (via `git archive`) over the same stored answers and comparing each request's sha256 as sent. 1018 compared, 0 differ.
- A guard checks each day's dispatched inputs (id, seq, hash, order) against the reference manifests before the day sends anything.
- `live` refuses without a passing sibling proof carrying the same code and input digests.
- `live --cap` passes the cap to replay.run.

I re-ran the four tests and `prove` on a fresh folder: 4 passed, and prove passed with the same totals as the reference replay.log.

**Answer, under 350 words:**
1. Does the proof establish what the plan requires (today's code sends production's exact bytes from the same seeded state)? What can it not establish?
2. Can `live` run anything other than poc-v108 on the seeded ledger over the window, or spend past its cap?
3. Is anything written outside its folder, or is a credential read during `prove`?
4. Is a test or mutant claim weaker than stated?

End with SEND or BLOCKER.
