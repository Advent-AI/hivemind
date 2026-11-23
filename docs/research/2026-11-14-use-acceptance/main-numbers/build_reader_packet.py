"""The main-numbers probe, the blind readers' packet ($0; PROBE-DESIGN.md, "Who reads"): every valid answer of both arms beside its article,
under shuffled answer labels, with the reason label of each new thesis removed and reason names masked in free text (the label alone would
tell the arms apart: only one arm's schema holds the fifth reason). For a target case the packet also carries the case's named facts and
every kept statement with its links; for the other cases, the new theses only. The key goes outside the repository.

  python3 build_reader_packet.py <records.jsonl> <cases.json> <key folder outside the repository> [packet name]
"""
import json
import random
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEMS = Path('/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite')
REASONS = re.compile(r'\b(main_driver|product_node|binding_obligation|shared_quantity|policy_stage)\b')


def masked(value):
    return REASONS.sub('[reason]', value) if isinstance(value, str) else value


def main():
    records_path, cases_path, key_folder = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    name = sys.argv[4] if len(sys.argv) > 4 else 'reader-packet'
    cases = {case['case']: case for case in json.loads(cases_path.read_text())}
    records = [json.loads(line) for line in records_path.read_text().splitlines() if line.strip()]
    valid = [record for record in records if record['attempts'] and record['attempts'][-1].get('outcome') == 'valid']
    items = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    article_number, articles = {}, []
    for case_name in sorted({record['case'] for record in valid}, key=lambda case_name: cases[case_name]['sequence']):
        case = cases[case_name]
        trace = sqlite3.connect(f"file:{case['trace']}?mode=ro", uri=True)
        input_id, before_state = trace.execute('select input_id, before_state from trace where sequence = ?', (case['sequence'],)).fetchone()
        day, title, text = items.execute('select publication_day, title, text from items where input_id = ?', (input_id,)).fetchone()
        article_number[case_name] = len(articles) + 1
        articles.append({'article': len(articles) + 1, 'day': day, 'title': title, 'text': text,
                         'questions_already_open': [{'id': thesis['id'], 'question': thesis['description'], 'period': thesis.get('period')}
                                                    for thesis in json.loads(before_state)],
                         'named_facts': [{'fact': number, 'text': fact['fact']} for number, fact in enumerate(case.get('named_facts') or [], 1)]})
    rng = random.Random(20261117)
    order = rng.sample(valid, len(valid))
    answers, key = [], []
    for number, record in enumerate(order, 1):
        label = f'A{number:02d}'
        case = cases[record['case']]
        entry = {'answer': label, 'article': article_number[record['case']],
                 'new_questions': [{'id': thesis['local_id'], 'question': masked(thesis.get('description')), 'outcome': masked(thesis.get('outcome')),
                                    'period': masked(thesis.get('period')), 'settled_by': masked(thesis.get('settled_by'))}
                                   for thesis in record.get('new_theses') or []]}
        if case.get('named_facts'):
            entry['kept_statements'] = [{'id': statement['local_id'], 'summary': statement.get('summary'),
                                         'passages': statement.get('verified_source_passages') or statement.get('source_passages'),
                                         'linked_to': [{'question': link.get('target_id'), 'new': link.get('target_type') == 'new',
                                                        'why': masked(link.get('relevance'))} for link in statement.get('links') or []]}
                                        for statement in record.get('links') or []]
        answers.append(entry)
        key.append({'answer': label, 'case': record['case'], 'arm': record['arm'], 'send': record['send'],
                    'reasons': {thesis['local_id']: thesis.get('opens_as') for thesis in record.get('new_theses') or []}})
    (HERE / f'{name}.json').write_text(json.dumps({'articles': articles, 'answers': answers}, ensure_ascii=False, indent=1))
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / f'main-numbers-key-{name}.json').write_text(json.dumps(key, indent=1))
    invalid = len(records) - len(valid)
    print(f'{len(answers)} valid answers over {len(articles)} articles ({invalid} sends not valid, left out and listed in the result); '
          f'{sum(len(a["new_questions"]) for a in answers)} new questions; packet {len(json.dumps(answers)) + len(json.dumps(articles))} characters')


if __name__ == '__main__':
    main()
