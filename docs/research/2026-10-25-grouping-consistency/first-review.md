One blocker: the baseline hides a grouping error inside a coverage difference.

[Plan line 7](/Users/lchingen/hivemind/docs/research/2026-10-25-grouping-consistency/plan.md:7) treats the extra OpenAI deployment mainly as different extraction coverage. But its [stored evidence explicitly names Vera Rubin](/Users/lchingen/hivemind/poc/reports/2026-10-25-direct-subjects-01/sample-2-retained/item3-extract.json:238), and [sample 2 places it only in g4](/Users/lchingen/hivemind/poc/reports/2026-10-25-direct-subjects-01/sample-2-retained/item3-result.json:26), outside the offered Rubin group. Under the plan’s same-product rule, these are two separate findings:

- Samples 1 and 3: OpenAI was not extracted—a coverage difference.
- Sample 2: OpenAI was extracted but missed Rubin—a grouping error.

Correct that baseline classification and include this existing case in the continuation review. Otherwise, the experiment could report preserved grouping while overlooking a known split.

I found no additional source/state/date/budget blocker in the proposed design. The new runner must enforce its separate **18-request/$2 cap**; inherited [Calls still hard-codes 48/$8](/Users/lchingen/hivemind/poc/hierarchy_study/study.py:281). No broader experiment or production change is needed.