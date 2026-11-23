"""Second dry run ($0): the readings as the test will run them.
A. Stage A, pass 1: three thesis packets of six ladders each (three "sends" from each of two arms, arm hidden), shown only as the judge
   would be shown them; common marks only.
B. Stage B: 20 stored judgements of the unseeded draw 1 replay (views v9 and v13, on the ruler's ladders), each with its request as sent
   and its answer; four carry a planted wrong rung.
Packets go into the repo without labels; the key stays beside this script until the readers have answered."""
import copy, json, random, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_dryrun as first      # the hand-written ladders of the first dry run (BASE, WRONG)

REPO = Path('/Users/lchingen/hivemind')
OUT = REPO / 'clean-arch/step4-2026-11-10/dryrun2'
rng = random.Random(20261110)


def judge_view(item):
    return item['shown']


def relabel(shown, labels):
    out = copy.deepcopy(shown)
    for r, l in zip(out['rungs'], labels):
        r['label'] = l
    return out


E, W = first.BASE, {k: v[0] for k, v in first.WRONG.items()}
# control-style ladders: the model writes labels and conditions itself, no reference suffix
c3_alt = copy.deepcopy(E['E1']['shown']); c3_alt['question'] = 'Will Vera Rubin start shipping to customers before the end of calendar 2026?'
c3_alt['rungs'][0]['condition'] = 'NVIDIA confirms Vera Rubin shipments to customers began in calendar 2026.'
c3_alt['rungs'][1]['condition'] = 'NVIDIA has not confirmed that Vera Rubin shipments to customers began in calendar 2026.'
c7_flip = relabel(E['E4']['shown'], ['Strongly bearish', 'Bearish', 'Neutral', 'Bullish', 'Strongly bullish'])
c7_text = copy.deepcopy(E['E4']['shown'])
for r, c in zip(c7_text['rungs'], ['NVIDIA reports commitments below $80 billion.', 'NVIDIA reports commitments of at least $80 billion and below $110 billion.',
                                    'NVIDIA reports commitments of at least $110 billion and below $140 billion.', 'NVIDIA reports commitments of at least $140 billion and below $180 billion.',
                                    'NVIDIA reports commitments of at least $180 billion.']):
    r['condition'] = c
c4_plain = copy.deepcopy(E['E5']['shown'])
for r in c4_plain['rungs']:
    r['condition'] = r['label']
c4_names = relabel(c4_plain, ['Lowest', 'Low', 'Middle', 'High', 'Highest'])
PACKETS_A = {
    ('u1', 'clean-3'): [('candidate', E['E1']['shown'], None), ('candidate', W['W5']['shown'], 'D'), ('candidate', E['E1']['shown'], None),
                        ('control', W['W1']['shown'], 'R'), ('control', c3_alt, None), ('control', W['W10']['shown'], 'N')],
    ('u1', 'clean-7'): [('candidate', E['E4']['shown'], None), ('candidate', W['W9']['shown'], 'G'), ('candidate', E['E4']['shown'], None),
                        ('control', c7_flip, 'F'), ('control', W['W6']['shown'], 'O'), ('control', c7_text, None)],
    ('u1', 'clean-4'): [('candidate', E['E5']['shown'], None), ('candidate', W['W7']['shown'], 'X'), ('candidate', W['W8']['shown'], 'Y'),
                        ('control', c4_plain, None), ('control', c4_names, None), ('control', W['W8']['shown'], 'Y')],
}
packet_a, key_a = [], {}
for (run, tid), ladders in PACKETS_A.items():
    t = first.thesis(run, tid)
    order = list(range(6)); rng.shuffle(order)
    shown = []
    for slot, i in enumerate(order, 1):
        arm, ladder, mark = ladders[i]
        shown.append({'ladder': f'{tid}-{slot}', 'as_the_judge_is_shown_it': ladder})
        key_a[f'{run} {tid}-{slot}'] = {'arm': arm, 'planted_mark': mark}
    packet_a.append({'thesis': t['thesis'], 'thesis_id': f'{run} {tid}', 'article': {k: t['article'][k] for k in ('publication_date', 'publisher', 'title', 'text')}, 'ladders': shown})

# ---- B: stored judgements
J = REPO / 'poc/data/clean-unseeded-2026-11-10/draw-d1/judged'
conn = sqlite3.connect(f'file:{J}/views.sqlite?mode=ro', uri=True); conn.row_factory = sqlite3.Row
arch = sqlite3.connect(f'file:{J}/archive.sqlite?mode=ro', uri=True)
packet_b, key_b = [], {}
n = 0
for view in ('v9', 'v13'):
    rungs = {r['position']: r['label'] for r in conn.execute('select position, label from rungs where view_id=? order by position', (view,))}
    rows = conn.execute('select * from judgements where view_id=? order by judgement_id', (view,)).fetchall()
    plant = set(rng.sample(range(len(rows)), 2))
    for i, row in enumerate(rows):
        n += 1
        request = json.loads(arch.execute('select request_json from model_calls where call_id=?', (row['call_id'],)).fetchone()[0])
        user = request['messages'][-1]['content'] if 'messages' in request else request['input'][-1]['content']
        rung = row['rung']
        if i in plant:
            rung = 1 if row['rung'] >= 3 else len(rungs)          # a rung at the other end of the ladder; the reasons are left as they were
        packet_b.append({'judgement': n, 'view': view, 'day': row['publication_day'], 'request_as_sent': user,
                         'answer': {'rung': rung, 'rung_label': rungs[rung], 'reference': row['reference'], 'implied_outcome': row['implied_outcome'],
                                    'reasons': row['reasons'], 'changed': bool(row['changed']), 'why_changed': row['why_changed']}})
        key_b[str(n)] = {'view': view, 'day': row['publication_day'], 'planted': i in plant, 'stored_rung': row['rung'], 'shown_rung': rung}
OUT.mkdir(exist_ok=True)
(OUT / 'packet-a.json').write_text(json.dumps(packet_a, indent=1, ensure_ascii=False))
(OUT / 'packet-b.json').write_text(json.dumps(packet_b, indent=1, ensure_ascii=False))
(HERE / 'dryrun2_key.json').write_text(json.dumps({'a': key_a, 'b': key_b}, indent=1))
print('A:', len(packet_a), 'packets,', sum(len(p['ladders']) for p in packet_a), 'ladders,', sum(1 for v in key_a.values() if v['planted_mark']), 'planted;',
      'B:', len(packet_b), 'judgements,', sum(1 for v in key_b.values() if v['planted']), 'planted;',
      (OUT / 'packet-a.json').stat().st_size, (OUT / 'packet-b.json').stat().st_size, 'bytes')
