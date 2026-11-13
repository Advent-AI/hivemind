"""The control: the request as FIRST sent (before any change), three times a topic.

Its first run (`control-first-request.json`, two topics) took the schema from the model archive, whose JSON is canonical: keys
sorted, so the answer's fields stood in alphabetical order and not in the order first sent. With `--as-sent` the schema is
`first-schema-as-sent.json`, in the order the first send used, and all eight topics are sent (D407).

  python3 clean-arch/step4-2026-11-10/probe-2026-11-10/control_first_request.py --as-sent
"""
import concurrent.futures
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
REPOSITORY = STEP.parents[1]
sys.path[:0] = [str(REPOSITORY / 'src'), str(REPOSITORY / 'clean-arch' / 'e2e-2026-11-09')]
from hivemind import config, model, universe  # noqa: E402
import budget  # noqa: E402

SENDS_A_TOPIC = 3
TOPICS = [('u1', 'clean-5'), ('u3', 'clean-10')]
ALL_TOPICS = [('u1', 'clean-3'), ('u1', 'clean-2'), ('u1', 'clean-7'), ('u1', 'clean-4'), ('u3', 'clean-12'), ('u2', 'clean-10'),
              ('u1', 'clean-5'), ('u3', 'clean-10')]
SETTING = config.Setting(name='clean_ladder_probe', model='gpt-6-luna', prompt_version='ladder-first-request-control',
                         reasoning_effort='medium', max_output_tokens=16000)


def main():
    as_sent = '--as-sent' in sys.argv
    output_path = HERE / ('control-first-as-sent.json' if as_sent else 'control-first-request.json')
    if output_path.exists():
        raise SystemExit(f'{output_path} exists')
    system_text = (HERE / 'sent-system.txt').read_text()
    closing_text = (HERE / 'sent-closing.txt').read_text().strip()
    schema = json.loads((HERE / ('first-schema-as-sent.json' if as_sent else 'sent-schema.json')).read_text())
    research_list = universe.load(str(REPOSITORY / 'poc' / 'universe.json'))
    themes = [{'id': theme_id, 'name': theme['name']} for theme_id, theme in research_list.themes.items()]
    stored = {(entry['run'], entry['id']): entry for entry in json.loads((STEP / 'census' / 'packet.json').read_text())}
    jobs = []
    for draw, thesis_id in (ALL_TOPICS if as_sent else TOPICS):
        entry = stored[(draw, thesis_id)]
        article = entry['article']
        payload = {'company': 'NVDA', 'fiscal_year_note': research_list.fiscal_note('NVDA', article['publication_date'], english=True),
                   'themes': themes,
                   'thesis': {'id': thesis_id, **{field: entry['thesis'][field] for field in ('description', 'outcome', 'period', 'opens_as', 'settled_by')}},
                   'item': {field: article[field] for field in ('publication_date', 'publisher', 'title', 'text')}}
        request = model.build_request(SETTING, system_text, json.dumps(payload, ensure_ascii=False) + '\n\n' + closing_text, schema,
                                      'clean_ladder', 'openai')
        jobs.extend((f'{draw}/{thesis_id}', number, request) for number in range(1, SENDS_A_TOPIC + 1))
    limit = budget.Budget(0.25 if as_sent else 0.10)

    def send(job):
        case, number, request = job
        answer = json.loads(limit.send('openai', request)['choices'][0]['message']['content'])
        ladder = answer.get('ladder')
        shape = 'declined' if answer.get('no_ladder') else next(name for name in ('yes_no', 'states', 'figure') if ladder.get(name))
        return {'case': case, 'send': number, 'shape': shape, 'answer': answer}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(send, jobs))
    output_path.write_text(json.dumps(results, ensure_ascii=False, indent=1) + '\n')
    for result in results:
        answer = result['answer']
        summary = answer['no_ladder'] if answer.get('no_ladder') else answer['ladder']['question']
        print(f"{result['case']:>12} #{result['send']} | {result['shape']:<8} | {summary[:170]}")
    print(f'spent ${limit.spent_usd:.4f}')


if __name__ == '__main__':
    main()
