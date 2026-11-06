# -*- coding: utf-8 -*-
"""Identity controls on stored A answers and real extraction handover, no paid model calls."""
import copy,json,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OLD=ROOT/'docs/research/2026-11-05-parallel-thesis-evidence-poc'
sys.path[:0]=[str(HERE),str(OLD),str(ROOT/'src')]
import a_id_contract as contract,prepare,run_poc
from hivemind import model
RUN=ROOT/'poc/data/parallel-thesis-evidence-poc-2026-11-05'
class Dummy:call_id=0;request_sha256='fake';cached=False;cost_usd=0

def load(ident):return json.loads((RUN/(ident.replace(':','_')+'-new')/'result.json').read_text())['answer']
def refusal(data,schema):
 try:contract.check_answer(data,schema)
 except contract.IdentityRefusal:return
 raise AssertionError('invalid ID accepted')
def main():
 cfg,uni,records=prepare.prepare();ident='gnews:d144b91986c520ea36e718cf';r=next(x for x in records if x['arm']=='new' and x['item']['input_id']==ident);schema=contract.experimental_schema(r['schema']);original=load(ident);contract.check_answer(original,schema)
 duplicate=copy.deepcopy(original);other=copy.deepcopy(duplicate['candidates'][0]);other['question']='A distinct candidate question with the same identifier?';duplicate['candidates'].append(other);refusal(duplicate,schema)
 one_survives=copy.deepcopy(duplicate);one_survives['candidates'][1]['settled_by']='';refusal(one_survives,schema)
 good=copy.deepcopy(duplicate);good['candidates'][1]['id']='c2';contract.check_answer(good,schema)
 for ident_value in ('n1','c١','c1\n'):
  bad=copy.deepcopy(original);bad['candidates'][0]['id']=ident_value;refusal(bad,schema)
 zero=copy.deepcopy(original);zero['candidates'][0]['id']='c0';contract.check_answer(zero,schema)
 ident2='gnews:69d682468e018e0065df5180';r2=next(x for x in records if x['arm']=='new' and x['item']['input_id']==ident2);saved=load(ident2);refusal(saved,contract.experimental_schema(r2['schema']))
 old=copy.deepcopy(saved);old['candidates'][0]['evidence_ids']=['e2'];e=copy.deepcopy(old['evidence'][0]);e.update(id='e2',quote='Total revenue reached $96.2 billion',links=[]);old['evidence'].append(e)
 h=run_poc.handover(old,r2,uni,Dummy());assert not h['candidates'] and h['evidence'][0]['links']==['n1']
 fixed=copy.deepcopy(old);fixed['candidates'][0]['id']='c1';fixed['evidence'][0]['links']=['c1'];h=run_poc.handover(fixed,r2,uni,Dummy());assert not h['candidates'] and not h['evidence']
 # A duplicate survives provider schema and is cached; local uniqueness is checked on fresh and cache reads.
 with tempfile.TemporaryDirectory(prefix='hivemind-a-id-') as tmp:
  archive=model.Archive(str(Path(tmp)/'archive.sqlite'));responses=[]
  def fake(provider,request):
   responses.append(1);return {'choices':[{'message':{'content':json.dumps(duplicate)}}],'usage':{'prompt_tokens':0,'completion_tokens':0}}
  for i in range(2):
   answer=model.call(archive,cfg,r['setting'],r['system'],r['user'],schema,'extraction','extract',transport=fake)
   assert answer.cached==(i==1)
   try:contract.checked_handover(answer.data,schema,r,uni,answer)
   except contract.IdentityRefusal:pass
   else:raise AssertionError('duplicate bypassed fresh/cache check')
  assert len(responses)==1;archive.conn.close()
 assert run_poc.join_results([{'status':'ok','arm':'existing'},{'status':'failed','arm':'new'}])['status']=='incomplete'
 print('A identity: valid c1/c2/c0; duplicate, Unicode/newline/n1 refused; cached duplicate refused; saved n1 orphan mutant reproduced, c1 control removed; failed pair incomplete.')
if __name__=='__main__':main()
