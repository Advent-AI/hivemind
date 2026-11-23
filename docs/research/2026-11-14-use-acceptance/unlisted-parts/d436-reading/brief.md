# Reading: one bet, separate bets, or a main part that must be declined? (read-only)

A step writes one judged question for each research topic, or declines. Alex's decisions govern what counts as one question; they are
in `decisions.md` (D397, D417, D436, D437), in full. Read them first.

The packet (`packet.json`) holds 12 topics. Each has a `description` (the topic's question), an `outcome` (what is tracked), a `period`
and the full `article` it came from. Read each article before deciding its topic.

For each topic:

1. List the parts the description and the outcome name (each figure, event, period or checkpoint, comparison, consequence).
2. Classify the topic as exactly one of:
   - `one_bet`: one bet; any other part is a second side of the same bet (D436) and stays as context, shown as not judged. Name the
     main part and each second side.
   - `separate_bets`: two or more parts an analyst would hold separate bets on, none of them the main one, so the topic gets no judged
     question (D397). Name them.
   - `main_declined`: there is one main part, but it itself breaks a decline case (for example a rolling twelve months with no
     publication day, D417). Name the part and the case.
   - `unresolved`: the decisions and the article do not settle it. Say what would.
3. Quote the words of the decisions that decide your classification, and the article's words that bear on it.

Return one JSON object per topic, one per line, in topic order:
{"topic": <n>, "parts": [...], "class": "one_bet|separate_bets|main_declined|unresolved", "main": "<main part or null>",
 "second_sides": [...], "separate": [...], "decision_words": "...", "article_words": "...", "why": "<one or two sentences>"}
and nothing else: no prose before or after, no code fence.
