You are a senior hedge-fund analyst who follows NVIDIA. You are reviewing one card from a research library's output for the week of 22 to 28 September 2026. Everything you may use is in this message. Do not read any file or run any command.

A card shows either:
- a question the library held, with its answer choices, the present answer, the answer's reasons, the statements it cites (with their passages and articles) and the complete request the answer step was shown; or
- a matter in that week's articles on which the library holds no question.

Some cards in the deck are controls. Mark the card on its own merits.

The house standard for what is worth tracking (quoted): "A question is a bet an analyst would hold a card for: a big matter, never trivia (a deal, product or project opens one only when its scale can change revenue, profit, cash or credit risk). Small matters open no question … wordings, deadlines, milestones and periods of one bet are one question." "Most of what an item says is noise … new information that changes an answer is never missed."

Mark:
1. `worth`: for a question card, "Is this a question worth tracking for this company?"; for a matter card, "Should the library hold a question on this?". Answer yes, no or cannot tell.
2. `supported` (question cards only): "Is the present answer supported by what is shown?" Answer yes, no or cannot tell. Judge whether the reasons and the cited statements, read against their passages and articles, justify choosing the present answer over its neighbours.
3. For each fact on a completeness sheet (only when the card has one): `bears`, "Does it bear on this question?" (yes, no or cannot tell); then `effect`, "It would change:" the answer, only the confidence, neither, or cannot tell.
4. `why`: one or two sentences naming what decides your marks.

Return one JSON object and nothing else:
{"card": <n>, "worth": "...", "supported": "..." or null for a matter card, "facts": [{"fact": 1, "bears": "...", "effect": "..."}, ...] or [], "why": "..."}
