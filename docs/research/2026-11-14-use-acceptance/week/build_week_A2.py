"""Lean step 2, reading A2 ($0): every question each system opened over the fresh week (2026-09-22..28), reduced to one shape under the
labels X and Y, with the article each was opened from. The clean draw's questions are the theses its Step 1 trace adds, step by step; the
production draw's are its views. An opening article is named by its number in the A1 packet when it is one of the 40, otherwise by a label
O-k, and every opening article's text goes to `opening-articles-A2.json` so a verdict on a question is read beside its source. The label
assignment is drawn with a fixed seed and the key goes outside the repository.

  python3 build_week_A2.py <key folder outside the repository>
"""
import json
import random
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/lchingen/hivemind/poc/data/clean-lean-week-2026-11-14')
CLEAN_TRACE = ROOT / 'week-r2/c1/step1/trace.sqlite'
PRODUCTION_VIEWS = ROOT / 'week/p1/prod/views.sqlite'
ITEMS = Path('/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite')


def clean_questions():
    trace = sqlite3.connect(f'file:{CLEAN_TRACE}?mode=ro', uri=True)
    opened = []
    for input_id, before_state, after_state in trace.execute(
            "select input_id, before_state, after_state from trace where status='complete' order by sequence"):
        known = {thesis['id'] for thesis in json.loads(before_state)}
        for thesis in json.loads(after_state):
            if thesis['id'] not in known:
                opened.append({'own_id': thesis['id'], 'question': thesis['description'], 'outcome': thesis.get('outcome'),
                               'period': thesis['period'], 'opened_from': input_id})
    return opened


def production_questions():
    views = sqlite3.connect(f'file:{PRODUCTION_VIEWS}?mode=ro', uri=True)
    return [{'own_id': view_id, 'question': question, 'outcome': looks_at, 'period': f'due {due_day}, year {year}', 'opened_from': created_from}
            for view_id, question, looks_at, due_day, year, created_from in views.execute(
                'select view_id, question, looks_at, due_day, year, created_from_input from views order by created_seq')]


def main():
    key_folder = Path(sys.argv[1])
    packet_number = {row['input_id']: row['article'] for row in json.loads((key_folder / 'week-key-A1.json').read_text())}
    systems = {'c1': clean_questions(), 'p1': production_questions()}
    rng = random.Random(20261116)
    labels = ['X', 'Y'] if rng.random() < 0.5 else ['Y', 'X']
    label_of = {'c1': labels[0], 'p1': labels[1]}
    items = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    outside, articles, libraries, key = {}, {}, {}, {'labels': label_of}
    for system, questions in systems.items():
        label = label_of[system]
        key[system] = []
        libraries[label] = []
        for number, question in enumerate(questions, 1):
            source = question['opened_from']
            if source in packet_number:
                name = f'article {packet_number[source]} of the packet'
            else:
                name = outside.setdefault(source, f'article O-{len(outside) + 1} (outside the 40)')
            if name not in articles:
                day, publisher, title, text = items.execute(
                    'select publication_day, publisher, title, text from items where input_id = ?', (source,)).fetchone()
                articles[name] = {'article': name, 'day': day, 'publisher': publisher, 'title': title, 'text': text}
            libraries[label].append({'system_id': f'{label}-{number}', 'question': question['question'], 'outcome': question['outcome'],
                                     'period': question['period'], 'opened_from': name})
            key[system].append({'system_id': f'{label}-{number}', 'own_id': question['own_id'], 'opened_from': source})
    (HERE / 'libraries-A2.json').write_text(json.dumps({label: libraries[label] for label in sorted(libraries)}, ensure_ascii=False, indent=1))
    (HERE / 'opening-articles-A2.json').write_text(json.dumps(list(articles.values()), ensure_ascii=False, indent=1))
    (key_folder / 'week-key-A2.json').write_text(json.dumps(key, indent=1))
    print(f"questions: clean {len(systems['c1'])}, production {len(systems['p1'])}; opening articles {len(articles)} "
          f"({len(outside)} outside the 40); the labels are in the key")


if __name__ == '__main__':
    main()
