"""Read the fixed D157 experiment; exact membership checks, no semantic scoring."""
import argparse
import hashlib
import json
import sqlite3
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def audit(root):
    manifest = read(root / 'manifest.json')
    states = read(root / 'status.json')
    judged = 0
    samples = []
    refs, invalid, wire_requests = 0, [], 0
    for label in manifest['labels']:
        folder = root / label
        calls = [read(f) for f in sorted(folder.glob('call-*.json'))]
        assert calls and all(c['status'] == 'complete' for c in calls), (label, 'incomplete call')
        with sqlite3.connect(f'file:{folder}/calls.sqlite?mode=ro', uri=True) as conn:
            archived = {r[0] for r in conn.execute('select request_sha256 from model_calls')}
        actual = {hashlib.sha256(json.dumps(c['request'], sort_keys=True, ensure_ascii=False).encode()).hexdigest() for c in calls}
        assert actual == archived and len(calls) == len(archived), (label, 'archive or freshness mismatch')
        row = {'sample': label, 'status': states[label], 'calls': len(calls),
               'cost': round(sum(c['estimated_usd'] for c in calls), 6), 'seconds': round(sum(c['seconds'] for c in calls), 2), 'articles': []}
        for path in sorted(folder.glob('item*/extraction.json')):
            raw = read(path)
            context = read(path.parent / 'context.json')
            item = {'item': path.parent.name, 'raw_candidates': len(raw['candidates']), 'raw_evidence': len(raw['evidence'])}
            if 'threads' in raw:
                wire_requests += 1
                allowed = {g['id'] for g in raw['threads']} | {g['thread_id'] for g in context['offered']}
                for candidate in raw['candidates']:
                    for ref in candidate['thread_ids']:
                        refs += 1
                        if ref not in allowed:
                            invalid.append([label, path.parent.name, candidate['id'], ref])
            if (path.parent / 'handover.json').exists():
                handover = read(path.parent / 'handover.json')
                item.update(kept_candidates=len(handover['candidates']), kept_evidence=len(handover['evidence']), dropped=handover['dropped'])
            if (path.parent / 'result.json').exists():
                result = read(path.parent / 'result.json')
                item.update(new_views=len(set(result['new_views'].values())), bindings=len(result['bindings']), stored_evidence=len(result['snapshot']['evidence']))
                if 'threads' in raw:
                    before, after = context['before'], result['snapshot']
                    definitions = {g['id']: g for g in raw['threads']}
                    outcomes = read(path.parent / 'matching.json')['outcomes'] if (path.parent / 'matching.json').exists() else {}
                    expected = []
                    for candidate in handover['candidates']:
                        assert candidate['thread_ids'] == next(c['thread_ids'] for c in raw['candidates'] if c['id'] == candidate['id'])
                        vid = result['new_views'].get(candidate['id'])
                        decision = outcomes.get(candidate['id'])
                        if not vid and decision and decision[0] == '归入已有的':
                            vid = decision[1]
                        if not vid:
                            continue
                        for ref in candidate['thread_ids']:
                            if ref in definitions:
                                definition = definitions[ref]
                                matches = [g['thread_id'] for g in after['threads'] if g['name'] == definition['name'] and g['scope'] == definition['scope'] and g['seq'] == result['seq'] and g['input_id'] == result['input_id']]
                                assert len(matches) == 1, (label, 'new declaration mapping', ref)
                                gid = matches[0]
                            else:
                                gid = ref
                            expected.append((candidate['id'], vid, gid))
                    actual_bindings = [(b['candidate_id'], b['view_id'], b['thread_id']) for b in result['bindings']]
                    assert sorted(actual_bindings) == sorted(expected), (label, 'bindings', actual_bindings, expected)
                    pairs = lambda rows: {(r['view_id'], r['thread_id']) for r in rows}
                    assert pairs(after['thread_members']) == pairs(before['thread_members']) | {(v, g) for _, v, g in expected}, (label, 'stored members')
                    assert all(old in after['thread_members'] for old in before['thread_members']), (label, 'changed old member')
                    judged += len(expected)
            row['articles'].append(item)
        if states[label] == 'complete':
            assert not (folder / 'failed.json').exists()
            checks = read(folder / 'checks.json')
            assert checks['history_unchanged'] and checks['resend_skipped']
            final = read(folder / 'item2/result.json')['snapshot']
            with sqlite3.connect(f'file:{folder}/views.sqlite?mode=ro', uri=True) as conn:
                conn.row_factory = sqlite3.Row
                for table, rows in final.items():
                    if table != 'details':
                        assert [dict(r) for r in conn.execute(f'select * from {table} order by rowid')] == rows, (label, table, 'snapshot differs from database')
        else:
            assert states[label] == 'refused' and (folder / 'failed.json').exists()
        samples.append(row)
    return {'samples': samples, 'grouped_extraction_requests': wire_requests, 'raw_candidate_refs': refs,
            'invalid_refs': invalid, 'exact_bindings_judged': judged,
            'calls': sum(r['calls'] for r in samples), 'cost': round(sum(r['cost'] for r in samples), 6),
            'api_seconds': round(sum(r['seconds'] for r in samples), 2), 'semantic_acceptance': 'not_scored_by_this_script'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    print(json.dumps(audit(args.out.resolve()), ensure_ascii=False, indent=2))
