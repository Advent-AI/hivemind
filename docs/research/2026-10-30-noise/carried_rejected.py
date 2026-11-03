"""Split the not-kept gold entries a version keeps (final_scores.py's count: a kept statement whose quote matches the entry's span by
score_gold.same) into two kinds per draw: carried, when every statement that matches the not-kept span also matches a core, supporting
or optional gold entry of the same article (score_gold.same_matter), so the not-kept words ride inside the quote of a matter the gold
keeps; and standalone, when at least one matching statement matches no kept gold entry.   python3 carried_rejected.py Y3 v53 v63"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / '2026-10-29-ledger-standard'
sys.path[:0] = [str(LEDGER), str(LEDGER / 'final-2026-10-30')]
import final_scores as fs  # noqa: E402
import score_gold as sg  # noqa: E402

prefix, versions = sys.argv[1], sys.argv[2:]
articles = json.loads(Path(fs.GOLDS['dev']).read_text())['articles']
for version in versions:
    counts = []
    for d in (1, 2, 3):
        run = sg.answers(f'{prefix}-{version}-d{d}')
        carried = standalone = 0
        for a in articles:
            s = sg.kept(run.get(a['input_id']), a['input_id'])
            if not s:
                continue
            kept_gold = [i for i in a['items'] if i['weight'] in ('core', 'supporting', 'optional')]
            kept_gold += [n for n in a['not_kept'] if n['weight'] == 'optional']
            for n in a['not_kept']:
                if n['weight'] != 'not_kept':
                    continue
                matching = [e for e in s['evidence'] if sg.same(n['span'], e['quote'])]
                if not matching:
                    continue
                if all(any(sg.same_matter(k, e) if 'meaning' in k or k in a['items'] else sg.same(k['span'], e['quote']) for k in kept_gold) for e in matching):
                    carried += 1
                else:
                    standalone += 1
        counts.append((carried, standalone))
    print(f'{version}: per draw (carried, standalone) {counts}; mean carried {sum(c for c, _ in counts) / 3:.1f}, standalone {sum(s for _, s in counts) / 3:.1f}')
