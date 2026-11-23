"""The fresh test of a presentation-only change to the previous conclusion (council H, D684), on answers the design never read.

  python3 fresh_test.py pool                       # $0: freshpool.json; every pooled request rebuilt byte for byte under the frozen judge
  python3 fresh_test.py censusdeck                 # $0 + plant confirmations: blind cards of every pooled answer as stored
  python3 fresh_test.py censusread                 # both reader families mark the census deck, rounds 0-2 (no API spend)
  python3 fresh_test.py select                     # $0: freshcases.json by the rule written in DESIGN-J2.md before any reading
  python3 fresh_test.py check [pool]               # $0: each arm's request built, the heading replaced exactly once, a synthetic answer checked
  python3 fresh_test.py probe <ledger> <arm> <k>   # cents: each fresh case's request under the arm, sent k times
  python3 fresh_test.py gold <ledger> <arm> <k>    # cents: the frozen judgement gold's requests under the arm
  python3 fresh_test.py testdeck <arm> [<arm> ...] # $0 + plant confirmations: blind cards of every answer of every arm and repeat
  python3 fresh_test.py testread                   # both reader families mark the test deck
  python3 fresh_test.py score <arm>                # $0: the screen, the arm against the same-day v7 re-send

The pool: per draw of the release comparison and per question of its library, the latest judgement on or before CUT (the day before the
dev window), unless the design read an answer of that question in that draw (the 24 targets, their 24 controls, the 49 census answers),
the question's last judgement is that same one (its answer was read at 09-20), it is a first judgement (no previous conclusion), or it is
a retry. Stores are read through read-only connections; keys stay outside the repository."""
import concurrent.futures
import json
import math
import random
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import judge_probe as jp  # noqa: E402

CUT = '2026-09-06'
DRAWS = ('old-1', 'old-2', 'old-3', 'new-2', 'new-3')
ITEMS = jp.ROOT / 'poc/data/comparison-2026-11-17/items-comparison.sqlite'
KEYS = Path.home() / '.hivemind-keys/hybrid-2026-11-20'
CENSUS_KEY = KEYS / 'fresh-census-key.json'
TEST_KEY = KEYS / 'fresh-test-key.json'
POOL = jp.OUT / 'freshpool.json'
FRESH = jp.OUT / 'freshcases.json'
OLD_HEADING = '\n\n[Previous conclusion, for comparison only] rung '
NEW_HEADING = "\n\n[Previous conclusion: earlier assessment and carried evidence. Derive today's forecast afresh.] rung "
OLD_SENTENCE = 'Do not add to or subtract from the previous score.'
NEW_SENTENCE = 'Derive the rung from this evidence rather than adjusting the previous score.'   # PRD 06, line 19
REJECTED = {'unsupported', 'insufficient'}


def arm_parts(arm):
    """(system text, whether the heading is replaced) of an arm: v7 the frozen judge; H1 the heading only; H2 the heading and the
    system sentence restated in the PRD's words."""
    frozen = jp.FROZEN_SYSTEM.read_text(encoding='utf-8')
    if arm == 'v7':
        return frozen, False
    if arm == 'H1':
        return frozen, True
    if arm == 'H2':
        assert frozen.count(OLD_SENTENCE) == 1
        return frozen.replace(OLD_SENTENCE, NEW_SENTENCE), True
    raise SystemExit(f'unknown arm {arm}')


def arm_user(user, arm):
    """The user text the arm sends: the stored text, with the heading replaced exactly once when the arm replaces it (a first
    judgement carries no previous conclusion and is sent unchanged)."""
    _, replaces = arm_parts(arm)
    if replaces and OLD_HEADING in user:
        assert user.count(OLD_HEADING) == 1
        user = user.replace(OLD_HEADING, NEW_HEADING)
    return user


def arm_request(request, arm):
    system, _ = arm_parts(arm)
    user = arm_user(request['messages'][1]['content'], arm)
    return jp.rebuild(dict(request, messages=[request['messages'][0], dict(request['messages'][1], content=user)]), system)


def stored_request(draw, request_sha256):
    _, archive = jp.store_paths(draw)
    row = jp.readonly(archive).execute('select request_json from model_calls where request_sha256=? limit 1', (request_sha256,)).fetchone()
    return json.loads(row['request_json'])


def pool():
    from hivemind import model
    frozen = jp.FROZEN_SYSTEM.read_text(encoding='utf-8')
    readings = json.loads((jp.DIAG / 'deck/readings.json').read_text())['cards']
    library_of = json.loads((jp.KEYS / 'mapping-key-diagnostic.json').read_text())
    exposed = {(c['draw'], c['label']) for c in json.loads((jp.OUT / 'cases.json').read_text())}
    exposed |= set(re.findall(r'^### \d+\. (\S+) (Q\d+) ', (HERE / 'census/rejected-answers.md').read_text(), re.M))
    out, dropped, mismatched = [], Counter(), []
    for draw in DRAWS:
        views, _ = jp.store_paths(draw)
        conn = jp.readonly(views)
        for entry in json.loads((jp.DIAG / f'mapping-out/library-{library_of[draw]}.json').read_text()):
            label, view_id = entry['question_id'], entry['source_id']
            if (draw, label) in exposed:
                dropped['an answer of it was read in the design'] += 1
                continue
            j = conn.execute('select * from judgements where view_id=? and publication_day<=? order by seq desc limit 1', (view_id, CUT)).fetchone()
            if j is None:
                dropped['no answer by the cut'] += 1
                continue
            last = conn.execute('select judgement_id from judgements where view_id=? order by seq desc limit 1', (view_id,)).fetchone()
            if last['judgement_id'] == j['judgement_id']:
                dropped['its answer at the cut is the one read at 09-20'] += 1
                continue
            request = stored_request(draw, j['request_sha256'])
            user = request['messages'][-1]['content']
            if len(request['messages']) != 2 or 'The code returned the previous answer because' in user:
                dropped['a retry'] += 1
                continue
            if OLD_HEADING not in user:
                dropped['a first judgement'] += 1
                continue
            _, sha = model.request_identity(jp.rebuild(request, frozen))
            if sha != j['request_sha256']:
                mismatched.append(f'{draw}-{label}')
                continue
            previous = int(re.search(r'\[Previous conclusion, for comparison only\] rung (\d+)', user).group(1))
            hidden = re.search(r'\[Not shown: (\d+) more pieces', user)
            mark = readings[draw].get(label, {})
            out.append({'case': f'F-{draw}-{label}', 'draw': draw, 'label': label, 'view_id': view_id, 'judgement_id': j['judgement_id'],
                        'seq': j['seq'], 'day': j['publication_day'], 'request_sha256': j['request_sha256'], 'rung': j['rung'],
                        'previous_rung': previous, 'held': j['rung'] == previous, 'hidden': int(hidden.group(1)) if hidden else 0,
                        'type': entry['type'], 'worth_at_0920': mark.get('worth')})
    POOL.write_text(json.dumps(out, indent=1))
    print(f'{len(out)} pooled answers; dropped {dict(dropped)};', f'{len(out)} of {len(out) + len(mismatched)} rebuilt byte for byte',
          ('mismatch: ' + ', '.join(mismatched)) if mismatched else '')
    print('by draw', dict(Counter(c['draw'] for c in out)), '; held the previous rung', sum(c['held'] for c in out))
    if mismatched:
        raise SystemExit(1)


class Cards:
    """The comparison's own card builder, as of the cut: the card's library list holds the questions opened by CUT; the answer is shown
    with its reference, implied outcome and reasons; the material and context come from the request the answer received (built from the
    stored v7 text, which an arm changes only in the heading line the card does not show)."""

    def __init__(self, cut=CUT):
        self.cut = cut
        sys.path[:0] = [str(jp.STAGE0), str(jp.STAGE0 / 'census')]
        import build_cards
        self.bc = build_cards
        self.libraries = {}
        self.items = build_cards.ro(ITEMS)

    def text(self, case, answer):
        views, archive = jp.store_paths(case['draw'])
        if case['draw'] not in self.libraries:
            self.libraries[case['draw']] = [e for e in self.bc.library(views, archive, ITEMS) if (e['opened'] or '') <= self.cut]
        lib = self.libraries[case['draw']]
        entry = dict(next(e for e in lib if e['question_id'] == case['view_id']))
        request_json = json.dumps(stored_request(case['draw'], case['request_sha256']))
        conn = self.bc.ro(views)
        rungs = self.bc.conditions(case['view_id'], conn)
        publisher_of = lambda input_id: (self.items.execute('select publisher from items where input_id=?', (input_id,)).fetchone() or [None])[0]
        entry['answer'] = rungs.get(answer['rung'])
        entry['reasons'] = f"Reference: {answer['reference']} Implied outcome: {answer['implied_outcome']} Reasons: {answer['reasons']}"
        entry['material'] = [dict(item, publisher=publisher_of(item['input_id'])) for item in self.bc.material(request_json)]
        entry['context'] = self.bc.context(request_json, conn)
        if entry['context']['previous']:
            entry['context']['previous']['answer'] = rungs.get(entry['context']['previous']['rung'])
        return self.bc.card_text(entry, lib), rungs


def stored_answer(case):
    views, _ = jp.store_paths(case['draw'])
    j = jp.readonly(views).execute('select rung, reasons, reference, implied_outcome from judgements where judgement_id=?', (case['judgement_id'],)).fetchone()
    return dict(j)


def plants(builder, cases, answer_of, count, seed):
    """Up to `count` plants: an answer moved one rung, entered only when a separate closed reader confirms it is not supported."""
    import mark_cards
    out, confirmations = [], []
    for case in random.Random(seed).sample(cases, len(cases)):
        if len(out) >= count:
            break
        answer = answer_of(case)
        text, rungs = builder.text(case, answer)
        rung = answer['rung']
        moved = rung + 1 if rung + 1 in rungs else rung - 1
        if moved not in rungs:
            continue
        planted = text.replace(f'Latest answer at the cutoff: {rungs[rung]}', f'Latest answer at the cutoff: {rungs[moved]}', 1)
        if planted == text:
            continue
        ok, mark = mark_cards.confirmed_by_reader(planted, False)
        confirmations.append({'case': case['case'], 'moved_to': moved, 'confirmed': ok, 'mark': mark})
        if ok:
            out.append({'arm': 'plant', 'case': case['case'], 'role': 'plant', 'repeat': 1, 'rung': moved, 'stored_rung': rung,
                        'kind': 'plant', 'text': planted})
    return out, confirmations


def write_deck(folder, key_path, cards, confirmations, seed):
    if key_path.exists():
        raise SystemExit(f'refused: {key_path} exists')
    folder.mkdir(parents=True, exist_ok=False)
    random.Random(seed).shuffle(cards)
    key = {}
    for n, card in enumerate(cards, 1):
        cid = f'C{n:03d}'
        key[cid] = {k: v for k, v in card.items() if k != 'text'}
        (folder / f'{cid}.txt').write_text(card['text'])
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_text(json.dumps({'cards': key, 'invalid': [], 'plant_confirmations': confirmations}, indent=1) + '\n')
    print(len(cards), 'cards;', dict(Counter((c['arm'], c['kind']) for c in cards)))


def census_deck():
    builder = Cards()
    rows = json.loads(POOL.read_text())
    cards = []
    for case in rows:
        answer = stored_answer(case)
        text, _ = builder.text(case, answer)
        cards.append({'arm': 'stored', 'case': case['case'], 'role': 'pool', 'repeat': 0, 'rung': answer['rung'], 'stored_rung': answer['rung'],
                      'kind': 'stored', 'text': text})
    planted, confirmations = plants(builder, rows, stored_answer, jp.PLANTS, jp.SEED)
    write_deck(jp.OUT / 'deck-fresh-census', CENSUS_KEY, cards + planted, confirmations, jp.SEED)


def read(deck, key_path, marks_name, cut_day='6'):
    """The comparison's readers (jp.read). For the 09-06 sets the brief's date is set to the cut (the cards show the library as it stood
    on 6 September); the diagnostic's cards are final answers at 20 September and keep the brief as written."""
    sys.path[:0] = [str(jp.STAGE0), str(jp.STAGE0 / 'census')]
    import mark_cards
    if cut_day != '20':
        brief, count = re.subn(r'as it stood on 20\nSeptember 2026', f'as it stood on {cut_day}\nSeptember 2026', mark_cards.BRIEF)
        assert count == 1, 'the brief names the cut date once'
        mark_cards.BRIEF = brief
    jp.read(deck, key_path, marks_name)


def rejected(mark):
    answer = (mark or {}).get('answer')
    if isinstance(answer, dict):
        return set(answer['split']) <= REJECTED
    return answer in REJECTED


def select():
    """The rule in DESIGN-J2.md ("The fresh test", amended by council I), written before any fresh mark was opened. Each pooled question
    has a bet (fresh-bets.json); a bet the design read is excluded, and each remaining bet yields at most one case, from its answers in
    seeded order: a target when any answer is rejected by both readers on a question both rate worth tracking (the first such), else a
    control candidate (the first answer both support on a worth-tracking question). Controls: ceil(8n/13) candidates matched to the
    targets by type, seeded. Refused unless n >= 8, the controls are complete and every plant is unsupported by both readers."""
    marks = json.loads((jp.OUT / 'marks-fresh-census.json').read_text())
    rows = {c['case']: c for c in json.loads(POOL.read_text())}
    bets = json.loads((HERE / 'fresh-bets.json').read_text())['bets']
    assert set(bets) == set(rows), 'every pooled answer has a bet'
    by_case = {m['case']: m['marks'] for m in marks.values() if m['kind'] == 'stored'}
    missing = [c for c in rows if c not in by_case]
    if missing:
        raise SystemExit(f'{len(missing)} pooled answers not marked: refused')
    plants = {cid: m['marks'] for cid, m in marks.items() if m['kind'] == 'plant'}
    plants_caught = all((m or {}).get('answer') in REJECTED or rejected(m) for m in plants.values())
    worth = {c for c, m in by_case.items() if m.get('worth') == 'worth'}
    rng = random.Random(jp.SEED)
    groups = {}
    for case in sorted(rows):
        if not bets[case].startswith('exposed:'):
            groups.setdefault(bets[case], []).append(case)
    targets, candidates = [], []
    for bet in sorted(groups):
        order = rng.sample(groups[bet], len(groups[bet]))
        hit = next((c for c in order if c in worth and rejected(by_case[c])), None)
        if hit:
            targets.append(hit)
            continue
        good = next((c for c in order if c in worth and by_case[c].get('answer') == 'supported'), None)
        if good:
            candidates.append(good)
    need = math.ceil(8 * len(targets) / 13)
    controls = []
    for t in targets:
        if len(controls) >= need:
            break
        free = [c for c in candidates if c not in controls and rows[c]['type'] == rows[t]['type']] or [c for c in candidates if c not in controls]
        if free:
            controls.append(rng.choice(free))
    print(f'bets: {len(groups)} fresh of {len(set(bets.values()))}; worth-tracking answers {len(worth)} of {len(rows)}; targets {len(targets)} '
          f'(held the previous rung: {sum(rows[t]["held"] for t in targets)}); control candidates {len(candidates)}; controls {len(controls)} of {need}; '
          f'screen: net repairs >= {math.ceil(5 * len(targets) / 13)}; plants caught: {plants_caught} {plants}')
    print('targets', [(t, bets[t]) for t in targets])
    if len(targets) < 8 or len(controls) < need or not plants_caught:
        raise SystemExit('refused: the prerequisites of the fresh test are not met (n >= 8, controls complete, plants caught); no send')
    out = [dict(rows[c], role='target', bet=bets[c], mark=by_case[c]) for c in targets] + \
          [dict(rows[c], role='control', bet=bets[c], mark=by_case[c]) for c in controls]
    FRESH.write_text(json.dumps(out, indent=1, ensure_ascii=False))


def check(path=FRESH):
    """$0: for every fresh case and arm, the request is built; the heading is replaced exactly once in H1 and H2 and nowhere else; the
    v7 request equals the stored bytes; a synthetic answer (the stored one) passes the production check against each arm's request."""
    from hivemind import model
    rows = json.loads(path.read_text())
    for case in rows:
        request = stored_request(case['draw'], case['request_sha256'])
        _, sha = model.request_identity(arm_request(request, 'v7'))
        assert sha == case['request_sha256'], case['case']
        for arm in ('H1', 'H2'):
            sent = arm_request(request, arm)
            user, stored_user = sent['messages'][1]['content'], request['messages'][1]['content']
            assert user.replace(NEW_HEADING, OLD_HEADING) == stored_user and user.count(NEW_HEADING) == 1, (case['case'], arm)
            views, _ = jp.store_paths(case['draw'])
            j = jp.readonly(views).execute('select * from judgements where judgement_id=?', (case['judgement_id'],)).fetchone()
            synthetic = {'rung': j['rung'], 'reasons': j['reasons'], 'reference': j['reference'], 'implied_outcome': j['implied_outcome'],
                         'cites': json.loads(j['cited_evidence_json']), 'cites_views': json.loads(j['cited_views_json']),
                         'pushes': json.loads(j['pushes_json']), 'changed': bool(j['changed']), 'why_changed': j['why_changed'] or '',
                         'theme_pushes': json.loads(j['theme_pushes_json'] or '[]')}
            refused = jp.refusals_before(views, case['view_id'], case['judgement_id'], synthetic, user)
            assert not refused, (case['case'], arm, refused)
    system_h2, _ = arm_parts('H2')
    print(f'{len(rows)} fresh cases: v7 bytes equal the stored request; H1/H2 change only the heading line; the stored answer passes the '
          f'production check under each arm; H2 system differs from v7 by one sentence ({len(system_h2) - len(arm_parts("v7")[0]):+d} characters)')


SETS = {'fresh': (FRESH, 'fresh-probe', 'deck-fresh-test', 'fresh-test-key.json', 'marks-fresh-test.json', CUT),
        'diag': (jp.OUT / 'diagcases.json', 'diag-probe', 'deck-diag', 'diag-key.json', 'marks-diag.json', '2026-09-20')}


def probe(ledger_path, arm, repeats, which='fresh'):
    transport, ledger = jp.transport_for(ledger_path)
    cases_path, probe_dir, *_ = SETS[which]
    rows = json.loads(cases_path.read_text())
    folder = jp.OUT / probe_dir / arm
    folder.mkdir(parents=True, exist_ok=False)
    jobs = [(case, k) for case in rows for k in range(1, repeats + 1)]

    def one(job):
        case, k = job
        response = transport('openai', arm_request(stored_request(case['draw'], case['request_sha256']), arm))
        (folder / f"{case['case']}-{k}.json").write_text(json.dumps({'case': case['case'], 'repeat': k, 'arm': arm,
                                                                    'answer': json.loads(response['choices'][0]['message']['content']),
                                                                    'usage': response.get('usage')}, indent=1, ensure_ascii=False))
        return f"{case['case']}-{k}"

    with concurrent.futures.ThreadPoolExecutor(jp.WORKERS) as pool:
        for name in pool.map(one, jobs):
            print('probe', arm, name, flush=True)
    print('ledger', json.dumps(ledger.read()))


def gold(ledger_path, arm, repeats):
    """The frozen judgement gold's requests (goldcases.json) under the arm, scored by the frozen scorer's rule."""
    transport, ledger = jp.transport_for(ledger_path)
    entries, questions = jp.gold_entries()
    by_qid = {e['question_id']: e for e in entries}
    rows = json.loads((jp.OUT / 'goldcases.json').read_text())
    folder = jp.OUT / 'goldprobe' / arm
    folder.mkdir(parents=True, exist_ok=False)

    def one(job):
        case, k = job
        archive = jp.readonly(jp.GOLD_RUN / case['draw'] / 'archive.sqlite')
        request = json.loads(archive.execute('select request_json from model_calls where request_sha256=? limit 1', (case['request_sha256'],)).fetchone()[0])
        answer = json.loads(transport('openai', arm_request(request, arm))['choices'][0]['message']['content'])
        rung = answer['rung']
        agrees = 1 <= rung <= len(case['rungs']) and jp.gold_agrees(by_qid[case['qid']], questions[case['qid']], case['rungs'], rung)
        (folder / f"{case['case']}-{k}.json").write_text(json.dumps({'case': case['case'], 'repeat': k, 'arm': arm, 'answer': answer,
                                                                    'agrees': agrees}, indent=1, ensure_ascii=False))
        return case['draw'], k, agrees

    tally = Counter()
    with concurrent.futures.ThreadPoolExecutor(jp.WORKERS) as pool:
        for draw, k, agrees in pool.map(one, [(c, k) for c in rows for k in range(1, repeats + 1)]):
            tally[k] += agrees
    print(arm, 'gold agreement per repeat', dict(sorted(tally.items())), 'of', len(rows))
    print('ledger', json.dumps(ledger.read()))


def test_deck(arms, which='fresh'):
    cases_path, probe_dir, deck_dir, key_name, _, cut = SETS[which]
    builder = Cards(cut)
    rows = json.loads(cases_path.read_text())
    for arm in arms:
        jp.expected_files(jp.OUT / probe_dir / arm, [c['case'] for c in rows])
    answer_file = lambda arm, case, k: json.loads((jp.OUT / probe_dir / arm / f"{case['case']}-{k}.json").read_text())['answer']
    cards = []
    for arm in arms:
        for case in rows:
            for k in (1, 2, 3):
                answer = answer_file(arm, case, k)
                if answer['rung'] not in builder.bc.conditions(case['view_id'], builder.bc.ro(jp.store_paths(case['draw'])[0])):
                    cards.append({'arm': arm, 'case': case['case'], 'role': case['role'], 'repeat': k, 'rung': answer['rung'],
                                  'stored_rung': case['rung'], 'kind': 'invalid rung', 'text': None})
                    continue
                text, _ = builder.text(case, answer)
                cards.append({'arm': arm, 'case': case['case'], 'role': case['role'], 'repeat': k, 'rung': answer['rung'],
                              'stored_rung': case['rung'], 'kind': 'probe', 'text': text})
    invalid = [c for c in cards if c['text'] is None]
    controls = [c for c in rows if c['role'] == 'control']
    planted, confirmations = plants(builder, controls, lambda case: answer_file('v7', case, 1), jp.PLANTS, jp.SEED + 1)
    key_path = KEYS / key_name
    write_deck(jp.OUT / deck_dir, key_path, [c for c in cards if c['text'] is not None] + planted, confirmations, jp.SEED + 1)
    if invalid:
        key = json.loads(key_path.read_text())
        key['invalid'] = [{k: v for k, v in c.items() if k != 'text'} for c in invalid]
        key_path.write_text(json.dumps(key, indent=1) + '\n')
        print('invalid rungs', len(invalid))


def score(arm, control='v7', which='fresh'):
    """The screen (DESIGN-J2.md, "The fresh test"): per case, jointly supported (both readers' final answer mark `supported`) in at
    least 2 of 3 repeats; net target repairs (the arm holds, v7 does not, minus the reverse) at least ceil(5n/13); no control lost; the
    arm's refusals, recomputed against the request each answer received on the store as of the stored judgement, not above v7's. An
    invalid rung counts as refused and not supported."""
    cases_path, probe_dir, _, key_name, marks_name, _ = SETS[which]
    key = json.loads((KEYS / key_name).read_text())
    marks = json.loads((jp.OUT / marks_name).read_text())
    rows = {c['case']: c for c in json.loads(cases_path.read_text())}
    supported = {(m['arm'], m['case'], m['repeat']): (m['marks'] or {}).get('answer') == 'supported' for m in marks.values() if m['kind'] == 'probe'}
    invalid = {(c['arm'], c['case'], c['repeat']) for c in key['invalid']}
    for item in invalid:
        supported[item] = False
    arms = (control, arm)
    missing = [(a, c, r) for a in arms for c in rows for r in (1, 2, 3) if (a, c, r) not in supported]
    if missing:
        raise SystemExit(f'{len(missing)} answers not marked, e.g. {missing[:4]}: refused')
    refused = Counter()
    for a in arms:
        for name, case in rows.items():
            user = arm_user(stored_request(case['draw'], case['request_sha256'])['messages'][1]['content'], a)
            views, _ = jp.store_paths(case['draw'])
            for r in (1, 2, 3):
                if (a, name, r) in invalid:
                    refused[a] += 1
                    continue
                answer = json.loads((jp.OUT / probe_dir / a / f'{name}-{r}.json').read_text())['answer']
                if jp.refusals_before(views, case['view_id'], case['judgement_id'], answer, user):
                    refused[a] += 1
                    supported[(a, name, r)] = False      # council I: a refused answer is not supported
    plants = {cid: m['marks'] for cid, m in marks.items() if m['kind'] == 'plant'}
    if not all(rejected(m) for m in plants.values()):
        raise SystemExit(f'a plant was not caught by both readers: the reading is void {plants}')
    holds = {a: {c: sum(supported[(a, c, r)] for r in (1, 2, 3)) >= 2 for c in rows} for a in arms}
    targets = sorted(c for c in rows if rows[c]['role'] == 'target')
    controls = sorted(c for c in rows if rows[c]['role'] == 'control')
    repaired = [t for t in targets if holds[arm][t] and not holds[control][t]]
    broken = [t for t in targets if holds[control][t] and not holds[arm][t]]
    lost = [c for c in controls if holds[control][c] and not holds[arm][c]]
    line = 2 if which == 'diag' else math.ceil(5 * len(targets) / 13)     # council J: two net repairs of three
    moved = {a: sum(sum(json.loads((jp.OUT / probe_dir / a / f'{t}-{r}.json').read_text())['answer']['rung'] != rows[t]['rung'] for r in (1, 2, 3)) >= 2
                    for t in targets) for a in arms}
    report = {'arm': arm, 'targets': len(targets), 'controls': len(controls), 'line': line,
              'targets held': {a: sum(holds[a][t] for t in targets) for a in arms}, 'targets moved off the stored rung (2 of 3)': moved,
              'controls held': {a: sum(holds[a][c] for c in controls) for a in arms}, 'repaired': repaired, 'broken': broken,
              'net': len(repaired) - len(broken), 'controls lost': lost, 'refused': dict(refused),
              'plants': {cid: m['marks'] for cid, m in marks.items() if m['kind'] == 'plant'},
              'screen passes': len(repaired) - len(broken) >= line and not lost and refused[arm] <= refused[control],
              'inconclusive': which == 'diag' and len(targets) - sum(holds[control][t] for t in targets) < 2}
    print(json.dumps(report, indent=1, ensure_ascii=False))
    (jp.OUT / f'{which}-score-{arm}.json').write_text(json.dumps(report, indent=1, ensure_ascii=False))



# ---- Council J's diagnostic: H1 against same-day v7 on the three clearest motivating cases and two controls ----------------------
DIAG_TARGETS = ('T-old-3-Q3', 'T-old-3-Q37', 'T-old-1-Q7')   # three bets; v7 kept the rejected rung 3/3, without the previous conclusion 3/3 moved
DIAG = jp.OUT / 'diagcases.json'
DIAG_KEY = KEYS / 'diag-key.json'


def diag_cases():
    """$0: the three targets, and two controls chosen with seed 20261120 among the controls that carry hidden evidence (1..100 pieces),
    were jointly supported in 3 of 3 v7 re-sends (marks-probe.json), and are not on a target's bet (FY2027 revenue, FY2028 gross margin,
    2027 capex); each with its stored final request, rebuilt byte for byte."""
    from hivemind import model
    cases = {c['case']: c for c in json.loads((jp.OUT / 'cases.json').read_text())}
    hidden = {c['case']: c['hidden'] for c in json.loads((jp.OUT / 'fullcases.json').read_text())}
    marks = json.loads((jp.OUT / 'marks-probe.json').read_text())
    held = Counter(m['case'] for m in marks.values() if m['kind'] == 'probe' and m['arm'] == 'v7' and (m['marks'] or {}).get('answer') == 'supported')
    target_bets = {'C-old-1-Q34', 'C-old-2-Q33', 'C-old-2-Q28', 'C-old-3-Q31', 'C-old-3-Q4'}     # FY2028/FY2027 gross margin, FY2028 revenue: the targets' neighbours
    pool = sorted(c for c in cases if cases[c]['role'] == 'control' and 1 <= hidden.get(c, 0) <= 100 and held[c] == 3 and c not in target_bets)
    controls = random.Random(jp.SEED).sample(pool, 2)
    out = []
    for name in DIAG_TARGETS + tuple(controls):
        case = cases[name]
        judgement, request, _, _ = jp.stored(case)
        _, sha = model.request_identity(arm_request(request, 'v7'))
        assert sha == judgement['request_sha256'], name
        out.append(dict(case, request_sha256=judgement['request_sha256'], judgement_id=judgement['judgement_id'], rung=judgement['rung']))
    DIAG.write_text(json.dumps(out, indent=1))
    print('control pool', pool, '-> controls', controls)
    print(len(out), 'cases rebuilt byte for byte; the heading replaced once in each:', all(OLD_HEADING in jp.stored(c)[1]['messages'][1]['content'] for c in out))


if __name__ == '__main__':
    command = sys.argv[1]
    if command == 'pool':
        pool()
    elif command == 'censusdeck':
        census_deck()
    elif command == 'censusread':
        read('deck-fresh-census', CENSUS_KEY, 'marks-fresh-census.json')
    elif command == 'select':
        select()
    elif command == 'check':
        check(POOL if sys.argv[2:] == ['pool'] else FRESH)
    elif command == 'probe':
        probe(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif command == 'gold':
        gold(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif command == 'testdeck':
        test_deck(sys.argv[2:])
    elif command == 'testread':
        read('deck-fresh-test', TEST_KEY, 'marks-fresh-test.json')
    elif command == 'score':
        score(sys.argv[2])
    elif command == 'diagcases':
        diag_cases()
    elif command == 'diagprobe':
        probe(sys.argv[2], sys.argv[3], int(sys.argv[4]), 'diag')
    elif command == 'diagdeck':
        test_deck(sys.argv[2:], 'diag')
    elif command == 'diagread':
        read('deck-diag', DIAG_KEY, 'marks-diag.json', cut_day='20')
    elif command == 'diagscore':
        score(sys.argv[2], which='diag')
    else:
        raise SystemExit(__doc__)
