"""Pick the 20 articles of the extraction gold by rule (gold-standard.md §4): fed items of the snapshot, 2026-07-01..08-18, 800–8,000
characters, the ten already read beside their answers excluded; T7 10 / T8 5 / T6 5, spread over the seven weeks first, seed 2026;
the last two of each category in seed order are held out. Prints one line per item and writes gold-items.json."""
import sqlite3, json, random, collections, datetime
random.seed(2026)
R='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
v=sqlite3.connect(f'file:{R}/views.sqlite?mode=ro', uri=True); v.row_factory=sqlite3.Row
t=sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); t.row_factory=sqlite3.Row
READ=['gnews:1ccf9aa753675c034466adb1','gnews:afcb313dd53b5e246ed37d78','gnews:deb37e6ad15fb74d545ca368','gnews:69c31079960ffe4f9805834c','gnews:011203b517e045ffe773b1fb',
      'gnews:cc2ef6f397d2a3f0606d3c18','gnews:6841237a15246406ae5e121a','gnews:c8d3108acfbd2f30deaf6fb2','gnews:68d9d8928a5fa88ceec6cc6a','gnews:26325b9e051efe16db34f758',
      'gnews:c8c39f971721fd820aab5c1c']   # the Straits Times H200 article was read with its answer too
fed=[r['input_id'] for r in v.execute("select distinct input_id from handovers")]
pool=collections.defaultdict(lambda: collections.defaultdict(list))
for iid in fed:
    it=t.execute("select input_id, category, publication_day, publisher, title, length(text) n from items where input_id=?",(iid,)).fetchone()
    if not it or iid in READ or not (800<=it['n']<=8000) or not ('2026-07-01'<=it['publication_day']<='2026-08-18'): continue
    week=(datetime.date.fromisoformat(it['publication_day'])-datetime.date(2026,7,1)).days//7
    pool[it['category']][week].append(dict(it))
want={'T7':10,'T8':5,'T6':5}; chosen=[]
for cat,k in want.items():
    weeks=sorted(pool[cat]); picked=[]
    for w in weeks: random.shuffle(pool[cat][w])
    i=0
    while len(picked)<k:
        w=weeks[i%len(weeks)]; i+=1
        if pool[cat][w]: picked.append(pool[cat][w].pop())
    for j,it in enumerate(picked): it['held_out']= j>=k-2; chosen.append(it)
for it in chosen: print(f"{it['category']} {it['publication_day']} {'HELD' if it['held_out'] else 'dev '} {it['input_id']} {it['n']:5d} {it['publisher'][:22]:22s} {it['title'][:70]}")
json.dump(chosen, open('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-extraction-quality/gold-items.json','w'), indent=1, ensure_ascii=False)
