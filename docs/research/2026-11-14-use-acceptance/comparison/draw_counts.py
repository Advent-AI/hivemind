"""The comparison's sizing, step 1 ($0; D516): what each stored draw of each system holds, counted by code. Read-only on finished runs.

For every stored draw named below it prints the questions opened, the statements stored, how many have no question, the links, the share
of links on the largest question, the judgements and the questions with a last judgement; for production also the statements its
handover log records as dropped, where the store keeps them. It writes `draw-counts.json`. It judges nothing: these are the counts a
reader-free line can use, and the spread between draws of one system that a comparison has to beat.

  python3 draw_counts.py
"""
import json
import sqlite3
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).resolve().parent
DRAWS = {
    'July window, 14 days (2026-07-01..14), full run of 2026-11-13': {
        'new c1': 'poc/data/clean-e2e-full-2026-11-13/c1/judge/draw-c1/views.sqlite',
        'new c2': 'poc/data/clean-e2e-full-2026-11-13/c2/judge/draw-c2/views.sqlite',
        'new c3': 'poc/data/clean-e2e-full-2026-11-13/c3/judge/draw-c3/views.sqlite',
        'old p1': 'poc/data/clean-e2e-full-2026-11-13/p1/prod/views.sqlite',
        'old p2': 'poc/data/clean-e2e-full-2026-11-13/p2/prod/views.sqlite',
        'old p3': 'poc/data/clean-e2e-full-2026-11-13/p3/prod/views.sqlite'},
    'Fresh week, 7 days (2026-09-22..28), lean step 2 of 2026-11-14': {
        'new c1': 'poc/data/clean-lean-week-2026-11-14/week-r2/c1/judge/draw-c1/views.sqlite',
        'old p1': 'poc/data/clean-lean-week-2026-11-14/week/p1/prod/views.sqlite'},
}


def counts(path):
    db = sqlite3.connect(f'file:{ROOT / path}?mode=ro', uri=True)
    one = lambda sql: db.execute(sql).fetchone()[0]
    links = one('select count(*) from evidence_links')
    largest = db.execute('select count(*) c from evidence_links group by view_id order by c desc limit 1').fetchone()
    tables = {name for (name,) in db.execute("select name from sqlite_master where type = 'table'")}
    dropped = None
    if 'handovers' in tables:
        columns = [d[1] for d in db.execute('pragma table_info("handovers")')]
        if 'dropped_json' in columns:
            dropped = sum(len(json.loads(value or '[]')) for (value,) in db.execute('select dropped_json from handovers'))
    return {'questions': one('select count(*) from views'), 'statements stored': one('select count(*) from evidence'),
            'with no question': one('select count(*) from evidence where evidence_id not in (select evidence_id from evidence_links)'),
            'links': links, 'links on the largest question': largest[0] if largest else 0,
            'share of links on the largest question': round(largest[0] / links, 2) if links else None,
            'judgements': one('select count(*) from judgements'), 'questions with a last judgement': one('select count(distinct view_id) from judgements'),
            'statements recorded as dropped': dropped}


def main():
    out = {}
    for window, draws in DRAWS.items():
        print(window)
        out[window] = {}
        for name, path in draws.items():
            if not (ROOT / path).exists():
                print(f'  {name}: store not found at {path}')
                continue
            out[window][name] = counts(path)
            print(f'  {name}: ' + '; '.join(f'{key} {value}' for key, value in out[window][name].items()))
    (HERE / 'draw-counts.json').write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
