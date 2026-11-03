# Page cleaning census: items-nvda-2026-07-01-10-27-cleaned.sqlite (2026-10-27, final)

Alex: "你先清理干净html 还有一些垃圾吧，至少确保这些数据信息基本上都是有用，可以抽取的 … 不要让我们的评估eval 会因为这些数据而被影响";
then "你确定这次这些数据都是属于好的，干净可用的吗？" and "不是你tmd 给我扫一遍啊". Script `poc/corpus/scripts/clean_pages.py`
(tests `test_clean.py`, 12 pass; rule mutants caught), sweep `sweep_pages.py`. The source database is untouched; the page
is kept in `text_page`, the counts per page in `cleaning` (JSON); the raw HTML stays in `poc/corpus/raw/pages/`.

## How a page is cleaned

1. Line rules on the page text, all closed: a publisher's template lines (in 3+ of its original pages; copies excluded);
   on article pages, fragments (under 40 characters, no digit, no end punctuation) except bylines; lines without a
   letter; lines repeated in the page; a closed list of boilerplate sentences (consent, legal, subscription, credits,
   "Read more"/"Also read" links, broker disclosures, CMS lines such as "Tags:", "0 Comments"); datelines and
   "N min read"; runs of three or more short unpunctuated lines (headline lists), keeping lines with a digit;
   forward-looking-statement paragraphs.
2. The HTML extractor (trafilatura 2.3.1, favour recall; a measured dependency) reads the stored HTML of every fed
   article (6,431 of 6,463 have one; 32 NVIDIA blog rows do not). The rule-cleaned page lines are kept in page order
   when the extractor's text contains them, when they are a byline, or when they are prose of 120+ characters with
   end punctuation (the extractor truncates some Yahoo and Fool articles, tail figures included; the re-add rule
   keeps them).
3. An article left with fewer than 3 lines of 120+ characters is not fed (`feed = 0`, `coverage = 'none'`).

## Numbers over the whole database

| | pages | chars before | chars after | kept | unfed |
|---|---:|---:|---:|---:|---:|
| all | 34,084 | 104,440,806 | 56,639,635 | 54% | 615 |
| T7 | 27,574 | 59,702,697 | 27,251,661 | 46% | 577 |
| T8 | 4,914 | 14,044,535 | 5,702,526 | 41% | 35 |
| T10 | 772 | 10,262,935 | 7,056,107 | 69% | 0 |
| T6 | 622 | 7,702,603 | 5,683,004 | 74% | 3 |
| 不算材料 | 72 | 229,128 | 174,575 | 76% | 0 |
| T3 | 43 | 4,723,146 | 4,303,300 | 91% | 0 |
| T1 | 28 | 696,548 | 623,506 | 90% | 0 |
| T11 | 28 | 1,536,700 | 433,938 | 28% | 0 |
| T4 | 16 | 784,939 | 784,173 | 100% | 0 |
| T2 | 15 | 4,757,575 | 4,626,845 | 97% | 0 |

Fed NVDA articles in the window (non-copy): 3,587, extractor used on 3,555; share of characters kept per article
p10 26%, median 44%, p90 76%. `check_corpus.py`: fed 3,852 → 3,643, median text 9,027 → 3,904 characters, no new
empty day, 0 duplicate texts. Full sweep of every remaining line (`sweep_pages.py`, 5,503 fed non-copy articles,
120,080 lines): lines with a broad junk keyword 1.0% of characters (mostly prose that merely contains the word);
unpunctuated short lines 2.7%; headline-list runs 489 (from 5,691 before the extractor).

## Line-by-line audits (an Opus reviewer labelling every line; assistant labels, not human gold)

| sample | junk share of characters | pages > 10% junk | lost body |
|---|---:|---:|---|
| 30 random pages, line rules only (first version) | 24.2% | 15 of 30 | tables lost their row labels; one video page without a story |
| 30 fresh random pages, final (rules + extractor) | **4.0%** (5.0% counting unsure) | 2 of 30 | 24 lines on 15 pages: 8 with information (a lede, a list bullet, five quotes, one sentence), 10 subtitles / key points repeating the text, 6 captions; no story missing |

Configurations measured on the first labelled sample before choosing (body recall / junk surviving / junk share of
output): line rules alone 98.5% / 88.6% / 22.5%; extractor alone (favour recall) 88.1% / 21.9% / 7.4%; extractor +
rules + re-add 94.1% / 46.9% / 13.9%. The extractor alone cut the tail of Yahoo and Fool articles (figures included),
so the union was chosen; the final audit on a fresh sample gave the 4.0% above.

Positive control (test): the three benchmark articles' hand-curated reporting lines (D338 `*.clean.txt`, 40+
characters or the byline, headline line excluded) all survive the final path; known junk lines are gone.

## Known residue and known loss, for the later data pipeline

- Residue (4% of characters): author bio boxes, a site's own tool promos ("See what NVIDIA's 26.4x P/E says…"),
  publisher self-descriptions, a paid-investment pitch, two other press releases' summaries inside one release.
- Loss (about 1.5% of body lines): short quotes, ledes and list bullets the extractor left out and that are under the
  120-character re-add line; subtitles and figure captions. Inline ticker chips "( NVDA +2.56% )" stay inside prose.

Unfed pages (615), first 40 (publisher, category, title, lines before → after):
- ('cnbc.com', 'T7', "Here are Friday's biggest analyst calls of the day: Nvidia, SpaceX, Te", 165, 1)
- ('investors.com', 'T7', 'Nvidia Gets No Break Amid Big Tech Earnings Beat; Is Nvidia A Buy Or S', 337, 2)
- ('navercorp.com', 'T6', 'Chairman Lee Hae-jin Announces Major Partnership with NVIDIA and Brook', 280, 6)
- ('cnbc.com', 'T7', "Nvidia's potential $250B backstop for OpenAI is another strike against", 164, 1)
- ('cnbc.com', 'T7', "Here are Monday's biggest analyst calls: Nvidia, SpaceX, Tesla, Apple,", 165, 1)
- ('cnbc.com', 'T7', "Here are Wednesday's biggest analyst calls: Nvidia, SpaceX, AMD, Snowf", 165, 1)
- ('fool.com', 'T8', 'Massive News for Nvidia Stock Investors', 295, 4)
- ('afr.com', 'T7', 'This Nvidia deal is sparking fears markets could ‘go straight down’', 261, 4)
- ('investors.com', 'T7', 'Nvidia Stock Rises As Microsoft Soars On Capex Control, Earnings Beat;', 337, 2)
- ('asia.nikkei.com', 'T7', 'Why Nvidia and others in Silicon Valley oppose a US ban on Chinese AI', 303, 3)
- ('cnbc.com', 'T7', "Here are Thursday's biggest analyst calls: Nvidia, Jersey Mike's, AMD,", 165, 1)
- ('cnbc.com', 'T7', "Here are Friday's biggest analyst calls: Nvidia, SpaceX, Apple, Amazon", 165, 1)
- ('investors.com', 'T7', "Nvidia Earnings: Turn A $265 Profit Trading Around The AI Chipmaker's ", 337, 2)
- ('cnbc.com', 'T7', "Here are Monday's biggest analyst calls: Nvidia, Apple, SpaceX, Dick's", 165, 1)
- ('paulweiss.com', 'T6', 'Apollo Partners With NVIDIA to Establish AI Compute Infrastructure Fin', 92, 2)
- ('investors.com', 'T7', 'Nvidia Stock Wavers As Chipmaker Rounds Up Funding For AI Buildout', 337, 2)
- ('cnbc.com', 'T7', "Here are Wednesday's biggest analyst calls: Nvidia, SpaceX, Tesla, Cor", 165, 1)
- ('cnbc.com', 'T7', "Here are Thursday's biggest analyst calls: Nvidia, SpaceX, AMD, Five B", 165, 1)
- ('investors.com', 'T7', 'Nvidia, IBD Stock Of The Day, Nears Buy Point Ahead Of Fiscal Q2 Earni', 337, 2)
- ('investors.com', 'T7', 'Nvidia, ASML Lead Five Stocks Near Buy Points With Roaring Growth', 337, 2)
- ('cnbc.com', 'T7', "Nvidia's stock has started to come alive. Here's 3 reasons why it can ", 164, 1)
- ('newcomer.co', 'T7', 'SOURCES: Poolside Strikes $6 Billion Licensing Deal with Nvidia & Rais', 19, 1)
- ('spacenews.com', 'T7', 'Nvidia joins Starcloud’s $250 million orbital data center funding roun', 236, 5)
- ('gurufocus.com', 'T8', "Nvidia's AI Chips Are Heading Into Space", 289, 2)
- ('seekingalpha.com', 'T8', 'Nvidia to hike AI server prices over 15% as memory chip costs soar - r', 128, 2)
- ('cnbc.com', 'T7', "Here are Monday's biggest analyst calls: Nvidia, Jersey Mike's, Dell, ", 165, 1)
- ('gurufocus.com', 'T8', "Nvidia's Earnings Could Trigger a $280 Billion Swing", 284, 1)
- ('finance.yahoo.com', 'T7', "Nvidia's Second-Quarter Results More Than Double Amid Record Data Cent", 289, 2)
- ('cnbc.com', 'T7', "Here are Thursday's biggest analyst calls: Nvidia, SpaceX, Tesla, Alph", 165, 1)
- ('gurufocus.com', 'T8', 'Nvidia Pulls Back on a Risky AI Cloud Strategy', 284, 1)
- ('cnbc.com', 'T7', "Here are Friday's biggest analyst calls: Nvidia, SpaceX, Tesla, Amazon", 165, 1)
- ('tech-insider.org', 'T7', 'Nvidia RTX 5090 Tops $5,000 as GPU Prices Jump 39% [2026] - https://te', 251, 0)
- ('phoronix.com', 'T7', 'Vulkan 1.4.361 Released With New NVIDIA Vendor Extension', 281, 0)
- ('cnbc.com', 'T7', "What caused Nvidia's nasty reversal Friday? Look to the Fed for clues", 164, 1)
- ('tech-insider.org', 'T7', 'OpenAI Jalapeño Chip Beats Nvidia by 1.9x on Power [2026] - https://te', 251, 0)
- ('phoronix.com', 'T7', 'NVIDIA Vulkan Frame Rate Up-Conversion "FRUC" Merged To FFmpeg', 281, 0)
- ('tech-insider.org', 'T7', 'Nvidia Faces 4 Custom Chip Rivals After OpenAI Move [2026] - https://t', 251, 0)
- ('fool.com', 'T8', "Here Was My Biggest Concern Before Nvidia's Earnings. Did It Play Out?", 290, 4)
- ('tech-insider.org', 'T7', 'Nvidia RTX Spark Sinks Intel, AMD Stock 4.4% [2026] - https://tech-ins', 251, 0)
- ('fool.com', 'T8', "What's Going on With Nvidia Stock?", 295, 4)
