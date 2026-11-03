"""Compare the v38 historical context reader against independent table snapshots."""
import json
from pathlib import Path
import sqlite3
import sys

ROOT=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28')
sys.path.insert(0,str(ROOT/'src'))
from hivemind import research_context,universe

LEDGER='/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/views.sqlite'
OUT=ROOT/'docs/research/2026-10-28-retention-audit/step2-v38-census-2026-10-29.json'


def main():
 c=sqlite3.connect(f'file:{LEDGER}?mode=ro',uri=True);c.row_factory=sqlite3.Row
 rows=lambda table:[dict(x) for x in c.execute('select * from '+table)]
 views=rows('views');switches=rows('view_switches');evidence=rows('evidence');links=rows('evidence_links')
 replacements=rows('replacements');deps=rows('dependencies');handovers=rows('handovers')
 assert len(handovers)==98 and not deps and not replacements
 uni=universe.load(str(ROOT/'poc/universe.json'));scope=set(uni.themes)|{'NVDA'};by_id={e['evidence_id']:e for e in evidence}
 seqs=sorted({r['seq'] for r in handovers});assert len(seqs)==98
 questions=evidence_links=0;bad=[];positive_control=False;max_questions=max_evidence=0
 for seq in seqs:
  expected=set()
  for view in views:
   known=[s for s in switches if s['view_id']==view['view_id'] and s['after_seq']<seq]
   if view['object_id'] in scope and view['created_seq']<seq and known and max(known,key=lambda x:(x['after_seq'],x['id']))['open']:
    expected.add(view['view_id'])
  with research_context.Reader(LEDGER,seq,['NVDA'],uni) as reader:
   cat=reader.catalog();out=reader.expand(sorted(expected));got={v['view_id'] for v in cat['questions']}
   questions+=len(expected);max_questions=max(max_questions,len(got))
   if got!=expected: bad.append({'seq':seq,'kind':'catalog','missing':sorted(expected-got),'extra':sorted(got-expected)})
   if expected and not positive_control:
    mutant=set(got);mutant.remove(next(iter(expected)));assert mutant!=expected;positive_control=True
   max_evidence=max(max_evidence,len(out['evidence']))
   for view in out['questions']:
    ref={l['evidence_id'] for l in links if l['view_id']==view['view_id'] and l['seq']<seq and by_id[l['evidence_id']]['created_seq']<seq}
    actual=set(view['evidence_ids']);evidence_links+=len(ref)
    if ref!=actual:bad.append({'seq':seq,'view_id':view['view_id'],'missing':sorted(ref-actual),'extra':sorted(actual-ref)})
 assert positive_control and questions>0 and evidence_links>0 and not bad
 result={'sequences':len(seqs),'question_instances':questions,'evidence_link_instances':evidence_links,'max_catalog_questions':max_questions,'max_distinct_expanded_evidence':max_evidence,
         'mismatches':bad,'positive_control':'a removed known question is detected',
         'unexercised':{'dependencies':len(deps),'replacements':len(replacements)},
         'limit':'Checks structural historical inclusion against saved v38 ledger; does not prove correct analyst questions, economic meaning or production integration.'}
 with OUT.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
