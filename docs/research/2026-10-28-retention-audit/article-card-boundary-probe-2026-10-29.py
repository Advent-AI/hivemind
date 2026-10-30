"""Exploratory HTML card-boundary signal over manually read source passages; no product change."""
import collections
import importlib.util
import json
import sqlite3
import sys
from pathlib import Path
from urllib.parse import urljoin,urlsplit
from lxml import html as lxml_html

HERE=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-retention-audit');CORPUS=Path('/Users/lchingen/hivemind/poc/corpus');DATA=Path('/Users/lchingen/hivemind/poc/data');OUT=HERE/'article-card-boundary-probe-2026-10-29.json'
sys.path.insert(0,str(CORPUS/'scripts'));spec=importlib.util.spec_from_file_location('clean_pages',CORPUS/'scripts/clean_pages.py');clean=importlib.util.module_from_spec(spec);spec.loader.exec_module(clean)
index=clean.pages_index(str(CORPUS/'raw'));references=json.loads((HERE/'article-readdition-evidence-read-2026-10-29.json').read_text())['items']
wrong_html={'nvblog:nvidia-unlocks-ai-compute-at-scale-capital-partners-to-power-ai-infrastructure-buildout','nvblog:geforce-now-thursday-july-2026-games-list','nvblog:nations-deploy-ai-strategic-priorities'}

def norm(text):return clean._letters(text or '')

def link_is_other(link,source):
 href=link.get('href') or ''
 if not href or href.startswith(('#','javascript:','mailto:')):return False
 dest=urlsplit(urljoin(source,href));home=urlsplit(source)
 return bool(dest.hostname and (dest.hostname.lower(),dest.path.rstrip('/'))!=(home.hostname.lower(),home.path.rstrip('/')))

def signal(tree,quote,source):
 key=norm(quote)[:25]
 if len(key)<15:return {'located':False,'reason':'quote too short'}
 candidates=[]
 for text in tree.xpath('//text()'):
  parent=text.getparent()
  if parent is None or any(a.tag in ('script','style','noscript') for a in [parent,*parent.iterancestors()]):continue
  if key not in norm(str(text)):continue
  candidates.append(parent)
 if not candidates:return {'located':False,'reason':'no single text node with initial quote'}
 hits=[]
 for node in candidates:
  chain=[node,*list(node.iterancestors())[:6]]
  for ancestor in chain:
   if ancestor.tag=='a' and link_is_other(ancestor,source) and len(ancestor.text_content().strip())>=60:
    hits.append({'kind':'linked_block','href':ancestor.get('href')});break
   # A short wrapper with a separate, descriptive article-headline link and a prose summary.
   if ancestor is node or ancestor.tag not in ('div','li','section','article','aside'):continue
   content=ancestor.text_content().strip()
   if len(content)>1600:continue
   for link in ancestor.xpath('.//a[@href]'):
    if not link_is_other(link,source) or len(link.text_content().strip())<25:continue
    if link is node or link in node.iterancestors() or node in link.iterancestors():continue
    hits.append({'kind':'linked_headline_near_summary','href':link.get('href')});break
   if hits:break
 return {'located':True,'signal':bool(hits),'matches':len(candidates),'examples':hits[:2]}

# Controls are artificial and exercise only page structure, not investment relevance.
base='https://example.org/main'
card=lxml_html.fromstring('<main><ul><li><a href="/other">An unrelated article headline that is clearly descriptive</a><p>The recommended article contains a long example sentence for the structural boundary check.</p></li></ul></main>')
body=lxml_html.fromstring('<main><p>The main article contains a long example sentence for the structural boundary check. <a href="/source">Read the underlying company report</a></p></main>')
if not signal(card,'The recommended article contains a long example sentence for the structural boundary check.',base).get('signal'):
 raise ValueError('related card positive control failed')
if signal(body,'The main article contains a long example sentence for the structural boundary check.',base).get('signal'):
 raise ValueError('main article linked-source negative control failed')

counts=collections.Counter();rows=[];cache={}
with sqlite3.connect(f'file:{DATA}/items-nvda-2026-07-01-10-27.sqlite?mode=ro',uri=True) as db:
 db.row_factory=sqlite3.Row
 for r in references:
  ident=r['input_id']
  if ident in wrong_html:counts['excluded_wrong_html']+=1;continue
  if ident not in cache:
   item=dict(db.execute('select * from items where input_id=?',(ident,)).fetchone());raw=clean.html_of(item,index)
   if not raw:raise ValueError('HTML missing '+ident)
   cache[ident]=(item,lxml_html.fromstring(raw))
  item,tree=cache[ident];answer=signal(tree,r['quote'],item['source_uri']);label=r['label'];counts[(label,'total')]+=1
  if answer.get('located'):counts[(label,'located')]+=1
  if answer.get('signal'):counts[(label,'signal')]+=1
  rows.append({'input_id':ident,'local_id':r['local_id'],'reference_label':label,'quote':r['quote'],'result':answer})
if len(rows)!=40 or counts['excluded_wrong_html']!=16:raise ValueError('frozen annotated population changed')
out={'scope':'Exploratory card-link signal on 40 already-inspected records; no independent held-out evaluation, no economic relevance judgment, no product modification.',
     'counts':{str(k):v for k,v in counts.items()},'records':rows}
if OUT.exists():
 if json.loads(OUT.read_text())!=out:raise ValueError('saved probe differs')
else:
 with OUT.open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(out['counts'])
for r in rows:
 if (r['reference_label']=='other_article_on_page' and not r['result'].get('signal')) or (r['reference_label']=='same_article_or_topic_summary' and r['result'].get('signal')):print('MISS/FP',r['input_id'],r['local_id'],r['reference_label'],r['result'])
