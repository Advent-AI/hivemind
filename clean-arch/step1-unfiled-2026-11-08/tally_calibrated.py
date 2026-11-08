"""Calibrated tally of a probe review (no model calls): items both readers agree on keep their verdict; disagreements take the two
adjudicators' verdict when they agree, otherwise the majority of the four readings, otherwise 'unresolved'. Per arm: new theses
judged small or duplicate, unfiled items that should have been filed (existing or should_open), and which reader's threshold the
adjudication sided with.

Usage: tally_calibrated.py <review folder> <key.json>"""
import collections, glob, json, sys
from pathlib import Path


def readings(folder, reader):
    out = {}
    for path in sorted(glob.glob(str(folder / f'reader-answer-{reader}-*.json'))):
        for entry in json.loads(Path(path).read_text()):
            for label, v in entry['answers'].items():
                out[f"{entry['case']}/{label}"] = v
    return out


def main():
    folder, key = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
    a, b = readings(folder, 'RA'), readings(folder, 'RB')
    items = json.loads((folder / 'disagreements.json').read_text())
    c1 = {r['id']: r['verdict'] for r in json.loads((folder / 'adjudication-C1.json').read_text())}
    c2 = {r['id']: r['verdict'] for r in json.loads((folder / 'adjudication-C2.json').read_text())}
    final, sided = {}, collections.Counter()
    for n, (kind, label, ref, va, vb) in enumerate(items, 1):
        x = f'X{n}'
        if c1.get(x) == c2.get(x):
            verdict = c1[x]
        else:
            votes = collections.Counter([va, vb, c1.get(x), c2.get(x)]).most_common()
            verdict = votes[0][0] if votes[0][1] > (votes[1][1] if len(votes) > 1 else 0) else 'unresolved'
        final[(kind, label, ref)] = verdict
        sided['with reader A (Codex)' if verdict == va else 'with reader B (Claude)' if verdict == vb else 'neither or unresolved'] += 1
    print('adjudication sided:', dict(sided), '| adjudicators agree on', sum(c1.get(f'X{n}') == c2.get(f'X{n}') for n in range(1, len(items) + 1)), 'of', len(items))
    table = collections.defaultdict(collections.Counter)
    for label, va in a.items():
        arm = key[label]['arm']
        vb = b.get(label, {})
        tb = {t['local_id']: t['verdict'] for t in vb.get('new_theses', [])}
        ub = {u['index']: u['verdict'] for u in vb.get('unfiled', [])}
        for t in va.get('new_theses', []):
            v = t['verdict'] if tb.get(t['local_id']) == t['verdict'] else final.get(('thesis', label, t['local_id']), 'unresolved')
            table[arm][f'thesis {v}'] += 1
        for u in va.get('unfiled', []):
            v = u['verdict'] if ub.get(u['index']) == u['verdict'] else final.get(('unfiled', label, u['index']), 'unresolved')
            table[arm][f'unfiled {v}'] += 1
        table[arm]['answers'] += 1
    cols = ['answers', 'thesis bet', 'thesis small', 'thesis duplicate', 'thesis unresolved', 'unfiled fine', 'unfiled existing', 'unfiled should_open', 'unfiled unresolved']
    print('calibrated: ' + ' | '.join(cols))
    for arm in [x for x in ['k6b', 'u1', 'u3', 'u1u3', 'u1k', 'u1ku3'] if x in table]:
        t = table[arm]
        print(f'  {arm:6s} ' + '  '.join(f'{t[c]:>4d}' for c in cols) + f"   | should-be-filed {t['unfiled existing'] + t['unfiled should_open']}, small+dup {t['thesis small'] + t['thesis duplicate']}")


if __name__ == '__main__':
    main()
