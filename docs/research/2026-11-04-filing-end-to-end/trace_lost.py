"""Where the evidence the judgement gold rests on goes, for the questions the frozen draws lose (judged wrong, never judged, never opened).

For each gold item a lost question cites (decisive, reference, implied and against items of gold-v1.json, reader B's answers, frozen), in each
frozen v108 draw: did the extraction see the item's article, which statements it wrote from that article (the raw answer, before any code
check), which of them reached the ledger, the question ids each was linked to, and whether the question's last judgement was shown it.
The statement matching an item is chosen by figures and words shared with the item's passage and meaning; every candidate is printed so the
match is read, not trusted.

usage: python3 trace_lost.py <question ids, comma-separated> [draws=d1,d2,d3]
"""
import json
import re
import sqlite3
import sys

GOLD = '/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold'
RUNS = '/Users/lchingen/hivemind/poc/data/e2e-r9-frozen-v108-2026-11-03'
WORD = re.compile(r'[a-z]{4,}|\d+(?:\.\d+)?')


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def words(text):
    return set(WORD.findall((text or '').lower()))


def main():
    question_ids = sys.argv[1].split(',')
    draws = (sys.argv[2] if len(sys.argv) > 2 else 'd1,d2,d3').split(',')
    gold = {e['question_id']: e for e in json.load(open(f'{GOLD}/gold-v1.json'))['entries']}
    items = {i['id']: i for i in json.load(open(f'{GOLD}/packet-v1.json'))['items']}
    for draw in draws:
        views, archive = ro(f'{RUNS}/{draw}/views.sqlite'), ro(f'{RUNS}/{draw}/archive.sqlite')
        questions = {r['view_id']: r['question'] for r in views.execute('select view_id, question from views')}
        answers = {}
        for request_json, answer_json in archive.execute("select request_json, answer_json from model_calls where purpose='extract' and answer_json is not null and request_sha256 not like '%:%'"):
            user = json.loads(request_json)['messages'][1]['content']
            match = re.search(r'(gnews|truenorth|sec|web)[:][^\s\]\)]+', user.split('[Item]')[-1]) if '[Item]' in user else None
            answers.setdefault(match.group(0) if match else None, []).append(json.loads(answer_json))
        for qid in question_ids:
            entry = gold[qid]
            seed = entry.get('seed_view_id')
            last = views.execute('select request_sha256, rung, publication_day from judgements where view_id=? order by seq desc limit 1', (seed,)).fetchone() if seed else None
            shown = set()
            if last:
                user = json.loads(archive.execute('select request_json from model_calls where request_sha256=?', (last['request_sha256'],)).fetchone()[0])['messages'][1]['content']
                shown = set(re.findall(r'^- (e\d+) \[', user, re.M))
            cited = list(dict.fromkeys((entry.get('decisive_items') or []) + ((entry.get('reference') or {}).get('items') or [])
                                       + ((entry.get('implied_outcome') or {}).get('items') or []) + ((entry.get('against') or {}).get('items') or [])))
            print(f'\n===== {draw} {qid} (seed {seed}: {questions.get(seed, "not in run")[:80]}) last judged {dict(last) if last else None}')
            for item_id in cited:
                item = items[item_id]
                target = words(item['passage'] + ' ' + json.dumps(item['meaning']))
                decisive = '*' if item_id in (entry.get('decisive_items') or []) else ' '
                print(f'  {decisive}{item_id} [{item["weight"]}] {item["input_id"]} {item["day"]}: {item["passage"][:150]}')
                ledger = views.execute('select e.evidence_id, e.quote, e.one_line from evidence e join evidence_sources s using(evidence_id) where s.input_id=?',
                                       (item['input_id'],)).fetchall()
                scored = sorted(((len(target & words(r['quote'] + ' ' + r['one_line'])), r) for r in ledger), key=lambda x: -x[0])
                for score, r in scored[:2]:
                    links = [l[0] for l in views.execute('select view_id from evidence_links where evidence_id=?', (r['evidence_id'],))]
                    print(f'      ledger {r["evidence_id"]} overlap {score} links {links} {"SHOWN" if r["evidence_id"] in shown else "not shown"} to {seed}: {r["one_line"][:120]}')
                if not ledger:
                    raw = answers.get(item['input_id'])
                    if raw is None:
                        print('      article never extracted in this draw (no extraction answer for its input)')
                    else:
                        written = [ev for a in raw for ev in a.get('evidence', [])]
                        best = sorted(written, key=lambda ev: -len(target & words(ev['quote'] + ' ' + ev['one_line'])))[:1]
                        print(f'      article extracted, {len(written)} statements written, none in the ledger' + (f'; closest written: links {best[0].get("links")} "{best[0]["one_line"][:110]}"' if best else ''))


if __name__ == '__main__':
    main()
