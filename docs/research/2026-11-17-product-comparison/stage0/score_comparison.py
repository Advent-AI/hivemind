"""The comparison's verdict (D665; `verdict-rule.json`, frozen before the first send; D672). Code applies the frozen rule to the readers'
marks; it decides nothing the rule leaves open.

    python3 score_comparison.py <readings.json>

`readings.json` holds what the reading produces, by system-draw ('new-1'..'new-3', 'old-1'..'old-3'):
  matters:      [{"matter": "M01", "company_figure": bool}, ...]                       (stage0/census/matters.json)
  mapping:      {draw: {matter: [{"question": id, "covers": true|false|"split"}]}}     (blind mapping, third readers applied)
  cards:        {draw: {question id: {"worth": mark, "answer": mark, "type": "figure"|"yes/no"|"other", "guardrail": bool}}}
                a mark is a final mark, or {"split": [mark given by one family, mark given by the other]}
  distinct:     {draw: {"ids": n, "duplicates_both": n, "duplicates_split": n}}
  controls:     {"plants": [mark, ...], "supported": [mark, ...], "repeats_same": [bool, ...]}
Prints the verdict and every quantity behind it, under both countings.
"""
import json
import math
import sys

RANK = {'answer': ['unsupported', 'insufficient', 'supported'], 'worth': ['trivia', 'duplicate', 'worth'], 'covers': [False, True]}
SYSTEMS = ('new', 'old')


def resolve(mark, kind, favoured):
    """A final mark, or a split resolved to one of the marks its readers gave: the most favourable for a favoured system, the least for the
    other (verdict-rule.json, countings). 'no answer' is never split."""
    if not (isinstance(mark, dict) and 'split' in mark):
        return mark
    given = [m for m in mark['split'] if m in RANK[kind]]
    if not given:
        raise ValueError(f'a split of unknown marks: {mark}')
    order = sorted(given, key=RANK[kind].index)
    return order[-1] if favoured else order[0]


def is_split(mark):
    return isinstance(mark, dict) and 'split' in mark


def system_of(draw):
    return draw.split('-')[0]


def served_by(readings, counting):
    """{system: set of matters served in at least 2 of its 3 draws} under one counting ('1': new favoured, '2': old favoured)."""
    favoured = 'new' if counting == '1' else 'old'
    served_draws = {}
    for draw, by_matter in readings['mapping'].items():
        system = system_of(draw)
        fav = system == favoured
        for matter, questions in by_matter.items():
            for q in questions:
                covers = q['covers'] if q['covers'] != 'split' else fav       # covers > does not cover
                if not covers:
                    continue
                card = readings['cards'][draw].get(q['question'])
                if card is None:
                    raise ValueError(f'{draw} {q["question"]}: a covering question has no card')
                if card['answer'] == 'no answer':
                    continue
                if resolve(card['worth'], 'worth', fav) == 'worth' and resolve(card['answer'], 'answer', fav) == 'supported':
                    served_draws.setdefault((system, matter), set()).add(draw)
                    break
    return {s: {m for (sys_, m), draws in served_draws.items() if sys_ == s and len(draws) >= 2} for s in SYSTEMS}


def guardrails(readings, counting):
    """Per system: the three shares over its pooled guardrail cards, and whether each subgroup is exercised (10 unsplit decided cards)."""
    favoured = 'new' if counting == '1' else 'old'
    out = {}
    for system in SYSTEMS:
        fav = system == favoured
        counts = {'figure': [0, 0, 0], 'yes/no': [0, 0, 0], 'worth': [0, 0, 0]}     # [bad, decided, decided without a split]
        for draw, cards in readings['cards'].items():
            if system_of(draw) != system:
                continue
            for card in cards.values():
                if not card.get('guardrail'):
                    continue
                if card['type'] in ('figure', 'yes/no') and card['answer'] != 'no answer':
                    answer = resolve(card['answer'], 'answer', fav)
                    if answer in ('supported', 'unsupported'):
                        c = counts[card['type']]
                        c[0] += answer == 'unsupported'
                        c[1] += 1
                        c[2] += not is_split(card['answer'])
                worth = resolve(card['worth'], 'worth', fav)
                c = counts['worth']
                c[0] += worth in ('trivia', 'duplicate')
                c[1] += 1
                c[2] += not is_split(card['worth'])
        out[system] = {k: {'share': (v[0] / v[1]) if v[1] else None, 'decided': v[1], 'unsplit': v[2]} for k, v in counts.items()}
    result = {}
    for k in ('figure', 'yes/no', 'worth'):
        new, old = out['new'][k], out['old'][k]
        exercised = new['unsplit'] >= 10 and old['unsplit'] >= 10
        breach = exercised and (new['share'] - old['share']) > 0.10
        result[k] = {'new': new, 'old': old, 'exercised': exercised, 'breach': breach}
    return result


def verdict(readings):
    n = len(readings['matters'])
    controls = readings['controls']
    report = {'N': n}
    invalid = []
    if any(m not in ('unsupported', 'insufficient') for m in controls['plants']):
        invalid.append('a planted wrong answer without an explicit rejection')
    if sum(m == 'supported' for m in controls['supported']) < 3:
        invalid.append('fewer than 3 of 4 supported controls accepted')
    if sum(bool(x) for x in controls['repeats_same']) < 2:
        invalid.append('fewer than 2 of 3 repeats marked the same')
    if len(controls['plants']) != 6 or len(controls['supported']) != 4 or len(controls['repeats_same']) != 3:
        invalid.append('the deck does not hold 6 plants, 4 supported controls and 3 repeats')
    if invalid:
        return dict(report, verdict='invalid', why=invalid)
    small = []
    if n < 20:
        small.append(f'N = {n} < 20')
    for draw, d in readings['distinct'].items():
        both_ways = (d['ids'] - d['duplicates_both'], d['ids'] - d['duplicates_both'] - d['duplicates_split'])
        if min(both_ways) < 30:
            small.append(f'{draw}: {both_ways} distinct bets')
    if small:
        return dict(report, verdict='too small', why=small)
    margin = max(3, math.ceil(0.15 * n))
    per_counting = {}
    for counting in ('1', '2'):
        served = served_by(readings, counting)
        a = len(served['new'] - served['old'])
        b = len(served['old'] - served['new'])
        per_counting[counting] = {'a': a, 'b': b, 'served_new': sorted(served['new']), 'served_old': sorted(served['old']),
                                  'guardrails': guardrails(readings, counting)}
    report['margin'] = margin
    report['countings'] = per_counting
    lead = all(c['a'] - c['b'] >= margin and c['a'] >= 2 * c['b'] for c in per_counting.values())
    all_exercised_pass = all(g['exercised'] and not g['breach'] for c in per_counting.values() for g in c['guardrails'].values())
    if lead and all_exercised_pass:
        return dict(report, verdict='practical lead')
    loss_count = all(c['b'] - c['a'] >= margin and c['b'] >= 2 * c['a'] for c in per_counting.values())
    breaches = {k for k in ('figure', 'yes/no', 'worth') if all(c['guardrails'][k]['breach'] for c in per_counting.values())}
    if loss_count or breaches:
        return dict(report, verdict='practical loss', why=(['served matters'] if loss_count else []) + [f'guardrail {k}' for k in sorted(breaches)])
    return dict(report, verdict='no practical winner')


if __name__ == '__main__':
    print(json.dumps(verdict(json.loads(open(sys.argv[1]).read())), indent=1, ensure_ascii=False))
