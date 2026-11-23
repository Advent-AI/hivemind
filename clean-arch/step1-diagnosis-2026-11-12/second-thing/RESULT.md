# The second-thing shapes, read against their sources (D434's $0 diagnosis), 2026-11-13

**Answer.** Of the 16 theses whose outcome both wording readers called "more than one thing", the source-backed readers (Codex and
Claude, blind, each with the full article; `source-reader-brief.md`, `source-packet-1..3.json`, `source-codex-*.jsonl`,
`source-claude-*.jsonl`) agree that **6 hold two bets or no main one**, **6 are one bet** whose extra is a reference, the same event's
alternative or context, and **4 are disputed**. The 2 theses the wording readers split on, and all 6 single-question controls, both
call one bet. So Step 1's real defect in this class is **two separate bets in one thesis**: 6 of 44 agreed, up to 10 with the disputes.
The other shapes are allowed (D397) and are not Step 1's to fix.

| group | theses | both source readers |
|---|---|---|
| two bets or no main one | u3/clean-10 (HBM added in 2027, and whether any arrives before late 2027), acc/clean-10 (CMX NAND demand, and whether makers' capacity keeps pace), u3/clean-7 (Kyber in 2028, and whether NVL576 ships in volume), acc/clean-8 (HBM shipment growth, and whether supply stays short), acc/clean-9 (chip revenue, and the AI-chip portion), u1/clean-5 (DRAM, NAND and HBM prices over 2026–2027, and the per-rack cost: no main one) | agree |
| one bet with a reference, alternative or context | u1/clean-6 (2027 "or delayed to 2028"), acc/clean-2 ("or abandons/restructures"), u3/clean-1 (amount, and the resulting exposure), u3/clean-12, u1/clean-2 (signing, with its amount), u2/clean-5 | agree |
| disputed | u3/clean-11 (the 19.5 GW split), u1/clean-8 ("or disclosed shipment volume"), u2/clean-10 (capacity and prices), u1/clean-9 (Nvidia's remaining share) | one says two bets or no main, one says one |
| the wording readers' splits | u3/clean-3, u1/clean-11 | one |
| controls (both wording readers: one) | u1/clean-7, u2/clean-3, u2/clean-9, u1/clean-12, u3/clean-6, u2/clean-4 | one, 6 of 6 |

**Against Stage A's fourth run.** Of the six two-bet theses: u1/clean-5 was declined rightly every send; u3/clean-10's ladder came
and went; u3/clean-7 drew the line-3 fault; acc/clean-9 was wrongly declined once; acc/clean-8 and acc/clean-10 were sound. Of the six
one-bet-with-extras theses, the two faults (u1/clean-6's Kyber question, acc/clean-2's restructuring) are the ladder step mishandling the
same event's alternative: Step 4's, not Step 1's.

**How Step 1 writes them (its stored reasoning, read by me).** The outcome is drafted as a full description of the article's point,
with nothing in the request bounding it: "Either supply or price. I'll combine" (u2/clean-10); "(or of the 19.5 GW of incremental
capacity)" (u3/clean-11); "in 2027 as originally planned, or slip to 2028 as SemiAnalysis reports" (u1/clean-6); "and the resulting
per-rack memory content cost" (u1/clean-5). The schema's `outcome` says only "The outcome or event being tracked by this thesis";
the unit rule sits in section 3.

**Limits.** One run's theses (44), two reader families with no third reader on the 4 disputes, one article each. The source readers
judged the shape, not whether either bet deserves a thesis.
