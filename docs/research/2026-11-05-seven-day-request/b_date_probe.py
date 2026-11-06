"""One stored-source B request testing source-date wording, no writer."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path[:0]=[str(HERE),str(ROOT/'src')]
import split_seven_day_poc as p
from hivemind import config,extraction,testdb,universe

def main(out):
 if out.exists():raise ValueError('output exists')
 out.mkdir(parents=True)
 cfg=config.load(str(ROOT/'poc/config/poc-v117.json'));uni=universe.load(str(ROOT/'poc/universe.json'))
 db=testdb.open_db(str(p.INPUT));item=testdb.item_of(db.execute('select * from items where input_id=?',('gnews:69d682468e018e0065df5180',)).fetchone());db.close()
 conn=p.prior.b_arm.prior.ro(p.prior.SNAP);shown=extraction.shown_views(conn,cfg,item,['NVDA']);conn.close()
 setting,requests=p.item_requests(cfg,uni,item,shown)
 response=p.call(cfg,setting,'b',requests['b'],out)
 print('B returned',len(response['evidence']),'items; original days:',[e['original_day'] for e in response['evidence']],flush=True)
if __name__=='__main__':main(Path(sys.argv[1]))
