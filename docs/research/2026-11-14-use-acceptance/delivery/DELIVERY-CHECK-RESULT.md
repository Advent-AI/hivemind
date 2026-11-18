# Do the kept financial figures reach the judgements of related questions? Result (D505), 2026-11-15

Design: `DELIVERY-CHECK-DESIGN.md` (version 2, frozen before any reader). Census: `census_delivery.py`, `delivery-census.json`. Tally:
`tally_delivery.py`, `tally-delivery.txt`, `delivery-candidates.json`. The run: the new system's stored fresh-week draw of D489
(2026-09-22..28, seven questions, 37 judgements). Cost: $0; nothing was sent to a model and nothing changed in the system.

## The verdict, by the rule written before any reader

**One finding, and six open leads.** One question did not receive a kept fact (two figures, stored in four table lines from two
articles) that both reader families, and a fresh reader of each family who saw everything the judge had, say bears on its answer. Six
other lines stay open leads (the fresh pair split on five; one was not settled). No missing figure was established for the other
five questions.

| Question | Lines either family listed | Of those, not shown by their own statement | After reading the requests and the fresh pair |
|---|---|---|---|
| v1 total of credit support and revenue guarantees | 6 | 5 | **finding: 4 lines (two figures, two articles); 1 open lead** |
| v2 purchase and supply commitments in the annual report | 23 | 20 | 15 delivered in substance (the request states the figure); **5 open leads** |
| v3 approval of Blackwell sales to China | 14 | 10 | 10 delivered in substance |
| v4 Vera Rubin volume shipments with first revenue | 1 | 0 | nothing missing |
| v5 the hyperscalers' 2026 data-center spending | 0 | 0 | nothing listed (both families) |
| v6 the Hugging Face purchase closing | 0 | 0 | nothing listed (both families) |
| v7 approval of RTX Pro 5500 purchases in China | 4 (one family) | 4 | dropped: both fresh readers say they do not bear |

Every question has its completion line from both families.

## The finding

- **The question (v1):** "What total amount in USD of NVIDIA's credit-support commitments and minimum-revenue guarantees or backstops
  to AI labs and cloud partners, including the support for the additional lab's nearly 2 gigawatts of computing capacity, will be
  disclosed in NVIDIA's FY2027 Form 10-K ...". Its judge was shown 37 statements: among them the nearly 2 gigawatts for one lab and
  4.25 gigawatts (with an option on 3.75 more) at another site, as volumes with no dollar value, and a $108.5 billion cap on
  guarantee obligations.
- **The figure it did not receive:** NVIDIA's own revenue opportunity per gigawatt: about $25 billion with Blackwell and about $40
  billion with Vera Rubin. Stated in two articles of the week, both read after the question was open:
  - article 98: "Management puts NVIDIA's revenue opportunity at about $40 billion per gigawatt of capacity with Vera Rubin, against
    $25 billion with Blackwell." The statement was kept and linked to the Vera Rubin question only.
  - article 203: "Nvidia said its revenue opportunity per gigawatt ... has risen from roughly $18 billion during the Hopper generation
    to $25 billion with Blackwell and $40 billion with Rubin." The statement was kept and linked to no question.
- **Why it bears** (the readers' reasons): it is a price to go with a volume the judge already has, a conditional indication of
  scale: if the nearly 2 gigawatts were built on these generations, they would be $50 to $80 billion of NVIDIA equipment. It is the
  company's revenue opportunity, not the amount it guarantees; the articles do not say which generation the capacity uses, what
  share NVIDIA supports, or that any of it sits outside the $108.5 billion cap.
- **What was observed of the judgements:** all seven stored judgements of this question chose its top band ($100 billion or more,
  on the $108.5 billion cap). The effect of adding the figure was not measured.
- **The kind of gap:** the reading step linked the per-gigawatt figure to the question whose own figure it is (the product's
  revenue) and not to the question it bears on by one step of reasoning (price times the volume under guarantee). That is the
  relation `docs/prd/10-filing-phase.md` §2 names ("an analyst also reasons onward from a fact: ... price and volume"), seen here
  once on the new system, in the scope of the financial table.

## The open leads (the fresh pair split; not findings, not dismissed)

- v1: the roughly $18 billion per gigawatt of the older Hopper generation (article 203): one fresh reader says it helps size the
  capacity, the other that a past generation prices nothing the question counts.
- v2 (supply commitments): the market's view of next year's sales ($671.95 billion; growth of 65.5% and 66%) and the CEO's remark
  that chip sales would double: one fresh reader says they support a higher commitment total, the other that they repeat the 70%
  guide and the doubling talk the judge already has (a reason that leans on the answer staying in its top band, though the design
  also counts a change in likelihood).
- v2, not settled: line T-104, "revenue growth around 70%" stored for FY 2027 as its two articles write it ("For FY 2027, Nvidia
  estimates its revenue growth will be around 70%"). The request states a 70% outlook for fiscal 2028, so by the design's rule (the
  period must match) this line is not delivered; the article's year looks wrong, and the line was not put to the fresh pair.

## Delivered in substance (read in the stored requests)

- v2: the 70% growth outlook for fiscal 2028 (twelve lines from other articles) is stated in the request, with its supply
  constraint, through the statement that was linked; the margin figures (three lines) likewise.
- v3: the $108 billion guide with its exclusion of China data-center revenue (ten lines from other articles) is stated in the request.

## The instrument's own check

- Of the lines the system did show, the readers also list: v1 1 of 1; v3 4 of 6 (both families); v2 2 of 7 (both), 3 (Codex); v4 1
  of 10 (both). For the Vera Rubin question the system showed ten financial lines and both families call only one answer-bearing
  (its expected share of data-center revenue): the reported quarter's revenue and data-center figures were shown to it as well. The
  readers' bar is higher than the system's there; this check did not examine whether such background belongs under a question.
- The first readers' lists were wide for one family (Claude listed 20, 14 and 4 lines where Codex listed 8, 4 and 0); the fresh pair,
  shown what the judge had, cut the one-family candidates to five open leads. One stored source was found wrong on the way (the
  "below 1%" share of China sales is the article's own statement, stored as the CEO's).

## What this result may and may not be said to show

- Shown, in one stored run, seven questions and the financial table's 146 lines: a judge is shown exactly the statements linked to
  its question (196 links; see the correction below); one kept fact that bears on a question by a step of reasoning did not
  reach it; six more lines are open. No rate is claimed: the check depends on what two first readers noticed and counts repeats of
  one figure as lines.
- Not shown: that any judgement would have changed; that all useful evidence reached the seven questions (389 of the run's 569 kept
  statements have no question, and only the 111 that carry a revenue or margin figure were examined); anything about production or
  about which system carries forward.

## What the reading step's stored reasoning says (read at $0; a stored reason is not a cause)

In both articles the credit-support question was in the list of open questions the reading step was shown (it opened at article 4).
- Article 98: the reasoning takes the per-gigawatt statement with the Vera Rubin shipments ("links to clean-4") and links it there;
  it links another statement of the same article (nearly $50 billion invested in AI labs) to the credit-support question. It does
  not weigh the per-gigawatt figure against that question.
- Article 203: the reasoning weighs the statement against the Vera Rubin question ("informs the value of the Rubin ramp, though not
  the shipment timing ... Could also be unlinked"), lists all seven open questions by name, and leaves it unlinked.
No check dropped the statement: it was kept both times. This is what was written, in two cases; it does not establish why.

## Council (thread mx, round 19; `clean-arch/step1-unfiled-2026-11-08/council/mx-challenge-18.md`, `mx-codex-19.md`): consensus, with corrections

- The finding stands by the rule as written: two figures in four lines from two articles, one question; not four gaps.
- Corrected in this page after the council's challenge: the per-gigawatt figures are a conditional indication of scale, not a
  guarantee and not shown to sit "on top of" the cap (one fresh reader's wording, not the articles'); "would not have moved the
  answer" was an untested counterfactual and is replaced by what was observed; T-104 had been filed as delivered against the
  design's own period rule and is an unsettled lead; "nothing missing for four questions" is "no missing figure established for
  five"; no general rate.
- Not recommended: a census of the 389 statements no question received. It widens beyond the financial figures Alex chose and
  leaves out statements linked to another question, which is the very pattern of article 98.
- The bounded next step the council named (trace what the reading step saw and how it linked, within the financial scope) is the
  section above; the count across all seven questions, statements linked elsewhere included, is this check's own scope.

## Lessons

1. **Whether a figure was delivered is read in the request.** The census first counted a figure as delivered when a statement of
   the same claim group was shown; a statement carries several figures and the group need not state this one. The council caught it
   before any reader.
2. **A first reader's list is a lead; what the judge already had decides.** 29 one-family candidates became five open leads once
   fresh readers saw the whole request.
3. **Apply every condition of the frozen rule when sorting by hand.** T-104 was sorted as delivered though its period does not
   match; the council caught it.
4. **Write what was observed, not the counterfactual.** "It would not have moved the answer" was never tested (the same fault as
   promising a measure a test cannot take, and as reading a cause into a stored reason).

## Correction (2026-11-15, found by the reflection council "my", round 3, and checked in the stored run)

This page said that nothing in the new system files an earlier statement under a question opened later, and that a judge is shown
the statements linked "when their articles were read". Both are wrong as written. **The new system has a later-linking step**
(`clean-arch/step3/library.py`, `link_later`): when a question opens, the system checks the earlier groups of statements (a
statement with its repeats) **whose original statement arrived without a question** (a batch that fails twice stays pending and is
tried again; none stayed pending in this run). In this week: seven calls, 516 group-and-question checks, 2 linked (both to the Vera
Rubin question); of the 196 links, 194 were made when the statement's article was read and 2 by this step. **A group whose original
arrived under another question is excluded, even if the new question also needs it:** e379 (the group `163:e3` in the stored
library) arrived linked to the export question at article 163, so it was not among the 166 checked when the RTX Pro 5500 question
opened at article 169. The counts and findings of this page do not change; the description of the cause does: the
case is "linked elsewhere and so never reconsidered", not "nothing looks back". Production does not link an earlier record to a
question opened later (D456: none of 3,225 links in six draws points back; a later article that repeats the fact can still deliver
it; `clean-arch/e2e-comparison-2026-11-13/unlinked-trace/UNLINKED-TRACE-RESULT.md`, which found that in those draws, on the graded
questions of the July window, such unlinked facts cost no final answer).
