"""Step 2 reader (D250 ported under D201): the catalog is the open questions in scope before a sequence number, the expansion is
every active piece of the chosen questions with sources, predecessors and the latest judgement, nothing from after that number."""
import os
import sys
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import research_context as context, universe  # noqa: E402
from hivemind.views import store  # noqa: E402


def make_ledger(path):
    db=store.open_db(str(path))
    for vid,obj,seq in [('v1','NVDA',1),('v2','NVDA',30),('v3','AMD',1),('v4','ai-capex',1),('v5','AMD',1)]:
        store.create_view(db,view_id=vid,object_id=obj,object_kind='theme' if obj=='ai-capex' else 'company',kind='numeric',
            looks_at='CPU revenue',question='Will standalone CPU sales grow?',due_day='2027-01-31',year='FY2027',
            rungs=[],seq=seq,input_id='test:source',created_at='2026-08-12T00:00:00Z')
    for n in range(1,16):
        store.add_evidence(db,evidence_id=f'e{n}',quote=f'CPU benchmark caveat {n}',one_line=f'CPU caveat {n}',
            speaker='Example News',original_who='',original_day='',tier='fact',event_time='',seq=n,input_id='test:source')
        store.add_source(db,f'e{n}','test:source','T6','2026-08-12','paragraph 1',n)
        store.link(db,f'e{n}','v1',n)
    store.replace(db,'e1','e2','2026-08-12',2)
    store.replace(db,'e15','e3','2026-08-30',30)
    store.add_source(db,'e3','test:future','T6','2026-08-30','paragraph 1',30)
    store.insert(db,'dependencies',view_id='v1',depends_on='v3',direction='same',seq=3)
    store.close_view(db,'v3','due','test',4)
    store.insert(db,'dependency_resolutions',dependency_id=1,resolved_to='v2',reason='later successor',seq=30)
    for seq,rung,day in [(4,1,'2026-08-12'),(30,2,'2026-08-30')]:
        store.insert(db,'judgements',view_id='v1',seq=seq,input_id='test:source',rung=rung,
            reasons='CPU demand estimate',publication_day=day)
    store.close_view(db,'v1','done','test',30)
    db.commit();db.close()


def test_complete_scoped_history_and_explicit_limit(tmp_path):
    """D250 catalog scope, no future leakage, all evidence beyond top ten."""
    path=tmp_path/'views.sqlite';make_ledger(path)
    uni=universe.Universe({'version':'test','companies':[{'id':'NVDA'},{'id':'AMD'}],
                           'themes':[{'id':'ai-capex','name':'AI capex'}]})
    with context.Reader(path,20,['NVDA'],uni) as reader:
        assert {q['view_id'] for q in reader.catalog()['questions']}=={'v1','v3','v4'}
        result=reader.expand(['v1'])
        assert result['questions'][0]['dependencies'][0]['resolved_to']=='v3'
        assert result['questions'][0]['latest_judgement']['seq']==4
        assert set(result['questions'][0]['evidence_ids'])=={f'e{i}' for i in range(2,16)}
        e2=next(e for e in result['evidence'] if e['evidence_id']=='e2')
        assert e2['replaced'][0]['evidence']['evidence_id']=='e1'
        assert all(s['input_id']!='test:future' for e in result['evidence'] for s in e['sources'])
        with pytest.raises(ValueError,match='from this historical catalog'):
            reader.expand(['v5'])
        assert reader.expand([])['evidence']==[]
    with context.Reader(path,20,['NVDA'],uni,evidence_limit=100) as reader:
        with pytest.raises(context.ContextTooLarge,match='complete context requires'):
            reader.expand(['v1'])
