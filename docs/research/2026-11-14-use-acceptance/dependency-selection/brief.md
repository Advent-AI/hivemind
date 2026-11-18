# Brief for a blind reader: which earlier question would a new question want as an input?

Read `packet.md` in this folder: fifteen questions a research system opened in one week about one company, and, for each newly
opened question, the earlier questions it was compared with at that moment (plus any question opened from the same article).

Think as a senior hedge-fund analyst. A question "wants another question as an input" when the answer to the first is made more
or less likely by how the second turns out, so that an analyst answering the first would ask for the current conclusion of the
second, and that conclusion would tell them something the first question's own news would not normally state.

For **every** pair listed under "The pairs to mark" (the new question first, then the other), give exactly one mark:

- `relies`: the new question would want the other question's conclusion as an input.
- `reverse`: it runs the other way only: the other question would want the new question's conclusion.
- `mutual`: each would want the other's.
- `same`: the two ask one thing (other wording, or another period or deadline of the same thing): a duplicate or a successor, not an input.
- `none`: neither would want the other's conclusion (sharing the company or the industry is not enough).

Add `strength`: `strong` (an analyst would clearly ask for it) or `weak` (second-order or arguable); leave it empty for `none`.
Add a `why` of at most twenty words for every mark other than `none`.

Use only `packet.md`. Do not open any other file. Write nothing but one JSON object per line, in the packet's order:
`{"new": "v4", "other": "v2", "mark": "...", "strength": "...", "why": "..."}`. There are 97 pairs; answer all of them.
