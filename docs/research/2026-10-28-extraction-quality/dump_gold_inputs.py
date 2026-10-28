"""For writing the gold: each article's text, the thesis ids the production request showed that day, and the theme theses open
at that point (the ledger's theme views created before the item's round). No model answer is printed (gold-standard.md §4)."""
import sqlite3, json, re, sys
R='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
v=sqlite3.connect(f'file:{R}/views.sqlite?mode=ro', uri=True); v.row_factory=sqlite3.Row
a=sqlite3.connect(f'file:{R}/archive.sqlite?mode=ro', uri=True)
t=sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); t.row_factory=sqlite3.Row
items=json.load(open(sys.argv[3] if len(sys.argv)>3 else '/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-extraction-quality/gold-items.json'))
for it in items[int(sys.argv[1]):int(sys.argv[2])]:
    iid=it['input_id']; row=t.execute("select * from items where input_id=?",(iid,)).fetchone()
    req=a.execute("select request_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1",(f'%[Item] id {iid},%',)).fetchone()
    user=[m['content'] for m in json.loads(req[0])['messages'] if m['role']=='user'][0]
    shown=re.search(r'\[Existing theses of these objects\](.*?)\n\n', user, re.S)
    seq=v.execute("select seq from handovers where input_id=? order by id desc limit 1",(iid,)).fetchone()['seq']
    themes=v.execute("select view_id, question from views where kind='theme' and created_seq<? order by created_seq",(seq,)).fetchall()
    print(f"\n######## {iid} | {row['category']} | {row['publisher']} | {row['publication_day']} | {'HELD-OUT' if it['held_out'] else 'dev'}\nTITLE: {row['title']}")
    print('SHOWN:', re.sub(r'\n\s+- ', '\n  ', re.sub(r', focus "[^"]*"', '', shown.group(1))).strip() if shown else 'none')
    print('THEMES OPEN THEN:', '; '.join(f"{x['view_id']} {x['question'][:80]}" for x in themes) or 'none')
    print('--- TEXT'); print(re.sub(r'\n{2,}', '\n', row['text']).strip())
