"""List every not-kept gold entry (development gold) that a version keeps in at least one draw of a full run, with the draws that keep
it in each version named and the kept statements that match it (score_gold.same, the scorer's own sentence match), grouped by the
gold's not-kept row.   python3 kept_rejected.py Y3 v63 v53   (first version: the one whose kept entries are listed)"""
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / '2026-10-29-ledger-standard'
sys.path[:0] = [str(LEDGER), str(LEDGER / 'final-2026-10-30')]
import final_scores as fs  # noqa: E402
import score_gold as sg  # noqa: E402


def row_class(row):
    """The not-kept row's name without its section prefix and parenthetical gloss, for grouping."""
    name = re.sub(r'^(§5\.3|D\d+ 第 \d+ 条：|§5\.3 后两条之一：)\s*', '', row or '')
    return re.split(r'[（(]', name)[0].strip()


prefix, listed_version, other_versions = sys.argv[1], sys.argv[2], sys.argv[3:]
articles = json.loads(Path(fs.GOLDS['dev']).read_text())['articles']
sifted = {v: [{a['input_id']: sg.kept(run.get(a['input_id']), a['input_id']) for a in articles}
              for run in (sg.answers(f'{prefix}-{v}-d{d}') for d in (1, 2, 3))] for v in [listed_version] + other_versions}
entries = []
for a in articles:
    iid = a['input_id']
    for n in a['not_kept']:
        if n['weight'] != 'not_kept':
            continue
        draws, matched = {}, []
        for v in [listed_version] + other_versions:
            draws[v] = []
            for d, run in enumerate(sifted[v], 1):
                s = run.get(iid)
                hits = [e for e in (s or {}).get('evidence', []) if sg.same(n['span'], e['quote'])]
                if hits:
                    draws[v].append(d)
                    if v == listed_version:
                        matched += [{'draw': d, 'quote': e['quote'], 'one_line': e.get('one_line'), 'kind': e.get('kind'),
                                     'tier': e.get('tier'), 'speaker': e.get('speaker')} for e in hits]
        if draws[listed_version]:
            entries.append({'input_id': iid, 'title': a['title'], 'publication_day': a['publication_day'], 'span': n['span'],
                            'row': n.get('row', ''), 'row_class': row_class(n.get('row', '')), 'draws': draws, 'kept_as': matched})
out = HERE / f'kept-rejected-{prefix}-{listed_version}.json'
out.write_text(json.dumps(entries, ensure_ascii=False, indent=1))
by_class = collections.defaultdict(lambda: [0, 0, 0])
for e in entries:
    c = by_class[e['row_class']]
    c[0] += 1
    c[1] += len(e['draws'][listed_version])
    c[2] += sum(len(e['draws'][v]) for v in other_versions)
print(f'{len(entries)} entries kept in >=1 draw by {listed_version}; draws kept {sum(len(e["draws"][listed_version]) for e in entries)} '
      f'(per draw {sum(len(e["draws"][listed_version]) for e in entries) / 3:.1f}); by draws: '
      f'{collections.Counter(len(e["draws"][listed_version]) for e in entries)}')
print(f'{"entries":>7} {listed_version + " draws":>9} {"/".join(other_versions) + " draws":>9}  row')
for k, (n_entries, own, other) in sorted(by_class.items(), key=lambda kv: -kv[1][1]):
    print(f'{n_entries:>7} {own:>9} {other:>9}  {k}')
print('wrote', out)
