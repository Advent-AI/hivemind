"""Count existing cleaned article lines re-added outside the structural HTML extractor."""
import collections
import hashlib
import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

HERE=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-retention-audit')
OLD=Path('/Users/lchingen/hivemind/poc/corpus')
DATA=Path('/Users/lchingen/hivemind/poc/data')
ITEMS=DATA/'items-nvda-2026-07-01-10-27.sqlite'
VIEWS=DATA/'english-v38-nvda-1w-2026-10-28/views.sqlite'
OUT=HERE/'article-readdition-census-2026-10-29.json'
sys.path.insert(0,str(OLD/'scripts'))
spec=importlib.util.spec_from_file_location('clean_pages',OLD/'scripts/clean_pages.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
idx=m.pages_index(str(OLD/'raw')); counts=collections.Counter(); rows=[]
with sqlite3.connect(f'file:{ITEMS}?mode=ro',uri=True) as items,sqlite3.connect(f'file:{VIEWS}?mode=ro',uri=True) as views:
    items.row_factory=sqlite3.Row
    ids=[ident for _,ident in views.execute('select seq,input_id from handovers order by seq')]
    if len(ids)!=98 or len(set(ids))!=98:raise ValueError('week input population differs')
    for ident in ids:
        row=dict(items.execute('select * from items where input_id=?',(ident,)).fetchone()); counts['inputs']+=1
        if row['document_format']!='article':counts['non_article']+=1;continue
        counts['article_inputs']+=1
        html=m.html_of(row,idx)
        if not html:counts['article_html_missing']+=1;continue
        extracted=m.extract_article(html)
        if not extracted.strip():counts['article_extractor_empty']+=1;continue
        counts['article_html_extracted']+=1
        joined=m._letters(extracted);short={m._letters(line) for line in extracted.split('\n')}
        added=[];unclassified=[]
        for line in m.lines_of(row['text']):
            key=m._letters(line);in_extract=(key[:120] in joined if len(key)>=20 else key in short)
            if in_extract or m.is_byline(line):continue
            if len(line)>=m.RE_ADD_LINE and m.END_PUNCTUATION.search(line):added.append(line)
            else:unclassified.append(line)
        counts['readded_lines']+=len(added);counts['unclassified_lines']+=len(unclassified)
        if added:counts['pages_with_readded_lines']+=1
        rows.append({'input_id':ident,'title':row['title'],'readded_count':len(added),'unclassified_count':len(unclassified),
                     'cleaned_sha256':hashlib.sha256((row['text'] or '').encode()).hexdigest(),
                     'readded_lines':added,'unclassified_lines':unclassified})
science=next((r for r in rows if r['input_id']=='gnews:8f5a03f1dde395491fc3814b'),None)
if not science or science['readded_count']<4:raise ValueError('known real-page control not found')
if sum('Microsoft has unveiled Frontier Company' in line for line in science['readded_lines'])!=1:raise ValueError('known teaser control not found')
if not counts['article_html_extracted'] or not counts['readded_lines']:raise ValueError('population unexercised')
out={'scope':'98 inputs in the v38 week; structural long-line fallback only, not a semantic junk count. Saved HTML extracted with installed trafilatura; results can depend on extractor version.',
     'counts':dict(counts),'cases':rows}
if OUT.exists():
    if json.loads(OUT.read_text())!=out:raise ValueError('saved census differs; do not overwrite')
else:
    with OUT.open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(dict(counts),ensure_ascii=False));print('known page fallback lines',science['readded_count'])
