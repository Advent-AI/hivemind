"""Alex's two hypotheses on the snapshot ($0): (1) a thesis with many pieces attracts more (cluster effect) versus the broad
question absorbing everything from day one (breadth); (2) what kind of pieces the two sinks hold. Reads only the snapshot."""
import sqlite3, json, collections, re
SNAP='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
v=sqlite3.connect(f'file:{SNAP}/views.sqlite?mode=ro', uri=True); v.row_factory=sqlite3.Row
day_of={r['seq']: r['publication_day'] for r in v.execute("select distinct sequence_no seq, publication_day from processing_steps")}
links=collections.defaultdict(list)
for r in v.execute("select l.view_id, l.evidence_id, l.seq from evidence_links l"): links[r['view_id']].append((r['seq'], r['evidence_id']))
total=sum(len(x) for x in links.values()); top=sorted(links, key=lambda k: -len(links[k]))[:6]
print('links total', total, '| top theses:', [(k, len(links[k]), f'{len(links[k])/total:.0%}') for k in top])
# (1) per-week link rate of v2 and v10 against their cumulative size
for vid in ('v2','v10'):
    byweek=collections.Counter()
    for seq,_ in links[vid]:
        d=day_of.get(seq,'?'); byweek[d[:7]+('-w'+str((int(d[8:10])-1)//7+1) if d!='?' else '')]+=1
    cum=0; row=[]
    for w in sorted(byweek): cum+=byweek[w]; row.append(f'{w}: +{byweek[w]} (cum {cum})')
    print(vid, ' | '.join(row))
# items per week for the denominator
byweek=collections.Counter()
for r in v.execute("select distinct input_id, publication_day from processing_steps"):
    d=r['publication_day']; byweek[d[:7]+'-w'+str((int(d[8:10])-1)//7+1)]+=1
print('items per week', dict(sorted(byweek.items())))
# (2) what the sinks hold: who said it, double-linked share, own-figure share
ev={r['evidence_id']: dict(r) for r in v.execute("select * from evidence")}
nlinks=collections.Counter(e for x in links.values() for _,e in x)
for vid in ('v2','v10'):
    ids=[e for _,e in links[vid]]
    who=collections.Counter(); own=0; dbl=0; tiers=collections.Counter()
    for e in ids:
        w=(ev[e]['original_who'] or '').lower(); tiers[ev[e]['tier']]+=1
        if 'nvidia' in w or 'huang' in w or 'kress' in w: own+=1
        if nlinks[e]>1: dbl+=1
    print(f"{vid}: pieces {len(ids)}, said by NVIDIA/Huang/Kress {own} ({own/len(ids):.0%}), also linked elsewhere {dbl} ({dbl/len(ids):.0%}), tiers {dict(tiers)}")
# (3) judge use of the sinks: cited share
cited=collections.Counter()
for r in v.execute("select view_id, cited_evidence_json from judgements"):
    for e in json.loads(r['cited_evidence_json'] or '[]'): cited[(r['view_id'], e)]+=1
for vid in ('v2','v10'):
    ids={e for _,e in links[vid]}; c=sum(1 for e in ids if cited[(vid,e)]); print(f'{vid}: cited by its own judgements {c}/{len(ids)} ({c/len(ids):.0%}), judgements {v.execute("select count(*) from judgements where view_id=?",(vid,)).fetchone()[0]}')
