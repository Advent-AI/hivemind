**The wider problem is the better statement. I was too narrow:** the system does not yet reliably turn an important matter in the news into a clear, answerable question. A topic with two main parts is one visible failure, not the whole problem.

I would soften one part of your wording. “No owner” suggests we have proved that assigning the decision to a different step would fix it. We have not. The record shows that the decision is **made across steps without a consistently usable result**; it does not yet establish the right architecture or that every choice of question needs a tighter rule.

1. **The five facts**

- **Different questions from the same news:** I checked all three [July topic lists](/Users/lchingen/hivemind/poc/data/clean-e2e-full-2026-11-13/c1/cases/cases.json). They contain 15, 10 and 15 topics. Cloud spending, rental prices and memory prices do take materially different shapes. A yearly average and an end-of-year price movement, for example, can have different answers. This supports the wider problem; my two-part explanation does not cover it. It does not by itself prove that every difference is wrong.

- **Repeated refusals:** I checked the [map data](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/second-week/proofs/first-gate-map.json): 9 of 44, 9 of 40, 0 of 7 and 3 of 13 topics were refused in at least two of three attempts. That supports a broader handoff problem, with different reasons. But 21 of 104 is **not a population failure rate**: the readings differ and some topics repeat. Some refusals also correctly prevent unworthy questions.

- **Reference-window losses:** I checked [the opening review](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/opening-review/OPENING-REVIEW.md). Its 71 lost question-draws include 14 shown breaches, 27 choices the standard did not settle, 19 unresolved and 11 reasonable alternatives. This supports the importance of question formation, while limiting claims that the system was wrong on every loss. The 6.33-versus-4 comparison in D466 is a small, historical comparison, not proof that supplying questions generally solves the product.

- **Failed wording changes:** D473, D479 and D491 show stopped candidates; D483 records nine measured changes with none adopted and identifies interacting decisions in the reading call. That makes repeated local tuning a poor next bet. It does not prove a separate call would work: the old system and c19 are counterexamples to that shortcut. [Decision log](/Users/lchingen/hivemind/docs/DECISIONS-log.md)

- **Empty starts:** the July comparison and fresh-week test started empty. D370 removes the artificial preset questions but retains existing research as context; it does not decide that every real deployment starts empty. This is a plausible reason the tests repeatedly expose question invention, **not measured evidence that a prior library would solve it**. [D370 and D466](/Users/lchingen/hivemind/docs/DECISIONS-log.md)

2. **Falsifying the wider statement**

I support your blind comparison with two additions. The reader should first group shared matters without being told our positions, then compare the actual questions and their answer choices—not just their descriptions. They should record what would make the answers differ, whether each question is answerable, and whether the source supports it.

If most shared matters have the same substantive question, usable answer choices and settlement period, and meaningful differences are confined to multi-part topics, that would **weaken my wider instability claim**. It would not establish that multi-part topics are the only important loss: the test also needs to count matters opened in only one run and important matters missing from all three. Conversely, differing shapes are not automatically errors; the reader must say whether the difference matters.

3. **The question for Alex**

Neither of our earlier questions should be put as the next choice yet. Mine jumped to a treatment for one class. Yours bundles three separate choices: starting with real prior research, asking a person to approve new questions, and requiring a fixed form. D370 already permits the first; it does not establish the second. A mandatory approval step changes the product and its operating burden, and we have not shown that it is needed.

The question above both is: **“Who should decide which research questions the system tracks: the system, an analyst, or both?”** My current recommendation is to retain the system’s ability to propose and track questions using an existing real library, without making analyst approval mandatory until the evidence shows that the benefit warrants it. The two-figure issue remains a separate product choice if the review shows it matters.

4. **One next step**

Do the **$0 blind review of the three stored July runs**, with shared matters, one-run-only matters and a bounded source-based check for matters none opened. For each, record whether the questions ask the same thing, can be answered, and are worth tracking; retain disagreements and show concrete examples.

It would decide whether the main observed loss is unstable question formation across several types, or whether a narrower class carries it. Its falsifier is the result above: mostly substantively equivalent, answerable questions, with consequential differences confined to multi-part topics. It cannot prove a remedy or measure final-answer impact; it can tell us whether a remedy deserves design.

Position: The core problem is forming reliable, answerable questions from important news; multi-part refusals are one symptom, and the cause and remedy remain open.