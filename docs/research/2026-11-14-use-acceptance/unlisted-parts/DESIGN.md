# A candidate for the unlisted parts (line 2): design for the council (D576), 2026-11-16, version 5 (council rounds 61 to 64), nothing sent

**What it should change for a reader.** The product's page shows each question's parts not judged beside its answer (D570). When the
topic's outcome names a second figure, or a distinction the answer choices do not separate, the list should name it. Example: an
approval that may come with capped quantities, or the earlier checkpoints of a shipment forecast. Today such a part is listed in
some attempts and not in others (`CENSUS.md`: 12 failing attempts on 7 matters, plus 2 disputed).

**Hypothesis.** The request never says that "the topic's wording" includes the outcome. Its two examples both put the second part in
the topic's question; none puts it in the outcome. So listing an outcome-only part is a coin flip per send. The hypothesis rests on a
pattern, not a proven cause (`CENSUS.md`).

## The arms (small first; one lever per arm)

- **Arm A, the definition only.** Every place that says "the topic's wording" names the description and the outcome instead. There are
  four such places, and none is left undefined: `make_arm.py` refuses an arm in which "wording" remains. Nothing else changes: "a
  comparison" stays in the list of kinds, no exclusion is added, and the two examples stay.
- **Arm B (one example of an outcome-only part from another domain) stays an idea.** It needs its own audit and decision. An
  inconclusive or harmful A is not a reason to send it.

| Place | Now | Arm A |
|---|---|---|
| system, line 5 | "A topic's wording may ask about more than one thing." … "List every other part of the topic's wording that the question leaves out" | "A topic's description and outcome together may ask about more than one thing." … "List every other part of the topic's description and outcome that the question leaves out" |
| system, line 13 (events) | "A difference inside an outcome, such as an approval with conditions against one without, is not an outcome of its own; when the topic's wording names it, list it in not_judged." | "… when the topic's description or outcome names it, list it in not_judged." |
| schema, `not_judged` | "Every other part of the topic's wording that the question leaves out (…); empty only when the question leaves nothing of the wording out." | "Every other part of the topic's description and outcome that the question leaves out (…); empty only when the question leaves nothing of either out." |
| closing check | "is every other part of the topic's wording listed in not_judged?" | "is every other part of the topic's description and outcome listed in not_judged?" |

Size (`make_arm.py`): system 9,545 → 9,601 characters, closing 1,326 → 1,342, schema 8,905 → 8,916. The growth is the definition the
audit found missing (PROMPT-AUDIT-LINE-2.md: verdict "missing"). Line 13 matters for the motivating "capping quantities": the request
already says to list such a difference "when the topic's wording names it", and that cap sat only in the outcome.

## What stays open as a question, and is measured as harm (not written as a rule)

| Question | D397 / D436 | The positive case that must still be listed | The case that should not be listed |
|---|---|---|---|
| Is a distinction already judged by an answer choice a part? | D397: the ladder judges the main part and shows the rest as not judged | a cap on an approval (Yes does not separate a capped approval from a full one) | "delayed past the check date or terminated" when Still open and Ruled out judge them (fortnight clean-6 pass 2 listed them) |
| Is how the answer is settled a part? | neither speaks to it | a topic that asks whether a company discloses something (the disclosure is the event) | "as reflected in its networking revenue disclosures and suppliers' shipments" |

A listed item of the second kind in either row is marked H, with "cannot tell" allowed. Neither question is settled as a rule here,
so H is read against the actual answer choices of each answer. No sentence about either is added.

## Inputs (stored requests, re-sent; Alex's 44 untouched, D426)

| Group | Topics | Why |
|---|---|---|
| motivating (the kind every reading failed) | fortnight clean-6, clean-7, clean-13; week of 10-06 clean-1, clean-3; July c1/clean-5 (DeepSeek), c3/clean-7 (graphics memory), if their stored requests are found byte for byte, else left out and said so | the class |
| regression watch (the disputed kinds) | fortnight clean-2 (prior year), clean-3 (consequence), clean-5 ($800 billion), clean-9 ($1.3 trillion); July c1/clean-6 ($650 billion) | the definition may change these too; the readings disagree on them, so each is reported, not scored as a win or a loss |
| harm controls | the fortnight's other six topics | lists no reader faulted |

The population is fixed before the send. All 18 stored first requests were rebuilt by the production builder with the same content,
July's three included (`probe.py check`, `check-output.txt`; what "the same" covers is under "Check before the send"). The harness refuses to send if a topic is missing or the check record
does not match the arm files.

Each topic: its stored request sent **unchanged** three times and **changed** three times, all on the same day. The unchanged sends
are the control; the stored answers are not, since a model call is a sampler. 18 topics, 108 sends.

## Reading (two families, blind to the arm), built and tested before the send

- **The folder.** `reading_prep.py` merges the two arms' outcomes and three planted controls into one Stage A run folder, so the
  fortnight's own tools read it unchanged:
  - `build_reader_packets.py` (its multi-run form) writes shuffled packets and a key kept outside the repository;
  - `collect_readings.py` reads the rows, lists the differences and loads the third readers' rulings.
- **The form.** The fortnight's reader brief (`ladder/stage-a-reader-brief.md`), every mark, so a change to the question or the
  choices is caught, not only L. Beside it, `h-brief.md` adds one field, **H**: one value per listed part, in order, like B:
  - `part`;
  - `already_judged` (a rung already decides it);
  - `settlement` (it names only where or how the answer will be known);
  - `cannot_tell`.

  A no-ladder answer and an empty list take `[]`.
- **Planted controls** (`reading_prep.py`; their expected marks are written to the key folder, outside the repository). Each is a
  stored fortnight answer.
  - Plant 1, the Hugging Face deal: a termination the Ruled out choice decides is added to its list. Expected `already_judged`.
  - Plant 2, the shipment forecast: the disclosures through which the volume is observed are added. Expected `settlement`.
  - Plant 3, the MIIT approval: unchanged. Its listed cap is expected `part`.

  A first reader who gives any other value on a planted item counts as a miss. A miss stops the reading before any verdict, even an
  inconclusive one, until the form is mended.
- **Third readers** of both families rule on every differing mark and every named fault (`collect_readings.py disputes`, the
  fortnight's third-reader brief). They also rule every H point where the first readers differ or either cannot tell: `h_disputes.py`
  writes those points with both marks as "a" and "b", sides drawn per point from a fixed seed, and `h-third-reader-brief.md` asks for
  one line per point. An unresolved point is counted both ways, and a conclusion stands only when both countings agree.
- **The score.** `probe_score.py` applies the rule below. It refuses to score (NOT SCORED) in each of these cases:
  - the reading does not hold each of the 108 arm sends and the 3 plants exactly once;
  - the plants file is not the one `reading_prep.py` builds;
  - a row is missing or not valid (H included);
  - a difference or an H point lacks a ruling from both third-reader families;
  - an H ruling is outside the four values, or one family rules a point twice.

  Tests: `test_probe_score.py`, 14, on a fake-transport run with made-up readings. They cover the decisions (a lead, inconclusive,
  harm, the changed arm failing L), a missed plant stopping the reading with a strong and a weak control, one H disagreement carried
  through the packet, two families' rulings and the score, and each refusal. Every guard's mutant fails its test
  (`test-mutants.txt`).
- **My own read:** every changed answer beside its control, and every H.
- **Incomplete sends.** An arm with a send that did not finish reads NOT MEASURED (the harness stops it). On the motivating topics, a
  changed send that is a refusal, or refused twice, counts as failing rule 1, so a missing L can never look like a pass. Refusals and
  sends refused twice are also counted as marks under rule 2.

## Decision rule (fixed before the send)

**What this probe is.** A small diagnostic on preselected cases: seven motivating topics, three sends each. Repeated sends of one topic
are not independent, and the topics were chosen because they failed. It can show a large drop on these topics. It does not measure the
rate of the class, and it cannot tell a modest change from noise. The thresholds below are written before the send; they are not
derived from a power calculation.

- **Inconclusive:** the same-day control fails L on fewer than 3 of the 7 motivating topics. The control did not meet the chosen
  exercise condition. That does not show the defect is gone.
- **A lead:** all three hold under both countings.
  1. The changed arm fails L, or is refused, on at most 1 motivating topic, in at most 1 send.
  2. In every group (motivating, regression watch and harm control), the changed arm's sends failing any mark other than L are no more
     than the control's plus one, mark by mark. Q, R, N, W, H, refusals and sends refused twice all count.
  3. No planted control is missed by either first reader.
- **L on the regression-watch topics** (comparisons and consequences) is reported both ways and does not veto. The readings disagree
  there, and scoring it would adopt one reading's threshold.
- **Otherwise negative.** Harm (rule 2 failed) stops the line.
- **A lead is not acceptance.** Acceptance is on fresh material: a new week (2026-10-13 to 10-19) through the frozen Steps 1 to 3, then
  the ladder step unchanged and changed. That run has its own design and decision. Its paid cost by the earlier weeks' ledgers is
  about $2.5 to $3.6.

## Check before the send ($0, done: `probe.py check`, `check-output.txt`, `check-mutants.txt`, `test_probe.py`)

- **The control is production's request, in content and in order.**
  - Each control, rebuilt by the production builder (`model.build_request` with the step's own payload and user text), has its stored
    first request's sha256: 18 of 18. That sha256 is computed over sorted keys, so it proves content, not wire order.
  - The order it cannot see is the same by construction. The user text is one string, and its order is inside the sha256. The schema
    keeps the frozen file's nested key order: checked, and the arm's schema keeps it too. The request is built by the function
    production uses, `model.build_request`, unchanged since 2026-11-08. The request files are unchanged since 2026-11-12, before all
    three stored runs.
- **The changed request differs only by the arm.** It equals the control with exactly the arm's replacements applied: 18 of 18.
- **The check catches what it should.** It fails on an arm file changed beyond the replacements (mutant 1) and on a control one byte
  off its stored request (mutant 2).
- **The stored answers pass the step's code checks.** Each is replayed from the model's own text as the step parses it. 17 of 17
  answers that wrote answer choices are accepted (the eighteenth was a refusal). A mutant answer (answer choices and a refusal at
  once) is refused. A synthetic answer that follows the changed request (clean-7 with its cap listed) is accepted.
  - On the way: replaying the stored answers as re-serialized JSON, not as the model's text, made 11 look refused. That was the
    harness's error, now fixed.
  - Also found: the step's code checks do not check the list's shape. The provider's strict schema holds it, and the product's bundle
    refuses a malformed list.
- **The send is bound to what was checked.** The record holds every control and changed request's sha256 (36). `send` rebuilds each
  from the same loaded cases and texts, refuses on any difference before any call, and then passes those same objects to the runner.
  `test_probe.py` shows three things, and each guard fails its test when removed (mutants):
  - a case changed after the check is refused, with no call and no folder;
  - a matching send files both arms;
  - an attempt charged above its reserve stops the probe as a breach.
- **Spending is held by reservation, under two stated assumptions.** Before every attempt, Stage A's limit reserves its worst-case
  cost. That cost counts every request byte as an input token and adds the full output cap: about $0.0104.
  - No attempt starts that could pass the $0.25 cap of its arm, and an arm that hits the cap stops and reads NOT MEASURED.
  - A missing usage is charged at its reserve. Concurrency is 8.
  - The bound holds only if the provider counts at most one token per byte and honours the output cap. If an answer's reported cost
    passes its reserve, the probe's transport guard (`BreachGuard`) stops every later attempt at once. Attempts already in flight,
    at most 8, finish. The ledger is read after the arm, and either finding stops the probe as a breach.
  - `test_probe.py` sets a charge above the reserve but below the cap. With the guard, at most 8 calls go. Without it about 19 go:
    the mutant fails the test.
  - So under a breach the spend can pass the cap by at most the in-flight attempts' excess. It is not a hard guarantee.
- **Expected cost.** By the stored sends' tokens (about 4,950 in and 1,590 out a request at `model.PRICES`), about $0.07 an arm and
  $0.15 in all, within D439 (about $26.07 used of $40).
  - The sum of one worst-case reserve per send is $1.12. So the $0.50 of caps bounds the spend, but it does not guarantee that the
    probe completes.
- **Preflight, run** (`preflight-output.txt`). On the fortnight's ladder archive it judged 0 extraction rows (sections A and B: the
  archive holds none), 170 matching records of its default ledger, and 43 schema enum values. It exits "UNEXERCISED: a check judged no
  case": unexercised, not passed (and its matching section skipped 2 records whose requests are not in that archive). It does not cover
  the ladder step. The ladder step's replay is the check above: the 17 stored answers that wrote answer choices, all accepted; the
  eighteenth stored send was a refusal, which the replay does not judge. The other
  two runs keep only outcomes in their Stage A folders, with no archive, so preflight has nothing of theirs to read.
- **Gate:** `probe.py send` refuses to run without a check record for these exact arm files and these exact requests.

## Prior decisions

- **D547:** refused "the wording is the description alone"; the direction here is the other one.
- **D558:** deferred a repair until the list had a reader. It has one since D570.
- **D426:** the 44 topics stay untouched.
- **AGENTS §6:** a missing definition goes at its owner (the schema field), with examples from other domains.
- **The council-loop skill:** one lever per arm. The definition goes first; the example only on a council round.

Reversal: nothing in production or in the frozen step changes. The arm is new files beside the frozen ones; it is used only if a fresh
acceptance passes and a decision adopts it.
