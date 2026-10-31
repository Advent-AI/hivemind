"""Blind field-reading packets for the record-field class (handoff plan T1, step 3): a fresh seeded sample of articles no
reader has read and no arm was tuned on (not the 24 of quality-2026-10-30, not the 17 of the small sample), each with the
article as the model saw it and the kept output of draw 1 of two versions of one simultaneous run (production sends each
article once), under letters shuffled per article. The letter key is written to a separate file the reader is told not to
open. event_time is left out: no step reads it.

    python3 build_packets.py S v51 v52
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_RESEARCH = HERE.parents[1]
sys.path.insert(0, str(ROOT_RESEARCH))
import score_gold as sg  # noqa: E402

FIELDS = ('id', 'quote', 'one_line', 'speaker', 'original_who', 'original_day', 'tier')
SMALL = ['gnews:085b1e1a1543437edb9756d6', 'gnews:2957e5c79a365952140c8cce', 'gnews:c6445931955f107b551cce85', 'gnews:c2924b0380602940d68de7ff',
         'gnews:1eeceeb212a2c82c2e75e806', 'gnews:c3e020d179ab025bf3ba56b0', 'gnews:022516991251df7f1af4d7cb', 'gnews:9e0d5b0d6b3e603c60340128',
         'gnews:31e1a1a229667bbb0eeb4518', 'gnews:2a41a34c16f5280b624481fb', 'gnews:aad624be9de524b95e766c96', 'gnews:784c556d2e58ed09dd8aa7fc',
         'gnews:d1a7a7f18dce5c8ae5e4d0ae', 'gnews:f0d529209a91c7a237e117f1', 'gnews:bf158d067256a39f02f7c7ce',
         'nvblog:nvidia-unlocks-ai-compute-at-scale-capital-partners-to-power-ai-infrastructure-buildout',
         'edgar:NVDA:0001045810-26-000060:nvda-20260628.htm']


def main(prefix, control, arm):
    dev = [a['input_id'] for a in json.load(open(ROOT_RESEARCH / 'golden-v3/golden-v3-signed.json'))['articles']]
    test = [a['input_id'] for a in json.load(open(ROOT_RESEARCH / 'test-set/golden-test-signed.json'))['articles']]
    read_before = set(json.load(open(ROOT_RESEARCH / 'quality-2026-10-30/sample.json')))
    excluded = read_before | set(SMALL)
    rng = random.Random(20261101)
    picked = rng.sample([i for i in dev if i not in excluded], 19) + rng.sample([i for i in test if i not in excluded], 5)
    runs = {v: sg.answers(f'{prefix}-{v}-d1') for v in (control, arm)}
    config_path = str(sg.bench.hw.ROOT / 'poc/config/poc-v67.json')
    key = {}
    for iid in picked:
        item = sg.bench.build(iid, config_path)[0]
        order = [control, arm]
        rng.shuffle(order)
        answers = {}
        for letter, v in zip('AB', order):
            s = sg.kept(runs[v].get(iid), iid)
            key[iid] = {**key.get(iid, {}), letter: v}
            answers[letter] = None if s is None else [{k: e.get(k) for k in FIELDS} for e in s['evidence']]
        packet = {'input_id': iid, 'title': item.get('title'), 'publication_day': item.get('publication_day'),
                  'publisher': item.get('publisher'), 'publisher_type': item.get('publisher_type'), 'category': item.get('category'),
                  'text': item['text'], 'answers': answers}
        (HERE / 'packets' / f'{iid.replace(":", "_")}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1) + '\n')
    (HERE / 'sample.json').write_text(json.dumps(picked, indent=1) + '\n')
    (HERE / 'letter-key-do-not-open.json').write_text(json.dumps(key, indent=1) + '\n')
    print(len(picked), 'packets; overlap with excluded:', len(set(picked) & excluded))


if __name__ == '__main__':
    main(*sys.argv[1:4])
