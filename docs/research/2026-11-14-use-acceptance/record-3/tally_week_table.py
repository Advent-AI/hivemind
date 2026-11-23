"""The table on the fresh week: the tally ($0; TABLE-WEEK-DESIGN.md version 2). Joins the comparers' marks to the label key and prints, per
matter, every key item with each table reader's mark (found in the key article's line, found elsewhere, misstated, not found), where the
code search found the figure in the table, how many of the four readers found it, each reader's misleading extra if both comparers give
one, and the matter's outcome by the frozen line. It judges nothing itself.

A matter on which the two comparers differ for any answer (found or not, misstated, an extra misstatement or none) is disputed: the
fresh pair's files, when they hold the matter, give the marks of all four answers; an answer on which the fresh pair differ is open.
Whether a figure was found in the key article's line or elsewhere is shown as each comparer gave it and decides nothing.

  python3 tally_week_table.py <key folder outside the repository>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')
SETS = ['codex-week-table-1', 'codex-week-table-2', 'claude-week-table-1', 'claude-week-table-2']
MATTERS = ['M01', 'M02', 'M03']


def objects(path):
    if not path.exists():
        return []
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find('{"matter"', position)
        if start == -1:
            return out
        row, position = decoder.raw_decode(text, start)
        out.append(row)


def kind(mark):
    return 'found' if mark in ('found_same_article', 'found_elsewhere') else mark


def main():
    key_folder = Path(sys.argv[1])
    key = json.loads((HERE / 'week-key.json').read_text())['key']
    in_table = json.loads((HERE / 'week-key-in-table.json').read_text())
    labels = {'first': json.loads((key_folder / 'record-3-key-week-compare-whole.json').read_text())}
    settle_path = key_folder / 'record-3-key-week-compare-settle.json'
    labels['fresh'] = json.loads(settle_path.read_text()) if settle_path.exists() else {}
    marks = {'first': {family: {row['matter']: row for row in objects(HERE / f'{family}-week-compare.jsonl')} for family in FAMILIES},
             'fresh': {family: {row['matter']: row for row in objects(HERE / f'{family}-week-compare-settle.jsonl')} for family in FAMILIES}}
    for family in FAMILIES:
        missing = [matter for matter in MATTERS if matter not in marks['first'][family]]
        if missing:
            raise SystemExit(f'{family} comparer left matters unmarked: {missing}: refused')

    def view(round_name, family, matter, item_id, name):
        label = next(l for l, n in labels[round_name][matter].items() if n == name)
        row = marks[round_name][family][matter]
        if item_id == 'extra':
            return bool((row.get('other_misstatement') or {}).get(label))
        return kind((row.get('items') or {}).get(item_id, {}).get(label))

    def raw(round_name, family, matter, item_id, name):
        label = next(l for l, n in labels[round_name][matter].items() if n == name)
        row = marks[round_name][family][matter]
        return (row.get('other_misstatement') or {}).get(label) if item_id == 'extra' else (row.get('items') or {}).get(item_id, {}).get(label)

    disputed, unsettled = [], []
    for matter in MATTERS:
        items = [item['id'] for item in key[matter]] + ['extra']
        differ = any(view('first', 'codex', matter, item_id, name) != view('first', 'claude', matter, item_id, name) for item_id in items for name in SETS)
        round_name = 'first'
        if differ:
            disputed.append(matter)
            if all(matter in marks['fresh'][family] for family in FAMILIES):
                round_name = 'fresh'
            else:
                unsettled.append(matter)
        print(f"\n{matter}: {'the first comparers agree on every mark' if not differ else 'disputed; ' + ('marks of the fresh pair' if round_name == 'fresh' else 'NOT YET RE-MARKED')}")
        if not key[matter]:
            print('  the key is empty: not exercised')
            continue
        outcome_open, not_findable, misstated_item, extra_agreed = False, [], [], []
        for item in key[matter]:
            cells, found_by = [], {'codex': 0, 'claude': 0}
            for name in SETS:
                pair = [view(round_name, family, matter, item['id'], name) for family in FAMILIES]
                detail = '/'.join(str(raw(round_name, family, matter, item['id'], name)) for family in FAMILIES)
                if pair[0] != pair[1]:
                    cells.append(f'{name}: OPEN ({detail})')
                    outcome_open = True
                else:
                    cells.append(f'{name}: {pair[0]}' + (f' ({detail})' if pair[0] == 'found' else ''))
                    if pair[0] == 'found':
                        found_by[name.split('-')[0]] += 1
                    if pair[0] == 'misstated':
                        misstated_item.append(f"{item['id']} by {name}")
            total = found_by['codex'] + found_by['claude']
            if not (found_by['codex'] and found_by['claude']):
                not_findable.append(f"{item['id']} (found by {found_by['codex']} of 2 Codex readers and {found_by['claude']} of 2 Claude readers)")
            print(f"  {item['id']} [{item['group']}] {item['value']} | {item['period']} | {item['whose']}")
            print(f"      in the table (by code): {in_table[item['id']]['where']}; found by {total} of 4 readers")
            for cell in cells:
                print(f'      {cell}')
        for name in SETS:
            pair = [view(round_name, family, matter, 'extra', name) for family in FAMILIES]
            texts = [raw(round_name, family, matter, 'extra', name) for family in FAMILIES]
            if pair[0] != pair[1]:
                outcome_open = True
                print(f'  misleading extra, {name}: OPEN (codex: {texts[0]} | claude: {texts[1]})')
            elif pair[0]:
                extra_agreed.append(name)
                print(f'  misleading extra, {name}: both comparers (codex: {texts[0]} | claude: {texts[1]})')
        if not_findable or misstated_item:
            outcome = 'NOT findable: ' + '; '.join(not_findable + [f'misstated: {m}' for m in misstated_item])
            if outcome_open:
                outcome += ' (open marks elsewhere do not change this)' if not_findable and not any('OPEN' in n for n in not_findable) else ''
        elif outcome_open:
            outcome = 'undecided (open marks)'
        elif extra_agreed:
            outcome = f'key figures found, with a misleading extra ({", ".join(extra_agreed)})'
        else:
            outcome = 'its key figures are findable'
        print(f'  OUTCOME {matter}: {outcome}')
    print(f'\ndisputed matters: {disputed or "none"}; without fresh marks yet: {unsettled or "none"}')


if __name__ == '__main__':
    main()
