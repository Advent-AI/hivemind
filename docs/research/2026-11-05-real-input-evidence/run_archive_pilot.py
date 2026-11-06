"""Paired, independent extraction draws on three archive variants; empty library only."""
import concurrent.futures
import hashlib
import json
import os
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, extraction, model, testdb, universe
import preflight_archived_variants as preflight

VARIANTS = ROOT / 'poc/data/real-evidence-d369-variants-draft-v1'
ORIGINAL = Path('/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite')
GOLD = HERE / 'gold-archive-three-v1.json'
GOLD_SHA = '5e73e033af784b689d19c494f088959e1c8dbebd3d69c1b213b60210644cf176'
PROTOCOL = HERE / 'pilot-protocol-v1.json'
HISTORICAL = HERE / 'preflight-d369/historical-preflight-verified.txt'
REPORT = HERE / 'draft-two-article-inputs.json'
CONFIG = ROOT / 'poc/config/poc-v117.json'
UNIVERSE = ROOT / 'poc/universe.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def plan():
    if digest(GOLD.read_bytes()) != GOLD_SHA:
        raise ValueError('frozen gold hash changed')
    checks = preflight.run(VARIANTS, ORIGINAL)
    cfg = config.load(CONFIG)
    uni = universe.load(UNIVERSE)
    report = json.loads(REPORT.read_text())['report']
    db = sqlite3.connect((VARIANTS / 'items.sqlite').resolve().as_uri() + '?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    manifest = json.loads((VARIANTS / 'manifest.json').read_text())
    gold = json.loads(GOLD.read_text())
    reference = {a['input_id']: a for a in gold['articles']}
    if set(reference) != {r['original_id'] for r in manifest['articles']}:
        raise ValueError('frozen gold article identities differ')
    requests = []
    for rec in manifest['articles']:
        row = db.execute('select * from items where input_id=?', (rec['variant_id'],)).fetchone()
        item = testdb.item_of(row)
        for entry in reference[rec['original_id']]['entries'] + reference[rec['original_id']]['exclusions']:
            for span in entry['source_spans']:
                if span not in item['text']:
                    raise ValueError('frozen gold source span missing from selected variant')
        if len(item['text']) > extraction.MAX_TEXT_CHARS:
            raise ValueError('article would be truncated')
        setting, system, control, schema = extraction.request_for(cfg, item, item['text'], [], uni)
        boundary = '\n\n' + extraction.CLOSING
        if control.count(boundary) != 1:
            raise ValueError('ambiguous insertion boundary')
        block = ('\n\n[Earlier earnings report: background] Source: ' + report['source_uri'] + '\n'
                 + 'Publication day: ' + report['publication_day'] + '\n' + report['text_page'])
        treatment = control.replace(boundary, block + boundary, 1)
        for arm, user in [('control', control), ('report', treatment)]:
            request = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
            identity = model.request_identity(request)[1]
            wire_hash = digest(json.dumps(request).encode('utf-8'))
            check = next(c for c in checks['arms'] if c['variant_id'] == item['input_id'] and c['arm'] == ('control' if arm == 'control' else 'treatment'))
            if wire_hash != check['wire_sha256'] or identity != check['request_identity']:
                raise ValueError('preflight request differs')
            requests.append((item, arm, setting, system, user, schema, identity, wire_hash))
    db.close()
    return cfg, uni, requests


def snapshot(requests):
    files = [CONFIG, UNIVERSE, REPORT, GOLD, VARIANTS / 'manifest.json', HISTORICAL, Path(__file__), HERE / 'preflight_archived_variants.py']
    files += sorted((ROOT / 'src/hivemind').rglob('*.py'))
    files += sorted(p for p in (ROOT / 'src/hivemind').rglob('*') if p.is_file() and p.suffix in ('.txt', '.json', '.md'))
    return {'files': {str(p): digest(p.read_bytes()) for p in files},
            'requests': [{'input_id': i['input_id'], 'arm': arm, 'request_identity': sha, 'wire_sha256': wire}
                         for i, arm, _, _, _, _, sha, wire in requests]}


def main():
    if len(sys.argv) == 2 and sys.argv[1] == '--freeze':
        if PROTOCOL.exists():
            raise SystemExit('protocol exists: refusing overwrite')
        _, _, requests = plan()
        PROTOCOL.write_text(json.dumps(snapshot(requests), ensure_ascii=False, indent=2) + '\n')
        print('protocol frozen', digest(PROTOCOL.read_bytes()))
        return
    if len(sys.argv) != 4 or sys.argv[1] not in ('--fake', '--send') or not Path(sys.argv[2]).is_absolute() or sys.argv[3] not in ('1', '2', '3'):
        raise SystemExit('usage: run_archive_pilot.py --freeze OR --fake|--send /absolute/new-output-directory DRAW')
    mode, out = sys.argv[1], Path(sys.argv[2])
    if out.exists():
        raise SystemExit('output exists: refusing restart or overwrite')
    cfg, uni, requests = plan()
    if not PROTOCOL.exists() or json.loads(PROTOCOL.read_text()) != snapshot(requests):
        raise SystemExit('frozen protocol differs: refusing send')
    out.mkdir(parents=True)
    inputs = {'mode': mode, 'gold_sha256': GOLD_SHA, 'config_sha256': digest(CONFIG.read_bytes()),
              'universe_sha256': digest(UNIVERSE.read_bytes()), 'report_sha256': digest(REPORT.read_bytes()),
              'manifest_sha256': digest((VARIANTS / 'manifest.json').read_bytes()),
              'script_sha256': digest(Path(__file__).read_bytes()), 'library': 'empty', 'draw': int(sys.argv[3]),
              'requests': [{'input_id': i['input_id'], 'arm': arm, 'request_identity': sha, 'wire_sha256': wire}
                           for i, arm, _, _, _, _, sha, wire in requests]}
    (out / 'plan.json').write_text(json.dumps(inputs, ensure_ascii=False, indent=2) + '\n')
    def run_one(job):
        idx, draw, entry = job
        item, arm, setting, system, user, schema, identity, wire_hash = entry
        directory = out / f'{idx:02d}-{arm}-draw{draw}'
        directory.mkdir()
        (directory / 'intent.json').write_text(json.dumps({'request_identity': identity, 'wire_sha256': wire_hash, 'input_id': item['input_id'], 'draw': draw, 'arm': arm}) + '\n')
        archive = model.Archive(str(directory / 'archive.sqlite'))
        received = []
        def fake(provider, request):
            if digest(json.dumps(request).encode('utf-8')) != wire_hash:
                raise ValueError('fake wire mismatch')
            return {'choices': [{'message': {'content': json.dumps({'evidence': [], 'candidates': [], 'new_groups': []})}}], 'usage': {'prompt_tokens': 0, 'completion_tokens': 0}}
        def real(provider, request):
            if digest(json.dumps(request).encode('utf-8')) != wire_hash:
                raise ValueError('real wire mismatch')
            response = model.openai_transport(provider, request)
            received.append(response)
            (directory / 'response.json').write_text(json.dumps(response, ensure_ascii=False) + '\n')
            return response
        try:
            answer = model.call(archive, cfg, setting, system, user, schema, 'extraction', 'extract', transport=fake if mode == '--fake' else real)
            if answer.cached or answer.request_sha256 != identity:
                raise ValueError('cache or request mismatch')
            evidence, candidates, dropped, groups = extraction.sift_with_groups(answer.data, item, item['text'], set(), uni)
            handover = extraction.file_reading(extraction.Reading(evidence, candidates, dropped, groups, answer, setting.prompt_version.rpartition('-')[2]), item, [])
            result = {'status': 'ok', 'answer': answer.data, 'sift': {'evidence': evidence, 'candidates': candidates, 'dropped': dropped, 'new_groups': groups},
                      'handover': {'evidence': handover.evidence, 'candidates': handover.candidates, 'dropped': handover.dropped, 'new_groups': handover.new_groups},
                      'input_tokens': answer.input_tokens, 'output_tokens': answer.output_tokens,
                      'known_final_response_cost_usd': answer.cost_usd if received and received[0].get('usage') else None,
                      'earlier_retry_cost': 'unknown; production transport may retry'}
        except Exception as error:
            result = {'status': 'failed_or_unknown', 'error': repr(error)[:500],
                      'raw_usage': received[0].get('usage') if received else None, 'cost': 'unknown; inspect raw usage and retries'}
        (directory / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        archive.conn.close()
        return {'directory': directory.name, 'status': result['status']}
    jobs = [(idx, int(sys.argv[3]), entry) for idx, entry in enumerate(requests)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        completed = list(pool.map(run_one, jobs))
    (out / 'complete.json').write_text(json.dumps(completed, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'mode': mode, 'planned': len(jobs), 'ok': sum(x['status'] == 'ok' for x in completed), 'failed_or_unknown': sum(x['status'] != 'ok' for x in completed)}))


if __name__ == '__main__':
    main()
