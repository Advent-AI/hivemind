"""Trace extraction evidence quoted only from structurally re-added source lines."""
import collections
import importlib.util
import json
import re
import sqlite3
import sys
from pathlib import Path
from hivemind import config,extraction,universe

ROOT=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
HERE=ROOT/'docs/research/2026-10-28-retention-audit'
OLD=Path('/Users/lchingen/hivemind/poc/corpus')
DATA=Path('/Users/lchingen/hivemind/poc/data')
OUT=HERE/'article-readdition-evidence-2026-10-29.json'
sys.path.insert(0,str(OLD/'scripts'))
spec=importlib.util.spec_from_file_location('clean_pages',OLD/'scripts/clean_pages.py');clean=importlib.util.module_from_spec(spec);spec.loader.exec_module(clean)
spec=importlib.util.spec_from_file_location('preflight',ROOT/'scripts/preflight.py');pre=importlib.util.module_from_spec(spec);spec.loader.exec_module(pre)
census=json.loads((HERE/'article-readdition-census-2026-10-29.json').read_text());by_id={r['input_id']:r for r in census['cases']};index=clean.pages_index(str(OLD/'raw'));uni=universe.load(str(ROOT/'poc/universe.json'));counts=collections.Counter();flagged=[]
with sqlite3.connect(f'file:{DATA}/items-nvda-2026-07-01-10-27.sqlite?mode=ro',uri=True) as items,sqlite3.connect(f'file:{DATA}/english-v38-nvda-1w-2026-10-28/archive.sqlite?mode=ro',uri=True) as archive,sqlite3.connect(f'file:{DATA}/english-v38-nvda-1w-2026-10-28/views.sqlite?mode=ro',uri=True) as views:
 items.row_factory=sqlite3.Row
 calls=list(archive.execute("select config_version,config_checksum,request_sha256,request_json,answer_json from model_calls where purpose='extract' and request_sha256 not like '%:%'"))
 if len(calls)!=98:raise ValueError('week archive population changed')
 known=set()
 for version,checksum,sha,encoded,answer in calls:
  request=json.loads(encoded);user=next(x['content'] for x in request['messages'] if x['role']=='user');match=pre.ITEM_ID.search(user)
  if not match:raise ValueError('input id missing')
  ident=match.group(1) or match.group(2)
  if ident in known:raise ValueError('duplicate input')
  known.add(ident);item=dict(items.execute('select * from items where input_id=?',(ident,)).fetchone());cfg=config.load(str(ROOT/'poc/config'/f'{version}.json'))
  if cfg.checksum!=checksum:raise ValueError('configuration differs')
  category,shown,groups=pre._preflight_extract_inputs(request,item,cfg)
  data=json.loads(answer);flat=extraction.flatten_account(data)
  accepted,_,_,_=extraction.sift_with_groups(data,item,item['text'] or '',set(shown),uni,english=extraction.is_english(category),shown_group_ids=groups,version=category,keep_unlinked=extraction.places(category))
  counts['all_raw_evidence']+=len(flat['evidence']);counts['all_accepted_evidence']+=len(accepted)
  if ident not in by_id:counts['items_without_extractor_replay']+=1;continue
  html=clean.html_of(item,index);extracted=clean.extract_article(html);corpus=extraction.normalise(extracted);lines=by_id[ident]['readded_lines'];accepted_ids={e['id'] for e in accepted}
  for e in flat['evidence']:
   q=extraction.normalise(e['quote']);hits=[line for line in lines if q and q in extraction.normalise(line)]
   if not hits or q in corpus:continue
   matches=[]
   for eid,stored_quote in views.execute('select es.evidence_id,e.quote from evidence_sources es join evidence e on e.evidence_id=es.evidence_id where es.input_id=?',(ident,)):
    if extraction.normalise(stored_quote)==q:matches.append(eid)
   counts['raw_evidence_only_readded']+=1;counts['accepted_only_readded']+=e['id'] in accepted_ids;counts['exact_quote_written_evidence']+=bool(matches)
   flagged.append({'input_id':ident,'local_id':e['id'],'quote':e['quote'],'one_line':e['one_line'],'accepted':e['id'] in accepted_ids,'same_quote_written_ids':matches,'supporting_readded_line':hits[0]})
if counts['all_raw_evidence']!=841 or counts['all_accepted_evidence']!=831:raise ValueError('preflight control mismatch: '+str(counts))
if not any(r['input_id']=='gnews:8f5a03f1dde395491fc3814b' and r['local_id']=='e6' for r in flagged):raise ValueError('known teaser evidence missing')
if not flagged:raise ValueError('unexercised population')
out={'scope':'Only evidence quotes entirely contained in a structurally re-added line and absent from the extractor output. Not a semantic junk count; may miss cross-line or differently worded source links. Matching ledger records requires same input and normalised exact quote.', 'counts':dict(counts),'flagged':flagged}
if OUT.exists():
 if json.loads(OUT.read_text())!=out:raise ValueError('saved evidence census differs')
else:
 with OUT.open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(dict(counts),ensure_ascii=False))
