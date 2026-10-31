"""Reader flags per version on the blind field read (raw counts, before Claude's check of every flag against the article).

    python3 aggregate.py
"""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FLAGS = ('who_ok', 'day_ok', 'tier_ok', 'one_line_ok')


def main():
    key = json.loads((HERE / 'letter-key-do-not-open.json').read_text())
    c = collections.defaultdict(collections.Counter)
    better = collections.Counter()
    rows = []
    for f in sorted((HERE / 'verdicts').glob('*.json')):
        v = json.loads(f.read_text())
        iid = v['input_id']
        for letter in 'AB':
            version = key[iid][letter]
            for s in v.get(letter) or []:
                c[version]['records'] += 1
                c[version]['worth ' + s['worth']] += 1
                bad = [k for k in FLAGS if s.get(k) is False]
                for k in bad:
                    c[version][k.replace('_ok', '') + ' flagged'] += 1
                if any(k in bad for k in ('who_ok', 'day_ok', 'tier_ok')):
                    c[version]['records with a who/day/tier flag'] += 1
                if s.get('duplicate_of'):
                    c[version]['duplicate flagged'] += 1
                rows.append({'article': iid, 'version': version, 'letter': letter, 'id': s['id'], 'flags': bad + (['dup'] if s.get('duplicate_of') else []),
                             'notes': {k: s.get(k) for k in ('who_note', 'day_note', 'tier_note', 'one_line_problem') if s.get(k)}})
        better[key[iid].get(v.get('fields_better'), 'same')] += 1
    versions = sorted(c)
    print('verdicts', len(list((HERE / 'verdicts').glob('*.json'))))
    for k in sorted({k for x in c.values() for k in x}):
        print(k.ljust(36) + ''.join(str(c[v][k]).rjust(8) for v in versions))
    print('fields better (reader):', dict(better))
    (HERE / 'aggregate.json').write_text(json.dumps({'counts': {v: dict(c[v]) for v in versions}, 'better': dict(better), 'rows': rows}, ensure_ascii=False, indent=1) + '\n')


if __name__ == '__main__':
    main()
