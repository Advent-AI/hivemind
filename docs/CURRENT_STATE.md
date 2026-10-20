# Current state

As of 2026-10-20. The design lives in `docs/system-design.html` (New tab); decisions D1–D50 in `docs/DECISIONS.md`.
The work is an architecture POC: the design page, a PRD per module and DECISIONS; no code.

## Status

- Sealed copies: v1 `docs/archive/2026-10-16-v1/` (the earlier design) and v7 `docs/archive/2026-10-20-v7/` (D49), the
  current stable version with the views database frozen. Each has `SHA256SUMS` and is never edited. The superseded
  v2–v6 were removed from the tree (D50) and are in commit `94622a5`.
- PRDs (D20): one per module in `docs/prd/` (index `README.md`), viewable from each module on the design page.
- After any change, Claude refreshes everything by reasoning, module by module (D22, procedure in
  `docs/prd/README.md`); `python3 docs/check.py` is only the last, mechanical step.
- Frozen v1 (D19, D37, 2026-10-18): the research universe, classification, Config, dispatch, extraction and the
  human review pool, in their current text; a change needs a new decision. D41, D42 and D45–D47 (2026-10-20) changed
  them for the rebuilt views database: extraction's hand-over and prompt part 5, Config's views settings, the
  universe's macro rule, the review pool's views inputs. Open inside them is what each PRD lists
  under "还没定的", among them the themes in the theme library, upstream supply, the review pool's output, each category's prompt wording.
- Boundary (D10): the system consumes a stream of classified items; dispatch is the single entry (D17). Upstream
  supply and classification are outside. Testing is a test feeder streaming a test database through the same path.
- Two modes (D14): stream mode, driven by arriving information and never by the calendar (D12, D13); pull mode, the
  only place time triggers work: in the rebuilt design, due dates; not designed yet.
- Frozen v1 (D48, 2026-10-20): the views database with match labelling, after the six-round consistency pass
  (D47), cleaned up after a code review (D49); a change needs a new decision.
- Rule for the views database (D45): only what Alex said or decided is written as decided. On 2026-10-20 he went
  through Claude's proposals one by one (D46); what is left of them is three items for pull mode.
- Core, rebuilt (D38, D42, D45, D46): a view is one question, a ladder and a due date, never rewritten; the ladder has
  five rungs, or two for a yes-or-no question, each rung a result that can be checked, rungs neither overlapping nor
  leaving gaps. One open view per thing (a number: this year and next, counted from the item's own year). Object
  views rank strongly bullish to strongly bearish for the business; theme views name their outcomes. A view has one
  state: where it sits on its ladder, pushed by evidence and judged by the model on facts; every judgement cites its
  evidence by number and code looks the numbers up. Evidence is stored once with its source and tier (D30). Views
  relate in one way: a view refers to another's conclusion (state and reasons), chosen by the model, never stored as
  evidence; code keeps these links free of loops. A message counts once, on the view it is about. The discussion is
  in `docs/views-rebuild-log.md`.
- Writing into the views database (D39, D42, D44–D46): one round per item, eight steps. A candidate view searches
  the whole views database (a search engine, how it ranks is to be designed; top N, N in Config, 10 to start); the model decides
  the same view or a part of it, its next period, a new view (no match or a weak one), or not opened (too broad).
  Evidence searches the evidence of its own view; the model decides repeat, replacement or new evidence. Upstream
  views are judged before downstream ones, each once per round. The timeline only grows forward: a late statement
  on a matter that already has a newer one does not count. Records are append-only; storage is chosen at build time.
- Matching judge (D40, D44, D46): the model alone decides; a general model first; every match recorded; people label
  the ones code refused and a few drawn at random; the labels later train a smaller, faster model.
- Extraction (D27, D33, D35, D37, D41, D42, D46; v1 frozen): only reads. Every item goes whole to the model, read by
  its category's template as a senior hedge fund analyst; prompt part 5 lists the related objects' open views and the
  views they depend on. It hands over evidence, each piece on the view it is about, and candidate views written in
  full (question, ladder, due date) for important matters those views do not cover. Financial reports stream again
  (D28). Table data comes one release per item and a filing's XBRL numbers are not pushed again (D32).
- Final verdict (D29) and pull mode: old drafts written for the previous views design; to be redone on D38–D40 (D41).
- Order and sync (D31, D46): numbers in arrival order, one writer per view (themes first), reads only the state left
  by earlier items plus what its own round has written; the timeline only grows forward (D46 replaced D31's late-item rule).
- Wording (D36, D41, D42, D44–D47): one word per concept in the universe, classification, dispatch, extraction and the views
  database; the glossary is in `docs/prd/00-system.md` and `docs/check.py` fails on an avoided word.
- Research behind extraction and matching: `reports/SEC 财报 代码抽取 开源方案.md`, `reports/观点库 向量检索 去重匹配.md`,
  `reports/观点库匹配 业界做法对比.md`, `reports/观点库重建 去重 证据 血缘（Codex 调研）.md`,
  `reports/观点库重建 接续 依赖 到期（Codex 调研）.md`, and for the evidence path the four 2026-10-20 reports named in D42;
  Codex reviewed the first D42 write-up in five read-only rounds (`reports/观点库重建 D42 审稿第 1–5 轮（Codex）.md`); the
  rules added for review edge cases were removed, four that real cases need were kept (log steps 32–33).

## Open defects

- `simulate_classification.py` resolves a ticker on the UTC date of `published_at`; the page says the New York
  publication day (D9). It does not model the SEC filing day (D34), and has no cases for the macro rules (D15) or for
  crypto, commodity and theme objects (D11). The script is not changed at the POC stage.

## Next task

Research, as Alex asked: what a thesis looks like from a hedge fund's side, so that the granularity of views is
neither too big nor too small (what to combine, what to carve out; a key part such as NVDA's China revenue stays its
own view; views must not all be financial-statement lines). Then the open items of the views database, the most
important being changes inside a rung that do not reach the views that refer to it, and opening views when an object
starts empty. Then pull mode and the final verdict are designed on the new views database, as Alex takes them up
(three of Claude's proposals wait for that). Deferred by Alex: upstream supply; the review pool's output.
