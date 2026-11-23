You are an independent writer of answer choices for a research system. Read-only: do not edit files or run anything that writes.

Open ONLY these two files:
- `/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-6/reference-control/writers/fortnight.md`: the system text,
  the strict answer schema, and 13 topics' user messages, exactly as a model receives them;
- `/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md`: the rules your answers will be judged by.

Do not open, list or search any other file or folder: no stored answers, runs, readings or keys, in the repository or anywhere else.

For each of the 13 topics, write the one best answer the system text asks for: the question, its answer ladder and its due day, or a
refusal (no_ladder) where the system text's cases apply. Follow the system text and the user message's closing check exactly, and meet
every rule of the reader brief.

Requirements on the answer:
- It must fit the schema exactly: every required field, nothing extra, the enums as listed.
- A reference's words must be copied exactly from the item's text.
- Amounts are in full (USD, not billions); a percentage is written as 31, not 0.31.
- Ranges are five, and each starts exactly where the one below it ends.

Return your final message as exactly 13 lines, one JSON object per line, in the order the topics appear:
{"topic": "<the topic id, e.g. c1/clean-4>", "answer": <your answer object>}
No prose before or after, and no code fence.
