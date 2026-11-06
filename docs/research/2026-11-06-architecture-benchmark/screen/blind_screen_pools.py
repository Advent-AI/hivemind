"""Blind packets for condition 3 of the screen (results-reading.md §4): from each pool (R1–R3, C1–C3, C4–C6, P1–P3), twenty unmatched additions
(filed statements matching no gold entry) and twenty links (a filed statement with one of the open questions it is linked to), drawn with seed
20261107; a pool with fewer is read whole. Mixed and shuffled; the pool goes to a key file the reader is never given. A link to a question the
production extraction proposed itself (a candidate id) is not sampled: its question text is not part of the stored answer.

    PYTHONPATH=src python3 blind_screen_pools.py <packet.json> <key.json>"""
import json
import random
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BENCH = HERE.parent
sys.path.insert(0, '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard')
import score_gold as sg  # noqa: E402

GOLDS = ['/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json',
         '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-test.json']
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
POOLS = {'R': ['R1', 'R2', 'R3'], 'C13': ['C1', 'C2', 'C3'], 'C46': ['C4', 'C5', 'C6'], 'P': ['P1', 'P2', 'P3']}
PER = 20


def questions(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    return {r[0]: f'{r[1]}: {r[2]}' for r in conn.execute('select view_id, object_id, question from views')}


def main():
    packet_path, key_path = sys.argv[1:]
    data = json.loads((HERE / 'sends.json').read_text())
    golds = {a['input_id']: a for g in GOLDS for a in json.load(open(g))['articles']}
    texts = {}
    items = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    q_split_dev, q_control_dev = questions(BENCH / 'runs/split-v3-d1/views.sqlite'), questions(BENCH / 'runs/control-v108-d1/views.sqlite')
    q_fixture = questions(BENCH / 'fixture/views.sqlite')
    rng = random.Random(20261107)
    chosen = []
    for pool, sends in POOLS.items():
        additions, links = [], []
        for name in sends:
            for input_id, entry in data['sends'][name].items():
                a = golds[input_id]
                lookup = q_fixture if entry['part'] == 'test' else (q_control_dev if pool == 'P' else q_split_dev)
                for r in entry['filed']:
                    if not any(sg.same_matter(it, r) for it in a['items']) and not any(sg.same(n['span'], r['quote']) for n in a['not_kept']):
                        additions.append({'kind': 'addition', 'input_id': input_id, 'quote': r['quote'], 'one_line': r['one_line'], '_pool': pool, '_send': name})
                    for link in r['links']:
                        if link in lookup:
                            links.append({'kind': 'link', 'input_id': input_id, 'quote': r['quote'], 'one_line': r['one_line'], 'question': lookup[link],
                                          '_pool': pool, '_send': name})
        chosen += rng.sample(additions, min(PER, len(additions))) + rng.sample(links, min(PER, len(links)))
        print(f'pool {pool}: additions {len(additions)}, links {len(links)}')
    rng.shuffle(chosen)
    packet, key = [], {}
    for index, entry in enumerate(chosen, 1):
        rid = f'S{index:03d}'
        if entry['input_id'] not in texts:
            texts[entry['input_id']] = items.execute('select title, text from items where input_id=?', (entry['input_id'],)).fetchone()
        title, text = texts[entry['input_id']]
        position = text.find(entry['quote'][:60])
        end = text.find('\n', position + len(entry['quote'])) if position >= 0 else -1
        paragraph = text[text.rfind('\n', 0, position) + 1:end if end > 0 else len(text)][:1500] if position >= 0 else 'NOT FOUND'
        key[rid] = {'pool': entry['_pool'], 'send': entry['_send'], 'kind': entry['kind'], 'input_id': entry['input_id']}
        item = {'id': rid, 'kind': entry['kind'], 'title': title, 'quote': entry['quote'], 'summary': entry['one_line'], 'paragraph': paragraph}
        if entry['kind'] == 'link':
            item['linked_question'] = entry['question']
        packet.append(item)
    json.dump(packet, open(packet_path, 'w'), ensure_ascii=False, indent=1)
    json.dump(key, open(key_path, 'w'), indent=1)
    print(f'{len(packet)} entries in the packet; key written apart')


if __name__ == '__main__':
    main()
