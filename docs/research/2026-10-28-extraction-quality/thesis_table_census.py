"""The thesis list as a routing table ($0, snapshot): every thesis with my senior-analyst label (root quantity / driver event / policy
theme / fold into / junk), its links and judgements, and the links share by class. The labels are the author's (2026-10-28)."""
import sqlite3, collections, json
SNAP='/Users/lchingen/hivemind/poc/data/english-v34-nvda-3m-2026-10-28/snapshots/2026-10-28T1450'   # a snapshot (snapshot.sh), never the live run directory
v=sqlite3.connect(f'file:{SNAP}/views.sqlite?mode=ro', uri=True); v.row_factory=sqlite3.Row
LABEL={'v2':'root quantity','v10':'root quantity','v6':'root quantity','v25':'root quantity','v13':'root quantity','v30':'root quantity','v7':'segment quantity','v24':'fold→v7',
 'v4':'theme quantity','v5':'theme quantity','v16':'fold→v5','v3':'policy theme','v11':'fold→v3','v14':'fold→v3','v17':'policy theme','v49':'fold→v17','v23':'policy theme','v54':'fold→v23',
 'v27':'policy theme','v35':'fold→v27','v39':'fold→v27','v48':'fold→v27','v38':'policy theme','v45':'fold→v38','v40':'edge','v42':'fold→v40','v44':'fold→v40','v41':'edge','v46':'edge',
 'v1':'obligation event','v31':'obligation event','v32':'obligation event','v33':'fold→v31','v50':'obligation event','v52':'obligation event','v29':'obligation event','v53':'obligation event','v56':'obligation event',
 'v8':'product event','v9':'product event','v21':'product event','v20':'fold→v21','v57':'edge','v37':'edge','v15':'edge',
 'v12':'junk (size)','v26':'junk (size)','v34':'junk (size)','v47':'junk (size)','v51':'junk (size)','v55':'junk (size)','v43':'junk (size)',
 'v18':'junk (customer project)','v28':'junk (customer project)','v19':'junk (product detail)','v22':'junk (product detail)','v36':'junk (beyond horizon)'}
links=collections.Counter(r['view_id'] for r in v.execute("select view_id from evidence_links"))
judg=collections.Counter(r['view_id'] for r in v.execute("select view_id from judgements"))
views=[dict(r) for r in v.execute("select view_id, kind, question from views order by created_seq")]
byclass=collections.Counter(); nclass=collections.Counter(); total=sum(links.values())
print('| 论点 | 我的标签 | 证据链接 | 判断次数 | 问题 |\n|---|---|---|---|---|')
for x in views:
    lab=LABEL.get(x['view_id'],'(unlabelled)'); cls=lab.split('→')[0] if lab.startswith('fold') else lab.split(' (')[0]
    byclass[cls]+=links[x['view_id']]; nclass[cls]+=1
    print(f"| {x['view_id']} | {lab} | {links[x['view_id']]} | {judg[x['view_id']]} | {x['question'][:80]} |")
print('\n| 类 | 论点数 | 证据链接 | 份额 |\n|---|---|---|---|')
for cls,n in sorted(byclass.items(), key=lambda kv:-kv[1]): print(f'| {cls} | {nclass[cls]} | {n} | {n/total:.0%} |')
print('total links', total, 'theses', len(views))
