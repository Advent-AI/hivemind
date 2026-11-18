# Applying one rule to 26 research topics (read-only)

Each topic in `topics.json` has three fields an analyst system wrote when it opened the topic:
- `description`: the topic's wording, the question an analyst is asking;
- `outcome`: what is tracked;
- `period`: when.

A later step turns each topic into one question with dated answer choices, or declines. It may decline when the topic has no main
thing to judge: the outcome names none, or "several with none of them the main one". The parts a question leaves out are listed
beside it as not judged.

**The rule to apply, exactly as written:**

> When a topic's outcome names several things, the main one is the thing its description asks about, if the description asks about
> exactly one of them. Judge that one, and list the outcome's other things as not judged. When the description asks about several of
> them alike, or about none of them, there is no main one.

**For each topic, answer in one JSON line:**
- `topic`;
- `several`: does the outcome name several things (true or false)?
- `main`: the main thing under the rule, in a few words, or `"none"`;
- `decisive_words`: the description's words that decide it, quoted exactly;
- `overrides_outcome`: true if the outcome expressly tracks two or more things as equal bets and the rule nevertheless picks one.
  Two years each asked for their own value, two separate decisions by two parties each tracked, and two figures each named as tracked
  all count;
- `arbitrary`: true if a careful analyst could read the description as asking a different one of the outcome's things;
- `why`: one sentence.

Apply the rule as written, not your own view of which thing matters more. Return exactly 26 lines, one JSON object per line, in the
file's order, and nothing else.
