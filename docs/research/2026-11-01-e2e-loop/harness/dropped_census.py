"""Census of the gold core and supporting matters that the pipeline drops at placement ("no home"), read against the homes the
gold itself names ($0, stored run folders). For every gold matter of a processed article, its state in each draw of an arm
(reaches, repeat, dropped, not extracted); for the matters dropped in at least one draw: the article, the span, the article's
gold questions (must_open / may_open gists), whether one of them shares words with the matter (a home the gold names), and the
questions that were open in the ledger when the item was processed (so "no home" can be read as "no question existed" against
"a question existed and the placer said no"). The classification is one matter in one article (score_gold.same_matter); meaning
is read by a person from the list this prints.

    python3 dropped_census.py poc/data/e2e-v83-seed-d1 poc/data/e2e-v83-seed-d2 poc/data/e2e-v83-seed-d3 > dropped-census.md
"""
import collections
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REFERENCE_CONTEXT = ROOT / 'docs/research/2026-10-31-reference-context'
sys.path[:0] = [str(REFERENCE_CONTEXT), str(ROOT / 'src')]
import score_ref as sr  # noqa: E402

STOP = set('the a an of to in for and or on at by with from as is are be will its it this that these those than into over under about'.split())


def words(text):
    return {w for w in re.findall(r'[a-z0-9]+', (text or '').lower()) if w not in STOP and len(w) > 2}


def states(run):
    views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); views.row_factory = sqlite3.Row
    archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    replaced = {r[0] for r in views.execute('select old_evidence_id from replacements')}
    repeats = {r[0] for r in views.execute('select new_evidence_id from same_claims')}
    all_views = [dict(r) for r in views.execute('select view_id, question, created_seq, created_from_input from views')]
    out = {}
    for a in sr.articles:
        iid = a['input_id']
        stored = [dict(r) for r in views.execute('select evidence_id, quote, one_line, created_seq from evidence where created_from_input=?', (iid,))]
        h = views.execute('select handover_json, seq from handovers where input_id=? order by id desc limit 1', (iid,)).fetchone()
        if not h and not stored:
            continue
        r = archive.execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {iid},%',)).fetchone()
        by_id = {e['id']: e for e in (json.loads(r[0]) if r and r[0] else {}).get('evidence', [])}
        handover = json.loads(h['handover_json']) if h else {}
        dropped = {e: reason for e, reason in handover.get('dropped', [])}
        shown = [s for s in stored if s['evidence_id'] not in replaced]
        item_seq = h['seq'] if h else None
        open_then = [v['question'] for v in all_views if item_seq is None or v['created_seq'] < item_seq]
        for idx, it in enumerate(a['items']):
            if it['weight'] not in ('core', 'supporting'):
                continue
            if any(sr.sg.same_matter(it, s) for s in shown if s['evidence_id'] not in repeats):
                state = 'reaches'
            elif any(sr.sg.same_matter(it, s) for s in shown):
                state = 'repeat'
            elif any(sr.sg.same_matter(it, by_id[e]) for e in dropped if e in by_id):
                reason = next(str(dropped[e]) for e in dropped if e in by_id and sr.sg.same_matter(it, by_id[e]))
                state = 'dropped' if reason == 'no home' else f'dropped: {reason[:40]}'     # a refused quote or a merged duplicate is not a placement decision
            elif any(sr.sg.same_matter(it, e) for e in by_id.values()):
                state = 'lost later'
            else:
                state = 'not extracted'
            out[(iid, idx)] = (state, open_then)
    return out


def main(runs):
    per_run = [states(str(ROOT / p) if not p.startswith('/') else p) for p in runs]
    articles = {a['input_id']: a for a in sr.articles}
    rows = []
    for key in per_run[0]:
        seq = [pr.get(key, ('absent', []))[0] for pr in per_run]
        if not any(s.startswith('dropped') for s in seq):
            continue
        iid, idx = key
        a = articles[iid]; it = a['items'][idx]
        gold_qs = [q.get('gist', q) if isinstance(q, dict) else q for k in ('must_open', 'may_open') for q in a.get('questions', {}).get(k, [])]
        matter_words = words(it['span']) | words(it.get('rule', ''))
        named_home = [q for q in gold_qs if len(words(q) & matter_words) >= 2]
        open_then = per_run[0][key][1]
        open_match = [q for q in open_then if len(words(q) & matter_words) >= 2]
        rows.append((it['weight'], seq.count('dropped'), a['publication_day'], a['title'][:70], it['span'][:160], it.get('rule', '')[:80], gold_qs, named_home, open_match, seq))
    rows.sort(key=lambda r: (r[0] != 'core', -r[1], r[2]))
    print(f'# Gold matters dropped at placement in at least one of {len(runs)} draws: {len(rows)} '
          f'(core {sum(1 for r in rows if r[0] == "core")}, supporting {sum(1 for r in rows if r[0] == "supporting")})\n')
    summary = collections.Counter()
    for weight, n, day, title, span, rule, gold_qs, named_home, open_match, seq in rows:
        home = 'gold names a home' if named_home else ('no gold question for it' if not gold_qs else 'gold questions exist, none fits')
        summary[(weight, home, 'a matching question was open' if open_match else 'no matching question open')] += 1
        print(f'## {weight} | dropped {n}/{len(runs)} {seq} | {day} | {title}')
        print(f'- span: {span!r}')
        print(f'- gold rule: {rule}')
        print(f'- gold questions of the article: {gold_qs if gold_qs else "none"}')
        print(f'- home the gold names (word overlap): {named_home if named_home else "none"}')
        print(f'- questions open in the ledger then that share words: {open_match if open_match else "none"} ({len(open_then)} open)\n')
    print('# Summary (weight, home in the gold, home in the ledger)')
    for k, v in sorted(summary.items()):
        print(f'- {v:3d}  {k}')


if __name__ == '__main__':
    main(sys.argv[1:])
