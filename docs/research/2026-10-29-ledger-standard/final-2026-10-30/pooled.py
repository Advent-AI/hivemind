"""Pool the simultaneous full runs (each run: the named versions sent together, development 118 + test 30, three draws)
from the per-article files final_scores.py writes. Per version and run: core kept per draw (summed), core kept in every
draw, supporting kept in at least two draws, not-kept entries kept per draw, extras per draw, must-open raised in every
draw, and questions on the four small-product articles (feature and service release dates the gold says must not open).

    python3 pooled.py G H K M N
"""
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SMALL = ('gnews:2c6a829280cba26d8c8adf60', 'nvblog:geforce-now-thursday-toronto-expansion', 'gnews:9026c944c63575a080ce7ba9', 'gnews:cafa45974d83b062f52155e9')


def main():
    table = {}
    for run in sys.argv[1:]:
        for gold in ('dev', 'test'):
            path = HERE / f'per-article-{run}-{gold}.json'
            if not path.exists():
                continue
            rows = json.loads(path.read_text())
            for v, arts in rows.items():
                t = table.setdefault((v, gold), {})
                core = [h for r in arts.values() for h in r['core']]
                supp = [h for r in arts.values() for h in r['supp']]
                mo = [h for r in arts.values() for h in r['must_open']]
                t.setdefault('runs', []).append(run)
                t.setdefault('core kept (sum of 3 draws)', []).append(sum(sum(h) for h in core))
                t.setdefault('core every draw', []).append(sum(all(h) for h in core))
                t.setdefault('supporting >=2', []).append(sum(sum(h) >= 2 for h in supp))
                t.setdefault('not-kept kept per draw', []).append(round(sum(sum(r['nk_hits']) for r in arts.values()) / 3))
                t.setdefault('extra per draw', []).append(round(sum(sum(r['extra']) for r in arts.values()) / 3))
                t.setdefault('must-open every draw', []).append(sum(all(h) for h in mo))
                t.setdefault('small-product questions (3 draws)', []).append(sum(sum(r['questions']) for i, r in arts.items() if i in SMALL))
                t['core total'] = len(core); t['supporting total'] = len(supp); t['must-open total'] = len(mo)
    for (v, gold), t in sorted(table.items(), key=lambda x: (x[0][1], x[0][0])):
        print(f"{gold:4s} {v}: runs {t['runs']}")
        for k, vals in t.items():
            if isinstance(vals, list) and k != 'runs':
                print(f"      {k:36s} {vals}  mean {statistics.mean(vals):.1f}")
        print(f"      totals: core {t['core total']}, supporting {t['supporting total']}, must-open {t['must-open total']}")


if __name__ == '__main__':
    main()
