"""B may link only to question IDs in the snapshot it actually saw."""
import copy
import json
import re
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / 'src')]
import split_seven_day_poc as poc  # noqa: E402
from hivemind import config, model, testdb, universe  # noqa: E402


def test_b_schema_uses_current_question_ids_not_subject_ids():
    folder = ROOT / 'poc/data/split-fresh-seven-day-2026-11-05-v2/items/1289'
    if not folder.exists():
        pytest.skip('saved 1289 trace is not present')
    shown = json.loads((folder / 'shown.json').read_text())
    saved = json.loads((folder / 'b-answer.json').read_text())
    input_id = 'gnews:493a177a82af08d677bf3ac2'
    with testdb.open_db(str(poc.INPUT)) as db:
        item = testdb.item_of(db.execute('select * from items where input_id=?', (input_id,)).fetchone())
    cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    _, requests = poc.item_requests(cfg, uni, item, shown)
    schema = requests['b'][2]
    ids = {v['view_id'] for v in shown}
    pattern = schema['properties']['evidence']['items']['properties']['links']['items']['pattern']
    assert all(re.fullmatch(pattern, value) for value in ids)
    assert not re.fullmatch(pattern, 'v999999') and not re.fullmatch(pattern, 'research:1174ba36750a7b35ddb6')
    errors = model.check_schema(saved, schema)
    assert len(errors) == 3 and all('does not match' in x for x in errors)
    repaired = copy.deepcopy(saved)
    mapping = {v['object_id']: v['view_id'] for v in shown if sum(w['object_id'] == v['object_id'] for w in shown) == 1}
    for evidence in repaired['evidence']:
        evidence['links'] = [mapping.get(link, link) for link in evidence['links']]
    assert not model.check_schema(repaired, schema)
    assert not model.check_schema({'evidence': []}, schema)
    _, empty_requests = poc.item_requests(cfg, uni, item, [])
    empty_links = empty_requests['b'][2]['properties']['evidence']['items']['properties']['links']['items']
    assert 'pattern' not in empty_links
