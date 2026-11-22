"""$0 step 2 of D694: rebuild old-2's ledger as it stood at the end of 2026-07-09 (the July test's starting state) by replaying the
product (poc-v118) from 2026-07-01 over old-2's own stored answers. Every request must be answered from the archive: the transport
refuses any send, so a request that differs from the stored one by a byte stops the rebuild. The archive is a scratch copy (a
refused judge answer is retired in the copy only).

  python3 rebuild_control.py <scratch folder>

Then it compares the rebuilt ledger with old-2's finished store up to the end of 07-09: views, keys, rungs, evidence, links and
judgements (rung, reasons, request sha) must be equal.
"""
import shutil
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / 'src'))
from hivemind import config, model, replay, universe        # noqa: E402

OLD2 = REPO / 'poc/data/comparison-2026-11-17/run/old-2/prod'
ITEMS = REPO / 'poc/data/comparison-2026-11-17/items-comparison.sqlite'
UNTIL = '2026-07-09'


class SendRefused(RuntimeError):
    pass


def refuse(*args, **kwargs):
    raise SendRefused('a request was not in the archive: the rebuilt request differs from the stored one')


def rows(conn, sql, args=()):
    return [tuple(r) for r in conn.execute(sql, args)]


def compare(rebuilt_path, last_seq):
    rebuilt = sqlite3.connect(f'file:{rebuilt_path}?mode=ro', uri=True)
    stored = sqlite3.connect(f'file:{OLD2}/views.sqlite?mode=ro', uri=True)
    checks = {
        'views': ('select view_id, question, created_seq from views where created_seq <= ? order by view_id', (last_seq,)),
        'view_keys': ('select view_id, measure, scope, period_start, period_end, unit from view_keys where seq <= ? order by view_id', (last_seq,)),
        'evidence': ('select evidence_id, quote, created_seq from evidence where created_seq <= ? order by evidence_id', (last_seq,)),
        'evidence_links': ('select evidence_id, view_id, seq from evidence_links where seq <= ? order by evidence_id, view_id', (last_seq,)),
        'judgements': ('select view_id, seq, rung, reasons, cited_evidence_json, cited_views_json, changed, reference, implied_outcome, request_sha256 from judgements where seq <= ? order by judgement_id', (last_seq,)),
        'rungs': ('select r.view_id, r.position, r.label, r.condition, r.lo, r.hi from rungs r join views v using(view_id) where v.created_seq <= ? order by r.view_id, r.position', (last_seq,)),
        'view_switches': ('select view_id, open, reason, after_seq from view_switches where after_seq <= ? order by id', (last_seq,)),
        'successions': ('select view_id, succeeds, seq from successions where seq <= ? order by id', (last_seq,)),
        'dependencies': ('select view_id, depends_on, seq from dependencies where seq <= ? order by dependency_id', (last_seq,)),
    }
    ok = True
    for name, (sql, args) in checks.items():
        a, b = rows(rebuilt, sql, args), rows(stored, sql, args)
        same = a == b
        ok = ok and same
        print(f'{name}: rebuilt {len(a)} stored {len(b)} {"equal" if same else "DIFFER"}')
        if not same:
            for x, y in zip(a, b):
                if x != y:
                    print('  first difference:', str(x)[:200], '|', str(y)[:200])
                    break
    return ok


def main():
    scratch = Path(sys.argv[1])
    scratch.mkdir(parents=True, exist_ok=True)
    views_path, archive_path = scratch / 'views.sqlite', scratch / 'archive.sqlite'
    for path in (views_path, archive_path):
        if path.exists():
            raise SystemExit(f'{path} exists: a rebuild starts from an empty folder')
    shutil.copyfile(OLD2 / 'archive.sqlite', archive_path)
    cfg = config.load(str(REPO / 'poc/config/poc-v118.json'))
    uni = universe.load(str(REPO / 'poc/universe.json'))
    totals = replay.run(testdb_path=str(ITEMS), views_path=str(views_path), archive=model.Archive(str(archive_path)), cfg=cfg,
                        universe=uni, from_day='2026-07-01', until_day=UNTIL, transport=refuse, log=print,
                        only_objects={'NVDA'})          # the comparison launcher's default (`budget_replay.py --only NVDA`)
    print('totals:', totals)
    conn = sqlite3.connect(f'file:{views_path}?mode=ro', uri=True)
    last_seq = conn.execute('select max(seq) from days_completed where day=?', (UNTIL,)).fetchone()[0]
    print('last completed seq at', UNTIL, last_seq)
    sys.exit(0 if compare(views_path, last_seq) else 1)


if __name__ == '__main__':
    main()
