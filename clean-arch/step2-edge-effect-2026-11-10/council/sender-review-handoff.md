You are an independent, read-only reviewer. Do not edit any file and do not send any network request.

Scope: one small paid probe about to be sent, in /Users/lchingen/hivemind (branch clean-arch).
- Protocol: clean-arch/step2-edge-effect-2026-11-10/PROTOCOL.md
- Sender and reader: clean-arch/step2-edge-effect-2026-11-10/judge_probe.py
- The offline replay that produced the two requests: clean-arch/step2-edge-effect-2026-11-10/edge_replay.py
- The count: clean-arch/step2-edge-effect-2026-11-10/inheritance_census.py
- Code they call: clean-arch/e2e-2026-11-09/adapter.py, budget.py, control_v108.py (ReferenceArchiveTransport); src/hivemind/model.py
  (build_request, openai_transport, call); src/hivemind/views/judging.py (round_of_judgements, evidence_in_view, check_answer);
  src/hivemind/views/store.py (revision_of, evidence_in_force).
- Outputs already on disk: poc/data/clean-step2-edge-effect-2026-11-10/ (control/, remove-relation/, remove-relation-keep-link/,
  inheritance-census.json). The saved run: poc/data/clean-e2e-2026-11-09/stage2-clean-d1/judged/.
- Governing rules: AGENTS.md sections 5 (verification; "a re-sent request is the bytes production sends"), 7.3 (small first, each
  send must decide something) and 9; the council conclusion reports/step2-after-failed-probe-council-2026-11-09/CONCLUSIONS.md.

Out of scope: the frozen judge's own quality, Jev's prompt, Step 1, Step 4, any redesign. Do not propose new mechanisms.

Answer these, each with the file and line you read, and say plainly "serious" or "not serious" for every finding:
1. Would `judge_probe.py send` put on the wire exactly the bytes production's `model.openai_transport` sent for the saved v20
   judgement of 2026-07-06 (control arm), and the same shape for the counterfactual? Name anything that could differ (key order,
   escaping, headers, retries, a cache answering instead of a fresh sample).
2. Is the counterfactual request really what the unchanged code builds when only the one relation is removed, or could the way
   edge_replay.py stops the round, patches Adapter.judge/article, or stamps the library copy make it differ from that?
3. Does the control replay's pass criterion actually prove the replay reproduces the saved run (name any table, column or request it
   does not compare), and is the "relation removed, link kept" arm a valid separation of link from relation?
4. Is the reading rule in PROTOCOL.md decidable from 3 answers per arm and free of a path by which the author could read either
   outcome as a success? Is any claim in "What each outcome means" wider than one case, one day supports?
5. Can the spending limit be passed, or a credential, or the saved run, be written to or damaged by this probe?
6. Is the census's count "5 of 700 links exist only because a revision relation carried them" computed correctly from the adapter's
   rule (adapter.py article()), including a link that a later revision relation would have carried had it not already existed?
End with one line: READY TO SEND, or NOT READY with the serious findings numbered.
