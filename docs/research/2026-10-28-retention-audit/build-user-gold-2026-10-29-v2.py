"""Preserve frozen references and apply only Alex's 11 recorded decisions.

The result is a reviewable candidate, not a scoring interface. Its top level
intentionally has no 'articles' field, so the historical scorer cannot load it.
"""
import collections
import copy
import hashlib
import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / '2026-10-28-extraction-quality'
OUT = HERE / 'gold-user-2026-10-29-v2'
ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
HASHES = {
    'old_random': ('gold-extraction.json', 'e0db1121c7fd99e1f1e56381ebeaca950943051c35aa82fccb35a2db60568e53'),
    'old_events': ('gold-extraction-themes.json', 'a9429a0fa947f58445d758b9a3aa7e58b6e60a7b6a69929c9170b7f1098a09f3'),
    'week_candidate': ('source-reference.json', '6549a6c7ea5283d8deedfb7cd14660566d2a76fc8a6df3a64d390ce0e4e5183d'),
}
ANSWER_TEXT = {'1': 'A', '2': 'C', '3': 'A', '4': 'B', '5': 'C', '6': 'B', '7': 'A', '8': 'B',
               '9': '辅助属于供给需求', '10': '属于产品进度问题', '11': '一条吧都属于财务'}
# These are exact substrings of the relevant original sources, not scoring rules.
AMD = ("AMD estimates its EPYC 9965 (Turin) chip delivers approximately 2.4x the rack-level throughput of NVIDIA's Vera baseline "
       'in a modeled 100kW deployment, with the next-generation EPYC 6 (Venice) projected to extend that advantage to roughly 3.3x total throughput')
REVENUE_CONTEXT = "That sounds like further revenue growth ahead, and that's exactly what Wall Street analysts are projecting as well."
GOOGLE_REVENUE = '82% year-over-year revenue growth to $24.8 billion'
GOOGLE_BACKLOG = 'backlog of customer orders rose to over half a trillion dollars'
OMNIVERSE_SUPPORT = 'Organizations that want enterprise support SLAs still buy NVIDIA AI Enterprise through a reseller or CSP marketplace.'
KYBER_CUSTOMERS = 'Cloud customers reportedly rejected it because the design was awkward and the service was expensive to run.'


def require_hash(data, expected, name):
    assert hashlib.sha256(data).hexdigest() == expected, name


def load_sources():
    raw = {}
    for key, (filename, expected) in HASHES.items():
        folder = HERE if key == 'week_candidate' else OLD
        raw[key] = (folder / filename).read_bytes()
        require_hash(raw[key], expected, key)
    source = {k: json.loads(v) for k, v in raw.items()}
    assert len(source['old_random']['articles']) == 20 and len(source['old_events']['articles']) == 6
    assert len(source['week_candidate']['articles']) == 20
    assert sum(len(a['statements']) for k in ('old_random', 'old_events') for a in source[k]['articles']) == 26
    assert sum(len(a['claims']) for a in source['week_candidate']['articles']) == 33
    return source


def source_texts():
    ids = {'amd': 'gnews:55b3b854d30ecb73679c2088', 'growth': 'gnews:71df54965281684cc500960f',
           'google': 'gnews:96e365fac0c2d3275358c1ea', 'omni': 'gnews:8c9d215416b714064de3b095',
           'kyber': 'gnews:d4c5dc540392f8df39aee250'}
    conn = sqlite3.connect('file:' + ITEMS + '?mode=ro', uri=True)
    texts = {}
    for name, input_id in ids.items():
        row = conn.execute('select text from items where input_id=?', (input_id,)).fetchone()
        assert row and row[0], (name, input_id)
        texts[name] = row[0]
    conn.close()
    for name, fragment in [('amd', AMD), ('growth', REVENUE_CONTEXT), ('google', GOOGLE_REVENUE),
                           ('google', GOOGLE_BACKLOG), ('omni', OMNIVERSE_SUPPORT), ('kyber', KYBER_CUSTOMERS)]:
        assert fragment in texts[name], name
    return ids, texts


def build_candidate(source, ids):
    decisions = [
        {'question': '1', 'answer': 'A', 'decision': 'core', 'cases': ['old:a11-2', 'week:a64-2']},
        {'question': '2', 'answer': 'C', 'decision': 'exclude', 'cases': ['week:a64-3']},
        {'question': '3', 'answer': 'A', 'decision': 'core', 'cases': ['old:a03-2']},
        {'question': '4', 'answer': 'B', 'decision': 'colour', 'cases': ['old:a04-2']},
        {'question': '5', 'answer': 'C', 'decision': 'exclude_case_overview', 'cases': ['old:a08', 'week:17', 'week:21'],
         'note': 'Personal asset details remain previously excluded; no separate answer is asserted.'},
        {'question': '6', 'answer': 'B', 'decision': 'colour', 'cases': ['old:t03-1', 'old:t03-2', 'old:t03-3'],
         'interpretation': 'The grouped answer 6.B applies to all three subcases; user may correct this reading.'},
        {'question': '7', 'answer': 'A', 'decision': 'core', 'cases': ['old:a11-1', 'week:a64-1']},
        {'question': '8', 'answer': 'B', 'decision': 'colour', 'cases': ['week:a33-1']},
        {'question': '9', 'answer': ANSWER_TEXT['9'], 'decision': 'supply_demand_support', 'cases': ['week:a18-3'],
         'note': 'Direction and auxiliary role only; specific page and core/colour not decided.'},
        {'question': '10', 'answer': ANSWER_TEXT['10'], 'decision': 'product_progress', 'cases': ['week:a70-3'],
         'note': 'Specific page, identity and weight not decided; week:a71-3 is a related account to verify separately.'},
        {'question': '11', 'answer': ANSWER_TEXT['11'], 'decision': 'one_fact', 'cases': ['old:a15-3'],
         'note': 'One item: preserve revenue $24.8bn, 82% growth and backlog over $500bn together.'},
    ]
    facts = []
    for set_name in ('old_random', 'old_events'):
        for article in source[set_name]['articles']:
            for original in article['statements']:
                fact = copy.deepcopy(original)
                item = {'key': 'old:' + fact['id'], 'input_id': article['input_id'], 'original': fact,
                        'candidate_weight': fact['weight'], 'weight_basis': 'historical_model_authored',
                        'target_status': 'historical_gold_not_revalidated'}
                if fact['id'] == 'a11-2':
                    item['candidate_weight'] = 'core'; item['weight_basis'] = 'user_answer_1'
                    item['source_context'] = [{'input_id': ids['growth'], 'quote': REVENUE_CONTEXT}]
                elif fact['id'] in ('t03-1', 't03-2', 't03-3'):
                    item['candidate_weight'] = 'colour'; item['weight_basis'] = 'user_answer_6_group'
                elif fact['id'] in ('a03-2', 'a11-1'):
                    item['weight_basis'] = 'user_answer_' + ('3' if fact['id'] == 'a03-2' else '7')
                if fact['id'] == 'a15-3':
                    item['grouping'] = {'basis': 'user_answer_11', 'facts_count': 1,
                                        'required_information': ['Google Cloud Q2 revenue $24.8bn', '82% year-over-year growth',
                                                                 'customer backlog over $500bn'],
                                        'source_parts': [{'input_id': ids['google'], 'quote': GOOGLE_REVENUE},
                                                         {'input_id': ids['google'], 'quote': GOOGLE_BACKLOG}]}
                facts.append(item)
    facts.append({'key': 'old:a04-2', 'input_id': ids['amd'], 'candidate_weight': 'colour', 'weight_basis': 'user_answer_4',
                  'meaning': 'AMD estimates EPYC 9965 at 2.4x Vera rack throughput at 100kW; EPYC 6 at 3.3x is a projection.',
                  'source_parts': [{'input_id': ids['amd'], 'quote': AMD}], 'source': 'AMD estimate as reported by BofA',
                  'target_status': 'not_adjudicated', 'target_ids': None})
    weekly = [
        {'case': 'week:a64-2', 'question': '1', 'decision': 'core'},
        {'case': 'week:a64-3', 'question': '2', 'decision': 'exclude'},
        {'case': 'week:17', 'question': '5', 'decision': 'exclude_case_overview'},
        {'case': 'week:21', 'question': '5', 'decision': 'exclude_case_overview'},
        {'case': 'week:a64-1', 'question': '7', 'decision': 'core'},
        {'case': 'week:a33-1', 'question': '8', 'decision': 'colour',
         'source_addition': {'input_id': ids['omni'], 'quote': OMNIVERSE_SUPPORT}},
        {'case': 'week:a18-3', 'question': '9', 'decision': 'supply_demand_support', 'target_status': 'not_adjudicated'},
        {'case': 'week:a70-3', 'question': '10', 'decision': 'product_progress', 'target_status': 'not_adjudicated'},
        {'case': 'week:a71-3', 'question': None, 'decision': 'source_correction_only',
         'source_addition': {'input_id': ids['kyber'], 'quote': KYBER_CUSTOMERS},
         'note': 'Potential related account; original judgment and event identity not newly adjudicated.'},
    ]
    return {'format': 'user-adjudicated-reference-candidate-v1', 'ready_for_scoring': False,
            'scoring_reason': 'Original cases and target identities need semantic audit; no scorer for this format exists.',
            'original_hashes': {k: value[1] for k, value in HASHES.items()}, 'base': copy.deepcopy(source),
            'user_answers_verbatim': copy.deepcopy(ANSWER_TEXT), 'decisions': decisions,
            'original_gold_candidates': facts, 'weekly_overrides': weekly}


def validate(candidate, source, ids, texts):
    assert candidate['format'] == 'user-adjudicated-reference-candidate-v1'
    assert candidate['ready_for_scoring'] is False and 'articles' not in candidate
    assert candidate['original_hashes'] == {k: value[1] for k, value in HASHES.items()}
    assert candidate['base'] == source                         # includes every empty article, date and exclusion note
    assert candidate['user_answers_verbatim'] == ANSWER_TEXT
    assert {x['question'] for x in candidate['decisions']} == set(ANSWER_TEXT)
    assert len(candidate['decisions']) == 11
    for d in candidate['decisions']:
        assert d['answer'] == ANSWER_TEXT[d['question']]
    expected = build_candidate(source, ids)
    # Every candidate and every overlay must equal the explicitly authorised transformation.
    for field in ('scoring_reason', 'decisions', 'original_gold_candidates', 'weekly_overrides'):
        assert candidate[field] == expected[field], field
    facts = candidate['original_gold_candidates']
    assert len(facts) == 27 and len({x['key'] for x in facts}) == 27
    assert collections.Counter(x['candidate_weight'] for x in facts) == {'core': 11, 'colour': 16}
    grouped = [x for x in facts if x['weight_basis'] == 'user_answer_6_group']
    assert {x['key'] for x in grouped} == {'old:t03-1', 'old:t03-2', 'old:t03-3'}
    amd = next(x for x in facts if x['key'] == 'old:a04-2')
    assert amd['target_status'] == 'not_adjudicated' and amd['target_ids'] is None
    by_id = {v: texts[k] for k, v in ids.items()}
    for item in facts:
        for part in item.get('source_parts', []) + item.get('source_context', []):
            assert part['quote'] in by_id[part['input_id']]
        for part in item.get('grouping', {}).get('source_parts', []):
            assert part['quote'] in by_id[part['input_id']]
    for item in candidate['weekly_overrides']:
        if 'source_addition' in item:
            part = item['source_addition']; assert part['quote'] in by_id[part['input_id']]
    week = source['week_candidate']['articles']
    week_claims = {c['id'] for a in week for c in a['claims']}
    assert {'a64-1','a64-2','a64-3','a33-1','a18-3','a70-3','a71-3'} <= week_claims
    assert {a['article_no'] for a in week} >= {17, 21}
    assert sum(len(a['claims']) for a in week) == 33


def mutation_checks(candidate, source, ids, texts):
    mutants = []
    bad = copy.deepcopy(candidate); del bad['user_answers_verbatim']['1']; mutants.append(('missing answer', bad))
    bad = copy.deepcopy(candidate); del bad['base']['old_random']['articles'][0]; mutants.append(('missing empty article', bad))
    bad = copy.deepcopy(candidate); bad['base']['old_random']['articles'][0]['day'] = '2026-07-02'; mutants.append(('changed day', bad))
    bad = copy.deepcopy(candidate); bad['base']['old_random']['articles'][0]['rejected_note'] = 'changed'; mutants.append(('changed exclusion', bad))
    bad = copy.deepcopy(candidate); bad['base']['week_candidate']['articles'][0]['excluded_reason'] = 'changed'; mutants.append(('changed week exclusion', bad))
    bad = copy.deepcopy(candidate); a = next(x for x in bad['original_gold_candidates'] if x['key'] == 'old:a03-2'); b = next(x for x in bad['original_gold_candidates'] if x['key'] == 'old:a04-1'); a['candidate_weight'], b['candidate_weight'] = b['candidate_weight'], a['candidate_weight']; mutants.append(('swap weights without changing totals', bad))
    bad = copy.deepcopy(candidate); next(x for x in bad['original_gold_candidates'] if x['key'] == 'old:a15-3')['grouping']['required_information'].pop(); mutants.append(('drop one required component', bad))
    bad = copy.deepcopy(candidate); next(x for x in bad['weekly_overrides'] if x['case'] == 'week:a33-1')['source_addition']['quote'] = KYBER_CUSTOMERS; mutants.append(('wrong article evidence', bad))
    bad = copy.deepcopy(candidate); bad['ready_for_scoring'] = True; mutants.append(('premature scoring', bad))
    for name, bad in mutants:
        try: validate(bad, source, ids, texts)
        except (AssertionError, KeyError, TypeError): pass
        else: raise AssertionError('mutation not caught: ' + name)
    try:
        require_hash(b'wrong frozen file', HASHES['old_random'][1], 'old_random')
    except AssertionError: pass
    else: raise AssertionError('wrong hash not caught')
    try: candidate['articles']                              # what the old scorer requires at top level
    except KeyError: pass
    else: raise AssertionError('old scorer can misread candidate shape')
    return [name for name, _ in mutants] + ['wrong source hash', 'old scorer shape']


def main():
    source = load_sources(); ids, texts = source_texts()
    candidate = build_candidate(source, ids)
    validate(candidate, source, ids, texts)
    caught = mutation_checks(candidate, source, ids, texts)
    assert not OUT.exists(), str(OUT)
    OUT.mkdir()                                            # exclusive claim; a partial directory is never READY
    raw = json.dumps(candidate, ensure_ascii=False, indent=2) + '\n'
    with (OUT / 'reference.json').open('x', encoding='utf-8') as f: f.write(raw)
    with (OUT / 'checks.json').open('x', encoding='utf-8') as f:
        json.dump({'source_hashes': candidate['original_hashes'], 'candidate_sha256': hashlib.sha256(raw.encode()).hexdigest(),
                   'old_articles': 26, 'old_facts_before': 26, 'candidate_facts': 27,
                   'candidate_weights_tentative': {'core': 11, 'colour': 16}, 'weekly_articles': 20,
                   'weekly_claims_unchanged_in_base': 33, 'scoreable': False, 'mutants_caught': caught}, f, ensure_ascii=False, indent=2)
        f.write('\n')
    with (OUT / 'READY').open('x', encoding='utf-8') as f: f.write('reference files written and validated; not approved for scoring\n')
    print('candidate reference written; 27 historical facts; question 6 group recorded as B; scoring disabled; mutants caught:', len(caught))

if __name__ == '__main__': main()
