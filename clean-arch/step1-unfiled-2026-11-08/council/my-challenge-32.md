# Reflection council "my", round 33: the unseeded failure-and-reader contract, done at $0; three places where decisions and code part; and a structural proposal

D541 recorded round 32 (the seed-label stop; the filing finding as a bounded hand reading, the outlook's home left open to
review). New: section 2.6 of `docs/research/2026-11-14-use-acceptance/dependency-selection/SEPARATION-DESIGN.md`; `seam_plugin.py`;
`old_rows_readers.py`. Nothing sent; no package, test, configuration or frozen file changed.

## 1. What was exercised, through the actual writer and readers

- **The package's own 287 tests run with the separated reading installed** (`seam_plugin.py`): 285 pass as they are. They
  include the paths you named: a dependency refused inside one answer and the retry ending (`test_identity_repair`), an awaited
  year bound when its question is created (`test_english`), resolutions through the bundle and the research context, the
  service's as-of relationships, the idea route's graph, the closed set for `cites_views`. The two that do not pass both write
  a row by hand with the seed label at an article's sequence, which neither writer produces: the resume test (a round that
  died after one judgement recovers its queue through a dependency: it passes once that one row is restated as a chosen
  dependency, 286 of 287) and the narrowest-rule test, which holds D265 in its literal reading over such rows.
- **Old rows through the product's readers** (`old_rows_readers.py`): in the 28 ledgers that hold only matching-era rows, the
  service shows exactly what the candidate reads for all 399 questions with an edge. In the 71 seeded ledgers it shows the
  stored direction, or nothing for most seed rows (the as-of filter hides rows at sequence 0): a seeded build's matter.
- **The whole week with a normal edge** (round 31's W2) and the label outcomes (X) stand as they were.

## 2. The state-by-event contract for the unseeded path (2.6): reachability first

A dependency chosen at creation is the only decided writer on the default path. At creation nothing yet reads the new
question, so a circle against stored edges, a duplicate across articles and a conflicting label across articles **cannot
occur**; they arise only with the later addition (D191 point 2, unbuilt). What can occur at creation (a normal edge; a name
that was not shown; a circle or a direction conflict among one answer's candidates; the read question closing, succeeded or
awaited; a theme named; a crash and a resume; an old row read by the pages) is handled by code the candidate does not touch,
and each was exercised above, with two exceptions stated in the table: no pair names a theme, and nothing covers a question
closed without a successor.

## 3. Three places where the decisions and the code part, or the decisions are silent (recorded; none decided by me)

1. **A circle against stored edges.** PRD 06: "Refuse a cycle and ask the model to correct it; persistent cycles follow normal
   failure handling." `writing.write` drops the edge with a note. Unreachable at creation; it matters for the later addition.
2. **A later proposal with another direction for a pair already read.** PRD 06 says only "A dependency has one direction".
   No decision says what happens to the later one. Your stop applies: I state the outcomes of 2.2 as the candidate's and do not
   decide the handling; it belongs to the later addition's design.
3. **A question closed without a successor.** PRD 06 has the reader keep its closing conclusion "historical only". The request
   can print that mark; no code in the package writes the resolution that sets it, and no test covers it.

## 4. A structural proposal, because this is the ninth round on one slice

Every round since 24 found real gaps, and they are of one class: contracts of pieces that do not exist yet (the selection call
and its retry on the Jev engine; the later addition; a seeded build and its label; the pages for seed rows). AGENTS §1: "When
one mechanism draws findings round after round, stop answering findings: propose one structural rule." Alex, on a stretch like
this one (D391): "感觉现在一直在修一些minor的原地打转，你是不是要思考下现在具体还差什么high priority big impact 的需要做？"

The rule I propose: **the design of a slice that is not open for build ends at a provisional candidate with (a) its rule, (b)
proofs of what stored data can show, and (c) the list of contracts its build must settle, each with its owner and the decision
or silence it rests on. A contract that depends on an unbuilt piece is written when that piece is opened, in its own design
review, not before.** Under it this slice's design is complete now: (a) section 2; (b) sections 8 and 9, 2.5, 2.6; (c)
section 7 with the three items above added. It is recorded as provisional, not sound for build.

Two facts weigh on continuing instead. The slice exists only in the old system: if Alex carries the new system forward, none
of it is used. And nothing in it has moved the lean path's question in nine rounds; the decision page already says the council
advises against more small tests of corners.

So: accept the rule and close the stretch, or tell me which event that can occur at creation on the unseeded path is still
undetermined. Then name the next task from the goal (D466). If you hold that the next task is still inside this slice, say
what it would let Alex decide that he cannot decide from the decision page today.

End with: "Council position: <...>".
