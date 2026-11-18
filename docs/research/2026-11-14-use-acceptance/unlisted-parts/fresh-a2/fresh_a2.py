"""FRESH-A2-DESIGN.md v4's reading of a first-step trace ($0): the topics a run opened beyond its starting library, each with the
article that opened it, and whether the run is complete. Only completed articles count; a run with any article not complete, or
with fewer articles than its manifest, is incomplete and gives no verdict."""
import json
import sqlite3


def read_trace(path):
    connection = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True)
    connection.row_factory = sqlite3.Row
    try:
        run = connection.execute('select * from run').fetchone()
        rows = [dict(row) for row in connection.execute('select * from trace order by sequence')]
        return {name: json.loads(run[name]) for name in ('manifest', 'settings', 'source_items', 'initial_theses')}, rows
    finally:
        connection.close()


def opened_topics(trace_path):
    """Returns (topics, complete, articles completed, articles in the manifest). A topic is a thesis in an article's library after
    that is in neither its library before nor the starting library; its opening article is that row's."""
    run, rows = read_trace(trace_path)
    starting = {thesis['id'] for thesis in run['initial_theses']}
    total = len(run['manifest']['item_ids'])
    done = [row for row in rows if row['status'] == 'complete']
    complete = len(done) == len(rows) == total
    topics = []
    for row in done:
        before = {thesis['id'] for thesis in json.loads(row['before_state'] or '[]')}
        for thesis in json.loads(row['after_state'] or '[]'):
            if thesis['id'] not in before and thesis['id'] not in starting:
                topics.append({'thesis': thesis, 'opening_article': row['input_id'], 'sequence': row['sequence']})
    return topics, complete, len(done), total
