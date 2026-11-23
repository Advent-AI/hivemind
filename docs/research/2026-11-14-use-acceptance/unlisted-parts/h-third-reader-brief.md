# Third reader: one listed part per point (read-only)

Two readers disagreed on one part of a question's list of parts not judged, or one could not tell. You decide that point.

## Your input

- `h-brief.md`: the four values and what each means.
- `third-reader/h-packet-1.json`: one entry per point.
  - `id`: the point.
  - `item`: the thesis (its description and outcome), the article, and the question with its answer choices
    (`ladder_as_the_judge_is_shown_it`).
  - `part`: the listed part and the reason given for it.
  - `marks`: the two readers' values, as `a` and `b`. Who wrote which is hidden.

Read the item's thesis, its answer choices and the part.

## Your answer

One line for each point:

```
{"id": "<the point's id>", "ruling": "<part | already_judged | settlement | cannot_tell>", "why": "<one sentence naming the words or the rung>"}
```

Write the lines to `third-reader/h-rulings-<your family>-1.jsonl`; your family is `codex` or `claude`, as you were told. One line for
each point, and no other text.

Rule each point on its own words. A rung decides a part only when holding that rung says whether the part happened.
