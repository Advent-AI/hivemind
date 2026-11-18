# Deck 1 marked by the council: result (2026-11-17, $0 of API spend)

**Answer: the council, argued to agreement, passes the instrument checks fixed before marking.** By D662's lines, with the time line not applicable,
that is "enough to design the next comparison". It does not rank the systems.

## How it ran (PROTOCOL.md)

- **Round 0.** Each card was marked by Codex (memories off) and by Claude (closed command line), every session fresh and inline, with logs checked.
  - The first launch voided Codex on startup configuration notices: a check error, not an action. The rule was narrowed to notices before the
    turn starts, and round 0 resumed with the 11 valid answers reused.
  - All 38 marks were valid.
  - 6 cards differed: 2, 5, 9, 11, 14 and 18.
- **Two debate rounds.** Card 18 converged, and card 14's support converged. Five cards keep a split, recorded as "cannot tell" for Alex's spot
  check (`splits.json`).
- **The tally.** The unchanged `tally_deck.py` read the sealed key (`tally-output.txt`).

## Against the lines fixed before marking

| Line | Result |
|---|---|
| Both planted wrong answers rejected | **Yes:** cards 3 and 19, supported = no |
| The confirmed supported controls accepted | **4 of 5:** cards 4, 6, 7 and 15 yes; card 5 (old v1, credit support and guarantees) split, and so is its repeat, card 11 |
| Hidden repeats marked the same | **3 of 3** (cards 5/11, 6/13 and 10/16; the first pair is the same split twice) |
| Missed matters | Both judged worth a question: M01 FY2027 revenue (missed by the new system) and M04 the $279B supply commitments (missed by the old) |
| Completeness sheets | The 3 confirmed undelivered facts "bear" on their question, but "would change only the confidence". The 3 negative controls "do not bear" |

**Card 5's split is substantive, not noise.**
- Codex: the disclosed guarantee caps do not establish what will be *outstanding* in the next commitments note.
- Claude: NVIDIA's disclosed maximum exposure is what such a note reports.

That is a question for Alex's spot check.

## Read with care (not a ranking; DESIGN.md: it "cannot show … which system is better")

- **The new system's 6 real answers:** 5 agreed supported (4, 6, 8, 10, 12) and 1 split (9). All are worth tracking.
- **The old system's 6 real answers:**
  - 3 agreed supported (7, 15, 18);
  - 1 agreed unsupported (14), whose worth is also split;
  - 2 split on support (2 and 5); card 2 is split on worth too.
- **Delivery.** The undelivered facts on the new system's v2, v3 and v7 would change only the confidence, not the answer.
- **Agreement with the stored model families of 11-14:** worth 8 of 12; supported 11 of 14 (Codex) and 10 of 14 (Claude). These carry D661's caveat.
