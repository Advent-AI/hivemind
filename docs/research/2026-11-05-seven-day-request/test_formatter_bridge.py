"""Offline bridge contract controls against a saved real A answer and article."""
import copy,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path[:0]=[str(HERE),str(ROOT/'src'),str(ROOT/'docs/research/2026-11-05-parallel-refinement')]
from hivemind import extraction,universe,testdb
import formatter_bridge as bridge

ID='gnews:69d682468e018e0065df5180'
def fixture():
 path=ROOT/'poc/data/start-state-new-question-diagnostic-2026-11-05-v1/gnews_69d682468e018e0065df5180/result.json'
 raw=json.loads(path.read_text())['answer'];db=testdb.open_db(str(ROOT/'poc/data/parallel-thesis-evidence-input-2026-11-05/items.sqlite'))
 item=testdb.item_of(db.execute('select * from items where input_id=?',(ID,)).fetchone());db.close()
 if len(raw['questions'])!=1 or len(raw['questions'][0]['evidence'])!=6:raise AssertionError('saved positive changed')
 # Synthetic record fields demonstrate only code wiring, not a real or approved ladder/date.
 bounds=[(350e9,None),(300e9,350e9),(250e9,300e9),(200e9,250e9),(None,200e9)]
 labels=['Strongly bullish','Bullish','Neutral','Bearish','Strongly bearish']
 rungs=[{'label':label,'condition':f'test band {i+1}','lo':lo,'hi':hi} for i,((lo,hi),label) in enumerate(zip(bounds,labels))]
 c={'candidate_id':'c1','object':'NVDA','kind':'asset','looks_at':'NVIDIA total critical component commitments at FY2027 end','rungs':rungs,'due_day':'2027-02-28','year':'FY2027','measure':'financing_amount','scope':'critical components','period_start':'2026-02-01','period_end':'2027-01-31','basis':'n/a','unit':'USD','event_type':'n/a','group_refs':[],'opens_as':'binding_obligation','settled_by':'FY2027 annual report; check date is test-only'}
 e=[{'evidence_id':f'e{i}','speaker':'Article author','original_who':ev['original_speaker'],'original_day':'','tier':'third_party_view','event_time':''} for i,ev in enumerate(raw['questions'][0]['evidence'],1)]
 meta={'candidate_fields':[c],'evidence_fields':e,'date_notes':[{'basis':'analyst_check','reason':'mock check day, not source-stated','source_span':'','rung_reason':'test fixture only; no analyst assessment'}],'new_groups':[]}
 return raw,item,meta

def expect_refusal(name,raw,item,meta,uni):
 try:bridge.build(raw,item['text'],item,{'v1','v2','v6'},uni,meta)
 except bridge.BridgeRefusal as e:print(name,': refused:',str(e)[:95]);return
 raise AssertionError(name+' did not refuse')

def main():
 raw,item,meta=fixture();uni=universe.load(str(ROOT/'poc/universe.json'))
 result=bridge.build(raw,item['text'],item,{'v1','v2','v6'},uni,meta)
 assert result['status']=='structure_only_semantics_unverified'
 assert result['candidates'][0]['question']==raw['questions'][0]['question']
 assert [(e['quote'],e['one_line']) for e in result['evidence']]==[(e['quote'],e['what_it_shows']) for e in raw['questions'][0]['evidence']]
 assert 'Analyst-selected check date' in result['candidates'][0]['looks_at']
 print('positive: saved A question and six source quotes/summaries preserved; mock only')
 a=copy.deepcopy(raw);a['questions'][0]['evidence'][0]['quote']='A fabricated sentence that never appeared.';expect_refusal('invented quote',a,item,meta,uni)
 m=copy.deepcopy(meta);m['evidence_fields'].pop();expect_refusal('missing evidence metadata',raw,item,m,uni)
 m=copy.deepcopy(meta);m['candidate_fields'][0]['question']='fabricated';expect_refusal('extra candidate question',raw,item,m,uni)
 m=copy.deepcopy(meta);m['candidate_fields'][0]['due_day']='2026-02-30';expect_refusal('invalid date',raw,item,m,uni)
 m=copy.deepcopy(meta);m['date_notes'][0].update(basis='source',source_span='invented date');expect_refusal('unsupported source date',raw,item,m,uni)
 m=copy.deepcopy(meta);m['date_notes'][0].update(basis='source',source_span='Nvidia');expect_refusal('source span without date',raw,item,m,uni)
 m=copy.deepcopy(meta);m['evidence_fields'][0]['original_day']='2026-07-17';expect_refusal('unsupported original day',raw,item,m,uni)
 m=copy.deepcopy(meta);m['evidence_fields'][0],m['evidence_fields'][1]=m['evidence_fields'][1],m['evidence_fields'][0];expect_refusal('reordered evidence metadata',raw,item,m,uni)
 m=copy.deepcopy(meta);m['candidate_fields'][0]['period_start']='2026-03-01';expect_refusal('period silently normalized',raw,item,m,uni)
 m=copy.deepcopy(meta);m['candidate_fields'][0]['rungs'].reverse();expect_refusal('rungs silently normalized',raw,item,m,uni)
 m=copy.deepcopy(meta);m['candidate_fields'][0]['group_refs']=['n1'];m['new_groups']=[{'id':'n1','name':'  Supply commitments  ','scope':'  Company supply commitments  ','aliases':[]}];expect_refusal('group definition normalized',raw,item,m,uni)
 a=copy.deepcopy(raw);a['questions'][0]['evidence'][1]['quote']=a['questions'][0]['evidence'][0]['quote'];expect_refusal('same quote distinct A matters merged',a,item,meta,uni)
 p=ROOT/'poc/data/parallel-b-link-2026-11-05-v2/gnews_3df0bbc8aff2c1d008bc0a32-control-3/result.json'
 result=json.loads(p.read_text()); es=result['answer']['evidence'];e1,e2=es[:2]
 assert e1['quote']==e2['quote'] and e1['one_line']!=e2['one_line']
 assert any('same quote as e1' in reason for _,reason in result['handover']['dropped'])
 saved=next(e for e in result['handover']['evidence'] if e['id']=='e1')
 assert 'v2' in saved['links'] and 'v10' in saved['links'] and saved['one_line']==e1['one_line']
 print('stored real B collision reproduced: total-revenue summary assigned to total and data-center links')
 print('No formatter model, matcher, writer, seven-day run or semantic score executed.')
if __name__=='__main__':main()
