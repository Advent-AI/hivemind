# Prompt audit of c14 against c8 (AGENTS §6; `.claude/skills/prompt-audit`), 2026-11-12

c14 (D433) is c8 with two sentences changed (`clean-arch/step1-unfiled-2026-11-08/arms/c14-system.txt`, `c14-closing.txt`; the
schema byte-identical; +206 characters, about 47 tokens, an estimate). Wording revised after the blind second read
(`council/ll-codex.md`), before any send. The audit reads each changed sentence, and the sentences it interacts with, against the
frozen extraction standard (`docs/prd/05-extraction-standard.html`, version 5, §3 table row D and §4) and the decisions.

| request sentence | the standard's line | verdict |
|---|---|---|
| c8 shared_quantity: "Another population or wording of the same aggregate is evidence for it." | §3 row D (shared quantity): "同一总量的另一种人群、另一种说法是这个量的证据 … 自然年的今年或明年。同一个量、同一年只有一个问题，由代码按'主题＋量＋期间'判 (D197)" | **c8 keeps narrower: missing at this sentence.** c8 carries the evidence half and drops "the same quantity, the same year has one question". c8 does say elsewhere "A thesis asks one quantity for one period" and "for this or next calendar year"; the narrower finding is that the merge sentences do not make the year boundary explicit, and the model's account (d1) reads another year as "another wording". |
| c14: "… evidence for it. Its figure for another year is a separate quantity, not another wording: this year's and next year's figure are two theses when an analyst would bet on each." | the same row; §3 "只开今年和明年"; §4 "开题标准 … 它的答案可能改变仓位 … 库里没有问题在问同一件事" | **consistent.** It restores the year identity (a separate quantity) and keeps the opening test. The first wording ("another year of it is not") read as barring another year's figure as evidence, against c8's "Do not exclude evidence solely because it concerns a related period" (the blind reader); the revised wording speaks of identity only, so cross-year evidence stays allowed. |
| c8 closing check: "A new thesis that asks the same underlying question, about the same subject and scope, as an open thesis or another new thesis is not proposed" | §4: "库里没有问题在问同一件事"; row D's identity "主题＋量＋期间" | **c8 keeps narrower for yearly quantities** (scope without period). |
| c14: "… about the same subject and scope (for a shared quantity, the same calendar year), …" | as above; §4 D248 boundary 2: "同一件事的不同截止日 … 晚的截止日是它的证据" (an event under another deadline stays one question); boundary 4: "公司自己的量只按财年开题；按日历年的估计是财年那题的证据" | **consistent**, limited to shared quantities and calendar years (the standard's row D identity), so events keep D248 boundary 2 and a company's fiscal year is not touched (boundary 4). |
| unchanged, interacting: "Do not open a thesis about … another estimate, source or wording of what an open thesis tracks; an annual quantity after next year" | §3 "只开今年和明年"; §4 boundary 1 | consistent; unchanged; it still refuses a year after next. |
| unchanged, interacting: "the closest open thesis with why an analyst would bet on the two separately because their answers can move apart" | §4 "另一题：同一件事里答案能分开走、分析员会分别下注的" | consistent; c14's year sentence gives the model a case where the answers can move apart (this year's spending against plan, next year's projection). |

**Principles (AGENTS §6).** General across companies: yes, the sentence names no company or industry ("this year's and next
year's figure" of any shared quantity). Growth: +206 characters, with a written reason (the standard's own identity missing at the
sentence the model cites; the four merge passages are not duplicates, so none is cut). No example added. The prompt still serves
every company; nothing is fitted to the bench's article.

**The whole request, schema included.** Read for every sentence on periods, years, sameness and dates, beyond the two changed: the
schema's `period` ("The period or check date that settles the thesis: the one the item supports, or the one its reason fixes"),
`closest_open_thesis`, `why_a_separate_bet` ("how their answers can move apart"), `evidence_period` and the figures' `period`
("as stated"); the system text's section 3 (the unit, the four reasons, the dates, the "do not open" list, the separate-bet test)
and the closing check. None contradicts the two edits; `why_a_separate_bet` is where a year split must be justified, and the c14
sentence gives the case ("this year's and next year's figure … when an analyst would bet on each"). No other sentence was found
that keeps wider or narrower than the standard on years. This is my read; the council's read is `council/lj-codex.md` and the
next round.

**The blind second read (`council/ll-codex.md`), the whole request clause by clause.** Besides the evidence wording (fixed above),
it found four things in c8 that c14 does not touch, recorded and not changed here (c8 is frozen, D391; one class at a time):
- the closing check's separate-bet test lets the same event under a later deadline open while the earlier is open, where the
  standard makes the later deadline evidence (D248 boundary 2): **keeps wider**, pre-existing;
- the four opening reasons have no company main-driver quantity (the standard's row A): **keeps narrower**, pre-existing (D370's
  product choice not to open company-figure questions may account for it; to be checked against D370 before it is called a defect);
- a company's fiscal-year rule for "an annual quantity after next year" is not stated: pre-existing;
- the schema's one `period` field serves both the covered period and the settling date: pre-existing.

**The second blind read (`council/ln-codex.md`), of the revised request.** Both edits are consistent with the standard: the year
sentence speaks of identity and leaves cross-year evidence to c8's "related period" instruction; the closing edit adds the calendar
year for shared quantities only; nothing else changed. Its verdict "no" rests on c8's pre-existing conflicts, the four above plus
two more: the closing check's "same subject and scope" beside "another population … is evidence" (pre-existing in c8's wording),
and Step 1 comparing against open theses where the standard gives that to matching (the clean design's reference-context choice,
recorded since D211's amendment). None is introduced by c14, and both arms of the probe carry them identically, so they do not
bias the comparison. They are findings for later classes; changing them needs Alex's word (c8 frozen, D391; D433's scope is the
year boundary). This judgement is mine and is reported to him.

**What the audit cannot show.** How the model applies the sentence: only sends show that (the c9 lesson, D388). The first test
measures it against c8's own spread on the same states.
