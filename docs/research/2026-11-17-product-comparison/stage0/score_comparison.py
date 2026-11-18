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


def company_figure_subgroup(readings, per_counting):
    figure = {m['matter'] for m in readings['matters'] if m['company_figure']}
    return {c: {'N': len(figure), 'a': len((set(v['served_new']) - set(v['served_old'])) & figure),
                'b': len((set(v['served_old']) - set(v['served_new'])) & figure)} for c, v in per_counting.items()}


def mark_counts(readings, per_counting):
    counts = {}
    for draw, cards in readings['cards'].items():
        c = counts.setdefault(system_of(draw), {'insufficient': 0, 'no answer': 0, 'split worth': 0, 'split answer': 0, 'cards': 0})
        for card in cards.values():
            c['cards'] += 1
            c['insufficient'] += card['answer'] == 'insufficient'
            c['no answer'] += card['answer'] == 'no answer'
            c['split worth'] += is_split(card['worth'])
            c['split answer'] += is_split(card['answer'])
    return counts


def split_resolutions(readings, per_counting):
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
    return resolutions


def beside(readings, per_counting):
    """What the rule prints beside the verdict (verdict-rule.json `printed_beside`, `guardrails.beside`)."""
    return {'company-figure subgroup': company_figure_subgroup(readings, per_counting), 'marks': mark_counts(readings, per_counting),
            'split resolutions': split_resolutions(readings, per_counting)}


MARKS = {'worth': ('worth', 'trivia', 'duplicate'), 'answer': ('supported', 'unsupported', 'insufficient')}


def validate_readings(readings):
    """Refuses malformed readings before any verdict or diagnostic (one owner for the readings' shape): every mark a frozen mark or a
    split of two, every cover true, false or "split" and naming a carded question, every count a non-negative integer, every day an ISO
    date. `mark_cards.readings` writes only such values; anything else means the file was not made by the reading."""
    import datetime
    problems = []
    def mark_ok(value, kind):
        if isinstance(value, dict):
            pair = value.get('split')
            return set(value) == {'split'} and isinstance(pair, list) and len(pair) == 2 and all(isinstance(v, str) and v in MARKS[kind] for v in pair)
        return isinstance(value, str) and (value in MARKS[kind] or (kind == 'answer' and value == 'no answer'))
    def cover_ok(value):
        return value is True or value is False or value == 'split'          # JSON booleans only: 1 is not True here
    def day_ok(value):
        try:
            datetime.date.fromisoformat(value)
            return True
        except (TypeError, ValueError):
            return False
    for draw, cards in readings['cards'].items():
        for q, card in cards.items():
            if not (mark_ok(card.get('worth'), 'worth') and mark_ok(card.get('answer'), 'answer') and card.get('type') in ('figure', 'yes/no', 'other')
                    and isinstance(card.get('guardrail'), bool) and cover_ok(card.get('covering'))
                    and (card.get('opened') is None or day_ok(card.get('opened')))):
                problems.append(f'{draw} {q}: a card mark, type, flag or day outside the closed set')
    frozen_matters = {m['matter'] for m in readings['matters']}
    for draw, by_matter in readings['mapping'].items():
        for matter, questions in by_matter.items():
            if matter not in frozen_matters or not isinstance(questions, list):
                problems.append(f'{draw} {matter}: a mapped matter outside the frozen list, or its questions not a list')
                continue
            for entry in questions:
                if not cover_ok(entry.get('covers')) or entry.get('question') not in readings['cards'].get(draw, {}):
                    problems.append(f'{draw} {matter}: a cover outside the closed set or naming no carded question')
    for draw, d in readings['distinct'].items():
        if not all(isinstance(d.get(k), int) and not isinstance(d.get(k), bool) and d.get(k) >= 0 for k in ('ids', 'duplicates_both', 'duplicates_split')):
            problems.append(f'{draw}: a distinct-bet count that is not a non-negative integer')
        elif d['duplicates_both'] + d['duplicates_split'] > d['ids']:
            problems.append(f'{draw}: more duplicates than ids')
    for matter, day in (readings.get('matter_first_day') or {}).items():
        if not day_ok(day):
            problems.append(f'{matter}: a first-article day that is not an ISO date')
    controls = readings['controls']
    if not (all(isinstance(controls[k], list) for k in ('plants', 'supported', 'repeats_same'))
            and all(mark_ok(m, 'answer') for m in controls['plants']) and all(mark_ok(m, 'answer') for m in controls['supported'])
            and all(isinstance(x, bool) for x in controls['repeats_same'])):
        problems.append('a control mark outside the closed set')
    if problems:
        raise SystemExit('refused: malformed readings: ' + '; '.join(problems[:10]) + (f' (and {len(problems) - 10} more)' if len(problems) > 10 else ''))


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


D428_LATEST = Fraction(3, 30)                                    # D428: at most 3 in 30 decided latest answers unsupported, scaled


def sign_test(a, b):
    """Two-sided exact binomial p of a against b at one half, and the Wilson 95% interval of a / (a + b): illustrative only."""
    n = a + b
    if n == 0:
        return {'discordant': 0, 'p': None, 'share': None, 'wilson95': None}
    tail = sum(math.comb(n, k) for k in range(0, min(a, b) + 1)) / 2 ** n
    z, phat = 1.959963984540054, a / n
    centre = (phat + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return {'discordant': n, 'p': min(1.0, 2 * tail), 'share': round(phat, 3), 'wilson95': [round(centre - half, 3), round(centre + half, 3)]}


D428_KEY = 'D428 limits (a comparison on the guardrail sample, not Stage B\'s measurement)'
DAYS_KEY = 'days from first article to opening (confirmed coverage only; split covers not counted)'


def d428_limits(readings, per_counting):
    out = {}
    for c, v in per_counting.items():
        fav_system = 'new' if c == '1' else 'old'
        limits = {}
        for system in SYSTEMS:
            fig, yn = v['guardrails']['figure'][system], v['guardrails']['yes/no'][system]
            latest_bad, latest_decided = fig['bad'] + yn['bad'], fig['decided'] + yn['decided']
            limits[system] = {
                'figure unsupported': f"{fig['bad']}/{fig['decided']} against 12.7%-14.4%" if fig['decided'] else 'none decided',
                'yes/no unsupported': f"{yn['bad']}/{yn['decided']} against 5%" if yn['decided'] else 'none decided',
                'latest answers unsupported': f"{latest_bad}/{latest_decided} against {float(D428_LATEST * latest_decided):.1f} (3 in 30 scaled)"
                                              if latest_decided else 'none decided',
                'latest answers insufficient (beside)': insufficient_count(readings, system, system == fav_system)}
        out[c] = limits
    return out


def sign_tests(readings, per_counting):
    return {c: sign_test(v['a'], v['b']) for c, v in per_counting.items()}


def floors(readings, per_counting):
    return {c: {system: floors_per_draw(readings, system, system == ('new' if c == '1' else 'old')) for system in SYSTEMS}
            for c in per_counting}


PRINTED_ITEMS = (('company-figure subgroup', company_figure_subgroup), ('marks', mark_counts), ('split resolutions', split_resolutions),
                 (D428_KEY, d428_limits), ('sign test (illustrative)', sign_tests), ('floors (proposed)', floors),
                 (DAYS_KEY, lambda readings, per_counting: days_to_opening(readings)))


def printed_beside(readings, per_counting):
    """The rule's printed-beside quantities that come from the cards (DESIGN-1.6.md §0, §4): D428's limits, the sign test, the floors and
    the days from a matter's first article to its opening. None of them enters the verdict."""
    return {name: compute(readings, per_counting) for name, compute in PRINTED_ITEMS[3:]}


def printed_items_tolerant(readings, per_counting):
    """Every printed item on its own (one item, one computation): the items that can be computed, and a flag naming each that cannot."""
    shown, flags = {}, []
    for name, compute in PRINTED_ITEMS:
        try:
            shown[name] = compute(readings, per_counting)
        except Exception as error:
            flags.append(f'{name}: {type(error).__name__}: {error}')
    return shown, flags


FLOORS = {'covered': Fraction(80, 100), 'trivial or duplicate': Fraction(20, 100), 'supported': Fraction(90, 100)}


def floors_per_draw(readings, system, fav):
    """The proposed absolute floors as their source states them (reflection-10 `codex-1.md`; RUN-PLAN-v2 §1.6), per draw, met when met in
    at least two of the system's three draws: important matters covered (a covering question, after the counting's split resolution) at
    least 80%; trivial or duplicate questions among the random sample's decided worth marks at most 20% (covering cards included: the
    frozen rule keeps them out of the guardrail shares, not the floors); supported latest answers among the random sample's answered cards
    at least 90%, an insufficient or unresolved (split) answer counted and given no credit (the
    verdict's own split resolution is unchanged). Citations and omissions are not measured."""
    n = len(readings['matters'])
    per_draw = {}
    for draw in DRAWS:
        if system_of(draw) != system:
            continue
        covered = sum(1 for questions in readings['mapping'][draw].values()
                      if any(q['covers'] is True or (q['covers'] == 'split' and fav) for q in questions))
        trivial = worth_decided = supported = answered = 0
        for card in readings['cards'][draw].values():
            if not card['guardrail']:                       # every random-sample card, covering or not: the floors speak of the library
                continue
            worth_decided += 1
            trivial += resolve(card['worth'], 'worth', fav) in ('trivia', 'duplicate')
            if card['answer'] != 'no answer':
                answered += 1
                supported += card['answer'] == 'supported'      # an unresolved (split) answer is counted without credit, as the source says
        shares = {'covered': (covered, n), 'trivial or duplicate': (trivial, worth_decided), 'supported': (supported, answered)}
        per_draw[draw] = {k: {'count': f'{a}/{b}', 'met': (b > 0 and (Fraction(a, b) <= FLOORS[k] if k == 'trivial or duplicate'
                                                                      else Fraction(a, b) >= FLOORS[k]))} for k, (a, b) in shares.items()}
    out = {'per draw': per_draw}
    for k in FLOORS:
        out[f'{k}: met in at least 2 of 3 draws'] = sum(d[k]['met'] for d in per_draw.values()) >= 2
    out['wrong citations'] = out['answer-changing omissions'] = 'not measured'
    return out


def insufficient_count(readings, system, fav):
    """Latest answers resolved to insufficient among the system's guardrail-share cards (outside the decided denominators)."""
    count = 0
    for draw, cards in readings['cards'].items():
        if system_of(draw) != system:
            continue
        for card in cards.values():
            covering = card['covering'] if card['covering'] != 'split' else fav
            if card['guardrail'] and not covering and card['answer'] != 'no answer' and resolve(card['answer'], 'answer', fav) == 'insufficient':
                count += 1
    return count


def trivia_count(readings, system, fav):
    """Trivia marks (duplicates apart) among the decided worth marks of the system's guardrail shares' cards."""
    trivia = decided = 0
    for draw, cards in readings['cards'].items():
        if system_of(draw) != system:
            continue
        for card in cards.values():
            covering = card['covering'] if card['covering'] != 'split' else fav
            if not card['guardrail'] or covering:
                continue
            decided += 1
            trivia += resolve(card['worth'], 'worth', fav) == 'trivia'
    return trivia, decided


def days_to_opening(readings):
    """Per draw and covered matter: days from the matter's earliest listed article to the first covering question's opening. A question
    opened before the scored window (09-07) is 'opened in the warm-up'; one opened in the window before the matter's first listed article
    is 'opened before the first listed article'."""
    import datetime
    out = {}
    for draw, by_matter in readings['mapping'].items():
        for matter, questions in by_matter.items():
            opened = [readings['cards'][draw][q['question']].get('opened') for q in questions if q['covers'] is True]
            opened = [d for d in opened if d]
            first = readings.get('matter_first_day', {}).get(matter)
            if not opened or not first:
                continue
            days = (datetime.date.fromisoformat(min(opened)) - datetime.date.fromisoformat(first)).days
            out.setdefault(matter, {})[draw] = (days if days >= 0 else 'opened in the warm-up' if min(opened) < '2026-09-07'
                                                else 'opened before the first listed article')
    return out


def verdict(readings):
    present = {k: sorted(readings[k]) for k in ('mapping', 'cards', 'distinct')}
    for k, draws in present.items():
        if sorted(DRAWS) != draws:
            raise SystemExit(f'refused: readings[{k!r}] holds {draws}, not the six draws {list(DRAWS)}')
    verify_inputs(readings)
    validate_readings(readings)
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
    small = []
    if not invalid:                                            # the size check runs only when the controls hold
        if n < 20:
            small.append(f'N = {n} < 20')
        for draw, d in readings['distinct'].items():
            both_ways = (d['ids'] - d['duplicates_both'], d['ids'] - d['duplicates_both'] - d['duplicates_split'])
            if min(both_ways) < 30:
                small.append(f'{draw}: {both_ways} distinct bets')
    margin = max(3, math.ceil(0.15 * n))

    def countings():
        per_counting = {}
        for counting in ('1', '2'):
            served = served_by(readings, counting)
            a = len(served['new'] - served['old'])
            b = len(served['old'] - served['new'])
            per_counting[counting] = {'a': a, 'b': b, 'served_new': sorted(served['new']), 'served_old': sorted(served['old']),
                                      'guardrails': guardrails(readings, counting)}
        return per_counting

    if invalid or small:
        # The verdict is decided first; each diagnostic is printed when it can be computed and flagged when it cannot, keeping the rest.
        flags = []
        try:
            per_counting = countings()
            report.update(margin=margin, countings=per_counting)
            report['beside'], flags = printed_items_tolerant(readings, per_counting)
        except Exception as error:
            flags.append(f'countings: {type(error).__name__}: {error}')
        if flags:
            report['diagnostics not computed'] = '; '.join(flags)
        return dict(report, verdict='invalid', why=invalid) if invalid else dict(report, verdict='too small', why=small)
    per_counting = countings()
    shown = beside(readings, per_counting)
    shown.update(printed_beside(readings, per_counting))
    report['margin'] = margin
    report['countings'] = per_counting
    report['beside'] = shown
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
