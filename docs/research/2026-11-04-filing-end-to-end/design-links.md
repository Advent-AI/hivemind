# Design: the links rule that files the way an analyst links (PRD 10 §5, step 1) — draft 3

2026-11-04. Governing page: `docs/prd/10-filing-phase.md` (read before every step). Base: extraction v74i (`poc-v108`, frozen, D274). New
version name **v74l**, configuration **poc-v115** (both never used anywhere in the repository; v74k and poc-v109 to poc-v114 were used and
retired, `retired-2026-11-03/manifest-sha256.txt`, so reusing them would give one name two meanings, AGENTS §3). Exact texts: `links-v74l.json`
(the same rule and role edits as arm `v74l` of `links-rules.json`). Nothing is built into the package.

Draft 1 was reviewed by Codex (`review-links-codex.md`) and an independent reader (`log.md` row 10); draft 2 by Codex (`review-links-codex-r2.md`)
and a second reader (row 11); its amendments by Codex rounds 3 to 7 (`review-links-codex-r3.md` … `-r7.md`; rows 12–16). Round 5 found the rule
text and the request builder ready; round 7 found nothing serious in the decision rule. Draft 3 answers every serious finding (§7).

## 1. What the request says about filing (audit, prompt-audit skill)

| Place | Text (v74i) | Verdict |
|---|---|---|
| role, first paragraph | "each with its takes line, which says what belongs in that question's file" | contradiction: makes the takes line, which names only the question's own quantity, the authority on filing |
| role, first paragraph | "file each one through its links, as the schema's links field says: the narrowest open question whose takes line covers it" | contradiction: "covers" is the literal reading the model gave in its own words ("not a figure for cloud-provider spending") |
| role, first paragraph | "A takes line says where a material statement goes, never that a statement is material." | contradiction: same authority given to the takes line |
| takes line of a figure question | "takes: <measure> figures, guidance, estimates and revisions for <scope>, this question's period …" | consistent with its job (what the question measures); unchanged |
| links field | "… as that question's own figure, step or estimate or through the demand, supply, competition or pricing behind its answer" | abstract: one clause for every indirect relation, applied differently per send (AGENTS §6); the relation is stated, not absent |
| links field | "compare the specific questions before a company-wide revenue or margin question and take that one only, never a broader question beside it" | consistent; the model quoted it when it judged its revenue links wrong (`probe-filing-account-d1.md`); kept verbatim |
| links field | "when no specific question is connected, a statement that moves the demand, supply, competition or pricing behind the company's results goes to the company-wide revenue question of its period" | D273's deliberate exception to the standard §6 ("没有问题接，记 no home 扔掉"), frozen by D274; removed under PRD 10 §5 (Alex: "好你去解决问题", "开始做") |
| links field | nothing says which of two specific questions takes a statement that bears on both (a seller's price: its product revenue or its buyers' spending) | missing (Codex r2, r3): one home (D207) with no rule to choose it is a coin flip per send |
| closing check | "a supplier's capacity, output, prices or revenue on supply and input costs" (among others), "the analyst supplies the connection" | consistent; the new list keeps every relation it names (reverse audit) |

## 2. The change

1. Role: the three sentences give the takes line its own job and leave filing to the field:
   - "each with its takes line, which says what belongs in that question's file" → "each with its takes line, which names what the question measures";
   - "file each one through its links, as the schema's links field says: the narrowest open question whose takes line covers it, your own candidate,
     or both." → "file each one through its links, as the schema's links field says.";
   - "A takes line says where a material statement goes, never that a statement is material." → "A takes line names what a question measures, never
     that a statement is material."
2. Links field (`links-v74l.json`, `rule`): the abstract clause becomes five ways a statement bears on a question, each with three examples from
   other industries; the compare-first sentence is kept verbatim; the fallback sentence is deleted; everything else is kept verbatim. The five ways:
   (1) the question's own figure, step or estimate, or the same quantity for another period or population when no open question covers that one;
   (2) a part or input of the question's figure: a segment's sales for the total, a product's price or volume for its revenue, an input's cost for a
   margin, profit for earnings per share; (3) the other side of the same purchases or the demand behind them: what suppliers sell to the buyers the
   question counts, what those buyers order or book, the demand that drives the buyers' spending; (4) a variant, stopgap, key part or schedule change
   of a product or project, for its event question; (5) a customer's, supplier's, competitor's or market's figure, forecast or action that changes the
   demand, supply, competition or pricing behind the answer.
3. One home stays (D207), and two sentences settle the cases one home left open:
   - "When it bears on two specific questions, take the one whose quantity it measures most directly (a hotel chain's room rate, under its
     room-revenue question rather than travellers' spending question; a parts maker's sales to carmakers, under the carmakers' parts-spending question
     rather than a rival parts maker's share question)."
   - "A statement that gives a separate figure for each of two questions (a drug maker's sales of two drugs in one sentence) is written as two
     evidence items, one under each." Each figure keeps one home; when both items quote the same sentence the code stores one piece with both links
     (`extraction.sift`: "the same sentence read out twice is one piece with both links"), so each judge reads the sentence.
   The draft-1 clause that filed one fact under both sides of one sale is dropped. PRD 10 §5.2's second half ("另一方的题开着…一并挂上") departs
   from Alex's D207 and is proposed for striking (`prd-amendment-proposal.md` §2).

## 3. Each clause against its source, both directions

| Clause | Source | Verdict |
|---|---|---|
| narrowest open question whose answer it makes more or less likely | standard §6, §5.1; D207, D265 | consistent (verbatim) |
| (1) own figure, step or estimate; another period or population | §5.1 kinds 1, 3; D248, D268 (v74i's period-population clause moved here) | consistent |
| (2) part or input: segment for total, price or volume for revenue, input cost for margin, profit for EPS | §5.1 four paths (supply/input costs, pricing, demand); D259 "what makes that figure more or less likely"; closing check "supplier's … prices … on supply and input costs" | consistent; restores what draft 1's list lost (Codex r1: memory cost → gross margin) |
| (3) other side of the same purchases, the demand behind them | §5.1 kind 2 (a customer's or supplier's figures) and its own example (a cloud provider's backlog); D259 | consistent; worded "bears on", never "measures" (audit r1) |
| (4) variant, stopgap, key part, schedule change → event | D259's event takes line; §5.3 product-progress boundary | consistent |
| (5) customer's, supplier's, competitor's or market's figure, forecast or action | §5.1 kinds 2 and 4 (named party's estimate), "有规模、有日期或有名字"; §5.2; D259 | consistent; the same breadth as v74i's clause, now with examples |
| compare-first, never a broader question beside it | v74i; D207; D265 | consistent (verbatim) |
| tie between two specific questions: the one whose quantity it measures most directly | D207 (one home); §6 narrowest; Codex r2, r3 (a seller's price between its product revenue and its buyers' spending; a supplier's sales between its buyers' spending and a rival's share) | consistent: chooses within one home by directness of measure; adds no kind of relation |
| a separate figure for each of two questions: two items, one under each | standard §11 counting unit (one research matter per unit, which several records may express); D250's counting unit; `extraction.sift` stores two items on one sentence as one piece with both links | consistent: applies the counting unit to filing; Codex r4 (two prices in one stored statement) |
| shared company … other name counts; whoever says it … weight later | v74i; D250; §5.2 | consistent (verbatim) |
| candidates; empty when none, however important | D264, D209 | consistent (verbatim) |
| fallback sentence | D273, D274 | removed by PRD 10 §5; returns to §6 |
| D259's leeway for company-wide questions | D259 (Alex) | unchanged: compare-first leaves a company-wide question available when no specific one is connected |

General-analyst check (AGENTS §6): eighteen examples — a lender, a retailer, a calendar-year estimate, a carmaker, an airline, a drug maker, a drug
wholesaler, an airline's bookings, a builder, a regulator, an aircraft maker, a plant, a bank, a buyers' survey, a supplier, a hotel chain, a parts
maker, a drug maker's two drugs — none names a chip company, NVIDIA, a test article's party or number. Examples that mirrored a test case were
replaced (round 2: a delayed component, a scrapped interim model; round 4: "a seller's price … its buyers' spending", "a supplier's sales … a rival's
share", "two products' prices in one sentence").

## 4. Sizes

Links field 1,226 → 3,067 characters (+1,841); role 11,028 → 10,928 (−100); whole request +1,741 characters on every one of the 69 test requests
(`resend_filing.py check`: stored 33,875–59,344, v74l 35,616–61,085), about +440 tokens at four characters a token; the measured prompt tokens are
read from the test's usage and reported. Reason for growth (AGENTS §6): eighteen examples replace one abstract clause, three per class as AGENTS §6
asks; two sentences settle what one home left to chance; the fallback sentence (192 characters) goes.

## 5. Contract checks on the code path (AGENTS §2, new path × old checks; AGENTS §6, check before the send)

The answer's shape does not change (links is still a list of ids), so every code check of `extraction.sift_with_groups` and `file_reading` runs as
before: a link must be a shown question or a kept candidate; a candidate left with none of its evidence is dropped; a statement whose only link was
a dropped candidate has no home; the same sentence read out twice is one piece with both links; `narrowest_links` keeps the narrower of a linked
question and its seed parent. Readers of the links: matching (one home per statement as today), judging (evidence in view by link).

Checked at no cost on 2026-11-04:
- A hand-written answer that follows v74l for the Morgan Stanley article (call 204), through `resend_filing.file_like_production` (the production
  sift, narrowest rule and no-home drop): the rack price under v20; the two-price sentence written twice, under v20 and v19, stored as one piece with
  both links (the second item reported "same quote as e2; merged"); the memory cost written under v3 and v1, kept under v3 only (v1 is v3's parent);
  the shipment schedule under v7; the self-sourced price under v20; a generic sentence with no link left with no home.
- `resend_filing.py check selection-test.json --arms stored,v74l`: all 69 requests rebuilt byte-identical to the stored ones; all 138 arm requests
  built; each role edit found exactly once in every request. The harness now builds and checks every request before the first send.

## 6. Predicted interactions (not hidden)

- `narrowest_links` reads seed edges as "narrower than", and the tie sentence puts a supplier's sales to a group of buyers under the buyers'
  spending question: Broadcom's figures go to custom silicon (v16) and the share question (v6), which does not read v16's conclusion, loses them
  (the wiring defect, PRD §3). Reported as class (c), not mended.
- D259's leeway keeps some parking under total revenue; the pile falls, it does not vanish.
- Statements dropped for no home rise; each gold-used one is read and classed.
- The leeway and (5) can still link ecosystem news (a partner using the company's product) to a company-wide question when no specific one exists:
  the standard keeps such a named adoption, D259 accepts the cost; counted in the per-question noise reading.

## 7. What each draft answered

| Finding (review) | Change |
|---|---|
| role keeps two sentences giving takes lines the filing authority (Codex r1, reader 1) | all three sentences edited (§2.1) |
| compare-first sentence dropped and unlisted (Codex r1, reader 1) | kept verbatim and listed |
| closed list narrower than the standard: input costs, profit lines, backlog, market forecasts (Codex r1, reader 1) | (2) part or input; (3) demand behind spending; (5) market figures and forecasts |
| two-sided clause ambiguous, a D207 departure (Codex r1) | dropped; one home stays |
| one example per class (Codex r1); class (1) without a period example, class (4) mirroring test cases (reader 2) | three per class; a calendar-year estimate; a regulator's data request and a failed test flight |
| "missing" overstated; D273 made to disappear (Codex r1) | audit table rewritten |
| contract checks absent; prompt tokens absent (Codex r1) | §5; whole-request size measured, tokens read at the test |
| identifiers already used: v74k / poc-v111 (Codex r1), poc-v112 (Codex r2) | v74l / poc-v115, absent from the repository and the retirement manifest (Codex r3 confirmed) |
| no rule between two specific questions: the rack price (Codex r2); "the party it describes" picks neither for Broadcom (Codex r3) | the tie sentence by directness of measure (§2.3) |
| one stored statement with two products' prices (Codex r4) | the split sentence (§2.3), checked on the code path (§5) |
| tie and split examples mirrored test cases (own check, the class reader 2 named) | a hotel chain's room rate, a parts maker's sales, a drug maker's two drugs |
| decision rule judges nothing; credit through the seed tree; bars on means; significance alone per question; per-question classes by a reader (reader 2; Codex r3, r4, r5) | `prd-amendment-proposal.md` §1, for Alex's word: totals by reassignment; per question by code with limits calibrated against luck (3 net drops, 5 net new noise statements); reading names mechanisms, decides nothing |

## 8. Measured: the one test (2026-11-04, `answers-links.json`, `decide-links.txt`)

414 sends (stored and v74l, three each, 69 articles), $0.59 at gpt-6-luna's published rates, no re-send; v74l prompt 8,503 tokens a send
against 8,113. **Verdict by PRD 10 §6 (D360): fail** on one line, the development reach increase (+7 over three sends, p = 0.26); every other line
passes, and no question fails the per-question guard (limits raised by the code to noise 6; an identical variant fails it in 9.2%).

| Measure (summed over three sends) | Set | Stored | v74l | p |
|---|---|---|---|---|
| supporting matters present (regression) | development | 205 | 166 | 0.0003 down |
| supporting matters present (regression) | held-out | 45 | 36 | 0.007 down |
| statements kept | development | 575 | 510 | 0.005 down |
| facts the gold uses reaching a question it uses them for | development | 185 | 192 | 0.26 up (fails "up") |
| the same | held-out | 39 | 38 | 0.50 down (passes) |
| statements under v1 or v22 | development | 147 | 68 | < 0.001 down |
| the standard's not-kept spans present | development | 120 | 78 | < 0.001 down |
| core matters present | development | 149 | 146 | 0.36 down (passes) |
| core matters present | held-out | 50 | 47 | 0.25 down (passes) |

Where each fact the gold uses went (both sets, summed): reaching a gold question 224 → 230 (p = 0.30); kept but filed elsewhere 59 → 36
(**−23, p = 0.0013**); written but no home 12 → 19 (+7, p = 0.14); not written or refused 71 → 81 (+10, p = 0.17). The filing fix works on what
is written; the gain is mostly offset by facts not written and facts left with no home, each within luck. The new rule writes fewer statements:
fewer in 39 of 69 articles, more in 20; mostly noise (not-kept spans −35%); facts the gold uses written in fewer v74l sends 28 times and in more
18 times. Supporting matters lost: 27 written but no home (the fallback's parking gone: of 12 sampled, about 9 have no question that takes them —
valuations, partners' adoptions of the company's software, a retail price of a gaming card; 2–3 had one: a next-year earnings estimate for the
earnings question by way (1), a rival's speed claim for the share question by way (5)), 12 not written.

The model's own account (`probe-links-account.md`, four sends, under a cent):
- The rack price filed under hyperscaler spending in all three sends: it cited way (3), "the demand that drives the buyers' spending"; asked
  afterwards, it said that filing "was not well supported" by the tie sentence, yet it still rejected the product-revenue question because "the
  rack-cost estimate is not itself a measure of product revenue": the literal reading the five ways were written to replace survives for this case.
- Micron's margin guidance not written in any send: "No instruction supports leaving it out"; it bears on the gross-margin question (v3).
- The Intel host-CPU statement was written in all three v74l sends and refused each time by the quote check (the model joined two passages or
  paraphrased); quote refusals 5 → 10 over the test.

Prompt audit of the failure classes (prompt-audit skill):

| Failure class | Request sentence | Standard's line | Verdict |
|---|---|---|---|
| a seller's price filed under its buyers' spending (1 fact, 3 of 3 sends) | way (3) "the demand that drives the buyers' spending"; the tie sentence unapplied in one pass | §5.1, D207 (narrowest, the question it bears on) | misread in one pass, corrected when asked; way (3)'s clause is wider than its examples |
| important facts not written (+10 sends, p = 0.17) | none named by the model ("No instruction supports leaving it out") | §2 keep kinds; D243 | misread in one pass (sampler); fewer statements overall under v74l |
| facts written with no link (+7 sends, p = 0.14), single sends | the five ways (concrete) | §6 | sampler: each a one-send coin flip |
| supporting matters with no home (+27) | the fallback deleted | §6 "没有问题接，记 no home 扔掉" | by design for about three in four; the rest misread ways (1) and (5) |
| quotes refused (+5) | not the links rule | the quote check (D236) | not the prompt's links text; within luck |

The listed cases, read by an independent reader (verified against the raw answers; `log.md` row 19): 2 helped (Broadcom's $10.8bn and $16bn
guidance to custom silicon in 3 of 3; the interconnect delay to the Rubin Ultra question in 3 of 3), 7 hurt, 14 showed no real difference (writing
variation, a refused quote, gold citing another outlet's copy). Six of the seven come through a way of the new rule matched on a word rather than on
whether the statement moves that question's answer: the rack price by "the demand that drives the buyers' spending" (the one decisive fact lost);
a custom-silicon margin warning and a rival's own chip by "margins" under gross margin; an undated space module by "variant" under the Rubin
shipping question; "a structural shift in AI demand" by "demand" under data-center revenue; a consensus without figures by "estimate" under
earnings per share; a statement that fits a way is also written. The seventh, Micron's margin guidance never written, has no cause found. The demand
clauses of ways (3) and (5) are wider than their examples.
