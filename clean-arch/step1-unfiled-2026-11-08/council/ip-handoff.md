# Council ip: independent read of one change to a request's closing check, before it is sent again (read-only)

Context, all in `clean-arch/step4-2026-11-10/probe-2026-11-10/`: a request was sent on six stored topics; three changes were made
for three classes of fault (decision D404 in `docs/DECISIONS-log.md`); the second send fixed those classes and broke one case
that had been right. The topic u2/clean-10 names two things, neither the main one, and should be declined (D397): the first
request declined it 4 times of 4 (`answers.jsonl`, `resend-u2-clean-10.json`), the second 0 times of 4 (`answers-round2.jsonl`,
the same file). Each change alone, added to the first request, still declines it 3 of 3, 3 of 3, 2 of 3 and 3 of 3
(`isolation-clean-10.json`, `isolate_changes.py`); only together do they stop the refusal. The model's own account of a
second-round answer is `account-round2-clean-10.json`.

My reading of the mechanism: the added sentences on how to write a question, in the body and in the closing check, together
outweigh the one sentence on declining; and the closing check, where the model reads its answer back, tested only a written
question and never asked whether the topic should have one.

The one change: the closing check (`clean-arch/step4-2026-11-10/ladder/candidate-closing.txt`) now begins by asking that. Its
second and third sentences are new; compare with `probe-2026-11-10/sent-closing.txt` plus the three tests added for D404. The
system text (`ladder/candidate-system.txt`, line 6) holds the rule it repeats.

Do not edit files, run model calls or start runs. Answer in under 300 words:
1. First line: "send", or "hold" with the exact words you would use instead.
2. Does the new test repeat only a rule stated in the system text (AGENTS.md §6: a closing check repeats rules above it)? Is it
   wider or narrower than line 6 and D397?
3. Could it push the model to decline a topic it should answer: the yes/no event, the topic that asks several things with one
   main (u1/clean-2, where the main thing is judged and the others listed), a figure? Say which words, and how to guard it.
4. Is my reading of the mechanism supported by the files, or is there a better one?
