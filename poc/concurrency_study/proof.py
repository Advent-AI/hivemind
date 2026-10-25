"""One check shared by the study harnesses: every accepted handover answers the exact request built from the ledger
committed before its item, and, where the parallel runner reported which request it accepted, that same request."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'docs/research/2026-10-25-day-batch-review'))
from snapshot_proof import snapshot  # noqa: E402
from hivemind import extraction  # noqa: E402
from hivemind.parallel_day import extraction_key  # noqa: E402
from hivemind.views import store  # noqa: E402


def accepted_requests(events):
    """The request each item's turn accepted, from a ParallelDay event list."""
    return {e['input_id']: e['request'] for e in events if e['event'] in ('reused', 'reextracted')}


def handover_errors(conn, items, cfg, uni, first, answer_for, accepted=None):
    """Rebuild each accepted request from its committed prefix; `answer_for(key)` returns the archived answer JSON or
    None. Returns the problems found and the rebuilt request per input."""
    by_id = {i['input_id']: i for i in items}
    errors, keys = [], {}
    for hand in conn.execute('select * from handovers where seq>=? order by seq', (first,)):
        item = by_id[hand['input_id']]
        before = snapshot(conn, hand['seq'], exclude_unordered=True)
        try:
            objects = [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
            shown = store.views_for_prompt(before, objects)
            groups = store.groups_for_prompt(before, objects, item.get('title') or '')
            key = extraction_key(cfg, item, item['text'], shown, uni, groups)
        finally:
            before.close()
        keys[item['input_id']] = key
        if accepted is not None and accepted.get(item['input_id']) != key:
            errors.append('the runner accepted another request: ' + item['input_id'])
        answer = answer_for(key)
        if answer is None:
            errors.append('accepted handover has no exact current-prefix request: ' + item['input_id'])
            continue
        version = cfg.extraction_setting(item['category']).prompt_version.rpartition('-')[2]
        evidence, candidates, dropped, new_groups = extraction.sift_with_groups(
            json.loads(answer), item, item['text'], {v['view_id'] for v in shown}, uni,
            english=extraction.is_english(version), shown_group_ids=[g['group_id'] for g in groups])
        expected = {'evidence': evidence, 'candidates': candidates, 'dropped': dropped, 'new_groups': new_groups}
        if json.loads(json.dumps(expected)) != json.loads(hand['handover_json']):
            errors.append('accepted handover differs from its bound answer: ' + item['input_id'])
    if len(keys) != len(items):
        errors.append(f'{len(keys)} handovers for {len(items)} items')
    return errors, keys
