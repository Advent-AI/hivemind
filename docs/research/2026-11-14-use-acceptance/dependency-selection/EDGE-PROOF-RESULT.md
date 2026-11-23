# What would one dependency edge do to filing and to judging? A stored-data proof (D537, under D439), 2026-11-15, $0

Script: `edge_proof.py <scratch folder>` (`edge-proof.json`); mutants `EDGE_MUTANT=none` and `EDGE_MUTANT=reverse`. The edge: data-center
revenue FY2027 (`v4`) depends on total revenue FY2027 (`v2`), dated at the article that opened `v4`, written on scratch copies by the
writer's own steps (refuse a cycle, then insert). The run: the old system's stored fresh week. Nothing was sent; no package,
configuration or frozen file changed; every judgement the proof wrote that the stored archive did not hold is a labelled fake.

## The answer

**Judging: in a conditional proof (the last day only, the rest of the week as stored) the edge shows the intended conclusion
through the real checks. Filing: the same edge removes seven existing links to the total-revenue question, and for at least one of
them that is contrary to what the filing rule is for.** A lost filing is not a demonstrated changed answer. By the stop rule set for
this proof (council round 28) the conflict goes back to the council as a design question; nothing is patched and no send is
designed.

## Judging (the last day's round, from the stored state before it)

The state before the round of 2026-09-28 was rebuilt from stored answers and equals the stored run (questions, statements, links,
handovers, earlier judgements). With the edge added, thirteen registered expectations hold:

- no cycle before the edge; the writer's steps write it; the edge the other way would then be refused as a cycle;
- a changed total-revenue conclusion queues the data-center question, and total revenue is judged before it;
- the same thirteen questions are judged as in the stored round; every other judgement equals the stored one in request, band
  and reasons (the unrelated Hugging Face and financing-commitments questions among them);
- only the data-center question's request is absent from the stored archive, and it is the stored request plus exactly this:
  the block "[Current conclusions of the theses it depends on]", one line with total revenue's conclusion of that round cut at
  600 characters ("... Zacks estimates $406.05 billion and another analyst consensus is around $412 billion ... Nvidia's $108
  billion Q3 guide ..."), and the closing sentence changed from "cites_views must be empty: this thesis depends on no other
  thesis" to "cites_views only the dependency thesis ids listed above";
- the judge's own check accepts an answer that cites total revenue.

Without the edge seven of these fail; with the edge the other way nine fail (total revenue would be judged last and read the
data-center conclusion).

## Filing (every stored reading of the week filed again by the production entry point)

The control (the day's list as stored) reproduces the stored filing of all 235 articles. The reading requests do not change with
the edge (a question's dependencies are not printed in them); the edge reaches filing only through the narrowest rule in code
(`extraction.narrowest_links`, D265: a statement linked to a question and to a question it depends on keeps the first only), from
the day after the edge is written. With the edge, **seven statements change**, each from both questions to data-center revenue
alone. An edge between the unrelated pair instead changes none.

| Statement | What it says | Read against the rule |
|---|---|---|
| e22 | "Nvidia hasn't factored any sales from China into its outlook for the year" | the company-wide outlook: total revenue's own matter. A total-revenue judgement cites it, and total revenue holds no other statement of it. **A loss the rule does not intend** |
| e60, e131, e179 | the quarter's total revenue ($96.2 billion, $96.22 billion and $96 billion as each states it) and its data-center revenue (about $89 billion) in one sentence | each holds total revenue's own reported figure. Total revenue would still hold that figure in fifteen other statements; none of the three is cited by its judgements. Contrary in principle, without a loss here |
| e66 | AMD's data-center revenue | about the segment's competition: the narrower home alone is what the rule intends |
| e241, e242 | Anthropic buying capacity elsewhere and designing its own chips | the same |

The same cost is on record for the seeded set (PRD 10 §3: "Code removes the total-revenue question's own figures ... each draw it
costs the total-revenue question only 0–2 of the facts it needs").

## Why the conflict is structural

One stored edge has two readers: judging ("this question reads that one's conclusion") and filing ("this question is the narrower
home of the two"). For a part reading its whole the two point the same way, which is why the edge can be written at all; but the
narrowest rule then also strips the whole's own statements whenever the reading step links one sentence to both. D368 item 4
already names the remedy for the seeded edges ("the fix separates the two uses of the edge"); that separation is not built, and
this proof shows a chosen dependency would need it too. For the general case PRD 06 gives (a question reading its driver), the
present code would do worse: it would keep the statement under the reader and remove it from the driver, against PRD 06's own
"a statement about A is A's evidence".

## Council round 29 (D538)

The judging result is a valid conditional proof; it does not show what would happen had the edge been present all week (the
filing changes could have altered total revenue's earlier statements and conclusions). The filing result is the stop: the
selection slice cannot use the present edge behaviour unchanged. Opened at $0: the slice's design, beginning with the separation
of "whose conclusion to read" from "which question is the narrower home", without assuming every dependency is a part and its
whole, and without deciding the representation here or reversing D368's direction. The six-call comparison stays deferred: the
stored total-revenue conclusion is conditional on a week without the edge's filing effects, so it would not be an end-to-end
test of adding the edge. No send; no frozen piece changed.

## Limits

- First-order only: the week's questions and lists are held as stored. With seven links gone, later matching and total-revenue
  judging requests would differ from the stored ones and cannot be replayed at $0; what total revenue would then conclude, and so
  what its line would carry, is not known.
- One edge, one week, one draw; fake outputs for the one changed judgement; whether the judge would use the line is untested.
