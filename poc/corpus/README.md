# The corpus toolchain

Raw harvest in `raw/` (listings, resolved links, fetched pages with their HTML under `raw/pages/`, EDGAR, official
notices, company blogs). Scripts in `scripts/`:

| step | script | writes |
|---|---|---|
| harvest | `harvest_*.py`, `resolve_gnews.py`, `fetch_bodies.py` | `raw/` (resumable; window from `HIVEMIND_WINDOW_START/END`) |
| assemble | `assemble.py` | `items.sqlite`: one row per document, whole-page text (`common.page_text`), labels |
| freeze | `relabel.py --in items.sqlite --out poc/data/<name>.page.sqlite` | the window a run reads, whole pages as fetched |
| clean (D351) | `clean_pages.py --in <name>.page.sqlite --out <name>.sqlite` | the source every script reads: line rules plus the trafilatura extractor over the stored HTML; the page stays in `text_page`, counts in `cleaning` |
| check | `check_corpus.py` (worktree, `docs/research/2026-10-27-nvda-3m/`), `sweep_pages.py` | per-day feed counts; a census of what still looks like junk |
| all of it | `freeze_window.sh <name> <from> <until>` | the chain above into new dated files |

Tests: `python3 -m pytest poc/corpus/scripts/test_labels.py poc/corpus/scripts/test_clean.py -q`. Dependency of the corpus
scripts only: `pip3 install -r poc/corpus/scripts/requirements.txt`. The cleaning's numbers and audits:
`poc/reports/items-nvda-2026-07-01-10-27-cleaned.census.md`.
