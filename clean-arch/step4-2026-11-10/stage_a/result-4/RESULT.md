# Fourth Stage A of the clean ladder step: the result (2026-11-10)

**Lines 2 and 6 are met under every reading. Line 5 is met on the two readings that favour the answer and missed by one
thesis on the strict one. Lines 1, 3 and 4 are still missed, by one, two and three answers on the two third readers' agreed
rulings (none, one and two on what both first readers fail).** By D401 a missed line stops the work and goes to Alex; Stage B
is not opened. Stage A does not compare the step with production (D400).

The step as measured (design version 35): the third run's request with D417 (a rolling twelve months with no publication day
declined), D420 (an authority's proceeding always has a ruling out), D418 narrowed (a tracked government decision is the
theme's) and D416 (an event's ruling out as who decides and what they decide), each tested alone before it (design §5.2.5);
the same 44 stored theses, three sends each; gpt-6-luna at medium effort. The code, the request and the readers' forms as
sent: `poc/data/clean-ladder-stage-a-2026-11-10/run-4/code-as-sent/`.

- Sent: `run-4/` (132 sends, 148 calls, $0.1091 from tokens; spent under D401's $3: $1.135). 104 ladders (46 events, 27
  figures for the company, 31 for a theme), 27 declined, 1 refused twice by code (u3/clean-10 send 3). 16 first answers were
  sent back, 15 for the reference's quotation (the third run: 23; the second: 72).
- Read by me, all 132 answers, before any reader's row (`own-read-before-readers.md`); then by two reader families with the
  form as sent; where they differ (42 of 840 marks, 5%, and 11 faults named outside the form) two third readers ruled, one of
  each family, their hand-off now carrying the list of themes. They agree on 29 of the 53 points (the third run: 21 of 70).
  The Codex third reader ruled 22 of the 42 marks failed, the Claude one 6. Two Claude third readers were cut off by a
  network failure: one had already written its 15 rulings, checked complete; the other was started again.
- Generated beside this page: `report.txt`, `tables.txt`, `code-counts.txt`.

## The lines

| line | third run: both readers fail | fourth run: both readers fail | fourth run: third readers agree, rest for the answer | fourth run: rest against it |
|---|---|---|---|---|
| 1. no ladder asks another question (Q) | 1 | **0** | missed: 1 | missed: 5 |
| 2. no ladder leaves a part unlisted (L) | 1 | **0** | **met: 0** | **met: 0** |
| 3. no outcome with no rung or two (R) | 3 | 1 | missed: 2 | missed: 4 |
| 4. no refusal without a justified reason (N) | 0 of 24 | **2 of 27** | missed: 3 | missed: 3 |
| 5. 35 of 44 theses right in two sends of three, 28 by a ladder | 39 and 31 | 43 and 33 | met: 40 and 31 | missed: 34 and 25 |
| 6. the favourable end the same in three sends | met: 0 of 9 differ | **met: 0 of 9** | by code | by code |
| 6. the due day the same, nine theses in ten | met: 34 of 35 | **met: 33 of 33** | by code | by code |
| ladders with no failed mark | 91 of 108 | 97 of 104 | 89 of 104 | 71 of 104 |

**The answers behind the missed lines, on the agreed rulings.**
- Line 1, one: u1/clean-6 send 3. The thesis asks whether Kyber ships "in 2027 or is delayed to 2028"; the question asks
  "by December 31, 2028", to which both branches answer Yes.
- Line 3, two: u3/clean-7 send 3 (the question asks for shipments "in calendar 2028", the Yes condition holds for "by
  2028-12-31"; both first readers); acc/clean-2 send 3 (the ruling out counts a "restructuring" of the acquisition, which
  need not prevent its completion; both third readers).
- Line 4, three: u3/clean-11 sends 1 and 3, acc/clean-9 send 2: declined for "two figures, none the main one" where the
  outcome leads with one figure and gives the other in brackets or as "the portion of it". **New in this run:** every send
  of both theses in the second and third runs was a ladder (`decline-accounts.json`: asked, the model says in all three that
  the first figure is the main one and that its decline "was incorrect"; "I over-applied the instruction").

## What the four changes were built for

One send carried all four, so the run attributes nothing to one of them; each rests on its own small send (design §5.2.5).

| built for | third run | fourth run |
|---|---|---|
| a wait written as the ruling out (D416) | 3 of 45 events, failed by both readers | none of 46; every event names who decides and a decision |
| an authority's proceeding (D420) | one French thesis with no ruling out in 3 of 3 sends, the readers parting | the nine French answers all write the abandonment without the conclusion; none is failed on R by both readers |
| the object of a government's decision (D418) | 5 ladders under the company failed by both readers | the three permission theses under the theme in 9 of 9; the company's own sales under the company in 3 of 3. One new fault both readers mark: u1/clean-10 send 3 files a ban on Chinese-made lidar under the export-controls theme, which does not cover it (declined in its other two sends and in every earlier run) |
| what is not a year's figure (D417) | the surveys declined in 5 of 6, re-cut once | declined in 6 of 6; the quarter in 3 of 3 |

## What is left, and where it sits

- Of the six answers behind lines 1, 3 and 4, five are on four theses whose own outcome names two things or two periods:
  u1/clean-6 ("in 2027 or is delayed to 2028"), u3/clean-7 ("in 2028 versus the original 2027 schedule, and whether the
  larger … system ships"), u3/clean-11 (a spending split "(and of the 19.5 GW …)"), acc/clean-9 ("revenue and the AI-chip
  portion of it"). The sixth, acc/clean-2, has an outcome that reads "closes (or abandons/restructures)".
- **Declines moved.** 27 against 24, and between theses: four theses have a ladder in some sends and none in others (the
  third run: two). u1/clean-5 is still declined three times, now with the seventh case's reason.
- **Not lines, and seen:** the 105 billion ceiling is the reference again in one send of acc/clean-3 (both readers fail XR);
  a year is carried as the reference's number on eight event ladders; u1/clean-6's two sends that ask about 2027 are due at
  the end of 2028 (two third readers uphold it as a fault outside the form).
- **Every fault the model was asked about, in five rounds of accounts on 23 stored answers, it called its own slip and
  quoted the rule against it** (the direction, the missing ruling out, the wait, the object, these declines). The accounts
  locate a kind of fault, one pass that slips a rule it knows; they do not show a mechanism that removes it.

## Against what I wrote before the send (round log §69)

Line 6 stays met: yes. No wait written as the ruling out, none missing on the French theses: yes. The permission theses
under the theme in every send: yes. The surveys and the quarter declined in every send: yes. u1/clean-6 asks about two
years: yes, and it is the one answer behind line 1. What I had said I could not say, whether lines 1 to 3 are met: lines 1
and 3 are missed and line 2 is met. Not expected: line 4 missed, by declines that had not occurred before; the lidar ban
under the export-controls theme.
