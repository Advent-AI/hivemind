"""$0 mutation check of the paid harness's own checks (PAID-DESIGN.md §3; AGENTS §4): each mutant changes one thing in its own process
and must make the acceptance gate refuse the sequence (the named check false) or the sequence stop; the unmutated dry runs
(paid-dry-*.log) are the controls. `units` runs the checks that need no replay.

  python3 paid_mutants.py <scratch> <mutant name>
  python3 paid_mutants.py units
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paid_run                                                         # noqa: E402
import july_test                                                        # noqa: E402
from hivemind.views import store as views_store                         # noqa: E402

MUTANTS = {
    'control not retired': ('control', '1', 'every post-link reader judgement fresh on its own day'),
    'stale upstream recorded': ('linked', '1', 'upstream snapshot clean'),
    'swapped upstreams': ('linked', '2', 'upstream snapshot clean'),
    'a reader missing from the allow-list': ('linked', '1', 'window completed, no stop'),
    'a probe link answer missing': ('linked', '1', 'window completed, no stop'),
    'a non-reader bought': ('linked', '1', 'fixed trajectory (H2)'),
    'window cut short': ('control', '1', 'calendar completed (every day old-2 completed)'),
}


class HarnessStore:
    """Only the harness's snapshot sees a mutated state; judging keeps the real store."""

    def __init__(self, current_state):
        self.current_state = current_state

    def __getattr__(self, attribute):
        return getattr(views_store, attribute)


def run(scratch, name):
    kind, draw, check = MUTANTS[name]
    if name == 'control not retired':
        paid_run.retired_rows = lambda reader_days: {}
    elif name == 'stale upstream recorded':
        def previous_state(conn, view_id):
            rows = conn.execute('select judgement_id, rung, reasons, changed, seq, publication_day, reference, implied_outcome from judgements '
                                'where view_id=? order by judgement_id desc limit 2', (view_id,)).fetchall()
            return dict(rows[-1]) if rows else None
        paid_run.store = HarnessStore(previous_state)
    elif name == 'swapped upstreams':
        def swapped(conn, view_id):
            other = {'v9': 'v16', 'v16': 'v9'}.get(view_id, view_id)      # v21 reads v16 and v9 in draw 2: their states exchanged
            return views_store.current_state(conn, other)
        paid_run.store = HarnessStore(swapped)
    elif name == 'a reader missing from the allow-list':
        original_readers = paid_run.readers
        paid_run.readers = lambda d: {k: v for k, v in original_readers(d).items() if k != 'v21'}
    elif name == 'a probe link answer missing':
        original_probe = paid_run.window_test.probe_answers

        def fewer(d):
            answers = original_probe(d)
            answers.pop(sorted(answers)[0])
            return answers
        paid_run.window_test.probe_answers = fewer
    elif name == 'window cut short':
        paid_run.WINDOW = ('2026-07-01', '2026-09-19')                  # the replay ends a day early without raising
    elif name == 'a non-reader bought':
        original_readers = paid_run.readers
        paid_run.readers = lambda d: dict(original_readers(d), v8='2026-07-10')      # admission widened; the pinned plan is not
        original_prepare = paid_run.prepare

        def prepare(folder, kind_, draw_):
            archive, top, retired = original_prepare(folder, kind_, draw_)
            for (call_id,) in paid_run.old2().execute("select call_id from judgements where view_id='v8' and publication_day>='2026-07-10'"):
                archive.retire(call_id)
            return archive, top, retired
        paid_run.prepare = prepare
    inner = july_test.dispatcher(july_test.fake_judge(f'mutant-{name}', {}), july_test.fake_jev(set()), [])
    summary = paid_run.run_sequence(Path(scratch) / name.replace(' ', '-'), kind, draw, inner, lambda: {}, 'dry')
    caught = not summary['acceptance'][check] and not summary['acceptance']['accepted']
    print(json.dumps({'mutant': name, 'check expected to fail': check, 'caught': caught, 'stopped': summary['stopped'][:200],
                      'acceptance': summary['acceptance']}, indent=1))
    return caught


def units():
    """Checks without a replay: the latch race (July's); a request titled "Thesis v14" without the judgement schema, sent while a judging
    day is set, is not admitted; a reader judgement whose call lies in another day's window is not fresh on its own day."""
    results = {'latch race': all(july_test.latch_race().values())}
    run = paid_run.SequenceRun('linked', '1', lambda *a: {'ok': True}, Path('/nonexistent'))
    run.day = '2026-07-20'
    try:
        run.transport('openai', {'messages': [{'role': 'user', 'content': 'Thesis v14 (NVDA, asset'}], 'response_format': {}})
        results['a non-judgement request is not admitted'] = False
    except july_test.Stop:
        results['a non-judgement request is not admitted'] = run.attempts[-1]['admitted'] is False
    pinned = {'readers': {'v9': '2026-07-10'}, 'graph': [], 'probe jobs': []}
    judgement = {'view': 'v9', 'day': '2026-07-20', 'call_id': 105, 'judgement_id': 1, 'must be fresh': True,
                 'fresh on its day': 100 < 105 <= 104, 'from the archive': False}
    summary = {'stopped': '', 'terminal': {'outcome': 'complete'}, 'links committed': [], 'link jobs consumed': [],
               'reader judgements': [judgement], 'snapshot problems': [], 'snapshot checks': 1, 'trajectory (H2)': {'x': True}}
    results['a call outside its own day\'s window is not fresh'] = not paid_run.acceptance(summary, pinned, 'control')['accepted']
    print(json.dumps(results, indent=1))
    return all(results.values())


if __name__ == '__main__':
    if sys.argv[1] == 'units':
        sys.exit(0 if units() else 1)
    sys.exit(0 if run(sys.argv[1], ' '.join(sys.argv[2:])) else 1)
