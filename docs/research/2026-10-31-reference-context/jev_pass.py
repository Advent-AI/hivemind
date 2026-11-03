"""Alex, 2026-10-31: measure the noise that reaches judgement, not what extraction keeps. Walk a sequential arm run (its answers and its
own ledger) day by day and put every kept statement that links to an open question through the production matching step's piece
relation as Jev answers it (views/jev_matching.piece_state, piece_question, PIECES, THRESHOLD; the stored list ranked as matching.rank_evidence
does, search_top_n from the configuration): repeat, replace or new against the pieces already stored under that question by this walk.
Statements linked to nothing go to the placement step (D207) and are counted apart. Each statement carries its gold class (core/supporting,
optional, not kept, unlisted) so the output says what reaches judgement as new and what Jev caught as a repeat. Jev input is priced from
model.PRICES; answers are archived under jev-pass-<tag>.sqlite so a rerun is free.

    python3 jev_pass.py SEQ-v68a 1        # one draw; prints the counts and writes jev-pass-<tag>-d<d>.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(HERE)]
import score_ref as sr  # noqa: E402
import score_seq as ss  # noqa: E402
import sequential_arm as sa  # noqa: E402
from hivemind import config, jev, model  # noqa: E402
from hivemind.views import jev_matching as jm  # noqa: E402
from hivemind.views.matching import _words  # noqa: E402

tag, draw = sys.argv[1], int(sys.argv[2])
cfg = config.load(str(ROOT / 'poc/config/poc-v69.json'))
archive = model.Archive(str(HERE / f'jev-pass-{tag}.sqlite'))
ledger = ss.ledger(tag, draw)
opened_from = {(q['from'], q['candidate_id']): q['id'] for q in ledger['questions']}       # a candidate that opened as a question
stored = {q['id']: [] for q in ledger['questions']}                                           # question id -> pieces stored so far by this walk
counts = {'kept': 0, 'unlinked': 0, 'linked': 0, 'repeat': 0, 'replace': 0, 'new': 0, 'calls': 0, 'cost_usd': 0.0}
by_class = {}
rows = []


def describe(piece):
    return f'{piece["eid"]} [{piece["tier"]}; {piece["speaker"]}; original source {piece["original_who"]} {piece["original_day"]}] {piece["one_line"]} | quote: {piece["quote"][:300]}'


def gold_class(a, e):
    if any(sr.sg.same_matter(i, e) for i in a['items'] if i['weight'] in ('core', 'supporting')):
        return 'core/supp'
    if any(sr.sg.same_matter(i, e) for i in a['items'] if i['weight'] == 'optional'):
        return 'optional'
    if any(sr.sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'not_kept'):
        return 'not_kept'
    return 'unlisted'


for day, ids in sa.by_day().items():
    day_new = []
    for iid in ids:
        a = ss.articles[iid]
        s = sr.sg.kept(sr.sg.answers(f'{tag}-d{draw}').get(iid), iid)
        if not s:
            continue
        raw = sr.raw(f'{tag}-d{draw}', iid) or {}
        raw_links = {e['id']: e.get('links', []) for e in raw.get('evidence', [])}      # the production sift drops links to ids it was not shown
        for e in s['evidence']:
            counts['kept'] += 1
            g = gold_class(a, e)
            links = [opened_from.get((iid, l), l) for l in raw_links.get(e['id'], [])]
            qs = [l for l in links if l in stored]
            if not qs:
                counts['unlinked'] += 1
                by_class.setdefault(('unlinked', g), 0); by_class[('unlinked', g)] += 1
                continue
            counts['linked'] += 1
            piece = {'eid': f'{iid}#{e["id"]}', 'tier': e['tier'], 'speaker': e['speaker'], 'original_who': e['original_who'], 'original_day': e.get('original_day') or a['publication_day'],
                     'one_line': e['one_line'], 'quote': e['quote']}
            outcome = 'new'
            for q in qs:
                target = _words(e['one_line'])
                listed = sorted(stored[q], key=lambda p: -len(target & _words(p['one_line'] + ' ' + p['quote'])))[:cfg.search_top_n]
                if not listed:
                    continue
                questions = {f'piece__{q}__{p["eid"]}': jm.piece_question(describe(p)) for p in listed}
                answer = jev.ask(archive, cfg, cfg.matching, jm.piece_state(e, piece['original_day']), questions, 'match')
                counts['calls'] += 1; counts['cost_usd'] += answer.cost_usd
                scored = [(answer.data[k], k) for k in questions]
                if any(x['choice'] == 'same_statement' and x['probabilities']['same_statement'] >= jm.THRESHOLD for x, _ in scored):
                    outcome = 'repeat'; break
                if any(x['choice'] == 'supersedes' and x['probabilities']['supersedes'] >= jm.THRESHOLD for x, _ in scored):
                    outcome = 'replace'
            counts[outcome] += 1
            by_class.setdefault((outcome, g), 0); by_class[(outcome, g)] += 1
            rows.append({'day': day, 'input_id': iid, 'id': e['id'], 'gold': g, 'links': qs, 'outcome': outcome, 'one_line': e['one_line'][:160]})
            if outcome != 'repeat':
                for q in qs:
                    day_new.append((q, piece))
    for q, piece in day_new:
        stored[q].append(piece)
(HERE / f'jev-pass-{tag}-d{draw}.json').write_text(json.dumps({'counts': counts, 'by_class': {f'{k[0]}|{k[1]}': v for k, v in by_class.items()}, 'rows': rows}, ensure_ascii=False, indent=1))
print(tag, f'd{draw}', counts)
for k in sorted(by_class):
    print(f'   {k[0]:>8} {k[1]:<10} {by_class[k]}')
