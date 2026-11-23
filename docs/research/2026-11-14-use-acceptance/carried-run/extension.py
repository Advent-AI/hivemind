"""Extend a completed first-step run by a following one (D563): the second run's inputs, and the two runs joined into one trace
of the form an unbroken run over both writes. Unlike `second-week/continuation.py` (a run cut with a call in flight), the first
run here is complete and the second reads articles of later days, starting from the first run's last library. It reads only
traces of runs that are no longer live and decides nothing about the articles.

  python3 extension.py inputs <first run's step1 folder> <next manifest> <second run folder> <limits json>
  python3 extension.py join <first trace> <second trace> <joined trace>
"""
import json
import shutil
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'second-week'))
import continuation  # noqa: E402
from continuation import Refused, read_part  # noqa: E402

TRACE_COLUMNS = continuation.TRACE_COLUMNS


def last_library(part):
    return json.loads(part['rows'][-1]['after_state'])


def days_of(part):
    return [item['publication_day'] for item in part['source_items']]


def check_complete(part):
    """A finished run: every article of its manifest once and in order, the library carried unbroken (continuation's own check)."""
    continuation.check_second_part(part['rows'], part['manifest']['item_ids'], part['initial'])


def write_inputs(first_folder, next_manifest, second_folder, limits):
    """The second run's manifest, starting library (the first run's last library), settings (the first run's) and limits."""
    first_folder, second_folder = Path(first_folder), Path(second_folder)
    first = read_part(first_folder / 'trace.sqlite')
    check_complete(first)
    manifest = json.loads(Path(next_manifest).read_text())
    if set(manifest['item_ids']) & set(first['manifest']['item_ids']):
        raise Refused('the next manifest repeats articles of the first run')
    if manifest['entity'] != first['manifest']['entity'] or manifest['from_day'] < first['manifest']['until_day']:
        raise Refused('the next manifest is not a later window of the same company')
    second_folder.mkdir(parents=True)
    (second_folder / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    (second_folder / 'initial.json').write_text(json.dumps(last_library(first), ensure_ascii=False, indent=1))
    settings = {key: value for key, value in first['settings'].items() if key != 'live_limits'}
    (second_folder / 'settings.json').write_text(json.dumps(settings, indent=1))
    (second_folder / 'limits.json').write_text(json.dumps(limits, indent=1))
    record = {'extends': str(first_folder / 'trace.sqlite'), 'first_articles': len(first['rows']), 'library_after': first['rows'][-1]['input_id'],
              'library_topics': [topic['id'] for topic in last_library(first)], 'next_articles': len(manifest['item_ids'])}
    (second_folder / 'extension.json').write_text(json.dumps(record, indent=1))
    return record


def join(first_trace, second_trace, output):
    """One trace from the two runs: the first run's rows, then the second's renumbered after them; the run row's manifest and
    articles are the two joined, its starting library the first run's. Refuses unless both runs are finished, they ran with the
    same settings (limits apart), the second started from the first's last library, no article is read twice and the days do not
    go back. The running reservations of the second run continue the first's last figure, as one run's would."""
    first, second = read_part(first_trace), read_part(second_trace)
    check_complete(first)
    check_complete(second)
    without_limits = lambda settings: {key: value for key, value in settings.items() if key != 'live_limits'}
    if without_limits(first['settings']) != without_limits(second['settings']):
        raise Refused('the two runs ran with different settings')
    if second['initial'] != last_library(first):
        raise Refused("the second run did not start from the first run's last library")
    ids = first['manifest']['item_ids'] + second['manifest']['item_ids']
    if len(ids) != len(set(ids)):
        raise Refused('an article is read in both runs')
    days = days_of(first) + days_of(second)
    if days != sorted(days):
        raise Refused('the days of the joined articles go back')
    if first['manifest']['entity'] != second['manifest']['entity']:
        raise Refused('the two runs follow different companies')
    output = Path(output)
    if output.exists():
        raise Refused(f'{output} exists')
    manifest = {'entity': first['manifest']['entity'], 'from_day': first['manifest']['from_day'], 'until_day': second['manifest']['until_day'],
                'item_limit': len(ids), 'item_ids': ids}
    shutil.copy(first_trace, output)
    conn = sqlite3.connect(output)
    try:
        with conn:
            conn.execute('update run set manifest = ?, source_items = ?', (json.dumps(manifest, ensure_ascii=False),
                                                                          json.dumps(first['source_items'] + second['source_items'], ensure_ascii=False)))
            conn.execute('attach database ? as second', (f'file:{second_trace}?mode=ro',))
            columns = ', '.join(TRACE_COLUMNS[1:])
            reserved_before = first['rows'][-1]['reserved_usd'] or 0.0
            selected = columns.replace('reserved_usd', 'reserved_usd + ?')
            conn.execute(f'insert into trace (sequence, {columns}) select sequence + ?, {selected} from second.trace order by sequence',
                         (len(first['rows']), reserved_before))
            call_columns = ', '.join(row[1] for row in conn.execute('pragma table_info(model_calls)') if row[1] != 'call_id')
            conn.execute(f'insert into model_calls ({call_columns}) select {call_columns} from second.model_calls order by call_id')
        conn.execute('detach database second')
    finally:
        conn.close()
    continuation.check_whole(output)
    return {'first_articles': len(first['rows']), 'second_articles': len(second['rows']), 'joined': str(output), 'manifest': manifest}


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'inputs':
            print(json.dumps(write_inputs(sys.argv[2], sys.argv[3], sys.argv[4], json.loads(Path(sys.argv[5]).read_text())), indent=1))
        elif sys.argv[1] == 'join':
            result = join(*sys.argv[2:5])
            print(json.dumps({k: v for k, v in result.items() if k != 'manifest'}, indent=1))
        else:
            raise SystemExit(__doc__)
    except Refused as refusal:
        raise SystemExit(f'refused: {refusal}')
