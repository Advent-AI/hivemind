You are an independent, read-only reviewer, new to this work. Do not edit any file and do not send any network request.

Scope: a second small paid probe (6 requests to the frozen judge, about 2 cents) in /Users/lchingen/hivemind, branch clean-arch.
Its sender, clean-arch/step2-edge-effect-2026-11-10/judge_probe.py, was reviewed in four rounds earlier today
(clean-arch/step2-edge-effect-2026-11-10/PROTOCOL.md, "Reviews before the send"; the reviews are in that folder's council/) and sent
once. Since then two things changed, and only these are under review:
1. judge_probe.py: the judgement it sends is now set by `--case DRAW QUESTION DAY SEQ EVIDENCE` (`use_case`), and the output may
   lie under a second data folder (`OUTPUT_ROOTS`).
2. clean-arch/step2-edge-effect-2026-11-10/edge_replay.py: `use_draw`, `clean_thesis_judged`, the `uncarried` argument of
   `run_replay` (hooks on `store.revise` and `store.views_linked_to`), `--draw` and `--uncarry` on the command line, and the control
   report now naming its saved run.
The protocol of this send: clean-arch/step2-revision-links-2026-11-10/PROBE-v22.md. Its inputs on disk:
poc/data/clean-step2-revision-links-2026-11-10/control-d3/ and uncarry-d3-70e4-v22/.

You may run, they send nothing:
  python3 clean-arch/step2-edge-effect-2026-11-10/judge_probe.py check /Users/lchingen/hivemind/poc/data/clean-step2-revision-links-2026-11-10/uncarry-d3-70e4-v22 --case 3 v22 2026-07-06 76 e176
  git diff --no-index is not available for these untracked files; read them.

Mark every finding "serious" (it could make the send differ from the protocol, send the wrong judgement, lose an answer, spend past
the cap, damage saved data, or let a verdict be printed that the protocol's rule does not give) or "not serious", with file and line:
A. Does `--case` reach every place the old constants were used (the saved judgement looked up, the block removed, the ledger the
   frozen check reads, the registration), so that the v22 case is sent and read as the protocol says? Could a stale constant of the
   first case (v20, e185, draw 1) survive anywhere?
B. Is the counterfactual request in uncarry-d3-70e4-v22/ what the unchanged adapter builds with only that one link not written? Can
   the hooks in `run_replay` change anything else (another record's links, the order of links, a relation row)?
C. Any sentence of PROBE-v22.md that claims more than the files show?
End with one line: READY TO SEND, or NOT READY with the serious findings numbered.
