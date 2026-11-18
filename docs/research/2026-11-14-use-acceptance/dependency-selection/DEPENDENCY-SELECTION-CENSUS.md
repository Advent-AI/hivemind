# Where could a new question have been given a dependency? A design census on the unseeded fresh week (D536, under D439), 2026-11-15, $0

Scripts and files beside this page: `build_pairs.py` (`pairs.json`, `packet.md`), `brief.md`, `own-read-before-readers.json` (Claude's
read, written before any reader), `codex-reader.jsonl` and `claude-reader.jsonl` (two blind readers of different model families, each
given only the packet and the brief in a clean folder), `tally_pairs.py` (`tally.json`). The run: the old system's stored draw of the
fresh week (`poc/data/clean-lean-week-2026-11-14/week/p1/prod`: 235 articles, 15 questions, no dependency written). Nothing was sent
to a model and nothing changed in either system. This is a census for a design, not a claim about what the matching step would
choose, and not a test of any answer.

## The answer

**One clear case in the week, and a negative control; the census is not stopped.** When the data-center revenue question opened, the
system had just compared it with the total-revenue question and recorded "part of" (1.00). All three readings mark that pair as
strong. The total-revenue question's conclusion stated a consensus for the year from 2026-09-23 ($406.05 billion; about $412
billion from 09-25) and the next quarter's guidance of $108 billion from 09-26; none of these three figures was anywhere in the
data-center question's seven requests, and its last answer says so and closes the gap with a step of its own. That is the one answer of this system's fifteen that both reviewing teams of the week marked as
resting on a number nobody gave it. A dependency chosen when the question opened is the route PRD 06 names for this ("A statement
about A is A's evidence ... B learns it through A's conclusion"). Whether the judge would have used the line is not tested, and
the line would not by itself make the answer supported: the total's conclusion holds forecasts and assumptions of its own, and
the data-center judge would still have to turn company-wide figures into a segment's (council round 28).

The relations an analyst would most want run the other way in time: the Rubin shipping questions opened after the revenue
questions they bear on, and a dependency is chosen only when a question is created.

## The pairs

The rule in force (PRD 06, D51): the matching call chooses a new question's dependencies only among the questions it was compared
with, the questions shown that day, and the candidates opened from the same article; "B depends on A" means B reads A's conclusion.
Over the 15 openings that gives **97 pairs** (95 compared when the question opened, 2 from one article). Each reader gave every
pair one mark: the new question would want the other's conclusion; only the other way; both; the same question (or another period
or deadline of it); none. The two blind readers give the same mark on 68 of the 97.

| | Both blind readers | Claude's own read (written first) |
|---|---|---|
| the new question would want the earlier question's conclusion | 11 (3 marked strong by both) | 5 (3 strong) |
| ... of which the other question is a theme already shown to it | 0 (one reader: 1) | 0 |
| only the other way, or both ways | 10 | 15 |
| ... of which the new question is a company question, so the earlier question could only gain the link later | 8 | 9 |
| both ways (a second link would close a circle) | 3 | 1 |
| the same question, or another period of it | 1 pair, marked in both of its orders (two of three readings: 3 pairs) | 3 pairs |
| none | 57 by one reader, 69 by the other | 75 |

Where the readings part (all kept in `tally_pairs.py`'s output): one blind reader marked no pair between a new theme and an earlier
company question (the packet says themes are shown to every company question already), the other marked sixteen; total revenue of
one year against the next is "the same thing, another period" for both blind readers and an input in Claude's read; next year's
market spending against this year's is an input for both blind readers and a successor in Claude's read and in the run's own
record. Where "an analyst reasons onward" stops is not settled by these readers, as in the earlier censuses.

## The eleven pairs both blind readers marked, read against the stored conclusions

For each: what the earlier question's conclusion would have shown (its first 600 characters, as a request shows a dependency) at
the new question's judgements, and whether the new question's whole request already held it.

| New question ← earlier question | Readers | What the line would carry | Read |
|---|---|---|---|
| data-center revenue FY2027 ← total revenue FY2027 | strong, all three (both ways) | the $406.05 billion consensus from 09-23, about $412 billion from 09-25, the $108 billion guidance from 09-26: none of the three anywhere in the new question's seven requests (the $96.2 billion quarter the line also names was already in all seven) | **useful and source-backed** (six cited passages); the question's last answer: "no full-FY2027 Data Center consensus or annual company target", then "a further roughly 25% step-up in Q4" of its own |
| total revenue growth FY2028 ← total revenue FY2027 | strong, all three | the same figures | arguable: the question asks a growth rate and holds the growth consensus and guidance; the base adds little. The question is itself a second form of the FY2028 revenue question |
| market AI spending 2027 ← cloud companies' spending 2026 (both themes) | strong, both blind | "nearly $800 billion for calendar 2026" | nothing new: the new question's answer already uses those figures; the run recorded the pair as one quantity's next year |
| gross margin FY2028 ← Rubin shipping by January 2027 | one strong, one weak | production shipments began in August 2026 | second-order: the answer rests on management's margin guidance |
| gross margin FY2028 ← total revenue FY2028; ← its growth | weak, both | revenue figures | context only |
| the two questions on China's permission for one card ← U.S. authorization of Blackwell exports (all themes) | weak, both (both ways) | the standing U.S. restriction, no figure | context only; a theme is not shown other themes, so a link would be the only route |
| total revenue growth FY2028 ← data-center revenue FY2027 | weak, both | **the data-center judge's own numbers** ($105 billion, $131 billion: the step nobody gave it) | a risk, not a gain: a dependency would pass an assumed number on |
| total revenue FY2028 and its growth ← financing commitments | weak, both | guarantee ceilings of $105 and $108.5 billion | context only |

**Negative controls.** The question on the Hugging Face purchase commitments against its eleven earlier questions, the financing-
commitments question among them (both are amounts in the same note of the annual report): "none" in all three readings, and the
financing conclusion carries nothing it needs. And the next-to-last row above: a link two readers would grant weakly that would
carry an unsupported number.

## The other direction, and what already covers part of it

- **A later question that an earlier one would want** (both blind readers, new company question): Rubin shipping by January 2027
  against the four revenue questions; Rubin GPUs by December 2027 against the two FY2028 revenue questions; data-center revenue
  against the two total-revenue questions. Read in the store: over all their requests, three of the four revenue questions held
  no statement naming Rubin (the data-center question held ten). A dependency chosen at creation cannot serve these; D191 point 2
  (a later article may add a dependency to an existing question) is decided and unbuilt.
- **A later theme that earlier company questions would want** (export authorization, the cloud companies' spending, the Chinese
  permissions): the theme block already shows every judged theme to every company question; no link is needed (D191).
- **Circles.** Data-center revenue and total revenue are marked both ways by all three readings: the part is sized from the
  whole, and the whole is mostly the part. Only one of the two links can exist (PRD 06 refuses a cycle); at creation the
  permitted one is the new question reading the earlier one, here the part reading the whole.

## What the matching step already records

Every new question's candidate is compared with each listed question and one relation of a closed set is stored (`RELATIONS` in
`views/jev_matching.py`: the same quantity or event; the same quantity for another period; part of; one matter, two quantities;
different; cannot tell). In this week: 85 "different", 3 "part of", 2 "another period", 4 "one matter, two quantities", 3 without a
relation. The one useful pair is the one recorded "part of" at 1.00. The relation is not the choice: of the nine pairs recorded
as other than "different", both blind readers want the conclusion on five; of the 85 "different", on five (all but one weak).
Whether two questions are part and whole is identity; whether one needs the other's conclusion is the model's judgement (AGENTS §2).

## What this may and may not be said to show

- Shown, for one stored week and one draw: the pairs on which a dependency could have been chosen; one pair where the earlier
  question's conclusion held source-backed figures the new question never received and whose absence its last answer names; that
  most pairs readers grant carry nothing the question needs; one pair where a link would carry an assumed number; that the
  strongest driver relations of the week are not available at creation.
- Not shown: that the judge would use the line, or that the answer would become supported (no send); a rate (fifteen questions,
  one clear case); what the matching step would choose if asked; anything about seeded edges or the reversal of D368 item 4 (the
  useful pair here is a part reading its whole, the stored direction of the seeded set); anything about the new system, which has
  no such mechanism; which system carries forward.
- The same figures could also have reached the question by filing (the sixteen guidance statements sit under total revenue only;
  D207 gives a statement one home, and PRD 06 gives the other question the conclusion instead). This census does not choose
  between the two routes.
