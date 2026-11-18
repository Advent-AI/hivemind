# Gate 1 preflight (G1-a, G1-b), $0, 2026-11-13

- **Requests.** `probe_c14.py` dry runs build all 18 (G1-a: c8, c15yc) and 24 (G1-b: c8, c15c) requests; for every state the c8 arm
  equals production's stored `sent_request` with the same keys in the same order, and every stored request carries c8's system text,
  closing check and schema exactly. About 166k and 246k input tokens.
- **Answers.** The synthetic linked two-year answer (`synthetic-two-year-answer.json`) passes the schema check and every runner check
  under c15yc's schema (c8's, unchanged): 2 new theses, none unlinked. The runner's checks and c8's schema are what the c14 preflight
  replayed 24 stored answers through (`preflight-c14.output.txt`, 24 of 24 pass); neither has changed since. `scripts/preflight.py` does
  not cover clean Step 1 (`scripts-preflight.output.txt`).
- **Harness.** One network attempt per send, as production's live transport (`max_attempts=1`); a required `--max-usd` ceiling with a
  reservation for every attempt in flight. Checked with a fake transport (`gate1/check_probe_ceiling.py`, run with a scratch folder argument): a $0.001 ceiling
  sends nothing and records each attempt as not sent; a $5 ceiling sends, every call asks for one attempt, and the ledger matches the
  usage.
- **After the council read `council/lv-codex.md`:** the reservation is production's own upper estimate (twice the bytes plus 4,096
  input tokens, the whole output cap); an attempt waits while reservations in flight would pass the ceiling; a response with no usage
  settles at its reservation. The fake-transport check adds that case: a $0.25 ceiling with no usage returned stops after two
  reservations ($0.20 counted).
- **After the council read `council/lw-codex.md`:** a settlement can no longer raise (usage that is not a pair of whole token counts
  settles at its reservation, and the record-keeping line no longer reads a non-object usage), and a response whose usage costs more
  than its reservation stops every later attempt. `gate1/check_probe_ceiling.py` now asserts five cases (tiny ceiling, ample ceiling,
  no usage, malformed usage, usage above the reservation) with a 60-second hang guard: 5 of 5 pass, three runs. Mutants in scratch
  copies: a settlement that raises on malformed usage hangs the run (caught); no overrun stop sends all 6 attempts (caught). The first
  run of the asserted check also caught a real crash in the probe on non-object usage, fixed above. The ceiling is production's own
  reservation rule plus the overrun stop; as production says of its rule, it is not a bill guarantee: the output part is the provider's
  enforced cap, and an overrun can pass the ceiling by at most the attempts already in flight.
- **After the council reads `council/lz-codex.md` and `ma-codex.md` (for gate 2):** an error while processing an answer is recorded as
  that send's outcome; a network loss is a transport failure with no HTTP status or with 429 or 5xx (a client HTTP error or a malformed
  or non-object response is an unusable answer, not resent); every reservation settles whatever happens. The check asserts nine cases,
  9 of 9 pass. Mutants in scratch copies: every transport error treated as a network loss resends an HTTP 400 (caught); a reservation
  left unsettled on a non-object response hangs the run under a one-reservation ceiling (caught).

