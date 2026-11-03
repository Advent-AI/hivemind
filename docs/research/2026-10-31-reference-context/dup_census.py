"""R2 census ($0, AGENTS §1): for every opened question a blind reader classed as a duplicate of an earlier one (blind-e2e-placement-v2/opened),
how the matching step came to open it: what Jev answered about the earlier question, whether the key rules (identity.conflicts: event type,
period, scope) or the collision judge kept them apart, or whether the earlier question was never compared. Classes are counted per arm.
    python3 dup_census.py <opened folder> name=run1,run2,run3 ..."""
import collections
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind.views import identity, store  # noqa: E402


def written_views(views, input_id):
    """candidate id -> view id, from the writer's own record (processing_steps 'written', reason JSON 'new'); the writer numbers views in
    its own order, so position in the decision list is not the mapping."""
    out = {}
    for r in views.execute("select reason from processing_steps where input_id=? and step='written' order by id", (input_id,)):
        try:
            out.update(json.loads(r[0]).get('new') or {})
        except (ValueError, TypeError):
            pass
    return out

folder = Path(sys.argv[1])
verdicts = json.loads(re.search(r'\{.*\}', (folder / 'verdicts.json').read_text(), re.S).group(0))
key = json.load(open(folder / 'opened.key.json'))
arms = {}
for arg in sys.argv[2:]:
    name, paths = arg.split('=', 1)
    arms[name] = [str(ROOT / p) if not p.startswith('/') else p for p in paths.split(',')]


def opened_by(views, input_id, view_id):
    """The matching decision and the handover candidate that opened this view from this item, by the writer's own candidate -> view record."""
    cid = next((c for c, v in written_views(views, input_id).items() if v == view_id), None)
    if cid is None:
        return None, None
    for rec in views.execute('select decisions_json from match_records where input_id=? order by id', (input_id,)):
        for c in json.loads(rec['decisions_json'])['candidates']:
            if c['id'] == cid and c['outcome'] in ('new', 'succession'):
                h = views.execute('select handover_json from handovers where input_id=? order by id desc limit 1', (input_id,)).fetchone()
                cands = {x['id']: x for x in json.loads(h['handover_json']).get('candidates', [])} if h else {}
                return c, cands.get(cid)
    return None, None

counts = collections.defaultdict(collections.Counter)
examples = collections.defaultdict(list)
for qid, k in key.items():
    v = verdicts.get(qid, {})
    if v.get('class') != 'duplicate':
        continue
    of = (v.get('of') or '').strip().split()[0] if v.get('of') else ''
    run = arms[k['arm']][int(k['draw']) - 1] if str(k['draw']).isdigit() else None
    if run is None:
        run = next(r for r in arms[k['arm']] if Path(r).name == k['draw']) if any(Path(r).name == k['draw'] for r in arms[k['arm']]) else arms[k['arm']][0]
    views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); views.row_factory = sqlite3.Row
    decision, cand = opened_by(views, k['input_id'], k['view_id'])
    if decision is None:
        counts[k['arm']]['no matching record found'] += 1; continue
    reason = decision['reason']
    m = re.search(rf'\b{re.escape(of)}: (\w+) ([0-9.]+)', reason) if of else None
    judge = re.search(rf'collision judge:.*?\b{re.escape(of)}: (\w+)', reason) if of else None
    earlier_key = store.view_key(views, of) if of else None
    if not of or not m:
        cls = 'earlier question not compared (not in the list shown)' if of else 'reader named no earlier id'
    else:
        choice, prob = m.group(1), float(m.group(2))
        if choice == 'same_quantity_or_event' and prob >= 0.5:
            if judge and judge.group(1) not in ('same_question', 'same_question_other_period'):
                cls = f'Jev: same; collision judge kept apart ({judge.group(1)})'
            elif earlier_key and cand and identity.conflicts(earlier_key, cand, merging=False):
                cls = 'Jev: same; key conflict: ' + ('event type' if earlier_key['event_type'] != cand.get('event_type', 'n/a') else 'measure/scope/basis')
            elif earlier_key and cand and identity.conflicts(earlier_key, cand, merging=True):
                cls = 'Jev: same; key conflict: period (another deadline)'
            else:
                cls = 'Jev: same; opened anyway (other)'
        elif choice == 'same_quantity_other_period':
            cls = 'Jev: same quantity, other period; no succession possible'
        else:
            cls = f'Jev kept apart: {choice}' + (f' (judge {judge.group(1)})' if judge else '')
    counts[k['arm']][cls] += 1
    if len(examples[cls]) < 2:
        q = views.execute('select question from views where view_id=?', (k['view_id'],)).fetchone()[0]
        examples[cls].append(f'{k["arm"]} {k["view_id"]} "{q[:70]}" vs {of} "{(store.view(views, of) or {}).get("question", "")[:60]}"')
for arm, c in counts.items():
    print(f'== {arm}: {sum(c.values())} blind-judged duplicates')
    for cls, n in c.most_common():
        print(f'   {n:>3}  {cls}')
print('\nexamples:')
for cls, ex in examples.items():
    for e in ex:
        print(f'   [{cls}] {e}')
