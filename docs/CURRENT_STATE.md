# Current state

As of 2026-10-18. The design lives in `docs/system-design.html` (New tab); decisions D1–D37 in `docs/DECISIONS.md`.
The work is an architecture POC: the design page, a PRD per module and DECISIONS; no code.

## Status

- Sealed copy of v1: `docs/archive/2026-10-16-v1/` (checksums in `SHA256SUMS`).
- PRDs (D20): one per module in `docs/prd/` (index `README.md`), viewable from each module on the design page.
- After any change, Claude refreshes everything by reasoning, module by module (D22, procedure in
  `docs/prd/README.md`); `python3 docs/check.py` is only the last, mechanical step.
- Frozen v1 (D19, D37, 2026-10-18): the research universe, classification, Config, dispatch, extraction and the
  human review pool, in their current text; a change needs a new decision. Open inside them is what each PRD lists
  under "还没定的", among them the themes in the theme library, upstream supply, the review pool's output, each category's prompt wording.
- Boundary (D10): the system consumes a stream of classified items; dispatch is the single entry (D17). Upstream
  supply and classification are outside. Testing is a test feeder streaming a test database through the same path.
- Two modes (D14): stream mode, driven by arriving information and never by the calendar (D12, D13); pull mode, the
  only place time triggers work: due views to the final verdict, back-up re-checks, periodic driver merges (D29, D31).
- Core (D26): the system builds, updates and closes a views database (thesis · ladder · evidence): object → driver →
  view with evidence, conditions and an optional premise; theme views and object views linked by premises; views are
  the model's judgments, evidence is objective; every view, piece of evidence and change carries its source; closed
  views are kept.
- Extraction (D27, D33, D35, D37; v1 frozen): only reads. Every item goes whole to the model, read by its category's template as a senior
  hedge fund analyst, into candidate views and evidence with sources, handed to the views database. The views
  database merges duplicate evidence, matches each candidate to a driver (all drivers of the related objects in full
  plus a search over theme drivers; a short model call), and code decides by direction and horizon class. Financial reports stream again
  (D28). Table data comes one release per item and a filing's XBRL numbers are not pushed again; nothing gets a
  price-specific rule (D32).
- Final verdict (D29): no view is closed without it; only conditions plus "happened" evidence close a view as confirmed
  or falsified; expiry at the due date is not a judgment, and no evidence at all is "no data to verify".
- Conflicts (D30): four evidence tiers, independent sources counted by original source, conditions add-only,
  consensus computed by code, source records shown only.
- Order and sync (D31): numbers in arrival order, one writer per view, reads only the state left by earlier items;
  premises are links with a seen version.
- Wording (D36): one word per concept in the universe, classification, dispatch and extraction; the glossary is in
  `docs/prd/00-system.md` and `docs/check.py` fails on an avoided word.
- Research behind extraction and matching: `reports/SEC 财报 代码抽取 开源方案.md`, `reports/观点库 向量检索 去重匹配.md`,
  `reports/观点库匹配 业界做法对比.md`.

## Open defects

- `simulate_classification.py` resolves a ticker on the UTC date of `published_at`; the page says the New York
  publication day (D9). It does not model the SEC filing day (D34), and has no cases for the macro rules (D15) or for
  crypto, commodity and theme objects (D11). The script is not changed at the POC stage.

## Next task

Move on to the modules still in design, as Alex takes them up: the views database, the final verdict and pull mode
(drafted on the page, not reviewed). Deferred by Alex: upstream supply; the review pool's output.
