"""Count the explicit coverage-object field on v38 inputs and historical stage-4 requests."""
import json
import sqlite3
from pathlib import Path

DATA=Path('/Users/lchingen/hivemind/poc/data')
REPORT=Path('/Users/lchingen/hivemind/poc/reports/2026-10-27-stage34-gold')
with sqlite3.connect(f'file:{DATA}/english-v38-nvda-1w-2026-10-28/views.sqlite?mode=ro',uri=True) as views, \
     sqlite3.connect(f'file:{DATA}/items-nvda-2026-07-01-10-27.sqlite?mode=ro',uri=True) as items:
    ids=[r[0] for r in views.execute('select distinct input_id from handovers')]
    if not ids:raise ValueError('no handed-over inputs')
    objects=[]
    for ident in ids:
        row=items.execute('select object_identifiers from items where input_id=?',(ident,)).fetchone()
        if row is None:raise ValueError('missing source '+ident)
        objects.append((ident,json.loads(row[0])))
    nvda=[ident for ident,obs in objects if any(o.get('value')=='NVDA' for o in obs)]
    if 'gnews:9a13ec8bfdc32e585c1f0604' not in nvda:raise ValueError('known coverage control missing')
    print('v38 handed-over inputs',len(ids),'carrying NVDA object',len(nvda))
for arm in ('arm2','fresh2'):
    prepared=json.loads((REPORT/arm/'prepared.json').read_text())
    if not prepared:raise ValueError('no archived stage-4 cases')
    cases=list(prepared.values())
    def has_object_ids(case):
        return 'object_ids' in case['payload'] or 'object_ids' in case['payload']['source_record']
    explicit=sum(has_object_ids(c) for c in cases)
    control={'payload':{'source_record':{},'object_ids':['NVDA']}}
    if not has_object_ids(control) or has_object_ids({'payload':{'source_record':{}}}):
        raise ValueError('explicit-field controls failed')
    empty=sum(not c['payload']['catalog'] for c in cases)
    if any('source_record' not in c['payload'] for c in cases):raise ValueError('missing source record')
    print(arm,'cases',len(cases),'explicit object_ids fields',explicit,'empty catalogs',empty)
