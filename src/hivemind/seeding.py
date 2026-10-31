"""Seed questions (D208 step one, D253): a covered company's root quantities and driver questions written before a run, so that evidence
about them has a home from the first day. `seed_views` writes a seed file's questions into a ledger that holds none of them yet: the view,
its ladder, its key (so an article-born candidate for the same quantity merges into it and the placer's 'takes' line reads as for any
keyed question), an open switch, and the driver's dependency on the root it feeds. A view id already present is left as it is, so a
resumed run seeds nothing twice. Seeds are created at seq 0, before any item, from the input 'seed:<file name>'.

Seed file: {"company": "NVDA", "as_of": "2026-07-01", "questions": [{"view_id": "s1", "object_id": "NVDA", "object_kind": "company",
"kind": "asset", "looks_at": ..., "question": ..., "due_day": ..., "year": ..., "rungs": [...], "key": {...}, "depends_on": "s1" | null,
"ladder_status": "copied from run ... | draft, analyst to confirm"}]}"""
import json
from pathlib import Path

from .views import store


def seed_views(conn, seed_path, created_at):
    """Returns the ids written. Refuses a seed whose view id exists with a different question (a changed seed file is a new file)."""
    seed = json.loads(Path(seed_path).read_text(encoding='utf-8'))
    written = []
    source = f'seed:{Path(seed_path).name}'
    for q in seed['questions']:
        existing = conn.execute('select question from views where view_id=?', (q['view_id'],)).fetchone()
        if existing:
            if existing['question'] != q['question']:
                raise ValueError(f'seed {q["view_id"]} exists with another question; a changed seed is a new file')
            continue
        store.create_view(conn, view_id=q['view_id'], object_id=q['object_id'], object_kind=q['object_kind'], kind=q['kind'], looks_at=q['looks_at'],
                          question=q['question'], due_day=q['due_day'], year=q['year'], rungs=q['rungs'], seq=0, input_id=source, created_at=created_at)
        if q.get('key'):
            store.add_key(conn, q['view_id'], dict(q['key'], key_version=2), 0)
        if q.get('depends_on'):
            store.insert(conn, 'dependencies', view_id=q['view_id'], depends_on=q['depends_on'], wait_chain_view_id='', wait_year='', direction='last_end', seq=0)
        written.append(q['view_id'])
    conn.commit()
    return written
