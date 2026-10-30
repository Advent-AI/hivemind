"""Freeze a one-variable research-scope comparison; this command makes no model calls."""
import copy
import hashlib
import importlib.util
import json
import re
import sqlite3
import sys
from pathlib import Path

from hivemind import config,extraction,model,research_context,universe

ROOT=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
HERE=ROOT/'docs/research/2026-10-28-retention-audit'
DATA=Path('/Users/lchingen/hivemind/poc/data')
WEEK=DATA/'english-v38-nvda-1w-2026-10-28'
RUN=HERE/'stage4-scope-arm-2026-10-29'
DESIGN=HERE/'stage4-scope-arm-design-v3-2026-10-29.md'
OLD=HERE/'stage4-haiku-luna-v3-2026-10-29'
CASES=[('nn','gnews:9a13ec8bfdc32e585c1f0604','e1',7,'development'),
       ('nvidia','nvblog:nvidia-unlocks-ai-compute-at-scale-capital-partners-to-power-ai-infrastructure-buildout','e1',1,'test'),
       ('corning','gnews:c3c81e4fb573a723e4081dd0','e3',6,'test')]
FIELDS=('id','quote','one_line','speaker','original_who','original_day','tier','event_time')
spec=importlib.util.spec_from_file_location('stage4_prep',HERE/'stage4-haiku-luna-v3-2026-10-29.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def put(name,obj):
    with (RUN/name).open('x',encoding='utf-8') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')


def build():
    cfg=config.load(str(ROOT/'poc/config/poc-v38.json'));uni=universe.load(str(ROOT/'poc/universe.json'));result={}
    with sqlite3.connect(f'file:{DATA}/items-nvda-2026-07-01-10-27.sqlite?mode=ro',uri=True) as items, \
         sqlite3.connect(f'file:{WEEK}/views.sqlite?mode=ro',uri=True) as views, \
         sqlite3.connect(f'file:{WEEK}/archive.sqlite?mode=ro',uri=True) as archive:
        items.row_factory=sqlite3.Row
        calls=list(archive.execute("select call_id,request_json,answer_json from model_calls where purpose='extract' and answer_json is not null and request_sha256 not like '%:%'"))
        for name,ident,target_id,seq,split in CASES:
            row=items.execute('select * from items where input_id=?',(ident,)).fetchone()
            if row is None or views.execute('select seq from handovers where input_id=?',(ident,)).fetchall()!=[(seq,)]:raise ValueError('item or sequence mismatch')
            item=dict(row);item['object_identifiers']=json.loads(item['object_identifiers']);text=item['text']
            covered=[{'kind':o['kind'],'value':o['value']} for o in item['object_identifiers'] if o.get('kind')=='ticker' and uni.has(o['value'])]
            if covered!=[{'kind':'ticker','value':'NVDA'}]:raise ValueError('coverage differs from reference')
            hits=[]
            for call,encoded,answer in calls:
                req=json.loads(encoded);user=next(m['content'] for m in req['messages'] if m['role']=='user');m=re.search(r'\[Item\] id (\S+?), category ',user)
                if m and m.group(1)==ident:hits.append((call,req,json.loads(answer)))
            if len(hits)!=1:raise ValueError('missing or ambiguous extraction')
            call,req,answer=hits[0];setting,system,user,schema=extraction.request_for(cfg,item,text,[],uni,[])
            original=model.build_request(setting,system,user,schema,'extraction',cfg.provider)
            if model.request_identity(original)[1]!=model.request_identity(req)[1] or model.check_schema(answer,schema):raise ValueError('stored extraction differs')
            ev,_,_,_=extraction.sift_with_groups(answer,item,text,set(),uni,english=True,shown_group_ids=(),version='v22',keep_unlinked=True)
            target=[e for e in ev if e['id']==target_id]
            if len(target)!=1:raise ValueError('missing target')
            def piece(e,eid):return {k:(eid if k=='id' else e[k]) for k in FIELDS}
            target=piece(target[0],'incoming');others=[piece(e,'item:'+e['id']) for e in ev if e['id']!=target_id]
            if target['quote'] not in text or any(e['quote'] not in text for e in others):raise ValueError('source quote not found')
            objects=[o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
            with research_context.Reader(str(WEEK/'views.sqlite'),seq,objects,uni) as reader:
                catalog=reader.catalog();expanded=reader.expand([q['view_id'] for q in catalog['questions']])
            if catalog['questions'] or expanded['evidence']:raise ValueError('cold-start history changed')
            source=dict(target,publisher=item['publisher'],publisher_type=item['publisher_type'],publication_day=item['publication_day'],category=item['category'],title=item['title'])
            baseline={'source_record':source,'source_article':text,'other_source_records':others,
                      'questions_to_consider':[],'stored_pieces':[],'catalog':[],'comparison_opinion':None}
            scope=copy.deepcopy(baseline);scope['research_scope']={'covered_companies':covered}
            for arm,payload in [('control',baseline),('scope',scope)]:
                key=name+'-'+arm;result[key]={'input_id':ident,'target_local_id':target_id,'sequence':seq,'split':split,
                    'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'extraction_call_id':call,
                    'question_ids':[],'old_ids':[],'item_ids':[e['id'] for e in others],'payload':payload}
            check=copy.deepcopy(scope);assert check.pop('research_scope')=={'covered_companies':covered} and check==baseline
            assert 'incoming' not in [e['id'] for e in others] and len({e['id'] for e in others})==len(others)
    return result


def prepare():
    cases=build();RUN.mkdir(exist_ok=False);manifest={'design_sha256':digest(DESIGN),'script_sha256':digest(Path(__file__)),
      'samples_per_model_case':3,'planned_calls':36,'cap_usd':.60,'cases':{}}
    for name,case in cases.items():
        a,b=prior.requests(case)
        for provider,req in [('luna',a),('haiku',b)]:put(name+'-'+provider+'-request.json',req)
        manifest['cases'][name]={k:v for k,v in case.items() if k!='payload'}
        manifest['cases'][name]['request_hashes']={p:digest(RUN/(name+'-'+p+'-request.json')) for p in ('luna','haiku')}
    put('manifest.json',manifest);print('prepared 6 case/group pairs and 12 requests; no model call')


def check_manifest(manifest,cases):
    allowed={'design_sha256','script_sha256','samples_per_model_case','planned_calls','cap_usd','cases'}
    if set(manifest)!=allowed or manifest['samples_per_model_case']!=3 or manifest['planned_calls']!=36 or manifest['cap_usd']!=.60:raise ValueError('plan changed')
    expected={n+'-'+a for n,*_ in CASES for a in ('control','scope')}
    if not cases or set(cases)!=expected or set(manifest['cases'])!=expected:raise ValueError('case population changed')
    for name,case in cases.items():
        x=manifest['cases'][name]
        if set(x.get('request_hashes',{}))!={'luna','haiku'} or {k:v for k,v in x.items() if k!='request_hashes'}!={k:v for k,v in case.items() if k!='payload'}:raise ValueError('case metadata changed')


def verify():
    manifest=json.loads((RUN/'manifest.json').read_text());cases=build()
    if manifest['design_sha256']!=digest(DESIGN) or manifest['script_sha256']!=digest(Path(__file__)):raise ValueError('design or preparation code changed')
    check_manifest(manifest,cases)
    mutants=[]
    m=copy.deepcopy(manifest);m['planned_calls']=99;mutants.append(m)
    m=copy.deepcopy(manifest);m['cap_usd']=999;mutants.append(m)
    m=copy.deepcopy(manifest);del m['cases']['nn-control'];mutants.append(m)
    m=copy.deepcopy(manifest);m['cases']['extra']={};mutants.append(m)
    for m in mutants:
        try:check_manifest(m,cases)
        except ValueError:continue
        raise ValueError('manifest mutant accepted')
    for name,case in cases.items():
        a,b=prior.requests(case)
        for provider,expected in [('luna',a),('haiku',b)]:
            path=RUN/(name+'-'+provider+'-request.json')
            if digest(path)!=manifest['cases'][name]['request_hashes'][provider] or prior.model.request_identity(json.loads(path.read_text()))!=prior.model.request_identity(expected):raise ValueError('request changed')
        print(name,case['split'],'sequence',case['sequence'],'siblings',len(case['item_ids']))
    for name,*_ in CASES:
        control=cases[name+'-control']['payload'];treatment=copy.deepcopy(cases[name+'-scope']['payload'])
        if treatment.pop('research_scope',None)!={'covered_companies':[{'kind':'ticker','value':'NVDA'}]} or treatment!=control:raise ValueError('more than one input changed')
    for provider in ('luna','haiku'):
        previous=json.loads((OLD/('cooling-'+provider+'-request.json')).read_text())
        if prior.model.request_identity(previous)!=prior.model.request_identity(prior.requests(cases['nn-control'])[0 if provider=='luna' else 1]):raise ValueError('NN control differs from the original experiment')
    print('six rebuilt cases, historical source, sole scope field, NN production-like control and manifest mutants verified')
    return manifest,cases


if __name__=='__main__':{'prepare':prepare,'verify':verify}[sys.argv[1]]()
