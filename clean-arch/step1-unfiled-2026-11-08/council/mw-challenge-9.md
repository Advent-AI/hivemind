# Council mw, round 10: the clean week draw stopped twice on dropped connections; a transport fix before the relaunch

Read `docs/research/2026-11-14-use-acceptance/NETWORK-RETRY-DESIGN.md`, `clean-arch/step1/live.py` (LiveTransport), `clean-arch/step1/runner.py`
(run, lines 286-365), `src/hivemind/model.py` (openai_transport), and the two failed traces under `poc/data/clean-lean-week-2026-11-14/week/c1/`.
Production's week draw completed. Is the diagnosis right, and is the fix (network-loss retries inside the transport, each attempt on the
ledger, recorded in the trace) the right one? Name only what would make the relaunch's result wrong or the fix unsafe. End with:
"Council position: <...>".
