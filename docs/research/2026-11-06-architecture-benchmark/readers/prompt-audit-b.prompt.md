You are the blind second reader of a prompt audit (AGENTS.md §6, "The prompt audit runs after every measurement"; the procedure is in
.claude/skills/prompt-audit/SKILL.md). Read-only: do not edit any file. You did not write the prompt.

Read the signed extraction standard docs/prd/05-extraction-standard.html (version 5) in full, AGENTS.md §6 and §8 (a general hedge-fund analyst;
lean cautious, catch the increment), and the whole request the split's evidence call (B) sends, as the model reads it:
docs/research/2026-11-06-architecture-benchmark/results/b-request-dump.md (system, user, schema). For comparison, the frozen production extraction's
system prompt is src/hivemind/prompts/role-v74i.txt; its user text and closing check are the ones B's user text was derived from.

The measured failure class: on 118 articles, B's arm lost about 9 helpful gold matters a draw against the frozen extraction, almost all because B
did not write the statement (competitors' and partners' figures, cross-company comparisons, product-plan changes). B's own account, on four stored
requests, cites a closing-check exclusion applied too broadly and the link rules read narrowly (probes/b-omission-account-2026-11-06.json).

Do the audit both ways:
1. Every sentence of B's request that decides keep, reject, link or a field value: say consistent / contradicts / keeps wider / keeps narrower /
   no source, against the standard's line (quote both).
2. Every keep rule of the standard (its §2 kinds and the evidence rule): is it carried by B's request, carried narrower, or missing?
3. Contradictions inside B's request (two sentences pulling opposite ways).
Then name, with quotes, the sentences most likely to make B write fewer statements than the standard keeps, and say whether the frozen role carries
the standard's keep rule differently. Return the audit as your final message: a table (sentence, standard line, verdict) and then the short list.
