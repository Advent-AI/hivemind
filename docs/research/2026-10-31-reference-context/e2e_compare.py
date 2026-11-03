"""Three draws against three draws, end to end (design-e2e.md, D253): for each run folder, the gold core and supporting matters by what
happened to them (reaches judgement, reaches marked repeat, dropped for no home, not extracted), the noise reaching judgement (gold
not-kept pieces plus the sampled share of unlisted pieces), and the questions opened; means per arm and the per-draw lists, so a
difference is read against its draws, not one number.

    python3 e2e_compare.py control=poc/data/e2e-v69-dev14-2026-10-31,poc/data/e2e-v69-dev14-d2,poc/data/e2e-v69-dev14-d3 \
                          seeded=poc/data/e2e-v69-seed-d1,poc/data/e2e-v69-seed-d2,poc/data/e2e-v69-seed-d3
"""
import collections
import json
import sqlite3
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import score_ref as sr  # noqa: E402

UNLISTED_NOISE_SHARE = 0.27          # two blind readers on 60 gold-unlisted statements (blind-v68a-ruler): 16 of 60 not kept


def measure(run):
    views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); views.row_factory = sqlite3.Row
    archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    replaced = {r[0] for r in views.execute('select old_evidence_id from replacements')}
    repeats = {r[0] for r in views.execute('select new_evidence_id from same_claims')}

    def answer(iid):
        r = archive.execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {iid},%',)).fetchone()
        return json.loads(r[0]) if r and r[0] else {}

    def gold_class(a, e):
        if any(sr.sg.same_matter(i, e) for i in a['items'] if i['weight'] in ('core', 'supporting')):
            return 'core/supp'
        if any(sr.sg.same_matter(i, e) for i in a['items'] if i['weight'] == 'optional') or any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'optional'):
            return 'optional'
        if any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'not_kept'):
            return 'not_kept'
        return 'unlisted'

    out = collections.Counter(); matters = collections.Counter(); processed = 0
    for a in sr.articles:
        iid = a['input_id']
        stored = [dict(r) for r in views.execute('select evidence_id, quote, one_line from evidence where created_from_input=?', (iid,))]
        h = views.execute('select handover_json from handovers where input_id=? order by id desc limit 1', (iid,)).fetchone()
        if not h and not stored:
            continue
        processed += 1
        by_id = {e['id']: e for e in answer(iid).get('evidence', [])}
        dropped_ids = {e for e, _ in json.loads(h['handover_json']).get('dropped', [])} if h else set()
        dropped = [by_id[e] for e in dropped_ids if e in by_id]
        shown = [s for s in stored if s['evidence_id'] not in replaced]
        for s in shown:
            g = gold_class(a, s)
            out[('reaches', g)] += 1
            if s['evidence_id'] in repeats:
                out[('reaches as repeat', g)] += 1
        for e in dropped:
            out[('dropped', gold_class(a, e))] += 1
        for it in a['items']:
            if it['weight'] not in ('core', 'supporting'):
                continue
            if any(sr.sg.same_matter(it, s) for s in shown if s['evidence_id'] not in repeats):
                state = 'reaches'
            elif any(sr.sg.same_matter(it, s) for s in shown):
                state = 'reaches as repeat'
            elif any(sr.sg.same_matter(it, e) for e in dropped):
                state = 'dropped'
            elif any(sr.sg.same_matter(it, e) for e in by_id.values()):
                state = 'extracted, other'
            else:
                state = 'not extracted'
            matters[(it['weight'], state)] += 1
    n_views = views.execute('select count(*) from views where created_seq > 0').fetchone()[0]
    noise = out[('reaches', 'not_kept')] + UNLISTED_NOISE_SHARE * out[('reaches', 'unlisted')]
    return {'processed': processed, 'pieces reaching judgement': sum(v for (p, g), v in out.items() if p == 'reaches'),
            'core/supp pieces reaching': out[('reaches', 'core/supp')], 'noise reaching (est.)': round(noise, 1),
            'gold-not-kept reaching': out[('reaches', 'not_kept')], 'dropped core/supp pieces': out[('dropped', 'core/supp')],
            'questions opened by articles': n_views,
            **{f'{w} {s}': matters[(w, s)] for w in ('core', 'supporting') for s in ('reaches', 'reaches as repeat', 'dropped', 'not extracted')}}


arms = {}
for arg in sys.argv[1:]:
    name, paths = arg.split('=', 1)
    arms[name] = [measure(str(ROOT / p) if not p.startswith('/') else p) for p in paths.split(',')]
keys = list(next(iter(arms.values()))[0])
print(f'{"":<32}' + ''.join(f'{name:>22}' for name in arms))
for k in keys:
    cells = []
    for name, runs in arms.items():
        vals = [r[k] for r in runs]
        cells.append(f'{statistics.mean(vals):>7.1f} {str(vals):>14}')
    print(f'{k:<32}' + ''.join(f'{c:>22}' for c in cells))
