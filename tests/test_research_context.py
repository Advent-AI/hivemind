"""Step 2 reader (D250 ported under D201): the catalog is the open questions in scope before a sequence number, the expansion is
every active piece of the chosen questions with sources, predecessors and the latest judgement, nothing from after that number."""
import os
import json
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


def test_complete_scoped_history_and_catalog_selection(tmp_path):
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
        with pytest.raises(ValueError,match='distinct IDs'):
            reader.expand(['v1','v1'])
        assert reader.expand([])['evidence']==[]


def test_complete_evidence_is_not_rejected_when_it_exceeds_one_megabyte(tmp_path):
    """D376: the complete evidence and original source survive above the retired byte limit."""
    path=tmp_path/'views.sqlite';make_ledger(path)
    db=store.open_db(str(path))
    count=1800
    def original_quote(n):
        return (f'The company disclosed supply agreement number {n}. ' +
                'The agreement covers additional capacity over several years and remains subject to the terms disclosed. '*8)
    for n in range(count):
        evidence_id=f'bulk{n}'
        store.add_evidence(db,evidence_id=evidence_id,quote=original_quote(n),one_line=f'The company disclosed supply agreement {n}.',
                           speaker='Example News',original_who='Example Company',original_day='',tier='fact',event_time='',seq=10,input_id='news:2026-08-12')
        store.add_source(db,evidence_id,'news:2026-08-12','T7','2026-08-12','paragraph 7',10)
        store.link(db,evidence_id,'v1',10)
    store.add_source(db,'bulk1799','news:2026-08-13','T7','2026-08-13','paragraph 12',11)
    db.commit();db.close()
    uni=universe.Universe({'version':'test','companies':[{'id':'NVDA'},{'id':'AMD'}],
                           'themes':[{'id':'ai-capex','name':'AI capex'}]})
    with context.Reader(path,20,['NVDA'],uni) as reader:
        result=reader.expand(['v1'])
    bulk={e['evidence_id']:e for e in result['evidence'] if e['evidence_id'].startswith('bulk')}
    originals={e['evidence_id']:e for e in result['evidence'] if e['evidence_id'].startswith('e')}
    assert len(json.dumps(result,ensure_ascii=False).encode())>1000000
    assert set(bulk)=={f'bulk{n}' for n in range(count)}
    assert set(originals)=={f'e{n}' for n in range(2,16)}
    for n in range(2,16):
        e=originals[f'e{n}']
        assert e['quote']==f'CPU benchmark caveat {n}'
        assert [(s['input_id'],s['category'],s['publication_day'],s['location']) for s in e['sources']] == [
            ('test:source','T6','2026-08-12','paragraph 1')]
    predecessor=originals['e2']['replaced'][0]['evidence']
    assert predecessor['evidence_id']=='e1' and predecessor['quote']=='CPU benchmark caveat 1'
    assert [(s['input_id'],s['category'],s['publication_day'],s['location']) for s in predecessor['sources']] == [
        ('test:source','T6','2026-08-12','paragraph 1')]
    for n in range(count):
        e=bulk[f'bulk{n}']
        assert e['quote']==original_quote(n)
        assert (e['sources'][0]['input_id'],e['sources'][0]['category'],e['sources'][0]['publication_day'],e['sources'][0]['location']) == ('news:2026-08-12','T7','2026-08-12','paragraph 7')
    assert [(s['input_id'],s['category'],s['publication_day'],s['location']) for s in bulk['bulk1799']['sources']] == [
        ('news:2026-08-12','T7','2026-08-12','paragraph 7'),('news:2026-08-13','T7','2026-08-13','paragraph 12')]


def test_complete_catalog_is_not_rejected_when_it_exceeds_150kb(tmp_path):
    """D377: large catalogs retain every scoped question and allow direct evidence expansion."""
    path=tmp_path/'views.sqlite';make_ledger(path)
    db=store.open_db(str(path))
    count=400
    def question(n):
        return (f'Will the company complete capacity plan {n}? ' +
                'The question tracks disclosed delivery plans and their commercial consequences. '*6)
    for n in range(count):
        store.create_view(db,view_id=f'v{1000+n}',object_id='NVDA',object_kind='company',kind='asset',
                          looks_at=f'Capacity plan {n}',question=question(n),due_day='',year='',rungs=[],
                          seq=10,input_id='news:2026-08-12',created_at='2026-08-12T00:00:00Z')
    db.commit();db.close()
    uni=universe.Universe({'version':'test','companies':[{'id':'NVDA'},{'id':'AMD'}],
                           'themes':[{'id':'ai-capex','name':'AI capex'}]})
    with context.Reader(path,20,['NVDA'],uni) as reader:
        catalog=reader.catalog()
        result=reader.expand(['v1'])
    assert len(json.dumps(catalog,ensure_ascii=False).encode())>150000
    questions={q['view_id']:q for q in catalog['questions']}
    assert set(questions)=={'v1','v3','v4'} | {f'v{1000+n}' for n in range(count)}
    for n in range(count):
        q=questions[f'v{1000+n}']
        assert q=={'view_id':f'v{1000+n}','object_id':'NVDA','object_kind':'company','kind':'asset',
                   'looks_at':f'Capacity plan {n}','question':question(n),'due_day':'','year':'',
                   'created_seq':10,'created_from_input':'news:2026-08-12','created_at':'2026-08-12T00:00:00Z',
                   'open':True,'rungs':[],'key':None,'dependencies':[]}
    assert questions['v1']['dependencies'][0]['resolved_to']=='v3'
    assert {e['evidence_id'] for e in result['evidence']}=={f'e{n}' for n in range(2,16)}
    with context.Reader(path,20,['NVDA'],uni) as reader:
        direct=reader.expand(['v1'])
    assert direct==result
    with context.Reader(path,1,['NVDA'],uni) as reader:
        assert reader.catalog()['questions']==[] and reader.expand([])['evidence']==[]
