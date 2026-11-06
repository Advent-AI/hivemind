"""Re-send the saved B request with the shown-question pattern in its schema."""
import copy
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / 'src')]
import split_seven_day_poc as poc  # noqa: E402
from hivemind import config, model, testdb  # noqa: E402

SOURCE = ROOT / 'poc/data/split-fresh-seven-day-2026-11-05-v2/items/1289'
OUT = ROOT / 'poc/data/b-question-id-pattern-probe-2026-11-05'


def main():
    request = json.loads((SOURCE / 'b-request.json').read_text())
    shown = json.loads((SOURCE / 'shown.json').read_text())
    system, user = [m['content'] for m in request['messages']]
    original_schema = request['response_format']['json_schema']['schema']
    schema = copy.deepcopy(original_schema)
    ids = list(dict.fromkeys(v['view_id'] for v in shown))
    schema['properties']['evidence']['items']['properties']['links']['items']['pattern'] = '^(?:' + '|'.join(re.escape(value) for value in ids) + ')$'
    cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
    db = testdb.open_db(str(poc.INPUT))
    item = testdb.item_of(db.execute('select * from items where input_id=?', ('gnews:493a177a82af08d677bf3ac2',)).fetchone())
    db.close()
    setting = cfg.extraction_setting(item['category'])
    original = model.build_request(setting, system, user, original_schema, 'extraction', cfg.provider)
    if json.dumps(original) != json.dumps(request):
        raise ValueError('saved B request does not match current production-built bytes')
    spec = (system, user, schema, 'extraction')
    OUT.mkdir(parents=True, exist_ok=False)
    answer = poc.call(cfg, setting, 'b', spec, OUT)
    if poc.completed_answer(cfg, setting, 'b', spec, OUT) != answer:
        raise ValueError('provider answer not verified')
    source_backed = sum(poc.source_quote(e['quote'], item['text'][:poc.extraction.MAX_TEXT_CHARS]) is not None for e in answer['evidence'])
    print(json.dumps({'evidence': len(answer['evidence']), 'source_backed': source_backed,
                      'links': [e['links'] for e in answer['evidence']]}, ensure_ascii=False))


if __name__ == '__main__':
    main()
