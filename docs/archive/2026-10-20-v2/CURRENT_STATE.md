# Current state

As of 2026-10-20. The design lives in `docs/system-design.html` (New tab); decisions D1–D43 in `docs/DECISIONS.md`.
The work is an architecture POC: the design page, a PRD per module and DECISIONS; no code.

## Status

- Sealed copies: v1 `docs/archive/2026-10-16-v1/`; v2 `docs/archive/2026-10-20-v2/` (D43, after the full refresh of
  2026-10-20). Each has `SHA256SUMS` and is never edited.
- PRDs (D20): one per module in `docs/prd/` (index `README.md`), viewable from each module on the design page.
- After any change, Claude refreshes everything by reasoning, module by module (D22, procedure in
  `docs/prd/README.md`); `python3 docs/check.py` is only the last, mechanical step.
- Frozen v1 (D19, D37, 2026-10-18): the research universe, classification, Config, dispatch, extraction and the
  human review pool, in their current text; a change needs a new decision. D41 and D42 (2026-10-20) changed four of
  them for the rebuilt views database: extraction's hand-over and prompt part 5, Config's views settings, the
  universe's macro rule, the review pool's views inputs. Open inside them is what each PRD lists
  under "还没定的", among them the themes in the theme library, upstream supply, the review pool's output, each category's prompt wording.
- Boundary (D10): the system consumes a stream of classified items; dispatch is the single entry (D17). Upstream
  supply and classification are outside. Testing is a test feeder streaming a test database through the same path.
- Two modes (D14): stream mode, driven by arriving information and never by the calendar (D12, D13); pull mode, the
  only place time triggers work: in the rebuilt design, due dates and the daily duplicate check.
- Core, rebuilt (D38, D42): a view is one question, a ladder and a due date, never rewritten; the ladder has five
  rungs, or two for a yes-or-no question; identity is object plus what it looks at (a number with its year, or the
  state of one thing). Object views rank strongly bullish to strongly bearish for the business; theme views name their
  outcomes and leave good or bad to each dependent's arrow. Two positions: where it is now (only "happened" evidence)
  and the state (re-judged from the view's evidence that has not been replaced). Evidence is stored once with its
  source and tier; its push is on the link. A dependency links only an input (B's answer uses A's
  answer); number dependencies pin the year, event dependencies follow the succession chain; a cycle is rewritten.
  Views end answered, unanswerable or merged. The discussion is in `docs/views-rebuild-log.md`.
- Writing into the views database (D39, D42): one round per item. Candidate views: key match, a short list (the
  objects' open views, a search for themes), then the matching call (attach, succeed, new, not opened, unsure). The
  same call compares each piece of evidence with the evidence its view holds (repeat, replacement, new evidence); a
  piece on several views is stored once; a replaced piece's other views get the new piece; a corrected version
  changes only its own source. Views that got new evidence or a replacement, or whose dependencies changed, are
  re-judged once, upstream first; repeats alone re-judge nothing. Merges: attach, succeed, and a daily
  duplicate check. Records are append-only; one relational database with rebuildable search indexes.
- Matching judge (D40, D42): a general model first; every match recorded; a sample
  labelled by people (test labels blind to the model's answer); labels measure the matching and later train a small
  matcher that takes over where confident.
- Extraction (D27, D33, D35, D37, D41, D42; v1 frozen): only reads. Every item goes whole to the model, read by its
  category's template as a senior hedge fund analyst; prompt part 5 lists the related objects' open views and the
  views they depend on (question and what each looks at). It hands over two things with sources: evidence attached to
  those views or to a candidate view of the item, and candidate views (question, ladder, due date, answer source) for
  important matters those views do not cover. Financial reports stream again (D28). Table data comes one release per item and a filing's XBRL
  numbers are not pushed again; nothing gets a price-specific rule (D32).
- Final verdict (D29) and pull mode: old drafts written for the previous views design; to be redone on D38–D40 (D41).
- Order and sync (D31, D39): numbers in arrival order, one writer per view (themes first), reads only the state left
  by earlier items; a late item is re-judged on arrival without rewriting past states.
- Wording (D36, D41, D42): one word per concept in the universe, classification, dispatch, extraction and the views
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

Alex reviews the stable version (v2) on the page and in `docs/prd/05-extraction.md` and `docs/prd/06-views.md`, then
settles the open items there; the two that matter most are opening views when an object starts empty (a
start-of-coverage step that sets two or three key debates) and changes inside a rung that do not reach dependents.
Then the final verdict and pull mode are redone on the new design, as Alex takes them up. Deferred by Alex: upstream
supply; the review pool's output.
