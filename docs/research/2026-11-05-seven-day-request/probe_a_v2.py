"""The version-2 new-question request (split-a-v2 prompt, shared closing check, closest-question fields) re-sent once on stored items
with every question open immediately before them in the stopped run's ledger. Compares what it proposes with the stored version-1 answer."""
import concurrent.futures, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / 'docs/research/2026-11-05-parallel-refinement'), str(ROOT / 'src')]
import split_seven_day_poc as p
from hivemind import config, model, testdb, universe
from hivemind.views import store

RUN = ROOT / 'poc/data/split-fresh-seven-day-matching-v4-2026-11-05'
OUT = ROOT / ('poc/data/a-v2-probe-2026-11-05' + (sys.argv[1] if len(sys.argv) > 1 else ''))
SHOULD_NOT = [1206, 1220, 1226, 1231, 1232, 1235, 1236, 1249, 1253, 1258, 1270, 1277, 1280]
LEGIT = [1209, 1210, 1237, 1238, 1246, 1269, 1273, 1275]

def main():
    OUT.mkdir(exist_ok=False)
    cfg = config.load(str(p.CONFIG)); uni = universe.load(str(ROOT / 'poc/universe.json'))
    snap = store.open_read_only(str(RUN / 'snapshot/views.sqlite')); items = testdb.open_db(str(p.INPUT))
    jobs = []
    for seq in SHOULD_NOT + LEGIT:
        folder = RUN / 'items' / str(seq)
        iid = json.loads((folder / 'b-request.json').read_text())['messages'][-1]['content'].split('[Item] id ')[1].split(',')[0]
        item = testdb.item_of(items.execute('select * from items where input_id=?', (iid,)).fetchone())
        shown = p.latest_library(snap, seq)
        setting, requests = p.item_requests(cfg, uni, item, shown)
        old = json.loads((folder / 'a-answer.json').read_text())
        jobs.append((seq, setting, requests['a'], old))
    archive = model.Archive(str(OUT / 'archive.sqlite'))
    def send(job):
        seq, setting, spec, old = job
        answer = model.call(archive, cfg, setting, spec[0], spec[1], spec[2], spec[3], 'a')
        return {'seq': seq, 'group': 'should_not' if seq in SHOULD_NOT else 'legit', 'old': [(q['question'], len(q['evidence'])) for q in old['questions']],
                'new': [{'question': q['question'], 'closest': q['closest_existing_question'], 'separates': q['what_separates_it'], 'evidence': len(q['evidence'])} for q in answer.data['questions']],
                'answer': answer.data, 'input_tokens': answer.input_tokens, 'cost': answer.cost_usd}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(send, jobs))
    (OUT / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=1) + '\n')
    for r in results:
        print(f"{r['seq']} [{r['group']}] OLD: " + ' || '.join(f'{q[:70]} ({n} ev)' for q, n in r['old']))
        for q in r['new']:
            print(f"      NEW: {q['question'][:90]} ({q['evidence']} ev) closest {q['closest']}")
        if not r['new']:
            print('      NEW: (none)')
    print('cost', round(sum(r['cost'] for r in results), 4), 'mean input tokens', sum(r['input_tokens'] for r in results) // len(results))

if __name__ == '__main__':
    main()
