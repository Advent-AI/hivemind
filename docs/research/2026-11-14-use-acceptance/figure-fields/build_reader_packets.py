"""The figure-fields probe, the blind readers' two packets ($0; PROBE-DESIGN.md, "Who reads").

Packet one (`reader-packet-1.json`): every valid answer of both arms under shuffled labels, in one shape: the article with its title and
publisher as the model saw them; every kept statement that holds figures, with its statement-level party and date; every figure with
measure, stored period, value, kind, basis and one `party` (c21: the figure's own; c8: the statement's party repeated). No fixed period
appears. For the target and control cases it also gives the questions open when the article was read and each such statement's links
(question and the answer's reason), or that it has none; for target cases, the named figures to locate (described, with no source given).

Packet two (`reader-packet-2.json`): c21's answers only: every figure with its stored period and its fixed period.

  python3 build_reader_packets.py <records.jsonl> <cases.json> <key folder outside the repository>
"""
import json
import random
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    records_path, cases_path, key_folder = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    cases = {case['case']: case for case in json.loads(cases_path.read_text())}
    records = [json.loads(line) for line in records_path.read_text().splitlines() if line.strip()]
    valid = [record for record in records if record['attempts'] and record['attempts'][-1].get('outcome') == 'valid']
    articles, article_number = [], {}
    for name in sorted({record['case'] for record in valid}, key=lambda case_name: cases[case_name]['sequence']):
        case = cases[name]
        trace = sqlite3.connect(f"file:{case['trace']}?mode=ro", uri=True)
        request_json, before_state = trace.execute('select request, before_state from trace where sequence = ?', (case['sequence'],)).fetchone()
        payload, _ = json.JSONDecoder().raw_decode(json.loads(request_json)['messages'][1]['content'])
        item = payload['source_item']
        article_number[name] = len(articles) + 1
        filing = not name.endswith('-keep')
        articles.append({'article': len(articles) + 1, 'title': item.get('title'), 'publisher': item.get('publisher'),
                         'publication_date': item.get('publication_date'), 'text': item.get('text'),
                         'named_figures': [{'figure': number, 'text': named['figure']} for number, named in enumerate(case.get('named_figures') or [], 1)],
                         'open_questions': ([{'id': thesis['id'], 'question': thesis['description'], 'period': thesis.get('period')}
                                             for thesis in json.loads(before_state)] if filing else None)})
    rng = random.Random(20261121)
    one, two, key = [], [], []
    for number, record in enumerate(rng.sample(valid, len(valid)), 1):
        label = f'B{number:02d}'
        filing = not record['case'].endswith('-keep')
        statements = []
        for statement in record.get('links') or []:
            if not statement.get('figures'):
                continue
            entry = {'id': statement['local_id'], 'summary': statement.get('summary'),
                     'passages': statement.get('verified_source_passages') or statement.get('source_passages'),
                     'statement_party': statement.get('original_party'),
                     'statement_date': statement.get('statement_date') or statement.get('statement_date_text'),
                     'figures': [{'n': position, 'measure': figure.get('measure'), 'period': figure.get('period'), 'value': figure.get('value'),
                                  'kind': figure.get('kind'), 'basis': figure.get('basis'),
                                  'party': figure['party'] if 'party' in figure else statement.get('original_party')}
                                 for position, figure in enumerate(statement['figures'], 1)]}
            if filing:
                entry['links'] = [{'question': link.get('target_id'), 'new_question': link.get('target_type') == 'new', 'reason': link.get('relevance')}
                                  for link in statement.get('links') or []] or 'none'
            statements.append(entry)
        one.append({'answer': label, 'article': article_number[record['case']], 'statements_with_figures': statements or 'none kept'})
        key.append({'answer': label, 'case': record['case'], 'arm': record['arm'], 'send': record['send']})
        if record['arm'] != 'c8':
            two.append({'answer': label, 'article': article_number[record['case']],
                        'figures': [{'statement': statement['local_id'], 'n': position, 'measure': figure.get('measure'),
                                     'period': figure.get('period'), 'fixed_period': figure.get('fiscal_period')}
                                    for statement in record.get('links') or [] for position, figure in enumerate(statement.get('figures') or [], 1)]})
    (HERE / 'reader-packet-1.json').write_text(json.dumps({'articles': articles, 'answers': one}, ensure_ascii=False, indent=1))
    (HERE / 'reader-packet-2.json').write_text(json.dumps({'articles': [{k: v for k, v in article.items() if k not in ('named_figures', 'open_questions')}
                                                                        for article in articles], 'answers': two}, ensure_ascii=False, indent=1))
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / 'figure-fields-key.json').write_text(json.dumps(key, indent=1))
    leak = sum('fixed_period' in json.dumps(answer) or 'fiscal_period' in json.dumps(answer) for answer in one)
    print(f'packet one: {len(one)} answers over {len(articles)} articles, {sum(len(a["statements_with_figures"]) for a in one if isinstance(a["statements_with_figures"], list))} '
          f'statements with figures; answers carrying a fixed period (must be 0): {leak}; packet two: {len(two)} answers, '
          f'{sum(len(a["figures"]) for a in two)} figures; invalid sends left out: {len(records) - len(valid)}')


if __name__ == '__main__':
    main()
