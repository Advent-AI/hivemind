# Source review of written answer choices (blind, read-only)

You read `review/packet.json` in the run's reading folder (the path is given in your handoff). Each item is one written judged question with its
answer choices, the topic it was written for and the article. For each item, compare the question with the article and the topic, and list
every material defect of these kinds (an empty list when there is none):

- **(i) The wrong side asked.** The topic names a figure together with a second side of the same bet: a share of that figure, whether supply
  stays short of demand, or whether capacity keeps pace with demand. The question asks the second side, or something else, instead of the
  figure. When the topic's outcome tracks the share itself, with the total only as its base, asking the total is this defect.
- **(ii) An invented measure.** The question asks a quantity, unit or series that neither the topic nor the article names, and the answer
  could not be settled from the material the question names.
- **(iii) A second side dropped.** The second side that the topic names is not in `not_judged`.
- **(iv) A due day that does not fit.** The day falls before the material that settles the question can exist, or contradicts a date the
  topic or the article gives. Report it; it is a separate class.

Return one JSON object per line, in item order, and nothing else:
`{"item": <n>, "defects": ["i" | "ii" | "iii" | "iv", ...], "why": "<one sentence quoting the source, or empty>"}`.
Edit nothing and make no model call.
