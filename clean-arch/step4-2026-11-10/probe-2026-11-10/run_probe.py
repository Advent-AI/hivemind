"""A probe of a few cents (D402): the ladder step's request, as design version 30 holds it, sent once on six stored theses.

It measures nothing: six answers, one draw, read by hand beside their articles. It builds each request as DESIGN.md §5.2 says
(the system text; the payload as one JSON object, a blank line, the closing check; the strict schema; gpt-6-luna at medium effort
with the judge's output cap) and sends it through the measurement's spending limit. No check of the step is applied here beyond
production's schema validation: the answers are for reading.

  python3 clean-arch/step4-2026-11-10/probe-2026-11-10/run_probe.py --dry     # build the requests, print sizes and worst cost, $0
  python3 clean-arch/step4-2026-11-10/probe-2026-11-10/run_probe.py --send    # send the six requests, once each
  ... --send --label round2                                                   # the same six with the request as it then stands (D404)
"""
import argparse
import concurrent.futures
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
REPOSITORY = STEP.parents[1]
sys.path[:0] = [str(REPOSITORY / 'src'), str(REPOSITORY / 'clean-arch' / 'e2e-2026-11-09')]
from hivemind import config, model, universe  # noqa: E402
import budget  # noqa: E402

COMPANY = 'NVDA'
CAP_USD = 0.25
SETTING = config.Setting(name='clean_ladder_probe', model='gpt-6-luna', prompt_version='ladder-candidate-v30',
                         reasoning_effort='medium', max_output_tokens=16000)
# (draw, thesis id): the answer shape each case was chosen for
CASES = [
    (('u1', 'clean-3'), 'a yes/no event'),
    (('u1', 'clean-2'), 'a topic that asks several things; a binding obligation'),
    (('u1', 'clean-7'), "a company's figure"),
    (('u1', 'clean-4'), "a theme's figure with a reference in the article"),
    (('u3', 'clean-12'), 'an event with more than two states'),
    (('u2', 'clean-10'), 'a topic that names two things, neither the main one'),
]
# D406: two more topics both census readers found to have no main thing; sent only with --more
MORE_CASES = [
    (('u1', 'clean-5'), 'no main thing: memory prices and the memory cost of a rack'),
    (('u3', 'clean-10'), 'no main thing: new HBM capacity and whether it arrives early'),
]
THESIS_FIELDS = ('description', 'outcome', 'period', 'opens_as', 'settled_by')
ITEM_FIELDS = ('publication_date', 'publisher', 'title', 'text')


def build_requests(cases):
    """One entry a case: its name, the system text, the user text and the request as it would be sent."""
    system_text = (STEP / 'ladder' / 'candidate-system.txt').read_text()
    closing_text = (STEP / 'ladder' / 'candidate-closing.txt').read_text().strip()
    schema = json.loads((STEP / 'ladder' / 'candidate-schema.json').read_text())
    research_list = universe.load(str(REPOSITORY / 'poc' / 'universe.json'))
    themes = [{'id': theme_id, 'name': theme['name']} for theme_id, theme in research_list.themes.items()]
    stored = {(entry['run'], entry['id']): entry for entry in json.loads((STEP / 'census' / 'packet.json').read_text())}
    entries = []
    for (draw, thesis_id), chosen_for in cases:
        entry = stored[(draw, thesis_id)]
        article = entry['article']
        payload = {'company': COMPANY,
                   'fiscal_year_note': research_list.fiscal_note(COMPANY, article['publication_date'], english=True),
                   'themes': themes,
                   'thesis': {'id': thesis_id, **{field: entry['thesis'][field] for field in THESIS_FIELDS}},
                   'item': {field: article[field] for field in ITEM_FIELDS}}
        user_text = json.dumps(payload, ensure_ascii=False) + '\n\n' + closing_text
        request = model.build_request(SETTING, system_text, user_text, schema, 'clean_ladder', 'openai')
        entries.append({'case': f'{draw}/{thesis_id}', 'chosen_for': chosen_for, 'system': system_text, 'user': user_text,
                        'schema': schema, 'request': request})
    checksum = hashlib.sha256(json.dumps({'system': system_text, 'closing': closing_text, 'schema': schema,
                                          'setting': [SETTING.model, SETTING.reasoning_effort, SETTING.max_output_tokens]},
                                         ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return entries, checksum


def send_one(entry, archive, call_config, limit):
    """Send one request once. The answer's own text is kept as it arrives, before anything parses it."""
    received = {}

    def transport(provider, request):
        response = limit.send(provider, request)
        try:
            received['text'] = response['choices'][0]['message']['content']
        except (KeyError, IndexError, TypeError):
            received['text'] = None
        received['usage'] = response.get('usage') if isinstance(response, dict) else None
        return response

    result = {'case': entry['case'], 'chosen_for': entry['chosen_for']}
    try:
        answer = model.call(archive, call_config, SETTING, entry['system'], entry['user'], entry['schema'], 'clean_ladder',
                            'ladder-probe', transport=transport)
        result.update(status='answered', answer=answer.data, input_tokens=answer.input_tokens, output_tokens=answer.output_tokens,
                      from_cache=answer.cached)
    except model.SchemaError as error:
        result.update(status='not valid against the schema', error=str(error))
    except (ValueError, RecursionError) as error:
        result.update(status='not readable', error=f'{type(error).__name__}: {error}')
    result['answer_text'] = received.get('text')
    result['usage'] = received.get('usage')
    return result


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--dry', action='store_true')
    mode.add_argument('--send', action='store_true')
    parser.add_argument('--more', action='store_true', help='add the two further topics of D406')
    parser.add_argument('--sends', type=int, default=1, help='how many times each request is sent; each send has its own archive')
    parser.add_argument('--label', default='', help='a later round keeps its own files: answers-<label>.jsonl, archive-<label>.sqlite')
    arguments = parser.parse_args()
    suffix = f'-{arguments.label}' if arguments.label else ''
    entries, checksum = build_requests(CASES + (MORE_CASES if arguments.more else []))
    worst_total = 0.0
    for entry in entries:
        worst = budget.worst_cost(entry['request'])
        worst_total += worst
        print(f"{entry['case']:>14} | {entry['chosen_for']:<52} | system {len(entry['system']):>5} chars | user {len(entry['user']):>6} chars "
              f"| worst cost ${worst:.4f}")
    print(f'{len(entries)} requests, {arguments.sends} send(s) each, worst cost in all ${worst_total * arguments.sends:.4f}; cap ${CAP_USD:.2f}; configuration {checksum[:16]}')
    (HERE / f'requests{suffix}.json').write_text(json.dumps([{'case': entry['case'], 'request': entry['request']} for entry in entries],
                                                   indent=1, ensure_ascii=True) + '\n')
    if arguments.dry:
        return
    answers_path = HERE / f'answers{suffix}.jsonl'
    if answers_path.exists():
        raise SystemExit(f'{answers_path} exists: the probe is sent once')
    call_config = SimpleNamespace(provider='openai', version='clean-ladder-probe', checksum=checksum[:16])
    limit = budget.Budget(CAP_USD)
    results = []
    for send_number in range(1, arguments.sends + 1):       # one archive a send, so that no answer comes from the cache
        archive_name = f'archive{suffix}.sqlite' if arguments.sends == 1 else f'archive{suffix}-send{send_number}.sqlite'
        archive = model.Archive(str(HERE / archive_name))
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            for result in pool.map(lambda entry: send_one(entry, archive, call_config, limit), entries):
                results.append({'send': send_number, **result})
    with answers_path.open('w') as handle:
        for result in results:
            handle.write(json.dumps(result, ensure_ascii=True) + '\n')
    for result in results:
        print(f"send {result['send']} {result['case']:>14} | {result['status']} | tokens in {result.get('input_tokens')} out {result.get('output_tokens')} | cache {result.get('from_cache')}")
    print(f'spent ${limit.spent_usd:.4f} of ${CAP_USD:.2f} (from tokens at the published rates)')


if __name__ == '__main__':
    main()
