**Do not send yet: one outcome the real runner can produce will crash the blind packet builder.**

If an answer is refused twice by code, its status is `no ladder: refused` and its `answer` is `None`. The new `reading()` passes every outcome to `build_reader_packets.item_of()`, which handles only a written ladder or a model’s `no ladder`; for a code refusal it tries to read `answer['ladder']`. The recorded preflight saw contract refusals that were repaired on resend, so a twice-refused answer is a relevant path. [Probe](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-6/due-day/dueday_probe.py), [packet builder](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/build_reader_packets.py:30)

Before sending, handle code-refused outcomes separately from model declines: count them as lost answers in the matched comparison, exclude them from semantic review, and prevent a new loss in v2 from producing “moves.” Adjust the expected packet and review counts, then prove the actual path with a $0 test that produces a twice-refused answer.

The other requested corrections are present: rendered views, the fuller decline brief, two-file validation and four blind controls. Once the code-refusal path is proven and preflight is refreshed, the probe is ready for its send decision.

**CONSENSUS: no, because a twice-refused answer currently breaks the review and must be accounted for before spending.**