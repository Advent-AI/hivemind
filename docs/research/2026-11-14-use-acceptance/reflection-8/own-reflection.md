# Own reflection before the deep council (Claude, 2026-11-17). Written before reading any cold review.

Alex, 2026-11-17: "你深度的跑council loop 来所有的trace还有决策自行battle当前的状态是什么，以及应该做什么下一步，不要scope drift 了。这次要完整的思考不要漏掉细节和log".

## 1. Goal and scope

**The goal.** The new system replaces the running pipeline only after five gates, in order (clean PRD §1.5, D548):
1. the ladder step against Alex's six lines (D400);
2. the judge on the system's own questions (D428);
3. end to end against the running pipeline (D427, D431);
4. use on unseen news (D484; its lines are proposed, not his);
5. integration and release.

**This round's scope.** Gate 1 is the live front, with what gate 2 needs from it.

**Out of scope:**
- clean Steps 1 to 3 (c8 is in force; Step 2 is frozen, D427);
- the frozen ruler;
- the frozen judge's internals;
- the product pages;
- the live-service design.

Note: AGENTS still names `docs/prd/10-filing-phase.md` as "the current phase". That phase closed with poc-v116/v118 (D366, D370). The clean path is
governed by `clean-arch/PRD.md`. The pointer is stale; it is a wording fix, and it is not touched in this round.

## 2. The state, by evidence

### 2.1 The model (Alex's choice, D648: astra)

**Three-draw screens on the 26 topics outside the 44**, failed sends on lines 1 to 4 (D628 to D634):

| Model | Failed sends |
|---|---|
| luna | 13 of 78 |
| sol | 9 of 78 (5 of 78 in D629's counting) |
| astra | 4 of 78, all declines on topics that name several things |

**One-draw trials** (D647, D650):
- Opus: agreed failures 1 against luna's 7, but the families split (Codex 7 against 7, Claude 1 against 9).
- DeepSeek V4.1 Flash: 3 against luna's 1.
- luna's own agreed count moved from 7 to 1 between two draws on the same 26 topics. One 26-topic draw cannot rank models.

**Cost, measured a topic:**

| Model | Cost |
|---|---|
| luna | about $0.001 |
| DeepSeek Flash | $0.008 |
| astra | $0.036 |
| Opus | $0.058 |

**At scale:** astra's ladder step is about $0.05 to $0.10 a day per NVDA-like asset. Reading articles costs about $0.18 a day per asset; that is
the larger cost (`poc/data/clean-e2e-full-2026-11-13/spend-by-component.json`).

### 2.2 Gate 1 with astra on the frozen request (D649)

Read with the fourth Stage A's procedure.

| Line | astra (this run) | luna (run 4) |
|---|---|---|
| 1 | met | missed (1 to 5) |
| 2 | met, or missed by 1 | met |
| 3 | met | missed (2 to 4) |
| 4 | **missed by 7** | missed (3) |
| 5 | 40 of 44, or 35 of 44 with 26 written, below 28 | 40, or 34 |
| 6 | met | met |

- **Line 4's seven misses are one class:**
  - acc/clean-9 ×3: the chip total plus its AI part;
  - acc/clean-8 ×3: HBM shipments plus "still short of demand";
  - u3/clean-10 ×1: capacity plus timing.
- **Alex already ruled this exact class** (D436, verified in `docs/DECISIONS-log.md` line 4847): "a second side of the same bet (the shortage beside the
  shipments, the AI-chip share beside the chip total, the capacity keeping pace beside the demand) is one question; it stays as context in that question
  and is shown as not judged". The frozen ladder request (2026-11-10, D426) predates D436 and never carried it. **The declines contradict his ruling.**
  Writing it into the request implements his decision. It is not a new rule.
- **The 20 unresolved points:**
  - 14 are one question: the due day of an obligation's year-end balance (supply, equity and credit commitments). The Codex third reader says "the next
    annual report, which the fiscal-year note places around 2027-02"; the Claude third reader says "code's day, 2027-04-01, 60 days after FY end".
  - The instrument holds both sources:
    - the reader brief's D mark: a figure without a stated day takes code's day, fiscal year-end plus 60 days (D414);
    - the same mark's last sentence: "an obligation already taken on is due at its next annual filing", with no day given;
    - the request's own fiscal-year note: "FY2027's full-year figures are published in the annual report around 2027-02; use that day as the due date".
  - So the split comes from the instrument, not from astra.
  - In the product, code sets the day (D414), so the question resolves on 2027-04-01, after the filing either way.
  - **If the points resolve as D414 reads,** line 5 is met (40 of 44, 31 written) and line 2 hinges on one point (u3/clean-11 pass 2). Gate 1 would then
    rest on line 4 alone.

### 2.3 The D436 diagnostic (D651, D652)

- **The edit:** D436's two sentences, with no examples.
- **pool-7** (a main figure plus a condition) recovered cleanly: 0 of 2 before, 2 of 2 sound after.
- **pool-17** (a total plus its part) stayed declined, and both families mark those declines unjustified.
- **No harm** on 9 other topics.
- **The verdict:** INCONCLUSIVE by the pre-set rule, with 2 targets exercised. The outside pool has almost no "total plus part" topics; pool-17 is the
  only one both classifiers agree on.

### 2.4 Gate 2 and beyond

- **Gate 2 is not met** (STAGE_B_RESULT):
  - the unsupported-answer lines were met;
  - controls are unexercised, 4 comparable of 8 needed;
  - the strictest last-answer reading missed, 3 of 24.
  - Re-sending the judge cannot close the control shortfall. "A new reference set would be your choice" (D576, D592).
  - It was measured on luna's questions. With astra writing the questions, gate 2 must be re-measured.
- **Gates 3 to 5:** owed, proposed, and partly built.

### 2.5 Alex's open decisions that touch gate 1 or 2

- D591, a postponement: "ruled out" or "still open". The council decided reversibly: ruled out.
- D631, which part is the question when an outcome names several. D436 answers the second-side subset.
- D403/D414, the wording of the obligation due day.
- D592, a reference set for gate 2's controls.
- Deck 1 marks; the role of the six lines; choices 3 to 6 of the decision page.

## 3. Process errors today, to log

1. **A cap below the attempts in flight:** made twice (sol earlier; luna in D646 run-1). The trial scripts now refuse it in `check`. Every new
   harness must copy that check.
2. **A patched function calling itself:** made twice (A2 in D639; the D651 diagnostic). Hold the original before re-pointing it.
3. **Opus priced from its list price:** off by about two times, because Claude counts about 68% more input tokens. Price a new model from one measured
   send.
4. **A memory file corrupted:** an index was computed before a replace. Repaired.
5. **A2's examples nearly reused:** they mirror two of the 44. Caught by reading, and dropped.
6. **One-draw model comparisons:** two were run (Opus, DeepSeek). After D650 they cannot decide a model choice.

## 4. What blocks production, by impact

1. **Gate 1:**
   - line 4, the second-side class, part of which (a total plus its part) is not yet fixed by any tested text;
   - the instrument's own due-day split, which decides lines 2 and 5.
2. **Gate 2:**
   - the structural control shortfall, which waits on Alex's choice (D592);
   - a re-measurement on astra's questions.
3. **Gate 3:** owed, and "beats" has no number.

## 5. My candidate next step, for the council to attack

1. **First, at $0: settle the instrument's due-day split.**
   - Re-read the 14 points with fresh third readers of both families, given the brief alone, as D568 and D569 did.
   - If both apply D414, the points resolve.
   - **Falsifier:** fresh readers still split. Then it goes to Alex as one wording question: an obligation's year-end balance is due at code's day, or at
     the filing.
2. **Second:** the request change implementing D436 in full.
   - D436's two sentences, plus one example clause for a part of a total, from other industries.
   - It is audited at $0 against the whole request and against the 44 for leakage.
   - **The test:** the outside check is thin (pool-17, maybe week-10-06 clean-2), so it is labelled a diagnostic. Its falsifier: no control flips and
     pool-17 recovers in both sends.
3. **Third:** gate 1 on the 44 with the changed request, about $5.
   - It is reported as an exposed set, both countings.
   - **Predicted:** line 4 at 0 or 1; lines 1, 3 and 6 still met.
   - **Falsifier:** line 4 misses by 2 or more, or line 1 or 3 regresses.
4. **Alex only:** D592's reference set, without which gate 2 cannot pass even with good questions.
