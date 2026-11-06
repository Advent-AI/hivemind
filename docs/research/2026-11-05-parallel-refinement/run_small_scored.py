"""Two real articles, two split calls. Freeze requests and test using a fake before sending."""
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
from hivemind import extraction, model

IDS = ('gnews:085b1e1a1543437edb9756d6', 'gnews:4d1b1ca014068fb532f116b3')
GOLD = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-dev.json')
GOLD_SHA = '6f9476bb6a81ea590af273a71565e7c3c0f49908d26274b8482d52cfdee31a21'


def digest(value):
    return hashlib.sha256(value).hexdigest()


def wire(req):
    return digest(json.dumps(req).encode())


def prepare():
    if digest(GOLD.read_bytes()) != GOLD_SHA:
        raise ValueError('frozen gold hash changed')
    cfg, uni, all_b = b_arm.base_requests()
    source = json.loads((HERE / 'source-only-inputs.json').read_text())
    records = []
    for ident in IDS:
        base = next(x for x in all_b if x['item']['input_id'] == ident)
        saved = next(x for x in source if x['input_id'] == ident)
        if base['item']['text'] != saved['article'] or base['shown'] != saved['questions']:
            raise ValueError('source or historical questions changed')
        b = dict(base)
        b['schema'] = copy.deepcopy(base['schema'])
        b['schema']['properties']['evidence']['items']['properties']['links']['description'] = b_arm.NEW
        b['system'] = (HERE / 'restructured-existing-evidence-draft.txt').read_text()
        b['arm'] = 'existing'
        setting, _, user, schema = extraction.request_for(cfg, base['item'], base['item']['text'], base['shown'], uni)
        oldhead = f'[Open questions at the start of {base["item"]["publication_day"]}]'
        assert user.count(oldhead) == user.count(extraction.CLOSING) == user.count(extraction.GROUPS_INSTRUCTION) == 1
        user = user.replace(oldhead, '[Open questions immediately before this item]', 1)
        user = user.replace(extraction.GROUPS_INSTRUCTION, '[Research groups] No separate group list is supplied. For a candidate that tracks an ongoing matter (a product rollout, a deal, a policy process, an investment or demand cycle), declare the group in new_groups (local ids n1, n2 …) and cite it in group_refs; leave group_refs empty for a company\'s own financial lines.', 1)
        user = user.replace(extraction.CLOSING, 'Return candidates, their article evidence, and any new groups per the schema. Evidence links contain only candidate IDs from this answer; each candidate evidence_ids names its own evidence.', 1)
        user = user.replace('Before you return the answer, check it once.', 'Before you return the answer, check it once. A clearly retold past actual figure may be kept or omitted; still-effective guidance and forecasts retain their usual weight.', 1)
        user = user.replace("- a share-price move, an investor's position or trade, or the market value", "- a share-price move or an investor's position or trade", 1)
        user = user.replace('it does not cover the news behind the move;', "it does not cover the news behind the move; the covered company's market value, a standalone valuation multiple, and its share-price reaction after earnings are optional;", 1)
        assert user.endswith('Return only the evidence items you keep.')
        user = user[:-len('Return only the evidence items you keep.')] + 'Return the candidates, new groups, and only the evidence items that pass this check, as required by the schema.'
        schema = a_id_contract.experimental_schema(schema)
        schema['properties']['evidence']['items']['properties']['links']['description'] = 'IDs of this answer’s candidate questions that this evidence can inform, whether supporting or opposing; never an existing question ID.'
        a = dict(base, arm='new', setting=setting, user=user, schema=schema, system=(HERE / 'restructured-new-thesis-draft.txt').read_text())
        for r in (a, b):
            r['request'] = model.build_request(r['setting'], r['system'], r['user'], r['schema'], 'extraction', cfg.provider)
            if r['item']['text'] not in r['user']:
                raise ValueError('article not in request')
        def questions(u):
            begin = u.index('[Open questions immediately before this item]')
            return u[begin:u.index('[Research groups]', begin)]
        if questions(a['user']) != questions(b['user']):
            raise ValueError('different question block')
        records.extend((a, b))
    return cfg, uni, records


class Dummy:
    call_id = 0
    request_sha256 = 'fake'
    cached = False
    cost_usd = 0


def fake_checks(cfg, uni, records):
    for r in records:
        if r['arm'] == 'new':
            d = {'evidence': [], 'candidates': [], 'new_groups': []}
            a_id_contract.checked_handover(d, r['schema'], r, uni, Dummy())
            saved = json.loads((ROOT / 'poc/data/parallel-thesis-evidence-poc-2026-11-05/gnews_d144b91986c520ea36e718cf-new/result.json').read_text())['answer']
            positive = copy.deepcopy(saved)
            a_id_contract.check_answer(positive, r['schema'])
            invalid = copy.deepcopy(positive)
            invalid['candidates'][0]['id'] = 'n1'
            duplicate = copy.deepcopy(positive)
            duplicate['candidates'].append(copy.deepcopy(duplicate['candidates'][0]))
            for bad in (invalid, duplicate):
                try:
                    a_id_contract.check_answer(bad, r['schema'])
                except a_id_contract.IdentityRefusal:
                    pass
                else:
                    raise ValueError('invalid candidate identity accepted')
        else:
            e = {'id': 'e1', 'quote': r['item']['text'][:100], 'one_line': 'A source-backed statement.', 'speaker': 'Source', 'original_who': '', 'original_day': '', 'tier': 'fact', 'event_time': '', 'links': [r['shown'][0]['view_id']]}
            d = {'evidence': [e]}
            if model.check_schema(d, r['schema']) or len(run_poc.handover(d, r, uni, Dummy())['evidence']) != 1:
                raise ValueError('positive evidence refused')
            bad = copy.deepcopy(d)
            bad['evidence'][0]['quote'] = 'A fabricated quote that cannot occur in the source.'
            if run_poc.handover(bad, r, uni, Dummy())['evidence']:
                raise ValueError('fabricated quote accepted')
            bad = copy.deepcopy(d)
            bad['evidence'][0]['links'] = ['missing-id']
            if run_poc.handover(bad, r, uni, Dummy())['evidence']:
                raise ValueError('invalid existing ID accepted')
        with tempfile.TemporaryDirectory(prefix='split-small-fake-') as tmp:
            archive = model.Archive(str(Path(tmp) / 'archive.sqlite'))
            def fake(provider, request):
                if json.dumps(request) != json.dumps(r['request']):
                    raise ValueError('sent wire differs from manifest')
                return {'choices': [{'message': {'content': json.dumps(d)}}], 'usage': {'prompt_tokens': 0, 'completion_tokens': 0}}
            answer = model.call(archive, cfg, r['setting'], r['system'], r['user'], r['schema'], 'extraction', 'extract', transport=fake)
            if answer.cached:
                raise ValueError('unexpected fake cache')
            archive.conn.close()
    if run_poc.join_results([{'status': 'ok', 'arm': 'new'}, {'status': 'failed', 'arm': 'existing'}])['status'] != 'incomplete':
        raise ValueError('failed pair reported complete')
    print('Fake check: 4 requests, article/ID/snapshot checks, schema, quote refusal and partial-pair failure passed.', flush=True)


def invoke(cfg, uni, r, out):
    directory = out / (r['item']['input_id'].replace(':', '_') + '-' + r['arm'])
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
        ans = model.call(archive, cfg, r['setting'], r['system'], r['user'], r['schema'], 'extraction', 'extract', transport=transport)
        if ans.cached:
            raise ValueError('unexpected paid-run cache')
        h = a_id_contract.checked_handover(ans.data, r['schema'], r, uni, ans) if r['arm'] == 'new' else run_poc.handover(ans.data, r, uni, ans)
        result = {'status': 'ok', 'id': r['item']['input_id'], 'arm': r['arm'], 'answer': ans.data, 'handover': h, 'input_tokens': ans.input_tokens, 'output_tokens': ans.output_tokens}
    except Exception as exc:
        result = {'status': 'failed', 'id': r['item']['input_id'], 'arm': r['arm'], 'error': repr(exc), 'response_received': bool(received)}
    finally:
        archive.conn.close()
    (directory / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(result['id'], result['arm'], result['status'], flush=True)
    return result


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ('--fake', '--send'):
        raise SystemExit('usage: --fake|--send NEW_ABSOLUTE_DIRECTORY')
    out = Path(sys.argv[2])
    if not out.is_absolute() or out.exists():
        raise ValueError('directory must be absolute and new')
    cfg, uni, records = prepare()
    fake_checks(cfg, uni, records)
    out.mkdir(parents=True)
    manifest = [{'id': r['item']['input_id'], 'arm': r['arm'], 'question_count': len(r['shown']), 'source_sha256': digest(r['item']['text'].encode()), 'wire_sha256': wire(r['request']), 'request': r['request']} for r in records]
    (out / 'manifest.json').write_text(json.dumps({'gold_sha256': GOLD_SHA, 'requests': manifest}, ensure_ascii=False, indent=2) + '\n')
    if sys.argv[1] == '--fake':
        return
    results = []
    for ident in IDS:
        pair = [r for r in records if r['item']['input_id'] == ident]
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(invoke, cfg, uni, r, out) for r in pair]
            pair_results = [f.result() for f in futures]
        results.extend(pair_results)
        joined = run_poc.join_results(pair_results)
        (out / (ident.replace(':', '_') + '-join.json')).write_text(json.dumps(joined, ensure_ascii=False, indent=2) + '\n')
        if joined['status'] != 'ok':
            break
    (out / 'complete.json').write_text(json.dumps({'status': 'ok' if len(results) == 4 and all(x['status'] == 'ok' for x in results) else 'incomplete', 'requests': len(results)}, indent=2) + '\n')


if __name__ == '__main__':
    main()
