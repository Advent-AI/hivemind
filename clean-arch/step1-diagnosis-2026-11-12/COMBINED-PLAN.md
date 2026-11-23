# One combined Step 1 version (D434), version 4: three candidate changes, a first gate fixed in detail, later gates fixed when reached (2026-11-13)

Alex (D434): "先查完第 1 步其他毛病，再合并改". c8 stays in force (D387, D391). Nothing is built or sent before his word. Version 2 was
reviewed (`clean-arch/step1-unfiled-2026-11-08/council/lr-codex.md`: not ready, chiefly because the second-thing diagnosis was not
finished); it is finished now (`second-thing/RESULT.md`), and every other point is answered below.

## The three defects (each with its evidence and its limits)

**1. The second year of a shared quantity is not opened** (DIAGNOSIS.md; STAGE1-RESULT.md). On the 2026-07-04 article c8 opened the
two years apart in 0 of 9 sends (5 held both years in one thesis, 4 opened one year); c14's two sentences did so in 7 of 9, below its
line of 8. One article, three stored states: the mechanism, not a rate. c14's misses: one year chosen as "the bet", and one send that
opened no capex thesis (defect 2).

**2. The customer sentences can hold back an aggregate of several companies.** c8 line 110: "A customer's deployment plan is evidence
for the company's demand and product theses, unless it changes the company's own cash or credit risk, which is judged as an
obligation"; line 130: "A customer expanding capacity informs demand; it is not a thesis of its own, and not a claim that the supplier
has received orders." My search of every completed c8 call's reasoning (729: d1 243, d2 243, d3 95 + 148 in the continued segment)
for the counterexample cited near a word for several companies found 9 calls (listed with file and step in version 2's table, kept in
`COMBINED-PLAN-v2-census.md`): 8 hold back a single customer or supplier (correct), 1 (draw-d2 step 237, Gulf buyers' combined
spending) holds back an aggregate, mixed with doubts about the item's date and figure. **One found by this search**, not the class's
rate. Under c14 the same sentence removed the capex question in 1 of 9 sends.

**3. Two separate bets in one thesis** (`second-thing/RESULT.md`). Read against their sources by two blind families: 6 of 44 Stage A
theses agreed to hold two bets or no main one (u3/clean-10, acc/clean-10, u3/clean-7, acc/clean-8, acc/clean-9, u1/clean-5), up to 10
with 4 disputes; 6 others carry only a reference, the same event's alternative or context (allowed, D397); the 6 single-question
controls read clean. Step 1's reasoning drafts the outcome as a full description of the article's point ("Either supply or price.
I'll combine"); the schema's `outcome` says only "The outcome or event being tracked by this thesis." The ladder step's faults on the
same event's alternative (u1/clean-6, acc/clean-2) are Step 4's and are not addressed here.

## The three changes (version c15 = c8 with them)

1. **Year boundary** (D38; final wording after the blind read `council/lt-codex.md`): shared_quantity "… evidence for it. The same
   aggregate for this year and for next year is two theses when an analyst would bet on each: another period is not another wording.";
   the closing check "(for a shared quantity, the same aggregate, in any population or wording, and the same calendar year)". Opening
   tests unchanged: a year still opens only when an analyst would bet on it.
2. **The capacity counterexample scoped**, the deployment-plan sentence left as the standard has it (final wording in Gate 1 below).
3. **The `outcome` field's own description** (stopped before any send: `gate1/PREREAD-RESULT.md`), as written for G1-c:
   "The one quantity for one period, or the one event, this thesis tracks. It may name the reference it is measured against, the
   event's own other outcomes (a later date, an abandonment) and context. A second quantity or event an analyst would bet on separately
   is not part of it: it is its own thesis when it is a big matter, otherwise evidence." Sources: c8 section 3 ("one quantity for one
   period, or one event"); D38 ("a question that needs a number and an event is two views"); D397 (extra parts allowed beside the main
   one), which the wording keeps explicitly.

Size and audit: measured on the final c15 text before any send (characters and tokens before and after); the whole-request audit with
a blind second reader (the prompt-audit skill).

## How the plan is staged (a rule adopted after three review rounds raised the later stages each time)

Three reviews (`council/lq`, `lr`, `ls-codex.md`) asked, each time, for more of the later stages' lines and costs. Following AGENTS
§7.3 ("Small first, then one run": a hypothesis is first validated the simplest way, then the full analysis), only **gate 1** is fixed
in detail now. Each later gate's lines and costs are written, reviewed and put to Alex only when the gate before it has passed; a
failed gate stops and goes to Alex. Every change stays a candidate until its gate shows it.

## Gate 1: the smallest proof of each change (for Alex's word now)

Harness: `probe_c14.py` generalised to name the arm (production's adapter, the byte check against every stored sent request including
the acceptance trace, the runner's retry rule, every response kept on arrival). Each arm three sends a state; c8 on every state; every
send read by hand; a control's stop fires when the candidate shows the bad outcome in **more sends than c8 on that state**.
Before any send: the changed requests built and measured (characters and tokens), the whole-request audit with a blind second reader
for each candidate text, and a council read.

**G1-c stopped before any send** (`gate1/PREREAD-RESULT.md`): the two blind source readers agree on no second matter that must
survive. Alex ruled (D436): "算一个题，第三处不改": a second side of the same bet is one question; change 3 is dropped. G1-a and G1-b,
below, test changes 1 and 2, and later gates use c8 with those two only.

**Change 2's wording, final** (after `council/lt-codex.md` and `lu-codex.md`): the deployment-plan sentence stays exactly as c8 and the
standard (line 336) have it; only the counterexample changes: "A customer expanding capacity informs demand; it is not a thesis of its
own, and not a claim that the supplier has received orders; several companies' combined spending is a shared quantity, opened only by
the tests above." (row D, line 279: "几家公司的合计（云厂商资本开支）"). Arms: **c15yc** = c8 + changes 1 and 2 (+332 characters);
**c15c** = c8 + change 2 (+91).

**Decision rules, fixed before any answer is read.**
- *A separated send* (G1-a): its retained new theses include two theses on hyperscalers' combined capital spending, one for 2026 and
  one for 2027, each with kept evidence (read by hand; the harness's year count is a lead only).
- *A control's stop* fires when the candidate shows the bad outcome in more of its sends than c8 shows on the same state; c8's own
  failures are measured, not charged.
- *A failed send* (refused, cut twice, refused by the runner's checks) counts as a send without the passing outcome and without the bad
  outcome.
- *A lost send* (lost to the network, or not sent under the ceiling) is not an answer and is not resent. Any lost send, in either arm,
  makes that state's lines unexercised; any lost send on the capex article makes G1-a unexercised. Unexercised is reported, neither
  passed nor failed.
- *Recorded at 00:59 on 2026-11-13, before any G1-a answer was read:* the first G1-a run lost d1 c8 send 2 to a DNS failure
  ("nodename nor servname provided"), so that run's G1-a is unexercised. After both runs finish, and after a network check, G1-a is
  sent again in full (18 fresh sends, same arms, states and ceiling) into a new folder, and G1-a is judged on that second run only; the
  first run's G1-a answers are kept and reported, not judged. No answer had been read when this was fixed, so the choice cannot select
  on results. If the second run also loses a send, G1-a is reported unexercised and goes to Alex.
- *Recorded on 2026-11-13 after both first runs finished, before the G1-a re-send, and before any answer was read by hand:* the first
  runs lost 3 of 45 attempts to the network (G1-a d1 c8 send 2, DNS; G1-a d2 c15yc send 1 and the Gulf state's c8 send 3, a connection
  cut after one byte). The Gulf state has no line, so G1-b's lines are unaffected. At about 7% a send, 18 sends without a loss would
  happen about one time in four, so the G1-a re-send uses `--network-resends 2`: a network failure with no answer received is sent
  again, up to twice, as `model.openai_transport`'s default retries a network failure; a received answer is sent again only for a
  format failure, so the rule cannot select on answers. Disclosure: when this was fixed I had seen the harness's printed lead count of
  the first G1-a run (c15yc 8 of 9, c8 0 of 9, by its year match), not any answer.
- *The stop column* lists bad outcomes; each fires under the control rule above (the candidate shows it in more sends than c8 on that
  state). The pass column's lines are absolute.

| proof | arms | states (3 sends per arm) | pass | stop (bad outcome) |
|---|---|---|---|---|
| **G1-a** years and customers together | c8, c15yc | the capex article, step 42, in draws d1, d2, d3 | the candidate separates in ≥8 of its 9 sends and every candidate send retains a capex thesis; c8 separates in ≤2 of 9 (else the proof cannot tell the arms apart, reported) | three or more capex theses in one send, or a capex thesis for a year after next |
| **G1-b** customers alone | c8, c15c | positive: the capex article, d1 step 42 | the candidate retains a capex thesis in 3 of 3 sends | a send with no capex thesis |
| | | negative: Goldman's broader estimate with the capex thesis open, d1 step 66 | — | the estimate opened as a new thesis, or its statement not kept at all |
| | | single customer: the Firmus and Sharon AI announcement, d1 step 1 | — | a new thesis on a customer's own deployment or capacity (a thesis on the supplier's own guarantee or credit obligation is allowed, line 110's exception) |
| | | Gulf buyers' combined spending, d2 step 237 | reported, no line (its suitability is disputed) | — |

Sends: G1-a 18, G1-b 24: 42 sends, about $0.6 at the stored mean. **Ceilings, enforced by the harness** (`--max-usd`: each attempt
reserves production's own upper estimate, twice its bytes plus 4,096 input tokens and its whole output cap; an attempt waits while
reservations in flight would pass the ceiling): G1-a $0.8, G1-b $1.2; $2 in all. The harness sends each
attempt once over the network, as production's live transport does.

## Later gates (outlined; their lines and costs fixed and reviewed when reached)

- **Gate 2, the combined version c15** on stored states: the controls of DIAGNOSIS.md's table (a repeat, another population, an event
  under another deadline, a two-year comparison, Ohio), with one stated rule for each control; estimate about $1.5.
- **Gate 3, a paired comparison on fresh articles** by D386's protocol: a new unused set; readers' lists frozen before either output;
  c8 and c15 both run, then Steps 2–3; dev ×3 for c15; D386's lines including dev helpful ≥ 190 of 234 in each draw; and a paired,
  source-read measure of separately worthwhile questions opened and retained (not a count of fewer combined theses), unexercised
  where the set has none. Five downstream runs and the reader sessions are priced then; a first estimate is $8–10 of model calls.

## What it does not do

Ohio (D388–D391); the ladder step's handling of an event's own alternative (u1/clean-6, acc/clean-2; Step 4, frozen by D426); the date
rule misapplied once; rolling periods and small matters (c8 states those rules); the article's angle; unlinked indirect evidence; the
gap between c8's shared_quantity and the ladder step's object and theme rules. Expected effect on the judgement (D391; named first,
not measured): the second year's question opens (q04, q13 in the graded subset); an aggregate is not lost to the customer sentences;
fewer theses the ladder step refuses or mishandles because they carry two bets.
