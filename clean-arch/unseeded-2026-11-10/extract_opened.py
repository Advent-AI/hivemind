"""List every thesis an unseeded clean draw opened by itself, for the matching read (MATCHING-v2.md): run, id, the article (its
position in the first manifest) where it opened, description, outcome and period. The trace may join continuation segments with '+'.

Usage: extract_opened.py <label> <trace or first+segment> <output.json>"""
import json, sqlite3, sys
from pathlib import Path


def opened(label, trace):
    out, position = [], None
    for part in trace.split('+'):
        conn = sqlite3.connect(f'file:{part}?mode=ro', uri=True)
        if position is None:
            position = {iid: n for n, iid in enumerate(json.loads(conn.execute('select manifest from run').fetchone()[0])['item_ids'], 1)}
        for input_id, before, after in conn.execute("select input_id, before_state, after_state from trace where status='complete' order by sequence"):
            before_ids = {t['id'] for t in json.loads(before)}
            out += [{'run': label, 'id': t['id'], 'article': position[input_id], 'description': t['description'], 'outcome': t['outcome'],
                     'period': t['period']} for t in json.loads(after) if t['id'] not in before_ids]
        conn.close()
    return out


if __name__ == '__main__':
    rows = opened(sys.argv[1], sys.argv[2])
    Path(sys.argv[3]).write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    print(len(rows), 'opened theses')
