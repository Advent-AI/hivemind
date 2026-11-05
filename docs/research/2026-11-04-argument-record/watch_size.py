"""How large judging-v7's reading gets, day by day, in a finished run or a snapshot of a live one (never the live databases).

Per day: judgements written, the largest request (pieces shown and characters), the largest number of pushes one answer wrote (the
per-piece list whose wrong id halted the three-month run, D358), the pieces in force that were not shown, and the judging answers code
refused that day. Then the five largest requests of the run with their question.

usage: python3 watch_size.py <run folder or snapshot folder>
"""
import collections
import json
import re
import sqlite3
import sys


def main():
    folder = sys.argv[1]
    views = sqlite3.connect(f'file:{folder}/views.sqlite?mode=ro', uri=True)
    archive = sqlite3.connect(f'file:{folder}/archive.sqlite?mode=ro', uri=True)
    calls = {}
    for sha, request_json, answer_json in archive.execute("select request_sha256, request_json, answer_json from model_calls where purpose='judge'"):
        calls[sha] = (request_json, answer_json)
    refused_by_day = collections.Counter()
    for sha, (request_json, _) in calls.items():
        if ':refused:' in sha:
            text = json.loads(request_json)['messages'][1]['content']
            match = re.search(r'\[Previous conclusion[^\n]*', text)
            refused_by_day['refused'] += 1
    per_day = collections.OrderedDict()
    largest = []
    for view_id, day, sha in views.execute('select view_id, publication_day, request_sha256 from judgements order by seq, judgement_id'):
        request_json, answer_json = calls[sha]
        text = json.loads(request_json)['messages'][1]['content']
        shown = len(re.findall(r'^- e\d+ \[', text, re.M))
        hidden = re.search(r'\[Not shown: (\d+) more', text)
        pushes = len((json.loads(answer_json) or {}).get('pushes') or [])
        row = per_day.setdefault(day, {'judgements': 0, 'max_shown': 0, 'max_chars': 0, 'max_pushes': 0, 'max_hidden': 0})
        row['judgements'] += 1
        row['max_shown'] = max(row['max_shown'], shown)
        row['max_chars'] = max(row['max_chars'], len(text))
        row['max_pushes'] = max(row['max_pushes'], pushes)
        row['max_hidden'] = max(row['max_hidden'], int(hidden.group(1)) if hidden else 0)
        largest.append((len(text), shown, day, view_id))
    linked = dict(views.execute('select s.publication_day, count(*) from evidence_links l join (select evidence_id, min(publication_day) publication_day '
                                'from evidence_sources group by evidence_id) s using(evidence_id) group by s.publication_day'))
    print(f'{"day":10} {"links":>5} {"judged":>6} {"max shown":>9} {"max chars":>9} {"max pushes":>10} {"max not shown":>13}')
    for day, row in per_day.items():
        print(f'{day:10} {linked.get(day, 0):5} {row["judgements"]:6} {row["max_shown"]:9} {row["max_chars"]:9,} {row["max_pushes"]:10} {row["max_hidden"]:13}')
    refused = sum(1 for sha in calls if ':refused:' in sha)
    print(f'judging answers sent {len(calls)}, refused by code {refused}; judgements written {sum(r["judgements"] for r in per_day.values())}')
    for chars, shown, day, view_id in sorted(largest, reverse=True)[:5]:
        question = views.execute('select question from views where view_id=?', (view_id,)).fetchone()[0]
        print(f'  largest: {chars:,} characters, {shown} pieces, {day} {view_id} {question[:70]}')


if __name__ == '__main__':
    main()
