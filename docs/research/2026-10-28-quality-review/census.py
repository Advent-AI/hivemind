import sqlite3, json, random, collections, re
random.seed(7)
R='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28'
v=sqlite3.connect(f'file:{R}/views.sqlite?mode=ro', uri=True); v.row_factory=sqlite3.Row
a=sqlite3.connect(f'file:{R}/archive.sqlite?mode=ro', uri=True)
t=sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True); t.row_factory=sqlite3.Row
out=[]; P=out.append
def item(iid):
    r=t.execute("select title, publisher, publication_day, text from items where input_id=?",(iid,)).fetchone(); return r
# 1. views + how opened
P("# 1. Views: how each was opened\n")
hand={r['input_id']:json.loads(r['handover_json']) for r in v.execute("select input_id, handover_json from handovers")}
mrec=collections.defaultdict(list)
for r in v.execute("select input_id, decisions_json from match_records"):
    for c in json.loads(r['decisions_json']).get('candidates',[]): mrec[r['input_id']].append(c)
cand_out=collections.Counter(); cand_reason=collections.Counter()
for iid,cs in mrec.items():
    for c in cs: cand_out[c['outcome']]+=1; cand_reason[(c['outcome'], c['reason'].split(';')[0][:40])]+=1
P(f"candidates decided by matching: {dict(cand_out)}")
for k,n in cand_reason.most_common(12): P(f"  {n:3d} {k}")
drop=collections.Counter(); cand_dropped=0
for iid,h in hand.items():
    for d in h.get('dropped',[]):
        s=json.dumps(d); drop[re.sub(r'\b[ec]\d+\b','#',re.sub(r"'[^']*'","'…'",s))[:90]]+=1
P(f"\ncode-dropped entries in handovers (top reasons):")
for k,n in drop.most_common(15): P(f"  {n:4d} {k}")
P("\n| view | kind | opened by item (publisher, day, title) | opens_as | folds_into | lost_if_folded | match reason |\n|---|---|---|---|---|---|---|")
for r in v.execute("select * from views order by created_seq"):
    iid=r['created_from_input']; it=item(iid); h=hand.get(iid,{})
    c=next((c for c in h.get('candidates',[]) if c['question']==r['question']), None)
    m=next((m for m in mrec.get(iid,[]) if c and m['id']==c['id']), None)
    P(f"| {r['view_id']} | {r['kind']} | {it['publisher'] if it else '?'}, {it['publication_day'] if it else '?'}, {(it['title'] or '')[:60] if it else iid} | {(c or {}).get('opens_as','')} | {(c or {}).get('folds_into','')} | {((c or {}).get('lost_if_folded') or '')[:90]} | {((m or {}).get('reason') or '')[:70]} |")
P("\nAll view questions (for duplicate reading):")
for r in v.execute("select view_id, kind, question from views order by created_seq"): P(f"- {r['view_id']} [{r['kind']}] {r['question']}")
# 2. wide links
P("\n# 2. Links\n")
P("| view | linked pieces | ever cited | share |\n|---|---|---|---|")
cited=collections.defaultdict(set)
for r in v.execute("select view_id, cited_evidence_json from judgements"):
    for e in json.loads(r['cited_evidence_json'] or '[]'): cited[r['view_id']].add(e)
for r in v.execute("select view_id, count(distinct evidence_id) n from evidence_links group by 1 order by n desc limit 12"):
    P(f"| {r['view_id']} | {r['n']} | {len(cited[r['view_id']])} | {len(cited[r['view_id']])/r['n']:.0%} |")
P("\n25 random pieces linked to v2 (FY2027 total revenue) — label: bears on the question? (Y/N)")
for r in v.execute("select e.evidence_id, e.tier, e.one_line from evidence_links l join evidence e on e.evidence_id=l.evidence_id where l.view_id='v2' order by random() limit 25"):
    P(f"- {r['evidence_id']} [{r['tier']}] {r['one_line'][:200]}")
# 3. same_claims
P("\n# 3. same_claims: 30 random pairs (label: same claim? Y/N)\n")
for r in v.execute("select a.evidence_id ai, a.one_line al, b.evidence_id bi, b.one_line bl from same_claims s join evidence a on a.evidence_id=s.old_evidence_id join evidence b on b.evidence_id=s.new_evidence_id order by random() limit 30"):
    P(f"- {r['ai']}: {r['al'][:170]}\n    = {r['bi']}: {r['bl'][:170]}")
# 4. evidence fidelity
P("\n# 4. Evidence quality\n")
src={r['evidence_id']:r['input_id'] for r in v.execute("select evidence_id, input_id from evidence_sources")}
texts={}; notfound=[]; total=0
for r in v.execute("select evidence_id, quote from evidence"):
    iid=src.get(r['evidence_id']); 
    if iid not in texts:
        it=item(iid); texts[iid]=(it['text'] or '') if it else ''
    total+=1
    q=re.sub(r'\s+',' ',r['quote']).strip(); tx=re.sub(r'\s+',' ',texts[iid])
    if q and q not in tx: notfound.append(r['evidence_id'])
P(f"quote verbatim in source text: {total-len(notfound)}/{total}; not found: {len(notfound)} e.g. {notfound[:8]}")
P("\n30 random pieces with source (label: quote faithful / one_line faithful / speaker right / tier right):")
for r in v.execute("select * from evidence order by random() limit 30"):
    it=item(src.get(r['evidence_id'])); P(f"- {r['evidence_id']} [{r['tier']}] who='{r['original_who']}' day='{r['original_day']}' src={it['publisher'] if it else '?'} «{(it['title'] or '')[:50] if it else ''}»\n    quote: {r['quote'][:220]}\n    one_line: {r['one_line'][:220]}")
# 5. dropped unlinked statements per week
P("\n# 5. Statements the model wrote with no link (dropped by code)\n")
wk=collections.Counter(); kept=collections.Counter(); samples=[]
for sha, ans, created in a.execute("select request_sha256, answer_json, created_at from model_calls where purpose='extract' and answer_json<>''"):
    try: d=json.loads(ans)
    except Exception: continue
    for e in d.get('evidence',[]):
        k='linked' if e.get('links') else 'unlinked'; kept[k]+=1
        if k=='unlinked' and len(samples)<20 and random.random()<0.05: samples.append(e)
P(f"pieces in raw answers: {dict(kept)}  (unlinked share {kept['unlinked']/max(1,sum(kept.values())):.0%})")
P("20 random unlinked statements (label: would an analyst want this kept? which question?):")
for e in samples: P(f"- [{e.get('tier')}] {e.get('one_line','')[:200]}")
# 6. judgements
P("\n# 6. Judgements\n")
pairs=set()
for r in v.execute("select old_evidence_id o, new_evidence_id n from same_claims"): pairs.add((r['o'],r['n']))
both=0; ex=[]
for r in v.execute("select view_id, judgement_id, cited_evidence_json, reasons, publication_day from judgements"):
    c=set(json.loads(r['cited_evidence_json'] or '[]'))
    hit=[p for p in pairs if p[0] in c and p[1] in c]
    if hit: both+=1; ex.append((r['view_id'], r['publication_day'], hit[:2], r['reasons'][:500]))
P(f"judgements citing both members of a same-claim pair: {both} of {v.execute('select count(*) from judgements').fetchone()[0]}")
for e in ex[:4]: P(f"- {e[0]} {e[1]} {e[2]}: {e[3]}")
P("\nrung history per view (first→last):")
for r in v.execute("select view_id, group_concat(rung,'') h from (select view_id, rung from judgements order by judgement_id) group by view_id order by cast(substr(view_id,2) as int)"): P(f"- {r['view_id']}: {r['h']}")
P("\n6 latest judgements with their cited evidence:")
for r in v.execute("select * from judgements order by judgement_id desc limit 6"):
    P(f"\n## {r['view_id']} rung {r['rung']} ({r['publication_day']}) changed={r['changed']}\n{r['reasons']}")
    for e in json.loads(r['cited_evidence_json'] or '[]')[:12]:
        x=v.execute("select tier, one_line from evidence where evidence_id=?",(e,)).fetchone()
        if x: P(f"  - {e} [{x['tier']}] {x['one_line'][:160]}")
open('/private/tmp/claude-501/-Users-lchingen-hivemind/028ded68-753e-421d-9355-3e9192f660ef/scratchpad/census.md','w').write('\n'.join(out))
print('written', len(out), 'lines')
