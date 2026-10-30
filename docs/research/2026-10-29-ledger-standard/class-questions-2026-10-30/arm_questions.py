"""Question counts for a class arm on the must-not product questions (D245): per version and draw, the questions opened on the
small-product articles (the gold lists no question to open there) and, on the articles whose gold holds a main-product question,
whether a must-open or may-open question of the same opens_as was raised (final_scores.matches). Counts are leads; every
question listed is read.

    python3 arm_questions.py PREFIX DRAWS v42 v51 ...
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'final-2026-10-30'))
import final_scores as fs  # noqa: E402

sg = fs.sg
SMALL = ['gnews:2c6a829280cba26d8c8adf60', 'nvblog:geforce-now-thursday-toronto-expansion', 'gnews:cafa45974d83b062f52155e9',
         'gnews:9026c944c63575a080ce7ba9', 'gnews:c638ce9c979628354cec3fbb']


def gold():
    out = {}
    for path in fs.GOLDS.values():
        for a in json.load(open(path))['articles']:
            out[a['input_id']] = a
    return out


def main():
    prefix, draws, versions = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
    g = gold()
    guards = [i for i, a in g.items() if any(q.get('type') == 'B' for k in ('must_open', 'may_open') for q in a['questions'].get(k, []))]
    for v in versions:
        runs = [sg.answers(f'{prefix}-{v}-d{d}') for d in range(1, draws + 1)]
        small, listing = [], []
        for d, run in enumerate(runs):
            n = 0
            for iid in SMALL:
                s = sg.kept(run.get(iid), iid)
                for q in (s or {}).get('candidates', []):
                    n += 1
                    listing.append(f'   d{d + 1} {iid[:28]} {q.get("opens_as")}: {q["question"][:120]}')
            small.append(n)
        raised = {'must': [0] * draws, 'any': [0] * draws}
        guard_lines = []
        for iid in guards:
            if iid not in runs[0]:
                continue
            qs = g[iid]['questions']
            for d, run in enumerate(runs):
                s = sg.kept(run.get(iid), iid)
                cands = (s or {}).get('candidates', [])
                must = any(fs.matches(gq, q) for gq in qs.get('must_open', []) if gq.get('type') == 'B' for q in cands)
                anyb = must or any(fs.matches(gq, q) for gq in qs.get('may_open', []) if gq.get('type') == 'B' for q in cands)
                raised['must'][d] += must
                raised['any'][d] += anyb
                if not anyb:
                    guard_lines.append(f'   d{d + 1} {iid[:28]} no main-product question; opened: ' + ' | '.join(f'{q.get("opens_as")}: {q["question"][:90]}' for q in cands))
        n_must = sum(1 for i in guards if i in runs[0] and any(q.get('type') == 'B' for q in g[i]['questions'].get('must_open', [])))
        n_guard = sum(1 for i in guards if i in runs[0])
        print(f'== {v}: small-product questions per draw {small} (total {sum(small)}); main-product question raised per draw: '
              f'must-open {raised["must"]} of {n_must}, must- or may-open {raised["any"]} of {n_guard}')
        print('\n'.join(listing))
        print('\n'.join(guard_lines))


if __name__ == '__main__':
    main()
