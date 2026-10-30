"""Prepare and verify an isolated fourth-step Haiku/Luna comparison; no sending on import."""
import copy
import hashlib
import importlib.util
import json
import re
import sqlite3
import sys
from pathlib import Path

from hivemind import config, extraction, model, research_context, universe

ROOT = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
HERE = ROOT/'docs/research/2026-10-28-retention-audit'
DATA = Path('/Users/lchingen/hivemind/poc/data')
WEEK = DATA/'english-v38-nvda-1w-2026-10-28'
RUN = HERE/'stage4-haiku-luna-v3-2026-10-29'
DESIGN = HERE/'stage4-user-baseline-design-v4-2026-10-29.md'
REFERENCE = HERE/'stage4-holdout-reference-v2-2026-10-29.md'
CASES = [('sharon','gnews:3854aeddaa3f31de00cf2816','e6','development'),
         ('product_progress','gnews:795ea94e1100415a67fd1a96','e3','development'),
         ('singapore','gnews:1eeceeb212a2c82c2e75e806','e8','development'),
         ('cooling','gnews:9a13ec8bfdc32e585c1f0604','e1','holdout'),
         ('games','nvblog:geforce-now-thursday-july-2026-games-list','e1','holdout')]
spec=importlib.util.spec_from_file_location('stage34',ROOT/'docs/research/2026-10-27-stage34-gold/run.py')
stage34=importlib.util.module_from_spec(spec);spec.loader.exec_module(stage34)
FIELDS=('id','quote','one_line','speaker','original_who','original_day','tier','event_time')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(name,obj):
    with (RUN/name).open('x',encoding='utf-8') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')


def source_cases():
    contexts = json.loads((HERE/'stage4-user-case-context-2026-10-29.json').read_text())['cases']
    contexts += json.loads((HERE/'stage4-holdout-context-2026-10-29.json').read_text())['cases']
    by_id = {r['input_id']:r for r in contexts}
    if len(by_id)!=5:
        raise ValueError('case population must be five distinct inputs')
    cfg=config.load(str(ROOT/'poc/config/poc-v38.json')); uni=universe.load(str(ROOT/'poc/universe.json'))
    out={}
    with sqlite3.connect(f'file:{DATA}/items-nvda-2026-07-01-10-27.sqlite?mode=ro',uri=True) as items, \
         sqlite3.connect(f'file:{WEEK}/archive.sqlite?mode=ro',uri=True) as archive:
        items.row_factory=sqlite3.Row
        calls=list(archive.execute("select call_id,request_json,answer_json from model_calls where purpose='extract' and answer_json is not null and request_sha256 not like '%:%'"))
        for name, input_id, target_id, split in CASES:
            ctx=by_id[input_id]; item=dict(items.execute('select * from items where input_id=?',(input_id,)).fetchone())
            item['object_identifiers']=json.loads(item['object_identifiers']);text=item['text']
            assert hashlib.sha256(text.encode()).hexdigest()==ctx['source_sha256']
            matching=[]
            for call_id, encoded, answer in calls:
                req=json.loads(encoded); user=next(m['content'] for m in req['messages'] if m['role']=='user')
                m=re.search(r'\[Item\] id (\S+?), category ',user)
                if m and m.group(1)==input_id:matching.append((call_id,req,json.loads(answer)))
            if len(matching)!=1:raise ValueError('missing or ambiguous archived extraction')
            call_id,req,answer=matching[0]
            setting,system,user,schema=extraction.request_for(cfg,item,text,[],uni,[])
            built=model.build_request(setting,system,user,schema,'extraction',cfg.provider)
            assert model.request_identity(built)[1]==model.request_identity(req)[1] and not model.check_schema(answer,schema)
            evidence,_,_,_=extraction.sift_with_groups(answer,item,text,set(),uni,english=True,shown_group_ids=(),version='v22',keep_unlinked=True)
            targets=[e for e in evidence if e['id']==target_id]
            if len(targets)!=1:raise ValueError('target absent after production check')
            def piece(e,ident):
                return {k:(ident if k=='id' else e[k]) for k in FIELDS}
            target=piece(targets[0],'incoming')
            others=[piece(e,'item:'+e['id']) for e in evidence if e['id']!=target_id]
            expansion=ctx['full_historical_expansion'];seq=ctx['sequence']
            assert expansion['before_seq']==seq and all(e['created_seq']<seq for e in expansion['evidence'])
            objects=[o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
            with research_context.Reader(str(WEEK/'views.sqlite'),seq,objects,uni) as reader:
                independently_rebuilt_catalog=reader.catalog()
                rebuilt=reader.expand([q['view_id'] for q in independently_rebuilt_catalog['questions']])
            if independently_rebuilt_catalog != ctx['historical_catalog'] or rebuilt != expansion:
                raise ValueError('historical snapshot differs from ledger')
            qids=[q['view_id'] for q in expansion['questions']]; old_ids=[e['evidence_id'] for e in expansion['evidence']]
            sibling_ids=[e['id'] for e in others]
            if len(set(old_ids))!=len(old_ids) or len(set(sibling_ids))!=len(sibling_ids) or set(old_ids)&(set(sibling_ids)|{'incoming'}):
                raise ValueError('ambiguous evidence identities')
            questions=[]
            for q in expansion['questions']:
                latest=q.get('latest_judgement')
                questions.append({'view_id':q['view_id'],'looks_at':q['looks_at'],'question':q['question'],'due_day':q['due_day'],
                    'rungs':[{'label':r.get('label'),'condition':r.get('condition')} for r in q.get('rungs',[])],
                    'latest_judgement':({'rung':latest['rung'],'reasons':latest['reasons'],'day':latest['publication_day']} if latest else None),
                    'argument':None,'piece_ids':q['evidence_ids']})
            old=[]
            for p in expansion['evidence']:
                old.append({'id':p['evidence_id'],'tier':p['tier'],'speaker':p['speaker'],'original_who':p['original_who'],
                    'original_day':p['original_day'],'event_time':p['event_time'],'one_line':p['one_line'],'quote':p['quote'],
                    'sources':[[s['input_id'],s['publication_day']] for s in p['sources']],
                    'replaced':p.get('replaced',[])})
            source=dict(target,publisher=item['publisher'],publisher_type=item['publisher_type'],publication_day=item['publication_day'],category=item['category'],title=item['title'])
            payload={'source_record':source,'source_article':text,'other_source_records':others,'questions_to_consider':questions,
                     'stored_pieces':old,'catalog':[{'view_id':q['view_id'],'looks_at':q['looks_at']} for q in expansion['questions']],
                     'comparison_opinion':None}
            assert target['quote'] in text and all(e['quote'] in text for e in others)
            out[name]={'split':split,'input_id':input_id,'sequence':seq,'target_local_id':target_id,'source_sha256':ctx['source_sha256'],
                       'extraction_call_id':call_id,'original_request_sha256':model.request_identity(req)[1],
                       'question_ids':qids,'old_ids':old_ids,'item_ids':sibling_ids,'payload':payload}
    return out


def requests(case):
    user=json.dumps(case['payload'],ensure_ascii=False)
    messages=[{'role':'system','content':stage34.SYSTEM},{'role':'user','content':user}]
    gpt={'model':'gpt-6-luna','messages':messages,'response_format':{'type':'json_schema','json_schema':{'name':'research_update','strict':True,'schema':stage34.SCHEMA}},
         'max_completion_tokens':6000,'reasoning_effort':'medium'}
    haiku={'model':'claude-haiku-5-5','max_tokens':6000,'system':stage34.SYSTEM,'messages':[messages[1]],
           'output_config':{'effort':'medium','format':{'type':'json_schema','schema':stage34.SCHEMA}}}
    assert messages==[{'role':'system','content':haiku['system']},*haiku['messages']]
    assert gpt['response_format']['json_schema']['schema']==haiku['output_config']['format']['schema']
    return gpt,haiku


def answer_checks(answer, case):
    """Check identity and shape only; do not infer investment or source independence."""
    errors=model.check_schema(answer,stage34.SCHEMA)
    if errors:
        return errors, []
    old=set(case['old_ids']); siblings=set(case['item_ids']); questions=set(case['question_ids'])
    observations=[]
    relations=('same_claim_as','revises','opposes')
    seen=set()
    for field in relations:
        for ident in answer[field]:
            if ident not in old:
                errors.append(field+': not a historical evidence id '+ident)
            if ident in seen:
                errors.append('same id in multiple relations '+ident)
            seen.add(ident)
    for ident in answer['question_ids']:
        if ident not in questions:
            errors.append('unknown question '+ident)
    if answer['action']=='update_existing' and not answer['question_ids']:
        errors.append('update_existing without question')
    if answer['action']=='propose_new' and not (answer['new_question'].strip() and answer['independent_judgement'].strip()):
        errors.append('propose_new without independent judgement')
    for arg in answer['arguments']:
        if arg['question_id'] not in questions:
            errors.append('argument references unknown question '+arg['question_id'])
        for ident in arg['support_ids']+arg['opposing_ids']:
            if ident in siblings:
                observations.append('same-article reference requires product resolution '+ident)
            elif ident not in old and ident!='incoming':
                errors.append('argument references unknown evidence '+ident)
    return errors,observations


def exercise_answer_checks(cases):
    case=next(c for c in cases.values() if c['question_ids'] and c['old_ids'] and c['item_ids'])
    q=case['question_ids'][0];old=case['old_ids'][0];sibling=case['item_ids'][0]
    base={'action':'update_existing','question_ids':[q],'same_claim_as':[],'revises':[],'opposes':[],
          'independent_sources':False,'original_source':'source','new_information':'statement',
          'arguments':[{'question_id':q,'statement':'current view','support_ids':['incoming',old,sibling],
                        'opposing_ids':[],'limitations':[],'what_would_change_it':[]}],
          'new_question':'','independent_judgement':'','reason':'reason'}
    errors,notes=answer_checks(base,case)
    assert not errors and len(notes)==1 and sibling in notes[0]
    mutants=[]
    m=copy.deepcopy(base);m['same_claim_as']=[sibling];mutants.append(m)
    m=copy.deepcopy(base);m['arguments'][0]['support_ids'].append('e999999');mutants.append(m)
    m=copy.deepcopy(base);m['question_ids']=['v999999'];mutants.append(m)
    m=copy.deepcopy(base);m['revises']=[old];m['opposes']=[old];mutants.append(m)
    m=copy.deepcopy(base);del m['reason'];mutants.append(m)
    assert all(answer_checks(m,case)[0] for m in mutants)
    print('answer shape/id positive control and five negative controls exercised')


def prepare():
    cases=source_cases();RUN.mkdir(exist_ok=False);manifest={'design_sha256':digest(DESIGN),'reference_sha256':digest(REFERENCE),'script_sha256':digest(Path(__file__)),
        'samples_per_model_case':3,'planned_calls':30,'cap_usd':.60,'cases':{}}
    for name,case in cases.items():
        gpt,haiku=requests(case)
        for provider,req in [('luna',gpt),('haiku',haiku)]:put(name+'-'+provider+'-request.json',req)
        manifest['cases'][name]={k:v for k,v in case.items() if k!='payload'}
        manifest['cases'][name]['request_hashes']={p:digest(RUN/(name+'-'+p+'-request.json')) for p in ('luna','haiku')}
    put('manifest.json',manifest)
    print('prepared five paired requests, three samples per model; no network call')


def check_manifest(manifest, cases):
    expected_fields={'design_sha256','reference_sha256','script_sha256','samples_per_model_case','planned_calls','cap_usd','cases'}
    if set(manifest)!=expected_fields or manifest['samples_per_model_case']!=3 or manifest['planned_calls']!=30 or manifest['cap_usd']!=.60:
        raise ValueError('experiment schedule, cap or manifest fields changed')
    if not cases or set(manifest['cases'])!=set(cases) or set(cases)!={c[0] for c in CASES}:
        raise ValueError('case population changed')
    for name, case in cases.items():
        item=manifest['cases'][name]
        if set(item.get('request_hashes',{}))!={'luna','haiku'}:
            raise ValueError('provider requests missing or added')
        if {k:v for k,v in item.items() if k!='request_hashes'}!={k:v for k,v in case.items() if k!='payload'}:
            raise ValueError('case metadata changed')


def exercise_manifest_checks(manifest,cases):
    check_manifest(manifest,cases)
    mutants=[]
    m=copy.deepcopy(manifest);m['samples_per_model_case']=99;mutants.append(m)
    m=copy.deepcopy(manifest);m['cap_usd']=999;mutants.append(m)
    m=copy.deepcopy(manifest);m['cases']['unexpected']={};mutants.append(m)
    m=copy.deepcopy(manifest);del m['cases'][next(iter(m['cases']))];mutants.append(m)
    m=copy.deepcopy(manifest);del m['cases'][next(iter(m['cases']))]['request_hashes']['luna'];mutants.append(m)
    for mutant in mutants:
        try:check_manifest(mutant,cases)
        except ValueError:continue
        raise ValueError('manifest mutant was not rejected')
    print('manifest positive control and five altered/missing-input controls exercised')


def verify():
    manifest=json.loads((RUN/'manifest.json').read_text());assert manifest['design_sha256']==digest(DESIGN) and manifest['reference_sha256']==digest(REFERENCE) and manifest['script_sha256']==digest(Path(__file__))
    cases=source_cases();exercise_manifest_checks(manifest,cases)
    exercise_answer_checks(cases)
    for name,case in cases.items():
        a,b=requests(case)
        saved={k:v for k,v in manifest['cases'][name].items() if k!='request_hashes'}
        assert saved=={k:v for k,v in case.items() if k!='payload'}
        for provider,expected in [('luna',a),('haiku',b)]:
            p=RUN/(name+'-'+provider+'-request.json')
            assert digest(p)==manifest['cases'][name]['request_hashes'][provider] and json.loads(p.read_text())==expected
        payload=case['payload']; assert payload['source_record']['id']=='incoming'
        assert not ({'status','drop_reason','final_links','final_status','stored_id','stored_links'}&set(payload['source_record']))
        assert all(x['id'].startswith('item:') for x in payload['other_source_records'])
        assert 'original_placement_answer' not in payload and 'original_placement_request' not in payload
        print(name,case['split'],'history',len(case['old_ids']),'questions',len(case['question_ids']),
              'user bytes',len(json.dumps(payload,ensure_ascii=False).encode()))
    print('verified exact paired inputs; no model sent')


if __name__=='__main__':
    {'prepare':prepare,'verify':verify}[sys.argv[1]]()
