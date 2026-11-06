"""Compare two ledgers table by table, every column except wall-clock stamps (*_at, seconds): the comparability gate's test that a replay
reproduced a stored draw. Prints per table the rows in each and the rows only in one; exits 1 on any difference or an empty comparison."""
import sqlite3
import sys

TABLES = ('views', 'rungs', 'view_keys', 'view_switches', 'evidence', 'evidence_sources', 'evidence_links', 'judgements', 'dependencies',
          'replacements', 'revisions', 'same_claims', 'successions', 'handovers', 'thesis_groups', 'thesis_group_members', 'days_completed',
          'late_statements', 'review_pool_entries', 'processing_steps', 'research_subjects', 'match_records', 'dependency_resolutions', 'thesis_group_aliases')


def rows(conn, table):
    columns = [r[1] for r in conn.execute(f'pragma table_info({table})') if not r[1].endswith('_at') and r[1] not in ('seconds', 'at')]
    if not columns:
        return None, []
    return columns, sorted(tuple(r) for r in conn.execute(f'select {", ".join(columns)} from {table}'))


def main(left_path, right_path):
    left = sqlite3.connect(f'file:{left_path}?mode=ro', uri=True)
    right = sqlite3.connect(f'file:{right_path}?mode=ro', uri=True)
    differ, compared = False, 0
    for table in TABLES:
        lcols, lrows = rows(left, table)
        rcols, rrows = rows(right, table)
        if lcols is None and rcols is None:
            continue
        if (lcols is None and not rrows) or (rcols is None and not lrows):
            print(f'{table}: absent on one side, empty on the other — same')
            continue
        if lcols != rcols:
            print(f'{table}: columns differ {lcols} / {rcols}')
            differ = True
            continue
        only_left = sorted(set(lrows) - set(rrows))
        only_right = sorted(set(rrows) - set(lrows))
        compared += len(lrows)
        mark = 'same' if not only_left and not only_right and len(lrows) == len(rrows) else 'DIFFERS'
        print(f'{table}: {len(lrows)} / {len(rrows)} rows; only left {len(only_left)}, only right {len(only_right)} — {mark}')
        for r in only_left[:3]:
            print('   left :', str(r)[:300])
        for r in only_right[:3]:
            print('   right:', str(r)[:300])
        differ = differ or mark != 'same'
    if compared == 0:
        print('unexercised: nothing compared')
    sys.exit(1 if differ or compared == 0 else 0)


if __name__ == '__main__':
    main(*sys.argv[1:3])
