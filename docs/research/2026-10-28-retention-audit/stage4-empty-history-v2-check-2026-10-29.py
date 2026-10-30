"""Offline positive and negative controls of the frozen empty-history arm."""
import copy
import hashlib
import json
import shutil
import tempfile
from pathlib import Path

HERE=Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-retention-audit')
p=HERE/'stage4-empty-history-arm-v2-2026-10-29.py';raw=p.read_bytes();namespace={'__name__':'empty_history_check','__file__':str(p),'__executed_sha256__':hashlib.sha256(raw).hexdigest()}
exec(compile(raw,str(p),'exec'),namespace);sender=namespace['sender'];_,cases,reqs=namespace['frozen_requests']()
old=json.loads((HERE/'stage4-evidence-first-arm-2026-10-29/science-control-luna-1.json').read_text())
case=cases['science-control'];req=reqs[('science-control','luna')];row=sender['reservation']('science-control','luna',req,10000)
record=sender['parse_response'](old['response'],'luna',case);record['error']=None
if not record['structural_errors'] or sender['should_stop'](record,'luna',row):raise ValueError('known control error not observed and allowed')
mutants=[]
x=copy.deepcopy(record);x['answer']['same_claim_as']=['item:e999999'];x['structural_errors']=['same_claim_as: not a historical evidence id item:e999999'];mutants.append(x)
x=copy.deepcopy(record);x['structural_errors'].append('unknown question');mutants.append(x)
x=copy.deepcopy(record);x['response'].pop('usage');mutants.append(x)
x=copy.deepcopy(record);x['error']={'type':'HTTPError'};mutants.append(x)
for x in mutants:
 if not sender['should_stop'](x,'luna',row):raise ValueError('unexpected failure did not stop')
for target in ('science-elide','sharon-control'):
 r=copy.deepcopy(row);r['case']=target
 if not sender['should_stop'](record,'luna',r):raise ValueError('wrong arm or historical case allowed')
for value in ([], 'not an object', 123):
 response={'choices':[{'finish_reason':'stop','message':{'content':json.dumps(value)}}], 'usage':{'prompt_tokens':20,'completion_tokens':10}}
 result=sender['parse_response'](response,'luna',cases['science-elide']);result['error']=None
 r=sender['reservation']('science-elide','luna',req,10000)
 if result['response']!=response or result['usable'] or not sender['should_stop'](result,'luna',r):raise ValueError('non-object result lost or did not stop')
original=namespace['RUN'];sender_run=sender['RUN']
with tempfile.TemporaryDirectory() as temp:
 d=Path(temp)
 for f in original.glob('*-request.json'):shutil.copyfile(f,d/f.name)
 manifest=json.loads((original/'manifest.json').read_text());manifest['cases']=dict(reversed(list(manifest['cases'].items())))
 (d/'manifest.json').write_text(json.dumps(manifest));namespace['RUN']=d;sender['RUN']=d
 try:
  try:namespace['frozen_requests']()
  except ValueError as e:
   if 'case order changed' not in str(e):raise
  else:raise ValueError('reordered case manifest accepted')
 finally:namespace['RUN']=original;sender['RUN']=sender_run
print('expected relation refusal continues; 6 unrelated failures stop; 3 non-object answers preserve response and stop; reordering rejected')
