"""Phase 1 of the hybrid plan (PLAN.md): the judge's stored final requests on the 24 answers both readers rejected, and matched
controls both readers supported, re-sent with a judge variant.

  python3 judge_probe.py cases                  # $0: cases.json (targets and matched controls, with their stored requests' ids)
  python3 judge_probe.py check                  # $0: every stored request rebuilt byte for byte from code (schema) + system file + user
  python3 judge_probe.py account <ledger>       # cents: the model's own account on the targets, continuing the stored conversation
  python3 judge_probe.py probe <ledger> <arm> <repeats>   # cents: each case's request with the arm's system text, sent <repeats> times
  python3 judge_probe.py goldcases              # $0: the frozen judgement gold's questions in the r9-frozen-v108 draws, last request at 07-14
  python3 judge_probe.py goldprobe <ledger> <arm> <repeats>  # cents: those requests under the arm, scored by the frozen gold's rule
  python3 judge_probe.py goldscore <arm>         # $0: the gold probe's agreement and refusals, complete coverage required
  python3 judge_probe.py deck <arm> [<arm> ...]  # $0 + plant confirmations: blind cards of every answer of every arm and repeat
  python3 judge_probe.py probescore             # $0: the locked rule (a)(b)(d) per arm against v7's re-send, after read
  python3 judge_probe.py read                   # both reader families mark the deck, debate rounds 1 and 2; marks.json
  python3 judge_probe.py forkcases              # $0: per target, the request where its final (rejected) rung was first chosen
  python3 judge_probe.py forkprobe <ledger> <arm> <repeats>  # cents: those requests under the arm
  python3 judge_probe.py forkscore              # $0: per arm, targets that repeat the rejected rung in >= 2 of 3 repeats
  python3 judge_probe.py window <draw> replay    # $0: the whole window 07-01..09-20 judge-only, answered with old's archived answers
  python3 judge_probe.py window <draw> <arm> <ledger>  # paid: the same under the arm, each arm building its own conclusions
  python3 judge_probe.py prodpath replay        # $0: the production-path copy answered with old's archived answers; request bytes checked
  python3 judge_probe.py prodpath <arm> <ledger>   # paid: the same two days through the judge's own round under the arm, empty archive

An arm is a system-text file arms/<arm>.txt; arm 'v7' is the frozen judging-v7.txt itself (the control arm). The stored stores are read
through read-only connections."""
import concurrent.futures
import importlib.util
import json
import random
import sqlite3
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT / 'src')]
RUN = ROOT / 'poc/data/comparison-2026-11-17/run'
DIAG = ROOT / 'poc/data/comparison-2026-11-17/reading-diagnostic'
KEYS = Path.home() / '.hivemind-keys/comparison-2026-11-17'
OUT = ROOT / 'poc/data/hybrid-2026-11-20'
FROZEN_SYSTEM = ROOT / 'src/hivemind/prompts/judging-v7.txt'
CONFIG = ROOT / 'poc/config/poc-v118.json'
# The 24 answers both readers rejected (census/CENSUS.md), by draw and deck label, with their census class.
TARGETS = {
    ('new-2', 'Q11'): 'E', ('new-2', 'Q20'): 'E', ('new-2', 'Q26'): 'S', ('new-2', 'Q27'): 'M', ('new-2', 'Q31'): 'S',
    ('new-2', 'Q4'): 'M', ('new-2', 'Q5'): 'R', ('new-3', 'Q23'): 'M', ('new-3', 'Q26'): 'E', ('new-3', 'Q4'): 'R',
    ('old-1', 'Q28'): 'S', ('old-1', 'Q45'): 'W', ('old-1', 'Q7'): 'S', ('old-2', 'Q16'): 'O', ('old-2', 'Q29'): 'O',
    ('old-2', 'Q6'): 'S', ('old-2', 'Q9'): 'E', ('old-3', 'Q14'): 'O', ('old-3', 'Q23'): 'W', ('old-3', 'Q3'): 'O',
    ('old-3', 'Q33'): 'O', ('old-3', 'Q37'): 'O', ('old-3', 'Q41'): 'E', ('old-3', 'Q7'): 'S',
}
SEED = 20261120
GOLD = ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold'
GOLD_SHA256 = '636c056d1e4252fa759660803067e6ccd67a81067b012905e918aa9dec4005f2'
GOLD_RUN = ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03'
GOLD_DAY = '2026-07-14'
STAGE0 = ROOT / 'docs/research/2026-11-17-product-comparison/stage0'
PROBE_KEY = Path.home() / '.hivemind-keys/hybrid-2026-11-20/probe-key.json'
PLANTS = 3
MERGE_TEST = ROOT / 'docs/research/2026-11-19-merge-council/merge_test.py'
PRODPATH_DRAW = 'old-2'
PRODPATH_BOUNDARY = '2026-09-16'                    # the copy holds what existed at the end of this day
PRODPATH_DAYS = ('2026-09-17', '2026-09-18')        # theme v5 changed on 09-18 and queued the asset theses (old-2's own run)
READER_SESSIONS = 12  # closed reader sessions at once
WORKERS = 24          # judge calls at once (production judges 32 at a time, AGENTS §9)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def store_paths(draw):
    """(views, archive) of a finished comparison draw, as the comparison's mapping read them."""
    root = RUN / draw
    record = json.loads((root / 'run.json').read_text())
    if draw.startswith('new'):
        judge = record['components']['judge']
        inner = json.loads((root / judge['folder'] / 'run.json').read_text())[draw]
        folder = root / judge['folder'] / inner['attempts'][-1]['folder']
    else:
        folder = root / record['components']['prod']['folder']
    return folder / 'views.sqlite', folder / 'archive.sqlite'


def readonly(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def cases():
    """Targets, and per target one control from the same draw and of the same type that both readers marked worth tracking and
    supported (seeded choice, no control used twice)."""
    readings = json.loads((DIAG / 'deck/readings.json').read_text())['cards']
    library_of = json.loads((KEYS / 'mapping-key-diagnostic.json').read_text())
    deck_key = json.loads((KEYS / 'deck-key.json').read_text())
    card_of = {(v['draw'], v['question']): c for c, v in deck_key.items() if v.get('role') == 'product'}
    rng = random.Random(SEED)
    out, used = [], set()
    for (draw, label), census_class in sorted(TARGETS.items()):
        library = {e['question_id']: e for e in json.loads((DIAG / f'mapping-out/library-{library_of[draw]}.json').read_text())}
        mark = readings[draw][label]
        assert mark['worth'] == 'worth' and mark['answer'] != 'supported', (draw, label, mark)
        out.append({'case': f'T-{draw}-{label}', 'role': 'target', 'draw': draw, 'label': label, 'view_id': library[label]['source_id'],
                    'type': mark['type'], 'class': census_class, 'card': card_of[(draw, label)], 'mark': mark['answer']})
        pool = sorted(q for q, m in readings[draw].items()
                      if m['worth'] == 'worth' and m['answer'] == 'supported' and m['type'] == mark['type'] and (draw, q) not in used
                      and (draw, q) not in TARGETS and (draw, q) in card_of)
        pick = rng.choice(pool)
        used.add((draw, pick))
        out.append({'case': f'C-{draw}-{pick}', 'role': 'control', 'draw': draw, 'label': pick, 'view_id': library[pick]['source_id'],
                    'type': mark['type'], 'class': None, 'card': card_of[(draw, pick)], 'mark': 'supported'})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'cases.json').write_text(json.dumps(out, indent=1))
    print(len(out), 'cases:', sum(c['role'] == 'target' for c in out), 'targets,', sum(c['role'] == 'control' for c in out), 'controls')


def stored(case):
    """The latest stored judgement of the case's view and its archived request and answer."""
    views, archive = store_paths(case['draw'])
    v = readonly(views)
    j = v.execute('select * from judgements where view_id=? order by seq desc limit 1', (case['view_id'],)).fetchone()
    a = readonly(archive)
    row = a.execute('select request_json, response_json, answer_json from model_calls where request_sha256=? limit 1', (j['request_sha256'],)).fetchone()
    return dict(j), json.loads(row['request_json']), json.loads(row['response_json']), json.loads(row['answer_json'])


def without_previous(user):
    """The request's user text with the previous conclusion removed (council F: pair identical requests with and without it): the
    "[Previous conclusion, for comparison only] …" block and the "[Not shown: …; the previous conclusion carries them]" line."""
    import re
    start = user.find('\n\n[Previous conclusion, for comparison only]')
    if start >= 0:
        end = user.find('\n\nAnswer per the JSON schema.', start)
        assert end > start, 'the previous conclusion block runs to the closing sentence'
        user = user[:start] + user[end:]
    return re.sub(r'^\[Not shown: \d+ more pieces in force, read in earlier judgements; the previous conclusion carries them\]\n?', '', user, flags=re.M)


def rebuild(stored_request, system_text, order=None, strip_previous=False):
    """The request as production builds it (model.build_request, key order and schema from code), with the given system text. With
    `order`, the schema's properties are written in that order (the same fields and types; the model writes fields in this order)."""
    from hivemind import config, model
    from hivemind.views import judging
    cfg = config.load(CONFIG)
    user = stored_request['messages'][1]['content']
    if strip_previous:
        user = without_previous(user)
    schema = judging.schema_for(cfg.rejudging.prompt_version)
    if order is not None:
        assert sorted(order) == sorted(schema['properties']), 'an order names exactly the schema fields'
        schema['properties'] = {field: schema['properties'][field] for field in order}
    return model.build_request(cfg.rejudging, system_text, user, schema, 'judgement', cfg.provider)


def arm_spec(arm):
    """(system text, schema order or None) of an arm; 'v7' is the frozen judge as stored; a '-noprev' suffix names the same arm sent
    without the previous conclusion (see `strips_previous`)."""
    for suffix in ('-fullnoprev', '-fullprev', '-noprev'):
        if arm.endswith(suffix):
            arm = arm[:-len(suffix)]
            break
    if arm == 'v7':
        return FROZEN_SYSTEM.read_text(encoding='utf-8'), None
    order_file = HERE / 'arms' / f'{arm}.order.json'
    return (HERE / 'arms' / f'{arm}.txt').read_text(encoding='utf-8'), (json.loads(order_file.read_text()) if order_file.exists() else None)


def check():
    """$0: each stored request, rebuilt from the frozen system file, code's schema and the stored user text, has the stored sha."""
    from hivemind import model
    frozen = FROZEN_SYSTEM.read_text(encoding='utf-8')
    rows = json.loads((OUT / 'cases.json').read_text())
    bad = []
    for case in rows:
        judgement, request, _, _ = stored(case)
        _, sha = model.request_identity(rebuild(request, frozen))
        if sha != judgement['request_sha256']:
            bad.append(case['case'])
    print(f'{len(rows) - len(bad)} of {len(rows)} stored requests rebuilt byte for byte', 'mismatch: ' + ', '.join(bad) if bad else '')
    if bad:
        raise SystemExit(1)


def transport_for(ledger_path):
    budget_replay = load('budget_replay', ROOT / 'clean-arch/e2e-comparison-2026-11-13/budget_replay.py')
    ledger = budget_replay.SharedLedger(ledger_path)
    return budget_replay.BudgetTransport(ledger), ledger


ACCOUNT_QUESTION = ('Look back at the answer you just gave. Which sentence of your instructions led you to this rung? Quote it. Which two '
                    'statements in the evidence did you set aside or weigh least, and why? Answer in under 150 words.')


def account(ledger_path):
    """Cents: the stored conversation of each target, continued with one question; plain text, no schema."""
    transport, ledger = transport_for(ledger_path)
    rows = [c for c in json.loads((OUT / 'cases.json').read_text()) if c['role'] == 'target']
    folder = OUT / 'account'
    folder.mkdir(parents=True, exist_ok=True)

    def one(case):
        _, request, response, _ = stored(case)
        follow = {'model': request['model'],
                  'messages': request['messages'] + [{'role': 'assistant', 'content': response['choices'][0]['message']['content']},
                                                     {'role': 'user', 'content': ACCOUNT_QUESTION}],
                  'max_completion_tokens': 4000, 'reasoning_effort': request.get('reasoning_effort', 'medium')}
        answer = transport('openai', follow)
        text = answer['choices'][0]['message']['content']
        (folder / f"{case['case']}.json").write_text(json.dumps({'case': case, 'question': ACCOUNT_QUESTION, 'account': text,
                                                                'usage': answer.get('usage')}, indent=1, ensure_ascii=False))
        return case['case']

    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        for name in pool.map(one, rows):
            print('account', name, flush=True)
    print('ledger', json.dumps(ledger.read()))


def probe(ledger_path, arm, repeats):
    """Cents: each case's rebuilt request with the arm's system text, sent `repeats` times, each answer stored with its usage."""
    transport, ledger = transport_for(ledger_path)
    system, order = arm_spec(arm)
    rows = json.loads((OUT / 'cases.json').read_text())
    full = arm.endswith('-fullprev') or arm.endswith('-fullnoprev')
    if full:                                   # council G: the cases with 1..100 hidden pieces, every piece in force shown
        rows = [c for c in json.loads((OUT / 'fullcases.json').read_text()) if c['hidden'] >= 1]
    folder = OUT / 'probe' / arm
    folder.mkdir(parents=True, exist_ok=False)
    jobs = [(case, k) for case in rows for k in range(1, repeats + 1)]

    def one(job):
        case, k = job
        _, request, _, _ = stored(case)
        if full:
            request = dict(request, messages=[request['messages'][0], dict(request['messages'][1], content=case['user_full'])])
        strip = arm.endswith('-noprev') or arm.endswith('-fullnoprev')
        response = transport('openai', rebuild(request, system, order, strip_previous=strip))
        content = response['choices'][0]['message']['content']
        (folder / f"{case['case']}-{k}.json").write_text(json.dumps({'case': {x: case[x] for x in case if not x.startswith('user_')}, 'repeat': k, 'arm': arm, 'answer': json.loads(content),
                                                                    'usage': response.get('usage')}, indent=1, ensure_ascii=False))
        return f"{case['case']}-{k}"

    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        for name in pool.map(one, jobs):
            print('probe', name, flush=True)
    print('ledger', json.dumps(ledger.read()))


def gold_entries():
    """The frozen judgement gold (refused unless its sha256 is the frozen one) and its questions."""
    import hashlib
    raw = (GOLD / 'gold-v1.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != GOLD_SHA256:
        raise SystemExit('gold-v1.json is not the frozen gold: refused')
    questions = {q['id']: q for q in json.loads((GOLD / 'questions-v1.json').read_text(encoding='utf-8'))['questions']}
    return json.loads(raw)['entries'], questions


def gold_agrees(entry, question, rungs, rung):
    """The frozen scorer's rule (score_judgement.py): a numeric question agrees when the gold's implied range overlaps the chosen rung's
    band; a yes/no question when the answers match."""
    resolved = entry.get('resolution') or entry
    implied = resolved['implied_outcome']
    chosen = rungs[rung - 1]
    if question['unit'] == 'yes/no':
        return (chosen['label'].lower() == 'yes') == bool(implied['yes_no'])
    lo, hi = chosen['lo'], chosen['hi']
    return (lo is None or implied['high'] >= lo) and (hi is None or implied['low'] < hi)


def goldcases():
    """$0: per r9 draw and gold question with a gold outcome, the view's last judgement at or before 07-14, its stored request rebuilt
    byte for byte under the frozen judge (the check), and the stored rung's agreement as the scorer computes it."""
    from hivemind import model
    entries, questions = gold_entries()
    frozen = FROZEN_SYSTEM.read_text(encoding='utf-8')
    out, bad = [], []
    for draw in ('d1', 'd2', 'd3'):
        views = readonly(GOLD_RUN / draw / 'views.sqlite')
        archive = readonly(GOLD_RUN / draw / 'archive.sqlite')
        mapping = {f'q{k:02d}': f'v{k}' for k in range(1, 23)}
        for qid, vid in mapping.items():
            row = views.execute('select question from views where view_id=?', (vid,)).fetchone()
            if not row or row['question'] != questions[qid]['question']:
                raise SystemExit(f'{draw} {vid} is not the seed question {qid}: refused')
        hit = views.execute("select view_id from views where question like '%Ohio%' and question like '%guarantee%' order by created_seq limit 1").fetchone()
        if hit:
            mapping['q23'] = hit['view_id']
        for entry in entries:
            qid = entry['question_id']
            if entry.get('no_view') or not entry.get('implied_outcome') or qid not in mapping:
                continue
            vid = mapping[qid]
            j = views.execute('select * from judgements where view_id=? and publication_day<=? order by judgement_id desc limit 1', (vid, GOLD_DAY)).fetchone()
            if j is None:
                continue
            rungs = [dict(r) for r in views.execute('select position, label, lo, hi from rungs where view_id=? order by position', (vid,))]
            request = json.loads(archive.execute('select request_json from model_calls where request_sha256=? limit 1', (j['request_sha256'],)).fetchone()[0])
            _, sha = model.request_identity(rebuild(request, frozen))
            if sha != j['request_sha256']:
                bad.append(f'{draw}-{qid}')
            out.append({'case': f'G-{draw}-{qid}', 'draw': draw, 'qid': qid, 'view_id': vid, 'request_sha256': j['request_sha256'],
                        'stored_rung': j['rung'], 'stored_agrees': gold_agrees(entry, questions[qid], rungs, j['rung']), 'rungs': rungs})
    (OUT / 'goldcases.json').write_text(json.dumps(out, indent=1))
    for draw in ('d1', 'd2', 'd3'):
        rows = [c for c in out if c['draw'] == draw]
        print(draw, f"stored agreement {sum(c['stored_agrees'] for c in rows)}/{len(rows)}")
    print(f'{len(out) - len(bad)} of {len(out)} gold requests rebuilt byte for byte', 'mismatch: ' + ', '.join(bad) if bad else '')
    if bad:
        raise SystemExit(1)


def goldprobe(ledger_path, arm, repeats):
    """Cents: each gold case's request under the arm, sent `repeats` times; agreement by the frozen scorer's rule, per draw and repeat."""
    transport, ledger = transport_for(ledger_path)
    system, order = arm_spec(arm)
    entries, questions = gold_entries()
    by_qid = {e['question_id']: e for e in entries}
    rows = json.loads((OUT / 'goldcases.json').read_text())
    folder = OUT / 'goldprobe' / arm
    folder.mkdir(parents=True, exist_ok=False)
    jobs = [(case, k) for case in rows for k in range(1, repeats + 1)]

    def one(job):
        case, k = job
        archive = readonly(GOLD_RUN / case['draw'] / 'archive.sqlite')
        request = json.loads(archive.execute('select request_json from model_calls where request_sha256=? limit 1', (case['request_sha256'],)).fetchone()[0])
        response = transport('openai', rebuild(request, system, order, strip_previous=arm.endswith('-noprev')))
        answer = json.loads(response['choices'][0]['message']['content'])
        rung = answer['rung']
        agrees = 1 <= rung <= len(case['rungs']) and gold_agrees(by_qid[case['qid']], questions[case['qid']], case['rungs'], rung)
        (folder / f"{case['case']}-{k}.json").write_text(json.dumps({'case': case['case'], 'repeat': k, 'arm': arm, 'answer': answer,
                                                                    'agrees': agrees, 'usage': response.get('usage')}, indent=1, ensure_ascii=False))
        return case['draw'], k, agrees

    tally = {}
    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        for draw, k, agrees in pool.map(one, jobs):
            tally.setdefault((draw, k), [0, 0])
            tally[(draw, k)][0] += agrees
            tally[(draw, k)][1] += 1
    for (draw, k), (a, n) in sorted(tally.items()):
        print(f'{arm} {draw} repeat {k}: agreement {a}/{n}')
    print('ledger', json.dumps(ledger.read()))


def probe_card(case, answer):
    """The comparison card of the case (same question, choices, material and library list) with the probe's answer: its rung's label,
    and the reference, implied outcome and reasons, labelled, the same way for every arm."""
    import re
    text = (DIAG / 'deck' / f"{case['card']}.txt").read_text()
    choices = re.findall(r'^(\d+)\. (.*)$', text.split('Possible answers', 1)[1].split('\n\n', 1)[0], re.M)
    labels = {int(k): v for k, v in choices}
    rung = answer['rung']
    if rung not in labels:
        return None
    reason = f"Reference: {answer['reference']} Implied outcome: {answer['implied_outcome']} Reasons: {answer['reasons']}"
    lines = text.split('\n')
    answer_line = next(i for i, line in enumerate(lines) if line.startswith('Latest answer at the cutoff: '))
    assert lines[answer_line + 1].startswith('Reason given: ')
    lines[answer_line] = f'Latest answer at the cutoff: {labels[rung]}'
    lines[answer_line + 1] = f'Reason given: {reason}'
    return '\n'.join(lines), labels


def refusals_before(views_path, view_id, judgement_id, answer, request_text):
    """The production check's refusals of an answer (`judging.check_answer` against the request it answered) on the store as it stood
    immediately before the stored judgement: later judgements are shadowed by a temporary table on a read-only connection (council C:
    the stored final judgement is not the previous one)."""
    from hivemind.views import judging
    conn = readonly(views_path)
    conn.execute('create temp table judgements as select * from main.judgements where judgement_id < ?', (judgement_id,))
    return judging.check_answer(conn, view_id, answer, request_text)


def refusals(case, answer):
    views, _ = store_paths(case['draw'])
    judgement, request, _, _ = stored(case)
    return refusals_before(views, case['view_id'], judgement['judgement_id'], answer, request['messages'][1]['content'])


def expected_files(folder, names, repeats=3):
    """Refuse unless every expected answer file exists (council C: complete coverage before scoring)."""
    missing = [f'{n}-{k}' for n in names for k in range(1, repeats + 1) if not (folder / f'{n}-{k}.json').exists()]
    if missing:
        raise SystemExit(f'{folder}: {len(missing)} expected answers missing, e.g. {missing[:5]}: refused')


def goldscore(arm):
    """$0: the gold probe of an arm, complete coverage required: per draw and repeat, agreement by the frozen scorer's rule, the
    production check's refusals (against the state before the stored judgement), and agreement counting a refused answer as not
    agreeing."""
    entries, questions = gold_entries()
    by_qid = {e['question_id']: e for e in entries}
    rows = json.loads((OUT / 'goldcases.json').read_text())
    folder = OUT / 'goldprobe' / arm
    expected_files(folder, [c['case'] for c in rows])
    tally = {}
    for case in rows:
        views = readonly(GOLD_RUN / case['draw'] / 'views.sqlite')
        judgement_id = views.execute('select judgement_id from judgements where request_sha256=? and view_id=?',
                                     (case['request_sha256'], case['view_id'])).fetchone()[0]
        archive = readonly(GOLD_RUN / case['draw'] / 'archive.sqlite')
        request = json.loads(archive.execute('select request_json from model_calls where request_sha256=? limit 1', (case['request_sha256'],)).fetchone()[0])
        for k in (1, 2, 3):
            record = json.loads((folder / f"{case['case']}-{k}.json").read_text())
            refused = refusals_before(GOLD_RUN / case['draw'] / 'views.sqlite', case['view_id'], judgement_id, record['answer'],
                                      request['messages'][1]['content'])
            t = tally.setdefault((case['draw'], k), {'agree': 0, 'refused': 0, 'agree_not_refused': 0, 'n': 0})
            t['n'] += 1
            t['agree'] += record['agrees']
            t['refused'] += bool(refused)
            t['agree_not_refused'] += record['agrees'] and not refused
    per_repeat = {k: sum(t['agree'] for (d, kk), t in tally.items() if kk == k) for k in (1, 2, 3)}
    strict = {k: sum(t['agree_not_refused'] for (d, kk), t in tally.items() if kk == k) for k in (1, 2, 3)}
    refused = sum(t['refused'] for t in tally.values())
    print(f'{arm}: agreement per repeat {per_repeat} of {len(rows)}; counting refused as not agreeing {strict}; refused answers {refused} of {3 * len(rows)}')
    return per_repeat, strict, refused


def deck(arms):
    """Blind deck: every probe answer of every arm and repeat (council B: a same-rung answer can be better or worse reasoned), with the
    production check's refusals recorded in the key, and plants
    (a control's v7 answer moved one rung, entered only when a separate closed reader confirms it is not supported). Shuffled; the key
    is kept outside the repository and never overwritten."""
    sys.path[:0] = [str(STAGE0), str(STAGE0 / 'census')]
    import mark_cards
    if PROBE_KEY.exists():
        raise SystemExit(f'refused: {PROBE_KEY} exists')
    folder = OUT / 'deck-probe'
    folder.mkdir(parents=True, exist_ok=False)
    rows = {c['case']: c for c in json.loads((OUT / 'cases.json').read_text())}
    for arm in arms:
        expected_files(OUT / 'probe' / arm, list(rows))
    stored_rung = {name: stored(case)[0]['rung'] for name, case in rows.items()}
    rng = random.Random(SEED)
    cards = []
    for arm in arms:
        for path in sorted((OUT / 'probe' / arm).glob('*.json')):
            record = json.loads(path.read_text())
            case = rows[record['case']['case']]
            built = probe_card(case, record['answer'])
            item = {'arm': arm, 'case': case['case'], 'role': case['role'], 'repeat': record['repeat'], 'rung': record['answer']['rung'],
                    'stored_rung': stored_rung[case['case']], 'kind': 'probe'}
            if built is None:                      # counted as refused and not supported by probescore (council D)
                item['kind'] = 'invalid rung'
                item['refusals'] = refusals(case, record['answer'])
                cards.append(dict(item, text=None))
                continue
            item['text'] = built[0]
            item['changed'] = item['rung'] != item['stored_rung']
            item['refusals'] = refusals(case, record['answer'])
            cards.append(item)
    confirmations = []
    controls = [c for c in rows.values() if c['role'] == 'control']
    for case in rng.sample(controls, len(controls)):
        if sum(c['kind'] == 'plant' for c in cards) >= PLANTS:
            break
        record = json.loads((OUT / 'probe' / 'v7' / f"{case['case']}-1.json").read_text())
        built = probe_card(case, record['answer'])
        if built is None:
            continue
        text, labels = built
        rung = record['answer']['rung']
        moved = rung + 1 if rung + 1 in labels else rung - 1
        if moved not in labels:
            continue
        planted = text.replace(f'Latest answer at the cutoff: {labels[rung]}', f'Latest answer at the cutoff: {labels[moved]}', 1)
        ok, mark = mark_cards.confirmed_by_reader(planted, False)
        confirmations.append({'case': case['case'], 'moved_to': moved, 'confirmed': ok, 'mark': mark})
        if ok:
            cards.append({'arm': 'plant', 'case': case['case'], 'role': 'plant', 'repeat': 1, 'rung': moved, 'stored_rung': rung,
                          'kind': 'plant', 'text': planted})
    readable = [c for c in cards if c['text'] is not None]
    rng.shuffle(readable)
    key = {}
    for n, card in enumerate(readable, 1):
        cid = f'C{n:03d}'
        key[cid] = {k: v for k, v in card.items() if k != 'text'}
        (folder / f'{cid}.txt').write_text(card['text'])
    PROBE_KEY.parent.mkdir(parents=True, exist_ok=True)
    PROBE_KEY.write_text(json.dumps({'cards': key, 'invalid': [c for c in cards if c['text'] is None], 'plant_confirmations': confirmations},
                                    indent=1) + '\n')
    from collections import Counter
    print(len(readable), 'cards;', dict(Counter((c['arm'], c['kind']) for c in readable)), '; invalid rungs:', sum(c['text'] is None for c in cards))


def read(deck='deck-probe', key_path=None, marks_name='marks-probe.json'):
    """Both reader families mark every card of a deck (mark_cards.mark), then debate rounds 1 and 2; the marks beside the deck's key
    fields. The readers' tool reads a flat key ({card: {"answered": ...}}), written beside the deck's key; a round with void marks is
    run again, up to three times."""
    sys.path[:0] = [str(STAGE0), str(STAGE0 / 'census')]
    import mark_cards
    key_path = key_path or PROBE_KEY
    key = json.loads(key_path.read_text())['cards']
    flat = key_path.parent / (key_path.stem + '-flat.json')
    if not flat.exists():
        flat.write_text(json.dumps({cid: dict(card, answered=True) for cid, card in key.items()}, indent=1) + '\n')
    mark_cards.KEY = flat
    import concurrent.futures as futures

    class Wider(futures.ThreadPoolExecutor):            # the readers' tool runs 6 sessions at once
        def __init__(self, max_workers=None, **options):
            super().__init__(max_workers=READER_SESSIONS, **options)
    mark_cards.concurrent.futures.ThreadPoolExecutor = Wider
    folder = OUT / deck
    for attempt in range(3):
        if not (folder / 'round-0.done').exists():
            mark_cards.mark(folder)
    for round_number in (1, 2):
        for attempt in range(3):
            if not (folder / f'round-{round_number}.done').exists():
                mark_cards.debate(folder, round_number)
    finals = {cid: mark_cards.final(folder, cid) for cid in sorted(key)}
    (OUT / marks_name).write_text(json.dumps({cid: dict(key[cid], marks=finals[cid]) for cid in key}, indent=1, ensure_ascii=False))
    print('marked', len(finals))


FULL_KEY = Path.home() / '.hivemind-keys/hybrid-2026-11-20/deck-full-key.json'


def deck_full(arms=('v7-fullprev', 'v7-fullnoprev')):
    """Council G's blind deck: every repeat of every full-evidence case in both arms. Each card is built by the comparison's own card
    builder from the request the answer actually received (full evidence, with or without the previous conclusion), with the answer's
    reference, implied outcome and reasons; plus plants (a control's full+prev answer moved one rung, entered only when a separate
    closed reader confirms it is not supported). Shuffled; the key outside the repository, never overwritten."""
    sys.path[:0] = [str(STAGE0), str(STAGE0 / 'census')]
    import build_cards
    import mark_cards
    if FULL_KEY.exists():
        raise SystemExit(f'refused: {FULL_KEY} exists')
    folder = OUT / 'deck-full'
    folder.mkdir(parents=True, exist_ok=False)
    rows = [c for c in json.loads((OUT / 'fullcases.json').read_text()) if c['hidden'] >= 1]
    for arm in arms:
        expected_files(OUT / 'probe' / arm, [c['case'] for c in rows])
    frozen = FROZEN_SYSTEM.read_text(encoding='utf-8')
    items = ROOT / 'poc/data/comparison-2026-11-17/items-comparison.sqlite'
    libraries = {}
    cards, rng = [], random.Random(SEED)

    def card(case, arm, answer):
        views, archive = store_paths(case['draw'])
        if case['draw'] not in libraries:
            libraries[case['draw']] = build_cards.library(views, archive, items)
        lib = libraries[case['draw']]
        entry = dict(next(e for e in lib if e['question_id'] == case['view_id']))
        _, request, _, _ = stored(case)
        request = dict(request, messages=[request['messages'][0], dict(request['messages'][1], content=case['user_full'])])
        sent = rebuild(request, frozen, None, strip_previous=arm.endswith('-fullnoprev'))
        request_json = json.dumps(sent)
        conn = build_cards.ro(views)
        rungs = build_cards.conditions(case['view_id'], conn)
        item_db = build_cards.ro(items)
        publisher_of = lambda input_id: (item_db.execute('select publisher from items where input_id=?', (input_id,)).fetchone() or [None])[0]
        entry['answer'] = rungs.get(answer['rung'])
        entry['reasons'] = f"Reference: {answer['reference']} Implied outcome: {answer['implied_outcome']} Reasons: {answer['reasons']}"
        entry['material'] = [dict(item, publisher=publisher_of(item['input_id'])) for item in build_cards.material(request_json)]
        entry['context'] = build_cards.context(request_json, conn)
        if entry['context']['previous']:
            entry['context']['previous']['answer'] = rungs.get(entry['context']['previous']['rung'])
        return build_cards.card_text(entry, lib), rungs

    for arm in arms:
        for case in rows:
            for k in (1, 2, 3):
                record = json.loads((OUT / 'probe' / arm / f"{case['case']}-{k}.json").read_text())
                text, rungs = card(case, arm, record['answer'])
                cards.append({'arm': arm, 'case': case['case'], 'role': case['role'], 'repeat': k, 'rung': record['answer']['rung'],
                              'stored_rung': stored(case)[0]['rung'], 'kind': 'probe', 'text': text,
                              'refusals': refusals(case, record['answer'])})
    confirmations = []
    controls = [c for c in rows if c['role'] == 'control']
    for case in rng.sample(controls, len(controls)):
        if sum(c['kind'] == 'plant' for c in cards) >= PLANTS:
            break
        record = json.loads((OUT / 'probe' / arms[0] / f"{case['case']}-1.json").read_text())
        text, rungs = card(case, arms[0], record['answer'])
        rung = record['answer']['rung']
        moved = rung + 1 if rung + 1 in rungs else rung - 1
        if moved not in rungs:
            continue
        planted = text.replace(f'Latest answer at the cutoff: {rungs[rung]}', f'Latest answer at the cutoff: {rungs[moved]}', 1)
        if planted == text:
            continue
        ok, mark = mark_cards.confirmed_by_reader(planted, False)
        confirmations.append({'case': case['case'], 'moved_to': moved, 'confirmed': ok, 'mark': mark})
        if ok:
            cards.append({'arm': 'plant', 'case': case['case'], 'role': 'plant', 'repeat': 1, 'rung': moved, 'stored_rung': rung,
                          'kind': 'plant', 'text': planted})
    rng.shuffle(cards)
    key = {}
    for n, c in enumerate(cards, 1):
        cid = f'C{n:03d}'
        key[cid] = {k: v for k, v in c.items() if k != 'text'}
        (folder / f'{cid}.txt').write_text(c['text'])
    FULL_KEY.parent.mkdir(parents=True, exist_ok=True)
    FULL_KEY.write_text(json.dumps({'cards': key, 'invalid': [], 'plant_confirmations': confirmations}, indent=1) + '\n')
    from collections import Counter
    print(len(cards), 'cards;', dict(Counter((c['arm'], c['kind']) for c in cards)))


def patch_judging(arm):
    """Put an arm into the judge's own code path for this process: the schema's field order and, when it differs from v7, the system
    text. Nothing in the package is edited."""
    from hivemind.views import judging
    system, order = arm_spec(arm)
    original_schema, original_prompt = judging.schema_for, judging.build_prompt
    frozen = FROZEN_SYSTEM.read_text(encoding='utf-8')
    if order is not None:
        def schema_for(version):
            schema = original_schema(version)
            schema['properties'] = {field: schema['properties'][field] for field in order}
            return schema
        judging.schema_for = schema_for
    if system != frozen:
        judging.build_prompt = lambda conn, view_id, version: (system, original_prompt(conn, view_id, version)[1])


def prodpath(arm, ledger_path=None):
    """The production-path check (council A): a copy of old-2 cut at the end of PRODPATH_BOUNDARY. On each of PRODPATH_DAYS every link the
    old system wrote that day is fed (every question, with the evidence, its sources and its repeat and revision relations), and the
    judge's own round judges the questions the old system judged at that day's close, unpatched otherwise: a changed theme queues its
    assets as in production. 'replay' answers with the old archived answers at $0 and checks each request's bytes against the archived
    one; any other arm sends, with an empty archive of its own (council B: J2a and v7 share an archive key)."""
    mt = load('merge_test', MERGE_TEST)
    mt.BOUNDARY_DAY = PRODPATH_BOUNDARY
    from hivemind import config, model
    from hivemind.views import judging, store
    cfg = config.load(CONFIG)
    folder = OUT / 'prodpath' / arm
    folder.mkdir(parents=True, exist_ok=False)
    boundary = mt.judging_copy(PRODPATH_DRAW, folder / 'views.sqlite')
    conn = store.open_db(str(folder / 'views.sqlite'))
    archive = model.Archive(str(folder / 'archive.sqlite'))
    old = mt.old_store(PRODPATH_DRAW)
    all_views = [r[0] for r in old.execute('select view_id from views')]
    day_seq = dict(old.execute('select day, seq from days_completed').fetchall())
    created = {v: old.execute('select created_seq from views where view_id=?', (v,)).fetchone()[0] for v in all_views}
    pending = {v for v, c in created.items() if c > boundary}
    log = []
    feed = mt.control_feed(PRODPATH_DRAW, all_views, conn, log)
    if arm == 'replay':
        import threading
        replay, lock = mt.ReplayOld(PRODPATH_DRAW), threading.Lock()

        def transport(provider, request):          # one sqlite connection answers the round's concurrent calls one at a time
            with lock:
                return replay(provider, request)
        transport.checks, transport.replay = replay.checks, replay
    else:
        patch_judging(arm)
        transport, ledger = transport_for(ledger_path)
    previous = boundary
    results = []
    for day in PRODPATH_DAYS:
        seq = day_seq[day]
        for view_id in sorted(v for v in pending if created[v] <= seq):
            mt.restore_view(conn, PRODPATH_DRAW, view_id)
            pending.discard(view_id)
        feed(day, previous, seq, pending)
        previous = seq
        conn.commit()
        from hivemind.views import round as round_module
        scheduled = sorted(round_module.changed_views_of_day(conn, day))     # production's own starting queue (council D)
        old_judged = {r[0] for r in old.execute('select view_id from judgements where seq=?', (seq,))}
        if arm == 'replay':
            transport.replay.seq = seq
        judged = judging.round_of_judgements(archive, cfg, conn, scheduled, seq, {'input_id': f'day:{day}', 'publication_day': day},
                                             transport=transport)
        conn.commit()
        mt.restore_closures(conn, PRODPATH_DRAW, all_views, seq)
        conn.commit()
        for j in judged:
            results.append({'day': day, 'view': j['view_id'], 'rung': j['rung'], 'changed': j['changed'], 'queued_by_round': j['view_id'] not in scheduled})
        judged_set = {j['view_id'] for j in judged}
        print(json.dumps({'arm': arm, 'day': day, 'starting queue': len(scheduled), 'judged': len(judged),
                          'added by the round': len(judged_set - set(scheduled)), 'same set as old': judged_set == old_judged,
                          'old only': sorted(old_judged - judged_set), 'arm only': sorted(judged_set - old_judged)}), flush=True)
    (folder / 'results.json').write_text(json.dumps(results, indent=1))
    (folder / 'feed-log.json').write_text(json.dumps(log, indent=1))
    if arm == 'replay':
        checks = transport.checks
        (folder / 'checks.json').write_text(json.dumps(checks, indent=1))
        print('replay:', sum(c['same text'] for c in checks), 'of', len(checks), 'requests byte-identical to the archived ones;',
              sum(c['same evidence shown'] for c in checks), 'show the same evidence')
    else:
        print('ledger', json.dumps(ledger.read()))


def probescore(arms=('v7', 'J2a', 'J2b')):
    """$0, after `read`: the locked decision rule (DESIGN-J2.md (a), (b), (d)) per arm against v7's re-send. Every arm x case x repeat
    must be accounted for; an invalid-rung answer counts as refused and not supported. Jointly supported = both readers' final answer
    mark is `supported` (a split is not)."""
    key = json.loads(PROBE_KEY.read_text())
    marks = json.loads((OUT / 'marks-probe.json').read_text())
    rows = json.loads((OUT / 'cases.json').read_text())
    supported, refused = {}, {}
    for cid, m in marks.items():
        if m['kind'] == 'plant':
            continue
        k = (m['arm'], m['case'], m['repeat'])
        supported[k] = (m['marks'] or {}).get('answer') == 'supported'
        refused[k] = bool(m.get('refusals'))
    for m in key['invalid']:
        k = (m['arm'], m['case'], m['repeat'])
        supported[k], refused[k] = False, True
    missing = [(a, c['case'], r) for a in arms for c in rows for r in (1, 2, 3) if (a, c['case'], r) not in supported]
    if missing:
        raise SystemExit(f'{len(missing)} answers not accounted for, e.g. {missing[:4]}: refused')
    holds = {a: {c['case']: sum(supported[(a, c['case'], r)] for r in (1, 2, 3)) >= 2 for c in rows} for a in arms}
    targets = [c['case'] for c in rows if c['role'] == 'target']
    controls = [c['case'] for c in rows if c['role'] == 'control']
    report = {}
    for a in arms:
        improved = [t for t in targets if holds[a][t] and not holds['v7'][t]]
        worsened = [t for t in targets if holds['v7'][t] and not holds[a][t]]
        lost = [c for c in controls if not holds[a][c]]
        report[a] = {'targets held (>=2 of 3)': sum(holds[a][t] for t in targets), 'paired improved': improved, 'paired worsened': worsened,
                     'net': len(improved) - len(worsened), 'controls lost': lost,
                     'refused answers': sum(refused[(a, c['case'], r)] for c in rows for r in (1, 2, 3))}
    for a in arms:
        r = report[a]
        verdict = '' if a == 'v7' else ('PASSES (a)(b)(d)' if r['targets held (>=2 of 3)'] >= 12 and r['net'] >= 8
                                         and len(r['controls lost']) <= len(report['v7']['controls lost'])
                                         and r['refused answers'] <= report['v7']['refused answers'] else 'does not pass (a)(b)(d)')
        print(a, json.dumps(r), verdict)
    plants = {cid: m['marks'] for cid, m in marks.items() if m['kind'] == 'plant'}
    print('plants (expected not supported):', json.dumps(plants))
    (OUT / 'probescore.json').write_text(json.dumps({'report': report, 'plants': plants}, indent=1))


def forkcases():
    """$0: per target, the judgement at which the final (both readers rejected) rung was first chosen and then held to the end: the
    request there shows the conclusion before the error (or none, at a question's first judgement), not the error carried forward.
    Its stored request is rebuilt byte for byte under the frozen judge."""
    from hivemind import model
    frozen = FROZEN_SYSTEM.read_text(encoding='utf-8')
    out, bad = [], []
    for case in json.loads((OUT / 'cases.json').read_text()):
        if case['role'] != 'target':
            continue
        views, archive = store_paths(case['draw'])
        v, a = readonly(views), readonly(archive)
        history = [dict(r) for r in v.execute('select judgement_id, rung, request_sha256, publication_day from judgements where view_id=? order by judgement_id', (case['view_id'],))]
        final = history[-1]['rung']
        k = len(history) - 1
        while k > 0 and history[k - 1]['rung'] == final:
            k -= 1
        fork = history[k]
        request = json.loads(a.execute('select request_json from model_calls where request_sha256=? limit 1', (fork['request_sha256'],)).fetchone()[0])
        if model.request_identity(rebuild(request, frozen))[1] != fork['request_sha256']:
            bad.append(case['case'])
        out.append(dict(case, fork_judgement_id=fork['judgement_id'], fork_day=fork['publication_day'], fork_request_sha256=fork['request_sha256'],
                        rejected_rung=final, previous_rung=history[k - 1]['rung'] if k > 0 else None, judgements_after=len(history) - k))
    (OUT / 'forkcases.json').write_text(json.dumps(out, indent=1))
    print(f'{len(out) - len(bad)} of {len(out)} fork requests rebuilt byte for byte', 'mismatch: ' + ', '.join(bad) if bad else '')
    print(sum(c['previous_rung'] is None for c in out), 'forks are first judgements;', sum(c['previous_rung'] is not None for c in out), 'are moves from another rung')
    if bad:
        raise SystemExit(1)


def forkprobe(ledger_path, arm, repeats):
    transport, ledger = transport_for(ledger_path)
    system, order = arm_spec(arm)
    rows = json.loads((OUT / 'forkcases.json').read_text())
    folder = OUT / 'forkprobe' / arm
    folder.mkdir(parents=True, exist_ok=False)
    jobs = [(case, k) for case in rows for k in range(1, repeats + 1)]

    def one(job):
        case, k = job
        _, archive = store_paths(case['draw'])
        request = json.loads(readonly(archive).execute('select request_json from model_calls where request_sha256=? limit 1', (case['fork_request_sha256'],)).fetchone()[0])
        response = transport('openai', rebuild(request, system, order))
        answer = json.loads(response['choices'][0]['message']['content'])
        views, _ = store_paths(case['draw'])
        refused = refusals_before(views, case['view_id'], case['fork_judgement_id'], answer, request['messages'][1]['content'])
        (folder / f"{case['case']}-{k}.json").write_text(json.dumps({'case': case['case'], 'repeat': k, 'arm': arm, 'answer': answer,
                                                                    'refusals': refused, 'usage': response.get('usage')}, indent=1, ensure_ascii=False))
        return case['case']

    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        for name in pool.map(one, jobs):
            print('fork', name, flush=True)
    print('ledger', json.dumps(ledger.read()))


def forkscore(arms=('v7', 'J2a', 'J2b')):
    """$0, complete coverage required: per arm, the targets whose fork answer repeats the rejected rung in at least 2 of 3 repeats,
    and the refusals."""
    rows = json.loads((OUT / 'forkcases.json').read_text())
    report = {}
    for arm in arms:
        folder = OUT / 'forkprobe' / arm
        expected_files(folder, [c['case'] for c in rows])
        repeats, refused, moved = [], 0, {}
        for c in rows:
            answers = [json.loads((folder / f"{c['case']}-{k}.json").read_text()) for k in (1, 2, 3)]
            refused += sum(bool(a['refusals']) for a in answers)
            rungs = [a['answer']['rung'] for a in answers]
            if sum(r == c['rejected_rung'] for r in rungs) >= 2:
                repeats.append(c['case'])
            moved[c['case']] = rungs
        report[arm] = {'repeat the rejected rung': len(repeats), 'cases': repeats, 'refused': refused, 'rungs': moved}
        print(arm, 'repeat the rejected rung on', len(repeats), 'of', len(rows), 'targets; refused answers', refused)
    (OUT / 'forkscore.json').write_text(json.dumps(report, indent=1))


def cut_copy(mt, draw, path, boundary_seq):
    """merge_test.judging_copy with a sequence-number boundary: a copy of the old store holding only rows written at or before
    `boundary_seq` (0: nothing but the schema and the processing record), the append-only triggers lifted for the cut and put back."""
    source = sqlite3.connect(f'file:{mt.RUN / draw / "prod/views.sqlite"}?mode=ro', uri=True)
    target = sqlite3.connect(path)
    source.backup(target)
    source.close()
    triggers = target.execute("select name, sql from sqlite_master where type='trigger'").fetchall()
    for name, _ in triggers:
        target.execute(f'drop trigger {name}')
    later_views = [r[0] for r in target.execute('select view_id from views where created_seq>?', (boundary_seq,))]
    for table, column in (('judgements', 'seq'), ('evidence_links', 'seq'), ('evidence_sources', 'seq'), ('same_claims', 'seq'),
                          ('revisions', 'seq'), ('replacements', 'seq'), ('view_switches', 'after_seq'), ('successions', 'seq'),
                          ('days_completed', 'seq'), ('evidence', 'created_seq')):
        target.execute(f'delete from {table} where {column}>?', (boundary_seq,))
    marks = ','.join('?' * len(later_views))
    for table in ('views', 'rungs', 'view_keys'):
        target.execute(f"delete from {table} where view_id in ({marks})", later_views)
    for _, sql in triggers:
        target.execute(sql)
    target.commit()
    target.close()


def window(draw, arm, ledger_path=None, first_day='2026-07-01', last_day='2026-09-20'):
    """The judge-only replay of a whole window (council F): a copy of an old draw holding nothing before `first_day`; each day the old
    system's links, evidence, sources and repeat/revision relations are fed, questions are put back on the day the old system opened
    them (with their choices), its closures and successions are restored, and the judge's own round runs from production's own queue
    (`round.changed_views_of_day`), so each arm builds its own conclusions, citations, theme effects and queue. 'replay' answers with
    the old archived answers at $0 and checks every request's bytes; any other arm sends, with an empty archive of its own."""
    mt = load('merge_test', MERGE_TEST)
    from hivemind import config, model
    from hivemind.views import judging, store
    from hivemind.views import round as round_module
    cfg = config.load(CONFIG)
    folder = OUT / 'window' / draw / arm
    folder.mkdir(parents=True, exist_ok=False)
    old = mt.old_store(draw)
    day_seq = dict(old.execute('select day, seq from days_completed').fetchall())
    days = sorted(d for d in day_seq if first_day <= d <= last_day)
    earlier = [s for d, s in day_seq.items() if d < first_day]
    boundary = max(earlier) if earlier else 0
    cut_copy(mt, draw, folder / 'views.sqlite', boundary)
    conn = store.open_db(str(folder / 'views.sqlite'))
    archive = model.Archive(str(folder / 'archive.sqlite'))
    all_views = [r[0] for r in old.execute('select view_id from views')]
    created = {v: old.execute('select created_seq from views where view_id=?', (v,)).fetchone()[0] for v in all_views}
    pending = {v for v, c in created.items() if c > boundary}
    log = []
    feed = mt.control_feed(draw, all_views, conn, log)
    if arm == 'replay':
        import threading
        replay, lock = mt.ReplayOld(draw), threading.Lock()

        def transport(provider, request):
            with lock:
                return replay(provider, request)
        transport.checks, transport.replay = replay.checks, replay
    else:
        patch_judging(arm)
        transport, ledger = transport_for(ledger_path)
    previous, results, days_log = boundary, [], []
    for day in days:
        seq = day_seq[day]
        for view_id in sorted(v for v in pending if created[v] <= seq):
            mt.restore_view(conn, draw, view_id)
            pending.discard(view_id)
        feed(day, previous, seq, pending)
        mt.copy_rows(conn, old, 'successions', 'seq>? and seq<=?', (previous, seq))
        previous = seq
        conn.commit()
        scheduled = sorted(round_module.changed_views_of_day(conn, day))
        old_judged = {r[0] for r in old.execute('select view_id from judgements where seq=?', (seq,))}
        if arm == 'replay':
            transport.replay.seq = seq
        judged = judging.round_of_judgements(archive, cfg, conn, scheduled, seq, {'input_id': f'day:{day}', 'publication_day': day},
                                             transport=transport) if scheduled else []
        conn.commit()
        mt.restore_closures(conn, draw, all_views, seq)
        conn.commit()
        judged_set = {j['view_id'] for j in judged}
        for j in judged:
            results.append({'day': day, 'view': j['view_id'], 'rung': j['rung'], 'changed': j['changed']})
        days_log.append({'day': day, 'starting queue': len(scheduled), 'judged': len(judged), 'same set as old': judged_set == old_judged,
                         'old only': sorted(old_judged - judged_set), 'arm only': sorted(judged_set - old_judged)})
        print(json.dumps(dict(days_log[-1], arm=arm, draw=draw)), flush=True)
    (folder / 'results.json').write_text(json.dumps(results, indent=1))
    (folder / 'days.json').write_text(json.dumps(days_log, indent=1))
    if arm == 'replay':
        checks = transport.checks
        (folder / 'checks.json').write_text(json.dumps(checks, indent=1))
        print('replay:', sum(c['same text'] for c in checks), 'of', len(checks), 'requests byte-identical to the archived ones;',
              sum(c['same evidence shown'] for c in checks), 'show the same evidence;', sum(d['same set as old'] for d in days_log), 'of', len(days_log), 'days judge the same set')
    else:
        print('ledger', json.dumps(ledger.read()))


def store_as_of(views_path, judgement_id, seq):
    """A read-only connection showing the store as it stood when a stored judgement's request was built: later judgements, and links,
    sources, relations and switches written after its sequence number, are shadowed by temporary tables (unqualified reads see them)."""
    conn = readonly(views_path)
    conn.execute('create temp table judgements as select * from main.judgements where judgement_id < ?', (judgement_id,))
    for table, column in (('evidence_links', 'seq'), ('evidence_sources', 'seq'), ('same_claims', 'seq'), ('revisions', 'seq'),
                          ('replacements', 'seq'), ('view_switches', 'after_seq'), ('successions', 'seq')):
        conn.execute(f'create temp table {table} as select * from main.{table} where {column} <= ?', (seq,))
    return conn


def full_requests():
    """$0, council G: for each case, the stored final request rebuilt by the judge's own `build_prompt` on the store as it stood
    (must equal the stored user text byte for byte), then the same request with every piece in force shown (no hidden line).
    Writes fullcases.json with both user texts and the hidden count; only cases with at most 100 hidden pieces are kept."""
    from hivemind.views import judging, store
    rows = json.loads((OUT / 'cases.json').read_text())
    out, mismatched = [], []
    original_view = judging.evidence_in_view
    for case in rows:
        judgement, request, _, _ = stored(case)
        views, _ = store_paths(case['draw'])
        conn = store_as_of(views, judgement['judgement_id'], judgement['seq'])
        judging.evidence_in_view = original_view
        _, user = judging.build_prompt(conn, case['view_id'], 'judging-v7')
        stored_user = request['messages'][1]['content']
        if user != stored_user:
            mismatched.append(case['case'])
            continue
        shown, hidden = original_view(conn, case['view_id'])
        if hidden > 100:
            continue
        judging.evidence_in_view = lambda c, v: (store.evidence_in_force(c, v), 0)
        _, full_user = judging.build_prompt(conn, case['view_id'], 'judging-v7')
        judging.evidence_in_view = original_view
        out.append(dict(case, hidden=hidden, shown=len(shown), user_clipped=stored_user, user_full=full_user))
    (OUT / 'fullcases.json').write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f'{len(rows) - len(mismatched)} of {len(rows)} stored requests rebuilt byte for byte by build_prompt on the as-of store;',
          'mismatch: ' + ', '.join(mismatched) if mismatched else '')
    print(len(out), 'cases with at most 100 hidden pieces:', sum(c['role'] == 'target' for c in out), 'targets,',
          sum(c['role'] == 'control' for c in out), 'controls; hidden pieces restored:', sum(c['hidden'] for c in out))


def fullscore(arms=('v7-fullprev', 'v7-fullnoprev')):
    """$0, after `readfull`: council G's screen. Every arm x case x repeat must be marked. Jointly supported = both readers' final
    answer mark `supported` (a split is not). Refusals are recomputed against the request each answer actually received (full evidence,
    with or without the previous conclusion), on the store as of the stored judgement. Screen: net target repairs (no-prev holds 2 of 3,
    with-prev does not, minus the reverse) at least 5; no control lost (held with the previous conclusion, not without); no added
    refusals."""
    from hivemind.views import judging
    key = json.loads(FULL_KEY.read_text())
    marks = json.loads((OUT / 'marks-full.json').read_text())
    rows = {c['case']: c for c in json.loads((OUT / 'fullcases.json').read_text()) if c['hidden'] >= 1}
    supported = {}
    for cid, m in marks.items():
        if m['kind'] != 'plant':
            supported[(m['arm'], m['case'], m['repeat'])] = (m['marks'] or {}).get('answer') == 'supported'
    missing = [(a, c, r) for a in arms for c in rows for r in (1, 2, 3) if (a, c, r) not in supported]
    if missing:
        raise SystemExit(f'{len(missing)} answers not marked, e.g. {missing[:4]}: refused')
    refused = {a: 0 for a in arms}
    for a in arms:
        for name, case in rows.items():
            judgement, _, _, _ = stored(case)
            views, _ = store_paths(case['draw'])
            text = without_previous(case['user_full']) if a.endswith('-fullnoprev') else case['user_full']
            for r in (1, 2, 3):
                answer = json.loads((OUT / 'probe' / a / f'{name}-{r}.json').read_text())['answer']
                refused[a] += bool(refusals_before(views, case['view_id'], judgement['judgement_id'], answer, text))
    holds = {a: {c: sum(supported[(a, c, r)] for r in (1, 2, 3)) >= 2 for c in rows} for a in arms}
    prev, noprev = arms
    targets = [c for c in rows if rows[c]['role'] == 'target']
    controls = [c for c in rows if rows[c]['role'] == 'control']
    repaired = [t for t in targets if holds[noprev][t] and not holds[prev][t]]
    broken = [t for t in targets if holds[prev][t] and not holds[noprev][t]]
    lost = [c for c in controls if holds[prev][c] and not holds[noprev][c]]
    passes = len(repaired) - len(broken) >= 5 and not lost and refused[noprev] <= refused[prev]
    report = {'targets held': {a: sum(holds[a][t] for t in targets) for a in arms}, 'controls held': {a: sum(holds[a][c] for c in controls) for a in arms},
              'repaired': repaired, 'broken': broken, 'net': len(repaired) - len(broken), 'controls lost': lost, 'refused': refused,
              'plants': {cid: m['marks'] for cid, m in marks.items() if m['kind'] == 'plant'}, 'screen passes': passes}
    print(json.dumps(report, indent=1))
    (OUT / 'fullscore.json').write_text(json.dumps(report, indent=1))


if __name__ == '__main__':
    command = sys.argv[1]
    if command == 'cases':
        cases()
    elif command == 'check':
        check()
    elif command == 'account':
        account(sys.argv[2])
    elif command == 'probe':
        probe(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif command == 'goldcases':
        goldcases()
    elif command == 'goldprobe':
        goldprobe(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif command == 'goldscore':
        goldscore(sys.argv[2])
    elif command == 'probescore':
        probescore()
    elif command == 'forkcases':
        forkcases()
    elif command == 'forkprobe':
        forkprobe(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif command == 'forkscore':
        forkscore()
    elif command == 'fullrequests':
        full_requests()
    elif command == 'deck':
        deck(sys.argv[2:])
    elif command == 'read':
        read()
    elif command == 'deckfull':
        deck_full()
    elif command == 'fullscore':
        fullscore()
    elif command == 'readfull':
        read('deck-full', FULL_KEY, 'marks-full.json')
    elif command == 'window':
        window(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
    elif command == 'prodpath':
        prodpath(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        raise SystemExit(__doc__)
