# The prompt audit after A2's measurement (AGENTS §6; `.claude/skills/prompt-audit`), 2026-11-16

**Scope:** every sentence of A2's request that decides what goes into `not_judged`, read against the decisions. Failure classes come
from `OVERLIST-AUDIT.md`, `RESULT-A2.md` and the model's account (`listing-accounts-output.txt`). A blind second reader (a fresh
read-only Codex session, without this table) read the same request; its verdicts are in `prompt-audit-a3-blind.md` and compared below.

## 1. The sentences, in the order the model reads them

| # | Where | Sentence (quoted) | Source | Verdict |
|---|---|---|---|---|
| 1 | system line 5 | "Judge the one the topic's outcome names as what is tracked. List every other part of the topic's description and outcome that the question leaves out, a second figure or event, a condition or a comparison, in not_judged" | D397 | consistent, but **abstract on its edge**: nothing says what "the question leaves out" means when the answer choices themselves decide a part |
| 2 | system line 5 | "A second side of the same bet … stays in the one question as context: list it in not_judged" | D436 | consistent |
| 3 | system line 13 | "A difference inside an outcome, such as an approval with conditions against one without, is not an outcome of its own; when the topic's description or outcome names it, list it in not_judged" | D409 ("finer differences are listed as not judged") | consistent. It is the grouped-choice case: a finer case inside a choice stays listed |
| 4 | system line 13 | the merger example: "ruled_out, by_whom the regulator or the parties … the regulator blocks the merger or the parties withdraw the filing" | D409, D420 | consistent. It shows a grouped Ruled out, so by sentence 3 "blocked by the regulator" stays listed |
| 5 | schema, `not_judged` | "Every other part of the topic's description and outcome that the question leaves out (a second figure or event, a condition, a comparison); empty only when the question leaves nothing of either out" | D397 | same edge as 1 |
| 6 | closing check | "is every other part of the topic's description and outcome listed in not_judged?" | D397 | **missing the other direction.** It asks only whether something is missing from the list, never whether a listed entry is already decided |
| — | nowhere | material the answer will be read from ("as reflected in …", "checked at …") | no decision | **missing**: nothing decides it, so the model guesses |

## 2. Failure classes mapped to the sentences

| Class (A2, both arms' entries) | Sentence | Verdict | The model's account |
|---|---|---|---|
| an outcome the choices decide is listed (5 of 137 entries; control 1 of 71) | 1, 5, 6 | missing (the reverse check) | "Formal termination is covered by 'ruled_out', but the ladder does not separately judge termination as an event"; it lists by "the instruction says to list other conditions the question leaves out" |
| the material the answer is read from is listed (4 of 137; control 0) | none | missing (no decision) | "revenue is a separate measure from shipment count" |

## 3. What A3 changes, and what it leaves

- **One lever:** sentence 6 gains the reverse check, with the test of sentences 3 and 4 kept: *"Then read each entry of not_judged
  against your answer choices: remove an entry only when, whichever choice holds, that choice says whether the entry happened; keep any
  part of an entry that some choice leaves unsettled."* About 210 characters, no example.
- **Left as it stands:** the source-material class.
  - No decision covers it.
  - The census of the 66 stored topics finds no topic where a disclosure is itself a side part: all twelve mentions of a disclosure,
    filing or report are the main event, the main figure's source or the settlement route. So the narrow "only the source" reading
    cannot be tested on stored material.
  - It stays a reported residual (4 entries in A2), and it is not changed.
- **Contradiction check:**
  - The added sentence removes only what every choice settles.
  - Sentence 3 keeps a finer case that a grouped choice leaves unsettled, so the two agree.
  - Nothing in the request asks to list a decided outcome.

## 4. The blind reader (`prompt-audit-a3-blind.md`) against this table

- **Agrees:**
  - sentences 1 to 5 are consistent with D397, D409 and D436;
  - the request leaves undecided whether an entry the choices settle is "left out".
- **Adds:**
  - the closing check omits "that the question leaves out", so it is wider than the schema;
  - a check written for every shape would remove, from a figure, a comparison with a level or a second side that the ranges happen
    to settle (its examples: output against last year's level, capacity against demand). D397 and D436 keep those visible.
- **Taken:** A3's sentence is limited to an event. The figure case is the disputed kind and stays untouched (DECLINE-AUDIT §5).
- **Not taken:** the closing check's missing "that the question leaves out". Changing it would be a second lever. It is noted for a
  later arm.

## 5. The whole request, after round 84: every failure class of A2's measurement

The request as sent: system (9,978 characters), user payload (10,369: company, fiscal-year note, topic, item, themes, then the closing
check), schema, settings. One row per class; the blind whole-request reader's verdicts are in §6.

| Class | Sentence(s), quoted, with location | Decision | Verdict | In A3? |
|---|---|---|---|---|
| H, decided outcomes listed | system line 5 "List every other part … that the question leaves out"; schema `not_judged` "that the question leaves out"; closing "is every other part of the topic's description and outcome listed in not_judged?" (without "that the question leaves out") | D397, D409 | **missing** (no reverse check). The closing check is **wider** than the schema (blind reader) | yes |
| H, the source material listed | none | none | **missing** (no decision) | no: reported residual |
| Y, FY2028 for calendar 2027 | system line 14 "the one year it covers (written FY2027 for a company's figure, which uses its fiscal year …)"; schema `figure/year` "Code refuses the other form"; line 21 "Company figures use the company's fiscal year"; line 6 lets "one fiscal or calendar year" through | none on a company's calendar-year figure | **contradiction**: line 6 accepts a calendar year that lines 14 and 21 and the code cannot write for a company | no: standing (control's sends too) |
| XR, a CEO's stated pace not carried | system line 16 "Its kind is expected when the item states what the market expects: a consensus, the company's guidance, the stated plan or deadline" | D413-era reference rule (frozen ladder) | **abstract**: whether a chief executive's description of an industry pace is "what the market expects" is not decided | no: standing |
| W, settling material after the due day | system line 20 "on or after the day the material that settles the question is published"; line 22 "period_end when it is the last day of the period the topic names" | frozen ladder | **contradiction** for an event settled by an annual report: line 22 puts the due day at the period's end, line 20 after the report | no: standing |
| N, declining with a main part | system line 6 and A2's clause | D397, D436, D417 | consistent after A2; no N failure on the motivating topics | — |

**The interaction the blind reader found:** the closing check asks for every other part, and A3 removes some of them.
- **The fix:** A3's sentence is written as the definition of "left out" in the schema's own words. "Every other part" then means
  every part the question leaves out, and the two sentences no longer pull opposite ways.
- **The sentence (v6):**
  > *For an event, an entry is not a part the question leaves out when, whichever outcome holds, that outcome says whether it
  > happened: remove it, and keep any part of an entry that some outcome leaves unsettled.*

**Second sides of an event (D436), checked:**
- A second side that is itself an event is never settled by the main event's outcomes, so the sentence keeps it. For example, on the
  stored export topic the main event is the approval of the newer chip. "Chinese restrictions on H200 shipments" is not decided by
  that approval holding, being ruled out or staying open.
- A figure beside an event is not settled either, for example the scale of the permitted purchases.
- The sentence removes only the main event's own alternatives.

**Standing faults (Y, XR, W):** each is one class for a later arm, one at a time (AGENTS §7.3). None is touched here.

## 6. The blind whole-request reader (`prompt-audit-a3-blind-whole.md`) against §5

| Class | Mine | Blind reader | Settled |
|---|---|---|---|
| H | missing (no reverse check); the closing check is wider | contradiction: "every other part" against the outcomes that already account for delay and termination; it also notes that the payload's `settled_by` names the checking documents | the same mechanism. A3 answers the decided-outcome half. The `settled_by` field is the request's own name for the source material, so it is a possible anchor for the residual class later. It is not used now: one lever |
| Y | contradiction | contradiction; D437 does not let the period the topic names be replaced | agreed; standing |
| XR | abstract | abstract; also, the closing check never asks whether a stated reference was left out | agreed; standing |
| W | contradiction (line 20 against line 22) | missing (no example that an annual report comes after the fiscal year-end); a plausible gap, not proven | the two labels name one gap; standing |
| N | consistent after A2 | abstract: nothing says how to choose the main part when several compete | taken as abstract. A2's motivating topics had no N failure, and DECLINE-AUDIT §3's rule is not written in any arm. Recorded for a later class |
| other | — | the 548-day cap can fall before the next annual filing; the fiscal-year note's "use that day as the due date" can conflict with another period | standing; recorded, not touched |

No class the blind reader found contradicts A3's sentence. Its H reading supports making the sentence the definition of "left out"
(§5).

## 7. Clause by clause: the whole request with A3's sentence (version 7), after round 85

**The sentence, now a closed set** (round 85: a separate event that follows logically from every outcome, such as a payment due
automatically at closing, is a second side D436 keeps visible, and "whichever outcome holds" would remove it):

> *For an event, an entry that only restates whether the event itself happens, is ruled out or has not happened by the due day is not
> a part the question leaves out: remove it. Keep every other entry, including a separate matter that would follow from one of those
> outcomes and a finer case inside one of them.*

| Entry (from the stored sends or the council) | Outcomes | Sentence |
|---|---|---|
| "A delay past March 24, 2028" | acquisition: closed / the parties terminate / neither | removed: it restates "has not happened by the due day" |
| "Termination of the acquisition" | Ruled out = the parties terminate | removed: it restates "is ruled out" |
| "Whether MIIT blocks or delays the purchases" | Ruled out = MIIT denies | removed: it restates two outcomes |
| "A payment due automatically at closing" | acquisition | kept: a separate matter that follows from an outcome (D436) |
| "Blocked by the regulator" | Ruled out = the regulator blocks or the parties withdraw | kept: a finer case inside an outcome (D409, line 13) |
| "Whether the acquisition is repriced"; "a cap on the chips approved" | — | kept: a separate matter; a finer case (line 13's own example) |
| "Chinese restrictions on H200 shipments" | the newer chip's approval | kept: a second side (D436) |

**The whole request** (system lines as numbered in `arm-a2/candidate-system.txt`; the closing check sits at the end of the payload):

| Location | Clause (short) | Source | Verdict |
|---|---|---|---|
| system 1 | the one question the topic is judged on, written once from this item | D397, D398 | consistent |
| system 4 | one figure for a named period or one event; it must decide the outcome on the due date; a figure names its period and settling material | D397, D398 | consistent; "names the period it covers" meets line 14 in **Y** |
| system 5 (arm A) | judge what the outcome names; list every other part left out, "a second figure or event, a condition or a comparison" | D397 | consistent. "A comparison" with the reference is the disputed kind: the decisions do not settle it (DECLINE-AUDIT §5) |
| system 5 (A2) | a second side stays as context and is listed; it is not by itself a reason to decline | D436, D397, D417 | consistent |
| system 5 | never fold two things: the drug and fuel examples | D397 | consistent |
| system 6 | the seven decline cases | D397/D406 (no main part), D403 (date; fiscal year-end for a pending regulatory decision), D417 (not one year), D418 (another company or no theme); the quarter, ended-year and beyond-next-year cases from the ladder design (D398) | consistent; **abstract** on choosing among competing parts (the blind reader's N) |
| system 9 | whose question: company or theme | D418 | consistent |
| system 12 | concrete conditions; no overlap or gap | D398 | consistent |
| system 13 | event: three outcomes, the typed ruling out, the proceeding rule, a finer difference listed, the merger and safety examples | D409, D416, D420 | consistent |
| system 14 | figure: unit, one year in the FY form for a company, five ranges, bounds | D398 | consistent, but **contradicts** line 4 and line 6 for a company's calendar-year figure (**Y**) |
| system 15 | exactly one of event and figure | D409/D398 | consistent |
| system 16 | reference: expected or last reported, the item's exact words, a range carried as a range, the middle range holds it | D398, D405, D411 | consistent; **abstract** for a spoken pace (**XR**) |
| system 17 | favourable end; owed amounts lower unless settled | D398, D413 | consistent |
| system 20 | due day after the item and on or after the settling material | D403 | consistent |
| system 21 | a figure's publication date; fiscal years for company figures | D414 | consistent; **Y** |
| system 22 | an event's due day: stated or the period's end | D403 | consistent with D403; meets line 20 in **W** for an event settled by an annual report |
| system 23 | a binding obligation's due day within 548 days | the ladder design | consistent; the blind reader notes that it can fall before the next annual filing (standing) |
| schema | question, object, figure, unit, year ("Code refuses the other form"), ranges, favourable end and why, reference fields, due-day basis, no_ladder, event fields | the same as the system lines they restate | consistent; year in **Y** |
| schema `not_judged` | every other part the question leaves out | D397 | consistent |
| closing 1 | one thing, and every other part listed | D397 | **keeps wider** than the schema (no "that the question leaves out") |
| closing + A3 | the sentence above | D397, D409, D436 | the closed set narrows closing 1 to the schema's scope, for an event only |
| closing 2–7 | contiguous ranges; event outcomes; reference; due day; owed amounts lower; correct where a check fails | D398, D409, D416, D420, D411, D403, D413 | consistent |
| payload | company, fiscal-year note ("use that day as the due date"), topic (description, outcome, `settled_by`, opens_as), item, themes | D414, the ladder design | consistent; the note can meet a topic's other period (standing). `settled_by` names the settling material (the residual class's possible anchor) |

**Classes left for later, one at a time:** Y (contradiction), XR (abstract), W (a gap between lines 20 and 22), N (abstract), the source
material listed (missing). The blind clause-by-clause reader's table is `prompt-audit-a3-blind-clauses.md`; see §8.

## 8. The blind clause-by-clause reader (`prompt-audit-a3-blind-clauses.md`) against §7

**On A3's sentence.** The reader calls it a contradiction of "every other part" and finds "no explicit source for removing
restatements": D397's literal words can include them, and "D409 itself treats that as an answer outcome".

**The source, in Alex's words (D409, his choice "分三种"):** the option he chose reads:
- "发生了 / 明确落空（被否决、被放弃）/ 到期还没结果";
- "保住了'否决'和'还在等'的区别";
- "更细的区别（如'附条件批准'）列为'不判'".

**What that settles:**
- A ruling out (a rejection or an abandonment) and the wait past the due day are distinctions he kept as the answer, so they are
  judged.
- Only a finer difference is listed as not judged.
- An entry that restates one of the three outcomes is therefore judged, and listing it as not judged contradicts D409. "Every other
  part" in D397 does not reach the judged question's own outcomes.
- The reader's boundary case ("termination" in a topic that contrasts completion with termination) is that case: termination is the
  ruled-out outcome.

**The reader's other findings, on clauses A3 does not change:**

| Finding | Status |
|---|---|
| some frozen clauses cite no decision in D397–D437 (the quarter, ended-year and beyond-next-year declines; a general rule on whose question it is; the figure format; the 548-day cap; settings) | they come from the frozen ladder design (D398 carries D186; D426 freezes the step) and earlier decisions outside that range; recorded, not touched |
| the model's "expected_publication" against D414's code-set day | D414's code overrides the model's day for an estimated year's figure, so the answer cannot carry it; the prompt's wording is a standing mismatch, recorded |
| "the item's own words" is wider than D405's unbroken passage | D405 is enforced by code, which refuses and re-asks; a standing mismatch, recorded |
| the fiscal-year note's "use that day as the due date" | the same as D414's row |

None of these touches the not-judged list. Each is a standing class for a later arm, one at a time.

## 9. After round 86: the complete choices as shown

As the judge is shown it, every Ruled out rung ends "This rung holds when that, or any other decision against the event of rung 1 …"
(item 112 of `reading/readers/packet-6.json`). Ruled out therefore never says which decision it was.
- **What changes:** v7 treated a termination by the parties as a restatement. It is now kept, as a named way of ruling out, which is a
  finer case under D409.
- **What the sentence still removes (v8):** an exact restatement of one outcome. That is the event happening; its being ruled out
  without naming how; or its still being awaited on the due day.
- The worked cases are in `DESIGN-A3.md` v8.

**The first readers marked termination `already_judged`** (A2's H rulings). Under the reading form's own test it is not decided by a
Ruled out that also holds on "any other decision". So the decision counts it both ways, and that disagreement is reported.
