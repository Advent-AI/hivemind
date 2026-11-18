"""The comparison's verdict (D665; `verdict-rule.json`, frozen before the first send; D672). Code applies the frozen rule to the readers'
marks; it decides nothing the rule leaves open.

    python3 score_comparison.py <readings.json>

`readings.json` holds what the reading produces, by system-draw ('new-1'..'new-3', 'old-1'..'old-3'):
  matters:      [{"matter": "M01", "company_figure": bool}, ...]                       (stage0/census/matters.json)
  mapping:      {draw: {matter: [{"question": id, "covers": true|false|"split"}]}}     (blind mapping, third readers applied)
  cards:        {draw: {question id: {"worth": mark, "answer": mark, "type": "figure"|"yes/no"|"other", "guardrail": bool,
                                         "covering": true|false|"split"}}}
                a mark is a final mark, or {"split": [mark given by one family, mark given by the other]}
  distinct:     {draw: {"ids": n, "duplicates_both": n, "duplicates_split": n}}
  controls:     {"plants": [mark, ...], "supported": [mark, ...], "repeats_same": [bool, ...]}
  inputs:       {"matters_sha256", "mapping_path", "mapping_sha256", "eligibility_path", "eligibility_sha256", "deck_key_path",
                 "deck_key_sha256"}    (mark_cards.readings); the scorer re-reads each file and checks it against the readings
Prints the verdict and every quantity behind it, under both countings.

Readings of the frozen rule written here (D675): the guardrail shares hold the random sample's cards that cover no matter, as the rule's
words say ("covering cards are not in the shares"); the 10-point bar is compared exactly, as fractions; a plant counts as explicitly rejected
when every mark its readers left is unsupported or insufficient, split between the two or not. A guardrail card whose cover the third readers
split is resolved per counting like any cover (covers > does not cover: covering, so out of the shares, for the favoured system). A supported
control is accepted only when marked supported by both (a split is not accepted); a repeat is the same only when both of its final marks equal
the original card's, splits included. No verdict without all six draws and the frozen matter list, and only on eligible draws.
"""
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

DRAWS = ('new-1', 'new-2', 'new-3', 'old-1', 'old-2', 'old-3')
MATTERS = Path(__file__).resolve().parent / 'census' / 'matters.json'
REJECTED = ('unsupported', 'insufficient')

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
                covering = card['covering'] if card['covering'] != 'split' else fav      # covers > does not cover
                if not card['guardrail'] or covering:
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
        out[system] = {k: {'share': Fraction(v[0], v[1]) if v[1] else None, 'bad': v[0], 'decided': v[1], 'unsplit': v[2]} for k, v in counts.items()}
    result = {}
    for k in ('figure', 'yes/no', 'worth'):
        new, old = out['new'][k], out['old'][k]
        exercised = new['unsplit'] >= 10 and old['unsplit'] >= 10
        breach = exercised and (new['share'] - old['share']) > Fraction(1, 10)
        result[k] = {'new': new, 'old': old, 'exercised': exercised, 'breach': breach}
    return result


def beside(readings, per_counting):
    """What the rule prints beside the verdict (verdict-rule.json `printed_beside`, `guardrails.beside`)."""
    figure = {m['matter'] for m in readings['matters'] if m['company_figure']}
    out = {'company-figure subgroup': {c: {'N': len(figure), 'a': len((set(v['served_new']) - set(v['served_old'])) & figure),
                                            'b': len((set(v['served_old']) - set(v['served_new'])) & figure)} for c, v in per_counting.items()}}
    counts = {}
    for draw, cards in readings['cards'].items():
        system = system_of(draw)
        c = counts.setdefault(system, {'insufficient': 0, 'no answer': 0, 'split worth': 0, 'split answer': 0, 'cards': 0})
        for card in cards.values():
            c['cards'] += 1
            c['insufficient'] += card['answer'] == 'insufficient'
            c['no answer'] += card['answer'] == 'no answer'
            c['split worth'] += is_split(card['worth'])
            c['split answer'] += is_split(card['answer'])
    out['marks'] = counts
    resolutions = {}
    for c in per_counting:
        favoured = 'new' if c == '1' else 'old'
        tally = {}
        for draw, cards in readings['cards'].items():
            fav = system_of(draw) == favoured
            for card in cards.values():
                for kind in ('worth', 'answer'):
                    if is_split(card[kind]):
                        key = f'{system_of(draw)} {kind} split resolved to {resolve(card[kind], kind, fav)}'
                        tally[key] = tally.get(key, 0) + 1
        for draw, by_matter in readings['mapping'].items():
            fav = system_of(draw) == favoured
            for matter, questions in by_matter.items():
                for q in questions:
                    if q['covers'] == 'split':                       # every split matter-question pair, as the counting resolves it
                        key = f"{system_of(draw)} cover split resolved to {'covers' if fav else 'does not cover'}"
                        tally[key] = tally.get(key, 0) + 1
        resolutions[c] = tally
    out['split resolutions'] = resolutions
    return out


def verify_inputs(readings):
    """Refuses readings that were not made from the frozen matter list, the mapping file, a passing eligibility check and the deck key
    they name: each file is read again and compared with what the readings carry."""
    inputs = readings.get('inputs') or {}
    def read(kind):
        path = Path(inputs.get(f'{kind}_path') or '/nonexistent')
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != inputs.get(f'{kind}_sha256'):
            raise SystemExit(f'refused: the {kind} file the readings name is missing or differs from its fingerprint')
        return json.loads(path.read_text())
    frozen = [{'matter': m['matter'], 'company_figure': m['company_figure']} for m in json.loads(MATTERS.read_text())['matters']]
    if readings['matters'] != frozen or inputs.get('matters_sha256') != hashlib.sha256(MATTERS.read_bytes()).hexdigest():
        raise SystemExit('refused: the readings were not made on the frozen matter list')
    mapped, eligibility, key = read('mapping'), read('eligibility'), read('deck_key')
    if mapped['mapping'] != readings['mapping'] or mapped['distinct'] != readings['distinct']:
        raise SystemExit('refused: the readings\' mapping differs from the mapping file')
    if mapped.get('eligibility_sha256') != inputs['eligibility_sha256'] or eligibility.get('eligible') is not True:
        raise SystemExit('refused: the mapping was not made from a passing eligibility check')
    keyed = {}
    for k in key.values():
        if k['role'] == 'product':
            keyed.setdefault(k['draw'], {})[k['question']] = {f: k[f] for f in ('guardrail', 'covering', 'type')}
    held = {draw: {q: {f: card[f] for f in ('guardrail', 'covering', 'type')} for q, card in cards.items()} for draw, cards in readings['cards'].items()}
    if keyed != held:
        raise SystemExit('refused: the readings\' cards, or their guardrail, covering or type marks, are not the deck key\'s product cards')


def verdict(readings):
    present = {k: sorted(readings[k]) for k in ('mapping', 'cards', 'distinct')}
    for k, draws in present.items():
        if sorted(DRAWS) != draws:
            raise SystemExit(f'refused: readings[{k!r}] holds {draws}, not the six draws {list(DRAWS)}')
    verify_inputs(readings)
    n = len(readings['matters'])
    controls = readings['controls']
    report = {'N': n}
    invalid = []
    def rejected(m):
        return m in REJECTED or (isinstance(m, dict) and 'split' in m and all(x in REJECTED for x in m['split']))
    if any(not rejected(m) for m in controls['plants']):
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
    report['beside'] = beside(readings, per_counting)
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
    print(json.dumps(verdict(json.loads(open(sys.argv[1]).read())), indent=1, ensure_ascii=False, default=str))
