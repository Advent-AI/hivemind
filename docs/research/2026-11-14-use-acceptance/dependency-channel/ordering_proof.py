"""D368's reading direction, ordering and propagation, with labelled fake judgement outputs ($0; D534, part 2).

On a scratch copy of a frozen seeded draw, one extra judging round is run through the production code (`judging.round_of_judgements`)
with the edges read in the direction D368 decides: the supported question reads the conclusions of the questions that support it.
The direction is changed in the harness only, for the judging use (`store.dependencies_of`, `store.dependants_of`); the filing use of
the same edges (`store.direct_parents`) is left as it is and checked to be unchanged. Every judgement output is a labelled fake. No
model call; no package or frozen file changed. The script exits with an error if a registered expectation fails.

  python3 ordering_proof.py <scratch folder>            (D368_MUTANT=stored-direction leaves the stored direction: must fail)
"""
import json
import os
import re
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, model  # noqa: E402
from hivemind.views import judging, store  # noqa: E402

RUN = ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
START, CHAIN = 'v6', ['v6', 'v2', 'v1']          # v6 supports v2 (data-center revenue), which supports v1 (total revenue): registered before the run


def main():
    work = Path(sys.argv[1])
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for name in ('views.sqlite', 'archive.sqlite'):
        shutil.copy(RUN / name, work / name)
    cfg = config.load(str(ROOT / 'poc/config/poc-v108.json'))
    conn, archive = store.open_db(str(work / 'views.sqlite')), model.Archive(str(work / 'archive.sqlite'))
    edges = [(row[0], row[1], row[2]) for row in conn.execute("select d.view_id, coalesce((select r.resolved_to from dependency_resolutions r where r.dependency_id = d.dependency_id order by r.id desc limit 1), d.depends_on), d.direction from dependencies d")]
    edges = [(supporting, supported, direction) for supporting, supported, direction in edges if supported]
    views = [row[0] for row in conn.execute('select view_id from views')]
    filing_before = {view: store.direct_parents(conn, view) for view in views}
    round_seq = conn.execute('select max(seq) from judgements').fetchone()[0] + 1
    originals = (store.dependencies_of, store.dependants_of)
    if os.environ.get('D368_MUTANT') != 'stored-direction':
        def supporters_first(connection, view_id):      # D368: the supported question depends, for judging, on the questions that support it
            return [{'dependency_id': None, 'view_id': view_id, 'depends_on': supporting, 'resolved_to': supporting, 'resolution': 'direct', 'direction': direction,
                     'wait_chain_view_id': None, 'wait_year': None} for supporting, supported, direction in edges if supported == view_id]
        store.dependencies_of = supporters_first
        store.dependants_of = lambda connection, view_id: sorted({supported for supporting, supported, _ in edges if supporting == view_id})
    calls = []

    def fake_judge(provider, request):
        user = request['messages'][-1]['content']
        view = re.match(r'Thesis (v\d+) ', user).group(1)
        block = user.split('[Current conclusions of the theses it depends on]', 1)[1].split('\n[', 1)[0] if '[Current conclusions of the theses it depends on]' in user else ''
        shown = re.findall(r'^- (v\d+) \(', block, re.M)
        fresh = [dep for dep in shown if re.search(rf'^- {dep} \([^\n]*LABELLED FAKE OUTPUT of round {round_seq}', block, re.M)]
        calls.append({'view': view, 'dependencies_shown': shown, 'shown_with_this_round_conclusion': fresh})
        state = store.current_state(sqlite3.connect(f"file:{work / 'views.sqlite'}?mode=ro", uri=True), view) if False else None
        rung = int(re.search(r'now rung (\d+)', user).group(1)) if False else 1
        answer = {'rung': current_rung[view], 'reference': f'LABELLED FAKE OUTPUT of round {round_seq} for {view}', 'implied_outcome': f'LABELLED FAKE OUTPUT of round {round_seq} for {view}',
                  'reasons': f'LABELLED FAKE OUTPUT of round {round_seq} for {view}: the ordering proof, not a model answer.', 'cites': [], 'cites_views': [], 'pushes': [],
                  'changed': True, 'why_changed': 'labelled fake output: marked changed so that the round queues what depends on it', 'theme_pushes': []}
        return {'choices': [{'message': {'content': json.dumps(answer)}}], 'usage': {'prompt_tokens': 0, 'completion_tokens': 0}, 'synthetic': True}

    current_rung = {view: (store.current_state(conn, view) or {'rung': 1})['rung'] for view in views}
    try:
        judged = judging.round_of_judgements(archive, cfg, conn, [START], round_seq, {'input_id': 'day:ordering-proof', 'publication_day': '2026-07-15'}, transport=fake_judge)
        conn.commit()
    finally:
        store.dependencies_of, store.dependants_of = originals
    filing_after = {view: store.direct_parents(conn, view) for view in views}
    written = [(row[0], row[1]) for row in conn.execute('select judgement_id, view_id from judgements where seq = ? order by judgement_id', (round_seq,))]
    order = [call['view'] for call in calls]
    by_view = {call['view']: call for call in calls}
    expectations = {
        'the chain is judged supporters first: v6, then v2, then v1, and nothing else': order == CHAIN and [view for _, view in written] == CHAIN,
        'the first supporter is not shown the question it supports': 'v2' not in by_view.get('v6', {}).get('dependencies_shown', ['v2']),
        'data-center revenue is shown its supporter\'s conclusion of this round': 'v6' in by_view.get('v2', {}).get('shown_with_this_round_conclusion', []),
        'total revenue is shown data-center revenue\'s conclusion of this round': 'v2' in by_view.get('v1', {}).get('shown_with_this_round_conclusion', []),
        'no question is shown a conclusion of a question it supports (no circle)': all(not any((call['view'], dep) in {(s, t) for s, t, _ in edges} for dep in call['dependencies_shown']) for call in calls),
        'the filing use of the edges is unchanged': filing_before == filing_after,
        'a changed conclusion queued exactly the questions it supports': len(judged) == len(CHAIN),
    }
    print(f"round {round_seq}: calls in order {order}; judgements written {written}")
    for call in calls:
        print(f"   {call['view']}: shown the conclusions of {call['dependencies_shown']}; of this round: {call['shown_with_this_round_conclusion']}")
    for name, held in expectations.items():
        print(f"  {'ok  ' if held else 'FAIL'} {name}")
    if not all(expectations.values()):
        raise SystemExit(1)
    print('PASS: every registered expectation holds (labelled fake outputs; the stored direction is untouched in every file)')


if __name__ == '__main__':
    main()
