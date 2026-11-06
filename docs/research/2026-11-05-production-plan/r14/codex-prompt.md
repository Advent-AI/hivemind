Round 8 of the read-only review of the split benchmark design, before any paid draw. Your round-7 review: docs/research/2026-11-05-production-plan/r13/codex-review.out
(one serious finding: record preparation tied to an article by quotes). Fix: bench_traces.raw_answers now ties a record-preparation call to the item
only when its request carries the item's whole article text ('[Article]\n' + text + '\n\n[Questions]', as split.preparation_request builds it); more
than one match is marked UNREAD as not attributable; none is marked UNREAD. Positive control: another article's preparation with the same quote is not
attributed and the item is marked unread; the item's own is found. On the probe's 73 items, all 21 preparations are tied by text and none is unread.
New: launch.sh (the launcher; refuses unless the design hashes verify and every draw folder is new; runs each draw under caffeinate). Hashes in
benchmark-design.sha256 (verify).
Say resolved / partly / not for the round-7 finding and judge launch.sh. Then report only a blocker or serious finding that could change the
benchmark's numbers or how they are read, or say "No remaining blocker or serious finding".
