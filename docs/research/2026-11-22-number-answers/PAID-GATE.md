# judging-v13 paid gate: plan, harness and reading rule (registered before any send; D725, D729, D730)

**Result (D733): STOP.** All 72 answers were refused, and $0.3677 was spent; see `PAID-GATE-RESULT.md`.

## 1. What is sent

`paid_gate.py plan paid-plan.json` builds 12 requests from the stored runs.

| Unit | Arm | Members | Evidence shown |
|---|---|---|---|
| pair-old-1 (09-20: v4 total, v8 Data Center) | joint; separate-v4; separate-v8 | both; one; one | the union of both stored requests' evidence in view (237 items), in every arm |
| pair-old-2 (v14, v9) | joint; separate-v14; separate-v9 | as above | 237 |
| pair-old-3 (v3, v35) | joint; separate-v3; separate-v35 | as above | 260 |
| single-O (old-2 v29, equity commitments) | single | v29 | its own request's (35) |
| single-S (old-2 v6, four hyperscalers' 2027 capex) | single | v6 | 31 |
| single-E (old-3 v41, FY2028 Vera CPU) | single | v41 | 15 |

- **Each request:** judging-v13's system text (`judging-v13-draft.txt`, 4,373 characters); the family header with the exact outcome
  keys; the evidence; the themes once. No earlier forecast is shown (D728). The strict v13 schema.
- **The model:** poc-v118's re-judging setting (gpt-6-luna, medium effort, 16,000 output tokens).
- **Draws:** three per request, so 36 first attempts.
- **Retry:** a calculation the checks refuse, or a schema-invalid answer, is retried once with the reasons. A second refusal makes the
  unit unresolved.
- **What is scored:** the first attempt, on both arms (§3f). Retries are sent and recorded for diagnosis only.
- **The separate arm:** its two first answers per pair and draw are merged and checked over the pair's family (C3, C4 across the two).

## 2. Spend and stops

- **The ledger:** one, at Alex's ceiling (`paid_gate.py send <folder> <ceiling> paid-plan.json` refuses any other ceiling).
- **Budget:** the real budget transport and stop gate, which reserve each request's worst case before sending. After a stop, nothing
  more is sent, and the remaining units are recorded as not sent.
- **Estimate** (at `hivemind.model.PRICES`: gpt-6-luna, $0.10 input and $0.50 output per million tokens; tokens estimated as
  characters / 4):
  - a pair request is about 34–38k input tokens and a singleton 6–9k;
  - the 36 first attempts cost about $0.17 at 4,000 output tokens each, and at most $0.39 if every answer used its 16,000-token cap;
  - the transport reserves at most $0.039 for one request.
  - **Proposed ceiling: $0.50.** It covers every scored attempt. Retries come last (§3g), so a ceiling stop among them leaves the
    scored test complete.
- **Sends:** one at a time, every first attempt before any retry (§3g). Each send has its own archive, so no draw is answered from
  another.

## 3. The $0 rehearsal (`paid_rehearsal.py`, `rehearsal.log`: 16 of 16)

- **Clean run:** 36 first attempts, every HTTP body byte-equal to an independently built request, every unit published, the separate
  arm reconciled in 9 of 9, the spend settled under the ceiling.
- **Paths:**
  - a refused calculation is retried, then published;
  - two refusals give unresolved;
  - a schema-invalid answer is retried;
  - two separate answers that each pass alone are refused when reconciled (C3);
  - after a ledger stop, nothing more is sent.
- **Packets:** 27 packets with the arm hidden. The verdict is computed on synthetic readings: both arms good gives STOP (gain under 3);
  a joint gain of 4 gives PASS; one published singleton defect gives STOP; a separate-arm defect alone does not stop; a missing
  reading gives INCOMPLETE.

## 3b. After council round 47 (`codex-r47.md`)

- **[47.1] Reconciliation:** forecasts of the same quantity and scenario with equal recomputed values and bounds are unified before the
  family's checks run. The duplicate's derivation is kept in results. Forecasts that differ stay as a conflict. Rehearsed: an agreeing
  pair passes, and a disagreeing pair is refused (C4).
- **[47.2] One authorization:**
  - `paid-plan.sha256` pins the reviewed plan, and the sender refuses any other plan;
  - `~/.hivemind-keys/v13-paid-gate/authorization.json` is created exclusively at the first send, so a second launch is refused;
  - (unit, arm) pairs are unique.
- **[47.3] Every attempt recorded:**
  - a `started` line is written before the provider is called;
  - checker failures and arithmetic errors are refusals, recorded with the raw answer;
  - every planned unit has a final status (`finals.json`), even after an abort;
  - a refused reservation never reaches the provider.
- **[47.4] Readings validated:** exact packets and cards, two readings (A, B) per card with yes or no and a ground for each question,
  and a third reading on every disagreement. Otherwise the verdict is INCOMPLETE.
- **[47.5] Packets:**
  - the question text and ladder;
  - each passage exactly as the request showed it, including those named only in `rests_on`;
  - declared figures with renumbered ids, the recomputed outcomes and the recorded assumptions;
  - the cards a non-reconciled separate unit has;
  - neutral decision labels.
- **Rehearsal:** 27 of 27 (`rehearsal.log`). The $0 gate still passes (`gate-run27.txt`: 87 of 87), and the mutants are unchanged.

## 3c. After council round 47b (`codex-r47b.md`)

- **[47b.1] Reconciliation:**
  - Two recomputed values are the same when their bounds match and each end agrees within 1e-9 relative. A floating-point copy
    unifies; a real difference stays a conflict.
  - The readers never see the unified calculation. Each card of a reconciled packet is shown with its own original answer.
- **[47b.2] Completeness comes from the attempt records.** `answers.jsonl` is the one record of what happened. For each planned unit
  and draw, the final status is derived from it:
  - no started line: **not sent**;
  - a started line with no finished line: **interrupted**;
  - a first refusal with no retry sent: **retry not sent**;
  - otherwise, the last attempt's decision, and a second refusal is **unresolved**.

  `results.json` is written from these records in a `finally`, so an abort still leaves it. The verdict is INCOMPLETE for every
  status other than published, held or unresolved. That includes a reservation or HTTP failure, recorded as **transport**.
- **[47b.3] Packets:**
  - Every attempt of every card is listed, with neutral labels and check codes only.
  - Each card is its own derivation: the figures its outcome and reference rest on, renumbered F1.. for that card alone.
  - Its recorded assumptions are mapped to the same numbers. A record that names a figure outside the card is left out.
- **[47b.4] Binding:**
  - `packets.md` and the key are each created exclusively, once. A second `packets` call is refused.
  - The key carries the run's digest (`answers.jsonl`, `results.json`, `plan.json`) and the sha256 of `packets.md`.
  - The readings file carries the sha256 of the packets it was read on.
  - The verdict is INCOMPLETE when any of the three differs, or when a ground is not a non-empty string naming a passage (e…) or a
    figure (F…) of that packet.
- **Rehearsal:** 41 of 41 (`rehearsal.log`). The new cases:
  - a floating-point copy unifies;
  - a reconciled card shows its own derivation;
  - every attempt is listed;
  - a transport failure makes the verdict INCOMPLETE;
  - an interruption during a retry leaves results, marks the unit interrupted and the rest not sent;
  - a retry that was never sent is incomplete;
  - the card view maps assumption records and leaves out other cards';
  - a second packets run, readings made on other packets, a run changed after freezing, and null or foreign grounds are each refused
    or INCOMPLETE.
- **Mutants:** 13 of 13 caught, and the control passes (`paid_mutants.py`, `paid-mutants.log`). Each mutant breaks one of these
  defences on a scratch copy. The plan is unchanged (sha256 `6f81dae5…`), and `calc_check.py` is unchanged since gate run 27.

## 3d. After council round 47c (`codex-r47c.md`)

- **[47c.1] Reconciliation, by the joint arm's rule:**
  - Only a forecast of a declared shared quantity is unified, and only with the other call's forecast of the same quantity and
    scenario when their values are the same.
  - Duplicates inside one call are never unified, so C3 and C4 judge them as they judge a joint answer.
- **[47c.2] The key only orders the packets.**
  - Each packet's decision, cards and allowed grounds come from the run.
  - The verdict renders all packets again from the run and the key's order, and requires the text to equal `packets.md`, the key's
    sha256 and the readings' sha256.
  - The key must map exactly one packet to each unit of the run. A decision written into the key is ignored.
- **[47c.3] Abstentions and attempts:**
  - Each card is labelled K1, K2, … and is itself a valid ground, so a no-figure abstention can be read.
  - Every earlier attempt shows its own answer, with figures named T<n>.F…. An attempt with no parsed answer shows its recorded
    failure as a neutral label.
  - Check codes are not shown: a cross-member code (C3, or C4 across members) occurs only in a joint answer and would reveal the arm.
    The reasons stay in `results.json`.
- **[47c.4] A torn journal:**
  - A line that does not parse is skipped and listed as damaged. Its attempt counts as unfinished.
  - `paid_gate.py recover <folder>` rebuilds `results.json` read-only and sends nothing.
  - The verdict is INCOMPLETE while any line is damaged.
- **Rehearsal:** 48 of 48, three times (`rehearsal.log`). The new cases:
  - two equal forecasts inside one answer, and two equal shared forecasts inside one call, are both refused after reconciliation, as
    in a joint answer;
  - an abstention reads with K1 as its ground;
  - earlier attempts show their answers, with no codes;
  - a key that maps packets to other units is INCOMPLETE;
  - a decision written into the key changes nothing;
  - a torn journal recovers with 35 units published and the torn one interrupted, and its verdict is INCOMPLETE.
- **A rehearsal fault found and traced:** one parallel control run failed 47 of 48.
  - The swap test exchanged P01 and P02. In about 2 of 26 shuffles, these are two draws of the same unit and arm.
  - The rehearsal's draws answer alike, so their text is identical and the swap changes nothing.
  - That is harmless to the verdict, which counts by unit, not by draw. The test now swaps two different units.
- **Mutants:** 19 of 19 caught, and the control passes (`paid-mutants.log`).
  - Three missed in the first run and were traced:
    - one was stale, because packets now render from the attempts;
    - one was masked by the shared-only filter, and a shared within-call case was added;
    - one disabled only half a condition.
  - One mutant is equivalent and is left out: unifying any key across calls, not only declared shared ones. C3 looks only at
    forecasts reachable from each member's own outcome, so the result does not change.

## 3e. After council round 47d (`codex-r47d.md`): three structural rules

Rounds 47b to 47d kept finding the same two things: process information inside the readers' packets, and a mapping from packets to
units that could change after reading. These findings were answered by rule, not one by one.

1. **The scoring text holds only what the four questions need.** For each card: the question, the ladder, the passages it names,
   its own figures, the recomputed outcome, the recorded assumptions and the card. It carries no attempt history, no code decision
   and no check code. The verdict applies the code's decision itself.
   - Earlier attempts go to `attempts.md`. That file is for diagnostic reading only and is never scored. Each attempt sits under its
     own shuffled label (D01, …), with no link to a packet. [47d.3]
   - A card with no final answer says why in plain words: no request was sent; the request was started and no answer was recorded;
     no answer arrived; the answer was refused and its retry was not sent; or the answer did not match the format. [47d.4]
2. **The text the readers receive commits to the mapping.** The key is {a random salt, the run's digest, the packet order, the
   attempt labels}. Its sha256 is the first line of `packets.md`. The verdict refuses a key whose sha256 differs from that line. It
   also renders the packets again from the run and the key, and refuses a mismatch with `packets.md` or with the readings' sha256.
   A swap of two packets with identical text is caught, and so is a decision written into the key. [47d.1]
3. **Reconciliation is one to one.** A declared shared forecast is unified only when each of the two calls holds exactly one
   candidate for that quantity and scenario, and their values are the same. Otherwise every copy stays, for C3 and C4 to judge as in a
   joint answer. [47d.2]

- **The record:** an attempt that was started and not finished is kept in `results.json` as interrupted.
- **Rehearsal:** 51 of 51, three times (`rehearsal.log`). The new cases:
  - the scoring text has no attempt, decision or code;
  - the refused first answer appears only in `attempts.md`;
  - a swap of identical-text packets is INCOMPLETE;
  - a forged key is INCOMPLETE;
  - two equal shared forecasts in the second call are refused (C4, three nodes);
  - an interrupted card says the request was started.
- **Mutants:** 20 of 20 caught, and the control passes (`paid-mutants.log`).

## 3f. After council round 47e (`codex-r47e.md`)

- **[47e.1] The first attempt is scored, on both arms.**
  - In the joint arm, a cross-card conflict (C3) is refused and retried with its reason, so the retry can repair it. In the separate
    arm, the same conflict appears only when the two answers are reconciled, after both calls are over, and there is no retry.
  - Scoring the final answers would credit the joint arm with a second chance the separate arm cannot have.
  - D725 registered both arms "under the same format and checks" and says nothing about retries. Its pass and stop lines stay as
    written and are applied to the first attempts.
  - Retries are still sent and read for diagnosis (`attempts.md`), and are not counted.
  - Rehearsed: the joint pair is published after its retry, but its refused first attempt is scored, so both arms come out at 6.
- **[47e.2] One unit.** A shared forecast is unified only when the two copies have the same unit, as well as the same value and bounds.
  Rehearsed: 110 USD bn against 110 USD is refused (C4).
- **[47e.3] Every returned text is readable.**
  - When the format check fails an answer, the scoring packet keeps its neutral label.
  - The text the model returned, and the passages it names, go to `attempts.md` under a blind label. This covers both a first attempt
    and a final one that fails the format.
- **[47e.4] One verdict per run.**
  - `verdict` copies the readings into the run once (`readings.json`, created exclusively).
  - It scores them and writes `verdict.json` once, holding the readings' sha256, the key commitment, the packets' sha256, the run digest
    and the result.
  - A second verdict on the run is refused. `paid_gate.py replay` recomputes from the sealed readings and must reproduce the result.
  - Rehearsed: the second verdict is refused; replay reproduces the result; after the sealed readings are edited, replay fails.
- **Rehearsal:** 55 of 55, run three times (`rehearsal.log`).
- **Mutants:** 25 of 25 caught, and the control passes (`paid-mutants.log`).
  - Two obsolete mutants were repointed or removed.
  - One mutant crashed on a missing file and not on the defence. The test was corrected, and the mutant now fails the right check.

## 3g. After council round 47f (`codex-r47f.md`)

- **[47f.1] Retries cannot decide whether the scored test is complete.**
  - The run sends every first attempt (all 36) before any retry.
  - Completeness is judged on the first attempts: each must end published, held or refused.
  - A retry that fails in transport, is interrupted or is never sent stays in the diagnostic record.
  - Rehearsed: an interruption during a retry leaves all 36 scored attempts and a complete verdict. A transport failure on a retry
    leaves the verdict complete. An interruption during a scored attempt makes the verdict INCOMPLETE. In the journal, every first
    attempt comes before every retry.
- **[47f.2] Every returned text survives.**
  - The record keeps the provider's whole response, as the archive stores it, with no 20,000-character cut.
  - A null content is shown as the model's refusal, or as "no text returned".
  - Both files are rendered before anything is written, and a failed render leaves no files.
  - Rehearsed: a refusal with null content, a 25,000-character malformed answer whose passage is named at its end, and a render that
    fails and then succeeds.
- **Rehearsal:** 61 of 61, three runs (`rehearsal.log`).
- **Mutants:** 30 of 30 caught, and the control passes (`paid-mutants.log`). Two mutants are caught by the crash the defence prevents:
  - without the interrupted branch, the summary fails on an unfinished attempt;
  - passing a null content on, packet rendering fails.

## 3h. After council round 47g (`codex-r47g.md`)

- **[47g] Two journals, read on the writer's own delimiter.**
  - Scored first attempts are written to `answers.jsonl`, and diagnostic retries to `retries.jsonl`. The run digest covers both.
  - A damaged line in `answers.jsonl` makes the verdict INCOMPLETE. A damaged line in `retries.jsonl` is reported and marks that retry
    interrupted, but leaves the scored test complete.
  - Records are split on '\n' only, the writer's delimiter. An answer may contain other Unicode line separators (U+2028, U+0085,
    U+2029), and these are kept inside the record.
  - Rehearsed: a torn retry record leaves the verdict complete; a torn scored record (the existing control) makes it INCOMPLETE; an
    answer holding U+2028, U+0085 and U+2029 stays one record; the order of every first attempt before any retry is checked on the
    provider's own call sequence.
- **Rehearsal:** 63 of 63, three runs (`rehearsal.log`).
- **Mutants:** 33 of 33 caught, and the control passes (`paid-mutants.log`).
  - One mutant (splitting on any line break) is caught when a scenario guard stops the rehearsal: 36 attempts started, 35 finished.
  - The mutant harness now counts such a stop as a catch and shows its reason.

## 4. The reading rule (fixed now, before any answer exists)

- **Packets:** 27 (`paid_gate.py packets`): 9 joint pair-draws, 9 reconciled separate pair-draws and 9 singleton draws. The labels are
  shuffled, the arm is hidden, and the key is kept in `~/.hivemind-keys/v13-paid-gate/`.
  - Each packet shows, per card (K1, K2), the question, the ladder, every passage the final answer names (as the request showed it),
    its figures, the recomputed outcome, the recorded assumptions and the card. Nothing about attempts or the code's decision is
    shown (§3e).
  - A packet the code did not publish (held, unresolved, not reconciled) is read too. The verdict, not the reader, applies the code's
    decision: its cards cannot count as usable.
  - The readers receive `packets.md` exactly, with its key-commitment line. The readings file carries that text's sha256.
- **Readers:** two fresh readers of different families, a Codex session and a Claude subagent, each blind to the other and to the arm.
  For each card each answers four questions, yes or no, with the passage that decides:
  1. **usable:** the outcome is usable and supported by the shown passages it rests on;
  2. **contradiction:** with the other card of its packet, it states a hard numerical contradiction;
  3. **internal_reference:** the system's own forecast is presented as the market's expectation;
  4. **deciding_gap:** an unresolved overlap, a change of scope or an unsized adjustment decides its band.
- **Agreement:** where the two readers agree, that is the reading. Where they disagree, a third fresh reader (Codex) reads the card with
  both readings and the passages, and its answer decides. No reading is changed after the verdict is computed.
- **Verdict** (`paid_gate.py verdict`, D725's lines, on the first attempts; computed once and sealed, §3f):
  - **PASS:** the joint arm has both cards usable in at least 8 of 9 pairs, at least 2 of 3 per snapshot, and at least 3 more usable
    pairs than the separate arm; and zero published defects (contradiction, internal reference or deciding gap) across the joint and
    singleton answers.
  - **STOP:** any such published defect; a coverage line missed; a gain under 3.
  - **INCOMPLETE:** a packet or a card missing a reading, or a unit not sent.
  - This is a small design test, not release acceptance.

## 5. What the result decides

- **PASS:** judging-v13 earns a production design: automatic families in matching, lifecycle and the request builder, each a further
  step Alex opens.
- **STOP or INCOMPLETE:** the line goes back to Alex with the readings, and nothing is tuned on these 36 answers.

## D753. The one-time v13s re-send (Alex: "破例一次，付费重发"), prepared before any answer exists

- **The plan.** `paid-plan-v13s.json`, pinned `0dc7c310…` in `paid-plan-v13s.sha256`. It holds 12 requests × 3 draws = 36 first
  attempts. Every request's system text is the registered D751 request (`080a0012…`). The cases are unchanged: three pairs, then O,
  S (CY2027) and E.
- **The cap.** $0.50 in total, diagnostic retries included (D732 and D753).
- **Authorization.** One-time, at `~/.hivemind-keys/v13s-paid-gate/authorization.json`. The spent v13 authorization and the v13 pin
  are unchanged. `send()` picks the pin and the authorization by the plan's format and refuses a mixed plan.
- **Checked at $0,** with a stub gate and scratch key paths:
  - an altered plan is refused, and so is a wrong ceiling;
  - the pinned plan passes;
  - a second use of the authorization is refused, and so is the spent v13 plan.
- **Changes from council round 70** (`codex-r70.md`), made before the send. The verdict lines, the four questions and the
  third-reader rule are unchanged.
  1. **The card renderer** (`card_view`, `normalise`) now shows:
     - every figure and passage the card's prose names, with the figures they rest on;
     - a written range such as e5399–e5404 in full, with no width limit (council 70b);
     - every passage in the card's `pushes` (council 70b: an unresolved E card had hidden 6 of the 15 passages it weighed). Figure ids inside the prose (reasons, why, basis_text) are
     renumbered with the figures, so a prose reference points to the figure the writer meant.
     - Checked at $0 on 20 stored v13s answers (D749–D751 and two controls): no dangling figure or passage reference, and every
       shown value equal to the writer's.
     - The re-check after council 70b covered every passage the answer names at card level (cites, pushes and prose, ranges
       expanded). Missing: 0 of 20. Each unresolved card shows all 15 of its passages.
  2. **The reader brief** is `reader-brief-v13s.md`. It is the v13 brief with Alex's two rulings, the same words for both readers and
     the third reader:
     - `usable` accepts an explained related figure (D747) and a "can't tell yet" that weighs the evidence, gives the target as
       context and names the deciding fact (D753);
     - `deciding_gap` is yes for a published number whose band an unsized adjustment determines, and no for a "can't tell yet".
  3. **The exact file.** Readers receive the exact `packets.md` (`assemble_readings.py split-exact`; `third-exact` for the third
     reader), with their packet ids named separately, so the sha256 the readings carry is the text they read.
  4. **The launch.** It runs from the repository root, detached, with the log and pid outside the run folder:
     `python3 docs/research/2026-11-22-number-answers/paid_gate.py send poc/data/judging-v13s-paid-2026-11-23 0.5
     docs/research/2026-11-22-number-answers/paid-plan-v13s.json`.
     - All 36 scored attempts precede any diagnostic retry.
     - A terminal transport failure on a first attempt makes the result INCOMPLETE.
- **Re-checked after the changes:** rehearsal 19 of 19, paid mutants 33 of 33 with the control passing, cases 111 of 111, and the plan
  pin unchanged.
