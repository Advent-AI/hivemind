"""Eligible cases for a measurement of D375, step 1 ($0; D528): by code, on the old system's stored runs, for every question opened by
an article that was not the last of its day: the statements that later articles of the same day produced and that did not reach that
question by the day's end (kept under other questions, or dropped for want of a question). These are candidates only: whether a
statement bears on the question is for readers. Read-only.

  python3 same_day_candidates.py
"""
import collections
import json
import sqlite3
from pathlib import Path

DATA = Path('/Users/lchingen/hivemind/poc/data')
RUNS = {'fresh week p1': DATA / 'clean-lean-week-2026-11-14/week/p1/prod', 'July p1': DATA / 'clean-e2e-full-2026-11-13/p1/prod',
        'July p2': DATA / 'clean-e2e-full-2026-11-13/p2/prod', 'July p3': DATA / 'clean-e2e-full-2026-11-13/p3/prod'}
HERE = Path(__file__).resolve().parent


def main():
    out = []
    for name, folder in RUNS.items():
        store = sqlite3.connect(f"file:{folder / 'views.sqlite'}?mode=ro", uri=True)
        archive = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        days = [(row[1], row[2]) for row in store.execute('select * from days_completed order by 1')]
        handovers = {seq: (input_id, json.loads(text)) for input_id, seq, text in store.execute('select input_id, seq, handover_json from handovers')}
        totals = collections.Counter()
        for view_id, opened, question in store.execute('select view_id, created_seq, question from views where created_seq > 0 order by created_seq'):
            day, day_end = next((d, end) for d, end in days if opened <= end)
            later = [seq for seq in handovers if opened < seq <= day_end]
            if not later:
                continue
            reached = {row[0] for row in store.execute('select evidence_id from evidence_links where view_id = ? and seq <= ?', (view_id, day_end))}
            judged_that_day = store.execute('select count(*) from judgements where view_id = ? and seq = ?', (view_id, day_end)).fetchone()[0]
            kept_elsewhere = store.execute('select count(*) from evidence where created_seq > ? and created_seq <= ? and evidence_id not in (select evidence_id from evidence_links where view_id = ?)',
                                           (opened, day_end, view_id)).fetchone()[0]
            reached_later = store.execute('select count(distinct evidence_id) from evidence_links where view_id = ? and seq > ? and seq <= ?', (view_id, opened, day_end)).fetchone()[0]
            dropped = sum(1 for seq in later for d in handovers[seq][1].get('dropped') or [] if d[1] == 'no home')
            totals['questions opened before the last article of their day'] += 1
            totals['statements of later same-day articles kept under other questions'] += kept_elsewhere
            totals['statements of later same-day articles dropped for want of a question'] += dropped
            totals['statements of later same-day articles that reached the question that day'] += reached_later
            out.append({'run': name, 'question': view_id, 'wording': question, 'opened_at': opened, 'day': day, 'day_end': day_end, 'later_articles': len(later),
                        'judged_at_day_end': bool(judged_that_day), 'reached_that_day_from_later_articles': reached_later, 'kept_elsewhere': kept_elsewhere, 'dropped_no_home': dropped})
        print(f"{name}: {dict(totals)}")
    (HERE / 'same-day-candidates.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    print('\nfresh week, by question:')
    for row in out:
        if row['run'] == 'fresh week p1':
            print(f"  {row['question']} (article {row['opened_at']} of {row['day']}; {row['later_articles']} later articles that day): reached it {row['reached_that_day_from_later_articles']}, "
                  f"kept elsewhere {row['kept_elsewhere']}, dropped {row['dropped_no_home']} | {row['wording'][:80]}")


if __name__ == '__main__':
    main()
