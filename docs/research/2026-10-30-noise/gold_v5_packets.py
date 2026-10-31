"""Packets for re-deriving the gold's evidence part under standard version 5 (D250): every core, supporting and optional evidence entry of
the development gold (golden-v3-signed.json) and the test gold (golden-test-signed.json), every not-kept entry whose reason cites D238,
another company or a 5.1 judgement ("按留的规则"), every Singapore entry marked not kept, and the 35 entries the blind reader of blind4/
would keep. Each carries its article's title, day, opening and the passage around it, never the gold's weight. Two orders (seeds) for two
independent readers: A in packets of 60, B in packets of 110. The key is written apart.   python3 gold_v5_packets.py"""
import json
import random
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / '2026-10-29-ledger-standard'
sys.path[:0] = [str(LEDGER)]
import score_gold as sg  # noqa: E402

ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
GOLDS = {'dev': LEDGER / 'golden-v3/golden-v3-signed.json', 'test': LEDGER / 'test-set/golden-test-signed.json'}
WINDOW, OPENING = 700, 500
disputed = {(e['input_id'], e['span']) for e in json.loads((HERE / 'key-v64.json').read_text())['disputed']}
chosen = []
for set_name, path in GOLDS.items():
    for a in json.loads(path.read_text())['articles']:
        for i in a['items']:
            chosen.append({'set': set_name, 'input_id': a['input_id'], 'list': 'items', 'span': i['span'], 'gold_weight': i['weight'],
                           'gold_reason': i.get('rule', '')})
        for n in a['not_kept']:
            row = n.get('row', '')
            if (n['weight'] == 'not_kept' and ('D238' in row or '别家公司' in row or '按留的规则' in row or '新加坡' in row)) \
                    or (a['input_id'], n['span']) in disputed:
                chosen.append({'set': set_name, 'input_id': a['input_id'], 'list': 'not_kept', 'span': n['span'], 'gold_weight': n['weight'],
                               'gold_reason': row})
titles = {a['input_id']: (a['title'], a['publication_day']) for p in GOLDS.values() for a in json.loads(p.read_text())['articles']}
db = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
texts = {iid: db.execute('select text from items where input_id=?', (iid,)).fetchone()[0] for iid in {c['input_id'] for c in chosen}}


def passage(text, span):
    at = text.find(span)
    if at < 0:
        at = text.find(span[:60])
    if at < 0:
        span_words = sg.words(span)
        at = max(range(0, max(1, len(text) - len(span)), 50), key=lambda i: len(span_words & sg.words(text[i:i + len(span) + 100])))
    start, end = max(0, at - WINDOW), min(len(text), at + len(span) + WINDOW)
    return ('…' if start else '') + text[start:end] + ('…' if end < len(text) else '')


key = {}
entries = []
for n, c in enumerate(chosen, 1):
    gid = f'G{n:03d}'
    key[gid] = c
    title, day = titles[c['input_id']]
    entries.append({'id': gid, 'article_id': c['input_id'], 'title': title, 'publication_day': day,
                    'article_opening': texts[c['input_id']][:OPENING], 'passage': passage(texts[c['input_id']], c['span']), 'statement': c['span']})
for reader, seed, size in (('A', 1, 60), ('B', 2, 110)):
    order = entries[:]
    random.Random(seed).shuffle(order)
    for p in range(-(-len(order) // size)):
        (HERE / 'gold-v5' / f'packet-{reader}{p + 1}.json').write_text(json.dumps(order[p * size:(p + 1) * size], ensure_ascii=False, indent=1))
(HERE / 'gold-v5' / 'key.json').write_text(json.dumps(key, ensure_ascii=False, indent=1))
(HERE / 'gold-v5' / 'articles.json').write_text(json.dumps({iid: {'title': titles[iid][0], 'publication_day': titles[iid][1], 'text': t}
                                                             for iid, t in texts.items()}, ensure_ascii=False, indent=1))
print(len(entries), 'entries:', sum(c['list'] == 'items' for c in chosen), 'evidence,', sum(c['list'] == 'not_kept' for c in chosen), 'not kept')
