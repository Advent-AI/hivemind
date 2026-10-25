"""Harness plumbing only: real stored answers through a fake provider, not model-quality evidence."""
import copy
import json
from pathlib import Path
import re
import shutil
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'poc'))
from concurrency_study import ingestion
from concurrency_study.budget import GuardedTransport

ARTIFACTS = Path(__file__).resolve().parent
raw = {}
with ingestion.readonly(ARTIFACTS / 'inputs/archive.sqlite') as db:
    for row in db.execute("select request_json,answer_json from model_calls where purpose='extract' and config_version='poc-v23'"):
        req = json.loads(row['request_json'])
        found = re.search(r'^\[Item\] id (.+?), category ', req['messages'][1]['content'], re.M)
        if found and found[1] in ingestion.INPUTS:
            raw[found[1]] = json.loads(row['answer_json'])
assert len(raw) == 3


def remap(value):
    if isinstance(value, dict):
        return {k: remap(v) for k, v in value.items()}
    if isinstance(value, list):
        return [remap(v) for v in value]
    if isinstance(value, str) and re.fullmatch(r'v\d+', value) and int(value[1:]) >= 15:
        return 'v' + str(int(value[1:]) - 2)  # Omitted INTC's two unrelated views in this selected-subset fixture.
    return value


def prepare(provider, req):
    def send():
        if provider == 'jev':
            answers = {}
            for key, q in req['questions'].items():
                if q['type'] == 'noul':
                    answers[key] = {'type': 'noul', 'noul': 0.05}
                else:
                    pick = 'same_statement' if key.startswith('piece__v13__') else 'different'
                    answers[key] = {'type': 'choice', 'choice': pick, 'confidence': 1,
                                    'probabilities': {k: int(k == pick) for k in q['criteria']}}
            return {'model': req['model'], 'answers': answers, 'usage': {'input_tokens': 1000, 'output_tokens': 100}}
        prompt = req['messages'][1]['content']
        if req['response_format']['json_schema']['name'] == 'extraction':
            ident = re.search(r'^\[Item\] id (.+?), category ', prompt, re.M)[1]
            answer = remap(copy.deepcopy(raw[ident]))
        else:
            answer = {'rung': 1, 'reasons': 'The supplied source reports the project plan.',
                      'cites': list(dict.fromkeys(re.findall(r'^- (e\d+) \[', prompt, re.M))), 'cites_views': [],
                      'pushes': [], 'changed': True, 'why_changed': 'The source adds a project statement.'}
        return {'model': req['model'], 'choices': [{'message': {'content': json.dumps(answer)}}],
                'usage': {'prompt_tokens': 1000, 'completion_tokens': 100}}
    return send


with tempfile.TemporaryDirectory() as name:
    directory = Path(name)
    for file in ('items.sqlite', 'ordered-baseline.sqlite', 'protected-before.json'):
        shutil.copyfile(ARTIFACTS / file, directory / file)
    (directory / 'study.json').write_text(json.dumps(ingestion.contract(directory)))
    transport = ingestion.StudyTransport(GuardedTransport(directory / 'budget.sqlite', prepare, max_calls=144))
    for trial in ('control-1', 'concurrent-1'):
        ingestion.run_trial(directory, trial, transport=transport)
        result = json.loads((directory / trial / 'result.json').read_text())
        print(trial, 'structural errors', result['audit']['errors'], 'events', [e['event'] for e in result['events']], flush=True)
    mutant = directory / 'substituted'; mutant.mkdir()
    for name in ('views.sqlite', 'archive.sqlite'):
        shutil.copyfile(directory / 'control-1' / name, mutant / name)
    with sqlite3.connect(mutant / 'views.sqlite') as db:
        db.execute('drop trigger handovers_no_update')
        db.execute('update handovers set handover_json=? where seq=21',
                   (json.dumps({'evidence': [], 'candidates': [], 'dropped': [], 'new_groups': []}),))
    cfg, uni = ingestion.configuration()
    caught = ingestion.audit(directory, 'substituted', cfg, uni)['errors']
    assert any('bound request answer' in error for error in caught), caught
    print('substituted-handover mutant caught', caught, flush=True)
