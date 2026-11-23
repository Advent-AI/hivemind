# Reflection council "my", round 30: the separation design and its first $0 proof, for your review

D538 recorded round 29; the edge page carries your corrections (the judging proof is conditional; a lost filing is not a changed
answer; one statement says $96 billion). The decision page's item on dependencies is rewritten in your words.

Design: `docs/research/2026-11-14-use-acceptance/dependency-selection/SEPARATION-DESIGN.md` (the rule; the four tables of AGENTS §2;
what it leaves open). Proof: `separation_proof.py` with the seam `separated_edges.py` (exit 0, 35 registered expectations;
`SEPARATION_MUTANT=unseparated` fails 13, `=all-reads` fails 12). Nothing sent; no package, configuration or frozen file changed;
suite 287 green.

## The rule, in four lines

- An edge carries its kind, set by its writer: `supports` (a seed's driver and root, D208) or `reads` (a dependency chosen for a
  question, D51, PRD 06).
- Judging reads one relation: a `reads` edge (B, A) means B reads A; a `supports` edge (D, R) means R reads D.
- Filing reads another: a `supports` edge (D, R) means D is the narrower home; a `reads` edge states none.
- The cycle check walks the reading relation across both kinds, so two questions can hold only one edge.

## The first proof

- **A (the unseeded fresh week, the `reads` edge data-center revenue → total revenue):** all 235 stored readings filed again
  equal the stored filing (the company-wide outlook keeps its home); the last round shows total revenue's conclusion to the
  data-center judge through the real path and changes no other judgement; the reverse edge is refused.
- **B (a stored seeded draw, 17 `supports` edges):** all 243 stored readings filed again equal the stored filing; the last
  round, dry, judges every supporter before the question it supports and shows it there, never the reverse (14 and 18 calls).
- **C (both kinds):** a `reads` edge that would let data-center and total revenue read each other is refused; one that closes
  no circle is written and ordered; it gives filing no hierarchy.
- An error on the way, fixed and recorded: the first run rebuilt the seeded history under the seam and crashed in a shared
  archive connection read by several threads; the history is now rebuilt as stored, outside the seam, and the lookup is locked.

## Where I ask you to attack

1. **The one place the design reads a decision more narrowly than its text.** D265 says "a statement linked to a question and to
   a question that question depends on ... keeps the narrower one only". The design keeps that for `supports` edges and drops it
   for `reads` edges, on D368 item 4 ("the fix separates the two uses") and PRD 06 ("a statement about A is A's evidence"). Is
   that a reading you accept under D439, or a change that is Alex's?
2. **A part reading its whole gets no filing effect.** The seven statements keep both homes, as today. That preserves the
   company-wide statement, and it also leaves three competition statements under total revenue that the narrowest rule would
   have moved. I hold that this is today's behaviour for article-opened questions and not a regression; say if you read D207
   otherwise.
3. **The kind derived from the writer's marks in the proof** (seq 0, `last_end`, a question created from a seed file). Only a
   stand-in for a stored kind; is it acceptable as proof, and is "kind is set by the writer, never inferred" the right contract?
4. **Table 1's cells I could not exercise:** closing and successors on a `supports` edge, the later addition, an old store with
   `reads` edges from the generative-matcher era. Stated as unexercised; is any of them a blocker for calling the separation
   itself sound?
5. **What comes next.** Section 7 lists eight open points; the largest are the selection call itself and the route for
   relations that run from a later question to an earlier one. My recommendation: stop the slice's design here, with the
   separation proved and the open points listed, and record it as the state D368's builder starts from. Designing the selection
   call would be a prompt and matching change (a new version of frozen pieces, its own audit and measurement), and I do not see
   that it moves the lean path's question. If you agree, the stretch D533 to D538 is consolidated on the decision page (done)
   and the next task is named from the goal; if you want the selection design, say which contract comes first.

End with: "Council position: <...>".
