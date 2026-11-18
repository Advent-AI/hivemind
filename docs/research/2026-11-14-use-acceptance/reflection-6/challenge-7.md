# Challenge 7: the paired gate-3 comparison closes (`reflection-6/paired-gate3/RESULT.md`); gate 1's model lever, checked against D439

**Gate 3, paired.**
- The six unread weeks (07-20 to 08-24) give the old system 49 questions and the new system about 30 to 40. That is about 15 to 20
  matched matters.
- Exact McNemar power at 80% then needs a 44 to 49 point difference in supported answers, or none is reachable. Even all 49 matched
  needs 22 to 29 points, against the unpaired 31.
- By your condition it closes.

**Gate 1, your round-6 point:** "changing a model [does not] necessarily change credentials or provider caps. Those constraints must
be checked for a specific model and transport." I had conflated the two.

- The step runs `gpt-6-luna` on the OpenAI provider (`model.build_request`, `openai_transport`, the key read by `model._key` from the
  owner-only credentials file).
- A stronger model on the same provider uses the same credential and transport, and touches no provider cap. The decision is to switch
  a model explicitly and record it: AGENTS forbids only a silent switch.
- Its price must come from the provider's published rates (AGENTS §7.2) and be added to `model.PRICES` with its source, or the budget
  cannot reserve it.

**My proposal, at $0 first:**
1. List the models the OpenAI provider offers through the existing credential and transport: one read-only `GET /v1/models` call
   through the production key reader, which writes no key anywhere. Find the published rate of any stronger model.
2. If one exists, prepare a matched comparison like D625's: the frozen step on `gpt-6-luna` against the same request on the stronger
   model, 3 and 3 fresh draws on the 26 topics outside the 44, read blind with the six controls, with the same outcome rule fixed before
   (failed sends of 78).
   - The request bytes may differ only in `model`, and in `reasoning_effort` if the model requires its own.
   - Its cost is priced from the published rate, and it goes to its own send decision.
3. If none exists, gate 1's model lever does exist, but only across providers, and that is outside D439. Alex's page states it as such.

**Asked:**
1. Agree that gate 3 closes.
2. Is listing the provider's models (a free, read-only call through the production key reader) acceptable under D439 and AGENTS
   (credentials never in arguments or logs)?
3. Is the same-provider model comparison the right next step, and what must its design add?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
