"""Inspect old frozen gold and archived old control scores without redefining the gold.

These are quote-based historical scores, not correctness or v38 acceptance.
"""
import collections
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
GOLD = HERE.parent / '2026-10-28-extraction-quality'
EXPECTED = {
    'gold-extraction.json': 'e0db1121c7fd99e1f1e56381ebeaca950943051c35aa82fccb35a2db60568e53',
    'gold-extraction-themes.json': 'a9429a0fa947f58445d758b9a3aa7e58b6e60a7b6a69929c9170b7f1098a09f3',
}

def load_gold():
    articles = []
    for filename, expected in EXPECTED.items():
        raw = (GOLD / filename).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == expected
        articles.extend(json.loads(raw)['articles'])
    assert len(articles) == 26 and len({a['input_id'] for a in articles}) == 26
    ids = [s['id'] for a in articles for s in a['statements']]
    assert len(ids) == len(set(ids)) == 26
    return articles

def reconcile(articles, rows):
    assert len(rows) == 78
    cases = {(r['input_id'], r['sample']): r for r in rows}
    assert len(cases) == 78
    results = []
    for sample in (1, 2, 3):
        counts = collections.Counter()
        details = []
        for art in articles:
            row = cases[(art['input_id'], sample)]
            assert row['arm'] == 'control' and row['held_out'] == art['held_out']
            assert set(row['cells']) == {s['id'] for s in art['statements']}
            for s in art['statements']:
                cell = row['cells'][s['id']]
                assert cell['weight'] == s['weight']
                assert cell['cell'] in ('kept_right', 'kept_wrong_link', 'written_dropped', 'not_written')
                placeable = bool(s['bears_on_now'])
                counts['facts'] += 1
                counts['core'] += s['weight'] == 'core'
                counts['shown_home' if placeable else 'no_shown_home'] += 1
                if s['weight'] == 'core':
                    counts['core_shown_home' if placeable else 'core_no_shown_home'] += 1
                counts[('shown_home_' if placeable else 'no_shown_home_') + cell['cell']] += 1
                details.append({'id': s['id'], 'input_id': art['input_id'], 'weight': s['weight'],
                                'gold_homes': s['bears_on_now'], 'original_quote_score': cell['cell'],
                                'note': s.get('note', '')})
        assert counts['facts'] == 26 and counts['core'] == 11
        assert counts['shown_home'] == 18 and counts['no_shown_home'] == 8
        results.append({'sample': sample, 'counts': dict(counts), 'cases': details})
    return results

def main():
    articles = load_gold()
    rows = json.loads((GOLD / 'results/send-control.json').read_text())
    result = reconcile(articles, rows)
    # Check this census fails closed on a duplicate/missing historical answer.
    mutant = rows[:-1] + [rows[0]]
    try:
        reconcile(articles, mutant)
    except (AssertionError, KeyError):
        pass
    else:
        raise AssertionError('duplicate/missing answer was not detected')
    out = {'scope': 'v34 historical control, original frozen gold; quote overlap alone does not prove semantic correctness',
           'random_articles': 20, 'event_selected_development_articles': 6,
           'cross_gold_article_overlap_with_v38_week': 1,
           'controls': result, 'missing_or_duplicate_answer_control_caught': True}
    with (HERE / 'frozen-gold-reconcile-2026-10-28.json').open('x') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write('\n')
    for entry in result:
        print('sample', entry['sample'], entry['counts'])

if __name__ == '__main__':
    main()
