"""Clean fed pages before the pipeline reads them, into a new dated items database.

`common.page_text` keeps the whole page (navigation, member offers, footers), as D27 asked; measured on the frozen NVDA
window the template lines of a publisher hold a median 44% of a page's characters, and a paywalled page can hold no
article at all. Five closed rules, applied to the stored page text, each reversible (`text_page` keeps the page):

1. A template line: a line that appears in TEMPLATE_PAGES or more pages of the same publisher is removed from every
   page (navigation, membership offers, footers, "About <company>" boilerplate, syndicated repeats).
2. A fragment, on an article page only (`document_format = 'article'`): a line shorter than SHORT_LINE characters
   with no digit and no end punctuation is removed ("Skip to main content", "GO PREMIUM"), except a byline: a line
   starting with "By " is kept, and a line that is only "By" is joined with the name on the next line (712 of 6,463
   fed articles carry the byline as such a fragment; the author is the article's own speaker). Subheadings and
   captions without punctuation go with the fragments. A filing, release or transcript keeps its short cells and
   headings.
3. On an article page, a boilerplate sentence from a closed list (consent and legal lines, subscription and newsletter
   offers, copyright, image credits, "Read more:" links, broker disclosures, "N min read", "N hours ago"), a dateline
   ("Published Thu, Oct 22 2026 9:12 AM EDT", "October 26, 2026"), and a list of headlines: a run of three or more
   consecutive lines of at most RUN_LINE characters without end punctuation (a sidebar of other stories), of which
   the lines without a digit are removed (a table of figures rendered as lines stays). A byline is "By" and a name
   ("By Alex Veiga | The Associated Press"); "By subscribing, you agree …" is not one.
4. On an article page, a line with no letter (a market widget's "7,675.94", "+0.69%", a pager's "1") and a line that
   repeats an earlier line of the same page (a headline shown twice, a sidebar list rendered twice) are removed; a
   repeat within a page is never new information.
5. An article whose HTML is stored (`raw/pages/index.jsonl` maps the URL to the file) is read by the trafilatura
   extractor (favour recall), which drops navigation, related-story cards, author boxes and comments by the page's
   structure; the extractor truncates some articles (Yahoo, Fool: the tail with the figures), so every line of the
   rule-cleaned page text of RE_ADD_LINE characters or more with end punctuation that the extractor left out is
   kept in page order. Measured on 30 audited pages: rules alone keep 98.5% of body and 22% junk;
   the extractor alone 87% / 7%; the union 94% / 14%. A long "forward-looking statements" paragraph and a
   "Read also" link are removed on article pages.
6. A page with no body: an article left with fewer than BODY_LINES lines of BODY_LINE characters or more is not fed
   (`feed = 0`, `coverage = 'none'`): a paywall shell, a listing, a page whose text repeats other pages.

Convention (D351): a frozen window is kept twice, `<name>.page.sqlite` (whole pages, as fetched) and `<name>.sqlite` (cleaned,
the one every script reads by default). `freeze_window.sh` runs the whole chain.

Usage: python3 poc/corpus/scripts/clean_pages.py --in poc/data/<name>.page.sqlite --out poc/data/<name>.sqlite
"""
import argparse
import collections
import json
import os
import re
import shutil
import sqlite3
import sys

import trafilatura   # article extraction from the stored HTML; a measured need, see the census (line rules alone leave 22% junk)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

RE_ADD_LINE = 120
FORWARD_LOOKING = re.compile(r'forward-looking statements', re.I)

TEMPLATE_PAGES = 3
SHORT_LINE = 40
BODY_LINE = 120
BODY_LINES = 3
END_PUNCTUATION = re.compile(r'[.!?:"”’)\]]$')
DIGIT = re.compile(r'\d')
LETTER = re.compile(r'[^\W\d_]')
RUN_LINE = 110
RUN_LENGTH = 3
BYLINE = re.compile(r"^By [A-Z][\w.'’-]*(?:[ ,|&]+(?:[A-Z][\w.'’-]*|and|the|of|for|de|van|von))*(?:\s*[–|•-].{0,60})?$")
BOILERPLATE = re.compile(r"(you agree to|you consent to|terms (?:of use|of service|& conditions|and conditions)|privacy policy|cookie policy"
                         r"|we use cookies|all rights reserved|may not be published, broadcast|©\s*\d{4}|copyright ©|unsubscribe|sign up for"
                         r"|subscribe to our|by subscribing|by submitting|by signing up|newsletter|getty images|image credit|photo by |credit: "
                         r"|click here|log in to|sign in with|follow us on|share this|read more:|has positions in|stock advisor returns"
                         r"|disclosure policy|content policy|add us on google|preferred source on google|powered by quotemedia"
                         r"|do not sell my personal|accept all|^advertisement$|\d+ min read$|\d+ (?:hours?|minutes?|days?) ago$|^search for:"
                         r"|^tags:$|^categories:$|^\d+ comments?$|^link copied|^loading\.\.\.$|premium support|mastodon instance|more ways to reach us"
                         r"|stock advisor|10 best stocks|view all posts by|ad-free browsing|requires javascript|save my name, email|^share:$|^x \(twitter\)$"
                         r"|markets close in|\[email protected\]|^(?:also read|read also|read next|don't miss|see also|related)\b)", re.I)
MONTH = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?'
DATELINE = re.compile(r'^(?:(?:Published|Updated|Posted|Last updated)\b.{0,70}(?:\d{4}|\d{1,2}:\d{2}| ago).{0,12}'
                      rf'|{MONTH} \d{{1,2}},? \d{{4}}(?: .{{0,40}})?|\d{{1,2}} {MONTH} \d{{4}}|\d{{4}}-\d{{2}}-\d{{2}})$')


def lines_of(text):
    return [line.strip() for line in (text or '').split('\n') if line.strip()]


def template_lines(rows):
    """publisher -> the lines that appear in TEMPLATE_PAGES or more of its pages."""
    pages = collections.defaultdict(collections.Counter)
    for row in rows:
        if row.get('copy_of') not in (None, '', 'None'):
            continue                                      # a copy repeats its original's lines; dispatch merges it
        for line in set(lines_of(row['text'])):
            pages[row['publisher']][line] += 1
    return {publisher: {line for line, n in counter.items() if n >= TEMPLATE_PAGES} for publisher, counter in pages.items()}


def is_fragment(line):
    return len(line) < SHORT_LINE and not DIGIT.search(line) and not END_PUNCTUATION.search(line)


def is_byline(line):
    return bool(BYLINE.match(line))


def is_boilerplate(line):
    return len(line) < 400 and (BOILERPLATE.search(line) is not None or DATELINE.match(line) is not None)


def without_headline_runs(lines):
    """Remove the digit-free members of every run of RUN_LENGTH or more consecutive short unpunctuated lines."""
    kept, run = [], []
    def flush():
        if len(run) >= RUN_LENGTH:
            kept.extend(line for line in run if DIGIT.search(line))
        else:
            kept.extend(run)
        run.clear()
    for line in lines:
        if len(line) <= RUN_LINE and not END_PUNCTUATION.search(line) and not is_byline(line):
            run.append(line)
        else:
            flush()
            kept.append(line)
    flush()
    return kept


def clean_lines(lines, template, article):
    """A byline is read before the rules: "By" on its own line takes the name from the next line, and a byline is
    never a template line (a prolific author's name repeats across pages) nor a fragment."""
    kept, seen, index = [], set(), 0
    stripped = [line.strip() for line in lines]
    while index < len(stripped):
        line = stripped[index]
        index += 1
        if article and line == 'By' and index < len(stripped) and stripped[index]:
            line = 'By ' + stripped[index]
            index += 1
        if not line:
            continue
        byline = article and is_byline(line)
        if line in template and not byline:
            continue
        if article and is_fragment(line) and not byline:
            continue
        if article and (not LETTER.search(line) or line in seen or is_boilerplate(line)):
            continue
        if article and len(line) >= 300 and FORWARD_LOOKING.search(line):
            continue
        seen.add(line)
        kept.append(line)
    return without_headline_runs(kept) if article else kept


def extract_article(html):
    """The article's own text by page structure, favouring recall; '' when the extractor finds no article."""
    document = trafilatura.bare_extraction(html, include_comments=False, include_tables=True, favor_recall=True)
    if document is None:
        return ''
    text = document.get('text') if isinstance(document, dict) else getattr(document, 'text', '')
    return text or ''


def _letters(text):
    return re.sub(r'[^a-z0-9]+', '', text.lower())


def clean_article(page_lines, html, template):
    """The rule-cleaned page lines, in page order, filtered by the extractor: a line stays when the extractor's text
    contains it, when it is a byline, or when it is a prose line of RE_ADD_LINE characters or more with end punctuation
    (the extractor truncates some articles; such a line is kept even when the extractor left it out)."""
    rule_lines = clean_lines(page_lines, template, article=True)
    extracted = extract_article(html) if html else ''
    if not extracted.strip():
        return rule_lines
    joined = _letters(extracted)
    short = {_letters(line) for line in extracted.split('\n')}
    kept = []
    for line in rule_lines:
        key = _letters(line)
        in_extract = key[:120] in joined if len(key) >= 20 else key in short
        if in_extract or is_byline(line) or (len(line) >= RE_ADD_LINE and END_PUNCTUATION.search(line)):
            kept.append(line)
    return kept


def pages_index(raw_root):
    """url -> stored HTML path, from the fetch index (both the stored and the cleaned form of each URL)."""
    index, mapping = os.path.join(raw_root, 'pages', 'index.jsonl'), {}
    if not os.path.exists(index):
        return mapping
    for line in open(index, encoding='utf-8'):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get('file') and record.get('url'):
            path = os.path.join(raw_root, 'pages', record['file'] + '.html')
            mapping[record['url']] = path
            mapping[common.clean_resolved_url(record['url'].strip())] = path
    return mapping


def html_of(row, index):
    uri = row.get('source_uri') or ''
    path = index.get(uri) or index.get(common.clean_resolved_url(uri))
    if path and os.path.exists(path):
        with open(path, 'rb') as handle:
            return handle.read().decode('utf-8', 'replace')
    return ''


def has_body(lines):
    return sum(1 for line in lines if len(line) >= BODY_LINE) >= BODY_LINES


def clean_database(source, destination, raw_root=None):
    """Copy the database, clean every page in place in the copy, keep the page in `text_page` and the counts in
    `cleaning`; return the census."""
    if os.path.exists(destination):
        raise FileExistsError(f'{destination} exists; new stored data gets a new name')
    shutil.copyfile(source, destination)
    conn = sqlite3.connect(destination)
    conn.row_factory = sqlite3.Row
    columns = {r[1] for r in conn.execute('pragma table_info(items)')}
    for column in ('text_page', 'cleaning'):
        if column not in columns:
            conn.execute(f'alter table items add column {column} text')
    rows = [dict(r) for r in conn.execute('select * from items')]
    template = template_lines(rows)
    index = pages_index(raw_root if raw_root is not None else common.RAW)
    census = {'pages': len(rows), 'changed': 0, 'unfed': 0, 'extracted': 0, 'chars_before': 0, 'chars_after': 0,
              'template_removed': 0, 'fragments_removed': 0, 'by_category': collections.defaultdict(lambda: {'pages': 0, 'chars_before': 0, 'chars_after': 0, 'unfed': 0}),
              'unfed_examples': []}
    for row in rows:
        lines = lines_of(row['text'])
        article = row.get('document_format') == 'article'
        publisher_template = template.get(row['publisher'], set())
        html = html_of(row, index) if article and row.get('feed') == 1 else ''   # only fed pages are read; the rest get the line rules
        kept = clean_article(lines, html, publisher_template) if article else clean_lines(lines, publisher_template, article)
        removed_template = sum(1 for line in lines if line in publisher_template)
        removed_fragments = len(lines) - len(kept) - removed_template
        text = '\n'.join(kept)
        feed, coverage = row.get('feed'), row.get('coverage')
        if article and feed == 1 and not has_body(kept):
            feed, coverage = 0, 'none'
            census['unfed'] += 1
            if len(census['unfed_examples']) < 40:
                census['unfed_examples'].append((row.get('publisher'), row.get('category'), (row.get('title') or '')[:70], len(lines), len(kept)))
        cleaning = {'lines_before': len(lines), 'lines_after': len(kept), 'chars_before': len(row['text'] or ''), 'chars_after': len(text),
                    'template_removed': removed_template, 'fragments_removed': max(0, removed_fragments), 'extractor': bool(html),
                    'unfed': feed == 0 and row.get('feed') == 1}
        conn.execute('update items set text=?, text_chars=?, text_page=?, cleaning=?, feed=?, coverage=? where input_id=?',
                     (text, len(text), row['text'], json.dumps(cleaning), feed, coverage, row['input_id']))
        census['changed'] += text != (row['text'] or '')
        census['extracted'] += bool(html)
        census['chars_before'] += cleaning['chars_before']; census['chars_after'] += cleaning['chars_after']
        census['template_removed'] += removed_template; census['fragments_removed'] += removed_fragments
        cat = census['by_category'][row.get('category')]
        cat['pages'] += 1; cat['chars_before'] += cleaning['chars_before']; cat['chars_after'] += cleaning['chars_after']; cat['unfed'] += cleaning['unfed']
    conn.commit()
    conn.close()
    census['by_category'] = dict(census['by_category'])
    return census


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--in', dest='source', required=True)
    parser.add_argument('--out', dest='destination', required=True)
    parser.add_argument('--raw', dest='raw_root', default=None, help='corpus raw root with pages/index.jsonl (default: common.RAW)')
    args = parser.parse_args()
    census = clean_database(args.source, args.destination, args.raw_root)
    print(json.dumps({k: v for k, v in census.items() if k != 'unfed_examples'}, ensure_ascii=False, indent=1))
    for example in census['unfed_examples']:
        print('unfed:', example)


if __name__ == '__main__':
    main()
