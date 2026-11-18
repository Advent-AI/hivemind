You are an independent reader acting as a senior hedge-fund analyst who covers NVIDIA. This is a read-only task: do not edit any
file, do not use the network, and do not open any file other than the one named here.

Read /Users/lchingen/hivemind/poc/data/clean-step2-revision-links-2026-11-10/readers/packet-filing.json. It holds `articles` (news
articles, by id) and `cases`. Each case is one statement taken from one article (`statement.article` names it; `summary` and
`passages` give the statement) and one open research question with its possible answers and due day. The cases are mixed and
shuffled; do not guess how a case came about, and judge each on its own.

For each case, read the article around the statement, then judge: would a careful analyst file this statement as evidence under
this question?
- "evidence": it bears on the answer; a careful analyst would weigh it when choosing among the listed answers.
- "context": related enough to note beside the question, but it should not move the answer.
- "unrelated": it concerns something else (another product, another period, another matter).
Read the question as written: mind the period, the products and the population it names.

Return only a JSON array, one object per case, all 56 cases, in the packet's order:
[{"id": "F01", "verdict": "evidence" | "context" | "unrelated", "why": "one sentence that cites the article"}]
