"""The decisive replay of D566 ($0; CLOSING-DESIGN.md §7.3): the extension proof's completed draw judged again through the changed
loop, run on to an end day past its due days with no further articles. The judge is answered from the stored judge archive by
the request's identity; a request with no stored answer stops the run (none is expected). It checks, from the store, that each
question due by the end day closed on its own due day at its last answer, that the one due later stayed open, that no model call
was made after the last article day, and what the page shows the day before and the day of each due day.

  python3 closing_replay.py <extension proof folder> <scratch output folder> [end day] [adapter folder]

It exits with status 1 unless every check holds: every judge request answered from the archive, as many as the stored draw made;
no judgement after the last article day; every question due by the end day closed on its due day at its last answer (or "no data
to verify"), open the day before; every other question open at the end day. The adapter folder (default: the repository's
stage_b) lets a mutant copy be run against it.
"""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
ADAPTER = Path(sys.argv[4]) if len(sys.argv) > 4 else ROOT / 'clean-arch/step4-2026-11-10/stage_b'
sys.path[:0] = [str(ADAPTER), str(ROOT / 'clean-arch/e2e-2026-11-09'), str(ROOT / 'src')]
import ladder_adapter  # noqa: E402
from hivemind import model, service  # noqa: E402


def main(proof, output, end_day='2027-04-02', adapter_folder=None):
    draw = Path(proof) / 'week/c1'
    stored = sqlite3.connect(f"file:{draw / 'judge/draw-c1/archive.sqlite'}?mode=ro", uri=True)
    answers = {sha: json.loads(response) for sha, response in stored.execute('select request_sha256, response_json from model_calls where response_json is not null')}
    stored_calls = stored.execute("select count(*) from model_calls where purpose='judge' and answer_json is not null").fetchone()[0]
    calls = []

    def from_the_archive(provider, request):
        sha = model.request_identity(request)[1]
        calls.append(sha)
        if sha not in answers:
            raise SystemExit(f'a judge request with no stored answer: {sha[:16]}')
        return answers[sha]

    output = Path(output)
    inputs = {'trace': str(draw / 'step1/trace.sqlite'), 'step2': str(draw / 'step2'), 'ladders': str(draw / 'ladder/send-1/outcomes.jsonl'),
              'ladder_archive': str(draw / 'ladder/send-1/archive.sqlite'), 'cases': str(draw / 'cases/cases.json'), 'output_root': str(output.parent)}
    runner = ladder_adapter.replay('c1', output, transport=from_the_archive, cap_usd=5.0, inputs=inputs, end_day=end_day)
    page = sqlite3.connect(output / 'views.sqlite')
    page.row_factory = sqlite3.Row
    last_article_day = max(day for day, in page.execute('select publication_day from processing_steps where step = ?', ('handed_over',)))
    days = service.seq_day_map(page)
    print(f'calls answered from the archive {len(calls)}; judgements {page.execute("select count(*) from judgements").fetchone()[0]}; '
          f'days completed {page.execute("select count(*) from days_completed").fetchone()[0]} (last {page.execute("select max(day) from days_completed").fetchone()[0]}); '
          f'last article day {last_article_day}; counts: closed {runner.counts["questions closed at their due day"]}')
    late = page.execute('select count(*) from judgements where publication_day > ?', (last_article_day,)).fetchone()[0]
    print(f'judgements after the last article day: {late}')
    failures = 0
    for view in page.execute('select view_id, due_day from views order by created_seq'):
        last = page.execute('select rung from judgements where view_id=? order by seq desc, judgement_id desc limit 1', (view['view_id'],)).fetchone()
        closing = page.execute('select reason, after_seq from view_switches where view_id=? and open=0', (view['view_id'],)).fetchone()
        if view['due_day'] <= end_day:
            ok = (closing is not None and days[closing['after_seq']] == view['due_day']
                  and (f'at rung {last["rung"]} ' in closing['reason'] + ' ' if last else 'no data to verify' in closing['reason'])
                  and service.is_open_as_of(page, view['view_id'], (__import__('datetime').date.fromisoformat(view['due_day']) - __import__('datetime').timedelta(days=1)).isoformat())
                  and not service.is_open_as_of(page, view['view_id'], view['due_day']))
        else:
            ok = closing is None and service.is_open_as_of(page, view['view_id'], end_day)
        failures += not ok
        print(f"  {'ok ' if ok else 'BAD'} {view['view_id']} due {view['due_day']}: "
              + (f"closed on {days[closing['after_seq']]}: {closing['reason']}" if closing else 'open at the end day'))
    due_by_end = page.execute('select count(*) from views where due_day <= ?', (end_day,)).fetchone()[0]
    counts_hold = len(calls) == stored_calls and runner.counts['questions closed at their due day'] == due_by_end
    print(f'calls {len(calls)} against the stored {stored_calls}; closed {runner.counts["questions closed at their due day"]} against due by the end day {due_by_end}')
    good = failures == 0 and late == 0 and counts_hold
    print('all as expected' if good else 'NOT AS EXPECTED')
    if not good:
        raise SystemExit(1)


if __name__ == '__main__':
    main(*sys.argv[1:])
