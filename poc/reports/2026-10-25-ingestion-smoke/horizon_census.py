"""Count actual horizon refusals on stored v23 responses, including this serial control."""
import json
from pathlib import Path
import re
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import extraction, universe

BASE = Path(__file__).resolve().parent
sources = {
    'stored-jev': ROOT / 'poc/data/english-v23-jev-2026-10-25/archive.sqlite',
    'stored-llm': ROOT / 'poc/data/english-v23-llm-2026-10-25/archive.sqlite',
    'fresh-serial': BASE / 'control-1/archive.sqlite',
}
uni = universe.load(ROOT / 'poc/universe.json')
out = {}
with sqlite3.connect((BASE / 'inputs/items.sqlite').as_uri() + '?mode=ro', uri=True) as inputs:
    inputs.row_factory = sqlite3.Row
    for name, path in sources.items():
        with sqlite3.connect(path.as_uri() + '?mode=ro', uri=True) as archive:
            archive.row_factory = sqlite3.Row
            cases, judged = [], 0
            cfg = 'poc-v23-llm' if name == 'stored-llm' else 'poc-v23'
            for row in archive.execute("select * from model_calls where purpose='extract' and config_version=? and answer_json is not null", (cfg,)):
                req, answer = json.loads(row['request_json']), json.loads(row['answer_json'])
                prompt = req['messages'][1]['content']
                ident = re.search(r'^\[Item\] id (.+?), category ', prompt, re.M)[1]
                item = dict(inputs.execute('select * from items where input_id=?', (ident,)).fetchone())
                shown = set(re.findall(r'^  - (v\d+) \(', prompt, re.M))
                _, _, drops = extraction.sift(answer, item, item['text'], shown, uni, english=True)
                judged += 1
                for cid, reason in drops:
                    if not re.fullmatch(r'year (?:FY)?\d{4} is beyond next year: not opened \(06-views 不开\)', reason):
                        continue
                    candidate = next(c for c in answer['candidates'] if c['id'] == cid)
                    cases.append({'input_id': ident, 'call_id': row['call_id'], 'candidate': candidate,
                                  'reason': reason, 'publication_day': item['publication_day']})
            out[name] = {'answers_judged': judged, 'horizon_refusals': len(cases), 'cases': cases}
print(json.dumps(out, indent=2, ensure_ascii=False))
