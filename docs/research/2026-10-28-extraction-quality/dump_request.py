import sqlite3, json, sys
R='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
a=sqlite3.connect(f'file:{R}/archive.sqlite?mode=ro', uri=True)
needle=sys.argv[1]
row=a.execute("select call_id, request_json, answer_json, prompt_chars, input_tokens, output_tokens from model_calls where purpose='extract' and request_json like ? limit 1",(f'%{needle}%',)).fetchone()
req=json.loads(row[1])
print('call', row[0], 'prompt_chars', row[3], 'tokens in/out', row[4], row[5])
print('request keys', list(req.keys()))
msgs=req.get('messages') or req.get('input') or []
for m in msgs:
    c=m.get('content'); c=c if isinstance(c,str) else json.dumps(c, ensure_ascii=False)
    print(f'\n===== {m.get("role")} ({len(c)} chars)')
    print(c if m.get('role')!='system' else c[:200]+' …')
for k in req:
    if k not in ('messages','input'): print('\n==', k, json.dumps(req[k], ensure_ascii=False)[:3000])
print('\n===== answer'); print(json.dumps(json.loads(row[2]), ensure_ascii=False, indent=1)[:6000])
