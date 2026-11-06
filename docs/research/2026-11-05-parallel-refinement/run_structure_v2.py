"""Freeze and compare split-prompt variants on the saved two-article requests."""
import copy
import hashlib
import json
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD = ROOT / 'docs/research/2026-11-05-parallel-thesis-evidence-poc'
sys.path[:0] = [str(HERE), str(OLD), str(ROOT / 'src')]
import a_id_contract
import b_arm
import run_poc
import run_small_scored as prior
from hivemind import model, placement

PREVIOUS = ROOT / 'poc/data/parallel-restructure-small-2026-11-05-v1/manifest.json'
CASES = prior.IDS
ARMS = ('A0', 'A1', 'B0', 'B1', 'B2')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def wire(request):
    return sha(json.dumps(request).encode())


def basis_labels(user, shown):
    """Append only recorded accounting bases to their own existing question lines."""
    start = user.index('[Open questions immediately before this item]')
    end = user.index('[Research groups]', start)
    block = user[start:end]
    added = []
    for q in shown:
        basis = (q.get('key') or {}).get('basis')
        if basis not in ('GAAP', 'non_GAAP'):
            continue
        line = placement.question_lines([q])[0]
        if block.count(line) != 1:
            raise ValueError('question identity/line mismatch: ' + q['view_id'])
        suffix = '\n      accounting basis: ' + ('GAAP' if basis == 'GAAP' else 'non-GAAP')
        block = block.replace(line, line + suffix, 1)
        added.append((q['view_id'], basis))
    return user[:start] + block + user[end:], added


def build():
    cfg, uni, old = prior.prepare()
    frozen = json.loads(PREVIOUS.read_text())
    saved = {(r['id'], r['arm']): r for r in frozen['requests']}
    if frozen['gold_sha256'] != prior.GOLD_SHA or sha(prior.GOLD.read_bytes()) != prior.GOLD_SHA:
        raise ValueError('frozen gold changed')
    by = {(r['item']['input_id'], r['arm']): r for r in old}
    records = []
    for ident in CASES:
        for lane in ('new', 'existing'):
            original = by[(ident, lane)]
            old_saved = saved[(ident, lane)]
            if wire(old_saved['request']) != old_saved['wire_sha256'] or json.dumps(original['request']) != json.dumps(old_saved['request']):
                raise ValueError('saved source request no longer reconstructs exactly')
            if sha(original['item']['text'].encode()) != old_saved['source_sha256']:
                raise ValueError('article identity mismatch')
            arms = ('A0', 'A1') if lane == 'new' else ('B0', 'B1', 'B2')
            for arm in arms:
                r = copy.deepcopy(original)
                # Source request is the archive's own object and insertion order, never a moved ledger's serialization.
                r['request'] = copy.deepcopy(old_saved['request'])
                r['system'] = r['request']['messages'][0]['content']
                r['user'] = r['request']['messages'][1]['content']
                r['schema'] = r['request']['response_format']['json_schema']['schema']
                labels = []
                if arm in ('B1', 'B2'):
                    r['user'], labels = basis_labels(r['user'], r['shown'])
                if arm == 'A1':
                    r['system'] = (HERE / 'structure-v2-new-thesis.txt').read_text()
                if arm == 'B2':
                    r['system'] = (HERE / 'structure-v2-existing-evidence.txt').read_text()
                r['request'] = model.build_request(r['setting'], r['system'], r['user'], r['schema'], 'extraction', cfg.provider)
                r['variant'] = arm
                r['basis_labels'] = labels
                records.append(r)
        group = {r['variant']: r for r in records if r['item']['input_id'] == ident}
        a = copy.deepcopy(group['A1']['request'])
        a['messages'][0]['content'] = group['A0']['system']
        if json.dumps(a) != json.dumps(group['A0']['request']):
            raise ValueError('A1 changes more than system')
        b2 = copy.deepcopy(group['B2']['request'])
        b2['messages'][0]['content'] = group['B1']['system']
        if json.dumps(b2) != json.dumps(group['B1']['request']):
            raise ValueError('B2 changes more than system')
        stripped = group['B1']['user']
        for qid, basis in group['B1']['basis_labels']:
            label = '\n      accounting basis: ' + ('GAAP' if basis == 'GAAP' else 'non-GAAP')
            line = placement.question_lines([next(q for q in group['B1']['shown'] if q['view_id'] == qid)])[0]
            if stripped.count(line + label) != 1:
                raise ValueError('basis cannot be reversed')
            stripped = stripped.replace(line + label, line, 1)
        if stripped != group['B0']['user'] or group['B1']['system'] != group['B0']['system']:
            raise ValueError('B1 changes more than question labels')
        if json.dumps(group['B1']['schema']) != json.dumps(group['B0']['schema']):
            raise ValueError('B1 changes schema')
    return cfg, uni, records


def manifest(records):
    files = [HERE / 'structure-v2-new-thesis.txt', HERE / 'structure-v2-existing-evidence.txt',
             HERE / 'structure-v2-design.zh.md', HERE / 'source-only-inputs.json', PREVIOUS, Path(__file__)]
    return {'gold_sha256': prior.GOLD_SHA,
            'files': {str(f.resolve()): sha(f.read_bytes()) for f in files},
            'requests': [{'id': r['item']['input_id'], 'arm': r['variant'], 'lane': r['arm'],
                          'basis_labels': [list(x) for x in r['basis_labels']], 'question_count': len(r['shown']),
                          'source_sha256': sha(r['item']['text'].encode()), 'wire_sha256': wire(r['request']),
                          'request': r['request']} for r in records]}


def fake_checks(cfg, uni, records):
    # Existing real-candidate and bad-quote/invalid-ID controls, on all revised requests.
    prior.fake_checks(cfg, uni, records)
    corpus = json.loads((HERE / 'source-only-inputs.json').read_text())
    _, _, saved_b = b_arm.base_requests()
    byid = {r['item']['input_id']: r for r in saved_b}
    judged = labeled = 0
    for sample in corpus:
        r = byid[sample['input_id']]
        new, labels = basis_labels(r['user'], r['shown'])
        expected = [(q['view_id'], q['key']['basis']) for q in r['shown'] if q.get('key') and q['key'].get('basis') in ('GAAP', 'non_GAAP')]
        if labels != expected:
            raise ValueError('known basis omitted or invented')
        judged += len(r['shown'])
        labeled += len(labels)
        for qid, basis in labels:
            line = placement.question_lines([next(q for q in r['shown'] if q['view_id'] == qid)])[0]
            marker = '\n      accounting basis: ' + ('GAAP' if basis == 'GAAP' else 'non-GAAP')
            if new.count(line + marker) != 1:
                raise ValueError('label not attached to right question')
    if judged != 334 or labeled != 19:
        raise ValueError(f'unexpected corpus accounting coverage {judged}/{labeled}')
    # Counterexamples: explicit non-GAAP; not-applicable and unknown must not become GAAP.
    sample = copy.deepcopy(records[-1]['shown'][0])
    sample['key']['basis'] = 'non_GAAP'
    line = placement.question_lines([sample])[0]
    user = '[Open questions immediately before this item]\n' + line + '\n\n[Research groups]'
    rendered, labels = basis_labels(user, [sample])
    if labels != [(sample['view_id'], 'non_GAAP')] or 'accounting basis: non-GAAP' not in rendered:
        raise ValueError('non-GAAP control')
    for val in ('n/a', '', None):
        sample['key']['basis'] = val
        rendered, labels = basis_labels(user, [sample])
        if labels or rendered != user:
            raise ValueError('unknown basis became asserted')
    print('Fake: baseline wire identical; A/B deltas isolated; 334 question rows and 19 bases checked; non-GAAP and unknown controls pass.', flush=True)


def invoke(cfg, uni, r, out, draw):
    name = r['item']['input_id'].replace(':', '_') + '-' + r['variant'] + '-' + str(draw)
    directory = out / name
    directory.mkdir()
    archive = model.Archive(str(directory / 'archive.sqlite'))
    received = []
    def transport(provider, request):
        if json.dumps(request) != json.dumps(r['request']):
            raise ValueError('wire changed')
        response = model.openai_transport(provider, request)
        received.append(True)
        (directory / 'response.json').write_text(json.dumps(response, ensure_ascii=False) + '\n')
        return response
    try:
        answer = model.call(archive, cfg, r['setting'], r['system'], r['user'], r['schema'], 'extraction', 'extract', transport=transport)
        if answer.cached:
            raise ValueError('unexpected archive cache')
        if r['arm'] == 'new':
            handover = a_id_contract.checked_handover(answer.data, r['schema'], r, uni, answer)
        else:
            handover = run_poc.handover(answer.data, r, uni, answer)
        result = {'status': 'ok', 'id': r['item']['input_id'], 'variant': r['variant'], 'draw': draw,
                  'answer': answer.data, 'handover': handover, 'input_tokens': answer.input_tokens,
                  'output_tokens': answer.output_tokens}
    except Exception as exc:
        result = {'status': 'failed', 'id': r['item']['input_id'], 'variant': r['variant'], 'draw': draw,
                  'error': repr(exc), 'response_received': bool(received)}
    finally:
        archive.conn.close()
    (directory / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(name, result['status'], flush=True)
    return result


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ('freeze', 'fake', 'send'):
        raise SystemExit('freeze|fake|send ABSOLUTE_NEW_RUN_DIR')
    command, out = sys.argv[1], Path(sys.argv[2])
    if not out.is_absolute():
        raise ValueError('absolute output required')
    cfg, uni, records = build()
    if command == 'freeze':
        if out.exists():
            raise ValueError('run exists')
        out.mkdir(parents=True)
        (out / 'manifest.json').write_text(json.dumps(manifest(records), ensure_ascii=False, indent=2) + '\n')
        (out / 'status.json').write_text(json.dumps({'status': 'frozen', 'completed': 0}) + '\n')
        print('Frozen', len(records), 'requests;', sha((out / 'manifest.json').read_bytes()), flush=True)
        return
    if manifest(records) != json.loads((out / 'manifest.json').read_text()):
        raise ValueError('manifest drift')
    if command == 'fake':
        fake_checks(cfg, uni, records)
        (out / 'fake-proof.json').write_text(json.dumps({'manifest_sha256': sha((out / 'manifest.json').read_bytes()), 'status': 'ok'}) + '\n')
        return
    proof = json.loads((out / 'fake-proof.json').read_text())
    if proof != {'manifest_sha256': sha((out / 'manifest.json').read_bytes()), 'status': 'ok'}:
        raise ValueError('missing or stale fake proof')
    status_path = out / 'status.json'
    if json.loads(status_path.read_text()) != {'status': 'frozen', 'completed': 0}:
        raise ValueError('existing or interrupted run must not resume automatically')
    status_path.write_text(json.dumps({'status': 'running', 'completed': 0}) + '\n')
    completed = 0
    for ident in CASES:
        for draw in (1, 2, 3):
            group = [r for r in records if r['item']['input_id'] == ident]
            with ThreadPoolExecutor(max_workers=5) as pool:
                futures = [pool.submit(invoke, cfg, uni, r, out, draw) for r in group]
                results = [f.result() for f in futures]
            completed += len(results)
            if any(r['status'] != 'ok' for r in results):
                status_path.write_text(json.dumps({'status': 'incomplete', 'completed': completed}) + '\n')
                raise SystemExit('failed arm; raw results preserved, not retried')
            status_path.write_text(json.dumps({'status': 'running', 'completed': completed}) + '\n')
    status_path.write_text(json.dumps({'status': 'complete', 'completed': completed}) + '\n')


if __name__ == '__main__':
    main()
