"""How stable role-v51's kept statements are across the three draws of run P, by gold class: for each kept statement, in how
many draws a statement with the same quote (score_gold.same) is kept on the same article.

    python3 stability.py
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_gold as sg  # noqa: E402

DRAWS = ['P-v51-d1', 'P-v51-d2', 'P-v51-d3']


def main():
    dev = json.load(open(HERE.parent / 'golden-v3/golden-v3-signed.json'))['articles']
    test = json.load(open(HERE.parent / 'test-set/golden-test-signed.json'))['articles']
    runs = {tag: sg.answers(tag) for tag in DRAWS}
    counts = collections.defaultdict(lambda: [0, 0, 0, 0])
    for a in dev + test:
        sifted = [sg.kept(runs[tag].get(a['input_id']), a['input_id']) for tag in DRAWS]
        if any(s is None for s in sifted):
            continue
        for s in sifted:
            for e in s['evidence']:
                gold = [it for it in a['items'] if sg.same(it['span'], e['quote'])]
                rejected = [n for n in a['not_kept'] if sg.same(n['span'], e['quote'])]
                if gold:
                    cls = gold[0]['weight']
                elif rejected:
                    cls = 'optional' if all(n['weight'] != 'not_kept' for n in rejected) else 'not kept'
                else:
                    cls = 'outside the gold'
                draws = sum(1 for other in sifted if any(sg.same(e['quote'], x['quote']) or sg.same(x['quote'], e['quote']) for x in other['evidence']))
                counts[cls][draws] += 1
    out = {cls: {'statements': sum(c), 'in all three draws': round(c[3] / sum(c), 2), 'in one draw only': round(c[1] / sum(c), 2)} for cls, c in counts.items()}
    (HERE / 'stability.json').write_text(json.dumps(out, indent=1) + '\n')
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
