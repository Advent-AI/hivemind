# How clean Step 1 cuts a matter into theses: diagnosis (D432, 2026-11-12), version 8

Alex chose this next (D432: "先查清第 1 步怎么切题"): a source-by-source diagnosis of the nine graded questions the unseeded draws
did not open, the eight theses with no ladder and the remaining Stage A faults, with one proposed change, before any build.
Added from Stage B: the trace of its lost controls (`clean-arch/step4-2026-11-10/stage_b/CONTROL_TRACE.md`). Step 1 is c8 (D387),
frozen until Alex opens a new version.

Version 1 of this page said c8's prompt does not carry D38's unit. **That was wrong** (council `lc-codex.md`): c8 says "A thesis
asks one quantity for one period, or one event", and a shared quantity is "for this or next calendar year". I had searched the
request for other words and not read the whole of section 3 (AGENTS §1, "the whole request read as the model reads it"). This
version starts from the model's own account of its choices.

Sources: the unseeded draws' Step 1 requests and answers (`poc/data/clean-unseeded-2026-11-10/draw-d*/trace.sqlite`, read-only),
their opened theses (`clean-arch/unseeded-2026-11-10/opened-u*.json`), the result (`result.txt`, `adjudication-runs.md`, round
log §67), Stage B's no-ladder reasons (`clean_ladders`), the c8 request as sent, the decisions D38, D210, D248, D397, and the
model's own account of six choices (`model-account.json`, `model_account_choices.py`: each stored conversation continued with
one question; 50,865 tokens in, 4,456 out on DeepSeek Flash, about $0.02 at the published rates).

## The answer

c8 states the unit; the model's own account points to its merge rules (a lead, below). The prompt says in four places, each with its own
scope, that a matter already asked is not asked again: "Another population or wording of the same aggregate is evidence for it"
(shared_quantity); "do not open a thesis about … another estimate, source or wording of what an open thesis tracks"; "the
closest open thesis with why an analyst would bet on the two separately because their answers can move apart … If the two cannot
move apart, link the evidence"; and, in the closing check, "A new thesis that asks the same underlying question, about the same
subject and scope, as an open thesis or another new thesis is not proposed". None carries the boundary Alex set on years (D38:
"yes to one view per year (this year and next)"); none carries D388's signing exception either.

Asked which instruction led it (`model-account.json`; leads, not proof: each question names the thesis not opened, so it can lead
the reply, council `ld-codex.md`), the model named a merge rule in 4 of the 5 cases about these two kinds: two of the three
capital-spending draws (d1 names two merge sentences and says it weighed the one-period sentence; d2 names the same-question rule)
and both Ohio draws ("the scoping rule wins"). The third capital-spending draw (d3) names no merge rule: it cites the
shared-quantity and one-period rules and says it chose 2027 as the bet, adding that "an experienced analyst would track both
years". Two of the three capital-spending replies say an analyst would track both years.

**The Ohio part is not new and is not proposed again.** D388 (Alex: "单独开") already decided that a material unsigned obligation
keeps its own signing question beside a total of its kind, with D389's size line and D390's plan rule. The focused call that
carries them opened Ohio in 36 of 36 draws but opened one wrong neighbouring case each round, and Alex closed Step 1 on c8 (D391)
with the rule "a fix that keeps moving its error to neighbouring cases stops being tuned on that set". It stays a tested
candidate, not adopted.

## The cases, one by one

### The nine graded questions not opened

| ruler question | missed in | what Step 1 did | the model's account |
|---|---|---|---|
| q04 (2026 capex), q13 (2027 capex) | q04 in d1, d3; q13 in d2 | The 2026-07-04 article gives the 2026 plan (~$650bn) and NVIDIA's 2027 projection (~$1tn). Each draw opened one thesis: d1 and d3 on 2027 with 2026 as its base, d2 on 2026 with 2027 as its benchmark; later articles with both years were filed under it. | d1: "I treated both years as one aggregate: 'Another population or wording of the same aggregate is evidence for it,' and 'A new thesis that asks the same underlying question … is not proposed'. Against those I weighed … 'A thesis asks one quantity for one period,' which would have permitted a separate 2026 card." d2: the same rules; an analyst "would arguably have opened 2027 separately". d3: "an experienced analyst would track both years". |
| q05 (2027 vs 2026 memory contract prices) | d1, d2, d3 | Three different things. d1 opened prices "through calendar 2026–2027" (no ladder: not one calendar year). d2 opened HBM capacity together with whether record prices persist (no ladder: two events) and left the 2026-07-07 price statements unfiled. d3 opened HBM capacity only and filed a price statement under supply commitments: the price question was not chosen at all. | d1: "spanning two years was a slip: the rule allows one calendar year … It should have been 2027 contract prices versus 2026." (d2, d3 not asked.) |
| q09 (credit support at FY2027 year-end) | d2 | Opened at a 2027-12-31 check date: c8's date for an unsigned obligation applied to an undertaken amount ("one already undertaken is tracked by its amount at the next annual report"). | not asked |
| q23 (Ohio guarantee signed by 2027-06-30) | d2, d3 | With clean-1 (the credit-support amount) open, d2 and d3 linked "NVIDIA has been negotiating to guarantee OpenAI's Ohio lease" to clean-1; d1 opened a signing thesis (with its amount in it). | d2: "Signing the OpenAI guarantee is a component of that amount, so the two cannot move apart." d3: "binding_obligation needs a check date; but the scoping rule wins." |

### The eight theses with no ladder, and the remaining Stage A faults (each read against the Step 1 answer that opened it)

| case | how Step 1 opened it (stored answer) | the ladder step's reason | where it goes wrong |
|---|---|---|---|
| u1 clean-5 | memory contract prices "through calendar 2026–2027" (shared_quantity); the article: "For any organization budgeting AI infrastructure for the second half of 2026 and beyond …", "the organizations planning capacity for the next two years" | not one calendar year | **Step 1 against c8** ("for this or next calendar year"; "one quantity for one period"): the article's two-year budgeting horizon became the period; the model: "a slip" |
| u2 clean-10 | HBM capacity **and** whether record prices persist through late 2027; the article joins them in one sentence: "no new HBM supply arrives before late 2027, keeping record prices intact" | two events, neither main | **Step 1 against c8** ("one quantity for one period, or one event"): the article's one sentence became one thesis with two outcomes |
| u3 clean-11 | the split of 2027 accelerator spending, "(and of the 19.5 GW of incremental compute capacity …)" in brackets; the article: the four "are forecast to spend over $1 trillion on AI infrastructure next year, adding 19.5 gigawatts (GW) of incremental compute capacity" | two figures, neither main | **the ladder step's wrong refusal**: the outcome leads with one figure. Stage A's agreed rulings count this decline (u3/clean-11 sends 1 and 3) and acc/clean-9 send 2 (global chip revenue "and the AI-chip portion of it") as unjustified; asked, the model says its decline "was incorrect" and "I over-applied the instruction" (`stage_a/result-4/RESULT.md`); earlier runs laddered both every time |
| u1 clean-9, u2 clean-8 | China's domestic share of AI-accelerator budgets "over the 12 months following the July 2026 survey", settled by "a follow-up … survey". The articles: "Executives … will allocate 46 per cent of their budget for AI accelerators to domestic products over the next 12 months … according to a Bloomberg Intelligence survey released on Tuesday (Jul 7)" (d1); "Industry surveys indicate Chinese firms plan to shift 46% … within 12 months" (d2). Neither names a follow-up survey or its date. | a rolling 12-month period, no publication day | **Step 1 against c8**: a shared quantity is "for this or next calendar year" with "its release date", and "A question no date can settle is rewritten or not opened" |
| u1 clean-10 | a US ban on Chinese-made lidar (policy_stage); its own reason says every open thesis is about NVIDIA's data-centre business. The article is about Hesai, "a Shanghai-based lidar manufacturer blacklisted … by the U.S. Department of Defense", and the physical-AI build-out that "depends on high-tech, low-cost lidar"; it names no effect on NVIDIA | no theme covers lidar | **Step 1 against c8**: "small matters open no thesis" (no named effect on NVIDIA's revenue, profit, cash or credit risk) |
| u3 clean-4 | Huawei and SMIC's combined 2026 AI-chip output (shared_quantity: "several companies' combined output"); the article: NVIDIA's own report "estimated that by the end of this year SMIC … will have made more than 700,000 Ascend 910C chips" and "If Nvidia is kept out of the China market, Huawei production and sales will soar" | "a figure about other companies … no object here" | **the two steps disagree**: c8's shared_quantity admits a rival's combined output; the ladder step has no object for it |
| u3 clean-2 | the CPU-to-GPU ratio in inference in 2026 (shared_quantity), settled by industry data; the article quotes Intel's CEO: "In inference workloads, we're starting to shift from 1 CPU to 8 GPUs towards 1 CPU to 1 GPU" | no listed theme covers it | **the two steps disagree** on where an industry measure belongs, and the settling release is loose |

So five of the eight are Step 1 breaking rules c8 already states (two years or two events; a rolling period; a small matter),
one is the ladder step's wrong refusal of a thesis that leads with one figure, and two are a contract gap between c8's
shared_quantity and the ladder step's object and theme rules.

### Every fault the fourth Stage A run recorded (`stage_a/result-4/RESULT.md`), all of them

The run's own summary: "five [of the six answers behind lines 1, 3 and 4] are on four theses whose own outcome names two things or
two periods … The sixth, acc/clean-2, has an outcome that reads 'closes (or abandons/restructures)'."

| fault (send) | the Step 1 thesis's words | where the fault is | Step 1's part |
|---|---|---|---|
| line 1: u1/clean-6 s3, Kyber "by December 31, 2028", both branches Yes | "reach first shipments in 2027 as originally planned, or slip to 2028"; period "2028" | the ladder step ("cannot tell the two apart", council `ke-codex.md`) | an outcome with two periods, and the 2028 period |
| outside the lines: u1/clean-6, two sends asking about 2027 due at the end of 2028 (upheld by two third readers) | as above | the ladder step's due day | the 2028 period |
| line 3: u3/clean-7 s3, Kyber question "in calendar 2028", Yes "by 2028-12-31" | "reach first shipments in 2028 … versus the original 2027 schedule, and whether the larger NVL576 … ships in volume" | the ladder step (question and condition disagree) | the article's date as the question, and a second outcome (NVL576) |
| line 3: acc/clean-2 s3, a "restructuring" counted as ruled out | "Whether Nvidia closes (or abandons/restructures) the announced $12.9 billion purchase" | the ladder step's ruling out | "restructures" written beside "abandons" |
| line 4: u3/clean-11 s1, s3; acc/clean-9 s2, declined for two figures | a spending split "(and of the 19.5 GW …)"; chip revenue "and the AI-chip portion of it" | the ladder step's wrong refusal (the model: "was incorrect") | an outcome naming a second figure beside the main one |
| outside the lines: acc/clean-3, one send takes the "up to $105 billion" ceiling as the reference (both readers) | "after agreeing in August 2026 to provide guarantees of up to $105 billion"; the article: "agreed to provide guarantees of up to $105 billion for a data center project in Ohio" | the ladder step (a ceiling is not an expectation) | none: the ceiling is the article's fact, correctly carried |
| outside the lines: a year carried as the reference's number on eight event ladders | — | the ladder step | none |
| outside the lines: u1/clean-10 s3, the lidar ban filed under the export-controls theme (both readers) | the lidar thesis (see the no-ladder table) | the ladder step's choice of object | opening a small matter (c8: "small matters open no thesis") |
| declines that moved between sends (27 against 24); u1/clean-5 declined in every send | u1/clean-5 "through calendar 2026–2027" | the ladder step (moved declines); u1/clean-5 is declined rightly | u1/clean-5's two-year period |

So every recorded Stage A fault is the ladder step's, and in six of the nine rows a Step 1 wording is the input it mishandled: an
outcome that also names a second period, event, figure or alternative, a 2028 period taken from the article, or a small matter
opened. These shapes are **a class to investigate**, not one established Step 1 fault: some are Step 1 breaking c8's "one quantity
for one period, or one event" (u1 clean-5, u2 clean-10), some are thesis wording with a main question and extra parts that D397
allows, where the ladder step erred (u3 clean-11 and acc/clean-9 wrongly declined; the Kyber question the council puts on the
ladder step). Stage A's accounts are the ladder model's; they do not say why Step 1 wrote each thesis so.


### Stage B's lost controls (`CONTROL_TRACE.md`, leads)

Several question differences are the article's angle written into the thesis (a programme inside a total, the article's reported
date, a later milestone). The pairing rule counts them as one matter (D248), but the trace leaves open whether each is Step 1's
narrower question or the comparison's breadth, and the pairing readers disagreed on two of them (u3/clean-7, u3/clean-5). Two missing items (analysts' NVIDIA growth forecast; the memory share
of data-centre spend) are stored with no link although the capex thesis was open. d1's account of the 2026-07-04 article adds that
it left the 82%/41% growth forecast unlinked under "Do not open a thesis about … a financial measure's level, growth, margin or
guidance for any period, on its own": a rule about opening, applied to linking.

## Counted by mechanism (cases overlap where one thesis is in two populations)

| mechanism | graded misses | no ladder | the model's account (leads) |
|---|---|---|---|
| a second year of an annual quantity not opened | 3 (q04 ×2, q13) | — | 2 of 3 name a merge rule; 1 chose one year as "the bet" |
| a material unsigned obligation folded into a total (D388's line, stopped by D391) | 2 (q23) | — | 2 of 2 name a merge rule |
| an outcome with a second thing in it (two periods, two events, a second figure, an alternative) | 1 (q05 d1) | 2, and u3 clean-11 wrongly declined | 1 asked: "a slip"; Stage A: 5 of the 6 answers behind its missed lines, every account "its own slip" |
| the ladder step wrongly declines a thesis that leads with one figure | — | 1 | Stage A: "was incorrect" |
| a rolling period or a small matter, against c8's own rules | — | 3 | not asked |
| c8's shared_quantity and the ladder step's object and theme rules disagree | — | 2 | — |
| the price question not chosen (capacity instead) | 2 (q05 d2, d3) | — | not asked |
| a date rule misapplied | 1 (q09) | — | not asked |
| the article's angle; indirect evidence unlinked | — | — | leads (Stage B controls) |

**Two classes stand out.** The year class removes whole graded questions (3 misses). The second-thing shapes sit under most of
the ladder step's recorded faults and refusals (Stage A's lines 1, 3 and 4) and one graded miss; how much of that is Step 1's is
still to be investigated. The ladder step's reasons for the eight no-ladder theses are its stated reasons; they do not show by themselves that each thesis
was wrongly opened. The first row is the largest graded class that no earlier line has worked on, and its source is Alex's.

## The one proposed change (for Alex; nothing built, nothing sent)

**Why this one first, of the two classes:** the year change is sourced in Alex's own words (D38), two sentence edits (+206
characters), testable on stored articles for cents, and its target, a whole question that does not open, is what the graded
measure and Alex's end-to-end gate (D427, D431) count. The second-thing shapes weigh more in the ladder step's faults, but which of
them are Step 1's, and what lever would hold, is not yet known: it is the next class to investigate, recorded here, not proposed.

**Carry D38's year boundary into the two merge sentences that decide it, for yearly quantities only.** Two edits to c8's
request, nothing removed. In shared_quantity, the sentence

> Another population or wording of the same aggregate is evidence for it.

becomes

> Another population or wording of the same aggregate is evidence for it. Its figure for another year is a separate quantity, not
> another wording: this year's and next year's figure are two theses when an analyst would bet on each.

In the closing check, the sentence

> A new thesis that asks the same underlying question, about the same subject and scope, as an open thesis or another new thesis
> is not proposed: link its evidence to that thesis.

becomes

> A new thesis that asks the same underlying question, about the same subject and scope (for a shared quantity, the same calendar
> year), as an open thesis or another new thesis is not proposed: link its evidence to that thesis.

The closing-check edit is limited to shared quantities by calendar year (councils `le-codex.md`, `ll-codex.md`): an event under
another deadline stays one bet (D248), and a company's fiscal year is not touched. The wording was settled before any send after a
blind read found the first version barred another year's figure as evidence.

- **Size:** +206 characters on a request of about 29,400 (0.7%); an estimated +47 prompt tokens at the 4.4 characters a token
  measured on these requests (an estimate, labelled as such). The written reason for the growth (AGENTS §6): the boundary is
  missing at the very sentences the model cites, and the four merge passages are not duplicates of one another (council
  `ld-codex.md`), so none can be cut without changing what c8 gets right.
- **Sources:** D38 ("yes to one view per year (this year and next)"; "a view … looks at one number (which year …)"); c8's own "for
  this or next calendar year" and "one quantity for one period". The opening standard is kept ("when an analyst would bet on
  each"; c8 already refuses "an annual quantity after next year").
- **The expected effect on the judgement, named first (D391; not measured):** the second year's question exists, so its evidence
  can be judged instead of sitting as a benchmark inside the other year's question; on the graded subset, q04 or q13 would open in
  the draws that miss it today.
- **The known risk (round log §§49–58, D388):** a sentence-level rule flipped by send there. So the first test is several sends,
  not one, and it has a stop line before any fresh articles.
- **The first test (opened by Alex, D433), staged.** *Cost correction:* the full design is about $2.0 at the stored mean of 9,490
  output tokens a call, not the "about $0.5" first stated (that figure left out output tokens). **Stage 1, the main case only**
  (c8 and c14, three sends from each of the three draws' stored state, 18 sends, about $0.25, within the approved amount). A stage-1
  pass leads to **stage 2, the controls below**, only after Alex's word on their cost (about $1.75); not to fresh articles. A stage-1
  fail stops the line and goes to Alex. Before any send ($0, `preflight-c14.output.txt`): production's adapter rebuilds every
  stored sent request byte for byte for the c8 arm; the arms differ only in the two passages; every stored answer passes the
  runner's checks; a synthetic two-year answer passes. Each case re-sent from each draw's stored state, three sends per draw for
  **both arms, c8 and the candidate**, so send-to-send variation is measured on the same states:

  | case (stored article) | c8's stored behaviour | expected under the candidate | stop line |
  |---|---|---|---|
  | **stage 1:** 2026-07-04, both years of hyperscaler capex (d1/d2/d3 step 42) | one year opened, 3 of 3 | both years open | read by hand: two distinct, valid, retained theses, each asking one of the two years, in at least 8 of 9 c14 sends **and** in at most 2 of 9 c8 sends; otherwise stop |
  | the same article, duplicates in one answer | — | exactly two capex theses, not three | any send with a third capex thesis |
  | 2026-07-07 articles repeating $650bn and $1tn (steps 85, 90), one year open | linked | link; may open the missing year | a new thesis on anything else |
  | another population of the aggregate (Goldman's broader AI-infrastructure estimate) | evidence | evidence, no new thesis | a new thesis in more sends than c8 |
  | an event under another deadline (the Kyber delay article) | one thesis | unchanged | a split into two |
  | a signed programme and a small obligation (NVIDIA's credit-support announcement, step 1) | one amount thesis | unchanged | a new signing or amount thesis |
  | a company's own figure for both a fiscal and a calendar year (the audit's watch point; an article to be chosen before stage 2) | — | one thesis at most (D248 boundary 4) | two theses for one company quantity |
  | a two-year comparison (memory prices, d1 step 56) | "2026–2027" | not expected to change; a "2027 against 2026" opening is reported apart | a blind reader marks, for every send of both arms, each memory thesis as asking a price for one year, the change from 2026 to 2027, a span of years, or not a price; stop if the candidate has no price thesis, or loses a change question c8 asked, in more sends than c8 (by more than 2 of 9); the price statements left unlinked count the same |
  | the Ohio article (step 8) | linked in d2, d3 | unchanged (not this change's target) | the candidate's count of sends that open the signing question differs from c8's by more than 2 of 9 |

  "More sends than c8" in a stop line means the candidate's count over its nine sends exceeds c8's count over its own nine by more
  than 2, a margin fixed before the send. It is a declared tolerance, not proof that nothing was lost: every send's result is
  reported, case by case.

  A pass of both stages justifies the comparison of c14 against c8 on fresh articles (D386's protocol), with readers marking each year thesis as a
  bet or trivia, evidence spanning both years checked for links to both, and no opening or link c8 got right lost. It does not
  establish a general improvement.
- **Not addressed** (later, one class at a time): the second-thing shapes (next to investigate); Ohio (D388's line, closed by D391); two outcomes in one thesis; the price question
  not chosen; the misapplied date; theses no release settles or outside the company's matters; the article's angle; unlinked
  indirect evidence, including d1's account of the opening rule ("a financial measure's level, growth … on its own") applied to
  linking.

## Limits

Three draws of one window, NVIDIA only; seven graded questions; the model's account was asked on six choices, names the thesis
it is asked about and so can lead the reply; it locates the instruction, it does not prove the fix. The Stage B controls are leads.
