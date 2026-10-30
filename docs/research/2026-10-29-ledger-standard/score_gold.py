"""Score stored extraction answers against a frozen gold file (D244). The scorer holds no rule of the standard: what is
core, supporting, optional or not kept comes only from the gold file it is given. It refuses a gold made for another
version of the standard (the page's <meta name="standard-version">), prints both sha256 values, and writes a reading
packet: a score is a lead, the traces are read every time.

Matching is a counting aid, not a judgement: an answer's statement counts as a gold entry when one quote contains the
other after normalising case, quotes and spaces, or when they share at least 60% of the shorter one's words. Every
missed core or supporting entry is listed with the answer's own statements so the reader can see whether it is a real
miss or a matching artefact.

    python3 score_gold.py --gold GOLD.json --page PAGE.html --sets week holdout --draws TAG1 TAG2 TAG3 --out DIR
"""
import argparse
import collections
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANALYST = HERE.parent / '2026-10-29-analyst-standard'
LOOP = ANALYST / 'loop-2026-10-29'
sys.path.insert(0, str(ANALYST))
import bench_v23 as bench  # noqa: E402  (the production request and the production sift)

KEEPS = ('core', 'supporting', 'optional')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def norm(text):
    text = (text or '').lower().replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('—', '-').replace('–', '-')
    return re.sub(r'\s+', ' ', text).strip()


def words(text):
    return set(re.findall(r"[a-z0-9$%.']+", norm(text)))


def same(gold_span, quote):
    a, b = norm(gold_span), norm(quote)
    if not a or not b:
        return False
    if a in b or b in a:
        return True
    x, y = words(a), words(b)
    return bool(x and y) and len(x & y) >= 0.6 * min(len(x), len(y))


STOP = {'the', 'a', 'an', 'of', 'to', 'in', 'and', 'for', 'on', 'its', 'is', 'as', 'with', 'by', 'that', 'it', 'at', 'from', 'has', 'have', 'be', 'will'}
MATTER_SHARE = 0.4   # checked 2026-10-30 on 14 read pairs: 4 of 5 same-matter pairs found, 0 of 9 different pairs matched


def same_matter(item, statement):
    """A second counting aid (the signed unit is a matter, which several sentences may express): the sentence match above,
    or at least MATTER_SHARE of the gold entry's words (span, meaning.what, meaning.how_much) appear in the statement's
    quote and one_line. Reported beside the sentence match, never instead of reading."""
    if same(item['span'], statement['quote']):
        return True
    m = item.get('meaning') or {}
    g = words(item['span'] + ' ' + str(m.get('what', '')) + ' ' + str(m.get('how_much', ''))) - STOP
    s = words(statement['quote'] + ' ' + statement.get('one_line', '')) - STOP
    return bool(g) and len(g & s) >= MATTER_SHARE * len(g)


def answers(tag):
    db = sqlite3.connect(f'file:{LOOP / tag / "answers.sqlite"}?mode=ro', uri=True)
    return {i: (c, d, cfg) for i, c, d, cfg in db.execute('select input_id, content, completed, config from answers')}


def kept(row, input_id):
    """The statements and candidates production keeps from one stored answer (the production sift), or None."""
    if row is None:
        return None
    content, completed, config_path = row
    answer = json.loads(content) if content else None
    rec = bench.sift_answer(answer, completed, input_id, config_path)
    if not rec['completed'] or rec['schema_errors']:
        return None
    return rec['sift']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gold', required=True)
    ap.add_argument('--page', required=True)
    ap.add_argument('--sets', nargs='+', required=True)
    ap.add_argument('--draws', nargs='+', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--corrections', help='a corrections file (D243 proposal 11): applied on top of the frozen gold, named in the header')
    args = ap.parse_args()
    gold = json.loads(Path(args.gold).read_text())
    page_version = int(re.search(r'<meta name="standard-version" content="(\d+)">', Path(args.page).read_text()).group(1))
    if gold.get('standard_version') != page_version:
        raise SystemExit(f'refused: the gold was made for standard version {gold.get("standard_version")}, the page is version {page_version}; re-derive the gold first')
    if args.corrections:
        corr = json.loads(Path(args.corrections).read_text())
        assert corr['gold'].endswith(Path(args.gold).name), 'corrections made for another gold'
        byid = {a['input_id']: a for a in gold['articles']}
        for c in corr['corrections']:
            a = byid[c['input_id']]
            if c['action'] == 'add_item':
                a['items'].append({'span': c['span'], 'weight': c['weight'], 'rule': c['reason']})
            elif c['action'] == 'item_to_not_kept':
                hit = [it for it in a['items'] if it['span'] == c['span']]
                assert len(hit) == 1, c['span'][:60]
                a['items'].remove(hit[0]); a['not_kept'].append({'span': c['span'], 'row': c['reason'], 'weight': 'not_kept'})
            else:
                raise SystemExit(f'unknown correction {c["action"]}')
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    header = {'gold': args.gold, 'gold_sha256': sha(args.gold), 'page': args.page, 'page_sha256': sha(args.page),
              'standard_version': page_version, 'sets': args.sets, 'draws': args.draws,
              'corrections': args.corrections, 'corrections_sha256': sha(args.corrections) if args.corrections else None}
    print(json.dumps(header, indent=1))
    articles = [a for a in gold['articles'] if a['set'] in args.sets]
    runs = {tag: answers(tag) for tag in args.draws}
    per_draw = {tag: collections.Counter() for tag in args.draws}
    item_hits = collections.defaultdict(list)          # (input_id, index) -> [hit per draw]
    matter_hits = {}
    packet = []
    for a in articles:
        iid = a['input_id']
        lines = [f'######## {iid} · {a["set"]} · {a.get("publication_day")} · {a["title"]}']
        sifted = {tag: kept(runs[tag].get(iid), iid) for tag in args.draws}
        for tag in args.draws:
            c = per_draw[tag]
            s = sifted[tag]
            if s is None:
                c['articles without a usable answer'] += 1
                continue
            c['statements kept'] += len(s['evidence'])
            c['candidates kept'] += len(s['candidates'])
            c['statements dropped by code'] += sum(1 for d in s['dropped'] if str(d[0]).startswith('e'))
        for k, it in enumerate(a['items']):
            hits, mhits = [], []
            for tag in args.draws:
                s = sifted[tag]
                hit = bool(s) and any(same(it['span'], e['quote']) for e in s['evidence'])
                mhit = bool(s) and any(same_matter(it, e) for e in s['evidence'])
                hits.append(hit); mhits.append(mhit)
                per_draw[tag][f'{it["weight"]} total'] += 1
                per_draw[tag][f'{it["weight"]} kept'] += hit
                per_draw[tag][f'{it["weight"]} matter kept'] += mhit
            matter_hits[(iid, k)] = mhits
            item_hits[(iid, k)] = hits
            marks = ''.join('K' if h else '-' for h in hits)
            lines.append(f'  [{marks}] {it["weight"]:<10} {it["span"][:160]}')
        for tag in args.draws:
            s = sifted[tag]
            if not s:
                lines.append(f'  {tag}: (no usable answer)')
                continue
            for e in s['evidence']:
                gold_hit = [it for it in a['items'] if same(it['span'], e['quote'])]
                reject_hit = [nk for nk in a['not_kept'] if same(nk['span'], e['quote'])]
                if gold_hit:
                    continue
                if reject_hit and all(nk['weight'] == 'not_kept' for nk in reject_hit):
                    per_draw[tag]['kept a not-kept sentence'] += 1
                    lines.append(f'  {tag} NOT-KEPT KEPT ({reject_hit[0].get("row", "")[:40]}): {e["quote"][:150]}')
                elif reject_hit:
                    per_draw[tag]['kept an optional sentence'] += 1
                else:
                    per_draw[tag]['extra (not in gold)'] += 1
                    lines.append(f'  {tag} EXTRA [{e["tier"]}] {e["quote"][:150]}  || {e["one_line"][:120]}')
            for q in s['candidates']:
                lines.append(f'  {tag} Q {q.get("opens_as")}/{q.get("measure")}: {q["question"][:130]}')
        qs = a.get('questions', {})
        for q in qs.get('must_open', []):
            lines.append(f'  GOLD must_open {q.get("type")}/{q.get("opens_as")}: {q.get("gist", "")[:130]}')
            for tag in args.draws:
                per_draw[tag]['must_open total'] += 1
        for q in qs.get('may_open', []):
            lines.append(f'  GOLD may_open {q.get("type")}/{q.get("opens_as")}: {q.get("gist", "")[:130]}')
        packet += lines + ['']
    summary = {'header': header, 'per_draw': {tag: dict(c) for tag, c in per_draw.items()}}
    n = len(args.draws)
    for w in ('core', 'supporting'):
        hits = [h for (iid, k), h in item_hits.items() if next(x for x in articles if x['input_id'] == iid)['items'][k]['weight'] == w]
        summary[f'{w}: kept in every draw'] = sum(all(h) for h in hits)
        summary[f'{w}: kept in at least two draws'] = sum(sum(h) >= 2 for h in hits) if n >= 2 else None
        summary[f'{w}: never kept'] = sum(not any(h) for h in hits)
        summary[f'{w}: total'] = len(hits)
        mh = [h for (iid, k), h in matter_hits.items() if next(x for x in articles if x['input_id'] == iid)['items'][k]['weight'] == w]
        summary[f'{w} (matter): kept in every draw'] = sum(all(h) for h in mh)
        summary[f'{w} (matter): kept in at least two draws'] = sum(sum(h) >= 2 for h in mh) if n >= 2 else None
        summary[f'{w} (matter): never kept'] = sum(not any(h) for h in mh)
    (out / 'scores.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1) + '\n')
    (out / 'reading-packet.md').write_text('\n'.join(packet) + '\n')
    missed = []
    for (iid, k), h in item_hits.items():
        it = next(x for x in articles if x['input_id'] == iid)['items'][k]
        if it['weight'] in ('core', 'supporting') and not all(h):
            missed.append({'input_id': iid, 'weight': it['weight'], 'hits': h, 'span': it['span'], 'rule': it.get('rule', '')})
    (out / 'misses.json').write_text(json.dumps(missed, ensure_ascii=False, indent=1) + '\n')
    hits_out = [{'input_id': iid, 'k': k, 'weight': next(x for x in articles if x['input_id'] == iid)['items'][k]['weight'], 'hits': h, 'mhits': matter_hits[(iid, k)],
                 'span': next(x for x in articles if x['input_id'] == iid)['items'][k]['span']} for (iid, k), h in item_hits.items()]
    (out / 'hits.json').write_text(json.dumps(hits_out, ensure_ascii=False, indent=1) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k != 'header'}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
