"""Pairwise agreement split by case group (round-1 cases vs new round-2 cases)."""
import json, sys
from pathlib import Path
sys.argv=[sys.argv[0]]+sys.argv[1:]
HERE=Path(__file__).resolve().parent
import importlib.util
rnd,a,b=sys.argv[1:4]
A=json.loads((HERE/f'sim-{rnd}-{a}.json').read_text()); B=json.loads((HERE/f'sim-{rnd}-{b}.json').read_text())
PRICE=('股价','市值')
def out(s):
    if not s.get('keep'):
        row=str(s.get('reject_row') or '')
        return 'optional' if any(p in row for p in PRICE) and '别家' not in row else 'reject'
    return str(s.get('weight'))
groups={'old (S,B,X)':('S','B','X'),'new (T,Y)':('T','Y')}
for g,pre in groups.items():
    ids=[s['id'] for s in A['statements'] if s['id'][0] in pre]
    n=len(ids); kd=oc=tk=tt=0
    for i in ids:
        x=next(s for s in A['statements'] if s['id']==i); y=next(s for s in B['statements'] if s['id']==i)
        ox,oy=out(x),out(y)
        kd+=((ox=='reject')==(oy=='reject')); oc+=(ox==oy)
        if ox!='reject' and oy!='reject':
            tk+=1; tt+=(str(x.get('tier'))==str(y.get('tier')))
    print(f'{g}: n={n} keep/drop {kd} ({100*kd/n:.0f}%), outcome {oc} ({100*oc/n:.0f}%), tier {tt}/{tk}')
for g,pre in {'old Q':('Q',),'new P':('P',)}.items():
    ids=[q['id'] for q in A['questions'] if q['id'][0] in pre]
    ag=sum(1 for i in ids if (lambda x,y:(x['open'],x.get('type'))==(y['open'],y.get('type')))(next(q for q in A['questions'] if q['id']==i),next(q for q in B['questions'] if q['id']==i)))
    print(f'{g}: {ag}/{len(ids)} open+type agree')
