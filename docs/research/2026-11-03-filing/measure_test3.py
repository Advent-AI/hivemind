"""Test 3: does a per-question "tracked by" line (written by the model from the question alone) bring other companies' figures to the
question they inform? Cases: facts the judgement gold cites, from other companies; guards: the company's own Q2 guidance and two noise
articles. Arms: stored (unchanged re-send, the control) and v4, three sends each. --dry checks the patterns on the three stored draws.

    python3 measure_test3.py --dry | --send --save test3-answers.json | --replay test3-answers.json
"""
import argparse, collections, json, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import measure_classes as mc  # noqa: E402
import variants  # noqa: E402
from hivemind import model  # noqa: E402

CASES = [
    (370, 'i233', [r'backlog|460'], {'v4', 'v13'}, 'Google Cloud backlog over $460bn'),
    (370, 'i232', [r'190'], {'v4'}, 'Google 2026 capex guided to $190bn'),
    (213, 'i140', [r'mi450'], {'v6'}, 'AMD: MI450 customer forecasts above expectations'),
    (213, 'i139', [r'broadcom', r'16(\.0)? ?billion|\$ ?16'], {'v6', 'v16'}, 'Broadcom Q3 AI revenue guided $16bn'),
    (213, 'i142', [r'micron', r'86'], {'v3', 'v5', 'v10'}, 'Micron gross margin forecast 86%'),
    (213, 'i143', [r'half', r'memory'], {'v4', 'v5', 'v13'}, 'half of data-center spend toward memory in 2027'),
    (205, 'i160', [r'41\.4'], {'v5'}, 'Micron revenue $41.46bn'),
    (205, 'i162', [r'apple'], {'v5'}, 'Apple raises prices citing memory costs'),
    (210, 'i155', [r'trainium'], {'v6', 'v16'}, 'Amazon: Trainium a multi-billion business'),
    (722, 'i300', [r'broadcom', r'meta|anthropic|openai'], {'v6', 'v16'}, 'Broadcom custom chips for Meta, Anthropic, OpenAI'),
    (397, 'i227', [r'huawei', r'half|50'], {'v6', 'v8', 'v17'}, 'Huawei about half of China AI chip market'),
    (397, 'i228', [r'jalape'], {'v16'}, 'OpenAI Jalapeno inference chip with Broadcom'),
    (311, 'i183', [r'46'], {'v6', 'v8', 'v17'}, 'Chinese buyers: 46% of AI accelerator budget to domestic'),
    (311, 'i187', [r'hygon|cambricon'], {'v17'}, 'Hygon and Cambricon accelerators evaluated'),
]
GUARD_OWN = (541, 'i281', [r'91(\.0)? ?billion'], {'v1', 'v2', 'v3', 'v6', 'v8', 'v10', 'v11', 'v17'}, 'own Q2 revenue guidance $91bn')
NOISE = [100, 198]
ARMS = ['stored', 'v4']


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dry', action='store_true'); ap.add_argument('--send', action='store_true')
    ap.add_argument('--save'); ap.add_argument('--replay'); args = ap.parse_args()
    calls = sorted({c[0] for c in CASES} | {GUARD_OWN[0]} | set(NOISE))
    got = json.load(open(args.replay)) if args.replay else {}
    if args.dry:
        for cid, item, pats, home, label in CASES + [GUARD_OWN]:
            iid, _ = mc.input_of(cid)
            row = [mc.outcome(a.get('evidence', []), pats, home)[0] for _, a in mc.stored_answers(iid)]
            print(f'{item} call {cid}: {label:<55} stored draws: {row}')
        return
    if args.send:
        send = lambda b: json.loads(model.openai_transport(mc.CFG.provider, b, timeout=300)['choices'][0]['message']['content'])
        with ThreadPoolExecutor(8) as pool:
            futs = {f'{cid}|{arm}|{n}': pool.submit(send, variants.apply(arm, mc.input_of(cid)[1])) for cid in calls for arm in ARMS for n in range(3)}
            for k, f in futs.items():
                try: got[k] = f.result()
                except Exception as exc: got[k] = {'error': str(exc)[:200], 'evidence': []}
        if args.save: json.dump(got, open(args.save, 'w'), ensure_ascii=False, indent=1)
    tot = {arm: collections.Counter() for arm in ARMS}
    for cid, item, pats, home, label in CASES + [GUARD_OWN]:
        line = []
        for arm in ARMS:
            outs = [mc.outcome(got[f'{cid}|{arm}|{n}'].get('evidence', []), pats, home) for n in range(3)]
            for o, hit in outs:
                if (cid, item) != GUARD_OWN[:2]: tot[arm][o] += 1
                for e in hit: tot[arm]['links on matched'] += len(e.get('links') or [])
            line.append(f"{arm}: " + ' '.join(f'{o[:9]:<9}' for o, _ in outs))
        print(f'{item} call {cid:<4} {label:<55} | ' + ' | '.join(line))
    articles = {a['input_id']: a for a in mc.sr.articles}
    for cid in NOISE:
        iid, _ = mc.input_of(cid); spans = [n['span'] for n in articles[iid]['not_kept'] if n.get('weight') == 'not_kept']
        line = []
        for arm in ARMS:
            cells = []
            for n in range(3):
                ev = got[f'{cid}|{arm}|{n}'].get('evidence', [])
                nk = [e for e in ev if any(mc.sr.sg.same(s, e.get('quote', '')) for s in spans)]
                cells.append(f"{sum(1 for e in nk if e.get('links'))}/{len(nk)}")
                tot[arm]['noise written'] += len(nk); tot[arm]['noise linked'] += sum(1 for e in nk if e.get('links'))
            line.append(f'{arm}: ' + ' '.join(cells))
        print(f'noise call {cid:<4} linked/written not-kept | ' + ' | '.join(line))
    all_links = {arm: [len(e.get('links') or []) for cid in calls for n in range(3) for e in got[f'{cid}|{arm}|{n}'].get('evidence', []) if e.get('links')] for arm in ARMS}
    print('\n== other-company facts, 14 cases x 3 sends')
    for arm in ARMS:
        t = tot[arm]; w = t['home'] + t['elsewhere'] + t['no link']
        print(f"{arm:<7} home {t['home']}, elsewhere {t['elsewhere']}, no link {t['no link']}, not written {t['not written']} | of written home {t['home'] / max(1, w):.0%}"
              f" | noise linked {t['noise linked']}/{t['noise written']} | links per linked statement, all ten requests {sum(all_links[arm]) / max(1, len(all_links[arm])):.2f}")


if __name__ == '__main__':
    main()
