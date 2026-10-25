"""D158 / 06 ladder rule 5: the next-year limit is numeric, not a deadline limit on events."""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import extraction, universe


def test_stored_future_deployment_survives_while_capacity_is_refused():
    """The real call lost both c1 (2028 capacity) and c2 (2028 deployment); only c2 should return."""
    with sqlite3.connect(f'file:{ROOT}/poc/data/keyed-2026-10-25/archive-T2.sqlite?mode=ro', uri=True) as db:
        raw = json.loads(db.execute('select answer_json from model_calls where call_id=217').fetchone()[0])
    with sqlite3.connect(f'file:{ROOT}/poc/data/items-window-tags2-2026-10-24.sqlite?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        item = dict(db.execute('select * from items where input_id=?', (
            'nvidianews:naver-nvidia-and-brookfield-to-expand-koreas-national-ai-factory-infrastructure-buildout',)).fetchone())
    evidence, candidates, _ = extraction.sift(raw, item, item['text'], set(), universe.load(ROOT / 'poc/universe.json'))
    assert [c['id'] for c in candidates] == ['c2']
    assert len(evidence) == 3 and all(e['links'] == ['c2'] for e in evidence)
