"""Re-send the stopped A request with one evidence item required per proposed question."""
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / 'src')]
import split_seven_day_poc as poc  # noqa: E402
from hivemind import config, model, testdb  # noqa: E402

SOURCE = ROOT / 'poc/data/split-fresh-seven-day-matching-v3-2026-11-05/items/1212'
OUT = ROOT / 'poc/data/a-evidence-required-probe-2026-11-05'


def main():
    request = json.loads((SOURCE / 'a-request.json').read_text())
    system, user = [m['content'] for m in request['messages']]
    original_schema = request['response_format']['json_schema']['schema']
    schema = copy.deepcopy(original_schema)
    schema['properties']['questions']['items']['properties']['evidence']['minItems'] = 1
    cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
    db = testdb.open_db(str(poc.INPUT))
    item = testdb.item_of(db.execute('select * from items where input_id=?', ('gnews:e02d9195cb9bb0a245bd15a0',)).fetchone())
    db.close()
    setting = cfg.extraction_setting(item['category'])
    if json.dumps(model.build_request(setting, system, user, original_schema, 'new_question', cfg.provider)) != json.dumps(request):
        raise ValueError('saved A request does not match current production-built bytes')
    spec = (system, user, schema, 'new_question')
    OUT.mkdir(parents=True, exist_ok=False)
    answer = poc.call(cfg, setting, 'a', spec, OUT)
    if poc.completed_answer(cfg, setting, 'a', spec, OUT) != answer:
        raise ValueError('provider answer not verified')
    for question in answer['questions']:
        if any(poc.source_quote(e['quote'], item['text'][:poc.extraction.MAX_TEXT_CHARS]) is None for e in question['evidence']):
            raise ValueError('new question evidence does not appear in source')
    print(json.dumps({'questions': len(answer['questions']), 'answer': answer}, ensure_ascii=False))


if __name__ == '__main__':
    main()
