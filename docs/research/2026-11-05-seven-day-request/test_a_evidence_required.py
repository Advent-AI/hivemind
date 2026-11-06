"""A may pass, or propose a question with article evidence; never an empty candidate."""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / 'src')]
import split_seven_day_poc as poc  # noqa: E402
from hivemind import config, model, testdb, universe  # noqa: E402


def test_a_requires_evidence_for_each_proposed_question_but_accepts_pass():
    folder = ROOT / 'poc/data/split-fresh-seven-day-matching-v3-2026-11-05/items/1212'
    if not folder.exists():
        pytest.skip('saved 1212 trace is not present')
    shown = json.loads((folder / 'shown.json').read_text())
    answer = json.loads((folder / 'a-answer.json').read_text())
    with testdb.open_db(str(poc.INPUT)) as db:
        item = testdb.item_of(db.execute('select * from items where input_id=?', ('gnews:e02d9195cb9bb0a245bd15a0',)).fetchone())
    cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
    _, requests = poc.item_requests(cfg, universe.load(str(ROOT / 'poc/universe.json')), item, shown)
    schema = requests['a'][2]
    assert not model.check_schema({'questions': []}, schema)
    # split version 2 (2026-11-05): the saved answer's why_not_already_covered is now the closest question and what separates it
    answer = {'questions': [dict({k: v for k, v in q.items() if k != 'why_not_already_covered'}, closest_existing_question='none',
                                 what_separates_it=q['why_not_already_covered']) for q in answer['questions']]}
    errors = model.check_schema(answer, schema)
    assert errors == ['$.questions[0].evidence: fewer than 1 items']
