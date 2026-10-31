"""The gold core and supporting matters the placement step dropped (no home) in at least two of three draws of one arm, each with the
statement the model wrote, the questions the placer was shown for that article and the drop reason: the list to read by hand (AGENTS §7.2,
"read what was dropped") and classify by mechanism: no question for the matter was shown, or one was shown and the placer answered none.
    python3 e2e_dropped.py run1 run2 run3 [--weight core|supporting]"""
import collections
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import score_ref as sr  # noqa: E402

weights = ('core', 'supporting')
args = sys.argv[1:]
if '--weight' in args:
    at = args.index('--weight')
    weights = (args[at + 1],)
    args = args[:at] + args[at + 2:]
runs = [str(ROOT / p) if not p.startswith('/') else p for p in args]
QUESTION_LINE = re.compile(r'^\s*- (v\d+) \(([^)]*)\): (.*)$', re.M)


def read_run(run):
    views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); views.row_factory = sqlite3.Row
    archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)

    def extraction(iid):
        r = archive.execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {iid},%',)).fetchone()
        return json.loads(r[0]) if r and r[0] else {}

    def placement(title):
        needle = json.dumps(title, ensure_ascii=False)[1:-1]
        r = archive.execute("select request_json, answer_json from model_calls where purpose='place' and request_json like ? order by call_id desc limit 1", (f'%{needle}%',)).fetchone()
        if not r:
            return [], {}
        user = json.loads(r[0])['messages'][-1]['content']
        shown = [(m.group(1), m.group(2), m.group(3)) for m in QUESTION_LINE.finditer(user)]
        answer = json.loads(r[1]) if r[1] else {}
        return shown, {p['id']: p['links'] for p in answer.get('placements', [])}

    return views, extraction, placement


dropped = collections.defaultdict(list)   # (input_id, span) -> [draw records]
per_run = [read_run(run) for run in runs]
for a in sr.articles:
    iid = a['input_id']
    for draw, (views, extraction, placement) in enumerate(per_run, 1):
        h = views.execute('select handover_json from handovers where input_id=? order by id desc limit 1', (iid,)).fetchone()
        if not h:
            continue
        by_id = {e['id']: e for e in extraction(iid).get('evidence', [])}
        reasons = {e: reason for e, reason in json.loads(h['handover_json']).get('dropped', [])}
        dropped_pieces = [dict(by_id[e], reason=reasons[e]) for e in reasons if e in by_id]
        shown, answer = placement(a['title'])
        for it in a['items']:
            if it['weight'] not in weights:
                continue
            hit = next((e for e in dropped_pieces if sr.sg.same_matter(it, e)), None)
            if hit:
                dropped[(iid, it['span'])].append({'draw': draw, 'one_line': hit.get('one_line') or hit.get('summary'), 'reason': hit['reason'],
                                                   'links': answer.get(hit['id']), 'shown': shown, 'weight': it['weight'], 'title': a['title'], 'day': a['publication_day']})
kept = {k: v for k, v in dropped.items() if len(v) >= 2}
print(f'{len(kept)} matters dropped in >=2 of {len(runs)} draws ({sum(v[0]["weight"] == "core" for v in kept.values())} core)\n')
for n, ((iid, span), recs) in enumerate(sorted(kept.items(), key=lambda kv: (kv[1][0]['weight'] != 'core', kv[1][0]['day'])), 1):
    r = recs[0]
    print(f'#{n} [{r["weight"]}] {r["day"]} {r["title"][:90]}')
    print(f'   gold: {span[:260]}')
    print(f'   model: {str(r["one_line"])[:260]}')
    print(f'   draws dropped: {[x["draw"] for x in recs]}; reasons: {sorted({x["reason"] for x in recs})}; placer links: {[x["links"] for x in recs]}')
    print(f'   shown ({len(r["shown"])}): ' + ' | '.join(f'{q} {text[:60]}' for q, _, text in r['shown']))
    print()
