"""How big is the filing problem, per class (Alex 2026-11-04: "先做1，量清楚问题有多大"). Each case is one fact the frozen judgement gold
(reader B) cites for named questions, so its home is those questions; a case is found in an answer by a hand-written pattern on the
statement. Noise cases are the frozen extraction gold's not-kept spans in five articles. Observations per case: the frozen run's three
stored draws (the answer's own links, before code) and three re-sends of the draw-1 request unchanged. $0 with --dry; about $0.0013 a send.

    python3 measure_classes.py --dry          # check the patterns on the stored draws, print every match
    python3 measure_classes.py --send --save classes-answers.json
    python3 measure_classes.py --replay classes-answers.json
"""
import argparse, collections, json, re, sqlite3, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / 'docs/research/2026-10-31-reference-context'), str(ROOT / 'src')]
import score_ref as sr  # noqa: E402
from hivemind import config, model  # noqa: E402

RUN = ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03'
CFG = config.load(str(ROOT / 'poc/config/poc-v108.json'))

# class, d1 call, gold item, pattern(s) that must all match the statement, home questions, label. Home = the questions the judgement gold cites
# the fact for, plus, where the fact is that question's own quantity and the gold's list leaves it out, that question (added before the
# re-sends, after the dry run on stored data: i151 Q1 total revenue -> v1; i130 Q2 revenue guidance -> v1, v2).
CASES = [
    ('1 quarter to year', 541, 'i281', [r'91(\.0)? ?billion'], {'v1', 'v2', 'v3', 'v6', 'v8', 'v10', 'v11', 'v17'}, 'Q2 revenue guidance $91bn'),
    ('1 quarter to year', 210, 'i151', [r'81\.6'], {'v1', 'v2', 'v6', 'v20'}, 'Q1 revenue $81.6bn, data center $75.25bn'),
    ('1 quarter to year', 214, 'i129', [r'75\.2'], {'v2', 'v11', 'v20'}, 'Q1 data-center revenue $75.25bn'),
    ('1 quarter to year', 214, 'i130', [r'91(\.0)? ?billion'], {'v1', 'v2', 'v3'}, 'Q2 revenue guidance $91bn (retold)'),
    ('2 share', 370, 'i236', [r'81 ?(%|percent)'], {'v6'}, 'NVIDIA ~81% of the AI chip market'),
    ('2 share', 213, 'i137', [r'81 ?(%|percent)'], {'v6'}, 'NVIDIA ~81% of the AI chip market'),
    ('2 share', 58, 'i027', [r'\$ ?60|60 (of|out of)'], {'v6'}, '$60 of every $100 on NVIDIA GPUs'),
    ('2 share', 59, 'i057', [r'zero'], {'v6', 'v17'}, 'NVIDIA China share fallen to zero'),
    ('3 forecast', 131, 'i090', [r'82 ?(%|percent)'], {'v1', 'v13', 'v22'}, 'analysts project 82% / 41% revenue growth'),
    ('3 forecast', 102, 'i082', [r'8\.97'], {'v11'}, 'consensus EPS $8.97'),
    ('3 forecast', 102, 'i080', [r'cpu', r'20 ?billion|\$ ?20'], {'v19'}, 'nearly $20bn of CPU sales'),
    ('3 forecast', 206, 'i173', [r'(1|one) ?trillion'], {'v4', 'v13', 'v22'}, 'hyperscaler spending to top $1tn in 2027'),
    ('4 other company', 205, 'i160', [r'41\.4'], {'v5'}, 'Micron revenue $41.46bn'),
    ('4 other company', 370, 'i233', [r'460|backlog'], {'v4', 'v13'}, 'Google Cloud backlog over $460bn'),
    ('4 other company', 370, 'i232', [r'190'], {'v4'}, '2026 capex guided up to $190bn'),
    ('4 other company', 213, 'i140', [r'mi450'], {'v6'}, 'AMD: MI450 customer forecasts above expectations'),
    ('4 other company', 213, 'i139', [r'broadcom', r'16(\.0)? ?billion|\$ ?16'], {'v6', 'v16'}, 'Broadcom Q3 AI revenue guided $16bn'),
]
NOISE_CALLS = [198, 210, 214, 207, 100]


def ro(path):
    return sqlite3.connect(f'file:{path}?mode=ro', uri=True)


def input_of(call_id):
    rj = ro(RUN / 'd1/archive.sqlite').execute('select request_json from model_calls where call_id=?', (call_id,)).fetchone()[0]
    return re.search(r'\[Item\] id ([^,]+),', rj).group(1), json.loads(rj)


def stored_answers(iid):
    out = []
    for d in ('d1', 'd2', 'd3'):
        r = ro(RUN / d / 'archive.sqlite').execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {iid},%',)).fetchone()
        out.append((f'stored {d}', json.loads(r[0]) if r and r[0] else {'evidence': []}))
    return out


def matches(e, patterns):
    text = (e.get('quote', '') + ' ' + e.get('one_line', '')).lower()
    return all(re.search(p, text) for p in patterns)


def outcome(ev, patterns, home):
    hit = [e for e in ev if matches(e, patterns)]
    if not hit: return 'not written', hit
    links = set().union(*[set(e.get('links') or []) for e in hit])
    if links & home: return 'home', hit
    if links: return 'elsewhere', hit
    return 'no link', hit


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dry', action='store_true'); ap.add_argument('--send', action='store_true')
    ap.add_argument('--save'); ap.add_argument('--replay'); args = ap.parse_args()
    calls = sorted({c[1] for c in CASES} | set(NOISE_CALLS))
    resent = json.load(open(args.replay)) if args.replay else {}
    if args.send:
        with ThreadPoolExecutor(8) as pool:
            futs = {f'{cid}|{n}': pool.submit(lambda b: json.loads(model.openai_transport(CFG.provider, b, timeout=300)['choices'][0]['message']['content']), input_of(cid)[1])
                    for cid in calls for n in range(3)}
            for k, f in futs.items():
                try: resent[k] = f.result()
                except Exception as exc: resent[k] = {'error': str(exc)[:200], 'evidence': []}
        if args.save: json.dump(resent, open(args.save, 'w'), ensure_ascii=False, indent=1)
    obs = {}
    for cid in calls:
        iid, _ = input_of(cid)
        obs[cid] = stored_answers(iid) + [(f'resend {n + 1}', resent[f'{cid}|{n}']) for n in range(3) if f'{cid}|{n}' in resent]
    by_class = collections.defaultdict(collections.Counter)
    for cls, cid, item, pats, home, label in CASES:
        row = []
        for tag, ans in obs[cid]:
            o, hit = outcome(ans.get('evidence', []), pats, home)
            by_class[cls][o] += 1
            row.append(o)
            if args.dry:
                for e in hit: print(f'    {cls} {item} {tag}: {",".join(e.get("links") or []) or "-":<12} {e.get("one_line", "")[:110]}')
        print(f'{cls:<16} {item} call {cid:<4} home {sorted(home)} | {label:<45} | ' + ' '.join(f'{o[:9]:<9}' for o in row))
    articles = {a['input_id']: a for a in sr.articles}
    noise = collections.Counter()
    for cid in NOISE_CALLS:
        iid, _ = input_of(cid)
        a = articles.get(iid)
        spans = [n['span'] for n in (a or {}).get('not_kept', []) if n.get('weight') == 'not_kept']
        row = []
        for tag, ans in obs[cid]:
            nk = [e for e in ans.get('evidence', []) if any(sr.sg.same(s, e.get('quote', '')) for s in spans)]
            linked = [e for e in nk if e.get('links')]
            noise['written'] += len(nk); noise['linked'] += len(linked); noise['observations'] += 1
            row.append(f'{len(linked)}/{len(nk)}')
            if args.dry:
                for e in linked: print(f'    noise call {cid} {tag}: {",".join(e.get("links"))} {e.get("one_line", "")[:110]}')
        print(f'5 noise          call {cid:<4} not-kept spans {len(spans):>2} | linked/written per observation: ' + ' '.join(row))
    print('\n== per class, all observations')
    for cls in sorted(by_class):
        c = by_class[cls]; n = sum(c.values()); w = n - c['not written']
        print(f'{cls:<16} observations {n}: home {c["home"]}, elsewhere {c["elsewhere"]}, no link {c["no link"]}, not written {c["not written"]}'
              + (f' | of written: home {c["home"] / w:.0%}' if w else ''))
    print(f'5 noise          not-kept statements written {noise["written"]} over {noise["observations"]} observations, of them linked {noise["linked"]}')


if __name__ == '__main__':
    main()
