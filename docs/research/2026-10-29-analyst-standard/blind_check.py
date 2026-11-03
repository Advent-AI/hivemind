"""A second, blind reader for the hand labels (AGENTS §7: measure the stick). build writes a packet with no model names and no
labels: (A) every core/supporting cell labelled other than c, plus 40 random c cells, each with the reference item, the
source paragraphs it rests on and every record that draw wrote for the article; (B) 80 random unmatched records with the
article's reference items. The key (cell id -> model, draw, my label) stays in a separate file the reader is not given.
compare reads the reader's answers and prints agreement and every disagreement.

    python3 blind_check.py build OUT_DIR
    python3 blind_check.py compare OUT_DIR
"""
import json
from pathlib import Path
import random
import sqlite3
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_meaning as sm  # noqa: E402

ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
SEED = 20261029


def paragraphs(text, needles):
    paras = [p for p in text.split('\n') if p.strip()]
    hit = [i for i, p in enumerate(paras) if any(n and n[:60] in p for n in needles)]
    keep = sorted({j for i in hit for j in (i - 1, i, i + 1) if 0 <= j < len(paras)})
    return [paras[j] for j in keep] or paras[:3]


def records(structure, input_id, draw):
    rows = []
    for key, cells in structure['per_item'].items():
        if key.startswith(input_id + '|'):
            for r in cells[draw].get('records', []):
                rows.append(r)
    rows += structure['unmatched'][input_id][draw]
    seen, out = set(), []
    for r in rows:
        if r['id'] in seen:
            continue
        seen.add(r['id'])
        out.append({'id': r['id'], 'one_line': r['one_line'], 'who': r.get('original_who') or r.get('speaker', ''),
                    'day': r.get('original_day', ''), 'tier': r.get('tier', ''), 'refused': r.get('kept') is False})
    return out


def build(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=False)
    rng = random.Random(SEED)
    structure = json.loads((HERE / 'structure.json').read_text())
    db = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    cells_other, cells_c, unmatched, articles = [], [], [], {}
    for label_set in ('week', 'holdout'):
        refs = json.loads((HERE / f'reference-{label_set}.json').read_text())['articles']
        labels = sm.parse(HERE / f'labels-{label_set}.txt')
        for art in refs:
            key = str(art.get('call_id', art['input_id']))
            block = labels[key]
            text, title = db.execute('select text, title from items where input_id=?', (art['input_id'],)).fetchone()
            articles[art['input_id']] = {'title': title, 'items': [{'id': s['id'], 'weight': s['weight'], 'note': s['note']} for s in art.get('statements', [])]}
            for item in art.get('statements', []):
                if item['weight'] not in ('core', 'supporting'):
                    continue
                for d, draw in sm.DRAWS.items():
                    given = block['items'].get(item['id'], {}).get(d)
                    reassigned = any(v == '>' + item['id'] for v in block['unmatched'].get(d, {}).values())
                    state = structure['per_item'][f"{art['input_id']}|{item['id']}"][draw]['state']
                    label = given['label'] + ('!' if given['material'] else '') if given else ('-' if state == 'omitted' and not reassigned else None)
                    cell = {'input_id': art['input_id'], 'item': item, 'draw': draw, 'label': label,
                            'source': paragraphs(text, [item['span']] + item.get('also', []))}
                    (cells_c if label == 'c' else cells_other).append(cell)
            for d, draw in sm.DRAWS.items():
                named = block['unmatched'].get(d, {})
                for r in structure['unmatched'][art['input_id']][draw]:
                    kind = named.get(r['id']) or block['rest'].get(d)
                    unmatched.append({'input_id': art['input_id'], 'draw': draw, 'record': r, 'label': kind})
    sample_a = cells_other + rng.sample(cells_c, 40)
    rng.shuffle(sample_a)
    sample_b = rng.sample(unmatched, 80)
    packet = {'part_a': [], 'part_b': []}
    key = {}
    for n, cell in enumerate(sample_a, 1):
        cid = f'A{n:03d}'
        key[cid] = {'input_id': cell['input_id'], 'item': cell['item']['id'], 'draw': cell['draw'], 'label': cell['label']}
        packet['part_a'].append({'cell': cid, 'article': cell['input_id'], 'title': articles[cell['input_id']]['title'],
                                 'reference_item': {k: cell['item'][k] for k in ('id', 'weight', 'note', 'span', 'also', 'who')},
                                 'source_paragraphs': cell['source'], 'records_this_answer_wrote': records(structure, cell['input_id'], cell['draw'])})
    for n, row in enumerate(sample_b, 1):
        cid = f'B{n:03d}'
        r = row['record']
        key[cid] = {'input_id': row['input_id'], 'draw': row['draw'], 'record': r['id'], 'label': row['label']}
        packet['part_b'].append({'cell': cid, 'article': row['input_id'], 'title': articles[row['input_id']]['title'],
                                 'reference_items_of_this_article': articles[row['input_id']]['items'],
                                 'record': {'one_line': r['one_line'], 'quote': r.get('quote', ''), 'who': r.get('speaker', ''),
                                            'tier': r.get('tier', ''), 'refused_by_quote_check': r.get('kept') is False}})
    (out / 'packet.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1) + '\n')
    (out / 'key.json').write_text(json.dumps(key, ensure_ascii=False, indent=1) + '\n')
    print('part A', len(packet['part_a']), 'cells (', len(cells_other), 'not c +40 c ); part B', len(packet['part_b']), 'records')


def compare(out_dir):
    out = Path(out_dir)
    key = json.loads((out / 'key.json').read_text())
    answers = {}
    for line in (out / 'answers.jsonl').read_text().splitlines():
        if line.strip():
            row = json.loads(line)
            answers[row['cell']] = row
    groups = {'A': {'c': 'ok', 'p': 'partial', 'w': 'wrong', '-': 'absent'}, 'B': {}}
    agree = {'A': [0, 0], 'B': [0, 0]}
    for cid, k in sorted(key.items()):
        a = answers.get(cid)
        if a is None:
            print('missing answer', cid)
            continue
        mine = (k['label'] or '?').rstrip('!')
        theirs = a['label']
        if cid[0] == 'A':
            same = mine == theirs or (mine == 'c' and theirs == 'c')
        else:
            mine_kind = 'cut' if mine.startswith('>') else mine
            same = mine_kind == theirs or (mine_kind in ('o', 'j') and theirs in ('o', 'j') and False)
        agree[cid[0]][0] += same
        agree[cid[0]][1] += 1
        if not same:
            print(cid, k, '| reader:', theirs, '|', a.get('reason', '')[:300])
    print('agreement', {g: f'{v[0]}/{v[1]}' for g, v in agree.items()})


if __name__ == '__main__':
    {'build': build, 'compare': compare}[sys.argv[1]](sys.argv[2])
