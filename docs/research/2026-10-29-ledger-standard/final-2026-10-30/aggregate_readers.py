"""Totals of the blind reader's verdicts per version, against the signed pass line (page §9.2): core kept with the
meaning correct and no material problem in every draw; supporting kept correct or partial in at least two draws;
not-kept sentences kept; junk; statements the reader says the gold missed; questions (must-open raised every draw,
must-not opened). Also how often the code's same-matter count agrees with the reader on whether a gold item was kept.

    python3 aggregate_readers.py KEY.json
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_gold as sg  # noqa: E402


def load(path):
    text = path.read_text()
    return json.loads(text[text.find('{'):text.rfind('}') + 1])


def main():
    key = json.load(open(sys.argv[1]))
    packets = {p.stem: json.loads(p.read_text()) for p in (HERE / 'packets').glob('*.json')}
    per = collections.defaultdict(lambda: collections.defaultdict(list))   # version -> (iid, k) -> [(kept, meaning, material)]
    counts = collections.defaultdict(collections.Counter)
    must_open = collections.defaultdict(lambda: collections.defaultdict(list))
    agree = collections.Counter()
    read = 0
    for vpath in sorted((HERE / 'verdicts').glob('*.json')):
        if not vpath.stat().st_size:
            continue
        v = load(vpath)
        packet = packets[vpath.stem]
        iid = packet['input_id']
        read += 1
        items = {it['k']: it for it in packet['gold']['items']}
        for letter, ans in v['answers'].items():
            version, draw = key[iid][letter].rsplit('-d', 1)
            if not ans.get('usable', True):
                counts[version]['unusable'] += 1
                continue
            stmts = {s['id']: s for s in (packet['answers'][letter] or {}).get('statements', [])}
            for g in ans.get('gold_items', []):
                it = items.get(g['k'])
                if not it or it['weight'] not in ('core', 'supporting'):
                    continue
                kept = bool(g.get('kept_by'))
                per[version][(iid, g['k'])].append((kept, g.get('meaning'), bool(g.get('material_problems'))))
                code = any(sg.same_matter(it, s) for s in stmts.values())
                agree[(kept, code)] += 1
                if g.get('material_problems'):
                    counts[version][f'{it["weight"]} material problem'] += 1
            for s in ans.get('other_statements', []):
                counts[version][f'statement {s.get("verdict")}'] += 1
            for q in ans.get('questions', []):
                counts[version][f'question {q.get("verdict")}'] += 1
            for n, raised in enumerate(ans.get('must_open_raised', []) or []):
                must_open[version][(iid, n)].append(bool(raised))
    print(f'articles read: {read}')
    for version in sorted(per):
        core = [h for (iid, k), h in per[version].items() if next(i for i in packets.values() if i['input_id'] == iid)['gold']['items'][k]['weight'] == 'core']
        supp = [h for (iid, k), h in per[version].items() if next(i for i in packets.values() if i['input_id'] == iid)['gold']['items'][k]['weight'] == 'supporting']
        core_pass = sum(all(kept and m == 'correct' and not mat for kept, m, mat in h) and len(h) == 3 for h in core)
        core_kept_every = sum(all(kept for kept, _, _ in h) and len(h) == 3 for h in core)
        supp_pass = sum(sum(kept and m in ('correct', 'partial') for kept, m, _ in h) >= 2 for h in supp)
        meanings = collections.Counter(m for h in core for _, m, _ in h)
        mo = must_open[version]
        print(f'{version}: core pass every draw {core_pass}/{len(core)} (kept every draw {core_kept_every}; meanings {dict(meanings)}) | '
              f'supporting pass {supp_pass}/{len(supp)} | must-open raised every draw {sum(all(x) and len(x) == 3 for x in mo.values())}/{len(mo)}')
        print('     ', dict(sorted(counts[version].items())))
    print('reader kept vs code same-matter (reader, code):', dict(agree))


if __name__ == '__main__':
    main()
