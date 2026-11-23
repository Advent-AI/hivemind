"""$0 census of the self-made market reference (D692): in the three finished poc-v118 draws, how often a judgement's `reference`
(the field judging-v7 asks for: "what the market expects for this question (consensus, the company's guidance, the stated plan or
deadline)") is the system's own earlier figure rather than a market figure.

Two measures, per judgement of a question that already has a previous judgement:
  carried:   the reference says it was taken from the previous judgement or conclusion (the words "previous", "prior" or "carried");
  own_value: the reference's first figure equals the first figure of the previous judgement's `implied_outcome` (the system's own
             estimate), within 0.5% (the same unit word: billion, trillion, million or percent).
  unsourced: no figure in the request the judge was sent equals the reference's first figure, outside the "[Previous conclusion"
             section (the stored request, found in the draw's archive by the judgement's request_sha256). A figure the evidence
             states (a signed amount, a guidance figure, a rung bound) is therefore not counted, whatever the estimate equals.
A judgement counts once per measure. The stores are opened read-only. The positive control is old-2 v9 on 2026-09-15 (reference
"$414 billion", the 09-14 implied outcome "$414 billion", not in the evidence shown): the script exits with an error unless
both own_value and unsourced mark it.

  python3 reference_census.py > reference-census.md
"""
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
RUNS = REPO / 'poc/data/comparison-2026-11-17/run'
FIGURE = re.compile(r'\$?\s?(\d+(?:,\d{3})*(?:\.\d+)?)\s?(trillion|billion|million|bn|B\b|T\b|%|percent)', re.IGNORECASE)
UNIT = {'trillion': 1e12, 't': 1e12, 'billion': 1e9, 'bn': 1e9, 'b': 1e9, 'million': 1e6, '%': 1.0, 'percent': 1.0}
CARRIED = re.compile(r'\b(previous|prior|carried)\b', re.IGNORECASE)


def first_figure(text):
    match = FIGURE.search(text or '')
    if not match:
        return None
    unit = match.group(2).lower()
    kind = 'percent' if unit in ('%', 'percent') else 'amount'
    return kind, float(match.group(1).replace(',', '')) * UNIT[unit]


def same(a, b):
    return a and b and a[0] == b[0] and abs(a[1] - b[1]) <= 0.005 * max(abs(a[1]), abs(b[1]), 1e-9)


def all_figures(text):
    for match in FIGURE.finditer(text or ''):
        unit = match.group(2).lower()
        yield ('percent' if unit in ('%', 'percent') else 'amount'), float(match.group(1).replace(',', '')) * UNIT[unit]


def without_previous_conclusion(user_text):
    """The request's user text with the "[Previous conclusion" section removed (it runs to the next bracketed header or the end)."""
    return re.sub(r'\n\[Previous conclusion[^\n]*(?:\n(?!\[)[^\n]*)*', '\n', user_text)


def shown_material(archive, request_sha256):
    row = archive.execute("select request_json from model_calls where request_sha256=? limit 1", (request_sha256,)).fetchone()
    if not row:
        raise SystemExit(f'request {request_sha256} not in the archive: the census cannot judge it')
    import json
    messages = json.loads(row[0])['messages']
    return without_previous_conclusion(messages[-1]['content'])


def census(draw):
    conn = sqlite3.connect(f'file:{RUNS / draw}/prod/views.sqlite?mode=ro', uri=True)
    archive = sqlite3.connect(f'file:{RUNS / draw}/prod/archive.sqlite?mode=ro', uri=True)
    questions = dict(conn.execute('select view_id, question from views'))
    units = dict(conn.execute('select view_id, unit from view_keys'))
    rows = conn.execute('select view_id, judgement_id, publication_day, reference, implied_outcome, request_sha256 from judgements order by view_id, judgement_id').fetchall()
    per_question, marked, previous = {}, [], {}
    for view_id, judgement_id, day, reference, implied, request_sha256 in rows:
        if units.get(view_id) not in ('USD', 'percent'):
            continue
        stats = per_question.setdefault(view_id, {'judged': 0, 'with_previous': 0, 'carried': 0, 'own_value': 0, 'unsourced': 0, 'carried_unsourced': 0, 'first_unsourced': None})
        stats['judged'] += 1
        if view_id in previous:
            stats['with_previous'] += 1
            carried = bool(CARRIED.search(reference or ''))
            figure = first_figure(reference)
            own = bool(same(figure, first_figure(previous[view_id])))
            unsourced = bool(figure) and not any(same(figure, shown) for shown in all_figures(shown_material(archive, request_sha256)))
            stats['carried'] += carried
            stats['own_value'] += own
            stats['unsourced'] += unsourced
            stats['carried_unsourced'] += carried and unsourced
            if unsourced and not stats['first_unsourced']:
                stats['first_unsourced'] = day
            marked.append((view_id, day, carried, own, unsourced))
        previous[view_id] = implied
    return questions, per_question, marked


def main():
    print('# Self-made market reference: census on the three finished poc-v118 draws ($0)\n')
    print('Generated by `reference_census.py`. Number questions only (unit USD or percent). "carried": the reference says it was taken')
    print('from the previous judgement; "own value": its first figure equals the previous judgement\'s implied outcome (the system\'s own')
    print('estimate); "unsourced": its first figure is nowhere in the request the judge was sent, outside the previous conclusion.')
    print('All are read from the stored fields and requests; none says the figure is wrong, only where it came from.\n')
    print('| draw | number questions | judgements with a previous one | carried | own value | unsourced | own value and unsourced | carried and unsourced |')
    print('|---|---|---|---|---|---|---|---|')
    details = {}
    control = False
    for draw in ('old-1', 'old-2', 'old-3'):
        questions, per_question, marked = census(draw)
        details[draw] = (questions, per_question)
        with_previous = sum(s['with_previous'] for s in per_question.values())
        counts = [sum(1 for row in marked if test(row)) for test in (lambda r: r[2], lambda r: r[3], lambda r: r[4], lambda r: r[3] and r[4], lambda r: r[2] and r[4])]
        print(f'| {draw} | {len(per_question)} | {with_previous} | ' + ' | '.join(f'{n} ({n / max(with_previous, 1):.0%})' for n in counts) + ' |')
        if draw == 'old-2':
            control = any(row[0] == 'v9' and row[1] == '2026-09-15' and row[3] and row[4] for row in marked)
    for draw, (questions, per_question) in details.items():
        print(f'\n## {draw}: per question\n')
        print('| question | judged | with previous | carried | own value | unsourced | carried and unsourced | first unsourced day | text |')
        print('|---|---|---|---|---|---|---|---|---|')
        for view_id, s in sorted(per_question.items(), key=lambda kv: -kv[1]['unsourced']):
            print(f'| {view_id} | {s["judged"]} | {s["with_previous"]} | {s["carried"]} | {s["own_value"]} | {s["unsourced"]} | {s["carried_unsourced"]} | {s["first_unsourced"] or "-"} | {questions.get(view_id, "?")[:80]} |')
    if not control:
        sys.exit('positive control failed: old-2 v9 on 2026-09-15 is not marked as both its own value and unsourced')
    print('\nPositive control: old-2 v9 on 2026-09-15 is marked "own value" and "unsourced".')


if __name__ == '__main__':
    main()
