# The loss trace: was the fact extracted? (read-only)

You are an independent reader. Do not edit files, run model calls or start runs, and do not read any file other than this brief and the one
packet you are given.

Each point of your packet holds one **decisive item**: a statement an earlier reader, called reader B, cited for a frozen answer (its day,
title, who said it, the passage and its meaning). Beside it is **every evidence item a system kept from that same article** (each with a
`ref`, a summary and the passages it quotes); the list is empty when the system kept nothing from the article.

For each point, answer one question: does one of the kept items **state the decisive item's fact** — the same fact or figure, in any wording?
Name the kept item's `ref` that states it (the first if several do), or `none` when no kept item states it. Search the kept items for the
figure or the fact; do not name an item because it is related, from the same article, or about the same topic.

Return one JSON object per point, one per line, in packet order, and nothing else (no prose, no code fence):
`{"point": 3, "extracted": "<ref>"|"none", "why": "one sentence naming the figure or fact that decides it"}`.
