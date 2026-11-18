# Blind reader, task S: did three runs make the same questions of the same news? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/reflection-3/july-topics-packet.json`.
Open no other file: keys and other readers' answers exist and you must not see them. Do not edit files or run model calls.

A research system read the same fourteen days of news about one company (NVIDIA) three times, independently (runs X, Y, Z),
each time starting with no questions. The packet holds the 40 topics the three runs opened. Each item: `run`; `topic` (the
topic as first written: `description`, `outcome`, `period`, `opens_as`, `settled_by`); `opening_article` (date, title); and
`attempts`: three independent attempts to turn the topic into one judged question, each either the `question` with `whose`
(the company's ticker or a theme id), its `due_day` and its `answer_choices`, or `declined` with the reason.

**1. Group the topics by matter**: the same underlying thing in the news (for example one deal, one product's launch, one
price, one regulator's proceeding), whichever run opened it and however it is worded.

**2. For every matter that two or three runs opened**, compare the judged questions across runs (use each topic's first
attempt; say so where a topic's own attempts disagree with each other). Verdict, one of:
- `same`: the same thing is measured or asked, for the same period or by the same deadline, so one real-world outcome gives
  the same answer in each run (differences of wording or of a few range edges do not count);
- `one_apart`: two runs the same, one different;
- `different`: the runs ask different things, or some run has no judged question (declined in at least two of its three
  attempts).
For `one_apart` and `different`, say **what differs**, from this closed list (several allowed): `what_is_measured`,
`period_or_deadline`, `whose_question` (company or which theme), `several_parts` (one topic asks two things), `no_question`
(declined), `answer_choices` (the ranges are far apart). And say in one sentence whether the difference could change the
answer a reader gets.

**3. For every topic**: `answerable` (yes, no, unsure: as written in its first attempt, can public material settle it on its
due day?) and `worth_tracking` (yes, no, unsure: would an analyst covering this company hold a view on it, because it can
change the company's revenue, profit, cash or credit risk?), each with a reason of at most 15 words.

Return, as your final message and nothing else, JSON lines:
- one line per matter: `{"matter": "<short name>", "topics": ["t..", ...], "runs": ["X", ...], "verdict": "same|one_apart|different|one_run_only", "differs": [...], "changes_the_answer": "yes|no|unsure", "why": "<= 30 words"}`
- then one line per topic: `{"id": "t..", "answerable": "...", "worth_tracking": "...", "why": "<= 15 words"}`
