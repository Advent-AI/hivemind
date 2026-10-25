"""D159: count financing records and trace the source-to-question change without model calls."""
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import extraction, model, universe

AFFECTED_INPUT = 'gnews:eb74b9d16d227f0c2b7a39d8'


def audit():
    records = []
    for path in sorted((ROOT / 'poc/data').glob('views-2026-10-25-v15-*.sqlite')):
        with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as db:
            db.row_factory = sqlite3.Row
            for row in db.execute("select v.* from views v join view_keys k using(view_id) where k.measure='financing_amount'"):
                records.append({'ledger': path.name, **dict(row), 'rungs': [dict(r) for r in db.execute(
                    'select * from rungs where view_id=? order by position', (row['view_id'],))]})
    source = ROOT / 'poc/data/keyed-2026-10-25/archive-T2.sqlite'
    with sqlite3.connect(f'file:{source}?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        traces = []
        for row in db.execute("select * from model_calls where purpose='extract'"):
            request = json.loads(row['request_json'])
            match = re.search(r'【信息】编号 (\S+?)，类别 ', request['messages'][1]['content'])
            if match and match.group(1) == AFFECTED_INPUT:
                traces.append(dict(row))
    assert len(records) == 29 and len(traces) == 1 and traces[0]['call_id'] == 460
    trace = traces[0]
    request, raw = json.loads(trace['request_json']), json.loads(trace['answer_json'])
    items = ROOT / 'poc/data/items-window-tags2-2026-10-24.sqlite'
    with sqlite3.connect(f'file:{items}?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        item = dict(db.execute('select * from items where input_id=?', (AFFECTED_INPUT,)).fetchone())
    item['object_identifiers'] = json.loads(item['object_identifiers'])
    shown = set(re.findall(r'^\s+- (v\d+)（', request['messages'][1]['content'], re.M))
    evidence, candidates, dropped = extraction.sift(raw, item, item['text'], shown, universe.load(ROOT / 'poc/universe.json'))
    assert len(candidates) == 1 and not dropped
    before = [r['condition'] for r in raw['candidates'][0]['rungs']]
    after = [r['condition'] for r in candidates[0]['rungs']]
    assert before == after
    return {'financing_records': len(records), 'affected_records': [(r['ledger'], r['view_id']) for r in records
            if r['created_from_input'] == AFFECTED_INPUT], 'source_call': trace['call_id'],
            'schema_errors': model.check_schema(raw, request['response_format']['json_schema']['schema']),
            'raw_conditions': before, 'current_sift_conditions': after, 'dropped': dropped,
            'evidence_kept': len(evidence), 'limitation': 'The semantic finding is source review, not a substring-based classifier.'}


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
