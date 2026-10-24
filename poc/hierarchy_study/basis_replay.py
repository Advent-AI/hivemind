"""Fixed-scope experiment: classify current evidence before rendering a main-thesis card."""
from __future__ import annotations

import argparse
import collections
import dataclasses
import fcntl
import json
from pathlib import Path

import replay
import study

FROZEN = study.ROOT / 'poc/reports/2026-10-24-main-thesis-replay-01'
ROLES = ['supports', 'challenges', 'context', 'irrelevant', 'uncertain']
REVIEW_PROMPT = """Assess each supplied current source against the business pathway in the research question.
Give each source one role and a brief reason: supports advances that pathway; challenges limits or weakens it;
context informs it without a direction; irrelevant has no bearing; uncertain cannot be assessed from this material.
Distinguish actual results, guidance, forecasts and prospective events. Use only the current sources and view assessments.
The change list shows arrival or current-citation changes, not proof that a removed source was false.
Review the whole current set, including contrary evidence. Do not count shared origins as independent confirmation.
Write English. Do not write the main conclusion, infer a stock return, or invent facts."""
SUMMARY_PROMPT = """Answer the supplied research question with one bounded business judgement using only current_material.
Distinguish actual results from guidance, forecasts, readiness and future events. Explain the business connection,
relevant counterarguments and limitations. A source's origin paths are provenance, not additional independent evidence.
Cite supplied source references for explanatory arguments. State insufficient support when appropriate.
Do not infer a stock return, average scores, invent an outcome or substitute one revenue/spending measure for another.
Write English JSON."""
PROBE_PROMPT = """Answer each requested facet of the question using only the supplied card. Explain the current
state and key limitations or risks, and select the source references you would inspect next. Plans, guidance and
readiness are not realized results. If the card lacks material, say so and leave references empty. Write English JSON."""


def catalog(snap):
    """Deduplicate evidence and attach all real current origins, without inventing semantic links."""
    records = {}
    for thesis in snap['theses']:
        for evidence in thesis['evidence']:
            ref = 'source_' + evidence['evidence_id']
            content = {key: evidence[key] for key in ['quote', 'one_line', 'tier', 'original_day']}
            if ref not in records:
                records[ref] = dict(content, source_ref=ref, origin_paths=[])
            elif any(records[ref][key] != value for key, value in content.items()):
                raise ValueError('One evidence identity has inconsistent content')
            origin = {'view_id': thesis['id'], 'judgement_id': thesis['assessment']['judgement_id']}
            if origin in records[ref]['origin_paths']:
                raise ValueError('Duplicate evidence origin')
            records[ref]['origin_paths'].append(origin)
    if not records:
        raise ValueError('No current evidence to judge')
    return [records[key] for key in sorted(records, key=lambda key: int(key.removeprefix('source_e')))]


def views(snap):
    return [{'view_id': t['id'], 'question': t['question'], 'assessment': t['assessment']} for t in snap['theses']]


def change_set(previous, current):
    old = {r['source_ref']: r for r in catalog(previous)} if previous else {}
    new = {r['source_ref']: r for r in catalog(current)}
    old_views = {t['id']: t['assessment'] for t in previous['theses']} if previous else {}
    return {'added': sorted(new.keys() - old.keys()), 'removed': sorted(old.keys() - new.keys()),
            'retained': sorted(new.keys() & old.keys()),
            'changed_views': [t['id'] for t in current['theses'] if old_views.get(t['id']) != t['assessment']]}


def refs_schema(records):
    return {'type': 'array', 'items': {'type': 'string', 'enum': [r['source_ref'] for r in records]}}


def review_schema(records):
    return study.obj({'assessments': study.obj({r['source_ref']: study.obj({
        'role': {'type': 'string', 'enum': ROLES}, 'reason': study.STRING,
    }) for r in records})})


def compile_basis(answer, snap, name):
    records = catalog(snap)
    errors = study.model.check_schema(answer, review_schema(records))
    if errors:
        raise ValueError('; '.join(errors))
    by_ref = answer['assessments']
    if any(not row['reason'].strip() for row in by_ref.values()):
        raise ValueError('Every source needs a reason, including irrelevant sources')
    return {'scope_id': name, 'as_of_seq': snap['cutoff_seq'], 'as_of': snap['as_of'],
            'rows': [dict(source, role=by_ref[source['source_ref']]['role'],
                          reason=by_ref[source['source_ref']]['reason']) for source in records]}


def summary_schema(records):
    return study.obj({'status': {'type': 'string', 'enum': ['supported', 'insufficient']},
                      'conclusion': study.STRING,
                      'arguments': {'type': 'array', 'items': study.obj({
                          'statement': study.STRING,
                          'role': {'type': 'string', 'enum': ['supports', 'challenges', 'context']},
                          'sources': refs_schema(records)})},
                      'limitations': study.STRINGS, 'watch_questions': study.STRINGS})


def compile_card(answer, records, snap, name, basis=None):
    errors = study.model.check_schema(answer, summary_schema(records))
    if errors:
        raise ValueError('; '.join(errors))
    if not answer['conclusion'].strip() or (answer['status'] == 'supported' and not answer['arguments']):
        raise ValueError('A supported summary needs a conclusion and cited arguments')
    selected = collections.defaultdict(set)
    for argument in answer['arguments']:
        if not argument['statement'].strip() or not argument['sources']:
            raise ValueError('Each argument needs text and source references')
        if len(argument['sources']) != len(set(argument['sources'])):
            raise ValueError('Duplicate source in argument')
        for ref in argument['sources']:
            selected[ref].add(argument['role'])
    groups = {role: [] for role in ROLES if role != 'irrelevant'}
    if basis is not None:
        for record in basis['rows']:
            if record['role'] != 'irrelevant':
                groups[record['role']].append(record)
    else:
        for record in records:
            for role in sorted(selected.get(record['source_ref'], [])):
                groups[role].append(record)
    return {'scope_id': name, 'as_of_seq': snap['cutoff_seq'], 'as_of': snap['as_of'],
            'summary': answer, 'basis': groups}


def visible_sources(card):
    unique = {}
    for records in card['basis'].values():
        for record in records:
            unique[record['source_ref']] = record
    return list(unique.values())


def probe_schema(card, scope):
    return study.obj({'facets': {'type': 'array', 'items': study.obj({
        'facet': {'type': 'string', 'enum': scope['facets']}, 'answer': study.STRING,
        'sources': refs_schema(visible_sources(card))})}})


def validate_probe(answer, card, scope):
    errors = study.model.check_schema(answer, probe_schema(card, scope))
    if errors:
        raise ValueError('; '.join(errors))
    if collections.Counter(r['facet'] for r in answer['facets']) != collections.Counter(scope['facets']):
        raise ValueError('Answer every requested facet exactly once')
    if any(not row['answer'].strip() for row in answer['facets']):
        raise ValueError('Empty answer')
    return answer


class Calls(replay.Calls):
    def __init__(self, out, sample):
        super().__init__(out, sample)
        self.cfg = dataclasses.replace(self.cfg, version='main-thesis-basis-v1')
        self.setting = dataclasses.replace(self.setting, max_output_tokens=7000)


def contract_hash():
    return replay.digest_value([REVIEW_PROMPT, SUMMARY_PROMPT, PROBE_PROMPT, ROLES, replay.SCOPES])


def prepare(out):
    if out.exists():
        raise ValueError('Use a new dated directory')
    prior_manifest = json.loads((FROZEN / 'manifest.json').read_text())
    if study.digest(replay.SOURCE) != prior_manifest['source_sha256'] or study.digest(FROZEN / 'input.json') != prior_manifest['input_sha256']:
        raise ValueError('Frozen input changed')
    data = json.loads((FROZEN / 'input.json').read_text())
    for snapshots in data.values():
        for snap in snapshots:
            catalog(snap)
    out.mkdir(parents=True)
    study.write_json(out / 'input.json', data)
    study.write_json(out / 'budget.json', {'attempts': [], 'estimated_spent': 0})
    study.write_json(out / 'manifest.json', {
        'source_sha256': study.digest(replay.SOURCE), 'input_sha256': study.digest(out / 'input.json'),
        'code_sha256': study.digest(__file__), 'contract_sha256': contract_hash(),
        'config_checksum': study.config.load(str(study.ROOT / 'poc/config/poc-v7.json')).checksum,
        'max_attempts': 42, 'max_estimated_usd': 8, 'max_output_tokens': 7000})
    print('Prepared six frozen snapshots without modifying the source ledger.')


def run(out):
    manifest = json.loads((out / 'manifest.json').read_text())
    expected = [manifest['source_sha256'] == study.digest(replay.SOURCE),
                manifest['input_sha256'] == study.digest(out / 'input.json'),
                manifest['code_sha256'] == study.digest(__file__), manifest['contract_sha256'] == contract_hash(),
                manifest['config_checksum'] == study.config.load(str(study.ROOT / 'poc/config/poc-v7.json')).checksum]
    if not all(expected):
        raise ValueError('Source, code, inputs or configuration changed')
    data = json.loads((out / 'input.json').read_text())
    with (out / 'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for sample in [1, 2, 3]:
            calls = Calls(out, sample)
            for name, scope in replay.SCOPES.items():
                previous, final_basis, alive = None, None, True
                for snap in data[name]:
                    records = catalog(snap)
                    changes = change_set(previous, snap)
                    study.write_json(out / f'{name}-changes-{snap["cutoff_seq"]}.json', changes)
                    if alive:
                        payload = {'question': scope['question'], 'as_of': snap['as_of'],
                                   'changes': changes, 'current_views': views(snap), 'current_sources': records}
                        final_basis = replay.attempt(calls, f'{name}-review-{snap["cutoff_seq"]}', REVIEW_PROMPT,
                                                     payload, review_schema(records),
                                                     lambda answer: compile_basis(answer, snap, name))
                        alive = final_basis is not None
                    previous = snap
                snap = data[name][-1]
                cards = {}
                if final_basis is not None and alive:
                    material = [r for r in final_basis['rows'] if r['role'] != 'irrelevant']
                    if material:
                        payload = {'question': scope['question'], 'as_of': snap['as_of'], 'current_material': material}
                        cards['basis'] = replay.attempt(calls, f'{name}-basis-final', SUMMARY_PROMPT,
                                                       payload, summary_schema(material),
                                                       lambda answer: compile_card(answer, material, snap, name, final_basis))
                material = catalog(snap)
                payload = {'question': scope['question'], 'as_of': snap['as_of'],
                           'current_views': views(snap), 'current_material': material}
                cards['direct'] = replay.attempt(calls, f'{name}-direct-final', SUMMARY_PROMPT,
                                                payload, summary_schema(material),
                                                lambda answer: compile_card(answer, material, snap, name))
                for arm, card in cards.items():
                    if card is not None and visible_sources(card):
                        payload = {'question': scope['question'], 'requested_facets': scope['facets'], 'card': card}
                        replay.attempt(calls, f'{name}-{arm}-probe', PROBE_PROMPT, payload,
                                       probe_schema(card, scope), lambda answer: validate_probe(answer, card, scope))
            calls.archive.conn.close()
    report(out)


def report(out):
    results = []
    for path in sorted(out.glob('sample-*/*-result.json')):
        item = json.loads(path.read_text())
        raw = json.loads(path.with_name(path.name.replace('-result.json', '.json')).read_text())
        results.append({'sample': path.parent.name, 'step': path.name.removesuffix('-result.json'),
                        'status': item['status'], 'input_tokens': raw.get('input_tokens'),
                        'output_tokens': raw.get('output_tokens'), 'seconds': raw.get('seconds'),
                        'estimated_usd': raw.get('estimated_usd'), **item})
    budget = json.loads((out / 'budget.json').read_text())
    summary = {'results': results, 'attempts': len(budget['attempts']), 'estimated_usd': budget['estimated_spent'],
               'source_unchanged': study.digest(replay.SOURCE) == json.loads((out / 'manifest.json').read_text())['source_sha256']}
    study.write_json(out / 'summary.json', summary)
    print(f'FINISHED attempts={summary["attempts"]} estimated_usd={summary["estimated_usd"]:.6f} source_unchanged={summary["source_unchanged"]}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'run', 'report'])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    {'prepare': prepare, 'run': run, 'report': report}[args.command](args.out.resolve())
