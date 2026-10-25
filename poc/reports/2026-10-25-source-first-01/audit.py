"""D162 artifact checks; semantic labels come from explicit reading, not a keyword judge."""
import json
import sqlite3
from pathlib import Path

OUT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def main():
    manifest, statuses, budget, annotations = [read(OUT / name) for name in
        ('manifest.json', 'status.json', 'budget.json', 'review-labels.json')]
    assert set(statuses) == set(manifest['labels']) == set(annotations)
    assert all(a['status'] == 'complete' for a in budget['attempts']), 'Incomplete paid request'
    output = {'semantic_annotation': 'Assistant reading of full sources and stored answers; not independent human gold',
              'attempts': len(budget['attempts']), 'estimated_usd': budget['reserved_or_spent'], 'samples': {}}
    for label in manifest['labels']:
        folder = OUT / label
        db = sqlite3.connect(f'file:{folder}/views.sqlite?mode=ro', uri=True)
        db.row_factory = sqlite3.Row
        archive = sqlite3.connect(f'file:{folder}/calls.sqlite?mode=ro', uri=True)
        archive.row_factory = sqlite3.Row
        counts = dict.fromkeys(('completed_inputs', 'raw_candidates', 'kept_candidates', 'raw_evidence',
            'kept_evidence', 'memberships_checked', 'sources_checked', 'prior_members_shown',
            'later_candidates', 'selected_observations', 'explicit_omissions', 'handoffs_checked'), 0)
        counts.update(drops=[], omissions=[], items=[])
        for n in range(1, len(manifest['item_ids']) + 1):
            path = folder / f'item{n}'
            if not (path / 'result.json').exists():
                assert statuses[label] != 'complete', 'Completed sample has missing input result'
                counts['items'].append({'input': n, 'completed': False})
                continue
            raw, handover, result, context = [read(path / f'{name}.json') for name in
                ('extraction', 'handover', 'result', 'context')]
            assert result['input_id'] == manifest['item_ids'][n - 1] and result['seq'] == n
            counts['completed_inputs'] += 1
            for prefix, data in (('raw', raw), ('kept', handover)):
                for key in ('candidates', 'evidence'):
                    counts[prefix + '_' + key] += len(data[key])
            counts['later_candidates'] += len(raw['candidates']) if n > 1 else 0
            counts['drops'] += [{'input': n, 'id': eid, 'reason': reason} for eid, reason in handover['dropped']]
            before_members = {m['view_id'] for m in context['before']['thread_members']}
            assert before_members <= {v['view_id'] for v in context['shown']}
            counts['prior_members_shown'] += len(before_members)
            expected_bindings = set()
            matched = read(path / 'matching.json')['outcomes'] if (path / 'matching.json').exists() else {}
            for c in handover['candidates']:
                vid = result['new_views'].get(c['id'])
                if vid:
                    assert db.execute('select question from views where view_id=?', (vid,)).fetchone()[0] == c['question']
                elif matched.get(c['id'], [''])[0] == '归入已有的':
                    vid = matched[c['id']][1]
                if not vid:
                    continue
                for ref in c['thread_ids']:
                    definition = next((g for g in raw['threads'] if g['id'] == ref), None)
                    if definition:
                        rows = list(db.execute('select thread_id from threads where name=? and scope=? and seq=? and input_id=?',
                            (definition['name'], definition['scope'], n, result['input_id'])))
                        assert len(rows) == 1
                        gid = rows[0][0]
                    else:
                        gid = ref
                    expected_bindings.add((c['id'], vid, gid))
                    assert db.execute('select 1 from thread_members where thread_id=? and view_id=? and seq<=?', (gid, vid, n)).fetchone()
            assert expected_bindings == {(b['candidate_id'], b['view_id'], b['thread_id']) for b in result['bindings']}
            counts['memberships_checked'] += sum(b['new_membership'] for b in result['bindings'])
            for eid in set(result['evidence_ids'].values()):
                assert db.execute('select 1 from evidence_sources where evidence_id=? and input_id=? and seq=?',
                                  (eid, result['input_id'], n)).fetchone()
                counts['sources_checked'] += 1
            if label.startswith('grouped'):
                source, provenance = [read(path / f'{name}.json') for name in ('source', 'reader-calls')]
                counts['selected_observations'] += len(source['observations'])
                calls = []
                for stage, info in provenance.items():
                    if info is None:
                        continue
                    call = archive.execute('select * from model_calls where call_id=?', (info['call_id'],)).fetchone()
                    assert call['request_sha256'] == info['request_sha256']
                    assert call['purpose'] == {'source': 'source_selection', 'organisation': 'question_construction'}[stage]
                    calls.append(call)
                assert abs(sum(c['cost_usd'] for c in calls) - handover['cost_usd']) < 1e-10
                assert handover['call_id'] == calls[-1]['call_id'] and handover['request_sha256'] == calls[-1]['request_sha256']
                if source['observations']:
                    organised = read(path / 'organisation.json')
                    assert set(organised['dispositions']) == {e['id'] for e in source['observations']}
                    expected = []
                    for e in source['observations']:
                        d = organised['dispositions'][e['id']]
                        assert bool(d['links']) != bool(d['omit_reason'].strip())
                        if d['links']:
                            expected.append(dict(e, links=d['links']))
                        else:
                            counts['explicit_omissions'] += 1
                            counts['omissions'].append({'input': n, 'id': e['id'], 'one_line': e['one_line'], 'reason': d['omit_reason']})
                    assert raw['evidence'] == expected, 'Selected content changed or silently omitted'
                    for c in raw['candidates']:
                        assert c['evidence_ids'] == [e['id'] for e in expected if c['id'] in e['links']]
                else:
                    assert provenance['organisation'] is None and raw == {'evidence': [], 'candidates': [], 'threads': []}
                counts['handoffs_checked'] += 1
            counts['items'].append({'input': n, 'completed': True, 'candidates': len(raw['candidates']),
                                   'evidence': len(raw['evidence']), 'written_sources': len(set(result['evidence_ids'].values()))})
        if statuses[label] == 'complete':
            checks = read(folder / 'checks.json')
            assert checks['history_unchanged'] and checks['resend_skipped']
        assert db.execute('select count(*) from thread_members').fetchone()[0] == counts['memberships_checked']
        assert db.execute('select count(*) from evidence_sources').fetchone()[0] == counts['sources_checked']
        for eid in annotations[label]['risk_evidence']:
            assert db.execute('select 1 from thread_members m join evidence_links l on l.view_id=m.view_id join evidence e on e.evidence_id=l.evidence_id where e.evidence_id=? and e.tier=?', (eid, '第三方看法')).fetchone()
        counts['call_details'] = [dict(row) for row in archive.execute('select call_id,purpose,input_tokens,output_tokens,cost_usd,seconds,prompt_chars from model_calls order by call_id')]
        counts['calls'] = len(counts['call_details'])
        for key in ('input_tokens', 'output_tokens', 'cost_usd', 'seconds', 'prompt_chars'):
            counts[key] = sum(c[key] for c in counts['call_details'])
        output['samples'][label] = {'status': statuses[label], 'counts': counts, 'review': annotations[label]}
        db.close()
        archive.close()
    output['totals'] = {key: sum(s['counts'][key] for s in output['samples'].values()) for key in
        ('completed_inputs', 'raw_candidates', 'kept_candidates', 'raw_evidence', 'kept_evidence',
         'memberships_checked', 'sources_checked', 'prior_members_shown', 'later_candidates',
         'selected_observations', 'explicit_omissions', 'handoffs_checked', 'calls', 'cost_usd', 'seconds', 'input_tokens', 'output_tokens', 'prompt_chars')}
    assert output['totals']['calls'] == output['attempts']
    # Archive rounds each cost to six decimal places; the transport keeps unrounded estimates.
    rounded_expected = 0
    for sample in output['samples'].values():
        for call in sample['counts']['call_details']:
            exact = call['input_tokens'] / 1e6 * 1.25 + call['output_tokens'] / 1e6 * 10.0
            assert call['cost_usd'] == round(exact, 6)
            rounded_expected += round(exact, 6)
    assert abs(output['totals']['cost_usd'] - rounded_expected) < 1e-12
    assert abs(sum(a['estimated_usd'] for a in budget['attempts']) - output['estimated_usd']) < 1e-12
    output['archive_rounding_difference_usd'] = output['totals']['cost_usd'] - output['estimated_usd']
    (OUT / 'audit.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(output['totals'], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
