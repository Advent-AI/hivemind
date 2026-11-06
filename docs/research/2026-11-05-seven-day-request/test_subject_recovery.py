"""An actually written research subject keeps its name after process restart."""
import copy,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path[:0]=[str(HERE),str(ROOT/'src')]
import split_seven_day_poc as p
from hivemind import extraction,universe
from hivemind.views import matching,store,writing

def main():
 cfg,uni,_,_=p.prior.build()
 with tempfile.TemporaryDirectory(prefix='subject-recovery-') as d:
  conn=store.open_db(str(Path(d)/'views.sqlite'))
  candidate={'id':'c1','kind':'asset','object':'Mariner Therapeutics','looks_at':'Its proposed therapy','question':'Will its therapy be approved?','year':'','due_day':'','rungs':[],'evidence_ids':['e1'],'group_refs':[]}
  rejected=dict(candidate,id='c2',object='Unwritten Research LLC',evidence_ids=[])
  hand=extraction.Handover([{'id':'e1','quote':'Mariner Therapeutics announced it has filed for approval.','one_line':'Mariner filed for approval.','speaker':'Mariner','original_who':'Mariner','original_day':'','tier':'party_statement','event_time':'','links':['c1']}],[candidate,rejected],[],0,'',False,0,[])
  p.register_subjects(uni,hand.candidates,conn);identity=candidate['object'];not_written=rejected['object']
  checked=matching.Checked({'c1':('new',None,[]),'c2':('skip',None,[])},{},[],{})
  item={'input_id':'news:2026-08-29','publication_day':'2026-08-29','category':'T7'}
  result=writing.write(conn,uni,1205,item,hand,checked,{})
  conn.commit();conn.close()
  restored=universe.load(str(ROOT/'poc/universe.json'));conn=store.open_db(str(Path(d)/'views.sqlite'));p.load_written_subjects(conn,restored)
  assert restored.resolve('Mariner Therapeutics')==identity
  assert restored.resolve('Unwritten Research LLC') is None
  view=store.view(conn,result.new_views['c1']);assert view['object_id']==identity and 'Mariner Therapeutics' in view['looks_at']
  name_collision={'id':'c3','kind':'theme','object':'NVIDIA','question':'Theme question','looks_at':'Theme','year':'','due_day':'','rungs':[],'evidence_ids':[],'group_refs':[]}
  p.register_subjects(restored,[name_collision],conn)
  assert restored.kind(name_collision['object'])=='theme' and name_collision['object']!='NVDA'
  theme={'id':'c4','kind':'theme','object':'Cloud Infrastructure','question':'What happens to infrastructure?','looks_at':'Infrastructure','year':'','due_day':'','rungs':[],'evidence_ids':[],'group_refs':[]}
  p.register_subjects(restored,[theme],conn)
  new_name={'id':'c5','kind':'theme','object':'cloud infrastructure','question':'What happens next?','looks_at':'Infrastructure','year':'','due_day':'','rungs':[],'evidence_ids':[],'group_refs':[]}
  p.register_subjects(restored,[new_name],conn)
  assert new_name['object']==theme['object']
  conn.close()
 print('PASS: written dynamic subject survives restart; unwritten subject stays out; company/theme names remain distinct.')
if __name__=='__main__':main()
