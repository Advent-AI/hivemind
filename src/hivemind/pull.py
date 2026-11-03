"""Pull mode (D54, D356): at the end of a day (the day passed in, never read from a clock), every open view whose due day has come
is frozen where its state stands and closed. The closing record names the rung it froze at; a view that was never judged closes
with "no data to verify" (AGENTS §8: missing data is neither a pass nor a fail). Nothing waits for the day's items, there is no
separate final review, and no other question is re-judged here."""
from . import dispatch
from .views import store

NO_DATA = 'no data to verify'


def closing_reason(conn, view_id, due_day, day):
    last = conn.execute('select rung from judgements where view_id=? order by seq desc, judgement_id desc limit 1', (view_id,)).fetchone()
    if last is None:
        return f'due {due_day}, closed on {day} with no judgement: {NO_DATA}'
    label = conn.execute('select label from rungs where view_id=? and position=?', (view_id, last['rung'])).fetchone()
    return f'due {due_day}, frozen on {day} at rung {last["rung"]} {label["label"] if label else ""}'.rstrip()


def closing_sequence(conn, day, seq):
    """The sequence number the day's closings are written under, so that they are dated on that day: the day's last number when
    the day wrote it, else a new one recorded as the day's own step (a day with no items would otherwise date them on the day before)."""
    row = conn.execute('select min(publication_day) from processing_steps where sequence_no=?', (seq,)).fetchone()
    if seq > 0 and row[0] == day:
        return seq
    own = max(store.next_sequence(conn), seq + 1)
    dispatch.mark(conn, {'input_id': f'day:{day}', 'publication_day': day}, own, 'closed', 'ok', 'due questions closed at the end of the day')
    return own


def end_of_day(conn, day, seq):
    due = [row for row in conn.execute('select view_id, due_day from views where due_day <= ? order by created_seq', (day,)).fetchall()
           if store.is_open(conn, row['view_id'])]
    if due:
        seq = closing_sequence(conn, day, seq)
    for row in due:
        store.close_view(conn, row['view_id'], closing_reason(conn, row['view_id'], row['due_day'], day), 'pull', seq)
    conn.commit()
    return [row['view_id'] for row in due]
