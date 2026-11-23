"""Rebuild the old system's fresh-week state up to a given article from its stored answers alone ($0; D524). The stored archive is
copied to a scratch folder and the production replay (`replay.run`, serial) is run with a transport that refuses every network call:
each request must be found in the copied archive, so the run reproduces the stored one or stops. The rebuilt store is compared with
the stored run. Nothing is written to the stored run or to any package file.

  python3 rebuild_state.py <scratch folder> <last whole day, or none> <next day> <items of the next day to process>
"""
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, model, replay, universe  # noqa: E402

RUN = ROOT / 'poc/data/clean-lean-week-2026-11-14/week/p1/prod'


class Refused(RuntimeError):
    pass


def refuse(*args, **kwargs):
    raise Refused('a request was not in the stored archive: the network is refused in this rebuild')


def main():
    scratch, last_whole_day, next_day, items_of_next_day = Path(sys.argv[1]), sys.argv[2], sys.argv[3], int(sys.argv[4])
    if (scratch / 'views.sqlite').exists():
        raise SystemExit(f'{scratch} already holds a rebuilt store: refused')
    scratch.mkdir(parents=True, exist_ok=True)
    shutil.copy(RUN / 'archive.sqlite', scratch / 'archive.sqlite')
    cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    archive = model.Archive(str(scratch / 'archive.sqlite'))
    calls_before = sqlite3.connect(scratch / 'archive.sqlite').execute('select count(*) from model_calls').fetchone()[0]
    lines = []
    common = dict(testdb_path=str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'), views_path=str(scratch / 'views.sqlite'), archive=archive, cfg=cfg,
                  universe=uni, only_objects={'NVDA'}, transport=refuse, log=lambda *parts: lines.append(' '.join(str(p) for p in parts)))
    totals = replay.run(from_day='2026-09-22', until_day=last_whole_day, **common) if last_whole_day != 'none' else {'failed': 0}
    partial = None
    if items_of_next_day:
        try:        # the items are written one by one; the day's closing judgement of a part-day is not in the stored archive and is refused, as it must be
            partial = replay.run(from_day=next_day, until_day=next_day, max_items_per_day=items_of_next_day, **common)
        except RuntimeError as error:
            if 'judging failed' not in str(error) or 'Refused' not in str(error):
                raise
            partial = {'stopped at': "the part-day's closing judgement, refused (expected: it was never sent)"}
    calls_after = sqlite3.connect(scratch / 'archive.sqlite').execute('select count(*) from model_calls').fetchone()[0]
    rebuilt = sqlite3.connect(f"file:{scratch / 'views.sqlite'}?mode=ro", uri=True)
    stored = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
    top = rebuilt.execute('select max(sequence_no) from processing_steps').fetchone()[0]
    print(f'whole days to {last_whole_day}: failed {totals.get("failed")}; partial day: {partial}; '
          f'highest article processed {top}; archive rows {calls_before} -> {calls_after} (any new row would be a call that was not stored)')
    checks = {'questions (id, article, wording)': 'select view_id, created_seq, question from views where created_seq <= ? order by view_id',
              'statements (id, article, passage)': 'select evidence_id, created_seq, quote from evidence where created_seq <= ? order by evidence_id',
              'links': 'select evidence_id, view_id, seq from evidence_links where seq <= ? order by evidence_id, view_id',
              'judgements (question, article, band)': 'select view_id, seq, rung from judgements where seq <= ? order by view_id, seq',
              'group members': 'select group_id, view_id from thesis_group_members order by group_id, view_id' if False else 'select view_id, open, after_seq from view_switches where after_seq <= ? order by id'}
    for name, query in checks.items():
        ours, theirs = rebuilt.execute(query, (top,)).fetchall(), stored.execute(query, (top,)).fetchall()
        print(f"  {name}: rebuilt {len(ours)}, stored {len(theirs)}: {'identical' if ours == theirs else 'DIFFERENT'}")
    for line in lines[-3:]:
        print('  log:', line[:200])


if __name__ == '__main__':
    main()
