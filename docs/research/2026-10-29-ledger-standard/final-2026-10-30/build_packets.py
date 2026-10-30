"""Blind reading packets for the final comparison (Alex 2026-10-30: is role-v42 the best extraction of the past two days?).
The signed page (§9.2) has meaning judged by a reader who did not write the change, against the frozen gold. One packet per
article: the article text, its gold entries, and the kept output (the production sift) of the named versions' three draws,
each answer set under a letter shuffled per article; the letter-to-draw key is written to a separate file the reader never sees.

    python3 build_packets.py --versions v29 v42 vXX --articles ids.json
"""
import argparse
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_gold as sg  # noqa: E402

CONFIG = {'v21': 'poc-v37', 'v22': 'poc-v38', 'v23': 'poc-v39', 'v29': 'poc-v45', 'v34': 'poc-v50', 'v36': 'poc-v52',
          'v42': 'poc-v58', 'v45': 'poc-v61', 'v48': 'poc-v64'}
CANDIDATE_FIELDS = ('id', 'object', 'kind', 'opens_as', 'question', 'looks_at', 'measure', 'period_start', 'period_end',
                    'due_day', 'settled_by', 'evidence_ids')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--versions', nargs='+', required=True)
    ap.add_argument('--articles', required=True)
    args = ap.parse_args()
    dev = {a['input_id']: a for a in json.load(open(HERE.parent / 'golden-v3/golden-v3-signed.json'))['articles']}
    test = {a['input_id']: a for a in json.load(open(HERE.parent / 'test-set/golden-test-signed.json'))['articles']}
    gold = {**dev, **test}
    ids = json.load(open(args.articles))
    runs = {(v, d): sg.answers(f'G-{v}-d{d}') for v in args.versions for d in (1, 2, 3)}
    key = {}
    rng = random.Random(20261030)
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for iid in ids:
        a = gold[iid]
        item = sg.bench.build(iid, str(sg.bench.hw.ROOT / f'poc/config/{CONFIG[args.versions[0]]}.json'))[0]
        draws = [(v, d) for v in args.versions for d in (1, 2, 3)]
        rng.shuffle(draws)
        answers = {}
        for letter, (v, d) in zip(letters, draws):
            s = sg.kept(runs[(v, d)].get(iid), iid)
            key.setdefault(iid, {})[letter] = f'{v}-d{d}'
            answers[letter] = None if s is None else {
                'statements': [{'id': e['id'], 'quote': e['quote'], 'one_line': e['one_line'], 'speaker': e.get('speaker'),
                                'original_day': e.get('original_day'), 'tier': e.get('tier')} for e in s['evidence']],
                'questions': [{k: q.get(k) for k in CANDIDATE_FIELDS} for q in s['candidates']]}
        packet = {'input_id': iid, 'title': a['title'], 'publication_day': a.get('publication_day'), 'publisher': item.get('publisher'),
                  'category': item.get('category'), 'text': item['text'],
                  'gold': {'items': [{'k': k, 'weight': it['weight'], 'span': it['span'], 'meaning': it.get('meaning'), 'rule': it.get('rule')}
                                     for k, it in enumerate(a['items'])],
                           'not_kept': [{'span': n['span'], 'weight': n['weight'], 'reason': n.get('row')} for n in a['not_kept']],
                           'questions': a.get('questions', {})},
                  'answers': answers}
        (HERE / 'packets' / f'{iid.replace(":", "_")}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1) + '\n')
    (HERE / 'letter-key.json').write_text(json.dumps(key, indent=1) + '\n')
    print(len(ids), 'packets;', len(draws), 'answer sets each')


if __name__ == '__main__':
    main()
