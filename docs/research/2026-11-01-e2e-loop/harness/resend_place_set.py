"""Cheapest proof of a placement change over its class and its guard (AGENTS §1 step 4, §6 "check before the send"): from one stored
run, take every gold core or supporting matter the placer left with no home (no statement of that matter reached a question in that
run) and the dropped statements that express it, plus a seeded sample of gold not-kept statements also left unfiled (the guard: a wider
rule must not file noise); re-send each stored placement request n times as stored and n times changed, eight sends at a time, and
print the links the statement gets, one statement at a time as its sends complete. The change is a replacement system prompt (a file)
and, optionally, edits of the code-written takes lines in the user message (a period phrase, or any old -> new text), so a code change
can be tried before it is written. Sends the bytes production would send, with only the named edits.

    python3 resend_place_set.py <run folder> <config json> <new system prompt file | -> <n> [--takes-period] [--takes-sub OLD NEW ...]
                                [--negatives 12] [--match TEXT ...]

--match keeps only the positives whose gold span or article title contains one of the texts (case-insensitive); the guard is unaffected.
A statement whose matter already reached a question through another statement of the same article is not a positive: filing it again
would be a repeat, not a recovery (found 2026-11-01: the 40%-word matter match had put such statements in the class).
"""
import argparse
import json
import random
import re
import sqlite3
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / 'docs/research/2026-10-31-reference-context'), str(ROOT / 'src')]
import score_ref as sr  # noqa: E402
from hivemind import config, model  # noqa: E402

PERIOD = re.compile(r'over (\d{4}-\d{2}-\d{2}\.\.\d{4}-\d{2}-\d{2})')
SENDERS = 8


def stored_place_request(archive, title):
    row = archive.execute("select request_json from model_calls where purpose='place' and request_json like ? order by call_id desc limit 1",
                          (f'%{json.dumps(title, ensure_ascii=False)[1:-1]}%',)).fetchone()
    return json.loads(row[0]) if row else None


def unreached_matters(article, reached_statements):
    """The gold core and supporting items of one article that no stored (reached) statement expresses."""
    return [i for i in article['items'] if i['weight'] in ('core', 'supporting')
            and not any(sr.sg.same_matter(i, s) for s in reached_statements)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('run'); ap.add_argument('config'); ap.add_argument('system_file'); ap.add_argument('n', type=int)
    ap.add_argument('--takes-period', action='store_true', help="append ' (stated for that period or with no period)' to every takes period")
    ap.add_argument('--takes-sub', nargs=2, action='append', default=[], metavar=('OLD', 'NEW'), help='replace OLD with NEW in the user message (a takes-line edit)')
    ap.add_argument('--negatives', type=int, default=12)
    ap.add_argument('--match', nargs='*', default=[], help='keep only positives whose gold span or article title contains one of these')
    args = ap.parse_args()
    cfg = config.load(args.config)
    views = sqlite3.connect(f'file:{args.run}/views.sqlite?mode=ro', uri=True)
    archive = sqlite3.connect(f'file:{args.run}/archive.sqlite?mode=ro', uri=True)
    new_system = None if args.system_file == '-' else Path(args.system_file).read_text().strip()
    wanted = [m.lower() for m in args.match]

    def answer(iid):
        r = archive.execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {iid},%',)).fetchone()
        return json.loads(r[0]) if r and r[0] else {}

    positives, negatives, matters_in_class = [], [], 0
    for a in sr.articles:
        h = views.execute('select handover_json from handovers where input_id=? order by id desc limit 1', (a['input_id'],)).fetchone()
        if not h:
            continue
        dropped = [e for e, reason in json.loads(h[0]).get('dropped', []) if reason == 'no home']
        if not dropped:
            continue
        reached = [{'quote': q, 'one_line': o} for q, o in views.execute('select quote, one_line from evidence where created_from_input=?', (a['input_id'],))]
        unreached = unreached_matters(a, reached)
        matters_in_class += len(unreached)
        by_id = {e['id']: e for e in answer(a['input_id']).get('evidence', [])}
        for sid in dropped:
            if sid not in by_id:
                continue
            e = by_id[sid]
            item = next((i for i in unreached if sr.sg.same_matter(i, e)), None)
            if item is not None:
                if not wanted or any(w in item['span'].lower() or w in a['title'].lower() for w in wanted):
                    positives.append((a, sid, item['weight'], item['span']))
            elif any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'not_kept'):
                negatives.append((a, sid, 'not_kept', e['quote']))
    random.Random(20261101).shuffle(negatives)
    negatives = negatives[:args.negatives]
    core_n = sum(1 for p in positives if p[2] == 'core'); supp_n = sum(1 for p in positives if p[2] == 'supporting')
    print(f'class: {matters_in_class} gold core/supporting matters with no statement reaching a question in this run; '
          f'{core_n} core + {supp_n} supporting dropped statements express them' + (f' (after --match {args.match})' if wanted else '')
          + f'; guard: {len(negatives)} gold not-kept statements also left with no home; edits: system prompt {"replaced" if new_system else "as stored"}, '
          f'takes-period {args.takes_period}, takes-sub {args.takes_sub}', flush=True)

    def edited_request(body):
        edited = json.loads(json.dumps(body))
        if new_system:
            edited['messages'][0]['content'] = new_system
        user = edited['messages'][-1]['content']
        if args.takes_period:
            user = PERIOD.sub(r'over \1 (stated for that period or with no period)', user)
        for old, new in args.takes_sub:
            user = user.replace(old, new)
        edited['messages'][-1]['content'] = user
        return edited

    def send(body, sid):
        answer_json = json.loads(model.openai_transport(cfg.provider, body)['choices'][0]['message']['content'])
        return next((p['links'] for p in answer_json['placements'] if p['id'] == sid), None)

    summary = {'core': [0, 0], 'supporting': [0, 0], 'not_kept': [0, 0]}
    with ThreadPoolExecutor(SENDERS) as pool:
        futures = []   # per statement: (row, [control futures], [edited futures])
        for a, sid, cls, span in positives + negatives:
            body = stored_place_request(archive, a['title'])
            if body is None:
                futures.append(((a, sid, cls, span), None, None)); continue
            edited = edited_request(body)
            futures.append(((a, sid, cls, span),
                            [pool.submit(send, json.loads(json.dumps(body)), sid) for _ in range(args.n)],
                            [pool.submit(send, json.loads(json.dumps(edited)), sid) for _ in range(args.n)]))
        for (a, sid, cls, span), control_futures, edited_futures in futures:
            if control_futures is None:
                print(f'- {cls} | {a["publication_day"]} | no stored placement request for {a["title"][:50]!r}', flush=True); continue
            control = [f.result() for f in control_futures]; edited = [f.result() for f in edited_futures]
            filed_control = sum(1 for l in control if l); filed_edited = sum(1 for l in edited if l)
            summary[cls][0] += filed_control >= (args.n + 1) // 2; summary[cls][1] += filed_edited >= (args.n + 1) // 2
            print(f'- {cls} | {a["publication_day"]} | {sid} | {span[:80]!r}\n    control {control} -> edited {edited}', flush=True)
    print('\nfiled in at least half the sends, control -> edited:', {k: f'{v[0]} -> {v[1]}' for k, v in summary.items()},
          f'(of core {core_n}, supporting {supp_n}, not-kept {len(negatives)})', flush=True)


if __name__ == '__main__':
    main()
