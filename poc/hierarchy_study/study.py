"""Read-only-source POCs for grouping atomic theses and synthesizing agent-facing main theses."""
from __future__ import annotations

import argparse
import collections
import dataclasses
import hashlib
import html
import importlib.metadata
import json
import os
from pathlib import Path
import sqlite3
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, model, search  # noqa: E402

CONTEXT_IDS = ['v1', 'v17', 'v28', 'v34', 'v54', 'v55', 'v81', 'v94']
CUTOFFS = [6, 166, 373, 584]
METHODS = ['A_density', 'B_graph', 'C_global_llm', 'D_incremental_llm']


def obj(properties):
    return {'type': 'object', 'additionalProperties': False, 'required': list(properties), 'properties': properties}


STRING = {'type': 'string'}
STRINGS = {'type': 'array', 'items': STRING}
GROUP = obj({'id': STRING, 'title': STRING, 'scope': STRING, 'members': STRINGS})
GROUP_SCHEMA = obj({'groups': {'type': 'array', 'items': GROUP}, 'unassigned': STRINGS})
UPDATE_SCHEMA = obj({
    'new_groups': {'type': 'array', 'items': obj({'id': STRING, 'title': STRING, 'scope': STRING})},
    'assignments': {'type': 'array', 'items': obj({'view_id': STRING, 'group_id': STRING})},
    'unassigned': STRINGS,
})
CLAIM = obj({'text': STRING, 'relation': {'type': 'string', 'enum': ['supports', 'challenges', 'context']}, 'view_ids': STRINGS})
HEAD = obj({
    'group_id': STRING, 'title': STRING,
    'status': {'type': 'string', 'enum': ['main_thesis', 'insufficient']},
    'thesis': STRING, 'claims': {'type': 'array', 'items': CLAIM},
    'limitations': STRINGS, 'watch_questions': STRINGS,
})
HEAD_SCHEMA = obj({'heads': {'type': 'array', 'items': HEAD}, 'ungrouped_note': STRING})
PROBE_SCHEMA = obj({'answers': {'type': 'array', 'items': obj({
    'question_id': STRING, 'answer': STRING, 'main_ids': STRINGS,
    'drill_down_ids': STRINGS, 'limitations': STRINGS,
})}})

GROUP_PROMPT = """Organize atomic financial-research theses into a small, coherent set of reusable business themes.
This is grouping, not deduplication and not an investment recommendation. Keep every atomic thesis ID distinct.
A theme is a bounded business process, product commercialization, economic driver, or operating outcome. Shared company,
year, revenue vocabulary, or bullish/bearish stance alone is not enough. Themes may cross companies and industries when
the same business mechanism justifies it. Give an English title and an explicit scope for each theme.
Do not force unrelated one-off events into a broad miscellaneous theme. Leave them unassigned when appropriate.
Use only the supplied texts; do not add outside knowledge. Every supplied ID appears exactly once, in members or unassigned.
Do not invent a fixed target number of themes. Return only the requested JSON."""

UPDATE_PROMPT = """Incrementally organize newly arrived atomic financial-research theses into reusable business themes.
Existing theme IDs, scopes and memberships are fixed for this minimal online baseline. Assign only the new IDs.
Choose an existing candidate theme when its explicit scope fits, or create a bounded new theme with a unique temporary
ID, English title and scope. Shared company, year or stance alone is not sufficient. Related businesses can cross companies.
Unrelated one-off events may remain unassigned. Do not create a new theme merely to paraphrase a single narrow question.
Every new ID appears exactly once in assignments or unassigned. New group IDs must be referenced by an assignment.
Do not rename, split, merge, or move old members. Use only supplied information and return the requested JSON."""

SYNTHESIS_PROMPT = """You are writing an agent-facing layer ABOVE atomic financial-research theses.
For each supplied group, write a bounded, argued main thesis about the business mechanism or operating outcome, not just
a topic label or a list of documents. Use only the supplied point-in-time research records, including their current labels,
conditions, reasons and evidence. These are research judgements, not guaranteed facts. Separate realized facts, guidance,
third-party forecasts and unresolved future events. Never turn a forecast into an actual result. Never infer a stock return
or valuation from operating data alone. Do not average the atomic scores or invent a new overall numerical score.
Every substantive explanatory claim has one or more supplied atomic view_ids and a supports/challenges/context relation.
The main thesis must use at least one member of its own group. You may also cite other supplied groups' members as cross-group
support or challenge. Keep conflicting evidence and limitations visible; do not hide them to make a persuasive story.
If the group cannot support a useful overarching judgement, use insufficient and explain the limitation instead of inflating
a narrow event into a grand thesis. Include specific questions that would change the judgement. Write concise English.
Return exactly one head per supplied group; use no outside sources. Return only the requested JSON."""

PROBE_PROMPT = """You are an agent using ONLY the supplied main-thesis cards. Answer each question concisely in English.
Cite the supplied main IDs and the atomic IDs you would inspect next. Do not invent information that is missing from these
cards, and distinguish a business judgement from a confirmed event. Explicitly state limitations. Return the requested JSON."""
QUESTIONS = [
    {'id': 'growth', 'question': 'What operating thesis and counterarguments can I form about NVIDIA growth, without claiming a stock-price conclusion?'},
    {'id': 'rubin', 'question': 'What must still happen for Vera Rubin commercialization, and which atomic theses should I inspect to separate shipments, revenue, and customer deployment?'},
    {'id': 'cross_company', 'question': 'Which cross-company or industry factors materially condition NVIDIA, and where does the supplied research stop short of supporting a causal conclusion?'},
]


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2))
    temp.replace(path)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_only(path):
    conn = sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute('begin')
    return conn


def snapshot(conn, ids, cutoff):
    result = []
    for row in conn.execute('select * from views where created_seq<=? order by created_seq,rowid', (cutoff,)):
        view = dict(row)
        if view['view_id'] not in ids:
            continue
        ident = view['view_id']
        rungs = [dict(r) for r in conn.execute('select position,label,condition from rungs where view_id=? order by position', (ident,))]
        judgement = conn.execute('select * from judgements where view_id=? and seq<=? order by seq desc,judgement_id desc limit 1', (ident, cutoff)).fetchone()
        assessment = None
        evidence = []
        if judgement:
            judgement = dict(judgement)
            rung = next((r for r in rungs if r['position'] == judgement['rung']), None)
            assert rung is not None, (ident, 'unknown rung')
            assessment = {k: judgement[k] for k in ['judgement_id', 'seq', 'publication_day', 'reasons']}
            assessment.update(rung)
            for eid in json.loads(judgement['cited_evidence_json'] or '[]'):
                record = conn.execute('select e.* from evidence e join evidence_links l on e.evidence_id=l.evidence_id where e.evidence_id=? and l.view_id=? and e.created_seq<=? and l.seq<=? limit 1', (eid, ident, cutoff, cutoff)).fetchone()
                assert record is not None, (ident, eid, cutoff, 'unavailable citation')
                record = dict(record)
                evidence.append({k: record[k] for k in ['evidence_id', 'one_line', 'quote', 'tier', 'original_who', 'original_day', 'created_seq']})
        dependencies = []
        for dep in conn.execute('select * from dependencies where view_id=? and seq<=? order by dependency_id', (ident, cutoff)):
            resolution = conn.execute('select resolved_to from dependency_resolutions where dependency_id=? and seq<=? order by seq desc,id desc limit 1', (dep['dependency_id'], cutoff)).fetchone()
            target = resolution['resolved_to'] if resolution else dep['depends_on']
            exists = conn.execute('select 1 from views where view_id=? and created_seq<=?', (target, cutoff)).fetchone()
            if exists:
                dependencies.append({'view_id': target, 'direction': dep['direction'], 'seq': dep['seq']})
        result.append({
            'id': ident, 'object': view['object_id'], 'question': view['question'],
            'focus': view['looks_at'], 'due_day': view['due_day'], 'created_seq': view['created_seq'],
            'grouping_text': search.view_text(view, rungs), 'assessment': assessment,
            'evidence': evidence, 'dependencies': dependencies,
        })
    return {'cutoff_seq': cutoff, 'theses': result}


def prepare(args):
    out = Path(args.out).resolve()
    if out.exists():
        raise ValueError('Use a new dated output directory')
    out.mkdir(parents=True)
    before = digest(args.views)
    conn, index = read_only(args.views), read_only(args.index)
    ids = [r[0] for r in conn.execute("select view_id from views where object_id='NVDA' order by created_seq,rowid")]
    ids += [ident for ident in CONTEXT_IDS if ident not in ids]
    assert len(ids) == 31, f'Expected the declared 31 records, got {len(ids)}'
    snapshots = [snapshot(conn, set(ids), cutoff) for cutoff in CUTOFFS]
    vectors = {}
    for thesis in snapshots[-1]['theses']:
        row = index.execute('select * from view_vectors where view_id=?', (thesis['id'],)).fetchone()
        assert row and row['text_sha256'] == search.sha(thesis['grouping_text']), (thesis['id'], 'missing or stale vector')
        vectors[thesis['id']] = json.loads(row['vector_json'])
    conn.close()
    index.close()
    assert before == digest(args.views), 'Source changed while preparing the snapshot'
    manifest = {
        'source': str(Path(args.views).resolve()), 'source_sha256': before,
        'index': str(Path(args.index).resolve()), 'index_sha256': digest(args.index),
        'cutoffs': CUTOFFS, 'records': len(ids), 'context_ids': CONTEXT_IDS,
        'snapshot_counts': [len(s['theses']) for s in snapshots],
        'versions': {package: importlib.metadata.version(package) for package in ['numpy', 'scikit-learn', 'networkx']},
        'model': 'gpt-6-luna', 'provider': 'openai', 'samples': 3,
        'max_http_attempts': 48, 'estimated_usd_cap': 8,
        'price_note': 'Costs use the repository price table; they are not provider invoices.',
    }
    write_json(out / 'manifest.json', manifest)
    write_json(out / 'input.json', {'snapshots': snapshots, 'vectors': vectors})
    write_json(out / 'budget.json', {'attempts': [], 'estimated_spent': 0.0})
    print(json.dumps(manifest, ensure_ascii=False), flush=True)


def check_partition(value, ids):
    errors = model.check_schema(value, GROUP_SCHEMA)
    if errors:
        raise ValueError('; '.join(errors))
    groups = value['groups']
    gids = [group['id'] for group in groups]
    if len(set(gids)) != len(gids) or any(not gid for gid in gids):
        raise ValueError('Group IDs must be nonempty and unique')
    actual = list(value['unassigned'])
    for group in groups:
        if not group['members'] or not group['title'].strip() or not group['scope'].strip():
            raise ValueError('A group needs members, title and scope')
        actual.extend(group['members'])
    if collections.Counter(actual) != collections.Counter(ids):
        raise ValueError('Every supplied thesis must occur exactly once')
    return value


def check_heads(value, partition, snap):
    errors = model.check_schema(value, HEAD_SCHEMA)
    if errors:
        raise ValueError('; '.join(errors))
    groups = {group['id']: group for group in partition['groups']}
    known = {thesis['id'] for thesis in snap['theses']}
    if collections.Counter(head['group_id'] for head in value['heads']) != collections.Counter(list(groups)):
        raise ValueError('Return exactly one head for every group')
    for head in value['heads']:
        referenced = set()
        for claim in head['claims']:
            if not claim['text'].strip() or not claim['view_ids'] or not set(claim['view_ids']) <= known:
                raise ValueError('Every claim needs real snapshot citations')
            referenced.update(claim['view_ids'])
        if head['status'] == 'main_thesis' and (
            not head['thesis'].strip() or not referenced.intersection(groups[head['group_id']]['members'])
        ):
            raise ValueError('A main thesis must cite its own group')
    return value


def matrix(data, theses):
    import numpy as np
    values = np.asarray([data['vectors'][thesis['id']] for thesis in theses], dtype=float)
    return values / np.linalg.norm(values, axis=1, keepdims=True)


def offline_partitions(data):
    import numpy as np
    import networkx as nx
    from sklearn.cluster import HDBSCAN
    theses = data['snapshots'][-1]['theses']
    ids = [thesis['id'] for thesis in theses]
    values = matrix(data, theses)
    distances = np.maximum(0, 1 - values @ values.T)
    np.fill_diagonal(distances, 0)
    labels = HDBSCAN(min_cluster_size=3, min_samples=2, metric='precomputed', n_jobs=1).fit_predict(distances)
    groups = []
    for label in sorted(set(labels) - {-1}):
        groups.append({'id': f'g{len(groups)+1}', 'title': f'Density community {label}', 'scope': 'Fixed HDBSCAN partition of the supplied semantic vectors.', 'members': [ident for ident, value in zip(ids, labels) if value == label]})
    density = check_partition({'groups': groups, 'unassigned': [ident for ident, value in zip(ids, labels) if value == -1]}, ids)
    graph = nx.Graph()
    graph.add_nodes_from(ids)
    for thesis in theses:
        for edge in thesis['dependencies']:
            if edge['view_id'] in ids and edge['view_id'] != thesis['id']:
                graph.add_edge(thesis['id'], edge['view_id'], weight=1.0)
    isolates = list(nx.isolates(graph))
    graph.remove_nodes_from(isolates)
    communities = nx.community.louvain_communities(graph, seed=17, resolution=1, weight='weight') if graph else []
    groups = [{'id': f'g{i+1}', 'title': f'Dependency community {i+1}', 'scope': 'Fixed Louvain community of recorded dependency edges, treated as undirected for discovery.', 'members': sorted(members, key=ids.index)} for i, members in enumerate(sorted(communities, key=lambda members: min(ids.index(member) for member in members)))]
    graph_result = check_partition({'groups': groups, 'unassigned': isolates}, ids)
    return {'A_density': density, 'B_graph': graph_result}


class Calls:
    """One HTTP attempt per named step, with durable reservations and no hidden resampling."""

    def __init__(self, out, sample):
        self.out, self.sample = Path(out), sample
        self.archive = model.Archive(str(self.out / f'sample-{sample}' / 'calls.sqlite'))
        self.cfg = dataclasses.replace(config.load(str(ROOT / 'poc/config/poc-v7.json')), version='hierarchy-poc-v1')
        assert self.cfg.provider == 'openai' and self.cfg.idea.model == 'gpt-6-luna'
        self.setting = dataclasses.replace(self.cfg.idea, name='hierarchy-study', max_output_tokens=7000)

    def call(self, step, prompt, payload, schema):
        path = self.out / f'sample-{self.sample}' / f'{step}.json'
        if path.exists():
            record = json.loads(path.read_text())
            if record['status'] != 'complete':
                raise RuntimeError(f'{step}: prior {record["status"]}; no automatic resend')
            return record['answer']
        user = json.dumps(payload, ensure_ascii=False)
        request = model.build_request(self.setting, prompt, user, schema, 'hierarchy_result', self.cfg.provider)
        serialized = json.dumps(request, ensure_ascii=False).encode()
        reserve = (len(serialized) * 1.25 + self.setting.max_output_tokens * 10) / 1e6
        budget_path = self.out / 'budget.json'
        budget = json.loads(budget_path.read_text())
        if len(budget['attempts']) >= 48 or budget['estimated_spent'] + reserve > 8:
            raise RuntimeError('Declared experiment budget reached; no request sent')
        entry = {'sample': self.sample, 'step': step, 'reserved_usd': reserve, 'status': 'started'}
        budget['attempts'].append(entry)
        budget['estimated_spent'] += reserve
        write_json(budget_path, budget)
        record = {'status': 'started', 'request': request, 'reserved_usd': reserve}
        write_json(path, record)
        print(f'START sample={self.sample} step={step} reserved=${reserve:.4f}', flush=True)
        started = time.perf_counter()

        def transport(provider, body):
            url, _ = model.ENDPOINTS[provider]
            headers = {'Authorization': f'Bearer {model._key(provider)}', 'Content-Type': 'application/json'}
            req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=180) as response:
                return json.loads(response.read().decode())

        try:
            answer = model.call(self.archive, self.cfg, self.setting, prompt, user, schema, 'hierarchy_result', step, transport=transport)
            record.update(status='complete', answer=answer.data, input_tokens=answer.input_tokens, output_tokens=answer.output_tokens, estimated_usd=answer.cost_usd, seconds=round(time.perf_counter()-started, 3), call_id=answer.call_id, request_sha256=answer.request_sha256, cached=answer.cached)
            entry.update(status='complete', estimated_usd=answer.cost_usd)
            budget['estimated_spent'] += answer.cost_usd - reserve
            write_json(path, record)
            write_json(budget_path, budget)
            print(f'DONE sample={self.sample} step={step} in={answer.input_tokens} out={answer.output_tokens} usd={answer.cost_usd:.4f}', flush=True)
            return answer.data
        except Exception as error:
            record.update(status='failed', error=type(error).__name__ + ': ' + str(error)[:300], seconds=round(time.perf_counter()-started, 3))
            entry.update(status='failed')
            write_json(path, record)
            write_json(budget_path, budget)
            raise


def grouping_nodes(snap):
    return [{'id': thesis['id'], 'text': thesis['grouping_text']} for thesis in snap['theses']]


def incremental(calls, data):
    import numpy as np
    result = {'groups': [], 'unassigned': []}
    seen, history = set(), []
    all_vectors = data['vectors']
    for snap in data['snapshots']:
        new = [thesis for thesis in snap['theses'] if thesis['id'] not in seen]
        fresh = [thesis['id'] for thesis in new]
        candidates = result['groups']
        if len(candidates) > 5 and fresh:
            def similarity(group):
                return max(float(np.dot(all_vectors[a], all_vectors[b]) / (np.linalg.norm(all_vectors[a])*np.linalg.norm(all_vectors[b]))) for a in fresh for b in group['members'])
            candidates = sorted(candidates, key=similarity, reverse=True)[:5]
        texts = {thesis['id']: thesis['grouping_text'] for thesis in snap['theses']}
        candidate_cards = [dict(group, representative_theses=[{'id': ident, 'text': texts[ident]} for ident in group['members'][:3]]) for group in candidates]
        payload = {'cutoff_seq': snap['cutoff_seq'], 'candidate_groups': candidate_cards, 'new_theses': grouping_nodes({'theses': new})}
        update = calls.call(f'D_incremental-{snap["cutoff_seq"]}', UPDATE_PROMPT, payload, UPDATE_SCHEMA)
        lookup = {group['id']: group for group in result['groups']}
        candidate_ids = {group['id'] for group in candidates}
        local_ids = set()
        local_lookup = {}
        for group in update['new_groups']:
            if group['id'] in local_ids or group['id'] in lookup:
                raise ValueError('New group IDs collide')
            local_ids.add(group['id'])
            created = {'id': f'g{len(result["groups"])+1}', 'title': group['title'], 'scope': group['scope'], 'members': []}
            result['groups'].append(created)
            local_lookup[group['id']] = created
        actual = list(update['unassigned'])
        for assignment in update['assignments']:
            gid = assignment['group_id']
            target = local_lookup.get(gid) if gid in local_ids else lookup.get(gid) if gid in candidate_ids else None
            if target is None:
                raise ValueError('Assignment names a group that was not shown')
            actual.append(assignment['view_id'])
            target['members'].append(assignment['view_id'])
        if collections.Counter(actual) != collections.Counter(fresh):
            raise ValueError('Incremental update must place only and all new IDs once')
        result['unassigned'].extend(update['unassigned'])
        seen.update(fresh)
        check_partition(result, list(seen))
        history.append({'cutoff_seq': snap['cutoff_seq'], 'new_ids': fresh, 'groups': json.loads(json.dumps(result['groups'])), 'unassigned': list(result['unassigned'])})
    write_json(calls.out / f'sample-{calls.sample}' / 'D_history.json', history)
    return result


def synthesis_records(snap):
    return [{k: value for k, value in thesis.items() if k != 'grouping_text'} for thesis in snap['theses']]


def synthesis_context(snap):
    records, evidence = [], {}
    for thesis in synthesis_records(snap):
        for piece in thesis['evidence']:
            evidence[piece['evidence_id']] = piece
        records.append(dict(thesis, evidence_ids=[piece['evidence_id'] for piece in thesis['evidence']], evidence=[]))
    return {'research_records': records, 'evidence': list(evidence.values())}


def probe_errors(probe, heads, snapshot):
    errors = []
    if collections.Counter(a['question_id'] for a in probe['answers']) != collections.Counter(q['id'] for q in QUESTIONS):
        errors.append('Agent probe did not answer all fixed questions')
    main_ids = {head['group_id'] for head in heads}
    atom_ids = {thesis['id'] for thesis in snapshot['theses']}
    for answer in probe['answers']:
        unknown = set(answer['main_ids']) - main_ids
        unknown_atoms = set(answer['drill_down_ids']) - atom_ids
        if unknown or unknown_atoms:
            errors.append(f'{answer["question_id"]}: unknown main IDs {sorted(unknown)}, atomic IDs {sorted(unknown_atoms)}')
    return errors


def run(args):
    out = Path(args.out).resolve()
    data = json.loads((out / 'input.json').read_text())
    manifest = json.loads((out / 'manifest.json').read_text())
    assert digest(manifest['source']) == manifest['source_sha256'], 'Original source changed; prepare a new study'
    fixed = offline_partitions(data)
    write_json(out / 'offline_partitions.json', fixed)
    final = data['snapshots'][-1]
    for sample in [1, 2, 3]:
        calls = Calls(out, sample)
        partitions = dict(fixed)
        partitions['C_global_llm'] = check_partition(calls.call('C_grouping', GROUP_PROMPT, {'theses': grouping_nodes(final)}, GROUP_SCHEMA), [t['id'] for t in final['theses']])
        partitions['D_incremental_llm'] = incremental(calls, data)
        for method in METHODS:
            partition = partitions[method]
            write_json(out / f'sample-{sample}' / f'{method}-partition.json', partition)
            payload = {'as_of': '2026-08-15', 'groups': partition['groups'], 'unassigned': partition['unassigned'], **synthesis_context(final)}
            heads = check_heads(calls.call(f'{method}-synthesis', SYNTHESIS_PROMPT, payload, HEAD_SCHEMA), partition, final)
            write_json(out / f'sample-{sample}' / f'{method}-heads.json', heads)
            probe = calls.call(f'{method}-agent', PROBE_PROMPT, {'main_theses': heads['heads'], 'questions': QUESTIONS}, PROBE_SCHEMA)
            errors = probe_errors(probe, heads['heads'], final)
            write_json(out / f'sample-{sample}' / f'{method}-agent-checks.json', {'valid': not errors, 'errors': errors})
            if errors:
                print(f'REJECTED agent output sample={sample} method={method}: {errors}; retained without resampling', flush=True)
    report(out)


def report(out):
    from sklearn.metrics import adjusted_rand_score
    out = Path(out)
    data = json.loads((out / 'input.json').read_text())
    ids = [t['id'] for t in data['snapshots'][-1]['theses']]
    results = []
    for method in METHODS:
        labels = []
        for sample in [1, 2, 3]:
            prefix = out / f'sample-{sample}'
            partition = json.loads((prefix / f'{method}-partition.json').read_text())
            heads = json.loads((prefix / f'{method}-heads.json').read_text())
            membership = {ident: i for i, group in enumerate(partition['groups']) for ident in group['members']}
            labels.append([membership.get(ident, -1-i) for i, ident in enumerate(ids)])
            groups = partition['groups']
            multi_object = sum(len({t['object'] for t in data['snapshots'][-1]['theses'] if t['id'] in g['members']}) > 1 for g in groups)
            cross_edges = sum(bool(set(claim['view_ids']) - set(next(g['members'] for g in groups if g['id'] == head['group_id']))) for head in heads['heads'] for claim in head['claims'])
            checks = json.loads((prefix / f'{method}-agent-checks.json').read_text())
            results.append({'method': method, 'sample': sample, 'groups': len(groups), 'unassigned': len(partition['unassigned']), 'largest': max([len(g['members']) for g in groups], default=0), 'cross_object_groups': multi_object, 'main_theses': sum(h['status'] == 'main_thesis' for h in heads['heads']), 'cross_group_claims': cross_edges, 'agent_references_valid': checks['valid']})
        scores = [adjusted_rand_score(labels[a], labels[b]) for a, b in [(0, 1), (0, 2), (1, 2)]]
        for record in results:
            if record['method'] == method:
                record['pairwise_sample_ARI'] = scores
    budget = json.loads((out / 'budget.json').read_text())
    write_json(out / 'metrics.json', {'records': results, 'budget': budget, 'note': 'ARI measures grouping repeatability, not correctness. Counts and reference checks do not judge the semantics of claims.'})
    sections = []
    for sample in [1, 2, 3]:
        for method in METHODS:
            prefix = out / f'sample-{sample}'
            partition = json.loads((prefix / f'{method}-partition.json').read_text())
            heads = json.loads((prefix / f'{method}-heads.json').read_text())
            body = []
            for head in heads['heads']:
                members = next(group['members'] for group in partition['groups'] if group['id'] == head['group_id'])
                claims = ''.join(f'<li><b>{html.escape(c["relation"])}</b> {html.escape(c["text"])} <small>{html.escape(", ".join(c["view_ids"]))}</small></li>' for c in head['claims'])
                body.append(f'<article><h3>{html.escape(head["title"])}</h3><small>{html.escape(head["status"])} · {html.escape(", ".join(members))}</small><p><strong>{html.escape(head["thesis"])}</strong></p><ul>{claims}</ul><p>Limits: {html.escape("; ".join(head["limitations"]))}</p><p>Watch: {html.escape("; ".join(head["watch_questions"]))}</p></article>')
            sections.append(f'<section id="{method}-{sample}"><h2>{method} · sample {sample}</h2><p>Unassigned: {html.escape(", ".join(partition["unassigned"]))}</p>{"".join(body)}</section>')
    options = ''.join(f'<option value="{method}-{sample}">{method} · sample {sample}</option>' for sample in [1, 2, 3] for method in METHODS)
    page = '<!doctype html><meta charset="utf-8"><title>Main thesis POC review</title><style>body{font:15px/1.6 system-ui;margin:32px;background:#f5f4ef;color:#172019}main{max-width:1050px;margin:auto}select{padding:8px}article{background:white;border:1px solid #deded5;border-radius:12px;padding:20px;margin:16px 0}small{color:#6b7068}section{display:none}section.active{display:block}li{margin-bottom:10px}</style><main><h1>Main thesis POC review</h1><p>31 stored atomic theses; four pipelines; three independent samples. Research output, not validated investment conclusions.</p><select id="pick">'+options+'</select>'+''.join(sections)+'</main><script>const pick=document.querySelector("select");function show(){document.querySelectorAll("section").forEach(s=>s.classList.toggle("active",s.id===pick.value));}pick.onchange=show;show();</script>'
    (out / 'review.html').write_text(page)
    print(json.dumps({'results': results, 'estimated_spent': budget['estimated_spent'], 'attempts': len(budget['attempts'])}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'run', 'report'])
    parser.add_argument('--out', required=True)
    parser.add_argument('--views', default=str(ROOT / 'poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite'))
    parser.add_argument('--index', default=str(ROOT / 'poc/data/service/search-index.sqlite'))
    args = parser.parse_args()
    {'prepare': prepare, 'run': run, 'report': lambda a: report(a.out)}[args.command](args)


if __name__ == '__main__':
    main()
