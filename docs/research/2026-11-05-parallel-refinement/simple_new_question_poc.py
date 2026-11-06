"""Diagnostic only: find new research questions and evidence without producing database fields."""
import copy
import hashlib
import json
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import b_arm
from hivemind import extraction, model

IDS = ('gnews:085b1e1a1543437edb9756d6', 'gnews:4d1b1ca014068fb532f116b3',
       'gnews:795ea94e1100415a67fd1a96', 'gnews:3df0bbc8aff2c1d008bc0a32')
GOLD = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json')
GOLD_SHA = '6f9476bb6a81ea590af273a71565e7c3c0f49908d26274b8482d52cfdee31a21'
PREVIEW = ROOT / 'poc/data/simple-new-question-preview-2026-11-05-v3/manifest.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def wire(request):
    return sha(json.dumps(request).encode())


def schema():
    def obj(props):
        return {'type': 'object', 'additionalProperties': False, 'properties': props, 'required': list(props)}
    text = {'type': 'string'}
    evidence = obj({'quote': text, 'what_it_shows': text, 'original_speaker': text})
    question = obj({'question': text, 'why_it_matters': text, 'why_not_already_covered': text,
                    'how_and_when_to_check': text, 'evidence': {'type': 'array', 'items': evidence}})
    return obj({'questions': {'type': 'array', 'items': question}})


def prepare():
    if sha(GOLD.read_bytes()) != GOLD_SHA:
        raise ValueError('frozen gold hash mismatch')
    cfg, uni, all_records = b_arm.base_requests()
    if cfg.provider != 'openai':
        raise ValueError('unexpected provider')
    system = (HERE / 'simple-new-question-prompt.txt').read_text()
    src = json.loads((HERE / 'source-only-inputs.json').read_text())
    result = []
    for ident in IDS:
        base = next(x for x in all_records if x['item']['input_id'] == ident)
        saved = next(x for x in src if x['input_id'] == ident)
        if base['shown'] != saved['questions'] or base['item']['text'] != saved['article']:
            raise ValueError('saved article or prior questions mismatch')
        user = base['user']
        category = user[:user.index('[Subjects]')]
        subjects = user[user.index('[Subjects]'):user.index('[What to read out]')]
        # An earlier request supplies only an approximate month but asks the model to use it as a day.
        if subjects.count('; use that day as the due date.') != 1:
            raise ValueError('unexpected fiscal note')
        subjects = subjects.replace('; use that day as the due date.', '.', 1)
        old_fiscal_header = 'Fiscal-year note (a numeric thesis takes its year and due date from it):'
        if subjects.count(old_fiscal_header) != 1:
            raise ValueError('unexpected fiscal header')
        subjects = subjects.replace(old_fiscal_header, 'Fiscal-year context for the company\'s own quantities:', 1)
        q = user[user.index('[Open questions immediately before this item]'):user.index('[Research groups]')]
        item = base['item']
        article = f"[Article] id {ident}; date {item['publication_day']}; title {item['title']}; publisher {item['publisher']}\n{item['text']}"
        payload = category + subjects + q + article
        setting = base['setting']
        request = model.build_request(setting, system, payload, schema(), 'new_question', cfg.provider)
        result.append({'item': item, 'shown': base['shown'], 'seq': base['seq'], 'setting': setting,
                       'system': system, 'user': payload, 'request': request})
    return cfg, result


def checked(answer, article):
    errors = model.check_schema(answer, schema())
    if errors:
        raise ValueError('schema: ' + '; '.join(errors))
    checked_questions = []
    for position, q in enumerate(answer['questions'], 1):
        checks = []
        for ev in q['evidence']:
            quote = ev['quote']
            normalized_quote = extraction.normalise(quote)
            exact = bool(quote.strip()) and quote in article
            normalized = bool(normalized_quote) and normalized_quote in extraction.normalise(article)
            checks.append({'exact': exact, 'normalized': normalized})
        checked_questions.append({'position': position, 'has_evidence': bool(checks), 'quotes': checks,
                                  'source_check_pass': bool(checks) and all(x['normalized'] for x in checks)})
    return checked_questions


def fake_tests(cfg, records):
    for r in records:
        empty = {'questions': []}
        assert checked(empty, r['item']['text']) == []
        phrase = r['item']['text'][:100]
        candidate = {'question': 'Will the outcome occur?', 'why_it_matters': 'It can affect the business.',
                     'why_not_already_covered': 'It is a distinct outcome.', 'how_and_when_to_check': 'The next public announcement.',
                     'evidence': [{'quote': phrase, 'what_it_shows': 'The source describes the outcome.', 'original_speaker': ''}]}
        response = {'questions': [candidate]}
        assert checked(response, r['item']['text'])[0]['source_check_pass']
        bad = copy.deepcopy(response)
        bad['questions'][0]['evidence'][0]['quote'] = 'Fabricated source wording which is absent.'
        assert not checked(bad, r['item']['text'])[0]['source_check_pass']
        bad['questions'][0]['evidence'][0]['quote'] = '  '
        assert not checked(bad, r['item']['text'])[0]['source_check_pass']
        missing = copy.deepcopy(response)
        missing['questions'][0]['evidence'] = []
        assert not checked(missing, r['item']['text'])[0]['source_check_pass']
        if not model.check_schema({'questions': [{'question': 'q'}]}, schema()):
            raise ValueError('invalid schema accepted')
        with tempfile.TemporaryDirectory(prefix='simple-question-fake-') as tmp:
            archive = model.Archive(str(Path(tmp) / 'archive.sqlite'))
            def fake(provider, request):
                if json.dumps(request) != json.dumps(r['request']):
                    raise ValueError('unexpected fake wire')
                return {'choices': [{'message': {'content': json.dumps(response)}}], 'usage': {}}
            answer = model.call(archive, cfg, r['setting'], r['system'], r['user'], schema(), 'new_question', 'extract', transport=fake)
            if answer.data != response or answer.cached:
                raise ValueError('fake call mismatch')
            archive.conn.close()
    print(f'Fake: {len(records)} requests; empty, valid quote, bad quote, empty evidence, bad schema, and wire controls passed.', flush=True)


def manifest(records):
    files = [Path(__file__).resolve(), HERE / 'simple-new-question-prompt.txt', HERE / 'simple-new-question-design.zh.md',
             HERE / 'source-only-inputs.json', GOLD]
    return {'gold_sha256': GOLD_SHA, 'files': {str(p): sha(p.read_bytes()) for p in files},
            'requests': [{'id': r['item']['input_id'], 'seq': r['seq'], 'question_count': len(r['shown']),
                          'question_sha256': sha(json.dumps(r['shown'], sort_keys=True).encode()),
                          'article_sha256': sha(r['item']['text'].encode()), 'wire_sha256': wire(r['request']),
                          'request': r['request']} for r in records]}


def send_one(cfg, r, out):
    path = out / r['item']['input_id'].replace(':', '_')
    path.mkdir()
    archive = model.Archive(str(path / 'archive.sqlite'))
    def transport(provider, actual):
        if provider != cfg.provider or json.dumps(actual) != json.dumps(r['request']):
            raise ValueError('sent wire differs from frozen preview')
        result = model.openai_transport(provider, actual)
        (path / 'response.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        return result
    try:
        answer = model.call(archive, cfg, r['setting'], r['system'], r['user'], schema(), 'new_question', 'extract', transport=transport)
        source_checks = checked(answer.data, r['item']['text'])
        status = 'ok' if all(x['source_check_pass'] for x in source_checks) else 'source_incomplete'
        result = {'status': status, 'id': r['item']['input_id'], 'answer': answer.data,
                  'source_checks': source_checks, 'request_sha256': answer.request_sha256,
                  'input_tokens': answer.input_tokens, 'output_tokens': answer.output_tokens}
    except Exception as exc:
        result = {'status': 'failed', 'id': r['item']['input_id'], 'error': repr(exc)}
    finally:
        archive.conn.close()
    (path / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(result['id'], result['status'], flush=True)
    return result


def main():
    if (len(sys.argv) != 3 or sys.argv[1] != '--preview') and (len(sys.argv) != 4 or sys.argv[1] != '--send'):
        raise SystemExit('usage: --preview absolute-new-directory | --send absolute-new-directory reviewed-manifest-sha256')
    out = Path(sys.argv[2])
    if not out.is_absolute() or out.exists():
        raise ValueError('output directory must be absolute and new')
    cfg, records = prepare()
    fake_tests(cfg, records)
    m = manifest(records)
    if sys.argv[1] == '--send':
        if sha(PREVIEW.read_bytes()) != sys.argv[3]:
            raise ValueError('reviewed manifest hash changed')
        if m != json.loads(PREVIEW.read_text()):
            raise ValueError('reviewed manifest no longer matches')
    out.mkdir(parents=True)
    (out / 'manifest.json').write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n')
    if sys.argv[1] == '--preview':
        return
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda r: send_one(cfg, r, out), records))
    (out / 'status.json').write_text(json.dumps({'status': 'complete' if all(r['status'] == 'ok' for r in results) else 'complete_with_refusals',
                                                'completed': sum(r['status'] in ('ok', 'source_incomplete') for r in results), 'total': len(records)}) + '\n')


if __name__ == '__main__':
    main()
