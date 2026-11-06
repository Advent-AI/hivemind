# Corrections to the extraction standard page

The extraction standard page, [`05-extraction-standard.html`](05-extraction-standard.html) (its version 5), is piece 1 of the frozen ruler
and is never edited (D261, AGENTS §7.1). A statement in it that a later decision changed is recorded here, dated, with its reason and its
before and after; the page is read together with these records, which are never merged into it. Records 1–3 below correct the page's description of the pipeline and judging; record 4 describes a later decision for a new evaluation version. Historical gold and scores do not change.

Recorded on 2026-11-05 (D368, on Alex's delegation: "你看该怎么处理核实"). Each statement was found verbatim in the page's text with its tags removed (the decision or PRD named at a quote's end is a link in the page).

## 1. What the extraction sees

- **Where:** §4, the test "not a duplicate" ("抽取看不到库D211，这一条在抽取时只对同一篇文章里提出的几个问题判；和库里的比由匹配做"), and §5.3,
  the row "known facts restated" ("抽取看不到库，只能从文字和日期看").
- **Before (D211):** the extraction request showed no question and no group of the library.
- **Now (D251, D264):** the request shows the questions open at the start of the item's day, each with its code-written takes line, and the
  extraction files each statement under them; it still sees no question's evidence or rung.
- **What still holds:** whether a candidate duplicates a question of the library is decided by matching (Jev with the collision judge,
  D169, D190); a restated known fact is still recognised from the text and its dates, since the extraction sees no stored evidence.

## 2. The research deliverable

- **Where:** §7 ("研究的交付物是论证：保留不可改的来源记录，和一份有版本的研究论证，写明支持和反对的来源、是否独立、变化和局限D201").
- **Before (D201):** the library would keep, besides the source records, a versioned research argument per question.
- **Now:** the argument record is not built. Two versions were measured on 2026-11-04 (judging-v8 and judging-v9) and set aside, and their
  code removed at Alex's word ("好，删掉卡片代码"; `docs/research/2026-11-04-argument-record/log.md`, rows 4–11). The library keeps the
  immutable source records, and each judgement stores its reasons, the outcome it implies and the evidence it cites with each piece's
  direction.

## 3. What decides a question's rung

- **Where:** §5, the relations between tiers ("判断时只有事实能确定到期落在哪一档PRD 06"), and §7 ("只有事实能确定落在哪一档PRD 06").
- **Before:** only the "fact" tier could establish the rung; the other tiers strengthened or weakened.
- **Now (D260, D263):** a judgement is a forecast: the rung the evidence in force makes most likely at the due day, judged against a
  reference (consensus, guidance, the stated plan or deadline); "not established" is never a reason to stay. The four tiers and counting
  by original source stand (D30): a fact fixes what is known, a party's own statement is the strongest input to the forecast, and views
  and rumours move it by their specificity. PRD 06 states the rule.


## 4. Capture of core and supporting evidence (D369; 2026-11-05 UTC)

- **Where:** §6 and §9.2–9.3 distinguish core and supporting, and score each separately.
- **Before:** core and supporting had separate evaluation thresholds under the frozen v5 ruler.
- **Future evaluation:** Alex decided that both should be captured without a strict pass/fail boundary between them. An indirect item may be retained when the model judges it relevant and the logic is clear; the reviewed MXC announcement is retained as supporting. Do not present inference as a sourced fact. The optional and not-kept boundaries, source tiers and quality checks are not changed by this decision.
- **Status:** the v5 page and its gold remain frozen. A new evaluation version and its gold require derivation, independent review and Alex's sign-off before scoring; old scores retain their original definitions.

## 5. Research-library context timing (D375; 2026-11-05)

- **Before:** D251/D264 described the open-question snapshot at the start of the item's day.
- **Current design:** Alex decided that each item reads the latest committed questions immediately before it, including earlier same-day writes. The two split extraction calls for that item share the same snapshot.
- **Status:** this changes the product design, not the frozen standard page or its historical gold and scores. The existing default still uses day-start context; implementation and acceptance of the new path are pending.
