"""Blind packet for benchmark-design.md §"Read, every time": twenty extras (stored records from gold articles that match no gold entry) and twenty
hits (records the counting aid matched to a helpful gold matter) of each arm, drawn with a fixed seed across the arm's window draws, mixed and
shuffled. Each record carries its quote and summary, the linked questions, its article paragraph and, for a hit, the gold entry it was matched to.
The arm and draw go to a key file the reader is never given.

    python3 blind_hits_extras.py <packet.json> <key.json> <arm>=<run>,<run>,<run> <arm>=<run>,<run>,<run>"""
import json
import random
import sqlite3
import sys

sys.path.insert(0, '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard')
import score_gold as sg  # noqa: E402

GOLD = '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json'
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
PER_KIND = 20


def classify(run, gold):
    conn = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
    hits, extras = [], []
    for eid, quote, one_line, input_id in conn.execute('select e.evidence_id, e.quote, e.one_line, s.input_id from evidence e join evidence_sources s using(evidence_id)'):
        article = gold.get(input_id)
        if not article:
            continue
        record = {'quote': quote, 'one_line': one_line or ''}
        links = [f'{r[0]}: {r[1]}' for r in conn.execute('select v.object_id, v.question from evidence_links l join views v using(view_id) where l.evidence_id=?', (eid,))]
        matched = [it for it in article['items'] if it['weight'] in ('core', 'supporting') and sg.same_matter(it, record)]
        entry = dict(record, input_id=input_id, linked_questions=links, _evidence=eid)
        if matched:
            hits.append(dict(entry, gold_entry=matched[0]['span']))
        elif not any(sg.same_matter(it, record) for it in article['items']) and not any(sg.same(n['span'], quote) for n in article['not_kept']):
            extras.append(entry)
    return hits, extras


def main():
    packet_path, key_path, *arms = sys.argv[1:]
    gold = {a['input_id']: a for a in json.load(open(GOLD))['articles']}
    items = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    rng = random.Random(20261106)
    chosen = []
    for argument in arms:
        arm, runs = argument.split('=', 1)
        hits, extras = [], []
        for draw, run in enumerate(runs.split(','), 1):
            h, e = classify(run, gold)
            hits += [dict(x, _source=f'{arm} d{draw}', _kind='hit') for x in h]
            extras += [dict(x, _source=f'{arm} d{draw}', _kind='extra') for x in e]
        chosen += rng.sample(hits, PER_KIND) + rng.sample(extras, PER_KIND)
    rng.shuffle(chosen)
    packet, key = [], {}
    for index, entry in enumerate(chosen, 1):
        rid = f'H{index:03d}'
        text = items.execute('select text from items where input_id=?', (entry['input_id'],)).fetchone()[0]
        position = text.find(entry['quote'][:60])
        paragraph = text[text.rfind('\n', 0, position) + 1:(text.find('\n', position + len(entry['quote'])) if text.find('\n', position + len(entry['quote'])) > 0 else len(text))][:1500] if position >= 0 else 'NOT FOUND'
        key[rid] = {'source': entry['_source'], 'kind': entry['_kind'], 'evidence_id': entry['_evidence']}
        item = {'id': rid, 'quote': entry['quote'], 'one_line': entry['one_line'], 'linked_questions': entry['linked_questions'], 'paragraph': paragraph}
        if entry['_kind'] == 'hit':
            item['gold_entry_matched'] = entry['gold_entry']
        packet.append(item)
    json.dump(packet, open(packet_path, 'w'), ensure_ascii=False, indent=1)
    json.dump(key, open(key_path, 'w'), indent=1)
    print(f'{len(packet)} records in the packet; key written apart')


if __name__ == '__main__':
    main()
