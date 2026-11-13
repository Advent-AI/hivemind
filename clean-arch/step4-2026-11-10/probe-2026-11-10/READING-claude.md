# The six-request probe (D402): my reading of each answer beside its article, written before any other reader's

Sent 2026-11-10 with `run_probe.py`: the request of design version 30, once, on six stored theses; gpt-6-luna, medium effort. All
six came back valid against the schema; five ladders and one refusal; $0.0059 from tokens. Six answers, one draw: this shows what
the model did here, and nothing of how often. No check of the step was applied; where I say a check "would" refuse, I ran the
design's rule on the answer by hand or with production's functions.

| case | chosen for | what the model wrote | read against the thesis and the article |
|---|---|---|---|
| u1/clean-3 | a yes/no event | "Will NVIDIA begin first shipments of its Vera Rubin AI chip platform by December 31, 2026, as established by NVIDIA earnings releases, regulatory filings, or shipping confirmations?"; Yes and No; reference "could begin shipping later this year", no value; due 2026-12-31, basis stated | As designed. The question names the day and the settling material; No is the complement of Yes; the reference's words are in the article word for word |
| u1/clean-2 | several things; a binding obligation | judges the signing by 2027-12-31; lists as not judged the amount, and whether it is large enough to change credit risk, each with a reason; no reference | As designed (D397): the main thing judged, the two other parts listed with reasons |
| u1/clean-7 | a company's figure | commitments in the FY2027 10-K; ranges below 70bn, 70 to 100, 100 to 140, 140 to 180, 180bn or more; lower is favourable ("less future purchasing exposure"); reference "The $119 billion cited in this item", value 119bn; due 2027-02-24, expected publication | Ranges, direction and due day are sensible. **Three faults.** (1) The reference's words are not the article's: they are the thesis's own phrase; the article says "Nvidia's $119B in supply commitments hinge on …". Check 6 would refuse the answer. (2) $119bn is today's amount, not what the market expects: it is not a reference as the request defines one. (3) The question says "compared with the $119 billion cited in this item": a later judge cannot see "this item" |
| u1/clean-4 | a theme's figure with a reference | the four hyperscalers' combined capital spending for calendar 2027; theme `ai-capex`; ranges below 800bn, 800 to 950, 950 to 1,050, 1,050 to 1,200, 1,200bn or more; no favourable end; reference value $1tn; lists "whether it reaches $1 trillion" and Nvidia's dependence as not judged; due 2028-02-15 | Ranges sit round the stated $1tn; the year is the calendar year; the theme is right. **One fault:** the reference's words are "Nvidia projects that this figure could reach $1 trillion next year."; the article says "Next year, Nvidia projects that this figure could reach $1 trillion." The model moved two words. Check 6 would refuse the answer |
| u3/clean-12 | an event with more than two states | theme `chip-export-controls`; question "By January 31, 2027, will the US Commerce Department … have issued a binding export-licensing rule or other formal escalated export-control restriction …?"; five states labelled Strongly bearish to Strongly bullish; due 2027-01-31, period end; lists the effect on Nvidia's sales as not judged | The five states follow the construction (issued: with or without a licensing requirement; not issued: a proposal pending, decided against, or neither) and I find no overlap or gap. **Two faults.** (1) It is a theme, and the states carry the company's bullish and bearish labels, which D38 rules out for a theme; the design's check 3 would not refuse it, since the five labels are five different names. (2) The question is worded as a yes/no question and answered with five states |
| u2/clean-10 | two things, neither the main one | declined: "The topic names two tracked outcomes … but neither is identified as the main one." | As designed |

## What I take from it

- The request works at the level it was written for: one main thing judged and the rest listed, a refusal where there is no main
  thing, ranges set round a stated reference, a favourable end with a reason, due days that follow the rules, five states built by
  the construction.
- **Largest problem: the reference quote.** Three answers carried a reference with words taken as a quote; two of the three are not
  the article's words (one rearranged, one taken from the thesis). The design refuses such an answer and asks again. On this
  showing that would happen often.
- **A hole in the checks the reviews did not find:** a theme's states named with the company's five labels pass check 3.
- Smaller: a reference that is today's level and not an expectation; "this item" inside a judged question; a yes/no wording over
  a five-state ladder; `stated` chosen where the day is also the end of the thesis's period (clean-3, clean-2), which the request
  leaves open.

## The cold reader (`clean-arch/step1-unfiled-2026-11-08/council/in-codex.md`), and where we differ

A fresh Codex session read the same six answers beside their requests before opening this page.

**Agreed:** the two reference quotes that are not the article's words; today's $119bn presented as an expectation; "this item" in
a question; the company's labels on a theme's states; the yes/no wording over five states; the justified refusal; the ranges of
both figures joining with no gap or overlap; the Ohio answer as a defensible reading of D397.

**What it saw and I did not:**
- **u3/clean-12, an overlap I missed.** The agency could decide against one restriction while a proposal for another is pending:
  the "Neutral" and the "Bullish" states would both hold. I had written "no overlap or gap". Its case stands. So the one answer
  with five states fails the rule that exactly one state holds.
- **u1/clean-4, the four companies are never named.** A later judge cannot know whose spending to add. I checked the article: it
  does not name them either ("several AI hyperscalers"), and the thesis says "the big four". The model wrote from the item only,
  as told; the gap comes from the article and the thesis, and the question passes it on.
- **u3/clean-12** drops "beyond its May 2026 guidance", the comparison a later judge needs to know what counts as escalation.

**Where it reads more strictly than I do:** "could begin shipping later this year" (clean-3) as a possibility more than a plan;
`period_end` as the truer basis for a day that is the end of the thesis's period (clean-3); "lower is favourable" for
commitments as not certain (clean-7).

## The classes, after both readings (six answers, one draw)

| class | where | what the design does with it today |
|---|---|---|
| the reference's words are not the article's | 2 of the 3 answers that quote one (clean-4 rearranged; clean-7 took the thesis's phrase) | check 6 refuses and asks once more; on this showing, often |
| a question that does not stand on its own for a later judge | clean-7 ("this item"); clean-12 (the May 2026 guidance dropped); clean-4 (four companies unnamed, inherited from the article) | nothing in the request asks for it; a reader could name it only under W |
| a theme's states carrying bullish and bearish labels | clean-12 | check 3 lets it through: five different names |
| five states that overlap; a yes/no wording over five states | clean-12, the only answer with states | marks R and Q, in Stage A |
| a present amount recorded as an expectation | clean-7 | mark XR, in Stage A |
| `stated` or `period_end` for a day that is both | clean-3, clean-2 | the request leaves it open |

## The second and third sends (D404), read the same way

Spend for everything in this folder: $0.035 from tokens (three sends of six, the re-sends of one case, the isolation arms, the
model's accounts). One draw a case unless a count is given.

| | first request | second: three changes and the closing check's three tests | third: the refusal test put first in the closing check |
|---|---|---|---|
| quoted references that are the article's words | 1 of 3 | 4 of 4 | 4 of 4 |
| a question that says "this item" | 1 of 5 | 0 of 6 | 0 of 5 |
| the theme's five states (u3/clean-12) | the company's bullish and bearish labels | named by outcome; no overlap | **the company's labels again** |
| the topic with no main thing (u2/clean-10): declined | **4 of 4** | **0 of 4** (two pick one of the two things, two join them) | **2 of 4** |
| the capital-spending question names four companies the article does not | no (unnamed) | yes | yes |
| a present amount recorded as an expectation | u1/clean-7 | u1/clean-7 | u1/clean-7, u3/clean-12 |

**Reading.**
- The exact-copy sentence and the stand-alone sentence held in both later sends.
- The theme's-names sentence did not hold: names in one draw, the company's labels in the next. A sentence does not own this; the
  check that refuses a company label on a theme state does (D404), and a separate answer shape for a theme's states would make
  the mistake impossible to write.
- The refusal went from 4 of 4 to 0 of 4 with the changes and to 2 of 4 with the refusal test put first. Each change alone left
  it at 3, 3, 2 and 3 of 3 (`isolation-clean-10.json`). No single sentence is the cause; the cause is not established. The model's
  account is that it read "the state of HBM supply and pricing" as one thing.
- "Must stand on its own" made the model supply four company names from outside the item.
- **I am now tuning sentences on six cases with one draw each, and each change moves a neighbouring case.** That is the pattern
  AGENTS §7.3 says to stop: the call is doing several jobs, and the rules that keep slipping (decline or not; a theme's names)
  belong in the answer's shape, not in more sentences.

## The fourth send (D406: the answer's shape) and the control it lacked

Eight topics, three sends each, with two new first fields (`named`, `main`) and separate shapes for a company's and a theme's
states (`answers-round4.jsonl`, $0.0226); then the request as first sent, three times on each of the two topics it had never
been sent on (`control-first-request.json`, $0.0038).

| the three topics with no main thing: declined | first request | fourth request |
|---|---|---|
| u2/clean-10, HBM supply and prices | 4 of 4 | 2 of 3 |
| u1/clean-5, memory prices and a rack's memory cost | 3 of 3 | 3 of 3 |
| u3/clean-10, new HBM capacity and whether it arrives early | 3 of 3 | **0 of 3** |
| in all | **10 of 10** | **5 of 9** |

- **The line I fixed before the send (8 of 9, none fewer than twice) is missed.**
- u3/clean-10 under the fourth request: all three sends put "the combined new HBM capacity added in 2027" in `main` and wrote a
  figure for it, in a unit the article does not give (wafer starts a month, three wordings). The field that was meant to make
  the model decide first made it pick: asked for a main thing, it names one.
- The five topics that should be answered: a ladder in 15 of 15; each `main` the thing earlier sends judged. The states ladder
  sat in the theme's shape; no company label on a theme. The export-controls topic came out as five states once and as a yes/no
  question twice: its outcome begins "Whether …", and both are readings of it.
- All 13 quoted references are the article's words; no question says "this item"; the Ohio answer lists the amount in all three
  sends and the credit-risk condition in two.

**What the four sends say together.** On deciding whether a topic should be judged at all, the first request is the best of the
four: 10 of 10. Every later request did the writing better and that decision worse: 0 of 4, 2 of 4, 5 of 9. The three faults of
writing are ones code can see (words not in the article; a company label on a theme; "this item"); the decision is not. So the
request should keep the decision and code should own the writing. D406's first field was my recommendation and it was wrong.

## The last send (D407), with its control in the order sent

A correction first. My re-sends, isolation arms and first control took requests from the model archive, whose JSON has its keys
sorted: in them the answer's fields stood in alphabetical order, not in the order first sent. The counts above that rest on them
("10 of 10", "0 of 4", "2 of 4", the isolation arms) are of that sorted request. This last send and its control are all in the
order sent (`answers-final.jsonl`, $0.0211; `control-first-as-sent.json`, $0.0162).

| eight topics, three sends each | the arm: first request + exact copy + stand-alone + two state shapes | control: the first request |
|---|---|---|
| the three with no main thing: declined | **6 of 9** (3, 3, 0) | **8 of 9** (3, 3, 2) |
| the five others: answered with a ladder | 15 of 15 | 15 of 15 |
| quoted references that are the article's words (check 6 would accept) | 12 of 12 | **3 of 10** |
| a theme's states with the company's labels | 0 | 1 |
| a question that says "this item" | 0 | 0 |

- **The line set with Alex (8 of 9) is missed by the arm.** By D407 the build uses the first request unchanged; the faults of
  writing are refused by code and sent back once.
- The swing topic is u3/clean-10 (new HBM capacity, and whether it arrives early): the arm answers it in all three sends; the
  first request declines it in two of three.
- The cost of the first request is plain in the control: seven of ten quoted references are not the article's words, so most
  answers that carry a reference will be sent back once. How many are right on the second send no probe here has measured;
  Stage A will.
- Probe spend in all: $0.105.

