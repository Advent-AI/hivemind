"""D162: replay every prior answer through the new handoff and capture representative complete requests."""
import json
from pathlib import Path
import source_first as split
import ohio_sequence as o

out=Path(__file__).resolve().parent
old=out.parent/'2026-10-25-extraction-evidence-01'
items=o.read(old/'items.json'); uni=o.universe.load(old/'universe.json'); cfg=o.config.load(old/'config.json')
counts={'answers':0,'candidates':0,'evidence':0,'kept_candidates':0,'kept_evidence':0,'drops':[]}
for f in sorted(old.glob('*/item*/extraction.json')):
    raw=o.read(f);ctx=o.read(f.parent/'context.json');item=items[int(f.parent.name[4:])-1]
    source={'observations':[{k:v for k,v in e.items() if k!='links'} for e in raw['evidence']]}
    organised={'candidates':[{k:v for k,v in c.items() if k!='evidence_ids'} for c in raw['candidates']], 'threads':raw['threads'],
               'dispositions':{e['id']:{'links':e['links'],'omit_reason':''} for e in raw['evidence']}}
    restored=split.assemble(source,organised,ctx['offered'])
    assert restored==raw
    ev,ca,dr=o.extraction.sift(restored,item,item['text'],{v['view_id'] for v in ctx['shown']},uni)
    previous=o.read(f.parent/'handover.json')
    assert ev==previous['evidence'] and ca==previous['candidates'] and [list(x) for x in dr]==previous['dropped']
    counts['answers']+=1;counts['candidates']+=len(ca);counts['evidence']+=len(raw['evidence'])
    counts['kept_candidates']+=len(ca);counts['kept_evidence']+=len(ev)
    counts['drops'] += [{'file':str(f.relative_to(old)),'reason':d} for d in dr]
assert counts['answers']==18
item=items[0];ctx=o.read(old/'control-1/item1/context.json')
raw=o.read(old/'control-1/item1/extraction.json')
source={'observations':[{k:v for k,v in e.items() if k!='links'} for e in raw['evidence']]}
context=split.research_context(item,ctx['shown'],uni)
requests={
 'control':o.read(old/'control-first-request.json'),
 'source':o.model.build_request(cfg.extraction_setting('T7'),(out/'read-source.txt').read_text(),json.dumps(dict(context,text=item['text']),ensure_ascii=False),split.source_schema(),'source_selection',cfg.provider),
 'organisation_example':o.model.build_request(cfg.extraction_setting('T7'),(out/'organise-source.txt').read_text()+'\n\n'+o.GROUP_PROMPT,json.dumps(dict(context,groups=ctx['offered'],observations=source['observations']),ensure_ascii=False),split.organisation_schema(source['observations'],ctx['offered']),'question_construction',cfg.provider)}
# D161's control request used D160; this comparison's control is D161's treatment role.
requests['control']=o.read(old/'grouped-first-request.json')
for name,request in requests.items():o.write(out/f'{name}-request.json',request)
counts['request_chars']={name:len(json.dumps(req,ensure_ascii=False)) for name,req in requests.items()}
counts['role_chars']={name:len((out/file).read_text()) for name,file in [('source','read-source.txt'),('organisation','organise-source.txt')]}
counts['control_role_chars']=len((old/'role-evidence.txt').read_text())
counts['organisation_note']='Representative saved 2-evidence answer; real second request depends on first response.'
o.write(out/'offline.json',counts)
print(json.dumps(counts,ensure_ascii=False,indent=2))
