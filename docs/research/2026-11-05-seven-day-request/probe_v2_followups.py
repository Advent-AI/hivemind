"""Follow-ups after the first split-v2 run: (1) record preparation with the part-period reference sentence on the run's numeric questions,
(2) the new-question call with the one-deal sentence on the two Hugging Face items, twice each, against the run's own ledger."""
import concurrent.futures, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / 'docs/research/2026-11-05-parallel-refinement'), str(ROOT / 'src')]
import split_seven_day_poc as p
from hivemind import config, extraction, model, testdb, universe
from hivemind.views import store

RUN = ROOT / 'poc/data/split-v2-first100-2026-11-05'
OUT = ROOT / 'poc/data/split-v2-followups-2026-11-05'
META_SEQS = [1211, 1246, 1252, 1254, 1268, 1275, 1207, 1228, 1247]
A_SEQS = [1248, 1256]

def item_of(items, seq):
    iid = json.loads((RUN / 'items' / str(seq) / 'b-request.json').read_text())['messages'][-1]['content'].split('[Item] id ')[1].split(',')[0]
    return testdb.item_of(items.execute('select * from items where input_id=?', (iid,)).fetchone())

def main():
    OUT.mkdir(exist_ok=False)
    cfg = config.load(str(p.CONFIG)); uni = universe.load(str(ROOT / 'poc/universe.json'))
    items = testdb.open_db(str(p.INPUT)); snap = store.open_read_only(str(RUN / 'snapshot/views.sqlite'))
    jobs = []
    for seq in META_SEQS:
        item = item_of(items, seq); a = json.loads((RUN / 'items' / str(seq) / 'a-answer.json').read_text())
        jobs.append(('meta', seq, 1, cfg.extraction_setting(item['category']), p.metadata_request(item, a, uni), a))
    for seq in A_SEQS:
        item = item_of(items, seq); setting, requests = p.item_requests(cfg, uni, item, p.latest_library(snap, seq))
        for draw in (1, 2):
            jobs.append(('a', seq, draw, setting, requests['a'], None))
    def send(job):
        kind, seq, draw, setting, spec, a = job
        archive = model.Archive(str(OUT / f'{kind}-{draw}.sqlite'))
        try:
            answer = model.call(archive, cfg, setting, spec[0], spec[1], spec[2], spec[3], kind)
        finally:
            archive.conn.close()
        if kind == 'meta':
            rows = []
            for i, q in enumerate(a['questions'], 1):
                m = answer.data['candidates']['c' + str(i)]; subject, k = p.chosen_subject(m, q, uni); rungs = m['rungs']
                problem = (extraction.check_ladder(rungs, k) or extraction.check_bounds(rungs)) if rungs else 'empty'
                neutral = next((r['condition'] for r in rungs if r['label'].lower() == 'neutral'), '')
                rows.append(f"{q['question'][:70]} | rungs {len(rungs)} {problem or 'ok'} | neutral: {neutral[:160]}")
            return kind, seq, draw, rows, answer.cost_usd
        return kind, seq, draw, [f"{q['question'][:90]} (closest {q['closest_existing_question']})" for q in answer.data['questions']] or ['(none)'], answer.cost_usd
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(send, jobs))
    (OUT / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=1) + '\n')
    for kind, seq, draw, rows, _ in results:
        for r in rows:
            print(kind, seq, draw, r)
    print('cost', round(sum(r[4] for r in results), 4))

if __name__ == '__main__':
    main()
