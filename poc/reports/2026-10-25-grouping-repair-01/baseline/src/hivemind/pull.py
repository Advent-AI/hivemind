"""Pull mode, the part D54 decided: at the end of a day (the day passed in, never read from a clock), every open
view whose due day has come is frozen where its state stands and closed. Nothing waits for the day's items."""
import time

from .views import store


def end_of_day(conn, day, seq):
    closed = []
    for row in conn.execute('select view_id, due_day from views where due_day <= ? order by created_seq', (day,)):
        if store.is_open(conn, row['view_id']):
            store.close_view(conn, row['view_id'], f'due {row["due_day"]}, frozen on {day}', 'pull', seq)
            closed.append(row['view_id'])
    conn.commit()
    return closed
