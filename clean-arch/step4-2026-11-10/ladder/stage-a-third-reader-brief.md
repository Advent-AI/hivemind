# Stage A: the third reader's rulings

Two readers each marked a set of judged questions, independently, with the form in
`/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/ladder/stage-a-reader-brief.md`. Read that form first: it says what an item
is, the rules a judged question must meet, and what each mark means. You rule where the two readers differ.

## What you are given

A packet of items. Each item is as the form describes it (the thesis, the article, the fiscal-year note, the ladder as the judge
is shown it or the refusal, the other fields), with one more field, `to_rule`: a list of the points to rule on for that item.

- A differing mark: `{"id": "17-Q", "mark": "Q", "reader_a": "holds", "reader_b": "fails", "reader_b_reason": "..."}`. One reader
  held the mark and the other failed it. The reason is the sentence the failing reader gave for all the marks it failed on the
  item, so part of it may concern another mark. "a" and "b" are not the same reader from one item to the next.
- A fault named under `W`: `{"id": "17-W-a", "mark": "W", "fault_named": "...", "the_reader_s_reason": "..."}`. One reader named a
  fault that no mark of the form covers.

## How to rule

- Read the thesis and the article of the item yourself before ruling. Rule from them and from the mark's definition in the form,
  as the form words it. The readers' values and reasons are leads: a reason may be right, wrong, or about another mark.
- A differing mark: decide whether the mark, as the form defines it, holds or fails for this item. Rule on that mark only. A
  fault that belongs to another mark does not fail this one.
- A fault named under `W`: uphold it only when it is true of the item and would mislead a reader of this judged question. Do not
  uphold a fault that is not there, a matter of taste, or a difference that changes nothing a reader would conclude.
- Do not rule a mark `fails` because you would have written the question differently, and do not rule it `holds` because the
  fault is small: the form's wording decides.

## What to return

One JSON object per point, one per line, in the order the packet gives them, as your final message: no prose before or after, no
code fence.

- for a differing mark: `{"id": "17-Q", "ruling": "holds"}` or `{"id": "17-Q", "ruling": "fails"}`, with `"why"`: one sentence
  naming the words or the figure that decide it;
- for a fault named under `W`: `{"id": "17-W-a", "upheld": true}` or `{"id": "17-W-a", "upheld": false}`, with `"why"` likewise.

Every `id` of the packet has exactly one line.
