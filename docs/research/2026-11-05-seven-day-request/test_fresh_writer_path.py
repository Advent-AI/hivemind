"""D375: a real writer makes a new question visible to both next-item requests."""
import copy, json, sqlite3, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path[:0]=[str(HERE),str(ROOT/'src')]
import split_seven_day_poc as p
from hivemind import extraction, testdb
from hivemind.views import matching, store, writing

def main():
 cfg,uni,_,_=p.prior.build()
 items=testdb.open_db(str(p.INPUT))
 first=testdb.item_of(items.execute('select * from items where input_id=?',('gnews:dbbde813240d4096829a72a9',)).fetchone())
 second=testdb.item_of(items.execute('select * from items where input_id=?',('gnews:69d682468e018e0065df5180',)).fetchone())
 old=p.REUSE/'items'
 first_saved=p.read(old/'1210'/'handover.json')
 second_saved=p.read(old/'1211'/'handover.json')
 with tempfile.TemporaryDirectory(prefix='fresh-writer-') as d:
  source=sqlite3.connect(p.prior.SNAP.resolve().as_uri()+'?mode=ro',uri=True)
  target=sqlite3.connect(str(Path(d)/'views.sqlite'));source.backup(target);source.close();target.close()
  conn=store.open_db(str(Path(d)/'views.sqlite'))
  before=p.latest_library(conn,1210)
  candidate=copy.deepcopy(first_saved['candidates'][0])
  evidence=[copy.deepcopy(e) for e in first_saved['evidence'] if 'c1' in e['links']]
  for e in evidence:e['links']=['c1']
  handover=extraction.Handover(evidence,[candidate],[],0,'',False,0,[])
  checked=matching.Checked({'c1':('new',None,[])},{},[],{})
  written=writing.write(conn,uni,1210,first,handover,checked,{})
  conn.commit();new_id=written.new_views['c1']
  assert new_id not in {v['view_id'] for v in before}
  shown=p.latest_library(conn,1211)
  assert new_id in {v['view_id'] for v in shown}
  _,req=p.item_requests(cfg,uni,second,shown)
  assert new_id in req['a'][1] and new_id in req['b'][1]
  later=copy.deepcopy(second_saved['evidence'][0]);assert later['quote'] in second['text']
  later['links']=[new_id]
  bh=extraction.Handover([later],[],[],0,'',False,0,[])
  bc=matching.Checked({}, {(later['id'],new_id):('new',None,'')},[],{})
  bwrite=writing.write(conn,uni,1211,second,bh,bc,{})
  conn.commit();stored=bwrite.evidence_ids[later['id']]
  assert new_id in store.views_linked_to(conn,stored)
  assert store.evidence(conn,stored)['quote']==later['quote']
  conn.close()
 items.close()
 print('PASS: real writer -> same-day shared A/B snapshot -> real writer attaches next article evidence; external model decisions are faked.')
if __name__=='__main__':main()
