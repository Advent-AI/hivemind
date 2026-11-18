"""Continue a clean draw whose first step was cut with a call in flight (D551): the second part's inputs, and the two parts
merged into one trace of the form an unbroken run writes. It reads only traces of runs that are no longer live, decides nothing
about the articles, and refuses anything outside the one case it was written for: a first part whose complete articles are the
manifest's first articles in order, followed by at most one row, the call in flight when the run was cut.

  python3 continuation.py inputs <first part's step1 folder> <second part folder> <calls used so far> <seconds used so far>
  python3 continuation.py merge <first part's trace> <second part's trace> <merged trace>
"""
import json
import shutil
import sqlite3
import sys
from pathlib import Path

TRACE_COLUMNS = ['sequence', 'input_id', 'before_state', 'request', 'raw_response', 'result', 'after_state', 'status', 'error',
                 'reserved_usd', 'retry_reason']


class Refused(Exception):
    """The parts are not the one case this tool continues."""


def read_part(trace_path):
    """A part's run row and trace rows (as dicts, in order)."""
    conn = sqlite3.connect(f'file:{trace_path}?mode=ro', uri=True)
    try:
        manifest, settings, source_items, initial = conn.execute('select manifest, settings, source_items, initial_theses from run').fetchone()
        rows = [dict(zip(TRACE_COLUMNS, row)) for row in conn.execute(f"select {', '.join(TRACE_COLUMNS)} from trace order by sequence")]
    finally:
        conn.close()
    return {'manifest': json.loads(manifest), 'settings': json.loads(settings), 'source_items': json.loads(source_items),
            'initial': json.loads(initial), 'rows': rows}


def first_part(trace_path):
    """The first part, checked: (part, number of complete articles, the cut row or None)."""
    part = read_part(trace_path)
    complete = [row for row in part['rows'] if row['status'] == 'complete']
    others = [row for row in part['rows'] if row['status'] != 'complete']
    ids = part['manifest']['item_ids']
    if not complete:
        raise Refused('the first part completed no article')
    if [row['sequence'] for row in complete] != list(range(1, len(complete) + 1)) or [row['input_id'] for row in complete] != ids[:len(complete)]:
        raise Refused('the complete articles are not the first articles of the manifest in order')
    if len(others) > 1:
        raise Refused(f'{len(others)} rows are not complete: only one call in flight is continued')
    cut = others[0] if others else None
    if cut is not None and (cut['status'] != 'in_flight' or cut['sequence'] != len(complete) + 1 or cut['input_id'] != ids[len(complete)]
                            or cut['raw_response'] is not None or cut['after_state'] is not None):
        raise Refused(f"the row after the complete articles is not a call cut in flight (status {cut['status']})")
    if len(complete) == len(ids):
        raise Refused('the first part is complete: nothing to continue')
    return part, len(complete), cut


def write_inputs(first_folder, second_folder, calls_used, seconds_used):
    """The second part's manifest, starting library, settings and limits. The limits are the first part's less what it used: the
    calls it reserved (the cut one among them) and the seconds its clock ran before the cut."""
    first_folder, second_folder = Path(first_folder), Path(second_folder)
    part, completed, cut = first_part(first_folder / 'trace.sqlite')
    remaining = part['manifest']['item_ids'][completed:]
    state = json.loads(part['rows'][completed - 1]['after_state'])
    limits = json.loads((first_folder / 'limits.json').read_text())
    limits['max_calls'] = limits['max_calls'] - int(calls_used)
    limits['max_seconds'] = limits['max_seconds'] - int(seconds_used)
    if limits['max_calls'] < len(remaining) or limits['max_seconds'] <= 0:
        raise Refused(f"the limits left ({limits['max_calls']} calls, {limits['max_seconds']} seconds) cannot cover {len(remaining)} articles")
    second_folder.mkdir(parents=True)
    (second_folder / 'manifest.json').write_text(json.dumps(dict(part['manifest'], item_ids=remaining, item_limit=len(remaining)), indent=1))
    (second_folder / 'initial.json').write_text(json.dumps(state, ensure_ascii=False, indent=1))
    shutil.copy(first_folder / 'settings.json', second_folder / 'settings.json')
    (second_folder / 'limits.json').write_text(json.dumps(limits, indent=1))
    record = {'continues': str(first_folder / 'trace.sqlite'), 'complete_articles': completed, 'state_after': part['rows'][completed - 1]['input_id'],
              'cut_call': cut['input_id'] if cut else None, 'remaining_articles': len(remaining), 'calls_used': int(calls_used),
              'seconds_used': int(seconds_used), 'reason': 'the machine slept with a call in flight; the call was never answered (D551)'}
    (second_folder / 'continuation.json').write_text(json.dumps(record, indent=1))
    return record


def check_second_part(rows, remaining_ids, state):
    """The second part's trace must be a finished run of every remaining article: each article once and in order; each row complete,
    or the one failure the runner itself goes on after (an answer that failed the format check twice); the library carried from
    each article to the next without a break, starting from `state`. Anything else (a part that stopped, a call still in flight,
    rows missing or out of order) is refused: such a part is not merged and nothing later runs on it."""
    if [row['sequence'] for row in rows] != list(range(1, len(rows) + 1)):
        raise Refused("the second part's rows are not numbered in order")
    if [row['input_id'] for row in rows] != list(remaining_ids):
        raise Refused(f"the second part's trace does not hold every remaining article once and in order ({len(rows)} rows for {len(remaining_ids)} articles)")
    library = state
    for row in rows:
        went_on = row['status'] == 'failed' and str(row['error'] or '').startswith('FormatFailure')
        if row['status'] != 'complete' and not went_on:
            raise Refused(f"article {row['sequence']} of the second part is {row['status']}, not complete: {str(row['error'])[:80]}")
        if json.loads(row['before_state']) != library or row['after_state'] is None:
            raise Refused(f"the library is not carried unbroken into article {row['sequence']} of the second part")
        library = json.loads(row['after_state'])


def check_whole(trace_path):
    """A trace that may stand as a draw's completed first step: every article of its manifest once and in order, each complete (or
    the one failure the runner goes on after), the library carried unbroken from the starting library. Returns the number of
    articles; refuses anything else."""
    part = read_part(trace_path)
    check_second_part(part['rows'], part['manifest']['item_ids'], part['initial'])
    return len(part['rows'])


def merge(first_trace, second_trace, output):
    """One trace from the two parts: the first part's complete articles, then the second part's articles renumbered after them.
    Refuses unless the second part starts exactly where the first stopped and is itself finished: the same settings (the limits
    apart, which the second part has less of), the remaining articles in order with the same stored text, the library as it
    stood after the first part's last complete article, and a trace that holds every remaining article (`check_second_part`). The merged run row is the first part's. The column of running reservations goes on from
    the first part's last figure, the cut call's reservation included, since that call was reserved and may have been charged."""
    part, completed, cut = first_part(first_trace)
    second = read_part(second_trace)
    state = json.loads(part['rows'][completed - 1]['after_state'])
    without_limits = lambda settings: {key: value for key, value in settings.items() if key != 'live_limits'}
    if without_limits(second['settings']) != without_limits(part['settings']):
        raise Refused('the two parts ran with different settings')
    if second['manifest']['item_ids'] != part['manifest']['item_ids'][completed:]:
        raise Refused("the second part's articles are not the first part's remaining articles in order")
    if second['source_items'] != part['source_items'][completed:]:
        raise Refused("the second part read different article records than the first part stored for the same articles")
    if second['initial'] != state:
        raise Refused("the second part did not start from the library after the first part's last complete article")
    check_second_part(second['rows'], part['manifest']['item_ids'][completed:], state)
    output = Path(output)
    if output.exists():
        raise Refused(f'{output} exists')
    shutil.copy(first_trace, output)
    conn = sqlite3.connect(output)
    try:
        with conn:
            conn.execute("delete from trace where status != 'complete'")
            conn.execute('attach database ? as second', (f'file:{second_trace}?mode=ro',))
            columns = ', '.join(TRACE_COLUMNS[1:])
            reserved_before = (cut or part['rows'][completed - 1])['reserved_usd'] or 0.0
            selected = columns.replace('reserved_usd', 'reserved_usd + ?')
            conn.execute(f'insert into trace (sequence, {columns}) select sequence + ?, {selected} from second.trace order by sequence',
                         (completed, reserved_before))
            call_columns = ', '.join(row[1] for row in conn.execute('pragma table_info(model_calls)') if row[1] != 'call_id')
            conn.execute(f'insert into model_calls ({call_columns}) select {call_columns} from second.model_calls order by call_id')
        conn.execute('detach database second')
    finally:
        conn.close()
    return {'complete_articles_of_the_first_part': completed, 'articles_of_the_second_part': len(second['rows']), 'merged': str(output)}


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'inputs':
            print(json.dumps(write_inputs(*sys.argv[2:6]), indent=1))
        elif sys.argv[1] == 'merge':
            print(json.dumps(merge(*sys.argv[2:5]), indent=1))
        else:
            raise SystemExit(__doc__)
    except Refused as refusal:
        raise SystemExit(f'refused: {refusal}')
