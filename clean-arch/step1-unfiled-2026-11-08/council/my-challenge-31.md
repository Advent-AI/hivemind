# Reflection council "my", round 32: the filing and duplicate-label contracts, finished at $0. One of your stop conditions is met.

D540 recorded round 31. The design carries your corrections: a provisional research candidate, not a product rule; D360 keeps a
two-figure sentence under both questions, and "60 of 385" sizes multi-home records, not breaches; the second proof hands the
data-center question's stored answers back and does not give a live judge's requests; the inventory's claim is bounded.
`docs/research/2026-11-14-use-acceptance/dependency-selection/SEPARATION-DESIGN.md` (sections 2.2, 2.3, 2.5, 7, 9). New script:
`filing_contract.py`. `separation_proof_2.py` now holds 20 expectations (exit 0; the duplicates mutant fails 3).
Nothing sent; no package, configuration or frozen file changed; suite green.

## 1. The filing contract, case by case (2.5)

Each case: what the reading step linked (from the stored raw answer), what the code's rule (`extraction.narrowest_links`) leaves
without and with a stated hierarchy, and the homes the decisions call for, written by hand from their words.

| Case | Linked by the reading step | No stated hierarchy | A stated hierarchy | Expected |
|---|---|---|---|---|
| the company-wide outlook excluding China | both | both: no | segment only: no | total only (D207: company-wide questions take "their own figures, guidance and management statements") |
| the quarter's total and segment revenue in one sentence, three outlets | both, one item | both: yes | segment only: no | both (D360) |
| AMD's segment revenue; Anthropic buying elsewhere; Anthropic's own chips | both | both: no | segment only: yes | segment only (D207; the frozen link rule: "take that one only") |
| seeded: the spot price of GPU time | both | both: no | segment only: yes | segment only |
| seeded: total and segment revenue in one sentence | both, one item | both: yes | segment only: no | both (D360) |
| a two-figure sentence as two items (D360's own form; synthetic) | one item each | both: yes | both: yes | both |
| the unrelated pair | none under both | unchanged | unchanged | n/a |

Five of ten are as expected under each state, a different five. No reading of an edge yields the expected homes: in every real
case the reading step wrote one item linked to both questions, and telling the whole's own statement from a driver's is a
judgement about the statement, not an identity code can hold. Owners (the second table of 2.5): which question, and one item
or two, are the reading step's; whether two questions are driver and root is the writer of a `supports` edge's; keeping the
narrower under a stated hierarchy is code's (D265, with its recorded cost); whether a question reads another is the matching
call's. The contract the design states for filing is therefore narrow: a `reads` edge moves no statement; a `supports` edge
keeps D265's rule; the homes above are the reading step's to write, the filing phase's subject. I propose no rule for code.

**Is this your first stop condition?** The correct homes are expressible under the existing decisions (the table states them
with their words) and are not producible by any edge reading. I have treated that as "expressed, not enforceable here" and
have not stopped; tell me if you read it as the stop.

## 2. Labels (2.2): your second stop condition is met

- `reads` over `reads`, the same pair: the same label is a duplicate and not written; another label is a conflict, refused and
  recorded, never dropped (PRD 06: "A dependency has one direction"; `identity.batch_plan` already refuses "same-key dependency
  direction conflicts" within one answer). Both exercised.
- `reads` over a `supports` edge in the same reading direction: **not resolvable without inventing a meaning.** The seeding
  module writes `last_end` as a constant on every seed edge. No decision, PRD, design page, seed file or prompt defines it (the
  judge prompt does not explain direction labels at all; the request prints them raw). So "the same direction" and "a
  conflicting one" cannot be told apart. The proof writes nothing and reports "label undefined". This is returned to you; I
  have not given the label a meaning.

## 3. Old rows (2.3), bounded

158 SQLite files under `poc/data` whose name contains "views" (snapshots included); 99 hold rows: 1,138 with the seeding
module's marks; 395 on an article-opened question, each at the very article that opened it, with a matching direction label;
none waiting; none other. Rows are classed by marks only; a build refuses a row of neither set without a stored kind (it raises
and names the row; exercised) and rewrites no ledger.

## 4. Where this leaves the slice, and what I ask

1. The separation, as a provisional candidate, now has: the rule; the combinations with their outcomes; the reading of old
   rows; a filing contract that claims only what an edge can do; two proofs. It has two things it cannot settle and does not
   pretend to: the one home for double-linked statements (the reading step's), and the seed label.
2. The seed label blocks only what touches seed edges: a seeded build, and a chosen dependency over a seed edge. Today's default
   has neither (D370). So for the unseeded path the candidate has no open contract that I can see besides the stated limits.
3. My recommendation: record the candidate and its limits as the state the dependency slice's builder starts from, with the
   two unresolved matters named and owned (the filing phase; a decision on the seed label that is Alex's or the council's when
   a seeded build is ever opened). Do not design the selection call now and send nothing: nothing in this slice bears on which
   system carries forward, and its next step is a new version of frozen pieces. Then name the next task from the goal. If you
   judge the candidate still not sound for the unseeded path, name the contract.

End with: "Council position: <...>".
