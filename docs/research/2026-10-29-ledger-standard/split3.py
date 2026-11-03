"""Round-3 pairwise agreement by group: repeat cases (disagreements of rounds 1-2) vs fresh cases (U, Z / R)."""
import json, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
a,b=sys.argv[1:3]
A=json.loads((HERE/f'sim-r3-{a}.json').read_text()); B=json.loads((HERE/f'sim-r3-{b}.json').read_text())
PRICE=('股价','市值')
def out(s):
    if not s.get('keep'):
        row=str(s.get('reject_row') or '')
        return 'optional' if any(p in row for p in PRICE) and '别家' not in row else 'reject'
    return str(s.get('weight'))
def fb(s): return 'fact' if s.get('tier')=='fact' else 'other'
for g,test in (('repeat',lambda i:i[0] in 'BSTXY'),('fresh',lambda i:i[0] in 'UZ')):
    ids=[s['id'] for s in A['statements'] if test(s['id'])]
    n=len(ids); kd=oc=tk=tt=tf=0; dis=[]
    for i in ids:
        x=next(s for s in A['statements'] if s['id']==i); y=next((s for s in B['statements'] if s['id']==i),None)
        if y is None: dis.append((i,'missing')); continue
        ox,oy=out(x),out(y)
        kd+=((ox=='reject')==(oy=='reject')); oc+=(ox==oy)
        if ox!='reject' and oy!='reject' and x.get('keep') and y.get('keep'):
            tk+=1; tt+=(str(x.get('tier'))==str(y.get('tier'))); tf+=(fb(x)==fb(y))
        if ox!=oy: dis.append((i,ox,oy))
    print(f'{g}: n={n} keep/drop {kd} ({100*kd/n:.0f}%), outcome {oc} ({100*oc/n:.0f}%), tier {tt}/{tk}, fact-vs-not {tf}/{tk}')
    print('   outcome differs:', dis)
for g,test in (('repeat Q',lambda i:i[0] in 'QP'),('fresh R',lambda i:i[0]=='R')):
    ids=[q['id'] for q in A['questions'] if test(q['id'])]
    d=[]
    for i in ids:
        x=next(q for q in A['questions'] if q['id']==i); y=next(q for q in B['questions'] if q['id']==i)
        if (x['open'],x.get('type'))!=(y['open'],y.get('type')): d.append((i,(x['open'],x.get('type')),(y['open'],y.get('type'))))
    print(f'{g}: {len(ids)-len(d)}/{len(ids)} agree', d)
