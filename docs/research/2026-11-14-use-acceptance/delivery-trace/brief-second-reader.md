# Brief: does a stored statement bear on a question, and did the judge already have it?

You are an independent reader, read-only. You did not write the system or this packet. The packet is
`docs/research/2026-11-14-use-acceptance/delivery-trace/packet-second-reader.json`. It holds three questions; for each, the whole
request the judge was last shown (`last_judging_request`) and a few stored statements (`candidates`), each with its quote from its
source article.

For each statement, answer from the question, the request and the quote only:

- `bears`: `yes`, `no` or `cannot tell`. Would an analyst holding this question weigh this statement as evidence, including evidence
  that only changes how likely an answer is?
- `in_request`: `yes`, `partly` or `no`. Is its substance (the same fact, figure, period and attribution) already in the request?
  `partly` when the request has the figure or the fact from another source or attribution.
- `moves_answer`: `likely`, `unlikely` or `cannot tell`. Given everything in the request, would adding it plausibly change the
  answer the judge gives, as opposed to only its confidence?
- `why`: one sentence naming the words that decide it.

Write one JSON object per line, `{"ref": "Q-…/S…", "bears": …, "in_request": …, "moves_answer": …, "why": …}`, for every statement in
the packet, and nothing else.
