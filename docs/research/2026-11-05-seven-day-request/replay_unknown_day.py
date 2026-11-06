"""Compare the stored unknown-day revision against a proposed writer edit in temporary copies."""
import json,sqlite3,sys,tempfile,types
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT/'src'))
from hivemind import testdb,universe
from hivemind.views import matching,store,writing
ID='gnews:71114e6d410b3ece8ed7f321'

def load():
 c=sqlite3.connect((ROOT/'poc/data/parallel-thesis-evidence-input-2026-11-05/views.sqlite').resolve().as_uri()+'?mode=ro',uri=True)
 raw=c.execute('select handover_json from handovers where seq=1208 and input_id=?',(ID,)).fetchone();c.close()
 e=next(e for e in json.loads(raw[0])['evidence'] if e['id']=='e3')
 items=testdb.open_db(str(ROOT/'poc/data/parallel-thesis-evidence-input-2026-11-05/items.sqlite'));item=testdb.item_of(items.execute('select * from items where input_id=?',(ID,)).fetchone());items.close()
 if e['original_day']!='' or e['links']!=['v64'] or item['publication_day']!='2026-08-29':raise ValueError('known case changed')
 return e,item

def module_with_proposal():
 src=Path(writing.__file__).read_text();old="new_day = said_day or e['original_day'] or item['publication_day']";new="new_day = e['original_day'] or ''"
 old2="if old and old['original_day'] and new_day < old['original_day']:";new2="if new_day and old and old['original_day'] and new_day < old['original_day']:"
 if src.count(old)!=1 or src.count(old2)!=1:raise ValueError('writer source changed')
 module=types.ModuleType('hivemind.views._day_probe');module.__package__='hivemind.views';sys.modules[module.__name__]=module
 exec(compile(src.replace(old,new).replace(old2,new2),writing.__file__,'exec'),module.__dict__)
 return module

def trial(module,e,item,uni):
 with tempfile.TemporaryDirectory(prefix='day-proof-') as d:
  target=Path(d)/'views.sqlite';source=sqlite3.connect((ROOT/'poc/data/pilot-d369-existing-library-v2/views.sqlite').resolve().as_uri()+'?mode=ro',uri=True);dest=sqlite3.connect(str(target));source.backup(dest);dest.close();source.close()
  c=store.open_db(str(target));assert store.evidence(c,'e3858') and 'v64' in store.views_linked_to(c,'e3858')
  h=type('H',(),{'candidates':[],'evidence':[e],'dropped':[],'new_groups':[]})();decisions=matching.Checked({}, {(e['id'],'v64'):('replace','e3858','2026-08-29')}, [], {})
  before=c.execute('select count(*) from revisions').fetchone()[0];out=module.write(c,uni,1208,item,h,decisions,{});after=c.execute('select count(*) from revisions').fetchone()[0]
  written=store.evidence(c,out.evidence_ids[e['id']]);links=store.views_linked_to(c,written['evidence_id']);result={'new_revisions':after-before,'original_day':written['original_day'],'links':links,'notes':out.notes};c.rollback();c.close();return result

def main():
 e,item=load();uni=universe.load(str(ROOT/'poc/universe.json'));old=trial(writing,e,item,uni);new=trial(module_with_proposal(),e,item,uni)
 if old['new_revisions']!=1 or new['new_revisions']!=0 or 'v64' not in new['links'] or new['original_day']!='' or not any('no stated day' in n for n in new['notes']):raise AssertionError((old,new))
 print('Original writer:',old);print('Proposed writer:',new);print('Stored case flipped on temporary copies; no source or production file edited.')
if __name__=='__main__':main()
