"""D148: expose source-to-thesis-to-group paths for human semantic review."""
import argparse
import json
from pathlib import Path

import grouping_consistency as experiment
import ingestion_groups as base
import study


def inspect_sample(folder, item, anchors):
    record = json.loads((folder / 'item3-extract.json').read_text())
    if record['status'] != 'complete':
        return {'sample': folder.name, 'status': record['status']}
    raw = record['answer']
    conn = study.read_only(folder / 'views.sqlite')
    core = {}
    for role, seq in [('shipment', 1), ('sk', 2)]:
        ids = [r[0] for r in conn.execute('select view_id from views where created_seq=?', (seq,))]
        if len(ids) != 1:
            raise ValueError('The fixed prefix must contain one thesis at each step')
        core[role] = ids[0]
    def groups(vid):
        return {r[0] for r in conn.execute('select thread_id from thread_members where view_id=?', (vid,))}
    shared = groups(core['shipment']) & groups(core['sk'])
    sk_only = groups(core['sk']) - groups(core['shipment'])
    body = base.extraction.normalise(item['text'])
    passages = {}
    for role, anchor in anchors.items():
        quote = base.extraction.normalise(anchor)
        if body.count(quote) != 1:
            raise ValueError('Source anchor is absent or ambiguous: ' + role)
        left, right = body.index(quote), body.index(quote) + len(quote)
        def overlaps(text):
            normal = base.extraction.normalise(text)
            start = body.find(normal)
            return bool(normal) and start >= 0 and start < right and start + len(normal) > left
        evidence = [e for e in raw['evidence'] if overlaps(e['quote'])]
        eids = {e['id'] for e in evidence}
        candidates = [c for c in raw['candidates'] if eids & set(c['evidence_ids'])]
        destinations = []
        for row in conn.execute('select evidence_id,quote from evidence where created_seq=3'):
            if not overlaps(row['quote']):
                continue
            for view in conn.execute('''select distinct v.view_id,v.question from views v
                    join evidence_links l on l.view_id=v.view_id where l.evidence_id=?''', (row['evidence_id'],)):
                destinations.append(dict(view) | {'evidence_id': row['evidence_id'],
                    'groups': sorted(groups(view['view_id'])), 'quote': row['quote']})
        passages[role] = {'raw_evidence': evidence, 'raw_candidates': candidates, 'destinations': destinations}
    openai = passages['openai']['destinations']
    pc = passages['pc']['destinations']
    risk = passages['risk']['destinations']
    failure = folder / 'failed.json'
    result = {
        'sample': folder.name, 'failure': json.loads(failure.read_text()) if failure.exists() else None,
        'core_groups': sorted(shared), 'passages': passages,
        'raw_candidates': raw['candidates'], 'raw_evidence': raw['evidence'],
        'openai_exact_quote_candidate': bool(passages['openai']['raw_candidates']),
        'openai_distinct_stored': any(v['view_id'] not in core.values() for v in openai),
        'openai_in_core_group': any(v['view_id'] not in core.values() and shared & set(v['groups']) for v in openai),
        'openai_in_sk_only_group': any(sk_only & set(v['groups']) for v in openai),
        'pc_observed': bool(pc), 'pc_in_core_group': any(shared & set(v['groups']) for v in pc),
        'risk_reaches_shipment': any(v['view_id'] == core['shipment'] for v in risk),
        'groups': experiment.history(conn, 3),
    }
    result_path = folder / 'item3-result.json'
    if result_path.exists():
        written = json.loads(result_path.read_text())
        result.update(dropped=written['dropped'], bindings=written['bindings'])
    conn.close()
    return result


def review(out):
    manifest = experiment.verify(out)
    original = json.loads((Path(manifest['source']) / 'item3-extract.json').read_text())['answer']
    source_quotes = {e['id']: e['quote'] for e in original['evidence']}
    anchors = {role: source_quotes[eid] for role, eid in [('openai', 'e4'), ('pc', 'e3'), ('risk', 'e2')]}
    item = json.loads((out / 'items.json').read_text())[2]
    samples = []
    for label in experiment.LABELS:
        folder = out / f'sample-{label}'
        if not (folder / 'item3-result.json').exists() and not (folder / 'failed.json').exists():
            raise ValueError('Sample is still in flight: ' + label)
        samples.append(inspect_sample(folder, item, anchors))
    calls = [json.loads(p.read_text()) for p in out.glob('sample-*/item3-*.json')
             if p.name != 'item3-result.json']
    report = {'samples': samples, 'call_count': len(calls),
              'estimated_usd': sum(c.get('estimated_usd', 0) for c in calls),
              'input_tokens': sum(c.get('input_tokens', 0) for c in calls),
              'output_tokens': sum(c.get('output_tokens', 0) for c in calls),
              'note': 'Source spans expose paths, not a semantic judge; read all questions and quotes.'}
    study.write_json(out / 'measurements.json', report)
    for sample in samples:
        print({k: v for k, v in sample.items() if k not in ['passages', 'groups', 'raw_candidates', 'raw_evidence']})
    print({k: v for k, v in report.items() if k != 'samples'})
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    review(parser.parse_args().out.resolve())
