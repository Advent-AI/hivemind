"""Compare current and corrected-URL listing policies without network or changing the corpus."""
import copy
import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

HERE=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-retention-audit');CORPUS=Path('/Users/lchingen/hivemind/poc/corpus');SOURCE=CORPUS/'scripts/fetch_bodies.py';OUT=HERE/'article-fetch-policy-proof-2026-10-29.json'
sys.path.insert(0,str(CORPUS/'scripts'));spec=importlib.util.spec_from_file_location('fetch_control',SOURCE);control=importlib.util.module_from_spec(spec);spec.loader.exec_module(control)
source=SOURCE.read_text();old='                if url != stored and stored in full_already:\n                    url = stored\n';new='                if False:\n                    url = stored\n'
if source.count(old)!=1:raise ValueError('listing decision not unique')
namespace={'__name__':'fetch_clean_experiment','__file__':str(SOURCE)};exec(compile(source.replace(old,new,1),str(SOURCE),'exec'),namespace)
before=control.listed_urls();after=namespace['listed_urls']();state=control.index_state();census=json.loads((HERE/'article-malformed-url-census-2026-10-29.json').read_text());cases=[]
for r in census['malformed_records']:
 oldurl=r['record_url'];clean=r['source_uri'];b=oldurl in before;a=clean in after
 if not b or not a:raise ValueError('named case did not flip '+r['input_id'])
 if not state.get(oldurl,(False,0))[0]:raise ValueError('old URL was not marked done '+r['input_id'])
 cases.append({'input_id':r['input_id'],'old_url':oldurl,'clean_url':clean,'old_listed':b,'clean_listed_after':a,
               'old_marked_done':True,'clean_marked_done':state.get(clean,(False,0))[0]})
oldkeys=set(before);newkeys=set(after);removed=oldkeys-newkeys;added=newkeys-oldkeys
out={'scope':'Scratch in-memory source mutation only; no fetch, write, product change, or historical reconstruction. Whole configured corpus listing is counted because the changed function is shared.',
     'input_count_before':len(before),'input_count_after':len(after),'urls_removed':len(removed),'urls_added':len(added),
     'week_cases':cases,'week_cases_with_clean_url_not_done':sum(not c['clean_marked_done'] for c in cases)}
if len(cases)!=8:raise ValueError('week control differs')
if OUT.exists():
 if json.loads(OUT.read_text())!=out:raise ValueError('saved proof differs')
else:
 with OUT.open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print('week cases flipped',len(cases),'clean not already done',out['week_cases_with_clean_url_not_done'])
print('configured corpus: listed before',len(before),'after',len(after),'removed',len(removed),'added',len(added))
