# Gate 2: c15yc against c8 on the stored neighbours of the year change (D437), version 11, 2026-11-13

Versions 1–10 were reviewed (`clean-arch/step1-unfiled-2026-11-08/council/ly-codex.md`, `lz-codex.md`, `ma-codex.md`, `mb-codex.md`,
`mc-codex.md`, `md-codex.md`, `me-codex.md`, `mf-codex.md`, `mg-codex.md`, `mh-codex.md`: not ready). The rounds found two recurring mechanisms. First: a list of bad outcomes written case by case misses a case each time (a dropped statement, a lost amount thesis, an
exception). **Structural rule adopted (AGENTS §1; §2, "the closed set of what passes"):** each control except Ohio states its good outcome
as a closed set; every other send, whatever its cause, is bad. Ohio is the one exception, compared by two counts, because it is not this
change's target.

**What it decides.** Whether c15yc (c8 with the year boundary and the scoped capacity counterexample, `arms/c15yc-*`, +332
characters) breaks a neighbouring case that c8 handles. It does not re-measure the year case: gate 1's year line **failed, 5 of 9
against 8 of 9**, and is carried by Alex's word (D437), not passed. A gate-2 pass leads to gate 3's design (a paired comparison on
fresh articles), put to Alex before any send; a fired stop, or an unexercised control, goes to Alex.

**The claims each control must keep** are fixed before any answer, from each state's stored c8 answer: `gate2/required-statements.json`
(sha256 `42fd6bae291befb7e9c3c04450975c90a5454ce986a4aa46d6185745f2b4d3bb`), one written claim per statement, naming the quantity or event, the figure or direction, and the speaker where every stored answer of
the state names the same one (checked): capex C26 (~$650bn of hyperscaler data-center capex planned for 2026) and C27 (~$1tn projected for 2027), with no
speaker required; Goldman's estimate G; the Kyber delay report K1 and NVIDIA's
denial K2; memory M1 (~$2m memory per rack, +435%), M2 (self-sourcing could cut the rack price to ~$6.7m) and M3 (constrained supply
pushed contract memory prices up), M2 and M3 only where the stored answer kept them (d1, d2). *Second recurring mechanism:* recognising a
kept statement by its words or passage let a lost claim count as kept (a denial carries the word "delay"). **Structural rule:** a claim
is kept when a kept evidence item of the send states the same figure or event for the same measure as the claim (the item may carry
more); a detail of the claim (a speaker, a count of companies, a percentage) is required only where the stored c8 item of that state
states it, so the reference is never more detailed than what c8 kept; and is linked as its control requires; a capex claim links to the capex thesis of its year when
that year's thesis is open or newly opened in the send, otherwise to the open capex thesis. It is judged by reading, twice: I read every
send of both arms with `gate1/print_records.py --full`; a blind reader (Codex, read-only) receives, for every send of both arms
(shuffled, labels hidden, key outside the repository), the claims of its state with the stored c8 items of that state beside them, the
send's kept evidence items with their links, and its theses, and marks each claim kept or not with the item it rests on. Where we differ, the claim counts as lost for a c15yc send and
kept for a c8 send.

**States.** The controls fixed for the year change before c14's send (`DIAGNOSIS.md`, "The first test"; `cases-c14.json`), each in the
three stored draws (d1, d2, d3), three sends per draw for each arm: nine sends per arm per control.

| control (stored article, step) | c8's stored behaviour | good send (closed set; every other send is bad) |
|---|---|---|
| 2026-07-07 repeat of $650bn and $1tn, one capex year open (capex-repeat-a, step 85) | linked | claims C26 and C27 are each kept and linked by the capex linking rule above, and the send opens no new thesis other than one for the missing capex year |
| a second 2026-07-07 repeat (capex-repeat-b, step 90) | linked | as above |
| another population of the aggregate: Goldman's broader estimate, the capex thesis open (population, step 66) | evidence on the open thesis | claim G is kept and linked to the open capex thesis, and no new thesis is opened on it |
| an event under another deadline: the Kyber delay article (kyber, step 45) | one thesis | the Kyber timing is held in exactly one thesis (open or new), and claims K1 and K2 are each kept and linked to it |
| a two-year comparison: memory prices (memory, step 56) | "2026–2027" | each listed memory claim is kept and linked to at least one thesis (in d2 and d3 the stored c8 answer opened no memory-price thesis and linked them elsewhere); whether a memory-price thesis and a change question exist is compared apart, below |
| a signed programme with a small obligation: NVIDIA's credit-support announcement (credit-model, step 1) | one amount thesis | exactly one thesis on the amount of NVIDIA's credit support (open or new), with no signing thesis and no thesis on a customer's own deployment |
| the Ohio article (ohio, step 8) | linked in d2, d3 | compared as two counts, below (not this change's target) |

**Decision rules, fixed before any answer is read.**
- *Bad send:* any send that is not a good send for its control, including an unusable answer (refused; unfinished; cut or malformed
  twice; refused by the runner's checks; a client HTTP error, 400, 401, 403 or 404; a malformed or non-object response; any error while
  processing the answer).
- *Unexercised:* a send the service never answered (a transport failure with no HTTP status, or status 429 or 5xx) after its two
  resends (`--network-resends 2`), a send not sent under the ceiling, or a send
  with no record (the harness now records an error while processing an answer as that send's outcome, so a missing record means the
  run itself stopped). Any unexercised send makes its control unexercised.
- *A stop fires* when c15yc has more bad sends than c8 over the nine, by more than 2 (the tolerance declared for these controls before
  c14's send). It allows a difference of two in nine by design: a pass is not proof that nothing regressed; every send is reported.
- *Memory's theses:* a stop also fires when c8's count of sends with a memory-price thesis (open or new) exceeds c15yc's by more than
  2, or c8's count of sends with a change question exceeds c15yc's by more than 2.
- *Ohio:* in each arm, the share of usable answers that open the signing question, times nine; a stop fires when the two
  differ by more than 2. Unusable answers are compared apart: a stop fires when c15yc has more of them than c8 by more than 2. If
  either arm has no usable answer on Ohio, Ohio is unexercised, and the gate does not pass.

- *Pass:* every control exercised and no stop fires. Otherwise the gate does not pass and goes to Alex.
- *Memory marks.* A blind reader (Codex, read-only) receives every memory thesis of both arms (question, outcome, period), shuffled,
  labels hidden (key outside the repository), and gives each exactly one mark: *one-year price* (a price level for one period),
  *change* (the move from one year to another; a thesis that tracks a level and the change is marked change), *span* (a price over
  several years without a change), or *not a price*. I mark every thesis the same way before reading the reader's marks. Two yes-or-no
  properties are read from the marks: *a price thesis* (marked one-year price, change or span) and *a change question* (marked change).
  Where the two of us agree on a property, that is its value; where we differ, a second blind reader (Claude, the same packet and
  brief) marks the thesis too, and each property is decided by the majority of the three readings, which is always defined. A send
  *has a price thesis* when any of its memory theses is a price thesis, and *has a change question* when any is a change question.
- *Claims kept and linked* are judged by the structural rule above (two readings; a disagreement counts against c15yc).
- *Not included, stated:* the Gulf buyers' combined spending (G1-b reported it under change 2 alone, with no line, its suitability
  disputed); a company's own figure for both a fiscal and a calendar year: no control in `cases-c14.json` exercises it
  and none was found among the stored states; the risk is untested, not shown safe.

**Sends and cost.** 7 controls × 3 draws × 2 arms × 3 sends = 126 sends. Gate 1 spent $0.83 at published rates over 63 attempts
($0.013 an attempt); at $0.014 a send, about $1.8. **Ceiling $2.2**, enforced by the harness: production's reservation rule, attempts
waiting while reservations in flight would pass it, and a stop after any response that costs more than its reservation. As production
says of its rule, it is not a bill guarantee: an overrun can pass the ceiling by at most the attempts already in flight.

**Preflight ($0, before the send):** the dry run's byte check on all 126 requests, and the 21 stored c8 answers of these states through
the runner's checks under c15yc's schema (c8's, unchanged); results in `gate2/PREFLIGHT.md`.

**Expected effect on the judgement (D391, named first).** None from the controls themselves; they guard the second capex year's
question that c15yc opens in about three sends of four on the capex article, by showing it does not cost a repeat, another population,
an event's deadline, a comparison, a small obligation or Ohio.
