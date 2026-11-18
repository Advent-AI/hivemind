The probe is **not ready to send**. The six-request check passed, but a returned answer can be lost, and the reader can count an answer under the wrong case or count a refusal for a reason other than the one assumed by the protocol.

**Serious findings**

1. **A returned answer can be lost if saving the raw response fails.** In [resend.py](/Users/lchingen/hivemind/clean-arch/e2e-misses-2026-11-11/resend.py:167), the response is assigned to `current.returned` only *after* the raw file is written. If that write raises, the exception handler has no saved response to put in the outcome. The spending guard charges the attempt, but the answer is lost.

2. **The reader does not verify an outcome’s case or send number.** [resend.py](/Users/lchingen/hivemind/clean-arch/e2e-misses-2026-11-11/resend.py:222) checks the folder’s registered request hashes, then reads each file by name without checking the `case` and `send` recorded inside it. For example, a copied or misnamed outcome can be counted as an answer to another case. A matching folder registration does not bind each outcome to its request.

3. **The reading rule counts refusals whose rung may itself be invalid.** [PROBE.md](/Users/lchingen/hivemind/clean-arch/e2e-misses-2026-11-11/PROBE.md:44) says refused answers count because the observed refusals concern cited IDs. But [judging.py](/Users/lchingen/hivemind/src/hivemind/views/judging.py:210) can also refuse an out-of-range rung or an inconsistent `changed` value, and [resend.py](/Users/lchingen/hivemind/clean-arch/e2e-misses-2026-11-11/resend.py:235) counts every check-refused rung. The reason for a future refusal must be inspected before applying that reading rule.

4. **`read` can overwrite a file outside the data folder.** [resend.py](/Users/lchingen/hivemind/clean-arch/e2e-misses-2026-11-11/resend.py:222) accepts any folder with a matching registration and writes `reading.json` there without checking its location or whether that file already exists. That can damage an existing reading.

**A. Saved requests and ledger.** The permitted offline check passed all six cases. For the first case, the first recorded request matches a refused archive row; its saved answer is rung 4 and is refused again for `v8 is not a dependency of v17`. All six rebuilt requests match their saved canonical requests and today’s production serialization. The ledger is stopped **before the day’s round**, not at the precise instant that answer was checked. The check’s relevant state appears consistent with that use: other judgments in the round are recorded separately, while the request supplies the shown IDs. The passing checks do not independently prove every ledger value is identical at the exact checking instant.

**B. Sending.** Apart from finding 1, the sender uses one-attempt transports inside the shared limit’s maximum of three attempts. The six cases’ computed worst cost is $0.6528 against the $0.70 cap; the limit reserves under a lock. The send output is constrained to a new folder beneath the data directory. This conclusion assumes the budget’s token-price and worst-cost bounds hold.

**C. Reading.** Individual malformed or unreadable outcomes are caught and reported rather than crashing the outcome loop. Findings 2–4 remain. A missing or malformed registration can still stop the reader before that loop; it does not produce a count.

**D. Protocol claims — not serious.** [PROBE.md](/Users/lchingen/hivemind/clean-arch/e2e-misses-2026-11-11/PROBE.md:11) says **4 of 8** changed rungs were on the China question, but lists five; the stored census also shows five. Its descriptions of a two-out-of-three result as the judge’s “usual” answer and as showing that the re-ask turned an answer into a miss go beyond what three samples establish. They support a lead, not a demonstrated rate or cause.

No network request was sent and no file was edited.



NOT READY — serious findings 1, 2, 3 and 4.