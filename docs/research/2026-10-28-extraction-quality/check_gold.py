"""Checks the extraction gold against the articles (gold-standard.md §2): every span and also-span is a verbatim substring of the
stored text, 8+ characters; every bears_on id was shown (now) or open (with themes) that day; ids unique. Prints the tally and
the sha256 of the gold file."""
import json, hashlib, sqlite3, sys, collections
D='/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-extraction-quality'
t=sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True)
raw=open(sys.argv[1] if len(sys.argv)>1 else f'{D}/gold-extraction.json','rb').read(); gold=json.loads(raw)
errors=[]; ids=set(); tally=collections.Counter()
for art in gold['articles']:
    text=t.execute("select text from items where input_id=?",(art['input_id'],)).fetchone()[0]
    tally['articles']+=1; tally['empty pages']+=int(not art['statements']); tally['held-out articles']+=int(art['held_out'])
    for s in art['statements']:
        if s['id'] in ids: errors.append(f"duplicate id {s['id']}")
        ids.add(s['id']); tally['statements']+=1; tally[s['weight']]+=1
        if s['bears_on_with_themes']!=s['bears_on_now']: tally['theme-bearing statements']+=1
        if not s['bears_on_now'] and not s['bears_on_with_themes']: tally['no destination']+=1
        for sp in [s['span']]+s['also']:
            if len(sp)<8: errors.append(f"{s['id']}: span under 8 chars: {sp!r}")
            if sp not in text: errors.append(f"{s['id']}: span not verbatim in text: {sp[:60]!r}")
        for v in s['bears_on_now']:
            if v not in art['shown']: errors.append(f"{s['id']}: bears_on_now {v} was not shown")
        for v in s['bears_on_with_themes']:
            if v not in art['shown'] and v not in art['themes_open']: errors.append(f"{s['id']}: bears_on_with_themes {v} neither shown nor open")
print(dict(tally)); print('errors:', errors or 'none'); print('sha256', hashlib.sha256(raw).hexdigest())
sys.exit(1 if errors else 0)
