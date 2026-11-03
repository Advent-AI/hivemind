"""$0 census on stored draws: every ledger piece from a gold article, matched to the gold's kept items and not_kept spans; the noise
grouped by the standard's row, by the item's source category and by the question it is filed under; double-hits (a quote that also
carries a kept matter) counted apart. Usage: python3 noise_by_row_category.py <arm folder> [more arm folders]; reads d1..d3 of each."""
import collections
import glob
import json
import os
import re
import sqlite3
import sys

ROOT = '/Users/lchingen/hivemind-extraction-quality-2026-10-28'
GOLD = os.path.join(ROOT, 'docs/research/2026-10-29-ledger-standard/golden-v5')


def norm(text):
    text = (text or '').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    text = text.replace('‑', '-').replace('–', '-').replace('—', '-').replace(' ', ' ')
    return re.sub(r'\s+', ' ', text).strip().lower()


def spans_of(item):
    out = []
    for key in ('span', 'quote', 'source_span'):
        if isinstance(item.get(key), str):
            out.append(item[key])
    for key in ('spans', 'quotes'):
        if isinstance(item.get(key), list):
            out.extend(s for s in item[key] if isinstance(s, str))
    return [norm(s) for s in out if len(norm(s)) >= 20]


def hit(quote, span):
    return span in quote or quote in span


gold = {}
for name in ('golden-v5-dev.json', 'golden-v5-test.json'):
    for article in json.load(open(os.path.join(GOLD, name)))['articles']:
        kept = [(spans_of(i), i.get('weight', '?')) for i in article.get('items', [])]
        noise = [(spans_of(n), n.get('row', '?')) for n in article.get('not_kept', [])]
        gold[article['input_id']] = {'kept': kept, 'noise': noise, 'title': article.get('title', '')}

if gold:
    sample = next(iter(gold.values()))
    print('gold articles', len(gold), '| first article kept items', len(sample['kept']), 'not_kept', len(sample['noise']))
    first = json.load(open(os.path.join(GOLD, 'golden-v5-dev.json')))['articles'][0]
    print('item keys:', list(first['items'][0].keys()) if first.get('items') else None)


def census(ledger):
    conn = sqlite3.connect(f'file:{ledger}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    counts = collections.Counter()
    by_row, by_cat, by_view, double_by_row = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    kept_by_cat = collections.Counter()
    samples = collections.defaultdict(list)
    pieces = 0
    for e in conn.execute('select evidence_id, quote from evidence'):
        src = conn.execute('select input_id, category from evidence_sources where evidence_id=? order by id limit 1', (e['evidence_id'],)).fetchone()
        if not src or src['input_id'] not in gold:
            continue
        pieces += 1
        q = norm(e['quote'])
        g = gold[src['input_id']]
        kept_hit = [w for spans, w in g['kept'] if any(hit(q, s) for s in spans)]
        noise_hit = [r for spans, r in g['noise'] if any(hit(q, s) for s in spans)]
        views = [r['view_id'] for r in conn.execute('select view_id from evidence_links where evidence_id=? order by id', (e['evidence_id'],))]
        cat = src['category'] or '?'
        if kept_hit:
            counts['kept'] += 1
            kept_by_cat[cat] += 1
        if noise_hit and not kept_hit:
            counts['noise'] += 1
            row = noise_hit[0][:30]
            by_row[row] += 1
            by_cat[cat] += 1
            by_view[views[0] if views else '-'] += 1
            samples[row].append((cat, views[0] if views else '-', e['quote'][:110]))
        elif noise_hit and kept_hit:
            counts['double'] += 1
            double_by_row[noise_hit[0][:30]] += 1
        elif not kept_hit:
            counts['unlisted'] += 1
    return pieces, counts, by_row, by_cat, by_view, double_by_row, kept_by_cat, samples


for arm in sys.argv[1:]:
    ledgers = sorted(glob.glob(os.path.join(arm, 'd*', 'views.sqlite')))
    print(f'\n##### {arm}: {len(ledgers)} draws')
    tot_row, tot_cat, tot_view, tot_double, tot_kept_cat = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    all_samples = collections.defaultdict(list)
    for ledger in ledgers:
        pieces, counts, by_row, by_cat, by_view, double_by_row, kept_by_cat, samples = census(ledger)
        print(f'{os.path.basename(os.path.dirname(ledger))}: gold-article pieces {pieces} | kept {counts["kept"]} | noise {counts["noise"]} | double (noise span + kept span in one quote) {counts["double"]} | unlisted {counts["unlisted"]}')
        tot_row.update(by_row); tot_cat.update(by_cat); tot_view.update(by_view); tot_double.update(double_by_row); tot_kept_cat.update(kept_by_cat)
        for k, v in samples.items():
            all_samples[k].extend(v)
    n = max(len(ledgers), 1)
    print('\nnoise by standard row (sum over draws):')
    for row, c in tot_row.most_common():
        print(f'  {c:4d}  {row}   (+{tot_double[row]} double)')
    print('\nnoise by source category (sum over draws) against kept pieces by category:')
    for cat in sorted(set(tot_cat) | set(tot_kept_cat)):
        print(f'  {cat:4s} noise {tot_cat[cat]:4d}  kept {tot_kept_cat[cat]:4d}')
    print('\nnoise by first question filed under (sum over draws):')
    for v, c in tot_view.most_common(8):
        print(f'  {v:5s} {c}')
    print('\nsamples of the three largest rows (category | question | quote):')
    for row, _ in tot_row.most_common(3):
        print(f' [{row}]')
        for cat, v, quote in all_samples[row][:7]:
            print(f'    {cat} | {v} | {quote}')
