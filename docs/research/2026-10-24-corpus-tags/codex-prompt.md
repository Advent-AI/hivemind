# Review request: the POC corpus's labels (read-only)

You are reviewing how the POC test corpus labels each item, so that the labels can be tightened before the next
replay. Read-only: do not modify files, do not run anything that writes, do not call any model API.

## What to review

The labelling code and tables (the only place labels are written):

- `poc/corpus/scripts/assemble.py` — builds `items.sqlite` from `poc/corpus/raw/`; every rule that sets
  `object_identifiers` (which company or theme an item is about and `why`), `category` (T1…T11), `publisher_type`
  (company | media | analyst | official | individual), `klass`, `copy_of`, `coverage`/`feed`, `publication_day`.
- `poc/corpus/scripts/author-table.json` (domain → publisher type; aggregators), `companies.json` (peer companies and
  the themes their filings carry), `topics.json` (Google News topics → objects).
- The harvesters only decide what is fetched: `harvest_gnews.py`, `harvest_gnews_topics.py`, `harvest_official.py`,
  `harvest_edgar.py`, `harvest_edgar_peers.py`, `harvest_truenorth.py` (skim for anything that pre-labels).

The data to count on (SQLite, open read-only, e.g. `sqlite3 "file:poc/data/items-window.sqlite?mode=ro"`):
`poc/data/items-window.sqlite`, table `items` (columns: input_id, klass, category, publisher, publisher_type,
publication_day, object_identifiers (JSON list of {kind, value, why}), title, text, text_article, coverage, feed,
source, topic, tier, extra, copy_of). The replay fed rows with `feed = 1` between 2026-07-24 and 2026-08-15 (740 rows)
plus NVDA's documents from 2026-02-25.

What the labels are supposed to mean (the governing documents; the corpus must follow them, they are not under
review): `docs/prd/01-universe.md` (the research list: which objects, which categories each is watched in; the POC's
list is `poc/universe.json`), `docs/prd/02-classification.md` (the 16 categories, the author table, copies, the time
rules), `docs/prd/03-inputs.md` (what an item carries), and `docs/poc/corpus-plan.md` (what the corpus was meant to
hold; note its rule "不筛内容，相关不相关由后面的管线判" and the "noise" tier that was put in on purpose).

How the labels are consumed, for reference only (do not review this code): `src/hivemind/dispatch.py` routes an item
to extraction only when one of its objects is on `poc/universe.json` and that object watches the item's category;
`src/hivemind/extraction.py` `build_prompt` tells the model "这条信息的相关对象：<objects>" and reads the category's
block from `src/hivemind/prompts/categories-v2.json`.

## What to deliver

1. **A table of every labelling rule**: field written, the rule in one sentence, file:line, which rows it fires on
   (count on the window database).
2. **For each rule, where it is too loose or too tight**, counted on the database with 2–3 concrete examples
   (input_id, title): rows it lets in that the governing documents would not call "about" that object or that
   category, and rows it keeps out that they would. Say which consumer the error reaches (routing, the prompt's
   object line, the category block, the tier the model assigns to a speaker).
3. **One tightening proposal per rule that needs one**, as a single structural rule (not a list of exceptions), with
   the expected effect counted on the database (rows added or removed, by source and category) and what would be
   lost. Prefer rules a reader can check from the row itself (title, publisher, exhibit type) over keyword lists.
4. **Anything the labels cannot express** that the governing documents require (e.g. an item about several objects,
   a press release issued by a company other than the object it names).

Rank findings by how many fed rows they touch. Count by field and path, not by substring, and check each census on
one row whose answer you know. Report numbers you computed, with the query.

## Out of scope

The pipeline code under `src/hivemind/`, the prompts, the design documents and decisions, the model's behaviour,
and anything about re-running: do not propose changes there and do not write them into any document. A gap in a
module not listed above is not a finding.
