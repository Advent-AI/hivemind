# The split version's prompt audit (AGENTS §6; council round 161's caveat), 2026-11-16

**Method.** My own table came first, written before reading any blind reader (`prompt-audit/own-audit.md`). Then five fresh read-only
Codex readers each read the whole request as the model reads it. Each saw only the request and its diff (`prompt-audit/split-request-r*.md`,
`split-diff-r*.md`) and the sources: D38, D397 and D436, and DESIGN.md §2 and §0b item 2. Each reader's findings were checked against
the text and fixed, until a round found only what the change did not introduce.

## What the rounds found and what changed

| Round | Finding (read against the text) | Change |
|---|---|---|
| own | The system text still said "in seven cases" while the schema offered eight | the system's decline list says eight and adds the case, with one example on each side of its boundary (a retailer's store openings in two years; its revenue against the year before) |
| 1 | The yearly line did not say that the two-year case does not apply in a re-ask | stated in the line |
| 1 | A part naming the other year and another limit could be dropped whole | the line keeps "every other part, including a condition or comparison that names" the other year |
| 1 | The new case and "no main figure" (the case the frozen step used for both T topics in every send) had no order | the case says it applies "rather than the first, since each year has its main figure" |
| 1 | The example's "2026 as its reference" contradicted the reference rule | removed |
| 2 | The yearly line, the closing check, the schema's `not_judged` and line 5 did not say which prevails | the line says "where the instructions above differ, this line prevails"; "that value alone is not listed"; "where a part joins the other year's value with another limit, a condition or a comparison, list that limit, condition or comparison" |
| 3 | My round-2 clause read as a condition ("neither year is picked as the one the outcome names") | reworded as an instruction ("rather than judging only one of the two years as the one the outcome names") |
| 4 | Both values asked and also compared: is either a base? | "a comparison between the two does not make either a base when the value of each is asked" (system and schema) |
| 5 | The unchanged closing check ("does it ask one thing … listed in not_judged?") sits beside the new decline on the topic's first request | **not changed:** the closing check has stood beside the seven frozen decline cases. In every stored frozen send of both T topics the model declined under it (9 of 9 and 9 of 9). It reads a written question back, and a decline writes none. Recorded, not answered |

## Growth (characters)

- System text: 9,545 → 10,155 (+610).
- Schema: 6,116 → 7,308 (+1,192).
- A yearly re-ask's added line: 431.

**Reasons:**
- the decline cases become the closed set AGENTS §6 asks for;
- the system lists the case where the seven are;
- one example on each side of the boundary replaces an abstract clause;
- each sentence of the yearly line answers a finding above.

## Left to the probe, not settled by reading

- whether the model names the case on the four C1 topics with an open base year (the control count, `BY`);
- whether a mixed part keeps its other limit (`LQ`);
- whether the model follows the yearly line's precedence (`L` on yearly items).
