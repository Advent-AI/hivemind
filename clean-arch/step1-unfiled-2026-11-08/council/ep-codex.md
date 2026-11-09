**Yes. v3 still has blockers before it goes to Alex.** For example, the proposed date check would reject evidence the judge is supposed to remember from earlier days.

- **The leakage check is wrong.** The judge can show evidence from its last five judgements and evidence cited in its last ten; it is not limited to links made since yesterday. Check against the judge’s actual selection rule, while separately preventing future evidence and relationships. [Judging code](/Users/lchingen/hivemind/src/hivemind/views/judging.py:41)

- **Stage 0 depends on Stage 1 output**, although Stage 0 is supposed to finish before any paid send. Use stored or constructed seeded cases first.

- **The control is not yet demonstrated.** `preflight.py` replays stored answers through checks; it does not establish the claimed production-byte comparison. Also, `replay.run` has no 243-item manifest argument. Show how the harness enforces the same ordered inputs and independently verifies rebuilt request bytes. [Preflight](/Users/lchingen/hivemind/scripts/preflight.py:4), [replay](/Users/lchingen/hivemind/src/hivemind/replay.py:51)

- **The ±3 threshold is uncalibrated.** Two archived totals of 46 do not estimate how often this decision rule declares a difference when there is none. The rules can also both say “better” and “worse” if the total rises by three while one question drops. Resolve precedence and measure the rule’s error rate.

- **The Stage 1 control cannot have “control seeds’ links”**: its request is unseeded. Define the comparison in terms observable in both requests and specify how duplicate questions are identified.

- **The adapter still needs explicit repeat/revision mappings and a rule for partial verification.** Dropping a clean record with no verified passage changes what the clean library delivers; report it as an adapter loss.

**NOT READY**