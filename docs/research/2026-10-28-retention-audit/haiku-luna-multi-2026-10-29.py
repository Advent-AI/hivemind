"""Four user-decided articles, three independent extraction calls per model."""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
import urllib.error

from hivemind import config, extraction, model, universe

HERE = Path(__file__).resolve().parent
RUN = HERE / 'haiku-luna-multi-2026-10-29'
DESIGN = HERE / 'haiku-luna-multi-design-2026-10-29.md'
ROOT = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
ARCHIVE = '/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/archive.sqlite'
IDS = {'memory':'gnews:fbce0469dbb5b33e2c34a0f5', 'amd':'gnews:55b3b854d30ecb73679c2088',
       'singapore':'gnews:1eeceeb212a2c82c2e75e806', 'policy':'gnews:f9e7da6ddbf890fa64baf922'}
CAP = .60
spec = importlib.util.spec_from_file_location('haiku_probe', HERE / 'haiku-extraction-probe-2026-10-29.py')
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def put(name, obj):
    with (RUN / name).open('x', encoding='utf-8') as file:
        json.dump(obj, file, ensure_ascii=False, indent=2)
        file.write('\n')


def read(name):
    return json.loads((RUN / name).read_text())


def source(name):
    db = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    item = dict(db.execute('select * from items where input_id=?', (IDS[name],)).fetchone())
    item['object_identifiers'] = json.loads(item['object_identifiers'])
    cfg = config.load(str(ROOT / 'poc/config/poc-v38.json'))
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    setting, system, user, schema = extraction.request_for(cfg, item, item['text'], [], uni, [])
    gpt = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
    assert item['category'] == 'T7' and gpt['model'] == 'gpt-6-luna' and gpt['max_completion_tokens'] == 8000
    haiku = {'model': 'claude-haiku-5-5', 'max_tokens': 8000, 'system': system,
             'messages': [gpt['messages'][1]], 'output_config': {'effort': 'low', 'format': {'type': 'json_schema', 'schema': schema}}}
    assert gpt['messages'] == [{'role': 'system', 'content': haiku['system']}, *haiku['messages']]
    assert probe.previous.wire(schema) == probe.previous.wire(haiku['output_config']['format']['schema'])
    return item, uni, setting, schema, gpt, haiku


def prepare():
    RUN.mkdir(exist_ok=False)
    archive = sqlite3.connect(f'file:{ARCHIVE}?mode=ro', uri=True)
    manifests = {}
    reserve = 0
    for name in IDS:
        item, uni, setting, schema, gpt, haiku = source(name)
        digest = model.request_identity(gpt)[1]
        found = archive.execute('select count(*) from model_calls where request_sha256=?', (digest,)).fetchone()[0]
        assert (found == 1) if name == 'singapore' else (found == 0)
        put(f'{name}-gpt-request.json', gpt)
        put(f'{name}-haiku-request.json', haiku)
        b1 = 3 * len(probe.previous.wire(gpt)) + 16384
        b2 = 3 * len(probe.previous.wire(haiku)) + 16384
        input_rate, output_rate = (.5, 2.5) if b2 > 100000 else (.1, .5)
        amount = 3*(b1*.1+8064*.5)/1e6 + 3*(b2*input_rate+8064*output_rate)/1e6
        reserve += amount
        manifests[name] = {'input_id': IDS[name], 'source_sha256': hashlib.sha256(item['text'].encode()).hexdigest(),
                           'request_sha256': digest, 'archive_matches': found, 'gpt_input_bound': b1,
                           'haiku_input_bound': b2, 'haiku_high_tariff': b2 > 100000,
                           'reserved_usd': amount,
                           'files': {f'{name}-{p}-request.json': probe.previous.digest(RUN / f'{name}-{p}-request.json') for p in ('gpt', 'haiku')}}
    assert reserve < CAP
    put('manifest.json', {'articles': manifests, 'design_sha256': probe.previous.digest(DESIGN),
        'reserved_usd': reserve, 'cap_usd': CAP, 'output_bound': 8064, 'planned_calls': 24,
        'gold_note': 'Six specific user-decided cases in the design; no complete article or population benchmark.'})
    print('prepared', len(IDS), 'articles; 24 calls; reserved USD', round(reserve, 6))


def verify():
    m = read('manifest.json')
    assert m['design_sha256'] == probe.previous.digest(DESIGN) and m['reserved_usd'] < CAP
    for name in IDS:
        item, uni, setting, schema, gpt, haiku = source(name)
        a = m['articles'][name]
        assert a['source_sha256'] == hashlib.sha256(item['text'].encode()).hexdigest()
        assert a['request_sha256'] == model.request_identity(gpt)[1]
        for file, digest in a['files'].items():
            assert probe.previous.digest(RUN / file) == digest
        assert probe.previous.wire(gpt) == probe.previous.wire(read(f'{name}-gpt-request.json'))
        assert probe.previous.wire(haiku) == probe.previous.wire(read(f'{name}-haiku-request.json'))
    # Existing v38 archive answer provides a production-path positive control; remove a required quote to create a negative control.
    item, uni, setting, schema, gpt, haiku = source('singapore')
    db = sqlite3.connect(f'file:{ARCHIVE}?mode=ro', uri=True)
    raw = db.execute('select answer_json from model_calls where request_sha256=?', (model.request_identity(gpt)[1],)).fetchone()
    answer = json.loads(raw[0])
    assert not model.check_schema(answer, schema) and answer['evidence']
    bad = json.loads(json.dumps(answer)); del bad['evidence'][0]['quote']
    assert model.check_schema(bad, schema)
    extraction.sift_with_groups(answer, item, item['text'], set(), uni, english=True, shown_group_ids=(), version='v22', keep_unlinked=True)
    print('verified four request pairs, archive identity, positive and missing-quote negative controls', flush=True)


def one(name, provider, number):
    start = time.monotonic()
    try:
        if provider == 'haiku':
            response = probe.haiku_api('https://api.anthropic.com/v1/messages', read(f'{name}-haiku-request.json'))
            complete = response.get('stop_reason') == 'end_turn'
            content = ''.join(c.get('text', '') for c in response.get('content', []) if c.get('type') == 'text')
        else:
            response = probe.previous.api('gpt', 'https://api.openai.com/v1/chat/completions', read(f'{name}-gpt-request.json'))
            complete = response['choices'][0]['finish_reason'] == 'stop'
            content = response['choices'][0]['message'].get('content') or ''
        try:
            answer = json.loads(content)
        except (ValueError, TypeError):
            answer = None
        item, uni, setting, schema, _, _ = source(name)
        errors = model.check_schema(answer, schema)
        record = {'response': response, 'answer': answer, 'completed': complete, 'schema_errors': errors,
                  'seconds': round(time.monotonic()-start,2)}
        if complete and not errors:
            try:
                e,c,d,g=extraction.sift_with_groups(answer, item, item['text'], set(), uni, english=True, shown_group_ids=(), version='v22', keep_unlinked=True)
                record['sift']={'evidence':e,'candidates':c,'dropped':d,'new_groups':g}
            except Exception as exc:
                record['sift_error']=type(exc).__name__
    except urllib.error.HTTPError as exc:
        record={'error':'HTTP error','http_status':exc.code,'seconds':round(time.monotonic()-start,2)}
    except Exception as exc:
        record={'error':type(exc).__name__,'seconds':round(time.monotonic()-start,2)}
    put(f'{name}-{provider}-{number}.json', record)
    print(name,provider,number,'completed',record.get('completed',False),'error',record.get('error'),flush=True)
    return record


def anomalous(name, provider, record):
    usage=record.get('response',{}).get('usage')
    if usage is None:
        return False  # unknown is charged at full reserve, not assumed free
    m=read('manifest.json')['articles'][name]
    if provider == 'haiku':
        inp=sum(usage.get(k,0) for k in ('input_tokens','cache_creation_input_tokens','cache_read_input_tokens'))
        out=usage.get('output_tokens',0)
        higher=inp>100000 and not m['haiku_high_tariff']
        cost=(inp*(.5 if inp>100000 else .1)+out*(2.5 if inp>100000 else .5))/1e6
        bound=(m['haiku_input_bound']*(.5 if m['haiku_high_tariff'] else .1)+8064*(2.5 if m['haiku_high_tariff'] else .5))/1e6
        return inp>m['haiku_input_bound'] or out>8064 or higher or cost>bound
    inp=usage.get('prompt_tokens',0);out=usage.get('completion_tokens',0)
    return inp>m['gpt_input_bound'] or out>8064 or (inp*.1+out*.5)>(m['gpt_input_bound']*.1+8064*.5)


def worker():
    verify()
    jobs=[(n,p,i) for n in IDS for i in (1,2,3) for p in ('haiku','gpt')]
    pending={};done=[];stop=False
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        while jobs or pending:
            while jobs and len(pending)<8 and not stop:
                job=jobs.pop(0);pending[pool.submit(one,*job)]=job
            if not pending: break
            finished,_=concurrent.futures.wait(pending,return_when=concurrent.futures.FIRST_COMPLETED)
            for future in finished:
                job=pending.pop(future); result=future.result();done.append({'job':job,'completed':result.get('completed',False),'error':result.get('error'),'usage':result.get('response',{}).get('usage')})
                if anomalous(job[0],job[1],result): stop=True
    put('run-summary.json', {'planned':24,'sent':len(done),'not_sent':jobs,'stopped_on_usage_anomaly':stop,'samples':done,'semantic_status':'pending manual review'})
    print('finished',len(done),'remaining',len(jobs),'anomaly',stop,flush=True)


def launch():
    verify()
    try:
        probe.haiku_api('https://api.anthropic.com/v1/models/claude-haiku-5-5')
    except urllib.error.HTTPError as error:
        print('Haiku model access HTTP',error.code); return
    except (OSError,subprocess.CalledProcessError,RuntimeError) as error:
        print('Haiku model access failed:',type(error).__name__); return
    assert not (RUN/'run.pid').exists()
    with (RUN/'run.log').open('x') as log:
        p=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'worker'],stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONPATH=str(ROOT/'src')))
    (RUN/'run.pid').write_text(str(p.pid)+'\n')
    print('detached pid',p.pid)


if __name__=='__main__':
    {'prepare':prepare,'verify':verify,'launch':launch,'worker':worker}[sys.argv[1]]()
