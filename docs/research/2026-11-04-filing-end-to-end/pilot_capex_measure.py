"""The capex-identity pilot's measure and decision (delivery-fixes.md, second fix; criteria fixed before the send, "at least two of three sends"
throughout), from the answers alone:
  A works      the motivating article's cash-flow statement (operating and free cash flow together) is kept under v12 in at least 2 of 3 clause sends;
  B fcf-only   NVIDIA statements carrying free cash flow alone land under v12 in at least 2 of 3 clause sends in 2 or more of the free-cash-flow-only
               articles: fail;
  C others     a statement about another company's cash flow or capex under v12 in at least 2 of 3 clause sends: fail (listed for reading; the
               party is read, not guessed by code);
  D moves      in an other-company capex article, a capex statement under v4 or v13 in at least 2 of 3 stored sends is under v12 in at least
               2 of 3 clause sends: fail;
  E inference  a v12 statement whose one-line states a capex amount ($, billion, million, %) its quote does not carry, in at least 2 of 3 clause
               sends: fail (D218); quarter, fiscal-year and year labels are not amounts;
  F delivery   a fact the judgement gold uses in these articles is delivered in 2 or more fewer clause sends than stored sends: fail.
Statements written per article are reported for both arms.

usage: python3 pilot_capex_measure.py answers-capex.json pilot-capex.json
"""
import collections
import json
import re
import sys

ROOT = '/Users/lchingen/hivemind'
sys.path[:0] = [f'{ROOT}/src', f'{ROOT}/docs/research/2026-11-04-filing-end-to-end']
import measure_filing as mf  # noqa: E402

CASH = re.compile(r'free cash flow|operating cash flow|cash from operations', re.I)
CAPEX = re.compile(r'capex|capital expenditure|capital spending', re.I)
AMOUNT = re.compile(r'\$\s?(\d+(?:[.,]\d+)*)|(\d+(?:[.,]\d+)*)\s?(?:billion|million|trillion|bn|%|percent)', re.I)   # amounts only: not quarter, fiscal-year or year labels


def amounts(text):
    return {(m.group(1) or m.group(2)).replace(',', '') for m in AMOUNT.finditer(text)}
ARMS = ('stored', 'capex_identity')


def text_of(s):
    return s['quote'] + ' | ' + s.get('one_line', '')


def main():
    answers, pilot = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
    sets = pilot['sets']
    items, pairs, cited_for, articles, by_passage = mf.load_gold()
    seeds = collections.defaultdict(set)
    for qid, seed, item_id in pairs:
        seeds[item_id].add(seed)
    verdict = {}
    # A
    motivating = sets['motivating'][0]
    a = {arm: sum(1 for r in answers[motivating][arm] if any('50.3' in text_of(s) and '48.6' in text_of(s) and 'v12' in s['links'] for s in r['kept'])) for arm in ARMS}
    verdict['A works'] = (a['capex_identity'] >= 2, f'cash-flow statement under v12: stored {a["stored"]}/3, clause {a["capex_identity"]}/3')
    # B
    hits = []
    for input_id in sets['nvidia_fcf_only']:
        n = sum(1 for r in answers[input_id]['capex_identity'] if any('v12' in s['links'] and CASH.search(text_of(s)) for s in r['kept']))
        if n >= 2:
            hits.append(input_id)
    verdict['B fcf-only'] = (len(hits) < 2, f'free-cash-flow-only articles with such a statement under v12 in 2+ clause sends: {len(hits)} {hits}')
    # D
    moved = []
    for input_id in sets['other_company_capex']:
        before = sum(1 for r in answers[input_id]['stored'] if any(set(s['links']) & {'v4', 'v13'} and CAPEX.search(text_of(s)) for s in r['kept']))
        after = sum(1 for r in answers[input_id]['capex_identity'] if any('v12' in s['links'] and CAPEX.search(text_of(s)) for s in r['kept']))
        if before >= 2 and after >= 2:
            moved.append(input_id)
    verdict['D moves'] = (not moved, f'hyperscaler capex moved to v12: {moved}')
    # E, C listing, F, writing
    inference_sends = []
    others_under_v12 = []
    for input_id in sets['pilot']:
        for arm in ARMS:
            for n, r in enumerate(answers[input_id][arm]):
                for s in r['kept']:
                    if 'v12' not in s['links']:
                        continue
                    stated = amounts(s['quote'])
                    claimed = amounts(s.get('one_line', ''))
                    if arm == 'capex_identity' and CAPEX.search(s.get('one_line', '')) and claimed - stated:
                        inference_sends.append((input_id, n, s['one_line'][:160]))
                    if input_id in sets['other_company_capex'] or input_id in sets['nvidia_fcf_only']:
                        others_under_v12.append((input_id, arm, n, s.get('tier'), s['quote'][:140], s.get('one_line', '')[:140]))
    by_article = collections.Counter((i, n) for i, n, _ in inference_sends)
    e_fail = [i for i in {i for i, _ in by_article} if sum(1 for (j, _) in by_article if j == i) >= 2]
    verdict['E inference'] = (not e_fail, f'articles with a v12 one-line stating a capex figure its quote lacks in 2+ clause sends: {e_fail}')
    drops = []
    for item_id in seeds:
        input_id = items[item_id]['input_id']
        if input_id not in answers:
            continue
        counts = {}
        for arm in ARMS:
            counts[arm] = 0
            for r in answers[input_id][arm]:
                carriers = mf.expressing(r['kept'], items[item_id])
                reached = set().union(*[set(c['links']) for c in carriers]) if carriers else set()
                counts[arm] += bool(reached & seeds[item_id])
        if counts['stored'] - counts['capex_identity'] >= 2:
            drops.append((item_id, counts))
    verdict['F delivery'] = (not drops, f'gold facts delivered in 2+ fewer clause sends: {drops}')
    print('statements written per article (kept + no home), stored | clause:')
    for input_id in sets['pilot']:
        w = {arm: [len(r['kept']) + len(r['homeless']) for r in answers[input_id][arm]] for arm in ARMS}
        print(f'  {input_id}: {w["stored"]} | {w["capex_identity"]}')
    print('\nstatements under v12 in the free-cash-flow-only and other-company articles (read for C):')
    for row in others_under_v12:
        print(f'  {row[0]} {row[1]} send {row[2]} [{row[3]}] quote: {row[4]} || one-line: {row[5]}')
    print('\nclause one-lines under v12 stating a capex figure the quote lacks (E):')
    for row in inference_sends:
        print(f'  {row}')
    print('\nverdict (C is decided by reading the list above):')
    for name, (ok, detail) in verdict.items():
        print(f'  {name:12} {"pass" if ok else "FAIL"}  {detail}')


if __name__ == '__main__':
    main()
