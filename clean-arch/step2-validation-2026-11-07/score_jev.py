"""Score Jev's comparison answers against reference v2 (no model calls).

Mapping: same_statement ↔ same_statement (merge); revision ↔ supersedes (link as a later version); every other relation
(different_fact_same_matter, same_quantity_other_party, different) ↔ different. insufficient pairs are not judged.
Wrong merge = Jev says same_statement where the reference says anything else; split by the reference relation.

Usage: score_jev.py <folder> <answers.json> [...]"""
import collections, json, sys
from pathlib import Path

EXPECTED = {'same_statement': 'same_statement', 'revision': 'supersedes', 'different_fact_same_matter': 'different',
            'same_quantity_other_party': 'different', 'different': 'different'}


def main():
    folder = Path(sys.argv[1])
    reference = {(r['earlier'], r['later']): r for r in json.loads((folder / 'reference-v2.json').read_text())}
    for name in sys.argv[2:]:
        answers = json.loads((folder / name).read_text())
        table = collections.Counter()
        for a in answers:
            r = reference.get((a['earlier'], a['later']))
            if r is None or r['relation'] == 'insufficient' or 'choice' not in a:
                continue
            table[(r['relation'], a['choice'])] += 1
        judged = sum(table.values())
        right = sum(v for (rel, ch), v in table.items() if EXPECTED[rel] == ch)
        merges = sum(v for (rel, ch), v in table.items() if ch == 'same_statement')
        wrong_merge = {rel: v for (rel, ch), v in table.items() if ch == 'same_statement' and rel != 'same_statement'}
        missed_merge = sum(v for (rel, ch), v in table.items() if rel == 'same_statement' and ch != 'same_statement')
        same_total = sum(v for (rel, ch), v in table.items() if rel == 'same_statement')
        print(f'{name}: judged {judged}; agreement {right}/{judged} = {right / judged:.1%}')
        print(f'  merges said {merges}; wrong merges {sum(wrong_merge.values())} = {sum(wrong_merge.values()) / max(1, merges):.1%} of merges, by reference relation {wrong_merge}')
        print(f'  same statements not merged {missed_merge}/{same_total}')
        for rel in EXPECTED:
            row = {ch: v for (r_, ch), v in table.items() if r_ == rel}
            if row:
                print(f'  reference {rel:27s} → {row}')


if __name__ == '__main__':
    main()
