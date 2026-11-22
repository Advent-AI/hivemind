# Paid acceptance probe of judging-v12 (design v5, D715; registered before any send)

**Alex's ceiling:** $0.50 (D715, "0.5 美元 (推荐)"), held by `budget_replay.SharedLedger`, which stops at it.

**Frozen inputs:**
- `probe-plan.json` (`probe_plan.py`, $0);
- `probe-targets.json`: the Part B targets, read from the stored refused answers before any send and never edited after the first.

**Model and settings:** poc-v121's rejudging setting (gpt-6-luna, medium effort, 16,000 output tokens), the provider's strict format.

v2 answers council round 40 (`codex-r40.md`):
- blind reading rules, an omitted material fact counted;
- all Part C comparisons read;
- the pass line stated as this probe's tolerance;
- completeness required;
- the sealed request last;
- a schedule proved against the real reservations;
- request-time checks;
- a full $0 rehearsal.

v3 answers round 40b (`codex-r40b.md`):
- the targets' sources completed against the stored accepted retries (e3768 for the signed agreement; e41 and e120 for the Kyber
  delay; the AMD entries), with a `partial` list;
- misattribution counted by claim;
- a material fact unsupported in all three draws treated as omitted;
- Part C reads what every answer says and attributes;
- a refused v7 control answer is still read;
- the budget claim corrected;
- the stops rehearsed.

v4 answers round 40c (`codex-r40c.md`):
- each evidence target's `required` claim and `optional` details;
- class precedence;
- Part C loss counted by claim;
- quotes of shared sources in the packets;
- one ordered verdict.

v5 answers round 40d (`codex-r40d.md`), and round 40e: a material loss needs all three draws received and read.
- each draw's valid support is recorded apart from its class, and a material loss means no draw with valid support;
- Part C's wrong attributions are counted by claim;
- a missing A1 or A0 result counts as incomplete.

## 1. What it decides

| Question | Part |
|---|---|
| Q1. Does the provider accept judging-v12's format on a real request, the largest of the five archives included, and on an empty list? | A |
| Q2. On the requests the open format let the model get wrong, does it now state each fact and cite a listed source for it, without a wrong listed id in its place, and without dropping a material fact? | B |
| Q3. On ordinary requests, does the closed format change what the judge cites or concludes, beyond its own variation under the open format? | C |

## 2. The sends, in this order

1. **A1:** old-1 call 5652, the largest stored request of the five archives (451 evidence ids). Its `cites_views` is empty, so it
   also exercises `maxItems: 0`.
2. **A0:** old-3 call 69, a request with an empty theme list (`theme_pushes` with `maxItems: 0`); under $0.001.
3. **Part B:** the 16 distinct refused requests, 3 sends each under v12's format.
   - control-1's 8941 is 8938's retry: one request, both attempts' bad ids targeted.
   - linked-1's 7 requests keep their stored judging-v8 text; only the answer format changes. That makes them a format probe on
     those texts. No v8-based version is built.
4. **Part C:** 12 matched comparisons, one per (source, question) of the refused set. Each is the same question's accepted
   first-attempt request in the same archive with the closest evidence count; ties go to the nearest call on either side, which is
   what `probe_plan.py` does.
   - Each comparison is 3 sends under v12's format and 3 under judging-v7's open format (the fresh control).
   - Comparisons run cheapest first. Within one comparison the six sends run one after another.
   - The 16 refused requests map to 12 (source, question) pairs. The four duplicates are dropped to fit the ceiling, so every
     question is covered once per source.
5. **A2,** last and only if the headroom then covers its reservation ($0.0824): the sealed D358 run's call 6918 (647 ids) with v12's
   format built from its lists. It is a size check on an older request text. A 200 shows that a request this size fits; a 400
   establishes an enum limit only if the provider's error says so. Its answer is not read.

**Start rule** (proved at $0 with `budget_replay.llm_estimate`):
- Only one Part C comparison runs at a time.
- It starts only when the ceiling minus spent minus reserved covers the sum of its six first attempts' reservations.
- On the stored-token estimate all 12 start: lowest margin $0.037; expected core spend $0.347.
- If every send costs 30% more than stored, only 10 start in this order: the 11th needs $0.136 with $0.107 left.
- A retry reserves again, so an admitted comparison can still stop incomplete.
- A comparison not started, or stopped, makes Part C incomplete, and the outcome inconclusive.

Each part's sends run at most 4 at a time. Every send gets its own archive (per part, request, format and draw), so `model.call`
never answers a draw from an earlier draw: every draw is a fresh provider call, counted at the transport.

A transport error is recorded. The budget transport retries a 429 or 5xx as it does in production, and settles an error at its
reservation.

## 3. Reading rule (frozen)

### Checks on every answer
Every answer is checked as at request time, with a harness check proved equal to `check_answer` on fixtures and on the stored
answers (§4):
- membership against the request's lists;
- the rung range from the request's ladder line;
- first-judgement and changed against the request's "[Previous conclusion …]" line;
- non-empty stance fields;
- duplicate theme pushes.

The archive's final ledger state is not used: it falsely refuses stored answers such as 8834 and 8851 (Codex r40).

### Part B (48 answers)
Each answer is read against `probe-targets.json`.
- **Evidence targets.** One class each, judged by the claim each cited or pushed entry is used for:
  - *intended*: the claim is stated, an entry in `sources` is used for it, and no other entry is used for it without carrying it;
  - *unsupported*: stated, with no entry in `sources`. An entry in `partial` alone leaves the exact claim unsupported, but is not a
    wrong attribution;
  - *misattributed*: an entry is used for the claim while its quote does not carry it. This counts even if the entry supports a
    different claim in the same answer, or a correct source is also cited;
  - *omitted*: the claim is not stated.
  - The class is judged on the target's `required` claim against `sources`. An `optional` detail stated without its own source is
    unsupported for that detail only, recorded, and does not change the class.
  - When more than one class applies, misattributed comes first, then intended, then unsupported, then omitted. A wrong source with
    no correct one is misattributed.
  - Apart from the class, each draw records **valid support**: the required claim is stated and an entry in `sources` is used for
    it, whether or not a wrong source is also used. The material-loss rules count draws without valid support, whatever their class.
  A `markers` search in the answer's text flags the reader's attention; the hand reading decides.
- **Placement targets.**
  - *correct*: the id appears only in its own field;
  - *absent*: not named;
  - a substitute evidence id carrying no claim the answer states is *misattributed*.
- **Ambiguous targets** (two acceptable sources, or an unclear fact) are reported and count neither way.
- **A second, blind reader** (Codex) reads the 48 against the frozen targets. A disagreement goes to a third, source-backed read whose
  class decides.

### Part C (12 comparisons, all 72 answers read)
- Every answer is read in full: its reference, implied outcome, reasons, and the claim each cited or pushed source is used for,
  shared sources included.
- The numbers only order the reading:
  - the sources cited by at least 2 of 3 answers in one arm and at most 1 of 3 in the other;
  - any v12 rung outside the range of the v7 rungs.
- A v7 answer the request-time check refuses is still read as an answer, and its refusal is recorded (it is the failure the closed
  format removes). A comparison is complete with its 3 + 3 answers.

A **material harm** is any of these, repeated (in at least 2 of 3 v12 answers and at most 1 of 3 v7 answers), counted by claim, not by
source id:
- (a) a claim that moves the forecast or the reference, which at least 2 of 3 v7 answers state with a listed source carrying it (any
  such source: one control citing e195 and another e669 for the $393 billion reference count as two), and which at least 2 of 3 v12
  answers do not state with a carrying source;
- (b) a claim that at least 2 of 3 v12 answers attribute to a source whose quote does not carry it, counted by claim whichever
  sources are used. For example, "the market reference is $390 billion" attributed to e195 in one answer and e669 in another, while
  both entries give $393 billion;
- (c) a changed reference or implied outcome whose stated support is a citation of kind (a) or (b);
- (d) a v12 rung outside the v7 range whose reasons trace to (a), (b) or (c).

A difference that is not repeated, or whose cause cannot be read, is **unresolved**.

### Outcome (registered; proposed tolerances for this probe, not historical rates)
One verdict, taken from the first rule that applies:
1. **Not ready (format):** A1 or A0 is rejected or returns a format-invalid answer.
2. **Not ready (confirmed failure):** any of
   - a v12 answer refused by the request-time check;
   - more than 2 of 48 Part B answers with a confirmed misattribution;
   - a confirmed material loss in Part B;
   - a confirmed material harm in Part C.

   A confirmed failure stands even when the run is incomplete.
3. **Inconclusive (incomplete):** a budget stop; A1 or A0 without a result (a transport failure or timeout, as opposed to a format
   rejection); a missing Part B answer; or a Part C comparison not started or interrupted.
4. **Inconclusive (unresolved):** an unresolved material loss in Part B, or an unresolved Part C difference that would be material if
   confirmed.
5. **Pass ("ready to propose adoption"):** otherwise.

A2, sent, skipped or rejected, never changes the verdict; it is reported. The conditions behind these rules:
- **Pass,** when every condition holds:
  - Q1: A1 and A0 return 200 with format-valid answers;
  - all 48 Part B answers and all 12 Part C comparisons (72 answers) are complete;
  - no v12 answer is refused by the request-time check;
  - in Part B, at most 2 of 48 answers have a confirmed misattribution (an answer counts once), with the number of requests affected
    and any repetition reported;
  - no confirmed material loss in Part B: a material target whose three draws were all received and read, none with valid support
    (whatever each draw's class), which the stored accepted v7 answer to the same request stated and supported;
  - no confirmed material harm in Part C.
- **Inconclusive:**
  - a budget stop, a missing answer, a comparison not started or interrupted;
  - an unresolved material loss in Part B: a material target whose three draws were all received and read, none with valid support,
    where no stored accepted v7 answer to that request kept it, as in control-1's 8938, whose retry also dropped 85.4%;
  - an unresolved Part C difference that would be material if confirmed.

The outcome is computed by code (`probe_read.py`) from the read classes; the rehearsal exercises it (§4).
- **Not ready:** any other failure of the pass conditions, with its reason.
- Every outcome goes to Alex; adoption is his decision.

## 4. Harness and the $0 rehearsal before the send

`probe.py`, harness-only:
- it reads `probe-plan.json` and builds each request with `model.build_request`, from poc-v121's setting and v12's format (or v7's
  for the control);
- it sends through `budget_replay.BudgetTransport` on a ledger at $0.50, in the order and under the start rule of §2;
- each answer goes through `model.call`'s format check and the request-time check;
- each answer is written to `probe-answers.jsonl` with its part, request, format, draw, the request sha, the cost and the transport's
  call number.
- `probe_read.py` builds the reading packets:
  - Part B by target, with marker flags;
  - Part C by comparison: all six answers in full, the quote of every source any of them cites (shared ones included), and the
    symmetric-difference sources marked.
- `probe_read.py` also computes the one verdict of §3 from the read classes.

**The $0 rehearsal** uses the real budget transport with the provider stubbed underneath (`model.openai_transport` replaced), on a
ledger file of its own. It must show:
- every scheduled send reaches the stub, with a count equal to the plan: 2 + 1 for A, 48 for B, 72 for C;
- each request's bytes: system and user equal the stored ones, the format strict and equal to `schema_for('judging-v12', lists)` (or
  v7's), the model settings as poc-v121's;
- three fresh stub calls per draw set;
- the request-time check equals `check_answer` on a ledger fixture whose state is known, accepts every stored committed answer of the
  planned requests, and refuses the stored refused ones on their ids;
- the stub's valid answer, a format-invalid answer, an HTTP 400 and a 5xx followed by success each take their path;
- only one Part C comparison runs at a time;
- a ceiling set low blocks a Part C start, and the outcome is "inconclusive", never "pass";
- a retry exhausts the remaining headroom inside an admitted comparison, which stops it; the outcome is "inconclusive";
- the outcome code's verdicts:
  - three Part B answers for control-1's 8938 that state 85.4% with no source are an unresolved material loss, so "inconclusive"
    (8938 has no stored accepted v7 answer);
  - three answers for control-1's 8807 that state the $393 billion reference with no source are a confirmed material loss, so "not
    ready" (its stored accepted retry 8809 cites e195 and e669);
  - three misattributions are "not ready";
  - for 8807, two draws giving the $393 billion reference with a wrong source and a third omitting it: within the misattribution
    tolerance, but a confirmed material loss, so "not ready";
  - A1 timing out after the transport's retries is "inconclusive (incomplete)", told apart from an explicit format rejection;
  - for 8807, one unsupported draw and two draws missing after a budget stop: no material loss can be declared, so "inconclusive";
  - a clean set is "pass";
  - an A1 rejection is "not ready (format)", even though it also leaves an answer missing;
  - a confirmed misattribution excess with Part C incomplete is "not ready";
  - an unresolved material Part C difference with everything else clean is "inconclusive";
  - A2 skipped, and A2 rejected, each leave a clean core "pass";
- the Part B packet for 8938 flags a stub answer that drops "85.4".

A mutant, Part B sent with the open format, is caught by the byte check.
