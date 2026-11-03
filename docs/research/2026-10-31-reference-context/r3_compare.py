"""R3's per-statement comparison (design-r3-review.md §5): the stored role-v65 draws against the role-v66 draws on the same articles
(development gold 118 and test gold 30). P1 and P2: every statement of the lost and guard lists (r3-lists.json, written by r3_lost.py)
kept in k of 3 draws under each version. P5: the statements the arm keeps in at least two draws that the control keeps in none, and
the reverse, each labelled by the gold entry it matches, for reading. Code counts structure only; meaning is read.
    python3 r3_compare.py [CONTROL_PREFIX CONTROL_VERSION ARM_PREFIX ARM_VERSION]      (default Y5 v65 Y6 v66)"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LEDGER = ROOT / 'docs/research/2026-10-29-ledger-standard'
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'docs/research/2026-10-29-analyst-standard'), str(LEDGER), str(LEDGER / 'final-2026-10-30')]
import final_scores as fs  # noqa: E402
import score_gold as sg  # noqa: E402

control_prefix, control_version, arm_prefix, arm_version = (sys.argv[1:5] if len(sys.argv) >= 5 else ('Y5', 'v65', 'Y6', 'v66'))
articles = {a['input_id']: a for name in ('dev', 'test') for a in json.loads(Path(fs.GOLDS[name]).read_text())['articles']}
lists = json.loads((HERE / 'r3-lists.json').read_text())


def draws(prefix, version):
    """input_id -> [kept statements of draw 1, 2, 3] (None for an unusable answer)."""
    out = collections.defaultdict(list)
    for d in (1, 2, 3):
        rows = sg.answers(f'{prefix}-{version}-d{d}')
        for iid in articles:
            s = sg.kept(rows.get(iid), iid)
            out[iid].append(None if s is None else s['evidence'])
    return out


def label(a, e):
    """The gold entry a kept statement expresses: its weight, or 'unlisted'."""
    for i in a['items']:
        if i['weight'] in ('core', 'supporting', 'optional') and sg.same_matter(i, e):
            return i['weight']
    for n in a.get('not_kept', []):
        if sg.same(n['span'], e['quote']):
            return 'not_kept'
    return 'unlisted'


control, arm = draws(control_prefix, control_version), draws(arm_prefix, arm_version)
usable = {v: sum(1 for iid in articles for s in d[iid] if s is not None) for v, d in ((control_version, control), (arm_version, arm))}
print(f'usable answers of {len(articles) * 3}: {usable}')
print(f'statements kept per draw: ' + ' | '.join(f'{v} ' + '/'.join(str(sum(len(d[iid][k] or []) for iid in articles)) for k in range(3)) for v, d in ((control_version, control), (arm_version, arm))))


def kept_in(statements_by_draw, test):
    return sum(1 for s in statements_by_draw if s is not None and any(test(e) for e in s))


print(f'\n## P1 lost core/supporting statements: kept in k of 3 draws, {control_version} -> {arm_version}')
for entry in lists['lost']:
    a = articles[entry['input_id']]
    item = next(i for i in a['items'] if i['span'] == entry['span'])
    c, r = kept_in(control[a['input_id']], lambda e: sg.same_matter(item, e)), kept_in(arm[a['input_id']], lambda e: sg.same_matter(item, e))
    print(f'- {c}/3 -> {r}/3 | {a["publication_day"]} {entry["input_id"][-12:]} | gold {item["weight"]}: {item["span"][:100]!r}')

print(f'\n## P2 guard statements (gold not kept, control kept in none): kept in k of 3 draws, {control_version} -> {arm_version}')
readmitted = 0
for entry in lists['guard']:
    a = articles[entry['input_id']]
    kept_gold = [i for i in a['items'] if i['weight'] in ('core', 'supporting', 'optional')]
    test = lambda e, span=entry['span'], kg=kept_gold: sg.same(span, e['quote']) and not any(sg.same_matter(k, e) for k in kg)   # D250 item 5
    c, r = kept_in(control[a['input_id']], test), kept_in(arm[a['input_id']], test)
    readmitted += r >= 2
    print(f'- {c}/3 -> {r}/3 | {a["publication_day"]} {entry["input_id"][-12:]} | {entry["span"][:100]!r}')
print(f'guard statements kept in >=2 draws by {arm_version}: {readmitted} of {len(lists["guard"])}')


def clusters(by_draw):
    """Distinct statements of one article across the draws of one version: a statement is the same when score_gold.same holds on the quotes."""
    reps = []
    for s in by_draw:
        for e in s or []:
            if not any(sg.same(r['quote'], e['quote']) for r in reps):
                reps.append(e)
    return reps


print(f'\n## P5 statements {arm_version} keeps in >=2 draws and {control_version} in none (new), and the reverse (gone)')
summary = collections.defaultdict(collections.Counter)
for iid, a in sorted(articles.items(), key=lambda x: (x[1]['publication_day'], x[0])):
    for name, this, other in (('new', arm, control), ('gone', control, arm)):
        for e in clusters(this[iid]):
            n_this = kept_in(this[iid], lambda x, q=e['quote']: sg.same(q, x['quote']))
            n_other = kept_in(other[iid], lambda x, q=e['quote']: sg.same(q, x['quote']))
            if n_this >= 2 and n_other == 0:
                lab = label(a, e)
                summary[name][lab] += 1
                print(f'- {name} [{lab}] {n_this}/3 vs 0/3 | {a["publication_day"]} {iid[-12:]} | {e["quote"][:110]!r}\n    one_line: {e.get("one_line", "")[:150]!r}')
for name in ('new', 'gone'):
    print(f'{name}: {sum(summary[name].values())} statements by gold label {dict(summary[name])}')
