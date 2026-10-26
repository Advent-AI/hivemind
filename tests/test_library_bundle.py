"""D181: the library read surface preserves collected groups and dated records."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import bundle, service
from hivemind.views import store

LEDGER = ROOT / 'poc/data/english-v23-jev-2026-10-25/views.sqlite'
ITEMS = ROOT / 'poc/data/items-window-tags2-2026-10-24.sqlite'


def test_full_collected_library_and_selected_group_members_are_exact():
    ledger, items = service.open_ledger(LEDGER), store.open_read_only(ITEMS)
    try:
        payload = bundle.library(ledger, items)
        assert payload['coverage'] == 'library'
        assert len(payload['views']) == 90 and len(payload['groups']) == 18
        assert sum(len(g['members']) for g in payload['groups']) == 51
        assert all(v['identity'] is not None for v in payload['views'])
        seen = {}
        for view in payload['views']:
            for evidence in view['evidence']:
                seen[evidence['id']] = evidence
                expected = ledger.execute('select count(*) from evidence_sources where evidence_id=?', (evidence['id'],)).fetchone()[0]
                assert len(evidence['sources']) == expected == evidence['outlets']
        assert len(seen) == 534
        assert sum(len(e['sources']) > 1 for e in seen.values()) == 99
        assert sum(e['replaced_by'] is not None for e in seen.values()) == 15
        group = next(g for g in payload['groups'] if g['id'] == 'g1')
        assert len(group['members']) == 6
        partial = bundle.thesis_bundles(ledger, items, ['v7'])
        assert partial['coverage'] == 'selection'
        assert next(g for g in partial['groups'] if g['id'] == 'g1')['members'] == [m for m in group['members'] if m['thesis_id'] == 'v7']
        earlier = bundle.library(ledger, items, '2026-07-23')
        assert len(earlier['views']) < len(payload['views'])
        assert all(m['day'] <= earlier['as_of'] for g in earlier['groups'] for m in g['members'])
        assert ledger.total_changes == items.total_changes == 0
        assert not ledger.in_transaction and not items.in_transaction
    finally:
        ledger.close()
        items.close()


def test_projection_preserves_waiting_resolution_replacement_and_succession_dates(tmp_path):
    """D181 state table: current resolutions cannot leak into an earlier snapshot."""
    ledger = store.open_db(tmp_path / 'views.sqlite')
    try:
        for seq, day in enumerate(['2026-07-24', '2026-07-25', '2026-07-26'], 1):
            store.insert(ledger, 'processing_steps', input_id=f'item-{seq}', sequence_no=seq, publication_day=day)
            store.insert(ledger, 'days_completed', day=day, seq=seq)
        for n in [1, 2]:
            store.create_view(ledger, view_id=f'v{n}', object_id='NVDA', object_kind='company', kind='asset', looks_at='Production shipments', question='Will production shipments begin?', due_day='2026-12-31', year='2026', rungs=[{'label': 'Yes', 'condition': 'Shipments begin'}, {'label': 'No', 'condition': 'Shipments do not begin'}], seq=n, input_id=f'item-{n}', created_at='2026-07-24T00:00:00Z')
        dep = store.insert(ledger, 'dependencies', view_id='v1', depends_on=None, wait_chain_view_id='v2', wait_year='2027', direction='same', seq=1)
        store.insert(ledger, 'dependency_resolutions', dependency_id=dep, resolved_to='v2', seq=3, reason='next period available')
        store.insert(ledger, 'successions', view_id='v2', succeeds='v1', seq=3)
        for n in [1, 2]:
            store.insert(ledger, 'evidence', evidence_id=f'e{n}', one_line='The company expects production shipments.', quote='We expect production shipments.', tier='party_statement', speaker='NVIDIA', original_who='NVIDIA', created_seq=n, created_from_input=f'item-{n}')
            store.insert(ledger, 'evidence_links', view_id='v1', evidence_id=f'e{n}', seq=n)
            store.insert(ledger, 'evidence_sources', evidence_id=f'e{n}', input_id=f'item-{n}', publication_day=f'2026-07-{23+n}', seq=n)
        store.insert(ledger, 'replacements', old_evidence_id='e1', new_evidence_id='e2', said_day='2026-07-24', seq=3)
        ledger.commit()
        before = bundle.thesis_bundles(ledger, None, ['v1'], '2026-07-25')['views'][0]
        after = bundle.thesis_bundles(ledger, None, ['v1'], '2026-07-26')['views'][0]
        assert before['dependencies'][0]['depends_on'] is None
        assert before['dependencies'][0]['resolutions'] == before['successions'] == []
        assert before['evidence'][0]['replaced_by'] is None
        assert after['dependencies'][0]['resolutions'] == [{'target': 'v2', 'day': '2026-07-26', 'seq': 3}]
        assert after['successions'] == [{'thesis_id': 'v2', 'relation': 'next', 'day': '2026-07-26'}]
        assert after['evidence'][0]['replaced_by']['day'] == '2026-07-26'
        assert after['evidence'][0]['replaced_by']['said_day'] == '2026-07-24'
        assert json.dumps(after)
    finally:
        ledger.close()
