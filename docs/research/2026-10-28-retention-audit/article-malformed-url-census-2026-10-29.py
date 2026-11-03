"""Reconstruct current page-index mapping and count malformed original fetch URLs."""
import collections
import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

HERE=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-retention-audit');CORPUS=Path('/Users/lchingen/hivemind/poc/corpus');DATA=Path('/Users/lchingen/hivemind/poc/data');OUT=HERE/'article-malformed-url-census-2026-10-29.json'
sys.path.insert(0,str(CORPUS/'scripts'));import common
mapping={}
with (CORPUS/'raw/pages/index.jsonl').open(encoding='utf-8') as file:
 for line in file:
  try:record=json.loads(line)
  except json.JSONDecodeError:continue
  if record.get('file') and record.get('url'):
   mapping[record['url']]=record;mapping[common.clean_resolved_url(record['url'].strip())]=record
if common.clean_resolved_url('https://example.org/a",1]')!='https://example.org/a':raise ValueError('known URL control failed')
counts=collections.Counter();rows=[]
with sqlite3.connect(f'file:{DATA}/items-nvda-2026-07-01-10-27.sqlite?mode=ro',uri=True) as items,sqlite3.connect(f'file:{DATA}/english-v38-nvda-1w-2026-10-28/views.sqlite?mode=ro',uri=True) as views:
 ids=[ident for _,ident in views.execute('select seq,input_id from handovers order by seq')]
 if len(ids)!=98 or len(set(ids))!=98:raise ValueError('week population differs')
 for ident in ids:
  uri,fmt,title=items.execute('select source_uri,document_format,title from items where input_id=?',(ident,)).fetchone()
  if fmt!='article':counts['non_article']+=1;continue
  counts['articles']+=1;r=mapping.get(uri) or mapping.get(common.clean_resolved_url(uri))
  if r is None:counts['not_indexed']+=1;continue
  counts['indexed']+=1
  if '"' not in r['url']:continue
  counts['malformed_fetch_url']+=1
  rows.append({'input_id':ident,'source_uri':uri,'input_title':title,'record_url':r['url'],'final_url':r.get('final_url'),
               'page_title':r.get('page_title'),'coverage':r.get('coverage'),'fetched_at':r.get('fetched_at'),'html_file':r.get('file')})
known={'nvblog:nvidia-unlocks-ai-compute-at-scale-capital-partners-to-power-ai-infrastructure-buildout',
       'nvblog:geforce-now-thursday-july-2026-games-list','nvblog:nations-deploy-ai-strategic-priorities'}
for ident in known:
 r=next((x for x in rows if x['input_id']==ident),None)
 if not r or r['page_title']!='11 Essential Explainers to Keep You in the Know in 2023 | NVIDIA Blog' or r['coverage']!='full':raise ValueError('known NVIDIA mismatch missing')
invalid=next((x for x in rows if x['input_id']=='gnews:cfa20b22ec2a161c6fd85d8e'),None)
if not invalid or invalid['page_title']!='Asia - Pacific - Anadolu' or invalid['coverage']!='full':raise ValueError('known list page missing')
if counts['articles']!=97 or counts['indexed']!=96 or counts['malformed_fetch_url']!=8:raise ValueError('census differs')
out={'scope':'Current index mapping for 98 v38 inputs. A quote in the stored fetch URL identifies malformed syntax, not by itself an incorrect final article; page identity requires separate review.', 'counts':dict(counts),'malformed_records':rows}
if OUT.exists():
 if json.loads(OUT.read_text())!=out:raise ValueError('saved output differs')
else:
 with OUT.open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(dict(counts),ensure_ascii=False));print('four known wrong-page records detected, four other malformed records require identity judgment')
