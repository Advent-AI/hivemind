"""Attach 33 candidate facts to real historical questions without endorsing candidate labels."""
import collections
import json
import re
import sqlite3
from pathlib import Path
HERE = Path(__file__).resolve().parent
ARCH = '/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/archive.sqlite'

def load(name): return json.loads((HERE / name).read_text())

def main():
    reference = load('source-reference.json'); ledger=load('ledger.json')['v38']
    homes=load('prestart-expected-homes-2026-10-28.json')['homes']
    conn=sqlite3.connect('file:'+ARCH+'?mode=ro',uri=True)
    calls=[]
    for call_id,raw in conn.execute("select call_id,request_json from model_calls where purpose='place' and request_sha256 not like '%:%'"):
        user=json.loads(raw)['messages'][1]['content']; calls.append((call_id,user))
    rows=[]
    for source_article in reference['articles']:
        article=ledger[source_article['article_no']-1]
        assert article['input_id']==source_article['input_id']
        matching=[(i,u) for i,u in calls if u.split('\n',1)[0].endswith(': '+article['title'])]
        assert len(matching)==1
        call_id,user=matching[0]; section=user.split('\n\n[Statements]\n',1)[0]
        blocks=re.findall(r'^  - (v\d+) \([^\n]*\n      [^\n]*',section,re.M)
        full=re.findall(r'^  - v\d+ \([^\n]*\n      [^\n]*',section,re.M)
        questions=dict(zip(blocks,full)); assert len(questions)==len(blocks)
        for claim in source_article['claims']:
            assert claim['source_text'] in article['source']
            candidate=homes[claim['id']]; visible={k:questions[k] for k in candidate if k in questions}
            rows.append({'id':claim['id'],'article_no':article['article_no'],'input_id':article['input_id'],
                         'day':article['day'],'source_text':claim['source_text'],'meaning':claim['meaning'],
                         'old_candidate_core':claim['core'],'candidate_homes':candidate,
                         'historically_shown_candidate_homes':visible,'placement_call_id':call_id,
                         'status':'pending analyst review; candidate homes and source importance not established'})
    assert len(rows)==33 and len({r['id'] for r in rows})==33
    counts=collections.Counter(bool(r['historically_shown_candidate_homes']) for r in rows)
    out={'scope':'33 provisional reference facts; historical question text, no semantic correctness judgment',
         'facts':len(rows),'shown_provisional_home':counts[True],'no_shown_provisional_home':counts[False],
         'warning':'Post-result material for development and review, not an unseen test or accepted gold.', 'rows':rows}
    with (HERE/'reference-evidence-map-2026-10-28.json').open('x') as f:
        json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
    print({k:v for k,v in out.items() if k!='rows'})

if __name__=='__main__':main()
