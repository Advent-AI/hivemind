"""Apply the current labelling rules of assemble.py to an existing items database and write a new, dated database.

The frozen database a run used is never changed (AGENTS §9: new stored data gets a new dated name). Each row is
relabelled from its own stored fields, the same way assemble.py labels it from the raw harvest:
  - official notices: publisher (the issuing agency), object_identifiers and tier (official_objects)
  - EDGAR documents: category, document_format and feed (exhibit_category, with the filing's primary document as
    the sibling row), and for peer companies the objects by category (themes only on results, reports and calls)
  - peer calls: the company object's reason
  - news pages: publisher, publisher_type and category (an aggregator's author is the byline's outlet; other
    domains re-read from the author table), coverage/feed for video pages
  - copies: copy_of recomputed over all rows with mark_copies
Prints, per rule, how many rows changed and what they became.

Usage: python3 poc/corpus/scripts/relabel.py --in poc/data/items-window.sqlite --out poc/data/items-window-tags2-2026-10-24.sqlite
"""
import argparse
import collections
import json
import os
import re
import shutil
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(__file__))
import assemble  # noqa: E402


def relabel(conn):
    rows = [dict(r) for r in conn.execute('select * from items')]
    changes = collections.defaultdict(collections.Counter)
    examples = collections.defaultdict(list)

    def note(rule, what, row):
        changes[rule][what] += 1
        examples[rule].append((row['title'] or row['input_id'])[:80])

    by_accession = collections.defaultdict(list)
    for row in rows:
        if row['channel'] == 'EDGAR':
            by_accession[row['input_id'].rsplit(':', 2)[-2]].append(row)
    for row in rows:
        extra = json.loads(row['extra'] or '{}')
        # official notices: publisher is the issuing agency; objects by source
        if row['klass'] == '官方材料':
            publisher = assemble.official_publisher(row['topic'])
            if publisher != row['publisher']:
                note('official: publisher', f'{row["publisher"]} → {publisher}', row)
                row['publisher'] = publisher
            objects = assemble.official_objects(row['topic'], row['title'])
            if json.dumps(objects) != row['object_identifiers']:
                before = [o['value'] for o in json.loads(row['object_identifiers'] or '[]')]
                note('official: object', f'{before} → {[o["value"] for o in objects]}', row)
                row['object_identifiers'] = json.dumps(objects)
                row['tier'] = 'geopolitics' if objects else 'noise'
        # EDGAR documents: category from the exhibit, with the primary document as the sibling row
        if row['channel'] == 'EDGAR':
            accession = row['input_id'].rsplit(':', 2)[-2]
            name = row['input_id'].rsplit(':', 1)[-1]
            siblings = by_accession[accession]
            is_exhibit = lambda s: (json.loads(s['extra'] or '{}').get('exhibit_type') or '').upper().startswith('EX-')   # the primary document's type is the form itself (10-Q, 8-K)
            primary = next((s for s in siblings if not is_exhibit(s)), None)
            primary_name = primary['input_id'].rsplit(':', 1)[-1] if primary else ''
            if is_exhibit(row):
                category, document_format = assemble.exhibit_category(extra.get('form') or '', name, primary_name, extra.get('exhibit_type'),
                                                                      '', extra.get('items'), primary['text'] if primary else '', row['text'])
            else:
                category, document_format = row['category'], row['document_format']   # primary documents keep their category
            if category != row['category']:
                feed = 0 if category == assemble.NOT_MATERIAL else (1 if row['coverage'] == 'full' and len(row['text'] or '') >= 200 else 0)
                note('EDGAR: exhibit category', f'{row["category"]} → {category}' + (f', feed {row["feed"]} → {feed}' if feed != row['feed'] else ''), row)
                row['category'], row['document_format'], row['feed'] = category, document_format, feed
            ticker = row['topic'].split('-', 1)[1] if row['topic'].startswith('company-') else 'NVDA'
            if ticker != 'NVDA':
                themes = (assemble.COMPANIES.get(ticker) or {}).get('themes')
                objects = assemble.objects_for_company(ticker, themes, row['category'])
                if json.dumps(objects) != row['object_identifiers']:
                    before = [o['value'] for o in json.loads(row['object_identifiers'] or '[]')]
                    note('EDGAR peers: objects by category', f'{row["category"]}: {before} → {[o["value"] for o in objects]}', row)
                    row['object_identifiers'] = json.dumps(objects)
        # peer calls: the company object's reason
        if row['channel'] == 'TrueNorth' and row['category'] == 'T4' and row['topic'].startswith('company-'):
            ticker = row['topic'].split('-', 1)[1]
            objects = assemble.objects_for_company(ticker, (assemble.COMPANIES.get(ticker) or {}).get('themes'), 'T4', 'the company speaking on its own call')
            if json.dumps(objects) != row['object_identifiers']:
                note('calls: object reason', "'filer' → 'the company speaking on its own call'", row)
                row['object_identifiers'] = json.dumps(objects)
        # news pages: author and category; video pages are not full
        if row['klass'] == '新闻':
            domain = assemble.domain_of(row['source_uri'])
            if domain in assemble.AGGREGATORS:
                publisher, kind, identified = assemble.page_author(domain, row['title'], row['text'])
                extra['author_unidentified'] = not identified
                row['extra'] = json.dumps(extra)
            else:
                publisher, kind = row['publisher'], assemble.author_type(row['publisher'])
            category = assemble.news_category(kind)
            if (publisher, kind, category) != (row['publisher'], row['publisher_type'], row['category']):
                note('news: author and category', f'{row["publisher"]} ({row["publisher_type"]}, {row["category"]}) → {publisher} ({kind}, {category})', row)
                row['publisher'], row['publisher_type'], row['category'] = publisher, kind, category
            if row['coverage'] == 'full' and assemble.VIDEO_PATH.search(assemble.__dict__['urllib'].parse.urlsplit(row['source_uri'] or '').path):
                note('news: video page', f'coverage full → video, feed {row["feed"]} → 0', row)
                row['coverage'], row['feed'] = 'video', 0
    # copies, recomputed from scratch
    before = {r['input_id']: r['copy_of'] for r in rows}
    for r in rows:
        r['copy_of'] = None
    assemble.mark_copies(rows)
    for r in rows:
        if r['copy_of'] != before[r['input_id']]:
            note('copies', f'{"was a copy" if before[r["input_id"]] else "was an original"} → {"copy of " + r["copy_of"].split(":")[0] if r["copy_of"] else "original"}', r)
    conn.executemany('update items set publisher=?, object_identifiers=?, tier=?, category=?, document_format=?, feed=?, publisher_type=?, coverage=?, extra=?, copy_of=? where input_id=?',
                     [(r['publisher'], r['object_identifiers'], r['tier'], r['category'], r['document_format'], r['feed'], r['publisher_type'], r['coverage'], r['extra'], r['copy_of'], r['input_id']) for r in rows])
    conn.commit()
    return changes, examples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in', dest='source', required=True)
    parser.add_argument('--out', dest='target', required=True)
    args = parser.parse_args()
    if os.path.exists(args.target):
        raise SystemExit(f'{args.target} exists; a relabelled database gets a new name')
    shutil.copy(args.source, args.target)
    conn = sqlite3.connect(args.target)
    conn.row_factory = sqlite3.Row
    changes, examples = relabel(conn)
    for rule, counter in changes.items():
        print(f'\n== {rule}: {sum(counter.values())} rows')
        for what, count in counter.most_common(12):
            print(f'   {count:4d}  {what}')
        for example in examples[rule][:4]:
            print(f'        e.g. {example}')
    print('\nfed rows by klass before/after:')
    src = sqlite3.connect(f'file:{args.source}?mode=ro', uri=True)
    for klass, fed in src.execute('select klass, sum(feed) from items group by 1'):
        after = conn.execute('select sum(feed) from items where klass=?', (klass,)).fetchone()[0]
        print(f'   {klass}: {fed} → {after}')
    print('written', args.target)


if __name__ == '__main__':
    main()
