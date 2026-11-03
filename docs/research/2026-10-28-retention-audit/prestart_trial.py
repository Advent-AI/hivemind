"""Paired experiment on archived v38 placement requests; no product writes."""
import collections, concurrent.futures, hashlib, json, os, re, sqlite3, sys, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, model, placement
HERE = Path(__file__).resolve().parent
ARCH = '/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/archive.sqlite'
OUT = HERE / 'placement-trial-2026-10-28'

def load(name): return json.loads((HERE / name).read_text())

def one_send(provider, request):
    # One attempt only: no hidden retries can consume the reserved budget.
    url, _ = model.ENDPOINTS[provider]
    data = json.dumps(request).encode('utf-8')
    headers = {'Authorization': 'Bearer ' + model._key(provider), 'Content-Type': 'application/json'}
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers, method='POST'), timeout=600) as response:
        return json.loads(response.read().decode('utf-8'))

def main():
    cfg = config.load(str(ROOT / 'poc/config/poc-v38.json'))
    reference = load('source-reference.json'); coverage = load('coverage.json')
    homes_doc = load('prestart-expected-homes-2026-10-28.json'); homes = homes_doc['homes']
    seed_doc = load('prestart-driver-hypothesis-2026-10-28.json'); seed = seed_doc['directions']
    assert hashlib.sha256((HERE/'source-reference.json').read_bytes()).hexdigest() == homes_doc['reference_sha256']
    assert hashlib.sha256((HERE/'prestart-driver-hypothesis-2026-10-28.json').read_bytes()).hexdigest() == homes_doc['seed_sha256']
    assert set(homes) == {x['id'] for x in coverage} and len(coverage) == 33
    ledger = load('ledger.json')['v38']; labels = load('labels-v38.json')
    numbers = [a['article_no'] for a in reference['articles']]; assert len(numbers) == len(set(numbers)) == 20
    db = sqlite3.connect('file:' + ARCH + '?mode=ro', uri=True)
    rows = db.execute("select request_sha256,request_json from model_calls where purpose='place' and request_sha256 not like '%:%'").fetchall()
    cases = []; missing = []
    for number in numbers:
        article = ledger[number-1]; assert article['article_no'] == number
        matches = []
        for sha, raw in rows:
            req = json.loads(raw); u = req['messages'][1]['content']
            if u.split('\n',1)[0].endswith(': ' + article['title']): matches.append((sha,req))
        if not matches:
            missing.append(number); continue
        assert len(matches)==1, (number,len(matches))
        sha, req = matches[0]; system = req['messages'][0]['content']; user = req['messages'][1]['content']
        rebuilt = model.build_request(cfg.placement,system,user,placement.SCHEMA,'placement',cfg.provider)
        assert model.request_identity(rebuilt)[1] == sha, number
        section = user.split('\n\n[Statements]\n',1)[1]
        ids = re.findall(r'^  - (e\d+) \[',section,re.M); assert ids and len(ids)==len(set(ids))
        records = {r['id']:r for r in article['records']}; assert set(ids)<=set(records)
        # d-questions are exploratory research topics, not product views.
        additions = ''.join('\n  - %s (NVDA, due 2027-12-31): %s\n      takes: %s' % (d['id'],d['question'],d['question']) for d in seed)
        arm = user.replace('\n\n[Statements]\n', additions+'\n\n[Statements]\n',1)
        assert arm != user and arm.replace(additions,'',1)==user
        shown = set(re.findall(r'^  - (v\d+) \(',user.split('\n\n[Statements]\n',1)[0],re.M))
        cases.append(dict(article=number,system=system,control=user,arm=arm,ids=ids,shown=sorted(shown),records=records))
    assert cases and not missing, missing
    case_by_n={c['article']:c for c in cases}
    eligible=[]
    for fact in coverage:
        cell=fact['versions']['v38']; case=case_by_n[fact['article_no']]
        eligible.append(dict(id=fact['id'],article=fact['article_no'],core=fact['core'],raw_ids=cell['raw_ids'],
                             pre_placement=bool(cell['complete'] and cell['raw_ids'] and set(cell['raw_ids'])<=set(case['ids']))))
    plan=[]; total=0
    for case in cases:
        for kind in ('control','arm'):
            request=model.build_request(cfg.placement,case['system'],case[kind],placement.SCHEMA,'placement',cfg.provider)
            # UTF-8 bytes are a conservative token bound; cap includes each maximum completion.
            n=len(json.dumps(request).encode()); maxout=cfg.placement.max_output_tokens
            bound=(n*model.PRICES[cfg.placement.model][0]+maxout*model.PRICES[cfg.placement.model][1])/1e6
            for draw in range(1,4): plan.append((case,kind,draw)); total+=bound
    assert total <= .60, total
    print('PLAN',json.dumps({'cases':len(cases),'missing':missing,'calls':len(plan),'max_cost_usd':round(total,6),'eligible_facts':sum(x['pre_placement'] for x in eligible),'eligible_core':sum(x['pre_placement'] and x['core'] for x in eligible)},ensure_ascii=False),flush=True)
    if sys.argv[1]=='prepare': return
    assert sys.argv[1]=='send' and OUT.is_dir()
    archives={(kind,draw):model.Archive(str(OUT / ('%s-%s.sqlite'%(kind,draw)))) for kind in ('control','arm') for draw in range(1,4)}
    def run(task):
        c,kind,draw=task
        try:
            a=model.call(archives[kind,draw],cfg,cfg.placement,c['system'],c[kind],placement.SCHEMA,'placement','place',transport=one_send)
            pp=a.data['placements']; ids=[p['id'] for p in pp]; allowed=set(c['shown']) | ({d['id'] for d in seed} if kind=='arm' else set())
            if sorted(ids)!=sorted(c['ids']) or any(set(p['links'])-allowed for p in pp):
                raise ValueError('incomplete, duplicate or invalid ID in answer')
            return {'article':c['article'],'kind':kind,'draw':draw,'placements':pp,'cost':a.cost_usd,'cached':a.cached}
        except Exception as e:
            return {'article':c['article'],'kind':kind,'draw':draw,'error':type(e).__name__+': '+str(e)[:300]}
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for future in concurrent.futures.as_completed([pool.submit(run,t) for t in plan]):
            row=future.result(); results.append(row)
            with (OUT/'responses.ndjson').open('a') as f: f.write(json.dumps(row,ensure_ascii=False)+'\n')
            print('DONE',len(results),'/',len(plan),'article',row['article'],row['kind'],row['draw'],'error',row.get('error',''),flush=True)
    scores={}
    for kind in ('control','arm'):
        for draw in range(1,4):
            group=[x for x in results if x['kind']==kind and x['draw']==draw]; errors=[x for x in group if 'error' in x]
            if errors: scores[f'{kind}-{draw}']={'errors':errors}; continue
            all_links={}
            counts=collections.Counter(); details=[]
            for row in group:
                c=case_by_n[row['article']]; decisions={p['id']:p['links'] for p in row['placements']}
                for rid in c['ids']:
                    rec=c['records'][rid]; links=list(decisions[rid])
                    # A candidate that actually survived the original downstream checks is held constant.
                    if any(x.startswith('c') for x in rec['links']) and rec['stored_id']:
                        links=list(dict.fromkeys(links + rec['stored_links']))
                    all_links[(c['article'],rid)]=links
                    if links:
                        label=labels[str(c['article'])]['records'][rid]['label']; counts[label]+=1
                        details.append({'article':c['article'],'id':rid,'label':label,'links':links,'text':rec['one_line']})
            facts=[]
            for e in eligible:
                links=[all_links.get((e['article'],rid),[]) for rid in e['raw_ids']]
                ok=e['pre_placement'] and all(set(ls)&set(homes[e['id']]) for ls in links)
                facts.append(dict(e,links=links,correct=bool(ok)))
            scores[f'{kind}-{draw}']={'correct':sum(x['correct'] for x in facts),'core_correct':sum(x['correct'] and x['core'] for x in facts),'placed_labels':dict(counts),'facts':facts,'placed':details,'cost':round(sum(x['cost'] for x in group),6)}
    (OUT/'scores.json').write_text(json.dumps({'plan_upper_bound_usd':total,'missing':missing,'eligible':eligible,'scores':scores},ensure_ascii=False,indent=2))
    print('SCORES',json.dumps({k:{x:v for x,v in s.items() if x not in ('facts','placed')} for k,s in scores.items()},ensure_ascii=False),flush=True)
if __name__=='__main__': main()
