"""Replay stored B records to expose the effects and limits of the offline identity prototype."""
import copy
import json
from pathlib import Path

import b_arm
import b_matter_handover_poc as poc
import run_poc

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / 'poc/data/parallel-b-link-2026-11-05-v2'


class Dummy:
    call_id = 0
    request_sha256 = 'offline'
    cached = False
    cost_usd = 0


def fields(row):
    return tuple(row[k] if k != 'links' else tuple(row[k]) for k in
                 ('quote', 'one_line', 'speaker', 'original_who', 'original_day', 'tier', 'event_time', 'links'))


def run():
    _, uni, records = b_arm.base_requests()
    byid = {r['item']['input_id']: r for r in records}
    paths = list(RUN.glob('*/result.json'))
    if len(paths) != 60:
        raise ValueError('expected all 60 stored answers')
    unchanged, changed = 0, []
    for path in paths:
        row = json.loads(path.read_text())
        r = byid[row['id']]
        data = copy.deepcopy(row['answer'])
        # Reassign code-owned identities in both paths; preserve original stored data.
        for i, evidence in enumerate(data['evidence'], 1):
            evidence['id'] = 'e' + str(i)
        before = run_poc.handover(data, r, uni, Dummy())
        after = poc.handover_by_record(data, r, uni, Dummy())
        if [fields(e) for e in before['evidence']] == [fields(e) for e in after['evidence']]:
            unchanged += 1
        else:
            changed.append((row['id'], row['variant'], row['draw'], before, after))
    assert unchanged == 58 and len(changed) == 2
    for ident, variant, draw, before, after in changed:
        assert ident == 'gnews:3df0bbc8aff2c1d008bc0a32' and draw == 3
        assert len(before['evidence']) == 1 and len(after['evidence']) == 2
        assert '$81.6 billion' in after['evidence'][0]['one_line']
        assert '$75.2 billion' in after['evidence'][1]['one_line']
        assert [e['links'] for e in after['evidence']] == [['v2'], ['v10']]
    sample = json.loads((RUN / 'gnews_3df0bbc8aff2c1d008bc0a32-control-3/result.json').read_text())['answer']
    r = byid['gnews:3df0bbc8aff2c1d008bc0a32']
    bad = copy.deepcopy(sample)
    bad['evidence'][0]['quote'] = 'A fabricated quote absent from the source.'
    checked = poc.handover_by_record(bad, r, uni, Dummy())
    assert not any(e['id'] == 'e1' for e in checked['evidence'])
    assert any(reason == 'quote not in item' for _, reason in checked['dropped'])
    bad = copy.deepcopy(sample)
    bad['evidence'][0]['links'] = ['missing-view']
    checked = poc.handover_by_record(bad, r, uni, Dummy())
    assert not any(e['id'] == 'e1' for e in checked['evidence'])
    # This exposes an unresolved limit: identical claims are also kept twice.
    duplicate = copy.deepcopy(sample)
    duplicate['evidence'] = [copy.deepcopy(sample['evidence'][0]), copy.deepcopy(sample['evidence'][0])]
    checked = poc.handover_by_record(duplicate, r, uni, Dummy())
    assert len(checked['evidence']) == 2 and checked['identity'][0]['raw_id'] == checked['identity'][1]['raw_id']
    assert checked['evidence'][0]['id'] != checked['evidence'][1]['id']
    print('60 saved B answers: 58 unchanged, 2 preserve both distinct same-quote summaries.')
    print('Bad quote and nonexistent link are refused; exact semantic duplicates remain twice and require matching.')


if __name__ == '__main__':
    run()
