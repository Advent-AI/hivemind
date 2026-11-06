"""Locate the version-2 new-question regressions: a quote written into the question field (1209, 1210, 1275) and legitimate
questions no longer proposed (1238, 1246, 1269). Arms: as built; without the quote-field definition; without the appended closing
check (and its pointer sentence). Two sends per arm and item, each in its own archive."""
import concurrent.futures, copy, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / 'docs/research/2026-11-05-parallel-refinement'), str(ROOT / 'src')]
import split_seven_day_poc as p
from hivemind import config, model, testdb, universe
from hivemind.views import store

RUN = ROOT / 'poc/data/split-fresh-seven-day-matching-v4-2026-11-05'
OUT = ROOT / 'poc/data/a-v2-variants-2026-11-05'
SEQS = [1209, 1210, 1275, 1238, 1246, 1269]
POINTER = ' Apply the closing check at the end of the request to every passage and drop what it rejects.'

def arms(spec):
    system, user, schema, name = spec
    no_quote = copy.deepcopy(schema); no_quote['properties']['questions']['items']['properties']['evidence']['items']['properties']['quote'].pop('description')
    assert system.count(POINTER) == 1
    no_check = (system.replace(POINTER, ''), user[:user.index('\n\n[Closing check for every evidence passage]')], schema, name)
    return {'built': spec, 'no_quote_definition': (system, user, no_quote, name), 'no_closing_check': no_check}

def broken(answer):
    return any(q['question'].strip()[-1:] != '?' for q in answer['questions'])

def main():
    OUT.mkdir(exist_ok=False)
    cfg = config.load(str(p.CONFIG)); uni = universe.load(str(ROOT / 'poc/universe.json'))
    snap = store.open_read_only(str(RUN / 'snapshot/views.sqlite')); items = testdb.open_db(str(p.INPUT))
    jobs = []
    for seq in SEQS:
        iid = json.loads((RUN / 'items' / str(seq) / 'b-request.json').read_text())['messages'][-1]['content'].split('[Item] id ')[1].split(',')[0]
        item = testdb.item_of(items.execute('select * from items where input_id=?', (iid,)).fetchone())
        setting, requests = p.item_requests(cfg, uni, item, p.latest_library(snap, seq))
        for arm, spec in arms(requests['a']).items():
            for draw in (1, 2):
                jobs.append((seq, arm, draw, setting, spec))
    archives = {}
    def send(job):
        seq, arm, draw, setting, spec = job
        archive = model.Archive(str(OUT / f'{arm}-{draw}.sqlite'))
        try:
            answer = model.call(archive, cfg, setting, spec[0], spec[1], spec[2], spec[3], 'a')
        finally:
            archive.conn.close()
        return {'seq': seq, 'arm': arm, 'draw': draw, 'questions': [q['question'] for q in answer.data['questions']], 'broken': broken(answer.data), 'cost': answer.cost_usd}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(send, jobs))
    (OUT / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=1) + '\n')
    for seq in SEQS:
        for arm in ('built', 'no_quote_definition', 'no_closing_check'):
            rs = [r for r in results if r['seq'] == seq and r['arm'] == arm]
            print(seq, f'{arm:20s}', ' | '.join(('BROKEN ' if r['broken'] else '') + (' / '.join(q[:60] for q in r['questions']) or '(none)') for r in rs))
    print('cost', round(sum(r['cost'] for r in results), 4))

if __name__ == '__main__':
    main()
