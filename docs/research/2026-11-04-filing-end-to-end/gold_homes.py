"""Where the facts the judgement gold uses for each question end up, over the three frozen v108 draws: for every (gold item, question) pair of
gold-v1.json (reader B's decisive, reference, implied and against items), the ledger statement from the item's article that shares the most
figures and words with it (at least MIN_OVERLAP), and whether that statement is linked to the question's seed thesis, only to NVIDIA's two
revenue questions, only elsewhere, or to nothing; or that no such statement was written. The question's seed thesis is matched by its text
in each draw (view ids differ between draws only for article-opened questions, which have no seed and are skipped).

usage: python3 gold_homes.py [--examples]
"""
import collections
import json
import re
import sqlite3
import sys

GOLD = '/Users/lchingen/hivemind/docs/research/2026-11-01-e2e-loop/judgement-gold'
RUNS = '/Users/lchingen/hivemind/poc/data/e2e-r9-frozen-v108-2026-11-03'
WORD = re.compile(r'[a-z]{4,}|\d+(?:\.\d+)?')
MIN_OVERLAP = 5
REVENUE_SEEDS = ('v1', 'v2')     # Nvidia FY2027 total revenue and Data Center segment revenue in every draw (seeded first)


def words(text):
    return set(WORD.findall((text or '').lower()))


def main():
    gold = json.load(open(f'{GOLD}/gold-v1.json'))['entries']
    items = {i['id']: i for i in json.load(open(f'{GOLD}/packet-v1.json'))['items']}
    pairs = []
    for entry in gold:
        if entry['no_view'] or not entry.get('seed_view_id'):
            continue
        cited = set((entry.get('decisive_items') or []) + ((entry.get('reference') or {}).get('items') or [])
                    + ((entry.get('implied_outcome') or {}).get('items') or []) + ((entry.get('against') or {}).get('items') or []))
        pairs += [(entry['question_id'], entry['seed_view_id'], item_id) for item_id in sorted(cited)]
    tally = collections.Counter()
    by_question = collections.defaultdict(collections.Counter)
    examples = collections.defaultdict(list)
    for draw in ('d1', 'd2', 'd3'):
        views = sqlite3.connect(f'file:{RUNS}/{draw}/views.sqlite?mode=ro', uri=True)
        for qid, seed, item_id in pairs:
            item = items[item_id]
            target = words(item['passage'] + ' ' + json.dumps(item['meaning']))
            rows = views.execute('select e.evidence_id, e.quote, e.one_line from evidence e join evidence_sources s using(evidence_id) where s.input_id=?',
                                 (item['input_id'],)).fetchall()
            best = max(rows, key=lambda r: len(target & words(r[1] + ' ' + r[2])), default=None)
            if not best or len(target & words(best[1] + ' ' + best[2])) < MIN_OVERLAP:
                outcome = 'not written'
            else:
                links = {r[0] for r in views.execute('select view_id from evidence_links where evidence_id=?', (best[0],))}
                if seed in links:
                    outcome = 'filed under its question'
                elif not links:
                    outcome = 'written, filed nowhere'
                elif links <= set(REVENUE_SEEDS):
                    outcome = 'filed only under NVIDIA revenue (v1/v2)'
                else:
                    outcome = 'filed only under other questions'
                if outcome != 'filed under its question' and qid not in ('q01', 'q02'):
                    examples[outcome].append(f'{draw} {qid} {item_id}: {best[2][:90]} → {sorted(links)}')
            tally[outcome] += 1
            by_question[qid][outcome] += 1
    total = sum(tally.values())
    print(f'(gold item, question) pairs: {len(pairs)} per draw, {total} over three draws')
    for outcome, n in tally.most_common():
        print(f'  {outcome}: {n} ({n / total:.0%})')
    print('\nper question (three draws):')
    for qid in sorted(by_question):
        c = by_question[qid]
        print(f'  {qid}: ' + ', '.join(f'{k} {v}' for k, v in c.most_common()))
    if '--examples' in sys.argv:
        for outcome, rows in examples.items():
            print(f'\n{outcome}:')
            for r in rows[:14]:
                print('  ', r)


if __name__ == '__main__':
    main()
