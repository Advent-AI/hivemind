"""$0 proof of A on stored data: every stored extraction answer of the run re-sifted with the theme theses open at its turn added to
the shown set (what a v19 request would have allowed). Counts the pieces that flip from dropped to kept and the ids they name."""
import json, re, sqlite3, sys, collections
ROOT='/Users/lchingen/hivemind-extraction-quality-2026-10-28'; sys.path.insert(0, ROOT+'/src')
from hivemind import extraction, universe
SNAP='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
v=sqlite3.connect(f'file:{SNAP}/views.sqlite?mode=ro', uri=True); v.row_factory=sqlite3.Row
a=sqlite3.connect(f'file:{SNAP}/archive.sqlite?mode=ro', uri=True)
t=sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); t.row_factory=sqlite3.Row
uni=universe.load(ROOT+'/poc/universe.json')
themes=[(r['view_id'], r['created_seq']) for r in v.execute("select view_id, created_seq from views where kind='theme' order by created_seq")]
flipped=collections.Counter(); n=0; kept_before=kept_after=0; items=0
for r in v.execute("select input_id, seq, handover_json from handovers"):
    row=a.execute("select request_json, answer_json from model_calls where purpose='extract' and request_json like ? and request_sha256 not like '%:%' order by call_id desc limit 1",(f'%[Item] id {r["input_id"]},%',)).fetchone()
    if not row: continue
    items+=1
    user=[m['content'] for m in json.loads(row[0])['messages'] if m['role']=='user'][0]
    shown=set(re.findall(r'^  - (v\d+) \(', (re.search(r'\[Existing theses of these objects\](.*?)\n\n', user, re.S) or [None,''])[1], re.M))
    gids=re.findall(r'^  - (g\d+) "', (re.search(r'\[Research groups\](.*?)\n\n', user, re.S) or [None,''])[1], re.M)
    item=dict(t.execute('select * from items where input_id=?',(r['input_id'],)).fetchone())
    answer=json.loads(row[1]); open_themes={vid for vid,seq in themes if seq<r['seq']}
    before,_,_,_=extraction.sift_with_groups(answer, item, item['text'], shown, uni, english=True, shown_group_ids=gids, version='v18')
    after,_,_,_=extraction.sift_with_groups(answer, item, item['text'], shown|open_themes, uni, english=True, shown_group_ids=gids, version='v18')
    kept_before+=len(before); kept_after+=len(after)
    for e in after:
        if e['id'] not in {x['id'] for x in before}:
            for l in e['links']:
                if l in open_themes: flipped[l]+=1
print(f'items {items}: pieces kept {kept_before} -> {kept_after} (+{kept_after-kept_before}); theme ids the flipped pieces name:', flipped.most_common(8))
