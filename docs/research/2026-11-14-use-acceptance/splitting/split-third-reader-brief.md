# Third reader: one BY or LQ point per entry (read-only)

The two first readers disagreed on `BY` or `LQ` for one item, or one of them could not tell. You decide that point.

## Your input

- `split-brief.md`: what `BY` and `LQ` mean, and how an item with `split` is read.
- `third-reader/split-packet-1.json`: one entry per point.
  - `id`: the point (`<item>-BY` or `<item>-LQ`).
  - `item`: the item as the first readers saw it (the thesis, the article, the question with its answer choices, and `split`).
  - `field`: `BY` or `LQ`.
  - `marks`: the two readers' values, as `a` and `b`. Who wrote which is hidden.

## Your answer

One line for each point:

```
{"id": "<the point's id>", "ruling": "<yes | no | cannot_tell>", "why": "<one sentence naming the year or the limit>"}
```

Write the lines to `third-reader/split-rulings-<your family>-1.jsonl`; your family is `codex` or `claude`, as you were told. One line
for each point, and no other text.
