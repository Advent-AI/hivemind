# Can the new system open questions on the company's revenue and margin without number cards? Probe design, version 3 (D490), 2026-11-14

**What it can decide.** Whether c20, the adopted clean Step 1 request (c8) with one more reason in its closed set (the company's own annual
revenue or gross margin), opens the three questions the fresh week showed it lacks (fiscal 2027 revenue, fiscal 2028 revenue, the fiscal
2028 gross margin) on the stored articles that carry them, keeps and links the figures those articles state, opens no question on other
statement lines, quarters or other companies' figures, and does not suppress what c8 opens today. Two steps: step one on the stored
states; step two, only after step one passes, the same later articles against a state that already holds the new questions (does it open
them twice, or file a year under the wrong year?). Both must pass before the forward draw on the second fresh week. A failure stops the line
and goes to Alex. Neither step shows how one article's choices shape the next over a week (only a forward draw does), nor whether final
judgements improve.

**Alex's word (D490):** "试开这类问题", on the option "先在这周已存的文章上…试：能否开出这 3 个问题，同时不乱开、不重复；通过后再跑第二个没用过的新鲜周". D382 and D384
stay in force for the adopted path; the arm departs from them on this one point, for the test.

## The candidate (`clean-arch/step1-unfiled-2026-11-08/arms/c20-*`)

One direction, stated at its owners (the differences from c8, all of them):
- **§3's closed set gains a fifth reason, first in the list:** "main_driver: the company's own annual revenue or gross margin, for its
  current or next fiscal year, whether or not the company guides it: the revenue that carries the business, in total or of its main segment,
  or the gross margin ("the bank's net interest income this fiscal year"; "the retailer's same-store sales next fiscal year"). It is not
  every line of the statements. Name the measure, its scope and the fiscal year the item supports; a level and its growth rate are one thesis
  when the same reported figure settles both. The material that publishes the figure, usually the annual report, settles it."
- **The date rule** gains "a main_driver quantity, the release of that fiscal year's results" among the dates a reason fixes when the item
  gives none.
- **The do-not-open row** "a financial measure's level, growth, margin or guidance for any period, on its own" becomes "a quarter's figures
  or guidance, or the level, growth, margin or guidance of a financial measure that is not a main_driver quantity, on its own".
- "four reasons" becomes "five reasons" in §3 and in the closing check; the schema's `opens_as` gains `main_driver` and its description says
  five.
- Nothing else changes: the CONDITION bullet already sends the company's figures to "an open thesis about its revenue or earnings path"
  ("open or new" in its next sentence); "another estimate, source or wording of what an open thesis tracks" and "an annual quantity after
  next year" stand; `closest_open_thesis` and `why_a_separate_bet` are as they were.

**Source.** The signed standard §3, row A: "A 主驱动量 | main_driver | 标的 | 承载公司价值的那个年度量，不管公司指不指引：撑起业务的分部收入、毛利率、资本开支；跨行业如银行的净利息
收入、零售商的同店销售、公用事业的费率基数、航空公司的燃油成本（当它是争论焦点时）。不是每一行报表数 | 量，五档 | 公司财年的今年或明年；到期日是这个数的发布日 | 公布这个数的公开材料，通常是年报";
§4 for the quarter row ("季度数字和季度指引"), for writing who and what is counted ("算谁、不算谁、算什么写清楚") and for one result settling one
question ("同一个结果能判掉两题，就是同一题"). The two examples are the row's own; none names the covered company, a product or a number.

**Narrower than row A, on purpose, by D490's scope.** The row is "the annual quantity that carries the company's value" and also names
capital expenditure, a utility's rate base and an airline's fuel cost; Alex opened the test for revenue and margin, so the arm says revenue
or gross margin and carries only the two revenue examples. A question on another annual quantity is therefore outside the request as
written and counts as a number card below; that is a limit of this test, not a reading of the standard, and the frozen standard is not
changed. If the arm is ever adopted, the narrowing goes to Alex.

**Size.** System text 15,828 → 16,574 characters (+746); closing check the same length; schema one enum value. Growth reason: the standard's
row A has no sentence in the request (left out by D384); D490 opens the test of carrying it; no sentence can be cut for it without becoming
a second direction.

**Reviews before any send.** Blind audit of version 1 (`audit-c20-blind.md`): wider than D490 (fixed: revenue or gross margin), no date for
an item that gives none (fixed: the date rule), a growth example that reads as a second measure (fixed: the example and the level-and-growth
sentence), measure and scope not asked for (fixed). Blind audit of version 2 (`audit-c20v2-blind.md`): those points resolved except the
date, where it notes that "the release of that fiscal year's results" names an event and no calendar day: that is the form the adopted
request already uses for an obligation ("its next annual report"), and the answer-options step sets the due day by code from the fiscal year
when neither thesis nor article states one, so it is left as it is and the probe reports each thesis's period; "the fiscal year the item
supports" added from its second point (§4, "原文支持这个期间"); its other notes (the margin's tie to "carries the business", a sentence that the
row leaves the other reasons alone) are risks the cases measure, not contradictions. Council rounds 13 to 15 (`mw-codex-13.md` to
`mw-codex-15.md`): the counting below, and the blind reading of the kept-and-linked line (round 15's one condition for the send: "先补上独立、盲读的
事实保留与关联检查及其分歧处理，再发送第一步；第二步的构造器另行审查"). A synthetic answer following the
arm (one main_driver thesis, one linked statement) passes the arm's schema and every runner check; the same answer fails c8's schema and a
reason outside the set fails the arm's, as they must.

**Prompt audit row** (`.claude/skills/prompt-audit`, §3):

| Failure class | The request's sentences | The standard's line | Verdict |
|---|---|---|---|
| The company's revenue and margin are never questions: 3 of the 5 matters both reader families listed; the stored reasoning names the sentence at 109 of 235 steps; 145 kept figure statements have no question | "It opens for one of four reasons, a closed set"; "Do not open a thesis about: … a financial measure's level, growth, margin or guidance for any period, on its own" | §3 row A | The request removes what the standard keeps, by Alex's D382 and D384; not a model misread. D490 opens the test of carrying the row for revenue and margin. |

**What arm c1 teaches (`LOG.md` §20).** c1's "a measure with a reason the item supports is a view" let any conditional count as a reason
(7 unwanted theses in 48 sends) and its narrower link sentence left a margin figure outside the revenue view, with three levers in one arm.
c20 has no "reason" clause and touches no link sentence; the links are counted below because c1 failed there.

## Step one: the stored states

The reviewed probe (`clean-arch/e2e-comparison-2026-11-13/identity-probe/probe_identity.py`) unchanged: it first rebuilds every stored
request byte for byte, then replaces only the three arm files. Both arms on all ten cases, three sends each: **60 sends**; about $0.55 at the
week's mean call cost ($0.0089) and $0.86 at the script's estimate (9,500 output tokens a call); spending ceiling $2.00. (Claude told Alex
"a few cents"; the honest figure for both steps is about one dollar. The step's spend so far is $4.69.)

Cases (`cases-main-numbers.json`; the stored week's own c8 requests and before-states, none of which holds a revenue or margin question):

| case | step | what the article holds | matters it should open | facts that must be kept and linked there |
|---|---|---|---|---|
| t1-target | 11 | consensus only | FY2027 revenue, FY2028 revenue | the $406.05 billion and $671.95 billion sales estimates |
| t2-target | 16 | the 70% outlook against the 45% modelled; margin estimates under 72% by the fourth quarter | FY2028 revenue | the 70% outlook |
| t4-target | 121 | the fiscal-2027 consensus; the 70% outlook; margins 72%–73% in fiscal 2028 | FY2027 revenue, FY2028 revenue, FY2028 gross margin | the $412 billion consensus; the 70% outlook; the 72%–73% outlook |
| t5-target | 98 | the 70% outlook; the 72%–73% margin outlook against a consensus of steady margins | FY2028 revenue, FY2028 gross margin | the 70% outlook; the 72%–73% outlook |
| t6-target | 92 | the fiscal-2027 consensus; the 70% outlook; AMD's and Broadcom's figures | FY2027 revenue, FY2028 revenue | the $406.05 billion consensus; the 70% outlook |
| g1-guard | 13 | only last quarter's reported figure ($89 billion of data-center revenue) | reported only | |
| g2-guard | 37 | EPS forecasts for two fiscal years, net income, the third-quarter guide | none on EPS, net income or a quarter | |
| g3-guard | 5 | AMD's revenue and guidance beside NVIDIA's profit | none on another company's figure | |
| k1-keep | 14 | c8 opened the supply-commitments thesis here (stored draw) | | |
| k2-keep | 35 | c8 opened the Vera Rubin thesis here; the quarter's results and the third-quarter guide are in the article | | |

**Who reads.** Claude reads every answer, send by send, beside the article, and keeps the listing. Because the author must not grade the
change alone (AGENTS §7.1; council round 15), two blind reader families (Codex, a Claude subagent) read every answer of both arms beside
its article, the arms under shuffled labels, and mark:
- each new thesis by what it asks, whatever its reason label: the company's revenue or gross margin for fiscal 2027 or 2028, with its
  measure, its scope (total, or which segment) and its year / another statement line / a quarter / a later year / another company's
  figure / not a figure question; and, for two new theses in one answer, whether the same reported result settles both;
- each named fact of a target case, per send: kept (a returned statement states it as the article does) or not; and, where it is linked to
  a new thesis, whether that thesis asks the fact's own measure, scope and year, a different scope (a total-revenue figure under a
  segment question) or a different year.
The lines below are counted on the readers' marks where the two families agree; Claude's own reading is listed beside them, and where it
differs from an agreed mark the item is shown with both. A fact linked to a thesis of a different scope is listed as such: it counts as
kept, and as linked only when both families say the thesis's result is what the fact forecasts.

**Counting** (frozen before any send). Every rate is over that arm's valid sends of that case (a valid send is one whose answer passed
the checks); "most" means at least two thirds, so 2 of 3, or 2 of 2 when one send is invalid.
- *Valid sends:* at least two of three per case and arm, or that case is inconclusive for that arm (listed, and it counts for nothing).
- *A main-number thesis for a matter:* a new thesis asking the company's revenue (total or its main segment) or gross margin for that fiscal
  year, naming measure, scope and year. A growth-rate question counts for that year's revenue only when it names the measure, the scope and
  the year it grows over, so that the year's reported revenue settles it; otherwise it is listed as unclear and not counted. Level or growth,
  total or segment: the shape is reported for every thesis.
- **Opened:** each of the three matters is opened in most of c20's valid sends on at least half of its conclusive cases (FY2027 revenue:
  t1, t4, t6; FY2028 revenue: t1, t2, t4, t5, t6; FY2028 gross margin: t4 and t5, both needed). *Room, case by case:* a case has room when c8
  opens the matter there in fewer than most of its sends (it should in none: its schema has no such reason); a case without room is
  reported and does not count for or against; a matter with room on fewer than half of its cases is "no room" and cannot pass.
- **Kept and linked:** for each named fact of a target case, c20's keep rate is not lower than c8's by more than one third; and over the
  sends where c20 opens that fact's matter, the fact is linked to that thesis in most of them. A fact neither arm keeps in any send is "not
  exercised". The line passes when every matter has at least one exercised fact and every exercised fact passes; facts not exercised are
  listed and are not called passed.
- **Number card (fails):** by what the question asks, on all ten cases: a new c20 thesis on EPS, net income, cash flow, cash, a small
  segment, the company's capital expenditure, a quarter, a year after fiscal 2028, or another company's figure, where c8 opens the same in
  at most one third of its sends of that case. Fails when it holds in most of c20's sends of any one case, or in more than one tenth of all
  c20's valid sends.
- **Twice in one answer (fails):** two new c20 theses that both reader families say the same reported result settles (a level and its
  growth for the same measure, scope and year). Same thresholds. A total and its main segment in one answer is listed with both families'
  marks and fails only when both call it one result.
- **Suppression (fails):** on k1 or k2, c20's rate of opening the stored thesis (supply commitments; Vera Rubin) is lower than c8's by two
  thirds or more in one case, or by half or more over both cases pooled. A keep case where c8 itself opens it in fewer than most of its
  sends is "control absent, cannot judge"; with both absent, suppression is not exercised and step one cannot pass. On every case, any
  other thesis c8 opens in most of its sends and c20 in none is listed and counts as suppression too.
- **Where readers part.** A mark on which the two families differ is listed with both. If counting it either way gives the same verdict,
  the verdict stands; if it could change the verdict, a third blind reader with the article decides that mark, and until then the result
  is undecided, not a pass.
- *Reported, not lines:* g1, shown with the question and the article (a main-number thesis from a bare reported figure: row A allows it
  "whether or not the company guides it"; it is also the "喊出来的数字" Alex ruled out in D382, so it is his to see, not a pass by the standard);
  every other new thesis of either arm; kept and unlinked counts per arm; each thesis's period and `settled_by`.

**Verdict of step one:** inconclusive = a required case below its valid sends, a matter with no room, or suppression not exercised;
undecided = a reader difference that could change the verdict; pass = opened, kept and linked, no number card, none twice in one answer,
no suppression; fail = anything else.

## Step two (only after step one passes): the same matters met again

- **State, labelled as constructed, case by case:** each case's own stored before-state plus main-number theses c20 wrote in step one,
  given the next clean ids. The theses are fixed by rule: per matter, the shape (level or growth; total or segment) most frequent among
  c20's valid step-one sends, a tie going to the level and to the total; the text is the first such thesis in case order (t1, t2, t4, t5, t6)
  and send order, and only from a case whose step comes before the step-two case's step, so no thesis carries what a later article said.
  A matter with no such earlier thesis is left out of that case's state and its opening there is not counted.
- **The builder is proved before anything is sent:** a small script takes each stored request, adds the theses to its `open_theses` and
  changes nothing else; with no thesis added it must return the stored request byte for byte, and with theses added the only difference
  from the stored request must be the added entries of `open_theses` (checked by code on every case, or it refuses). The reviewed probe
  sends them, c20 only (c8 cannot hold these theses). A council round reads the builder and the fixed theses before the send.
- **Cases:** steps 16, 92 and 121 (t2, t6, t4) and one later article that states the margin outlook, chosen by code as the first step
  after 121 whose stored c8 answer kept a statement giving the 72%–73% outlook; three sends each: 12 sends, about $0.15.
- **Opened again (fails):** a new thesis on a measure, scope and fiscal year the state already holds, in most sends of any case, or in more
  than one tenth of all valid sends.
- **Wrong year (fails):** a named fact linked to the thesis of another fiscal year and not to its own, in most sends of any case (the 70%
  outlook under fiscal 2027; the $412 billion consensus under fiscal 2028).
- **Filed:** each named fact whose measure and scope match an open thesis (total revenue to a total-revenue thesis, a segment figure to that
  segment's) is kept and linked to it in most valid sends on at least half of its cases. A fact whose scope differs from the open thesis
  (a total-revenue consensus where the state asks the main segment) is marked by the readers for the part it plays and listed; it is
  neither filed nor failed. If fewer than half of the named facts match in scope, "filed" is not exercised and step two cannot pass.
- *Reported:* a new thesis on a year, measure or scope the state lacks (the fiscal 2027 gross margin at step 16; the segment beside the
  total), with both reader families' marks.
- **Verdict of step two:** pass = none opened again, no wrong year, filed; a reader difference that could change it leaves it undecided;
  anything else, or a case below two valid sends, is not a pass. Without a pass there is no fresh week. A pass shows how the arm treats
  these matters when they are already open in these wordings; it does not show that a forward run opens them first, nor other wordings.

**Stop.** A fail, an inconclusive or an undecided result that the third reader does not settle stops the line and goes to Alex with the
listing (D355); nothing is tuned on these cases, and a change after reading them is a new arm with its own council round.

**After both pass (not part of this probe):** the forward draw on the second fresh week (2026-09-29..10-05) is designed then, with its
budget put to Alex first (about $2.50 for the new system alone would take the step slightly past the $8 it was sized at), and with the
answer-options step checked for the fifth reason before any send (its code reads `opens_as` for obligations only; its request names no
closed set).
