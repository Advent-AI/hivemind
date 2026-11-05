- **Serious — [docs/DECISIONS.md:35](/Users/lchingen/hivemind/docs/DECISIONS.md:35):** Open item 3 says neither pull-mode decision is built, but closing due questions **is** built. D356 says `pull.py` writes the closing record and describes its test and replay ([log:3747](/Users/lchingen/hivemind/docs/decisions/log.md:3747)). Fix: say the successor-opening step is not built, while D356’s closing is built; retain the decision conflict for Alex.

- **Serious — [docs/DECISIONS.md:263](/Users/lchingen/hivemind/docs/DECISIONS.md:263):** The summary rejects “a published comparison” and an analyst’s reading with “no new fact.” Both are broader than D250. D250 preserves a competitor’s comparison for assessment and says an analyst’s reading that adds a new **fact or calculation** is judged under the evidence rule ([log:2979](/Users/lchingen/hivemind/docs/decisions/log.md:2979)). Fix: state both exceptions and the scope of the comparison rule.

- **Serious — [docs/DECISIONS.md:184](/Users/lchingen/hivemind/docs/DECISIONS.md:184):** The theme rule says a changed theme queues open asset questions without the qualification that they have evidence in force. D195 explicitly limits the queue to “every open asset thesis with evidence in force” ([log:2542](/Users/lchingen/hivemind/docs/decisions/log.md:2542)). Fix: restore that qualification.

- **Serious — [docs/DECISIONS.md:245](/Users/lchingen/hivemind/docs/DECISIONS.md:245):** The coverage-start entry names `baseline-v3` but omits its freeze and the requirement for Alex to open another prompt version. D365 says “the reading is frozen as baseline-v3 with this check; no further prompt version without Alex’s decision” ([log:3913](/Users/lchingen/hivemind/docs/decisions/log.md:3913)). Fix: include that rule alongside the description of the reading.

- **Serious — [docs/DECISIONS.md:272](/Users/lchingen/hivemind/docs/DECISIONS.md:272):** The Idea service section omits D134’s still-standing instruction for the MCP front to provide the workflow recipe to an external agent. D135 removed the agent loop **inside the service**, but explicitly kept that recipe at the MCP front, using the object list ([log:2022](/Users/lchingen/hivemind/docs/decisions/log.md:2022)). Fix: add the external-agent instruction and cite D134 and D135.

- **Serious — [docs/DECISIONS.md:132](/Users/lchingen/hivemind/docs/DECISIONS.md:132):** Extraction says items are read whole, but omits D23’s standing rule that untagged tables inside text are read by model extraction with no separate code parser. D23 states both and says the rule still applies to text that arrives after later changes ([log:416](/Users/lchingen/hivemind/docs/decisions/log.md:416)). Fix: add the rule to extraction and cite D23.

- **Serious — [docs/DECISIONS.md:329](/Users/lchingen/hivemind/docs/DECISIONS.md:329):** The index sends D9 to Classification, but its rule appears under System ([register:75](/Users/lchingen/hivemind/docs/DECISIONS.md:75)). This breaks the index’s instruction that its last column identifies the section holding the decision ([register:317](/Users/lchingen/hivemind/docs/DECISIONS.md:317)). Fix: change D9’s section to System.

The index’s **in-force versus non-in-force statuses** agree with `final.jsonl`. This review does not establish that every remaining sentence and every later amendment has been fully checked; the findings above are the discrepancies I verified against their sources.

serious: 7, wording: 0

