"""The duplicate-question trace, step 2 ($0; D520): the two reader families' rows on each pair, joined by the statement ids they name.
A fact is "listed by both" when both families name it as lacking in the same question with at least one statement id in common. It
judges nothing: it prints what each family said, where they agree, and each family's sentence on the two answers.

  python3 tally_pairs.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')
PAIRS = ('rtx', 'rubin', 'fy2028')


def rows_of(path):
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find('{"', position)
        if start == -1:
            return out
        try:
            row, position = decoder.raw_decode(text, start)
            out.append(row)
        except json.JSONDecodeError:
            position = start + 1


def main():
    for pair in PAIRS:
        rows = {family: rows_of(HERE / f'{family}-pair-{pair}.jsonl') for family in FAMILIES}
        for family in FAMILIES:
            if not any(row.get('done') for row in rows[family]):
                raise SystemExit(f'{family} {pair}: no completion line: refused')
        facts = {family: [row for row in rows[family] if 'lacking' in row] for family in FAMILIES}
        print(f'\n===== {pair}')
        for family in FAMILIES:
            bearing = [row for row in facts[family] if str(row.get('bears')).lower().startswith('yes')]
            print(f"  {family}: {len(facts[family])} facts listed (lacking in P {sum(1 for r in facts[family] if r['lacking'] == 'P')}, in Q {sum(1 for r in facts[family] if r['lacking'] == 'Q')}); "
                  f"said to bear {len(bearing)} (P {sum(1 for r in bearing if r['lacking'] == 'P')}, Q {sum(1 for r in bearing if r['lacking'] == 'Q')})")
        shared = []
        for row in facts['codex']:
            ids = set(row.get('ids_in_the_other_request') or [])
            match = next((other for other in facts['claude'] if other['lacking'] == row['lacking'] and ids & set(other.get('ids_in_the_other_request') or [])), None)
            if match:
                shared.append((row, match))
        both_bear = [(a, b) for a, b in shared if str(a.get('bears')).lower().startswith('yes') and str(b.get('bears')).lower().startswith('yes')]
        print(f'  listed by both families (same question lacking it, a statement id in common): {len(shared)}; both say it bears: {len(both_bear)}')
        for a, b in both_bear:
            print(f"    lacking in {a['lacking']} {sorted(set(a.get('ids_in_the_other_request') or []) | set(b.get('ids_in_the_other_request') or []))}: {str(a['fact'])[:230]}")
            print(f"        codex: {str(a.get('why'))[:200]}")
            print(f"        claude: {str(b.get('why'))[:200]}")
        for a, b in shared:
            if (a, b) not in both_bear:
                print(f"    listed by both, not both bearing (codex {a.get('bears')}, claude {b.get('bears')}), lacking in {a['lacking']} {a.get('ids_in_the_other_request')}: {str(a['fact'])[:150]}")
        for family in FAMILIES:
            answer = next((row['answers'] for row in rows[family] if 'answers' in row), None)
            print(f'  {family} on the two answers: {answer}')


if __name__ == '__main__':
    main()
