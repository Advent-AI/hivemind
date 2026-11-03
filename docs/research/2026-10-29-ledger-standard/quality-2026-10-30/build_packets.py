"""Analyst-reading packets for the quality review of 2026-10-30 (Alex: "现在到底质量怎么样你深度的解析不要只是看尺子").
A fresh seeded random sample of the development and test articles; each packet holds the article as the model saw it and
what production keeps from one answer of role-v51 (run P, draw 1: production sends each article once). No gold is shown:
the reader judges as an analyst; the gold is compared afterwards.

    python3 build_packets.py --dev 19 --test 5
"""
import argparse
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_gold as sg  # noqa: E402

CANDIDATE_FIELDS = ('id', 'object', 'kind', 'opens_as', 'question', 'looks_at', 'measure', 'period_start', 'period_end',
                    'due_day', 'settled_by', 'evidence_ids')
EVIDENCE_FIELDS = ('id', 'quote', 'one_line', 'speaker', 'original_who', 'original_day', 'event_time', 'tier')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dev', type=int, required=True)
    ap.add_argument('--test', type=int, required=True)
    args = ap.parse_args()
    dev = json.load(open(HERE.parent / 'golden-v3/golden-v3-signed.json'))['articles']
    test = json.load(open(HERE.parent / 'test-set/golden-test-signed.json'))['articles']
    rng = random.Random(20261031)
    picked = rng.sample([a['input_id'] for a in dev], args.dev) + rng.sample([a['input_id'] for a in test], args.test)
    run = sg.answers('P-v51-d1')
    config_path = str(sg.bench.hw.ROOT / 'poc/config/poc-v67.json')
    for iid in picked:
        item = sg.bench.build(iid, config_path)[0]
        s = sg.kept(run.get(iid), iid)
        packet = {'input_id': iid, 'title': item.get('title'), 'publication_day': item.get('publication_day') or item.get('day'),
                  'publisher': item.get('publisher'), 'text': item['text'],
                  'output': None if s is None else {
                      'statements': [{k: e.get(k) for k in EVIDENCE_FIELDS} for e in s['evidence']],
                      'questions': [{k: q.get(k) for k in CANDIDATE_FIELDS} for q in s['candidates']],
                      'dropped_by_code': [list(map(str, d)) for d in s['dropped']]}}
        (HERE / 'packets' / f'{iid.replace(":", "_")}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1) + '\n')
    (HERE / 'sample.json').write_text(json.dumps(picked, indent=1) + '\n')
    print(len(picked), 'packets')


if __name__ == '__main__':
    main()
