"""The saved 1207 A answer must not lose evidence when metadata is prepared."""
import copy,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path[:0]=[str(HERE),str(ROOT/'src')]
import split_seven_day_poc as p
from hivemind import model,testdb

def main():
 run=ROOT/'poc/data/split-fresh-seven-day-2026-11-05-v1';f=run/'items'/'1207';a=p.read(f/'a-answer.json');b=p.read(f/'b-answer.json');shown=p.read(f/'shown.json');old=p.read(f/'meta-answer.json');
 c=p.store.open_read_only(str(run/'snapshot/views.sqlite'));input_id=c.execute('select input_id from processing_steps where sequence_no=1207 limit 1').fetchone()[0];c.close()
 db=testdb.open_db(str(p.INPUT));item=testdb.item_of(db.execute('select * from items where input_id=?',(input_id,)).fetchone());db.close()
 _,uni,_,_=p.prior.build();spec=p.metadata_request(item,a);schema=spec[2]
 meta={'candidates':{r['id']:{k:v for k,v in r.items() if k!='id'} for r in old['candidates']},'evidence':{}}
 for i in range(1,16):
  # Placeholder values exercise the interface only; they are not a source attribution or a model response.
  meta['evidence']['e'+str(i)]={'speaker':item['publisher'],'original_who':'','original_day':'','tier':'unknown','event_time':''}
 assert not model.check_schema(meta,schema)
 hand=p.build_handover(item,shown,uni,a,b,meta)
 assert len(a['questions'])==1 and len(a['questions'][0]['evidence'])==15
 actual=[e for e in hand.evidence if 'c1' in e['links']]
 assert len(actual)==15
 assert [(e['quote'],e['one_line']) for e in actual]==[(p.source_quote(e['quote'],item['text']),e['what_it_shows']) for e in a['questions'][0]['evidence']]
 for index,e in enumerate(b['evidence'],1):
  matching=[x for x in hand.evidence if x['id']=='e'+str(15+index)]
  if e['links'] and p.source_quote(e['quote'],item['text']) is not None:
   assert len(matching)==1 and matching[0]['quote']==p.source_quote(e['quote'],item['text']) and matching[0]['links']==e['links']
 reordered={'candidates':[dict(v,id=k) for k,v in reversed(list(meta['candidates'].items()))],
            'evidence':[dict(v,id=k) for k,v in reversed(list(meta['evidence'].items()))]}
 assert p.build_handover(item,shown,uni,a,b,reordered).evidence==hand.evidence
 missing=copy.deepcopy(meta);del missing['evidence']['e8']
 assert model.check_schema(missing,schema)
 try:p.build_handover(item,shown,uni,a,b,missing)
 except ValueError:pass
 else:raise AssertionError('missing evidence metadata accepted')
 extra=copy.deepcopy(meta);extra['evidence']['e16']=copy.deepcopy(meta['evidence']['e1'])
 assert model.check_schema(extra,schema)
 try:p.build_handover(item,shown,uni,a,b,extra)
 except ValueError:pass
 else:raise AssertionError('unknown evidence metadata accepted')
 print('PASS: all 15 saved A passages survive; missing and unknown metadata IDs are refused. Values were synthetic.')
if __name__=='__main__':main()
