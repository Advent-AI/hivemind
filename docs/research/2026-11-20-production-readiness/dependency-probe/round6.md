# Council Q, round 6 (read-only; no edits, no model calls)

Your round-5 changes are taken in `probe.py` (`one_attempt`, the `send` loop):
- one transport attempt per call (`model.openai_transport(..., max_attempts=1)`);
- the reservation is one token per character of the full serialized request (`json.dumps(build_request(...))`, about 74,000
  characters) plus the full 16,000-token output allowance: about $0.0154 a call; six worst-case calls $0.093, under the $0.15 cap;
- an exception (transport failure or malformed answer, usage unknown) keeps the reservation charged;
- a cap stop before both arms have three samples is reported as inconclusive.

$0 dry run (fake transport returning old-2's stored 09-20 answer; the credential reader replaced by a refusal): 6 calls, old-2 only,
control and changed interleaved, every answer through `judging.check_answer`, rows written; a second run on the same scratch is
refused because the archives exist. Serialized requests 73,632 (control) and 74,397 (changed) characters.

Is it sound to send now? End with CONSENSUS or DISAGREE. Under 100 words.
