"""Continue saved conversations for three observed decisions; no prompt or product mutation."""
import copy,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT/'src'))
from hivemind import model
PREV=ROOT/'docs/research/2026-11-05-parallel-thesis-evidence-poc/frozen-requests.json'
RUN=ROOT/'poc/data/parallel-thesis-evidence-poc-2026-11-05'
CASES=[('gnews:d144b91986c520ea36e718cf','new','The article includes analyst expectations for Microsoft FY2027 total revenue and management next-quarter total-revenue guidance, while your answer proposed an Azure FY2027 question. Explain how you considered the total-revenue perspective; which instructions guided that choice, and which two alternative candidate questions or interpretations did you consider and reject? Use only the supplied request and article; do not invent a prior question.'),('gnews:69d682468e018e0065df5180','existing','In your answer, the quarterly revenue guidance is linked to v2, while the immediately following assumption of no China compute sales has an empty links array. Explain the decisions you made for both statements and which instructions or question descriptions guided them. Identify any alternatives you considered; do not change your prior answer.'),('gnews:8f8a2d115ab834c7026aefd1','existing','Explain why you linked the statement about a possible Hugging Face acquisition to v64. Identify the article statements and question description that led you there, what the source does or does not establish, and which other filing or rejection possibilities you considered. Do not invent negotiations or new facts.')]
def sha(b):return hashlib.sha256(b).hexdigest()
def build():
 frozen=json.loads(PREV.read_text());out=[]
 for ident,arm,question in CASES:
  entry=next(x for x in frozen if x['id']==ident and x['arm']==arm)
  req=copy.deepcopy(entry['request']);assert sha(json.dumps(req).encode())==entry['request_sha256']
  response=json.loads((RUN/(ident.replace(':','_')+'-'+arm)/'response.json').read_text());answer=response['choices'][0]['message']['content'];json.loads(answer)
  req['messages'] += [{'role':'assistant','content':answer},{'role':'user','content':question}]
  req.pop('response_format',None);req['max_completion_tokens']=2000
  out.append({'id':ident,'arm':arm,'question':question,'request':req,'wire_sha256':sha(json.dumps(req).encode())})
 return out
if __name__=='__main__':
 if len(sys.argv)!=3 or sys.argv[1] not in ('freeze','send'):raise SystemExit('freeze|send new-absolute-dir')
 out=Path(sys.argv[2]);records=build()
 if not out.is_absolute():raise ValueError('absolute path')
 if sys.argv[1]=='freeze':
  if out.exists():raise ValueError('already exists')
  out.mkdir(parents=True);(out/'requests.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');print('frozen',len(records),sha((out/'requests.json').read_bytes()))
 else:
  frozen=json.loads((out/'requests.json').read_text());assert frozen==records
  for i,r in enumerate(records):
   path=out/f'response-{i}.json'
   if path.exists():raise ValueError('refuse resend')
   response=model.openai_transport('openai',r['request']);path.write_text(json.dumps(response,ensure_ascii=False,indent=2)+'\n')
   print(i,r['id'],r['arm'],response['choices'][0]['message'].get('content',''),flush=True)
