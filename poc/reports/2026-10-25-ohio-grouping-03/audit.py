"""D160: count the complete registered population; semantic labels are explicit human-readable assistant annotations."""
import json
import sqlite3
from pathlib import Path
OUT = Path(__file__).resolve().parent

def read(path):
    return json.loads(path.read_text())

# Read against the original articles, questions, ranges and actual evidence links.
# These are assistant annotations, not a model judge, keyword classifier or independent human gold.
ANNOTATIONS = {
 'control-1': {'O1':False,'O2':False,'O3':False,'O4':None,'O5':False,'O6':True,'annual_cash_drift':False,
  'risk_evidence':[], 'issues':['item1 e1 changes the source quote; c1 then loses its only evidence.', 'item2 e2 project cost and item3 e3 project financing link to v1 industry spending.']},
 'control-2': {'O1':True,'O2':True,'O3':True,'O4':True,'O5':False,'O6':True,'annual_cash_drift':False,
  'risk_evidence':['e5','e7'], 'issues':['item1 c5/v5 global spending is grouped with the individual Ohio project.', 'item3 e1/e2 are linked to v2 chip financing instead of v1 project guarantee.']},
 'control-3': {'O1':True,'O2':True,'O3':True,'O4':True,'O5':False,'O6':True,'annual_cash_drift':False,
  'risk_evidence':['e7','e8','e9'], 'issues':['item1 c5/v5 global spending is grouped with the individual Ohio project.']},
 'grouped-1': {'O1':True,'O2':False,'O3':False,'O4':True,'O5':True,'O6':True,'annual_cash_drift':False,
  'risk_evidence':[], 'issues':['Project total cost above $500B absent in all three answers.', 'Goldberg criticism absent from item2 raw answer despite the displayed project question.']},
 'grouped-2': {'O1':True,'O2':True,'O3':True,'O4':True,'O5':True,'O6':True,'annual_cash_drift':False,
  'risk_evidence':['e4','e5','e6'], 'issues':[]},
 'grouped-3': {'O1':True,'O2':True,'O3':True,'O4':True,'O5':True,'O6':True,'annual_cash_drift':False,
  'risk_evidence':['e4','e5','e6'], 'issues':[]},
}

def main():
    manifest, statuses, budget = (read(OUT/name) for name in ('manifest.json','status.json','budget.json'))
    assert set(statuses) == set(manifest['labels']) == set(ANNOTATIONS)
    assert all(s == 'complete' for s in statuses.values()), statuses
    assert all(a['status'] == 'complete' for a in budget['attempts'])
    output={'semantic_annotation':'assistant read of full source and artifacts; no independent human gold',
            'attempts':len(budget['attempts']), 'estimated_usd':budget['reserved_or_spent'], 'samples':{}}
    for label in manifest['labels']:
        folder=OUT/label
        db=sqlite3.connect(f'file:{folder}/views.sqlite?mode=ro',uri=True);db.row_factory=sqlite3.Row
        counts={'inputs':0,'raw_candidates':0,'kept_candidates':0,'raw_evidence':0,'kept_evidence':0,
                'memberships_checked':0,'sources_checked':0,'prior_members_shown':0,'later_candidates':0,'drops':[]}
        for n in range(1,len(manifest['item_ids'])+1):
            path=folder/f'item{n}'
            raw,handover,result,context=(read(path/f'{x}.json') for x in ('extraction','handover','result','context'))
            assert result['input_id']==manifest['item_ids'][n-1] and result['seq']==n
            counts['inputs']+=1
            for key,dat in [('raw',raw),('kept',handover)]:
                counts[key+'_candidates']+=len(dat['candidates']);counts[key+'_evidence']+=len(dat['evidence'])
            counts['later_candidates']+=len(raw['candidates']) if n>1 else 0
            counts['drops'] += [{'input':n,'id':x,'reason':why} for x,why in handover['dropped']]
            before=context['before']
            member_ids={m['view_id'] for m in before['thread_members']}
            assert member_ids <= {v['view_id'] for v in context['shown']}
            counts['prior_members_shown']+=len(member_ids)
            for c in handover['candidates']:
                if c['id'] not in result['new_views']:continue
                vid=result['new_views'][c['id']]
                assert db.execute('select question from views where view_id=?',(vid,)).fetchone()[0]==c['question']
                for ref in c['thread_ids']:
                    definition=next((g for g in raw['threads'] if g['id']==ref),None)
                    if definition:
                        rows=list(db.execute('select thread_id from threads where name=? and scope=? and seq=? and input_id=?',
                          (definition['name'],definition['scope'],n,result['input_id'])))
                        assert len(rows)==1;gid=rows[0][0]
                    else:gid=ref
                    assert db.execute('select 1 from thread_members where thread_id=? and view_id=? and seq=? and input_id=?',
                                      (gid,vid,n,result['input_id'])).fetchone()
                    counts['memberships_checked']+=1
            for eid in result['evidence_ids'].values():
                assert db.execute('select 1 from evidence_sources where evidence_id=? and input_id=? and seq=?',
                                  (eid,result['input_id'],n)).fetchone()
                counts['sources_checked']+=1
        checks=read(folder/'checks.json');assert checks['history_unchanged'] is True and checks['resend_skipped'] is True
        assert db.execute('select count(*) from thread_members').fetchone()[0]==counts['memberships_checked']
        for eid in ANNOTATIONS[label]['risk_evidence']:
            assert db.execute('select 1 from thread_members m join evidence_links l on l.view_id=m.view_id join evidence e on e.evidence_id=l.evidence_id where e.evidence_id=? and e.tier=?',(eid,'第三方看法')).fetchone()
        archive=sqlite3.connect(f'file:{folder}/calls.sqlite?mode=ro',uri=True)
        calls,usd,seconds,it,ot=archive.execute('select count(*),sum(cost_usd),sum(seconds),sum(input_tokens),sum(output_tokens) from model_calls').fetchone()
        counts.update(calls=calls,estimated_usd=usd,call_seconds=seconds,input_tokens=it,output_tokens=ot,
                      first_input_tokens=archive.execute('select input_tokens from model_calls order by call_id limit 1').fetchone()[0])
        output['samples'][label]={'counts':counts,'review':ANNOTATIONS[label]}
        db.close();archive.close()
    output['totals']={key:sum(s['counts'][key] for s in output['samples'].values()) for key in
      ['inputs','raw_candidates','kept_candidates','raw_evidence','kept_evidence','memberships_checked','sources_checked','prior_members_shown','later_candidates','call_seconds','input_tokens','output_tokens']}
    (OUT/'audit.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'attempts':output['attempts'],'estimated_usd':output['estimated_usd'],'totals':output['totals']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
