"""R2 acceptance at $0 (design-r2-identity.md §3): re-derive, from the stored matching records (Jev's top answer per listed question and the
collision judge's verdicts, as the decision reason records them), the handover's candidates and the ledger's keys, what the identity rules
R2-a (one event, any deadline) and R2-b (one product generation, any milestone) would have done with every candidate that opened a question,
and score it against the blind reader's labels of the opened questions (duplicate of X / not a duplicate). --judge adds R2-c (a Jev or judge
'same' is not overridden by the judge's 'distinct_question_same_matter').
    python3 replay_identity.py <opened folder> [--judge] name=run1,run2,run3 ..."""
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

GENERATION_MILESTONES = ('launch', 'shipment', 'deployment')
folder = Path(sys.argv[1])
with_judge = '--judge' in sys.argv
verdicts = json.loads(re.search(r'\{.*\}', (folder / 'verdicts.json').read_text(), re.S).group(0))
key = json.load(open(folder / 'opened.key.json'))
labels = {(k['arm'], str(k['draw']), k['view_id']): verdicts.get(q, {}) for q, k in key.items()}
arms = {}
for arg in sys.argv[2:]:
    if '=' in arg:
        name, paths = arg.split('=', 1)
        arms[name] = [str(ROOT / p) if not p.startswith('/') else p for p in paths.split(',')]


def rule(views, cand, reason):
    """The view R2-a/b (and R2-c with --judge) would merge this candidate into, or None."""
    if cand.get('measure') not in identity.EVENT_MEASURES:
        return None, ''
    answers = {m.group(1): (m.group(2), float(m.group(3))) for m in re.finditer(r'\b(v\d+): (\w+) ([0-9.]+)', reason.split('collision judge:')[0])}
    judged = {m.group(1): m.group(2) for m in re.finditer(r'\b(v\d+): (\w+)', reason.split('collision judge:')[1])} if 'collision judge:' in reason else {}
    same = {v for v, (choice, prob) in answers.items() if choice in ('same_quantity_or_event', 'same_quantity_other_period') and prob >= 0.5}
    if with_judge:
        same |= {v for v, verdict in judged.items() if verdict in ('same_question', 'same_question_other_period')}
    for v in sorted(same, key=lambda s: -answers.get(s, ('', 0))[1]):
        k = store.view_key(views, v)
        view = store.view(views, v) or {}
        if not k or view.get('object_id') != cand.get('object') or k['measure'] != cand['measure'] or not store.is_open(views, v):
            continue
        if not with_judge and judged.get(v) == 'distinct_question_same_matter':
            continue
        if k['event_type'] == cand.get('event_type') or (k['event_type'] in GENERATION_MILESTONES and cand.get('event_type') in GENERATION_MILESTONES):
            return v, ('R2-a same event, another deadline' if k['event_type'] == cand.get('event_type') else 'R2-b generation milestone')
    return None, ''


totals = collections.defaultdict(collections.Counter)
reads = []
for arm, runs in arms.items():
    for draw, run in enumerate(runs, 1):
        views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); views.row_factory = sqlite3.Row
        for rec in views.execute('select input_id, decisions_json from match_records order by id'):
            decisions = json.loads(rec['decisions_json'])['candidates']
            openers = [c for c in decisions if c['outcome'] in ('new', 'succession')]
            if not openers:
                continue
            written = written_views(views, rec['input_id'])
            h = views.execute('select handover_json from handovers where input_id=? order by id desc limit 1', (rec['input_id'],)).fetchone()
            cands = {c['id']: c for c in json.loads(h['handover_json']).get('candidates', [])} if h else {}
            for decision in openers:
                view_id = written.get(decision['id'])
                if view_id is None:
                    continue
                label = labels.get((arm, str(draw), view_id), {})
                cand = cands.get(decision['id']) or {}
                target, why = rule(views, cand, decision['reason'])
                is_dup = label.get('class') == 'duplicate'
                of = (label.get('of') or '').strip().split()[0] if label.get('of') else ''
                if target:
                    if is_dup:
                        totals[arm]['merged, blind duplicate' + (' (same target)' if of == target else ' (other earlier question)')] += 1
                    else:
                        totals[arm][f'merged, blind {label.get("class", "unlabelled")}: READ'] += 1
                        q = views.execute('select question from views where view_id=?', (view_id,)).fetchone()[0]
                        reads.append(f'{arm} d{draw} {view_id} "{q[:80]}" -> {target} "{(store.view(views, target) or {}).get("question", "")[:70]}" [{why}; blind {label.get("class")}: {label.get("note", "")[:80]}]')
                elif is_dup:
                    totals[arm]['still opened, blind duplicate' + (' (event)' if cand.get('measure') in identity.EVENT_MEASURES else ' (figure question)')] += 1
                else:
                    totals[arm]['still opened, not a duplicate'] += 1
for arm, c in totals.items():
    print(f'== {arm} ({"R2-a/b/c" if with_judge else "R2-a/b"}): {sum(c.values())} opened questions over 3 draws')
    for k2, n in sorted(c.items()):
        print(f'   {n:>3}  {k2}')
print('\nmerges the blind reader did not call duplicates (every one to read):')
for r in reads:
    print('  ', r)
