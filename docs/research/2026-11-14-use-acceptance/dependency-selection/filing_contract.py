"""The filing contract, case by case, through the code's own rule ($0; council round 31).

For each case: the links the reading step wrote (taken from the stored raw answer, before the code's rule), the homes the code's
rule (`extraction.narrowest_links`, applied per item by `extraction.file_reading`) leaves when no hierarchy is stated between
the two questions and when one is, and the homes the existing decisions call for with the owner of that decision. The expected
homes are written here by hand from D207, D259, D360 and the frozen link rule; the script does not decide them.

  python3 filing_contract.py
"""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import extraction  # noqa: E402

FRESH = ROOT / 'poc/data/clean-lean-week-2026-11-14/week/p1/prod'
SEEDED = ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
TOTAL, SEGMENT = 'total revenue', 'data-center revenue'
BOTH, READING_STEP = [TOTAL, SEGMENT], 'the reading step'
# (label, run, article, statement id in that article's answer, the narrower question, the broader one, expected homes, the decision's words, owner)
CASES = [
    ('the company-wide outlook excluding China', FRESH, 33, 'e4', 'v4', 'v2', [TOTAL], 'D207: "company-wide figure questions take only their own figures, guidance and management statements"', READING_STEP),
    ('the quarter\'s total and segment revenue in one sentence', FRESH, 53, 'e1', 'v4', 'v2', BOTH, 'D360: "a statement giving a separate figure for each of two questions is written as two evidence items, one under each"', READING_STEP),
    ('the same, another outlet', FRESH, 92, 'e2', 'v4', 'v2', BOTH, 'D360, as above', READING_STEP),
    ('the same, a third outlet', FRESH, 115, 'e1', 'v4', 'v2', BOTH, 'D360, as above', READING_STEP),
    ('a competitor\'s segment revenue (AMD)', FRESH, 53, 'e8', 'v4', 'v2', [SEGMENT], 'D207: "one home, the narrowest question"; the frozen link rule: "compare the specific questions before a company-wide revenue or margin question and take that one only"', READING_STEP),
    ('a customer buying capacity elsewhere (Anthropic)', FRESH, 141, 'e4', 'v4', 'v2', [SEGMENT], 'as above', READING_STEP),
    ('the same customer designing its own chips', FRESH, 141, 'e5', 'v4', 'v2', [SEGMENT], 'as above', READING_STEP),
    ('seeded draw: one matter of the driver (the spot price of GPU time)', SEEDED, 127, 'e3', 'v2', 'v1', [SEGMENT], 'D207 and D259 (pricing behind the segment\'s figure): the narrowest question', READING_STEP + '; the code repairs a double link where the hierarchy is stated (D265)'),
    ('seeded draw: the quarter\'s total and segment revenue in one sentence', SEEDED, 165, 'e8', 'v2', 'v1', BOTH, 'D360, as above', READING_STEP),
]


def written_links(run, article, statement):
    """The statement as the reading step wrote it: the stored handover holds the links after the code's rule, so the raw answer is read."""
    db = sqlite3.connect(f"file:{run / 'views.sqlite'}?mode=ro", uri=True)
    archive = sqlite3.connect(f"file:{run / 'archive.sqlite'}?mode=ro", uri=True)
    input_id, handover = db.execute('select input_id, handover_json from handovers where seq = ?', (article,)).fetchone()
    filed = next(e for e in json.loads(handover)['evidence'] if e['id'] == statement)
    for (response,) in archive.execute("select response_json from model_calls where purpose = 'extract' and request_json like ? order by call_id desc", (f'%{input_id}%',)):
        content = json.loads(response)['choices'][0]['message']['content']
        for e in json.loads(content).get('evidence', []):
            if e.get('quote') == filed['quote']:
                return filed, sorted(link for link in e['links'] if link.startswith('v'))
    raise SystemExit(f'article {article} {statement}: the raw answer does not hold the filed statement')


def main():
    names = lambda links, narrower, broader: sorted({narrower: SEGMENT, broader: TOTAL}.get(link, link) for link in links)
    rows = []
    for label, run, article, statement, narrower, broader, expected, words, owner in CASES:
        filed, links = written_links(run, article, statement)
        pair = [link for link in links if link in (narrower, broader)]
        without = extraction.narrowest_links(pair, {})
        with_hierarchy = extraction.narrowest_links(pair, {narrower: [broader]})
        rows.append({'case': label, 'article': article, 'statement': filed['one_line'][:150], 'linked_by_the_reading_step': names(pair, narrower, broader),
                     'homes_with_no_stated_hierarchy': names(without, narrower, broader), 'homes_with_a_stated_hierarchy': names(with_hierarchy, narrower, broader),
                     'expected_homes': sorted(expected), 'decision': words, 'owner': owner})
    two_items = [extraction.narrowest_links([link], {'narrower': ['broader']}) for link in ('narrower', 'broader')]      # D360's own form: two items, one link each
    rows.append({'case': 'a two-figure sentence written as two items (D360\'s form; synthetic)', 'linked_by_the_reading_step': 'one item under each question',
                 'homes_with_no_stated_hierarchy': BOTH, 'homes_with_a_stated_hierarchy': sorted(SEGMENT if item == ['narrower'] else TOTAL for item in two_items), 'expected_homes': BOTH,
                 'decision': 'D360', 'owner': READING_STEP + ' writes the two items; the code\'s rule then leaves both'})
    fresh = sqlite3.connect(f"file:{FRESH / 'views.sqlite'}?mode=ro", uri=True)
    unrelated = fresh.execute("select count(*) from (select evidence_id from evidence_links where view_id in ('v12', 'v1') group by evidence_id having count(distinct view_id) = 2)").fetchone()[0]
    for row in rows:
        ok = lambda homes: 'as expected' if sorted(homes) == sorted(row['expected_homes']) else 'NOT as expected'
        print(f"{row['case'][:66]:66} | linked {row['linked_by_the_reading_step']} | no hierarchy: {row['homes_with_no_stated_hierarchy']} ({ok(row['homes_with_no_stated_hierarchy'])}) | "
              f"hierarchy: {row['homes_with_a_stated_hierarchy']} ({ok(row['homes_with_a_stated_hierarchy'])}) | expected {row['expected_homes']}")
    as_expected = lambda key: sum(1 for row in rows if sorted(row[key]) == sorted(row['expected_homes']))
    print(f"\ncases {len(rows)}: as expected with no stated hierarchy {as_expected('homes_with_no_stated_hierarchy')}, with a stated hierarchy {as_expected('homes_with_a_stated_hierarchy')}; "
          f"statements under both questions of the unrelated pair (Hugging Face commitments, financing commitments): {unrelated}")
    (Path(__file__).parent / 'filing-contract.json').write_text(json.dumps({'cases': rows, 'statements_under_both_questions_of_the_unrelated_pair': unrelated}, indent=1, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
