"""D467's proof 4 ($0): the ladder step's cases for the measured seeds, one per seed and seeded draw. Each case's article is the one a
blind reader chose (`article-choice.jsonl`, `article-choice-v5.jsonl`): the earliest article linked to the seed whose own text states the
question's subject (the code-chosen first linked article was off the subject for about half the seeds: Azure's backlog for capex, Intel's
host CPU for Rubin). opens_as and settled_by follow the standard's class and its settling material (§3 table: 核对材料), written here with
that source. Measured: the six graded seeds (q04, q05, q08, q09, q13, q18) and q07; q16 has no qualifying article among its first ten.

  python3 build_seed_cases.py > seed-cases.output.txt      # writes seed-cases.json beside this file
"""
import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = ROOT / 'poc/data/clean-e2e-2026-11-09'
ITEMS = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
CLASSES = {   # seed: (opens_as, settled_by), from the standard §3 table's reason and settling material
    'v4': ('shared_quantity', "The four hyperscalers' full-year 2026 capital-expenditure disclosures in their annual results."),
    'v13': ('shared_quantity', "The largest hyperscalers' full-year 2027 capital-expenditure disclosures in their annual results."),
    'v5': ('shared_quantity', 'Industry contract-price releases for server DRAM and HBM covering calendar 2027 and 2026.'),
    'v7': ('product_node', "NVIDIA's confirmation of first Rubin shipments."),
    'v18': ('product_node', "NVIDIA's confirmation of first Rubin Ultra shipments in Kyber NVL144 racks."),
    'v8': ('policy_stage', 'An official Chinese authorization for Chinese companies to import H200 chips.'),
    'v9': ('binding_obligation', "NVIDIA's FY2027 annual report, its note on financing commitments and capacity backstops."),
}


def chosen_articles():
    chosen = {}
    for name in ('article-choice.jsonl', 'article-choice-v5.jsonl'):
        for line in (HERE / name).read_text().splitlines():
            if line.strip().startswith('{'):
                row = json.loads(line)
                if row['question'] in CLASSES and row.get('input_id'):
                    chosen[row['question']] = row['input_id']
    missing = set(CLASSES) - set(chosen)
    if missing:
        raise SystemExit(f'no chosen article for {sorted(missing)}')
    return chosen


def main():
    items = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    items.row_factory = sqlite3.Row
    cases = []
    chosen = chosen_articles()
    for draw in ('d1', 'd2', 'd3'):
        seeds = {s['id']: s for s in json.loads((DATA / f'stage2-clean-{draw}' / 'initial.json').read_text())}
        for view_id in sorted(CLASSES, key=lambda v: int(v[1:])):
            row = items.execute('select * from items where input_id=?', (chosen[view_id],)).fetchone()
            seed = seeds[view_id]
            opens_as, settled_by = CLASSES[view_id]
            cases.append({'case': f'seeded-{draw}/{view_id}',
                          'thesis': {'id': view_id, 'description': seed['description'], 'outcome': seed['outcome'], 'period': seed['period'],
                                     'opens_as': opens_as, 'settled_by': settled_by},
                          'item': {'publication_date': row['publication_day'], 'publisher': row['publisher'], 'title': row['title'],
                                   'text': row['text']},
                          'chosen_by': f"blind reader ({chosen[view_id]})"})
            print(f"{draw} {view_id:4s} {row['publication_day']} | {row['title'][:100]}")
    if len(cases) != 3 * len(CLASSES):
        raise SystemExit(f'{len(cases)} cases, expected {3 * len(CLASSES)}: a seed with no linked article')
    (HERE / 'seed-cases.json').write_text(json.dumps(cases, ensure_ascii=False, indent=1) + '\n')
    print(f'{len(cases)} cases written to seed-cases.json')


if __name__ == '__main__':
    main()
