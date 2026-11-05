# Core PRD for the next phase: filing must recognise indirect relations the way an analyst does

> Status: in progress (opened 2026-11-04). Alex: "你把这个写好成下一阶段核心PRD然后不要drift, 把所有需要的context 全部充分记录，每次开始前都需要revisit, 然后开始做".
> This page is the single source for this phase. In a conflict: Alex's words → `docs/DECISIONS.md` → this page → the other design documents. This page's
> conclusions, evidence, constraints, measuring method and process are not rewritten to follow test results;
> test results go into `docs/research/2026-11-04-filing-end-to-end/log.md`, and changing this page first needs Alex's word.
> Amended 2026-11-04 (Alex replied "go" to the proposed amendment; D360): §5.2 drops "also file under the other party's question" and puts two
> sentences in its place, one on choosing and one on splitting; §6's decision rule is rewritten. How it came about:
> `docs/research/2026-11-04-filing-end-to-end/prd-amendment-proposal.md` and `log.md` rows 11–16.
> 2026-11-05 (D368): translated into English on Alex's word ("不，用英文吧"); §4 corrected to name the frozen standard's version 5 and §5 given a status line, on his delegation ("你要来帮我看到底做不做").

## 0. Checklist before every start (Alex: "每次开始前都需要revisit")

Before starting any step, finish these in order; if one cannot be done, do not start:

1. Read §§1–8 of this page in full; read the last three rows of `log.md`, and confirm where the previous step stopped and why.
2. Check against §3, "not in scope": what this step does is not in that table. If it is in the table, stop and take it to Alex.
3. Check against §4, "constraints": this step changes nothing frozen; a change to the frozen extraction prompt is the one place §5 names, and Alex's
   word for it is already given.
4. If this step costs money: its predictions and stop conditions are written down and frozen as §7 says (with their sha256 recorded beside them); the
   requests are rebuilt byte for byte as §6 says; the control is re-sent the same day.
5. What goes to Alex: one conclusion, one recommendation, one test, after §7's rounds of review; no menu of options; in plain words (the opening of
   AGENTS, "Explain and answer as to a sixteen-year-old").

## 1. Goal (end to end)

Each question's judgement must receive the facts that can change its answer; facts that no question receives, those that bear on no question, must
not be piled into some one question. What is measured is the final judgement (the frozen judgement ruler, reader B, at the window end 2026-07-14), not
any one step's own score.

## 2. The core blocker (proven)

**The system uses a fact for a question only when the fact "states exactly this question's own figure". An analyst also reasons onward from a fact: the other party's figure in a deal, price and volume for a product's revenue, a product's variants for its launch, and so on. The filing step cannot do this; the judging step reasons onward once it has the facts.**

This one blocker has two faces (described earlier as "two problems"):

- **The parking lot.** Filing does not recognise facts that bear on a question indirectly, so no question takes them; yet to be kept, a fact must
  first be filed (D209, D264). So D273 added the fallback sentence, which parks them in NVIDIA's total-revenue question. Of the reports under the
  total-revenue question, in the part the gold read, 32–39% are ones the standard does not keep, 31–44% are kept but used by none of the 22 questions,
  and only 7–10% are what the gold actually uses to judge total revenue (three draws); 24–44% of the total-revenue question's judgement citations are
  news about other companies or the whole market (Intel graphics-card retail prices, a gas-fired power plant in Taiwan).
- **Narrow questions starve.** Questions that only indirect facts can answer do not receive them: the custom-chip question received none of Broadcom's
  figures in any of the three draws, and judged "below $40 billion" in all three; the operating-margin and NVIDIA capital-spending questions received
  nothing at all and were never judged.

**Evidence:**

| Evidence | Content | Source |
|---|---|---|
| Filing recognises only "its own figure" | The model says "Broadcom's AI chip revenue is not cloud providers' spending on custom chips" and "Google Cloud's backlog is not capital spending"; on a neutral refiling (no question id named, the rule not shown), 23 of 42 facts that matter are still not filed | `probe-filing-account-d1.md`, `refile-no_fallback.json` |
| The judgement reasons onward once it has the facts | The custom-chip question's request of 7-14, sent 3 times in each of the three draws: as it was, 9/9 "below $40 billion"; with the Broadcom, Trainium and other facts written in that draw's ledger added, 9/9 left the lowest rung (6 times $40–60 billion, 3 times $60–80 billion), reasoning as the two readers did ("guidance $16 billion, about $64 billion annualised, less networking chips") | `predictions-one-test.md`, `one-test-result.json`, `log.md` row 8 |
| Where the parking lot came from | D273: with the fallback sentence added, the core items on the extraction ruler went 64 → 68; the extraction ruler does not look at which question a fact is filed under (AGENTS §7.1, "What it does not measure") | `docs/DECISIONS.md` D273 |
| What the parking lot holds | The figures above; an independent reader on 12 random articles: of 25 misfilings as it was, 21 were parked in the revenue question; 8 and 5 with the fallback deleted | `sink_by_standard.py`, the independent reader's report (`log.md` row 8) |

All files above are in `docs/research/2026-11-04-filing-end-to-end/` unless noted otherwise.

## 3. Ruled out or secondary (outside this phase's scope, each recorded separately)

| Matter | Conclusion | Source |
|---|---|---|
| The argument card | Not built; its code is deleted (Alex: "好，删掉卡片代码") | `docs/research/2026-11-04-argument-record/log.md` rows 4–11 |
| The arrows of the question graph | Really wired backwards: a seed question's arrow means "supports" (D208), while the judging code reads it as "whose conclusion to read" (PRD 06). As a result themes are judged only after the total-revenue question, so the total-revenue question reads the themes' conclusions of the previous day, and in draw 3 a chain of questions went wrong in turn. But it does not explain the misfiling (filing comes before judging), and the gold itself judges data-center revenue as "total revenue × 92%". A topic of its own; settled by D368 (item 4: the arrow means "supports"), its fix to be built and measured | `core-problem.md`, `review-core-codex.md` |
| Code removes the total-revenue question's own figures | True ("keep only the narrowest question" takes a seed arrow for "a narrower sub-question"), but each draw it costs the total-revenue question only 0–2 of the facts it needs | `log.md` row 8 |
| A filing re-check added at the end | Recovers some, and misfiles about as many (independent reader: about one misfiled for each one filed right); not the solution | The independent reader's report |
| One general sentence, "the other party's figure in a deal counts too" | The custom-chip question gains, but it pulls Morgan Stanley's price for a Rubin rack from the Rubin revenue question to the capital-spending question, and leaves some facts with no home | `answers.json` (the two arms definition and definition_no_fallback), `measure-corrected.txt` |
| Tightening D259's "leeway" | Alex's own decision; this phase does not overturn it | D259 |
| Opening questions (the Ohio guarantee was not opened); the two readers' disagreement on the China-share question | Another class of problem, not in this phase | `docs/research/2026-11-04-filing-end-to-end/diagnosis.md` §0 |
| Model drift | With the same requests, today about half as many facts go into the total-revenue question as on 11-03; the cause is not proven. Compare only with a control re-sent the same day, never with the archive | `log.md` row 6 |

## 4. Constraints (what must not move, and why)

- **The frozen ruler** (AGENTS §7.1, D261, D262): the extraction standard, version 5 (the signed version 3 with D248's seven boundaries and D250's four
  evidence boundaries and counting unit), golden-v5, the seed questions and the judgement gold; not a word changes; a disagreement is a gap in the
  system (D263).
- **The frozen extraction prompt** (D274): v74i (`poc-v108`) does not change by a word; what this phase changes is the one place that holds the filing
  rule (the description of the `links` field), made into a new version with a new configuration and compared with v74i. Alex has given his word for this
  work (2026-11-04: "好你去解决问题", "开始做"); making it the default needs his word again.
- **Frozen opening and judging** (D354): this phase does not touch them.
- **The standard's text** (in translation): §6, "file under the narrowest open question; when no question takes it, record no home and drop it, and read
  each one at evaluation"; §5.1, "makes the answer to some question more or less likely", with four paths, "demand, supply, competition, pricing"; §5.3,
  "another company's matter is not kept when one cannot say which question about the covered company it moves through a path such as demand, supply,
  competition or pricing".
- **Decisions**: D207 (one home per fact, the narrowest question), D209 (no home means dropped, each one read), D259 (leeway: a figure question takes
  "the demand, supply, competition and pricing that make it more or less likely"; the total-revenue question taking more is an accepted cost, "bounded by
  the narrowest-question rule and the driver questions"), D265 (code keeps only the narrowest), D273 (the fallback sentence), D355 (the two failed tests
  of the previous filing topic).
- **Prompt principles** (AGENTS §6): carry only the standard and add no new rule; a general hedge-fund analyst: every rule and example reads the same
  for a bank, a drug maker, a retailer or a chip company, names neither NVIDIA nor its products or figures, and is not taken from a test article; a
  classification is written as a closed set with two or three examples per class, replacing the abstract wording; quality is not fixed by lengthening
  the prompt: remove as much as is added, or write down the reason.
- **Code decides only "is it the same thing", never "does it matter"** (AGENTS §2).

## 5. What to do

Status: the links-rule version that carried items 1–3 (v74l) failed its one test (§8 step 5); D361 keeps the fallback sentence, so item 3 is not carried out. The plan below is kept as written.

1. **Replace the abstract sentence "makes the answer more or less likely through demand, supply, competition or pricing" with the few classes in which an analyst recognises an indirect relation, written as a closed set, each class with two or three examples from other industries** (AGENTS §6: one
   abstract sentence is a coin flip on every send; examples replace it). A first draft of the classes (checked against the standard line by line at
   design time; it holds only meanings the standard already has):
   - The question's own figure: this question's figures, guidance, estimates and revisions (estimates for another period or another population follow
     the existing rule).
   - The other side of the same money: a seller's revenue from the buyers the question counts; those buyers' orders and backlog with these sellers.
   - Price and volume: a product's price or shipments, for the question on that product's revenue.
   - Variants and parts: a product's variants, alternatives, key parts and schedule changes, for the question on that product's launch.
   - Demand, supply and competition moves with a number: customers' orders and capital-spending plans, suppliers' capacity and prices, competitors'
     sales and share, for the question they affect.
2. **State how to file a fact when two specific questions both bear on it** (the problem the `definition_no_fallback` arm exposed: Morgan Stanley's rack
   price was filed under the buyers' capital-spending question, and the seller's Rubin revenue question lost it). One home per fact (D207): file it under
   the question its figure measures most directly (for example, a hotel's room rate goes under its room-revenue question, not under the
   travellers'-spending question; a parts maker's revenue from carmakers goes under the carmakers' parts-spending question, not under a rival parts
   maker's share question); when one sentence gives a separate figure for each of two questions, write two items, each filed under its own question
   (code stores two items that quote the same sentence as one record linked to both questions); never also file it under a broader question about the
   same company (the failure of D355's test 2: the model filed it under an NVIDIA revenue question as well). The original draft's "when the other
   party's question is open … file it there as well" conflicted with D207 and was deleted on 2026-11-04 with Alex's agreement (D360).
3. **Delete the fallback sentence** and return to the standard's §6: when no question takes a fact, it is not filed; code drops it as "no home" and
   records it (D209), and evaluation reads each one.
4. Change only the one place that holds the filing rule; report its length in characters before and after, and write down the reason for any growth
   (this time's reason: examples replace one abstract sentence).

## 6. How to measure (the ruler does not move; the method does not change again)

- **Requests**: rebuild each stored request byte for byte with the production code, changing only the one place that holds the filing rule; the
  rebuilt request's archive id must equal the original's, or it is not sent (`resend_filing.py`, AGENTS §5). Never re-send the archive's copy whose
  keys were sorted alphabetically.
- **Articles**: development set = the 54 articles of `selection.json` (already read many times); held-out set = articles the extraction gold read and
  the judgement gold uses that are not among those 54, drawn once before the test, with the list frozen and never changed afterwards. Both sets are
  measured and reported apart.
- **Control**: the unchanged requests re-sent 3 times the same day. No comparison with the archive (model drift).
- **Each answer**: goes through the production code checks and filing first (including "keep only the narrowest" and "no home means dropped"), and is
  counted after.
- **What is counted** (`measure_filing.py`, with its matching rule fixed: items are matched on the distinct numbers and the proper nouns other than
  NVIDIA in the source text; a source passage the system quotes that overlaps the gold's passage also counts as the same matter; "optional" counts as
  optional; the citations in the body of the gold's answers are read):
  - whether each fact that matters (one the gold uses to judge any question) reached the question that uses it, counted per fact, not per "fact ×
    question";
  - per question: the facts that matter that reached it and the new noise that appeared, counted by the decision rule below;
  - the parking lot: how many facts the total-revenue question (v1, together with v22) takes in, and what they are;
  - noise: how many of the sentences the standard does not keep are kept; per question, how noise is filed (links on facts the standard does not keep
    or no question uses);
  - how many core and supporting facts appear; the facts that matter that are dropped; how many questions each fact is filed under on average.
  - Matching still has a small error (spot check: the new rule mismatches a few and misses a few); say so when reporting the numbers, and read the
    ones that matter one by one.
- **Decision rule** (rewritten on 2026-11-04 with Alex's agreement, D360. The original draft required "every draw above the highest of the control's
  three" and the like, which the control itself fails when measured again, so it cannot tell good from bad. Script `decide.py`; written down and frozen
  before each test; each draw's numbers and the totals are all reported):
  - **Totals, with luck ruled out first**: each article's 6 answers from the new and the old arm are randomly reassigned between the two arms 4,000
    times (with a fixed random seed); the new rule's difference counts as a real change only when fewer than 5% of the reassignments reach it.
    - Development set: facts that matter reaching the question that uses them must rise; the count under the total-revenue questions (v1, v22) must
      fall; sentences the standard does not keep must not rise; core facts must not fall.
    - Held-out set: facts that matter reaching the question that uses them must not fall; sentences the standard does not keep must not rise; core
      facts must not fall.
  - **Per question, counted by code against the gold** (development and held-out sets together):
    - A fact that matters which reaches the question at least two fewer times under the new rule than under the control counts as "one fewer" for that
      question; in under the control all three times and under the new rule none of the three, it counts as "lost outright". A move to another question
      that the gold also uses it for and that is no broader than the original (one home per fact, D207) does not count as fewer; a move to a broader
      question counts. "One more" in the opposite direction offsets it.
    - A noise sentence (not kept by the standard, or kept but used by no question) that the new rule files under the question at least twice while the
      control never does counts as "new noise"; filed all three times, it counts as "outright new noise". The opposite direction offsets it.
    - Any question with a net 3 fewer, a net 2 lost outright, a net 5 more new noise, or a net 3 more outright new noise fails. These thresholds are the
      smallest values that keep "misjudged when new and old are exactly the same" within about one in ten; at the test, first compute the
      misjudgement rate from the reassignments; if it is above one in ten, raise the threshold most prone to misjudgement by one step, then compare with
      what was measured.
  - **Smaller changes** (a question 2 fewer, two or three more noise) cannot be told from luck in three measurements: all are listed, given to a reader
    who did not write the rule to read against the raw answers, and written into the report; they do not decide pass or fail.
  Only when everything passes does it become a candidate; a candidate runs end to end three times on the 14-day window (extraction re-sent, matching and
  judging run as usual, scored on the frozen judgement ruler), and that step needs Alex's word.

## 7. Process (no drift)

- **One recommendation and one test at a time** (AGENTS §7.3, Alex: "就测试一种，一次"): write the design first and put it through rounds of review (own
  checks, Codex read-only, a reader who did not write it reading the raw records) until a round finds nothing serious; write down and freeze the
  predictions and stop conditions; test once; if it does not match, stop and take it to Alex (D355: "如果有什么不符合hypothesis 的地方你需要终止然后和我说我们重新评估").
- **A review's report is a lead**: each finding counts only once it is checked against the records (AGENTS §1).
- **A prompt audit before any prompt change** (`.claude/skills/prompt-audit/SKILL.md`): check the whole request against the standard sentence by
  sentence, in both directions.
- **Every step goes into `log.md`**: what was done, what came of it, the files; mistakes and overturned results stay in it too.
- **Do not repeat what was ruled out** (§3).

## 8. Steps and where we are

| # | Step | Output | Status |
|---|---|---|---|
| 1 | Design: the classes of indirect relation (a closed set + examples from other industries), how to file when a fact measures both sides, deleting the fallback; checked against the standard sentence by sentence; length before and after | `docs/research/2026-11-04-filing-end-to-end/design-links.md` | Done (draft 3, v74l / poc-v115) |
| 2 | Checks at no cost: a sample answer written by the new rule goes through every code check; the new rule's text goes through the prompt audit | Same as above | Done |
| 3 | Review rounds (Codex, independent readers, own), until nothing serious remains | `review-links-*.md` | Done (Codex 7 rounds, independent readers 3 times; round 7 found nothing serious) |
| 4 | Draw and freeze the held-out set; write down and freeze this test's predictions and decision rule | `heldout.json`, `predictions-links.md` | Done (sha256 recorded for both) |
| 5 | Test once: development set + held-out set, the new rule and the same-day control 3 times each | `answers-links.json`, `log.md` | Done (2026-11-04): failed: facts that matter reaching the right question, development set +7 (p 0.26); every other condition passed |
| 6 | If passed: to Alex, to decide whether to run three 14-day end-to-end draws; if failed: stop, to Alex | `design-links.md` §8 | Stopped, to Alex |
| 7 | (D361, Alex: "按照你的提以来，但是你一定是自己反思多轮之后才给出的行动") Measure the ceiling first: hand the source passages the gold cites straight to the frozen judgement; the custom-chip, operating-margin and capital-spending questions judged 3 times each at the window end, the custom-chip question as it was 3 times as the control; the fallback sentence is not deleted for now | `reflection-v74l.md`, `oracle-design.md` | Done: operating margin grounded 3/3, capital spending 2/3, custom chips 0/3 (the gap is in interpretation); the next step waits for Alex |
| 8 | (D362, Alex: "你继续啊不要scope drift and strongly follow evidence of your discovery and learning") Two small changes where facts are not delivered, one at a time: ① when a quote is rewritten, code matches it back to the source sentence (changing nothing the model sees; verified by replaying the archive); ② a figure question's description states which figures it is derived from by definition (first sent 3 times each on the article that motivated it) | `delivery-fixes.md` | Stopped: an independent check overturned the first change's code (it would take in wrong figures); the second failed its trial send (1/3). The root: the signed standard's §5.3 does not keep two key facts, treating them as "a restatement of known facts" (proposal 6, awaiting approval); to Alex |
| 9 | (D363, Alex: "乙") At coverage start, record each question's starting figure once from the company's latest earnings report; the daily path still takes no restatements: design, rounds of self-checks and independent checks, validated first on the archive in the simplest way | `baseline-design.md` | Validated on two questions: the frozen extraction does not read the report's tables (0/3); with each question reading the report once on its own, the operating-margin question read its starting figure 2/3 and the capital-spending question 3/3, and the judgement then judged right (2/3, 3/3), about 2.5 cents. All 22 questions tested once (2026-11-05, Alex: "你充分验证"; files chosen by code, a same-day control, about $0.43): v10 and v12 judged right 9/9 each; no question already judged right turned wrong; but 5 of the 53 figures read were other quantities (the Vera CPU question and the Blackwell and Rubin question took a larger or neighbouring revenue line), so it failed condition 3, written beforehand. The model itself pointed to the reading instructions' sentence "write the lines it is computed from, or the line the report uses for it"; stopped, to Alex. Alex: "改"; only this sentence was changed ("write only the lines it is computed from, or the same quantity under another name; never a broader line or a line next to it"), tried on 4 questions first, then tested on all 22 (about $0.36): all three conditions passed: v10 and v12 9/9 each, no question judged right turned wrong, and all 46 figures were the questions' own quantities. Checked after an independent reader's challenge: the new sentence made the reading miss the capital-spending line in 3 of 12 reads, and it had been tested only on the one May report; the fourth version (a line-by-line re-check after writing) removed too much and failed; after a census of every failure trace (Alex: "我需要你深度看完所有失败trace给我准信"), the third version with the repaired quote check was chosen (D365): 0 wrong figures on the held-out August report; built into the production system (poc-v116; the $0 checks and the tests all pass). The full acceptance, three 14-day draws (Alex: "跑验收"; a same-day control; about $4.79): all passed: operating margin and capital spending judged right 3/3 each (the control never judged them), 53 against 45 in total (of 57); for the China-share question, the only one two fewer, both readers found the starting figures did not lead it astray. Alex: "都做": poc-v116 became the default (D366); the code was committed and a PR opened |

## 9. Alex's own words on this matter (in time order)

- "你这个单独开一个专题出来解决 … 是promot，是系统结构设计还是到底哪里有问题挂错一堆东西，机制是不是有问题（一定要挂吗？有没有可能是杂音" (2026-11-03)
- "So if it's a customer problem or other companies that you think is relating NVIDIA and it's the wrong evidence, then what is the standard for it? … from a hedge fund analyst standpoint, are these even relevant? Do you think your ruler is wrong in this aspect?" (2026-11-04)
- "你确定下你接下来要改进的量化目标，以及你要看到端到端我们的管线是要做什么的，不要乱硬优化，要看到目标" (2026-11-04)
- "就测试一种，一次 … 能不能自己有个超级自信的定论和证据再给我提建议" (2026-11-04)
- "这些只是类型题，你需要抽象拔高我们现在的核心问题和卡点。这个很重要这样改下去才是对的" (2026-11-04)
- "你把这个写好成下一阶段核心PRD然后不要drift, 把所有需要的context 全部充分记录，每次开始前都需要revisit, 然后开始做" (2026-11-04)
- "go" (2026-11-04, on the proposed amendments to §5.2 and §6 and on this test)
