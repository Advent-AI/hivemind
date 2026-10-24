# Disposition of the Codex review of the corpus labels (2026-10-24)

The review is `codex-review.md` (read-only, prompt in `codex-prompt.md`). Each finding was checked against the code
and the frozen window database before anything changed; what was built lives in `poc/corpus/scripts/assemble.py`
(the one place labels are written), is proven in `test_labels.py` on real stored rows, and is applied to a copy of the
frozen corpus by `relabel.py` → `poc/data/items-window-tags2-2026-10-24.sqlite`. The frozen corpus and the sealed
run are untouched. Counts are N/F: rows in the whole database / rows fed in the 2026-07-24..08-15 window.

| # | Codex finding | Checked | Done |
|---|---|---|---|
| ① | `publisher` of Federal Register notices is "Federal Register", the channel, not the issuing agency (756/199) | Confirmed; 02-classification 作者规则 3 | `official_publisher(source)`: BIS, USTR, Department of Commerce, BLS, Federal Reserve Board. 756 rows relabelled |
| ② | Peer companies' themes are inherited by every exhibit, incl. certifications and consents (254/123 labels; 57/29 on certification exhibits) | Confirmed | Themes ride only on T1/T2/T4 (`THEME_CARRYING_CATEGORIES`); certification exhibits are 不算材料 (my census). 163 rows lose a theme label; routing unchanged (the ticker stays) |
| ③a | Aggregator pages (Yahoo, Morningstar) keep the aggregator as author (65/49) | Confirmed; found independently | `byline_outlet` + `page_author`: 39 of 72 aggregator pages get their outlet; 34/30 rows T7→T8 |
| ③b | Company-owned newsrooms default to media (15/11: IBM, SK hynix, Naver, CoreWeave, OpenAI, AWS, law firms…) | Confirmed | 13 domains added to the author table as company → T6 |
| ③c | Research sites and analyst columns default to media (11/9) | Confirmed for domains; the "CNBC Investing Club" column cannot be read from the row | 9 domains added as analyst → T8; columns left (02-classification wants a series table the corpus does not have; noted under "cannot express") |
| ④ | Copies only among news rows; 28/21 Google listings of NVIDIA newsroom/blog pages were separate items; copies do not inherit labels | Confirmed | `mark_copies` keys every row by canonical URL, company/official rows first as originals: 28 rows become copies (routing 合并). Label inheritance not built: a copy is never fed, so its labels reach nothing |
| ⑤a | CNBC video pages fed as full (10/9) | Confirmed | `page_texts(page, url)`: a `/video/` path is coverage `video`, feed 0. 12 rows |
| ⑤b | Official harvest file names collide (title cut at 80 chars): 97/17 rows, 56/9 with the wrong body | Confirmed as a harvest defect | Not relabelled (the text is wrong, not the label; all 17 window rows carry no object and were never routed). Fix belongs in `harvest_official.py` (name files by URL hash) and a re-fetch before the next corpus build; recorded as an open defect |
| ⑥ | Official themes both too wide (BIS pharma tariffs, FTZ notices) and too narrow (two China AD/CVD notices missed); Codex holds that Commerce China AD/CVD notices do belong to 中美关税 (29 in window) | Half agreed | Commerce notices carry no object at all (my rule, kept): the theme in `poc/universe.json` is the macro tariff fight that moves NVDA, and the 29 AD/CVD notices on mattresses, crepe paper and graphite electrodes produced only junk views in the run. BIS and USTR keep their source themes; the pharma-tariff and FTZ examples are 1 and 3 rows and are reported, not special-cased. **This is the one point of disagreement; Alex decides** Settled 2026-10-24 by Alex's thesis test ("你自己评价下是不是会有影响的 thesis"): of 89 China notices none mentions the chip or server supply chain, and the ledger cites Commerce evidence only under the 5 procedural tariff views (0 dependants); the rule stays. |
| ⑦ | Peer call objects say `why='filer'` (13/6) | Confirmed, cosmetic | reason now "the company speaking on its own call" |
| ⑧a | 8-K Item 2.02 read from the table of contents, so Amazon's two results exhibits were T6 (2/2) | Confirmed | `item_202_section` takes the longest Item 2.02 body; test on the real Amazon rows |
| ⑧b | 6-K EX-99 with a bare description falls to T6 though the cover says results (6/1) | Confirmed | the exhibit's own cover is read when the description is a bare number; test on the real TSM row |
| ⑨ | "NVIDIA Sets Conference Call for … Financial Results" is T1 (1/1) | Confirmed | newsroom rule requires "reports/announces … financial results" and excludes "conference call" |
| ⑩ | Fed speeches all T11 and all 利率 theme (9/0) | Confirmed, outside the window | Not changed now; needs a series table (02-classification 发布系列表) rather than a URL rule; recorded |
| — | Cannot express: series/column, author table validity periods, several reasons per object, `supersedes` never written | Agreed | Recorded; none affects the window |

Also from my own census (before Codex returned), kept: Google News "nvidia" topic → NVDA label needs no tightening
(405/422 titles name NVIDIA; a title or word-count rule would lose the useful 6 of the other 17); whole-page text costs
about $0.65 more than article bodies over the window (Alex's rule: original, unprocessed); the topic harvests are not
in the corpus yet and need the same census before they are added.

Effect on the window range 2026-02-25..08-15 (fed rows): 771 → 720; routed to extraction 584 → 480 (T10 38 → 6,
T6 149 → 96, T7 300 → 251, T8 65 → 92, T1 11 → 14); copies 8 → 29. Fields changed and nothing else: publisher 790,
object_identifiers 281, category 139, feed 84, document_format 80, extra 61, publisher_type 59, copy_of 28,
coverage 12, tier 105.
