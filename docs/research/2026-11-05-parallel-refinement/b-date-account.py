# -*- coding: utf-8 -*-
"""Ask the model about one saved date decision, without a prompt change."""
import copy,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT/'src'))
from hivemind import model
ident='gnews:69d682468e018e0065df5180';RUN=ROOT/'poc/data/parallel-b-link-2026-11-05-v2';FROZEN=HERE/'b-arm-frozen-v2.json'
question="In this answer, you set original_day to 2026-08-29 for the NVIDIA reported figures and for the CFO's remarks. Identify the exact text in the supplied article that establishes the date each original party made those statements, and the instruction you applied. Explain whether the author's publication date establishes the CFO's original statement date. Do not invent an event or date."
def request():
 frozen=json.loads(FROZEN.read_text());r=next(x for x in frozen['requests'] if x['id']==ident and x['variant']=='treatment');q=copy.deepcopy(r['request']);assert hashlib.sha256(json.dumps(q).encode()).hexdigest()==r['wire_sha256'];response=json.loads((RUN/'gnews_69d682468e018e0065df5180-treatment-2'/'response.json').read_text());answer=response['choices'][0]['message']['content'];json.loads(answer);q['messages'] += [{'role':'assistant','content':answer},{'role':'user','content':question}];q.pop('response_format');q['max_completion_tokens']=2000;return q
if __name__=='__main__':
 if len(sys.argv)!=3 or sys.argv[1] not in ('freeze','send'):raise SystemExit('freeze|send absolute-path')
 out=Path(sys.argv[2]);r=request()
 if not out.is_absolute():raise ValueError('absolute path required')
 if sys.argv[1]=='freeze':
  if out.exists():raise ValueError('exists')
  out.mkdir(parents=True);(out/'request.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('frozen',hashlib.sha256(json.dumps(r).encode()).hexdigest())
 else:
  assert r==json.loads((out/'request.json').read_text());path=out/'response.json'
  if path.exists():raise ValueError('already sent')
  response=model.openai_transport('openai',r);path.write_text(json.dumps(response,ensure_ascii=False,indent=2)+'\n');print(response['choices'][0]['message'].get('content',''))
