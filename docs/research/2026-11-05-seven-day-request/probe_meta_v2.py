"""The version-2 record-preparation request re-sent on every stored A answer of the stopped run's first 100 items: which subject each
question is filed under, and whether a numeric question gets a ladder the code accepts. One send per item; nothing is written to a ledger."""
import concurrent.futures, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / 'docs/research/2026-11-05-parallel-refinement'), str(ROOT / 'src')]
import split_seven_day_poc as p
from hivemind import config, extraction, model, testdb, universe

RUN = ROOT / 'poc/data/split-fresh-seven-day-matching-v4-2026-11-05'
OUT = ROOT / 'poc/data/meta-v2-probe-2026-11-05'

def main():
    OUT.mkdir(exist_ok=False)
    cfg = config.load(str(p.CONFIG)); uni = universe.load(str(ROOT / 'poc/universe.json'))
    manifest = json.loads((RUN / 'manifest.json').read_text()); first = {r['id'] for r in manifest['input_rows'][:100]}
    items = testdb.open_db(str(p.INPUT)); jobs = []
    for folder in sorted((RUN / 'items').glob('*'), key=lambda f: int(f.name)):
        if not (folder / 'a-answer.json').exists():
            continue
        a = json.loads((folder / 'a-answer.json').read_text())
        user = json.loads((folder / 'b-request.json').read_text())['messages'][-1]['content']
        iid = user.split('[Item] id ')[1].split(',')[0]
        if iid not in first or not a['questions']:
            continue
        item = testdb.item_of(items.execute('select * from items where input_id=?', (iid,)).fetchone())
        setting = cfg.extraction_setting(item['category'])
        jobs.append((folder.name, item, a, setting))
    archive = model.Archive(str(OUT / 'archive.sqlite'))
    def send(job):
        seq, item, a, setting = job
        system, user, schema, name = p.metadata_request(item, a, uni)
        answer = model.call(archive, cfg, setting, system, user, schema, name, 'meta')
        rows = []
        for i, q in enumerate(a['questions'], 1):
            m = answer.data['candidates']['c' + str(i)]
            subject, kind = p.chosen_subject(m, q, uni)
            rungs = m['rungs']; problem = (extraction.check_ladder(rungs, kind) or extraction.check_bounds(rungs)) if rungs else 'empty'
            rows.append({'seq': seq, 'question': q['question'], 'object': m['object'], 'new_subject': m['new_subject'], 'kind': kind,
                         'shared': p.shared_key(m, kind).get('measure', ''), 'year': m['year'], 'rungs': len(rungs), 'ladder_problem': problem,
                         'neutral': next((r['condition'] for r in rungs if r['label'].lower() == 'neutral'), '')})
        return rows, answer.cost_usd
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(send, jobs))
    rows = [r for rs, _ in results for r in rs]
    (OUT / 'results.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1) + '\n')
    for r in rows:
        print(f"{r['seq']} {r['object'][:22]:22s} {r['kind']:5s} {r['shared'] or '-':11s} rungs {r['rungs']} {r['ladder_problem'] or 'ok':10.10s} | {r['question'][:80]}")
    print('cost', round(sum(c for _, c in results), 4), 'questions', len(rows))

if __name__ == '__main__':
    main()
