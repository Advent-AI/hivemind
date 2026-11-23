"""The same-day candidate pairs of the old system's stored runs, against the visibility path ($0; D521). A candidate is a pair of
questions that share a research group and were opened on the same day: a list of leads, not a complete census of duplicates. For each,
from the stored records only: both questions; whether the earlier one was committed and open before the later one's article; whether
the later article's reading request printed the earlier question (the request's own text is searched for the question's wording); the
questions the later candidate was compared with, and the recorded outcome. Read-only. It judges nothing: whether a pair is one matter
asked twice is read by people.

  python3 same_day_pairs.py
"""
import collections
import itertools
import json
import re
import sqlite3
from pathlib import Path

DATA = Path('/Users/lchingen/hivemind/poc/data')
RUNS = {'fresh week p1': DATA / 'clean-lean-week-2026-11-14/week/p1/prod', 'July p1': DATA / 'clean-e2e-full-2026-11-13/p1/prod',
        'July p2': DATA / 'clean-e2e-full-2026-11-13/p2/prod', 'July p3': DATA / 'clean-e2e-full-2026-11-13/p3/prod'}
HERE = Path(__file__).resolve().parent


def main():
    rows = []
    for name, folder in RUNS.items():
        store = sqlite3.connect(f"file:{folder / 'views.sqlite'}?mode=ro", uri=True)
        archive = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        days = [(row[1], row[2]) for row in store.execute('select * from days_completed order by 1')]

        def day_of(seq):
            return next((day for day, end in days if seq <= end), None)

        def day_start(seq):
            ends = [end for _, end in days if end < seq]
            return max(ends) if ends else 0
        views = {row[0]: row for row in store.execute('select view_id, created_seq, created_from_input, question, object_id, kind, due_day from views')}
        groups = collections.defaultdict(set)
        for group_id, view_id in store.execute('select group_id, view_id from thesis_group_members'):
            groups[view_id].add(group_id)
        for first, second in itertools.combinations(sorted(views, key=lambda v: (views[v][1], int(v[1:]))), 2):
            if not groups[first] & groups[second] or day_of(views[first][1]) != day_of(views[second][1]):
                continue
            earlier, later = views[first], views[second]
            same_article = earlier[2] == later[2]
            opened = store.execute('select open, after_seq from view_switches where view_id = ? order by id limit 1', (first,)).fetchone()
            committed_before = bool(opened and opened[0] and opened[1] < later[1])
            reading = archive.execute("select request_json from model_calls where purpose = 'extract' and request_json like ? order by call_id desc limit 1", (f'%{later[2]}%',)).fetchone()
            request_text = ' '.join(m['content'] for m in json.loads(reading[0])['messages']) if reading else ''
            printed = earlier[3] in request_text
            at_start = [v for v, row in views.items() if row[1] <= day_start(later[1])]
            printed_control = sum(1 for v in at_start if views[v][3] in request_text)
            compared, outcome = {}, None
            for decisions, in store.execute('select decisions_json from match_records where input_id = ? order by id', (later[2],)):
                for candidate in json.loads(decisions).get('candidates') or []:
                    reason = candidate.get('reason') or ''
                    found = dict(re.findall(r'(v\d+): ([a-z_]+)', reason.split('groups joined')[0]))
                    if found and (outcome is None or first in found):
                        compared, outcome = found, f"{candidate.get('outcome')} {candidate.get('target_view_id') or ''}".strip() + ' | ' + reason.split('; groups joined')[-1][:150]
            rows.append({'run': name, 'day': day_of(earlier[1]), 'earlier': first, 'later': second, 'earlier_question': earlier[3], 'later_question': later[3],
                         'earlier_article': earlier[1], 'later_article': later[1], 'same_article': same_article, 'earlier_committed_and_open_before_later': committed_before,
                         'later_reading_request_prints_earlier': printed, 'questions_open_at_day_start_printed_in_that_request': f'{printed_control} of {len(at_start)}',
                         'earlier_among_compared': first in compared, 'verdict_on_earlier': compared.get(first), 'compared_with': sorted(compared, key=lambda v: int(v[1:])),
                         'recorded_outcome': outcome, 'subject': earlier[4], 'due_days': [earlier[6], later[6]]})
    (HERE / 'same-day-pairs.json').write_text(json.dumps(rows, indent=1, ensure_ascii=False) + '\n')
    for row in rows:
        print(f"\n{row['run']} {row['day']}: {row['earlier']} (article {row['earlier_article']}) / {row['later']} (article {row['later_article']}); subject {row['subject']}; due {row['due_days']}; same article: {row['same_article']}")
        print(f"   {row['earlier']}: {row['earlier_question'][:170]}\n   {row['later']}: {row['later_question'][:170]}")
        print(f"   earlier committed and open before the later article: {row['earlier_committed_and_open_before_later']}; the later article's reading request prints the earlier question: {row['later_reading_request_prints_earlier']} "
              f"(questions open at the day's start printed there: {row['questions_open_at_day_start_printed_in_that_request']})")
        print(f"   the later candidate was compared with {row['compared_with']}; earlier among them: {row['earlier_among_compared']} ({row['verdict_on_earlier']}); recorded: {row['recorded_outcome']}")


if __name__ == '__main__':
    main()
