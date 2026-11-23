"""The whole judging round of 2026-07-14 in D368's direction, dry, with labelled fake outputs ($0; D535, before any measurement design).

Starts from the rebuilt and verified state of 2026-07-14 before that day's round (`rebuild_seeded_state.py`), copies it, and runs the
production day round (`round.judge_day`) with the edges read in D368's direction for the judging use only, as `ordering_proof.py`
does. Every judgement output is a labelled fake. Two runs bound the number of calls: no fake conclusion says it changed (unless a
first judgement must), and every fake conclusion says it changed. The script exits with an error if a registered expectation fails.

  python3 full_day_dry_run.py <verified state folder> <scratch folder>      (D368_MUTANT=stored-direction: must fail)
"""
import json
import os
import re
import shutil
import sys
import threading
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, model  # noqa: E402
from hivemind.views import round as rounds, store  # noqa: E402

DAY = '2026-07-14'
BLOCK = '[Current conclusions of the theses it depends on]'


def one_run(state, work, every_conclusion_changes):
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(state, work)
    cfg = config.load(str(ROOT / 'poc/config/poc-v108.json'))
    conn, archive = store.open_db(str(work / 'views.sqlite')), model.Archive(str(work / 'archive.sqlite'))
    edges = [(row[0], row[1], row[2]) for row in conn.execute("select d.view_id, coalesce((select r.resolved_to from dependency_resolutions r where r.dependency_id = d.dependency_id order by r.id desc limit 1), d.depends_on), d.direction from dependencies d")]
    edges = [(supporting, supported, direction) for supporting, supported, direction in edges if supported]
    views = [row[0] for row in conn.execute('select view_id from views')]
    filing_before = {view: store.direct_parents(conn, view) for view in views}
    current = {view: store.current_state(conn, view) for view in views}
    seq = store.next_sequence(conn) - 1
    changed_today = sorted(rounds.changed_views_of_day(conn, DAY))
    originals = (store.dependencies_of, store.dependants_of)
    if os.environ.get('D368_MUTANT') != 'stored-direction':
        store.dependencies_of = lambda connection, view_id: [
            {'dependency_id': None, 'view_id': view_id, 'depends_on': supporting, 'resolved_to': supporting, 'resolution': 'direct', 'direction': direction,
             'wait_chain_view_id': None, 'wait_year': None} for supporting, supported, direction in edges if supported == view_id]
        store.dependants_of = lambda connection, view_id: sorted({supported for supporting, supported, _ in edges if supporting == view_id})
    calls, lock = [], threading.Lock()

    def fake_judge(provider, request):
        user = request['messages'][-1]['content']
        view = re.match(r'Thesis (v\d+) ', user).group(1)
        block = user.split(BLOCK, 1)[1].split('\n[', 1)[0] if BLOCK in user else ''
        shown = re.findall(r'^- (v\d+) \(', block, re.M)
        fresh = [dep for dep in shown if re.search(rf'^- {dep} \([^\n]*LABELLED FAKE OUTPUT of round {seq}', block, re.M)]
        with lock:
            calls.append({'view': view, 'dependencies_shown': shown, 'shown_with_this_round_conclusion': fresh, 'request_characters': sum(len(m['content']) for m in request['messages'])})
        first = current[view] is None
        label = f'LABELLED FAKE OUTPUT of round {seq} for {view}'
        answer = {'rung': 1 if first else current[view]['rung'], 'reference': label, 'implied_outcome': label, 'reasons': label + ': the dry run, not a model answer.', 'cites': [],
                  'cites_views': shown,           # every conclusion shown is cited: the judge's own check must accept a citation of a supporter
                  'pushes': [], 'changed': bool(first or every_conclusion_changes), 'why_changed': 'labelled fake output' if (first or every_conclusion_changes) else '', 'theme_pushes': []}
        return {'choices': [{'message': {'content': json.dumps(answer)}}], 'usage': {'prompt_tokens': 0, 'completion_tokens': 0}, 'synthetic': True}

    try:
        result = rounds.judge_day(conn, archive, cfg, DAY, seq, transport=fake_judge, log=lambda *parts: None)
        conn.commit()
    finally:
        store.dependencies_of, store.dependants_of = originals
    order = [row[0] for row in conn.execute('select view_id from judgements where seq = ? order by judgement_id', (seq,))]
    position = {view: index for index, view in enumerate(order)}
    by_view = {call['view']: call for call in calls}
    pairs = [(supporting, supported) for supporting, supported, _ in edges if supporting in position and supported in position]
    edge_set = {(supporting, supported) for supporting, supported, _ in edges}
    expectations = {
        'the round finished without a refusal': not result.failed,
        'every judgement of the round is a labelled fake (none answered from the stored archive)': sorted(by_view) == sorted(order),
        'every question whose reading changed that day and that can be judged was judged': all(view in position for view in changed_today if store.is_open(conn, view) and store.evidence_in_force(conn, view)),
        f'every supporting question is judged before the question it supports ({len(pairs)} pairs both judged)': bool(pairs) and all(position[a] < position[b] for a, b in pairs),
        'every supported question is shown this round\'s conclusion of each supporter judged this round': bool(pairs) and all(a in by_view.get(b, {}).get('shown_with_this_round_conclusion', []) for a, b in pairs),
        'no question is shown the conclusion of a question it supports': all((call['view'], dep) not in edge_set for call in calls for dep in call['dependencies_shown']),
        'the filing use of the edges is unchanged': filing_before == {view: store.direct_parents(conn, view) for view in views},
    }
    conn.close()
    return {'changed_today': changed_today, 'order': order, 'calls': len(calls), 'request_characters': sum(call['request_characters'] for call in calls), 'pairs': pairs, 'expectations': expectations,
            'shown': {call['view']: call['dependencies_shown'] for call in calls if call['dependencies_shown']}}


def main():
    state, scratch = Path(sys.argv[1]), Path(sys.argv[2])
    failed = False
    summary = {}
    for name, every in (('fewest calls: no fake conclusion says it changed', False), ('most calls: every fake conclusion says it changed', True)):
        run = one_run(state, scratch / ('all-changed' if every else 'none-changed'), every)
        summary[name] = {key: run[key] for key in ('changed_today', 'order', 'calls', 'request_characters', 'pairs', 'shown')}
        print(f"\n{name}\n  questions whose reading changed on {DAY}: {len(run['changed_today'])} {run['changed_today']}\n  judged, in order ({run['calls']} calls, {run['request_characters']:,} request characters): {run['order']}")
        print(f"  supporting -> supported pairs both judged: {run['pairs']}")
        for held_name, held in run['expectations'].items():
            print(f"  {'ok  ' if held else 'FAIL'} {held_name}")
            failed = failed or not held
    (Path(__file__).parent / 'full-day-dry-run.json').write_text(json.dumps(summary, indent=1) + '\n') if not os.environ.get('D368_MUTANT') else None
    if failed:
        raise SystemExit(1)
    print('\nPASS: every registered expectation holds in both runs (labelled fake outputs; no model call; no package or frozen file changed)')


if __name__ == '__main__':
    main()
