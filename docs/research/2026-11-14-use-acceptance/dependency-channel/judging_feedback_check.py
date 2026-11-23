"""Do a day's judgements feed back into later reading or matching requests? ($0.) If they do not, a run of the 14 days that re-runs
only the judging can take every reading and matching answer from the stored archive. The stored seeded draw is replayed from its
preset questions through all 14 days with every judgement replaced by a labelled fake (the first band of the ladder, so the
question states differ from the stored run's wherever they can) and every other request answered from the stored archive or
refused. If the replay completes, no reading or matching request depended on a judgement.

  python3 judging_feedback_check.py <scratch folder> [stored|corrected]
"""
import json
import re
import shutil
import sqlite3
import sys
import threading
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, model, replay, seeding, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

RUN = ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
SEEDS = json.loads((ROOT / 'poc/seeds/nvda-2026-07-01-v2.json').read_text())['questions']


def main():
    scratch, direction = Path(sys.argv[1]), (sys.argv[2] if len(sys.argv) > 2 else 'stored')
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    shutil.copy(RUN / 'archive.sqlite', scratch / 'archive.sqlite')
    cfg, uni = config.load(str(ROOT / 'poc/config/poc-v108.json')), universe.load(str(ROOT / 'poc/universe.json'))
    archive = model.Archive(str(scratch / 'archive.sqlite'))
    rows_before = sqlite3.connect(scratch / 'archive.sqlite').execute('select count(*) from model_calls').fetchone()[0]
    ledger = store.open_db(str(scratch / 'views.sqlite'))
    seeding.seed_views(ledger, str(ROOT / 'poc/seeds/nvda-2026-07-01-v2.json'), created_at='2026-07-01T00:00:00Z')
    ledger.commit()
    ledger.close()
    originals = (store.dependencies_of, store.dependants_of)
    if direction == 'corrected':                      # the seed edges read the other way for judging only, as in ordering_proof.py (the run holds no other edge)
        edges = [(q['view_id'], q['depends_on']) for q in SEEDS if q.get('depends_on')]
        store.dependencies_of = lambda connection, view_id: [
            {'dependency_id': None, 'view_id': view_id, 'depends_on': supporting, 'resolved_to': supporting, 'resolution': 'direct', 'direction': 'last_end',
             'wait_chain_view_id': None, 'wait_year': None} for supporting, supported in edges if supported == view_id]
        store.dependants_of = lambda connection, view_id: sorted({supported for supporting, supported in edges if supporting == view_id})
    fakes, lock = [], threading.Lock()

    def transport(*args, **kwargs):
        request = args[1] if len(args) == 2 else None
        name = ((request or {}).get('response_format') or {}).get('json_schema', {}).get('name') if isinstance(request, dict) else None
        if name == 'judgement':
            user = request['messages'][-1]['content']
            view = re.match(r'Thesis (v\d+) ', user).group(1)
            first = '[Previous conclusion, for comparison only]' not in user
            with lock:
                fakes.append(view)
            label = f'LABELLED FAKE OUTPUT for {view}'
            answer = {'rung': 1, 'reference': label, 'implied_outcome': label, 'reasons': label + ': the feedback check, not a model answer.', 'cites': [], 'cites_views': [], 'pushes': [],
                      'changed': True, 'why_changed': 'labelled fake output', 'theme_pushes': []}
            return {'choices': [{'message': {'content': json.dumps(answer)}}], 'usage': {'prompt_tokens': 0, 'completion_tokens': 0}, 'synthetic': True}
        raise RuntimeError(f'a request that is not a judgement was not in the stored archive (kind: {name or "matching engine"}): judgements feed back into it')

    try:
        totals = replay.run(testdb_path=str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'), views_path=str(scratch / 'views.sqlite'), archive=archive, cfg=cfg, universe=uni,
                            from_day='2026-07-01', until_day='2026-07-14', only_objects={'NVDA'}, transport=transport, log=lambda *parts: None)
        outcome = f"the replay completed: failed {totals.get('failed')}"
    except Exception as error:
        outcome = 'the replay stopped: ' + repr(error)[:400]
    finally:
        store.dependencies_of, store.dependants_of = originals
    rows_after = sqlite3.connect(scratch / 'archive.sqlite').execute('select count(*) from model_calls').fetchone()[0]
    rebuilt = sqlite3.connect(f"file:{scratch / 'views.sqlite'}?mode=ro", uri=True)
    stored = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
    counts = {name: (rebuilt.execute(query).fetchone()[0], stored.execute(query).fetchone()[0]) for name, query in (
        ('statements', 'select count(*) from evidence'), ('links', 'select count(*) from evidence_links'), ('questions', 'select count(*) from views'), ('judgements', 'select count(*) from judgements'),
        ('days completed', 'select count(*) from days_completed'))}
    same_links = set(rebuilt.execute('select evidence_id, view_id, seq from evidence_links')) == set(stored.execute('select evidence_id, view_id, seq from evidence_links'))
    print(f"direction {direction}: {outcome}; fake judgements {len(fakes)}; archive rows {rows_before} -> {rows_after} (every new row is a fake judgement: {rows_after - rows_before == len(fakes)})")
    print('   rebuilt against stored (rebuilt, stored):', counts, '| the same statements under the same questions at the same articles:', same_links)


if __name__ == '__main__':
    main()
