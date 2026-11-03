"""Verify shared request builders against the preserved sequential archives; no network."""
import json
from pathlib import Path
import sqlite3
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import jev, model

totals = {'archives': 0, 'requests': 0, 'openai_rebuilt': 0, 'jev_rebuilt': 0}
for arm in ('jev', 'llm'):
    path = ROOT / f'poc/data/english-v23-{arm}-2026-10-25/archive.sqlite'
    with sqlite3.connect(path.as_uri() + '?mode=ro', uri=True) as db:
        totals['archives'] += 1
        for encoded, sha in db.execute('select request_json,request_sha256 from model_calls'):
            request = json.loads(encoded)
            actual_json, actual_sha = model.request_identity(request)
            assert actual_json == encoded
            assert actual_sha == sha[:64]
            if 'state' in request:
                rebuilt = jev.request_for(SimpleNamespace(model=request['model']), request['state'], request['questions'])
                totals['jev_rebuilt'] += 1
            else:
                shape = request['response_format']['json_schema']
                setting = SimpleNamespace(model=request['model'], max_output_tokens=request['max_completion_tokens'],
                                          reasoning_effort=request.get('reasoning_effort'), temperature=0.2)
                rebuilt = model.build_request(setting, request['messages'][0]['content'], request['messages'][1]['content'],
                                              shape['schema'], shape['name'], 'openai')
                totals['openai_rebuilt'] += 1
            assert model.request_identity(rebuilt) == (actual_json, actual_sha)
            totals['requests'] += 1
assert totals['requests'] > 0 and totals['jev_rebuilt'] > 0 and totals['openai_rebuilt'] > 0
print(json.dumps(totals, indent=2))
