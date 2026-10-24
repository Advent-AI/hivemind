"""Two fixed research scopes: historical fresh-versus-update experiment, never production writes."""
from __future__ import annotations

import argparse
import collections
import dataclasses
import fcntl
import hashlib
import json
from pathlib import Path

import study

SOURCE = study.ROOT / 'poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite'
PRIOR = study.ROOT / 'poc/reports/2026-10-24-hierarchy-poc-2246'
MAX_CALLS = 42
SCOPES = {
    'rubin': {
        'question': 'What does current research support about Vera Rubin commercialization across production shipments, customer deployments and revenue realization?',
        'ids': ['v7', 'v14', 'v15', 'v16', 'v48', 'v60'],
        'cutoffs': [66, 379, 532],
        'facets': ['shipments', 'deployments', 'revenue'],
    },
    'capex': {
        'question': 'How does cloud infrastructure investment support the NVIDIA revenue outlook, and where is conversion to NVIDIA revenue still unproven?',
        'ids': ['v1', 'v2', 'v3', 'v9', 'v17', 'v28', 'v34', 'v81', 'v94'],
        'cutoffs': [379, 552, 584],
        'facets': ['spending_outlook', 'revenue_conversion', 'constraints'],
    },
}
PROMPT = """Write one bounded business judgement answering the supplied research question, using only current_research.
Explain what is supported, the business connection, and its limits. Distinguish actual results from forecasts,
guidance, readiness and future events. No stock-price inference or numerical aggregate score.
Each argument states its role relative to your conclusion and explains why. Cite explicit view/evidence pairs
from current_research; a shared source does not make different questions or amounts interchangeable.
If previous_version is supplied, update that judgement using current_research. It is historical context, not
additional current evidence. A missing old citation does not mean its underlying fact was disproved.
Preserve relevant contrary evidence. If support is insufficient, say so. Do not manufacture an outcome.
Write all prose in English and return the requested JSON."""
PROBE_PROMPT = """Answer the supplied question using only the supplied main-thesis card.
For each requested facet, explain the current conclusion and choose the view/evidence references you would
inspect next. Use only references actually on the card. If it lacks the needed material, say so and leave
references empty. Distinguish guidance, plans and readiness from realized results. Write English JSON."""


def digest_value(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def reference_schema(snap):
    return study.obj({
        'view_id': {'type': 'string', 'enum': [t['id'] for t in snap['theses']]},
        'evidence_ids': study.STRINGS,
    })


def schema(snap):
    return study.obj({
        'status': {'type': 'string', 'enum': ['supported', 'insufficient']},
        'conclusion': study.STRING,
        'arguments': {'type': 'array', 'items': study.obj({
            'statement': study.STRING,
            'role': {'type': 'string', 'enum': ['supports', 'challenges', 'context']},
            'reason': study.STRING,
            'references': {'type': 'array', 'items': reference_schema(snap)},
        })},
        'limitations': study.STRINGS, 'watch_questions': study.STRINGS,
    })


def bind_references(references, snap):
    """Bind only the selected real view/evidence pairs to their current judgement."""
    theses = {t['id']: t for t in snap['theses']}
    result, seen = [], set()
    for ref in references:
        thesis = theses.get(ref['view_id'])
        if thesis is None or thesis['assessment'] is None or not ref['evidence_ids']:
            raise ValueError('Reference needs a visible judged view and evidence')
        known = {e['evidence_id'] for e in thesis['evidence']}
        for eid in ref['evidence_ids']:
            pair = (ref['view_id'], eid)
            if eid not in known or pair in seen:
                raise ValueError('Unknown, stale, future or duplicate view/evidence pair')
            seen.add(pair)
        result.append(dict(ref, judgement_id=thesis['assessment']['judgement_id']))
    return result


def validate(answer, snap):
    errors = study.model.check_schema(answer, schema(snap))
    if errors:
        raise ValueError('; '.join(errors))
    if not answer['conclusion'].strip() or (answer['status'] == 'supported' and not answer['arguments']):
        raise ValueError('A supported judgement needs a conclusion and arguments')
    arguments = []
    for argument in answer['arguments']:
        if not argument['statement'].strip() or not argument['reason'].strip() or not argument['references']:
            raise ValueError('Each argument needs a statement, relation reason and references')
        arguments.append(dict(argument, references=bind_references(argument['references'], snap)))
    used = {r['view_id'] for a in arguments for r in a['references']}
    return dict(answer, arguments=arguments, unused_ids=sorted({t['id'] for t in snap['theses']} - used))


def current_context(snap):
    context = study.synthesis_context(snap)
    for record in context['research_records']:
        for key in ['dependencies', 'evidence', 'created_seq']:
            record.pop(key)
    return context


def material_fingerprint(snap):
    return digest_value(current_context(snap))


def update_required(previous, snap):
    return previous is None or previous['input_fingerprint'] != material_fingerprint(snap)


def make_card(answer, snap, name):
    return dict(validate(answer, snap), scope_id=name, as_of_seq=snap['cutoff_seq'],
                as_of=snap['as_of'], input_fingerprint=material_fingerprint(snap))


def probe_schema(scope, snap):
    return study.obj({'facets': {'type': 'array', 'items': study.obj({
        'facet': {'type': 'string', 'enum': scope['facets']},
        'answer': study.STRING,
        'references': {'type': 'array', 'items': reference_schema(snap)},
    })}})


def validate_probe(answer, card, snap, scope):
    errors = study.model.check_schema(answer, probe_schema(scope, snap))
    if errors:
        raise ValueError('; '.join(errors))
    if collections.Counter(x['facet'] for x in answer['facets']) != collections.Counter(scope['facets']):
        raise ValueError('Answer each facet exactly once')
    visible = {(r['view_id'], eid) for a in card['arguments'] for r in a['references'] for eid in r['evidence_ids']}
    for facet in answer['facets']:
        if not facet['answer'].strip():
            raise ValueError('Each facet needs an answer or an explicit limitation')
        bind_references(facet['references'], snap)
        selected = {(r['view_id'], eid) for r in facet['references'] for eid in r['evidence_ids']}
        if not selected <= visible:
            raise ValueError('Probe cited a pair absent from its card')
    return answer


def prepare(out):
    if out.exists():
        raise ValueError('Use a new dated directory')
    out.mkdir(parents=True)
    conn = study.read_only(SOURCE)
    data = {}
    for name, scope in SCOPES.items():
        data[name] = []
        for cutoff in scope['cutoffs']:
            snap = study.snapshot(conn, set(scope['ids']), cutoff)
            snap['as_of'] = conn.execute('select max(day) from (select publication_day day from judgements where seq<=? union all select day from days_completed where seq<=?)', (cutoff, cutoff)).fetchone()[0]
            data[name].append(snap)
    conn.close()
    study.write_json(out / 'input.json', data)
    manifest = {'source': str(SOURCE), 'source_sha256': study.digest(SOURCE), 'scopes': SCOPES,
                'contract_sha256': digest_value([PROMPT, PROBE_PROMPT, SCOPES]),
                'input_sha256': study.digest(out / 'input.json'), 'code_sha256': study.digest(__file__),
                'config_checksum': study.config.load(str(study.ROOT / 'poc/config/poc-v7.json')).checksum,
                'max_calls': MAX_CALLS, 'max_estimated_usd': 8, 'max_output_tokens': 4000}
    study.write_json(out / 'manifest.json', manifest)
    study.write_json(out / 'budget.json', {'attempts': [], 'estimated_spent': 0})
    print(json.dumps(manifest, indent=2))


class Calls(study.Calls):
    """Use the existing durable single-attempt transport with a smaller call/output limit."""

    def __init__(self, out, sample):
        super().__init__(out, sample)
        self.cfg = dataclasses.replace(self.cfg, version='main-thesis-replay-v1')
        self.setting = dataclasses.replace(self.setting, max_output_tokens=4000)

    def call(self, step, prompt, payload, response_schema):
        path = self.out / f'sample-{self.sample}' / f'{step}.json'
        if path.exists():
            expected = study.model.build_request(self.setting, prompt, json.dumps(payload, ensure_ascii=False), response_schema, 'hierarchy_result', self.cfg.provider)
            if json.loads(path.read_text())['request'] != expected:
                raise ValueError('Stored request differs; use a new experiment directory')
        elif len(json.loads((self.out / 'budget.json').read_text())['attempts']) >= MAX_CALLS:
            raise RuntimeError('42-attempt experiment cap reached')
        return super().call(step, prompt, payload, response_schema)


def attempt(calls, step, prompt, payload, response_schema, checker):
    result_path = calls.out / f'sample-{calls.sample}' / f'{step}-result.json'
    try:
        raw = calls.call(step, prompt, payload, response_schema)
        result = {'status': 'valid', 'value': checker(raw)}
    except (ValueError, RuntimeError, OSError) as error:
        result = {'status': 'rejected', 'error': type(error).__name__ + ': ' + str(error)[:400]}
    study.write_json(result_path, result)
    print(f'CHECK {step}: {result["status"]}', flush=True)
    return result.get('value')


def run(out):
    manifest = json.loads((out / 'manifest.json').read_text())
    if (manifest['source_sha256'] != study.digest(SOURCE)
            or manifest['code_sha256'] != study.digest(__file__)
            or manifest['input_sha256'] != study.digest(out / 'input.json')
            or manifest['config_checksum'] != study.config.load(str(study.ROOT / 'poc/config/poc-v7.json')).checksum
            or manifest['contract_sha256'] != digest_value([PROMPT, PROBE_PROMPT, SCOPES])):
        raise ValueError('Source or experiment contract changed')
    data = json.loads((out / 'input.json').read_text())
    with (out / 'run.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for sample in [1, 2, 3]:
            calls = Calls(out, sample)
            for name, scope in SCOPES.items():
                previous, last_fresh, last_update = None, None, None
                for index, snap in enumerate(data[name]):
                    payload = {'question': scope['question'], 'as_of': snap['as_of'], 'current_research': current_context(snap)}
                    step = f'{name}-fresh-{snap["cutoff_seq"]}'
                    last_fresh = attempt(calls, step, PROMPT, payload, schema(snap), lambda answer: make_card(answer, snap, name))
                    if index == 0:
                        previous = last_fresh
                    elif previous is not None and update_required(previous, snap):
                        updated_payload = dict(payload, previous_version=previous)
                        step = f'{name}-update-{snap["cutoff_seq"]}'
                        last_update = attempt(calls, step, PROMPT, updated_payload, schema(snap), lambda answer: make_card(answer, snap, name))
                        previous = last_update
                    elif previous is not None:
                        last_update = previous
                        study.write_json(out / f'sample-{sample}' / f'{name}-update-{snap["cutoff_seq"]}-result.json', {'status': 'unchanged', 'value': previous})
                    else:
                        last_update = None
                for arm, card in [('fresh', last_fresh), ('update', last_update)]:
                    if card is None:
                        continue
                    payload = {'question': scope['question'], 'requested_facets': scope['facets'], 'card': card}
                    attempt(calls, f'{name}-{arm}-probe', PROBE_PROMPT, payload, probe_schema(scope, snap), lambda answer: validate_probe(answer, card, snap, scope))
            calls.archive.conn.close()
    report(out)


def report(out):
    budget = json.loads((out / 'budget.json').read_text())
    rows = []
    for path in sorted(out.glob('sample-*/*-result.json')):
        result = json.loads(path.read_text())
        row = {'sample': path.parent.name, 'step': path.name.removesuffix('-result.json'), 'status': result['status']}
        if result['status'] in {'valid', 'unchanged'}:
            value = result['value']
            if 'arguments' in value:
                row.update(conclusion=value['conclusion'], unused_ids=value['unused_ids'],
                           pairs=sorted({(r['view_id'], eid) for a in value['arguments'] for r in a['references'] for eid in r['evidence_ids']}))
            else:
                row['facets'] = value['facets']
        else:
            row['error'] = result['error']
        rows.append(row)
    summary = {'attempts': len(budget['attempts']), 'estimated_usd': budget['estimated_spent'],
               'source_unchanged': study.digest(SOURCE) == json.loads((out / 'manifest.json').read_text())['source_sha256'], 'results': rows}
    study.write_json(out / 'summary.json', summary)
    text = ['# Fresh versus update: all stored outputs', '', 'Diagnostic observations only; not an accuracy score.', '']
    for path in sorted(out.glob('sample-*/*-result.json')):
        text.extend([f'## {path.parent.name} / {path.stem}', '', '```json', path.read_text(), '```', ''])
    (out / 'outputs.md').write_text('\n'.join(text))
    print(f'FINISHED attempts={summary["attempts"]} estimated_usd={summary["estimated_usd"]:.6f} source_unchanged={summary["source_unchanged"]}', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'run', 'report'])
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    {'prepare': prepare, 'run': run, 'report': report}[args.command](args.out.resolve())


if __name__ == '__main__':
    main()
