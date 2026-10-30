"""Compare source URLs with canonical URLs in the HTML currently mapped to week inputs."""
import collections
import importlib.util
import json
import sqlite3
import sys
from pathlib import Path
from urllib.parse import urlsplit
from lxml import html as lxml_html

HERE=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-retention-audit')
OLD=Path('/Users/lchingen/hivemind/poc/corpus');DATA=Path('/Users/lchingen/hivemind/poc/data');OUT=HERE/'article-html-identity-census-2026-10-29.json'
sys.path.insert(0,str(OLD/'scripts'));spec=importlib.util.spec_from_file_location('clean_pages',OLD/'scripts/clean_pages.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);index=m.pages_index(str(OLD/'raw'))
def canonical_key(url):
 p=urlsplit(url);host=(p.hostname or '').lower().removeprefix('www.');return (host,p.path.rstrip('/') or '/')
if canonical_key('https://www.example.com/a/?x=1')!=canonical_key('http://example.com/a'):raise ValueError('URL control failed')
if canonical_key('https://example.com/a')==canonical_key('https://example.com/b'):raise ValueError('wrong-page URL control failed')
rows=[];counts=collections.Counter()
with sqlite3.connect(f'file:{DATA}/items-nvda-2026-07-01-10-27.sqlite?mode=ro',uri=True) as items,sqlite3.connect(f'file:{DATA}/english-v38-nvda-1w-2026-10-28/views.sqlite?mode=ro',uri=True) as views:
 items.row_factory=sqlite3.Row;ids=[ident for _,ident in views.execute('select seq,input_id from handovers order by seq')]
 if len(ids)!=98 or len(set(ids))!=98:raise ValueError('week population changed')
 for ident in ids:
  row=dict(items.execute('select * from items where input_id=?',(ident,)).fetchone());counts['inputs']+=1
  if row['document_format']!='article':counts['non_article']+=1;continue
  raw=m.html_of(row,index)
  if not raw:counts['html_missing']+=1;continue
  try:tree=lxml_html.fromstring(raw)
  except (ValueError,TypeError):counts['html_parse_error']+=1;continue
  declared=tree.xpath('//link[contains(concat(" ",normalize-space(@rel)," ")," canonical ")]/@href') or tree.xpath('//meta[@property="og:url"]/@content')
  title=tree.xpath('string(//title)').strip();href=declared[0] if declared else ''
  if not href or not urlsplit(href).hostname:kind='no_absolute_canonical'
  elif canonical_key(href)==canonical_key(row['source_uri']):kind='canonical_matches_source'
  else:kind='canonical_differs_review_needed'
  counts[kind]+=1
  rows.append({'input_id':ident,'input_title':row['title'],'source_uri':row['source_uri'],'html_title':title,'html_canonical':href,'status':kind})
if counts['inputs']!=98 or not counts['canonical_differs_review_needed'] or not counts['canonical_matches_source']:
 raise ValueError('population/control not exercised')
known=next(r for r in rows if r['input_id']=='nvblog:geforce-now-thursday-july-2026-games-list')
if known['status']!='canonical_differs_review_needed' or '11 Essential Explainers' not in known['html_title']:
 raise ValueError('known wrong HTML control failed')
out={'scope':'URL identity triage on current saved HTML only. Differences may be legitimate redirects; neither exact URL nor title alone establishes historical HTML identity.', 'counts':dict(counts),'cases':rows}
if OUT.exists():
 if json.loads(OUT.read_text())!=out:raise ValueError('saved output differs')
else:
 with OUT.open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(dict(counts),ensure_ascii=False))
for r in rows:
 if r['status']=='canonical_differs_review_needed':print(r['input_id'],'|',r['input_title'][:70],'|',r['html_title'][:70])
