"""Tests of the comparison's verdict (verdict-rule.json; D665, D672). Each names the rule it proves. Synthetic readings only.

Run: python3 -m pytest docs/research/2026-11-17-product-comparison/stage0/test_score_comparison.py
"""
import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_comparison as sc  # noqa: E402

DRAWS = [f'{s}-{d}' for s in ('new', 'old') for d in (1, 2, 3)]


def base(n=20, new_served=0, old_served=0, guard_cards=12):
    """N matters; the first `new_served` served by the new system in all draws, the next `old_served` by the old one; every draw has
    `guard_cards` guardrail cards of each type, all supported and worth (no breach)."""
    matters = [{'matter': f'M{i:02d}', 'company_figure': False} for i in range(1, n + 1)]
    mapping = {d: {} for d in DRAWS}
    cards = {d: {} for d in DRAWS}
    for i, m in enumerate(matters):
        for d in DRAWS:
            system = d.split('-')[0]
            served = (system == 'new' and i < new_served) or (system == 'old' and new_served <= i < new_served + old_served)
            if served:
                q = f'{d}-q{i}'
                mapping[d][m['matter']] = [{'question': q, 'covers': True}]
                cards[d][q] = {'worth': 'worth', 'answer': 'supported', 'type': 'figure', 'guardrail': False, 'covering': True}
    for d in DRAWS:
        for t in ('figure', 'yes/no'):
            for j in range(guard_cards):
                cards[d][f'{d}-g-{t}-{j}'] = {'worth': 'worth', 'answer': 'supported', 'type': t, 'guardrail': True, 'covering': False}
    return {'matters': matters, 'mapping': mapping, 'cards': cards,
            'distinct': {d: {'ids': 40, 'duplicates_both': 0, 'duplicates_split': 0} for d in DRAWS},
            'controls': {'plants': ['unsupported'] * 6, 'supported': ['supported'] * 4, 'repeats_same': [True] * 3},
            'inputs': {}}


def seal(r):
    """The files a real reading is made from, written for these readings (temporary folder): the matter list (in place of the frozen one),
    a passing eligibility check, the mapping file and the deck key, with the fingerprints mark_cards.readings records."""
    folder = Path(tempfile.mkdtemp())
    files = {'matters': {'matters': r['matters']}, 'eligibility': {'eligible': True}}
    for name, data in files.items():
        (folder / f'{name}.json').write_text(json.dumps(data))
    sc.MATTERS = folder / 'matters.json'
    eligibility_sha = hashlib.sha256((folder / 'eligibility.json').read_bytes()).hexdigest()
    (folder / 'mapping.json').write_text(json.dumps({'mapping': r['mapping'], 'distinct': r['distinct'], 'eligibility_sha256': eligibility_sha}))
    key = {f'C{n}': {'draw': d, 'question': q, 'role': 'product', **{f: r['cards'][d][q][f] for f in ('guardrail', 'covering', 'type')}}
           for n, (d, q) in enumerate((d, q) for d in r['cards'] for q in r['cards'][d])}
    (folder / 'deck-key.json').write_text(json.dumps(key))
    sha = lambda name: hashlib.sha256((folder / name).read_bytes()).hexdigest()
    r['inputs'] = {'matters_sha256': sha('matters.json'), 'mapping_path': str(folder / 'mapping.json'), 'mapping_sha256': sha('mapping.json'),
                   'eligibility_path': str(folder / 'eligibility.json'), 'eligibility_sha256': eligibility_sha,
                   'deck_key_path': str(folder / 'deck-key.json'), 'deck_key_sha256': sha('deck-key.json')}
    return r


def verdict(r):
    """The scorer's entry point on readings sealed as a real reading is."""
    return sc.verdict(seal(r))


def test_a_plant_without_an_explicit_rejection_makes_the_reading_invalid():
    """Rule: invalid when a planted wrong answer is not explicitly rejected (a split or 'cannot tell' is not a rejection)."""
    r = base(new_served=10)
    r['controls']['plants'][0] = {'split': ['supported', 'unsupported']}
    assert verdict(r)['verdict'] == 'invalid'


def test_fewer_than_three_supported_controls_or_two_repeats_is_invalid():
    """Rule: invalid with fewer than 3 of 4 supported controls accepted, or fewer than 2 of 3 repeats the same."""
    r = base(new_served=10)
    r['controls']['supported'] = ['supported', 'supported', 'unsupported', 'insufficient']
    assert verdict(r)['verdict'] == 'invalid'
    r = base(new_served=10)
    r['controls']['repeats_same'] = [True, False, False]
    assert verdict(r)['verdict'] == 'invalid'


def test_too_small_when_n_under_20_or_a_draw_under_30_distinct_bets_either_way():
    """Rule: too small when N < 20, or a draw has fewer than 30 distinct bets (split duplicates counted both ways)."""
    assert verdict(base(n=19, new_served=10))['verdict'] == 'too small'
    r = base(new_served=10)
    r['distinct']['old-2'] = {'ids': 32, 'duplicates_both': 1, 'duplicates_split': 2}     # 31 one way, 29 the other
    assert verdict(r)['verdict'] == 'too small'


def test_a_practical_lead_needs_the_margin_twice_b_and_every_guardrail_exercised_and_passing():
    """Rule: lead when a - b >= max(3, ceil(0.15 N)) and a >= 2b under both countings, with every guardrail exercised and passing."""
    r = base(n=20, new_served=5, old_served=1)               # a 5, b 1: margin max(3, 3) = 3; 5 - 1 = 4 >= 3; 5 >= 2
    assert verdict(r)['verdict'] == 'practical lead'
    r = base(n=20, new_served=4, old_served=2)               # a 4, b 2: 4 - 2 = 2 < 3
    assert verdict(r)['verdict'] == 'no practical winner'


def test_an_unexercised_guardrail_blocks_a_lead_but_not_a_loss():
    """Rule: a subgroup with fewer than 10 unsplit decided cards per system cannot breach; it blocks only a lead."""
    assert verdict(base(n=20, new_served=5, old_served=1, guard_cards=3))['verdict'] == 'no practical winner'
    assert verdict(base(n=20, new_served=1, old_served=5, guard_cards=3))['verdict'] == 'practical loss'


def test_a_guardrail_breach_under_both_countings_is_a_loss():
    """Rule: loss when the new system's unsupported share is more than 10 points above the old's, under both countings."""
    r = base(n=20, new_served=5, old_served=1)
    for d in ('new-1', 'new-2', 'new-3'):
        for j in range(3):                                     # 3 of 12 figure cards unsupported per draw: 25% against 0%
            r['cards'][d][f'{d}-g-figure-{j}']['answer'] = 'unsupported'
    out = verdict(r)
    assert out['verdict'] == 'practical loss' and 'guardrail figure' in out['why']


def test_a_matter_counts_as_served_only_in_two_of_three_draws():
    """Rule: served by a system when served in at least 2 of its 3 draws."""
    r = base(n=20, new_served=5, old_served=1)
    for d in ('new-2', 'new-3'):
        r['mapping'][d].pop('M01')                             # M01 served by the new system in one draw only
    out = verdict(r)
    assert out['countings']['1']['a'] == 4


def test_splits_resolve_for_the_favoured_system_in_each_counting():
    """Rule: counting 1 resolves the new system's splits favourably and the old's unfavourably; counting 2 the reverse."""
    r = base(n=20, new_served=5, old_served=1)
    for d in ('new-1', 'new-2', 'new-3'):
        q = r['mapping'][d]['M01'][0]['question']
        r['cards'][d][q]['answer'] = {'split': ['supported', 'unsupported']}
    out = verdict(r)
    assert out['countings']['1']['a'] == 5 and out['countings']['2']['a'] == 4
    assert out['verdict'] == 'practical lead'                 # 4 - 1 = 3 >= 3 and 4 >= 2 under counting 2 as well


def test_a_resolved_insufficient_stays_out_of_the_decided_shares():
    """Rule: insufficient (final or resolved) is outside the decided denominators."""
    r = base(n=20, new_served=5, old_served=1)
    r['cards']['new-1']['new-1-g-figure-0']['answer'] = 'insufficient'
    g = sc.guardrails(r, '1')['figure']['new']
    assert g['decided'] == 35 and g['share'] == 0.0


def test_exactly_ten_points_is_not_a_breach_and_more_is():
    """Rule: the new system's share may be at most 10 points above the old's, compared exactly (D675): 12/30 against 9/30 is exactly 10
    points, which floating point computes as 0.10000000000000003."""
    r = base(n=20, new_served=5, old_served=1, guard_cards=10)          # 30 decided figure cards per system
    for d in ('new-1', 'new-2', 'new-3'):
        for j in range(4):
            r['cards'][d][f'{d}-g-figure-{j}']['answer'] = 'unsupported'  # 12 of 30
    for d in ('old-1', 'old-2', 'old-3'):
        for j in range(3):
            r['cards'][d][f'{d}-g-figure-{j}']['answer'] = 'unsupported'  # 9 of 30
    assert verdict(r)['verdict'] == 'practical lead'
    r['cards']['new-1']['new-1-g-figure-4']['answer'] = 'unsupported'   # 13 of 30: above 10 points
    out = verdict(r)
    assert out['verdict'] == 'practical loss' and 'guardrail figure' in out['why']


def test_a_plant_both_readers_rejected_with_different_labels_is_rejected():
    """Rule: a plant needs an explicit rejection; unsupported and insufficient split between the readers are both rejections (D675)."""
    r = base(n=20, new_served=5, old_served=1)
    r['controls']['plants'][0] = {'split': ['unsupported', 'insufficient']}
    assert verdict(r)['verdict'] == 'practical lead'


def test_readings_without_all_six_draws_are_refused():
    """Rule: no release verdict without six complete draws."""
    r = base(n=20, new_served=5, old_served=1)
    for k in ('mapping', 'cards', 'distinct'):
        r[k].pop('old-3')
    try:
        verdict(r)
    except SystemExit as e:
        assert 'six draws' in str(e)
    else:
        raise AssertionError('five draws were scored')


def test_the_company_figure_subgroup_is_printed_beside():
    """Rule: the company-figure subgroup's a, b and N are printed beside the verdict."""
    r = base(n=20, new_served=5, old_served=1)
    r['matters'][0]['company_figure'] = True                           # M01: served by the new system only
    r['matters'][5]['company_figure'] = True                           # M06: served by the old system only
    out = verdict(r)
    assert out['beside']['company-figure subgroup']['1'] == {'N': 2, 'a': 1, 'b': 1}


def test_a_sampled_card_that_covers_a_matter_is_not_in_the_shares():
    """Rule: guardrail sample; covering cards are not in the shares (D675 reads the words as written)."""
    r = base(n=20, new_served=5, old_served=1)
    card = r['cards']['new-1']['new-1-g-figure-0']
    card.update(answer='unsupported', covering=True)
    g = sc.guardrails(r, '1')['figure']['new']
    assert g['decided'] == 35 and g['bad'] == 0


def test_a_split_cover_on_a_sampled_card_resolves_per_counting():
    """countings: covers > does not cover; a guardrail card whose cover is split is out of the shares for the favoured system only (D675)."""
    r = base(n=20, new_served=5, old_served=1)
    card = r['cards']['new-1']['new-1-g-figure-0']
    card.update(answer='unsupported', covering='split')
    assert sc.guardrails(r, '1')['figure']['new']['bad'] == 0          # counting 1 favours the new system: it covers, so it is left out
    assert sc.guardrails(r, '2')['figure']['new']['bad'] == 1          # counting 2: it does not cover, so it is in the shares


def test_readings_not_made_from_their_named_inputs_are_refused():
    """No verdict on other matters than the frozen list's, or on a mapping that is not the mapping file's (D671, D675)."""
    r = seal(base(n=20, new_served=5, old_served=1))
    r['matters'] = r['matters'][:-1] + [{'matter': 'M99', 'company_figure': False}]
    for change, reason in ((lambda x: None, 'frozen matter list'),):
        try:
            sc.verdict(r)
        except SystemExit as e:
            assert reason in str(e)
        else:
            raise AssertionError('readings on another matter list were scored')
    r = seal(base(n=20, new_served=5, old_served=1))
    r['mapping']['new-1'].pop('M02')                                        # changed after the mapping file was written
    try:
        sc.verdict(r)
    except SystemExit as e:
        assert 'mapping differs' in str(e)
    else:
        raise AssertionError('a mapping that is not the file was scored')


def test_every_split_matter_question_pair_is_reported_with_its_resolution():
    """beside: splits and their resolution, for every split pair, also when the question covers another matter outright (D675)."""
    r = base(n=20, new_served=5, old_served=1)
    q = r['mapping']['new-1']['M01'][0]['question']
    r['mapping']['new-1']['M07'] = [{'question': q, 'covers': 'split'}]
    out = verdict(r)
    assert out['beside']['split resolutions']['1'] == {'new cover split resolved to covers': 1}
    assert out['beside']['split resolutions']['2'] == {'new cover split resolved to does not cover': 1}


def test_card_marks_that_differ_from_the_deck_key_are_refused():
    """Which cards enter the guardrail shares comes from the verified deck key, never from the readings alone (D675)."""
    r = seal(base(n=20, new_served=5, old_served=1))
    r['cards']['new-1']['new-1-g-figure-0']['guardrail'] = False
    try:
        sc.verdict(r)
    except SystemExit as e:
        assert 'guardrail, covering or type' in str(e)
    else:
        raise AssertionError('a guardrail flag changed after the deck was scored')


def test_the_printed_beside_quantities_hold_their_definitions():
    """DESIGN-1.6.md §0 and §4: the sign test over discordant matters, D428's limits with denominators, the floors, and a covering
    question opened before the matter's first article printed as opened in the warm-up. None changes the verdict."""
    r = base(n=20, new_served=5, old_served=1)
    for d in ('new-1', 'new-2', 'new-3'):
        r['cards'][d][f'{d}-q0']['opened'] = '2026-07-04'
    r['matter_first_day'] = {'M01': '2026-09-08'}
    out = verdict(r)
    sign = out['beside']['sign test (illustrative)']['1']
    assert sign['discordant'] == 6 and abs(sign['p'] - 0.21875) < 1e-9          # 5 against 1: two-sided exact p = 14/64
    limits = out['beside']["D428 limits (a comparison on the guardrail sample, not Stage B's measurement)"]['1']['new']
    assert limits['figure unsupported'] == '0/36 against 12.7%-14.4%' and limits['latest answers insufficient (beside)'] == 0
    floors = out['beside']['floors (proposed)']['1']['new']
    assert floors['per draw']['new-1']['covered'] == {'count': '5/20', 'met': False}
    assert floors['per draw']['new-1']['trivial or duplicate'] == {'count': '0/24', 'met': True}
    assert out['beside']['days from first article to opening (confirmed coverage only; split covers not counted)']['M01']['new-1'] == 'opened in the warm-up'
    assert out['verdict'] == 'practical lead'


def test_an_opening_inside_the_window_before_the_first_listed_article_is_not_called_warm_up():
    """beside: 'warm-up' only before 09-07; an opening in the window before the matter's first listed article is named as such."""
    r = base(n=20, new_served=5, old_served=1)
    for d in ('new-1', 'new-2', 'new-3'):
        r['cards'][d][f'{d}-q0']['opened'] = '2026-09-09'
    r['matter_first_day'] = {'M01': '2026-09-12'}
    assert verdict(r)['beside']['days from first article to opening (confirmed coverage only; split covers not counted)']['M01']['new-1'] == 'opened before the first listed article'


def test_the_support_floor_gives_an_unresolved_answer_no_credit_in_either_counting():
    """floors: insufficient and unresolved latest answers are counted and get no credit toward 90% (reflection-10, codex-1.md)."""
    r = base(n=20, new_served=5, old_served=1, guard_cards=5)
    r['cards']['new-1']['new-1-g-figure-0']['answer'] = {'split': ['supported', 'unsupported']}
    out = verdict(r)
    assert out['beside']['floors (proposed)']['1']['new']['per draw']['new-1']['supported'] == {'count': '9/10', 'met': True}
    r['cards']['new-1']['new-1-g-figure-1']['answer'] = 'insufficient'
    out = verdict(r)
    assert out['beside']['floors (proposed)']['1']['new']['per draw']['new-1']['supported'] == {'count': '8/10', 'met': False}


def test_the_floors_count_every_random_sample_card_covering_or_not():
    """floors: trivial or duplicate and supported are over the library's random sample; covering cards leave only the guardrail shares."""
    r = base(n=20, new_served=5, old_served=1, guard_cards=5)
    card = r['cards']['new-1']['new-1-g-figure-0']
    card.update(worth='trivia', covering=True)
    out = verdict(r)
    assert out['beside']['floors (proposed)']['1']['new']['per draw']['new-1']['trivial or duplicate'] == {'count': '1/10', 'met': True}


def test_an_invalid_or_too_small_reading_still_prints_what_the_rule_prints_beside():
    """printed_beside: the quantities accompany every verdict, as diagnostics when the reading is invalid or too small (D675)."""
    r = base(n=19, new_served=5, old_served=1)
    out = verdict(r)
    assert out['verdict'] == 'too small' and out['countings']['1']['a'] == 5 and 'floors (proposed)' in out['beside']
    r = base(n=20, new_served=5, old_served=1)
    r['controls']['repeats_same'] = [False, False, True]
    out = verdict(r)
    assert out['verdict'] == 'invalid' and 'sign test (illustrative)' in out['beside']


def test_a_diagnostic_that_cannot_be_computed_never_stops_an_invalid_or_too_small_verdict():
    """The verdict is decided first; a printed-beside quantity that fails is flagged, never in the verdict's way (D675, Codex round 11)."""
    r = base(n=19, new_served=5, old_served=1)
    for d in ('new-1', 'new-2', 'new-3'):
        r['cards'][d][f'{d}-q0']['opened'] = 'not a date'
    r['matter_first_day'] = {'M01': '2026-09-08'}
    out = verdict(r)
    assert out['verdict'] == 'too small' and 'ValueError' in out['diagnostics not computed']
    assert out['countings']['1']['a'] == 5 and 'floors (proposed)' in out['beside']     # the other diagnostics are kept
    r['controls']['repeats_same'] = [False, False, True]
    r['distinct']['new-1']['ids'] = 'not a count'                                       # the size check is skipped once invalid
    out = verdict(r)
    assert out['verdict'] == 'invalid' and 'ValueError' in out['diagnostics not computed']
