"""Score a run against key-v64.json (sha256 checked first): on the key's articles, per version and draw, the agreed-noise entries kept
on their own (carried ones apart, as partition_rejected.py), the disputed entries kept (reported apart; they decide nothing), and the
core and supporting guards kept (score_gold.same_matter, the counting aid). Every guard one version keeps in fewer draws than the other
is listed with the gold span, to be read against the raw answers.   python3 score_v64.py Y4 v63 v64"""
import collections
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / '2026-10-29-ledger-standard'
sys.path[:0] = [str(LEDGER), str(LEDGER / 'final-2026-10-30')]
import final_scores as fs  # noqa: E402
import score_gold as sg  # noqa: E402

expected = (HERE / 'key-v64.sha256').read_text().split()[0]
actual = hashlib.sha256((HERE / 'key-v64.json').read_bytes()).hexdigest()
if actual != expected:
    sys.exit(f'key-v64.json sha256 {actual} does not match the frozen {expected}')
key = json.loads((HERE / 'key-v64.json').read_text())
print('key-v64.json sha256', actual[:8], '| gold sha256', sg.sha(fs.GOLDS['dev'])[:8])
prefix, versions = sys.argv[1], sys.argv[2:]
articles = {a['input_id']: a for a in json.loads(Path(fs.GOLDS['dev']).read_text())['articles']}
sifted = {v: [{iid: sg.kept(run.get(iid), iid) for iid in key['articles']} for run in (sg.answers(f'{prefix}-{v}-d{d}') for d in (1, 2, 3))]
          for v in versions}


def kept_draws(version, iid, span, standalone):
    """Draws in which a statement matching the not-kept span is kept; with standalone, only when it matches no kept gold entry."""
    kept_gold = [i for i in articles[iid]['items'] if i['weight'] in ('core', 'supporting', 'optional')]
    hits = []
    for s in sifted[version]:
        matching = [e for e in (s.get(iid) or {}).get('evidence', []) if sg.same(span, e['quote'])]
        own = [e for e in matching if not any(sg.same_matter(k, e) for k in kept_gold)]
        hits.append(bool(own) if standalone else bool(matching))
    return hits


for group in ('agreed_noise', 'disputed'):
    entries = [e for e in key[group] if any(n['span'] == e['span'] and n['weight'] == 'not_kept' for n in articles[e['input_id']]['not_kept'])]
    print(f'== {group} ({len(entries)} of {len(key[group])} entries still not kept in the gold given)')
    key[group] = entries
    for v in versions:
        standalone = [sum(x) for x in zip(*[kept_draws(v, e['input_id'], e['span'], True) for e in key[group]])]
        any_match = [sum(x) for x in zip(*[kept_draws(v, e['input_id'], e['span'], False) for e in key[group]])]
        print(f'   {v}: kept on its own per draw {standalone} (mean {sum(standalone) / 3:.1f}); counting carried too {any_match} (mean {sum(any_match) / 3:.1f})')
guard_hits = {v: {} for v in versions}
live_guards = [g for g in key['guards'] if any(i['span'] == g['span'] and i['weight'] == g['weight'] for i in articles[g['input_id']]['items'])]
print(f'guards the gold given still holds at the same weight: {len(live_guards)} of {len(key["guards"])} (the rest changed with the gold version and are not scored)')
key['guards'] = live_guards
for g_index, g in enumerate(key['guards']):
    item = next(i for i in articles[g['input_id']]['items'] if i['span'] == g['span'])
    for v in versions:
        guard_hits[v][g_index] = [bool(s.get(g['input_id'])) and any(sg.same_matter(item, e) for e in s[g['input_id']]['evidence']) for s in sifted[v]]
print(f'== guards ({len(key["guards"])}: {sum(g["weight"] == "core" for g in key["guards"])} core)')
for v in versions:
    for weight in ('core', 'supporting'):
        idx = [i for i, g in enumerate(key['guards']) if g['weight'] == weight]
        draws = sum(sum(guard_hits[v][i]) for i in idx)
        every = sum(all(guard_hits[v][i]) for i in idx)
        two = sum(sum(guard_hits[v][i]) >= 2 for i in idx)
        print(f'   {v} {weight}: draws {draws}, every draw {every}, >=2 draws {two}')
control, arm = versions[0], versions[-1]
print(f'== guards {arm} keeps in fewer draws than {control} (read each against the raw answers)')
for i, g in enumerate(key['guards']):
    c, a = sum(guard_hits[control][i]), sum(guard_hits[arm][i])
    if a < c:
        print(f'   {g["weight"]:<10} {control} {c}/3 {arm} {a}/3 | {g["input_id"][:34]} | {g["span"][:150]}')
