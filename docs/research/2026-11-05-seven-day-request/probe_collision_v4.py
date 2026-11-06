"""Review prompt collision-v3 against collision-v4 on stored candidates and real ledger questions, three sends each.
Pairs that should be one question and pairs that must stay apart (D248; standard section 4). Writes one archive per arm and draw."""
import concurrent.futures, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, model
from hivemind.views import jev_matching, store

RUN = ROOT / 'poc/data/split-fresh-seven-day-matching-v4-2026-11-05'
OUT = ROOT / ('poc/data/collision-v4-probe-2026-11-05' + (sys.argv[1] if len(sys.argv) > 1 else ''))
conn = store.open_read_only(str(RUN / 'snapshot/views.sqlite'))

def stored(seq, index=0):
    h = json.loads((RUN / 'items' / str(seq) / 'handover.json').read_text())
    return h['candidates'][index], h['evidence']

def from_view(view_id):
    view = store.view(conn, view_id); pieces = store.evidence_in_force(conn, view_id)[:4]
    ev = [dict(p, id='x' + str(i)) for i, p in enumerate(pieces)]
    c = {'id': 'c1', 'kind': view['kind'], 'object': view['object_id'], 'looks_at': view['looks_at'], 'question': view['question'],
         'year': view['year'], 'due_day': view['due_day'], 'rungs': [], 'evidence_ids': [e['id'] for e in ev]}
    return c, ev

# (name, expected, candidate source, existing question)
PAIRS = [('cpu_same_period', 'same', stored(1253), 'v85'), ('capex_population', 'same', stored(1250), 'v5'),
         ('fed_coarse_fine', 'same', stored(1271), 'v82'), ('hf_completion_vs_agreement', 'same', stored(1208), 'v64'),
         ('rtx_later_deadline', 'same', stored(1312), 'v109'),
         ('cpu_vs_total_growth', 'apart', stored(1253), 'v73'), ('cpu_fy28_vs_fy27', 'apart', stored(1253), 'v7'),
         ('server_cpu_vs_dc_fy27', 'apart', stored(1246), 'v10'), ('fed_yearend_vs_sept', 'apart', stored(1262), 'v82'),
         ('commitments_total_vs_one_deal', 'apart', stored(1209), 'v29'), ('networking_vs_dc', 'apart', from_view('v65'), 'v10'),
         ('total_vs_dc', 'apart', from_view('v2'), 'v10'), ('capex_2026_vs_2027', 'apart', from_view('v4'), 'v5')]

def run():
    OUT.mkdir(parents=False, exist_ok=False)
    jobs = []
    for arm, path in (('v3', 'poc/config/poc-v118.json'), ('v4', 'poc/config/poc-split-v2.json')):
        cfg = config.load(str(ROOT / path))
        system = (ROOT / 'src/hivemind/prompts' / (cfg.collision.prompt_version + '.txt')).read_text()
        schema = jev_matching.COLLISION_SCHEMA_V4 if arm == 'v4' else jev_matching.COLLISION_SCHEMA
        for draw in (1, 2, 3):
            archive = model.Archive(str(OUT / f'{arm}-{draw}.sqlite'))
            for name, expected, (c, ev), target in PAIRS:
                user = jev_matching.candidate_state(c, ev) + '\n\nTHESES:\n' + f'--- {target}\n{jev_matching.thesis_text(conn, target)}' + '\n\nFor each thesis id, state the relation.'
                jobs.append((arm, draw, archive, cfg, system, schema, name, expected, target, user))
    def send(job):
        arm, draw, archive, cfg, system, schema, name, expected, target, user = job
        answer = model.call(archive, cfg, cfg.collision, system, user, schema, 'collision', 'match')
        rel = next((r for r in answer.data['relations'] if r['thesis_id'] == target), {'relation': '(none)', 'why': ''})
        return {'arm': arm, 'draw': draw, 'pair': name, 'expected': expected, 'relation': rel['relation'], 'why': rel['why'], 'cost': answer.cost_usd}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(send, jobs))
    (OUT / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=1) + '\n')
    for name, expected, _, _ in PAIRS:
        line = {arm: [r['relation'] for r in results if r['pair'] == name and r['arm'] == arm] for arm in ('v3', 'v4')}
        print(f'{name:32s} expected {expected:5s} v3 {line["v3"]} v4 {line["v4"]}')
    print('cost', round(sum(r['cost'] for r in results), 4))

if __name__ == '__main__':
    run()
