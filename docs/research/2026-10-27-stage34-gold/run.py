"""Steps 3 and 4 on the 24 gold cases (D201): build every request from stored data ($0), send once per case under a cap, score
against gold.json. The step 2 reader (ported, `hivemind.research_context`) supplies the catalog and the complete evidence of the
linked questions at the case's historical sequence number; Jev gives relation opinions (step 3); one gpt-6-luna call places and
merges (step 4). Nothing is written to any ledger.

  python3 run.py build <arm>            # requests, sizes and offline checks, no call
  python3 run.py send <arm> [cap_usd]   # sends what build prepared; stops at the cap or on a transport error; no retry, no vote
  python3 run.py score <arm>            # the arm's answers against gold.json, exact fields only
Arm folders: poc/reports/2026-10-27-stage34-gold/<arm>/ (requests, answers, measurement, scores)."""
import concurrent.futures
import dataclasses
import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, jev, model, research_context, universe as universe_module  # noqa: E402
from hivemind.views import jev_matching  # noqa: E402

DATA = '/Users/lchingen/hivemind/poc/data'
LEDGER = f'{DATA}/english-v29-nvda-3m-2026-10-27/views.sqlite'
ITEMS = f'{DATA}/items-nvda-2026-07-01-10-27.sqlite'
REPORTS = '/Users/lchingen/hivemind/poc/reports/2026-10-27-stage34-gold'
CASES = f'{REPORTS}/cases.json'
GOLD = os.path.join(HERE, 'gold.json')
JEV_BATCH = 40

QUESTION_RELATIONS = {
    'direct': 'the record states a reported, guided or estimated value of the quantity this question measures, for its period or a part of it, or reports the event the question asks about',
    'lead': 'the record is a driver, a customer or partner action, a product or supply fact, a denial or a confirmation that bears on the answer without stating it',
    'background': 'context, an argument without a figure, or a figure for a later or earlier period than the question\'s',
    'unrelated': 'no substantive relation; a shared company or industry word is not enough',
    'uncertain': 'the supplied text does not establish which of the above holds'}

SYSTEM = '''You are a hedge-fund analyst keeping one research record per question on a name you cover. One source record arrives. Read it beside every stored piece of the questions it may bear on, then write the update. Sources are never edited or deleted: you say what the record adds to each question's argument, and what it is the same as, revises or opposes.

Procedure. Read the record: who first said it (original source), when, with what period and definition. Then walk every stored piece of each linked question, first to last, and classify each one against the record:
- same_claim_as: the same claim, in any wording, by any outlet, on any day, whoever reports it. A second newspaper relaying NVIDIA's own benchmark; an author repeating his own figure five days later; a bank's note repeating the customer's remark; two newspapers reporting the same talks from their own sources. The argument counts one claim however many records carry it.
- revises: the same claim's later value or status from the party that owns it. A rumoured guarantee becomes an announced amount; management raises guidance it gave before. Both pieces stay; the argument cites the later one and keeps the path.
- opposes: a claim that contradicts the piece. A company's denial against an analyst's delay report; an independent test against a vendor's benchmark. Both stay side by side; the argument says contested and names what resolves it.
- otherwise the piece is different: leave it alone.
Period and definition: a record bears on a question only if its period and definition match or the mapping is stated. A Q1 print is not a full year; FY2028 growth is not FY2027 growth; five companies' total AI outlays are not four hyperscalers' data-center capex. On a mismatch the record is background and new_information names the mismatch.
Action: update_existing when the record moves a number, a probability, a risk or a condition of an existing question's argument (would it appear in this week's note?); background_only when it is a pickup or context that moves nothing (a sizeless first delivery, a vendor efficiency claim, a consumer-GPU price note); propose_new only when the record carries an investment judgement no catalog question carries, a decision that could change the position, and independent_judgement says what that view is (a narrower scope, a new figure, or a second legal form of one deal is not one: a $6bn license inside an equity deal already tracked updates that question; twenty yes/no questions on individual stakes are one judgement about investment exposure and circularity, and a candidate phrased as "did NVIDIA sign this round" does not carry it); unresolved when the texts do not let you decide.
Independence is a separate question from claim identity: independent_sources is true when the record's original source has its own access to the fact and is not the same source as the pieces in same_claim_as (a customer's own disclosure, a filing, a third-party test, a second newspaper's own reporting of the same talks). A vendor claim relayed by ten outlets is one source; two papers each citing their own people familiar with the talks are two sources of one claim. A record with no same_claim_as pieces leaves independent_sources true unless it merely relays one of them.
The argument is the deliverable. For each question you update, rewrite it in full as the statement you would defend now: the current lean, the piece ids it rests on with their source quality, the ids that oppose it, the limitations the texts impose (vendor benchmark, unverified leak, period unstated, guidance not result), and what would change it (the next print, a shipment confirmation, a filing). Keep conditions and periods exactly as the texts state them. Comparison opinions are hints with scores; the texts decide. Answer in the JSON schema only.'''

ARGUMENT = {'type': 'object', 'additionalProperties': False,
            'required': ['question_id', 'statement', 'support_ids', 'opposing_ids', 'limitations', 'what_would_change_it'],
            'properties': {'question_id': {'type': 'string'}, 'statement': {'type': 'string'},
                           'support_ids': {'type': 'array', 'items': {'type': 'string'}},
                           'opposing_ids': {'type': 'array', 'items': {'type': 'string'}},
                           'limitations': {'type': 'array', 'items': {'type': 'string'}},
                           'what_would_change_it': {'type': 'array', 'items': {'type': 'string'}}}}
PROPS = {
    'action': {'type': 'string', 'enum': ['update_existing', 'propose_new', 'background_only', 'unresolved']},
    'question_ids': {'type': 'array', 'items': {'type': 'string'}},
    'same_claim_as': {'type': 'array', 'items': {'type': 'string'}},
    'revises': {'type': 'array', 'items': {'type': 'string'}},
    'opposes': {'type': 'array', 'items': {'type': 'string'}},
    'independent_sources': {'type': 'boolean'},
    'original_source': {'type': 'string'},
    'new_information': {'type': 'string'},
    'arguments': {'type': 'array', 'items': ARGUMENT},
    'new_question': {'type': 'string'},
    'independent_judgement': {'type': 'string'},
    'reason': {'type': 'string'}}
SCHEMA = {'type': 'object', 'additionalProperties': False, 'properties': PROPS, 'required': list(PROPS)}
SETTING = config.Setting('stage34', 'gpt-6-luna', 'stage34-v2', 0.2, 'low', 6000)


def arm_dir(arm):
    path = os.path.join(REPORTS, arm)
    os.makedirs(path, exist_ok=True)
    return path


def save(arm, name, value):
    with open(os.path.join(arm_dir(arm), name), 'w', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=1)


def load(arm, name):
    with open(os.path.join(arm_dir(arm), name), encoding='utf-8') as f:
        return json.load(f)


def linked_ids(case, catalog_ids):
    piece = case['piece'] or {}
    if 'one_line' in piece:
        return [v for v in piece.get('links', []) if v in catalog_ids]
    for key in ('folds_into', 'target'):
        if piece.get(key) in catalog_ids:
            return [piece[key]]
    if case.get('target') in catalog_ids:
        return [case['target']]
    return []


def question_text(q, pieces):
    rungs = ' / '.join(f'{r.get("label")}: {r.get("condition", "")}' for r in q.get('rungs', []))
    quotes = ''.join(f'\n    Evidence: [{p["speaker"]} {p["original_day"]}] {p["quote"][:400]}' for p in pieces[:2])
    return f'{q["view_id"]} ({q["kind"]}, object {q["object_id"]}, focus "{q["looks_at"]}", due {q["due_day"]}): {q["question"]}\nLadder: {rungs}{quotes}'


def piece_text(p):
    return f'{p["evidence_id"]} [{p["tier"]}; {p["speaker"]}; original source {p["original_who"]} {p["original_day"]}] {p["one_line"]} | quote: {p["quote"][:300]}'


def chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def build(arm, cases_path=CASES):
    cases = json.load(open(cases_path, encoding='utf-8'))
    uni = universe_module.load(os.path.join(ROOT, 'poc', 'universe.json'))
    items = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True); items.row_factory = sqlite3.Row
    prepared, report = {}, []
    for case in cases:
        name, seq = case['case'], case['seq']
        item = dict(items.execute('select * from items where input_id=?', (case['input_id'],)).fetchone())
        objects = [o['value'] for o in json.loads(item['object_identifiers']) if uni.has(o['value'])]
        with research_context.Reader(LEDGER, seq, objects, uni) as reader:
            catalog = reader.catalog()
            catalog_ids = [q['view_id'] for q in catalog['questions']]
            linked = linked_ids(case, catalog_ids)
            expansion = reader.expand(linked)
        piece = case['piece'] or {}
        is_piece = 'one_line' in piece
        said_day = piece.get('original_day') or item['publication_day']
        state = jev_matching.piece_state(piece, said_day) if is_piece else jev_matching.candidate_state(piece, [])
        by_question = {q['view_id']: q for q in expansion['questions']}
        pieces = {p['evidence_id']: p for p in expansion['evidence']}
        questions = {}
        if is_piece:
            for q in expansion['questions']:
                first = [pieces[e] for e in q['evidence_ids'][:2] if e in pieces]
                questions[f'rel__{q["view_id"]}'] = {'type': 'choice', 'criteria': QUESTION_RELATIONS,
                    'instructions': 'How does the INCOMING PIECE bear on the QUESTION below? Use only the supplied text. QUESTION:\n' + question_text(q, first)}
            for q in expansion['questions']:
                for eid in q['evidence_ids']:
                    questions[f'piece__{q["view_id"]}__{eid}'] = jev_matching.piece_question(piece_text(pieces[eid]))
        else:
            for q in catalog['questions']:
                questions[f'rel__{q["view_id"]}'] = jev_matching.relation_question(question_text(q, []))
        jev_requests = [{'state': state, 'questions': dict(batch)} for batch in chunks(list(questions.items()), JEV_BATCH)]
        source = ({k: piece.get(k) for k in ('id', 'one_line', 'quote', 'speaker', 'original_who', 'original_day', 'tier', 'event_time')} if is_piece
                  else {'candidate': {k: v for k, v in piece.items() if k not in ('evidence_ids',)}})
        source.update({'publisher': item['publisher'], 'publisher_type': item['publisher_type'], 'publication_day': item['publication_day'],
                       'category': item['category'], 'title': item['title']})
        payload = {'source_record': source,
                   'linked_questions': [{'view_id': q['view_id'], 'looks_at': q['looks_at'], 'question': q['question'], 'due_day': q['due_day'],
                                         'rungs': [{'label': r.get('label'), 'condition': r.get('condition')} for r in q.get('rungs', [])],
                                         'latest_judgement': ({'rung': q['latest_judgement']['rung'], 'reasons': q['latest_judgement']['reasons'],
                                                               'day': q['latest_judgement']['publication_day']} if q.get('latest_judgement') else None),
                                         'argument': None, 'piece_ids': q['evidence_ids']} for q in expansion['questions']],
                   'stored_pieces': [{'id': p['evidence_id'], 'tier': p['tier'], 'speaker': p['speaker'], 'original_who': p['original_who'],
                                      'original_day': p['original_day'], 'event_time': p['event_time'], 'one_line': p['one_line'], 'quote': p['quote'][:300],
                                      'sources': [[s['input_id'], s['publication_day']] for s in p['sources']],
                                      'replaced': [r['old_evidence_id'] for r in p.get('replaced', [])]} for p in expansion['evidence']],
                   'catalog': [{'view_id': q['view_id'], 'looks_at': q['looks_at']} for q in catalog['questions']],
                   'comparison_opinion': None}
        prepared[name] = {'seq': seq, 'input_id': case['input_id'], 'linked': linked, 'catalog_ids': catalog_ids, 'piece_ids': list(pieces),
                          'jev_requests': jev_requests, 'payload': payload}
        user_chars = len(json.dumps(payload, ensure_ascii=False))
        report.append({'case': name, 'linked': linked, 'pieces': len(pieces), 'jev_questions': len(questions), 'jev_requests': len(jev_requests),
                       'analyst_user_chars': user_chars, 'analyst_tokens_est': user_chars // 4})
    save(arm, 'prepared.json', prepared)
    save(arm, 'build-report.json', report)
    # offline checks: every enum word of the schema appears in the system prompt (preflight D); ids resolve; sizes
    missing = [w for w in PROPS['action']['enum'] if w not in SYSTEM]
    print(f'arm {arm}: {len(prepared)} cases prepared; enum words missing from the prompt: {missing or "none"}; system {len(SYSTEM)} chars')
    print('| case | linked | pieces | jev questions | jev requests | analyst user chars | est. tokens |')
    print('|---|---|---|---|---|---|---|')
    for r in report:
        print(f"| {r['case']} | {','.join(r['linked']) or '-'} | {r['pieces']} | {r['jev_questions']} | {r['jev_requests']} | {r['analyst_user_chars']:,} | {r['analyst_tokens_est']:,} |")
    print('total est. analyst input tokens:', f"{sum(r['analyst_tokens_est'] for r in report):,}", '| jev requests:', sum(r['jev_requests'] for r in report))


def normalised(answer):
    """Arm 2 renamed same_as → same_claim_as and independent → independent_sources; checks and scores read one shape."""
    a = dict(answer)
    if 'same_claim_as' in a:
        a['same_as'] = a.pop('same_claim_as')
    if 'independent_sources' in a:
        a['independent'] = a.pop('independent_sources')
    return a


def code_checks(answer, prepared_case):
    answer = normalised(answer)
    problems = []
    ids = set(prepared_case['piece_ids']); qids = set(prepared_case['catalog_ids'])
    own = (prepared_case['payload']['source_record'].get('id') or '')      # the incoming record may be cited by its own id
    for field in ('same_as', 'revises', 'opposes'):
        bad = [x for x in answer[field] if x not in ids]
        if bad:
            problems.append(f'{field}: ids not in the expansion: {bad}')
    overlap = set(answer['same_as']) & set(answer['revises']) | set(answer['same_as']) & set(answer['opposes']) | set(answer['revises']) & set(answer['opposes'])
    if overlap:
        problems.append(f'ids in two relations: {sorted(overlap)}')
    bad_q = [q for q in answer['question_ids'] if q not in qids]
    if bad_q:
        problems.append(f'question_ids not in the catalog: {bad_q}')
    if answer['action'] == 'update_existing' and not answer['question_ids']:
        problems.append('update_existing without question_ids')
    if answer['action'] == 'propose_new' and not (answer['new_question'].strip() and answer['independent_judgement'].strip()):
        problems.append('propose_new without new_question and independent_judgement')
    for a in answer['arguments']:
        if a['question_id'] not in qids:
            problems.append(f'argument for unknown question {a["question_id"]}')
        bad = [x for x in a['support_ids'] + a['opposing_ids'] if x not in ids and x not in ('incoming', own)]
        if bad:
            problems.append(f'argument ids not in the expansion: {bad}')
    return problems


def send(arm, cap, repeats=1, only=None):
    prepared = load(arm, 'prepared.json')
    if only:
        prepared = {k: v for k, v in prepared.items() if k in only}
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v34.json'))
    archive = model.Archive(os.path.join(arm_dir(arm), 'archive.sqlite'))
    results = {}
    stop = {'reason': ''}

    def spent():
        return archive.totals()[1]

    def run_case(job):
        name, sample = job
        case = prepared[name]
        if stop['reason']:
            return (f'{name}.s{sample}' if sample else name), {'status': 'not_sent', 'reason': stop['reason']}
        opinion = {'questions': {}, 'pieces': {}}
        jev_cost = 0.0
        try:
            for req in case['jev_requests']:
                answer = jev.ask(archive, cfg, cfg.matching, req['state'], req['questions'], f'stage34:{arm}:jev:{name}')
                jev_cost += answer.cost_usd
                for qid, value in answer.data.items():
                    label, prob = value.get('choice'), (value.get('probabilities') or {}).get(value.get('choice'))
                    kind, _, rest = qid.partition('__')
                    if kind == 'rel':
                        opinion['questions'][rest] = [label, prob]
                    else:
                        vid, _, eid = rest.partition('__')
                        opinion['pieces'][eid] = [label, prob]
        except (model.SchemaError, model.TransportError) as error:
            opinion = {'questions': {}, 'pieces': {}, 'unavailable': str(error)[:300]}
        except Exception as error:  # a network failure closes new admissions; the case is recorded, not retried
            stop['reason'] = f'transport failure on {name}: {error!r}'[:300]
            return (f'{name}.s{sample}' if sample else name), {'status': 'not_sent', 'reason': stop['reason'], 'jev_cost': jev_cost}
        payload = dict(case['payload'], comparison_opinion=opinion)
        if sample:
            payload['sample'] = sample                       # variance only: a different request, the same content
        user = json.dumps(payload, ensure_ascii=False)
        tag = f'{name}.s{sample}' if sample else name
        save(arm, f'{tag}.analyst.request.json', {'system': SYSTEM, 'user': payload, 'schema': SCHEMA})
        if spent() >= cap:
            stop['reason'] = f'cap {cap} reached before {name}'
            return tag, {'status': 'not_sent', 'reason': stop['reason'], 'jev_cost': jev_cost, 'opinion': opinion}
        try:
            answer = model.call(archive, cfg, SETTING, SYSTEM, user, SCHEMA, 'research_update', f'stage34:{arm}:analyst:{tag}')
        except model.SchemaError as error:
            return tag, {'status': 'refused_schema', 'reason': str(error)[:300], 'jev_cost': jev_cost, 'opinion': opinion}
        except Exception as error:
            stop['reason'] = f'transport failure on {name}: {error!r}'[:300]
            return tag, {'status': 'not_sent', 'reason': stop['reason'], 'jev_cost': jev_cost, 'opinion': opinion}
        problems = code_checks(answer.data, case)
        save(arm, f'{tag}.analyst.answer.json', answer.data)
        return tag, {'status': 'refused_code' if problems else 'accepted', 'reason': '; '.join(problems)[:400], 'jev_cost': jev_cost,
                      'analyst_cost': answer.cost_usd, 'input_tokens': answer.input_tokens, 'output_tokens': answer.output_tokens,
                      'cached': answer.cached, 'opinion': opinion, 'answer': answer.data}
    jobs = [(name, k) for name in prepared for k in range(repeats)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for name, result in pool.map(run_case, jobs):
            results[name] = result
            print(f"{name}: {result['status']} {result.get('reason', '')[:120]} | jev ${result.get('jev_cost', 0):.4f} analyst ${result.get('analyst_cost', 0):.4f} in {result.get('input_tokens', 0):,}")
    calls, cost, tin, tout = archive.totals()
    try:
        previous = load(arm, 'results.json')['cases']
    except FileNotFoundError:
        previous = {}
    previous.update(results); results = previous
    save(arm, 'results.json', {'cases': results, 'archive_totals': {'calls': calls, 'cost_usd': cost, 'input_tokens': tin, 'output_tokens': tout}, 'cap': cap, 'stopped': stop['reason']})
    print(f'archive: {calls} calls, ${cost:.4f}, {tin:,} in / {tout:,} out; stopped: {stop["reason"] or "no"}')


S3_MAP = {'same': 'same_statement', 'revision': 'supersedes', 'different': 'different'}


def score(arm, gold_path=GOLD):
    gold = json.load(open(gold_path, encoding='utf-8'))
    results = {k: v for k, v in load(arm, 'results.json')['cases'].items() if '.s' not in k}
    rows = []
    for name, g in gold.items():
        if name.startswith('_'):
            continue
        r = results.get(name, {}); a = normalised(r['answer']) if r.get('answer') else None; op = r.get('opinion') or {}
        row = {'case': name, 'held_out': g.get('held_out', False), 'status': r.get('status', 'missing')}
        # step 3
        qs = op.get('questions', {}); ps = op.get('pieces', {})
        row['s3_question'] = all(qs.get(v, [None])[0] in (rel if isinstance(rel, list) else [rel]) for v, rel in g['s3_question'].items()) if g['s3_question'] else None
        row['s3_evidence'] = all(ps.get(e, [None])[0] in [S3_MAP[r] for r in (rel if isinstance(rel, list) else [rel])] for e, rel in g['s3_evidence'].items()) if g['s3_evidence'] else None
        if a is None:
            row.update(action=False, questions=False, same_as=False, revises=False, opposes=False, independent=False, untouched=False)
            rows.append(row); continue
        row['action'] = a['action'] in g.get('action_any', [g['action']])
        if g['action'] == 'propose_new':
            row['questions'] = True
        elif 'question_ids_any' in g:
            row['questions'] = bool(a['question_ids']) and set(a['question_ids']) <= set(g['question_ids_any'])
        else:
            row['questions'] = set(g['question_ids']) <= set(a['question_ids'])
        def relation(field, any_key, optional_key, optional_flag=None):
            groups = g.get(any_key) or ([g[field]] if g[field] else [])
            if optional_flag and g.get(optional_flag):
                groups = []
            allowed = set(x for grp in (g.get(any_key) or []) for x in grp) | set(g[field]) | set(g.get(optional_key, []))
            if optional_flag and g.get(optional_flag):
                allowed |= set(x for grp in (g.get(any_key) or []) for x in grp)
            return all(set(grp) & set(a[field]) for grp in groups) and set(a[field]) <= allowed
        row['same_as'] = relation('same_as', 'same_as_any_of', 'same_as_optional') and not (set(a['same_as']) & set(g.get('must_not_touch_same', [])))
        row['revises'] = relation('revises', 'revises_any_of', 'revises_optional')
        row['opposes'] = relation('opposes', 'opposes_any_of', 'opposes_optional_ids', 'opposes_optional')
        if g.get('relation_any_of'):
            joined = set(a['same_as']) | set(a['revises']) | set(a['opposes'])
            row['revises'] = row['revises'] and all(set(grp) & joined for grp in g['relation_any_of'])
        if g.get('question_ids_forbidden'):
            row['questions'] = row['questions'] and not (set(a['question_ids']) & set(g['question_ids_forbidden']))
        if g['same_as'] or g.get('same_as_any_of') or g['opposes'] or g.get('opposes_any_of') or g.get('relation_any_of'):
            row['independent'] = a['independent'] in g.get('independent_any', [g['independent']])
        else:
            row['independent'] = None          # vacuous when nothing is the same or opposed
        touched = set(a['same_as']) | set(a['revises'])
        row['untouched'] = not (touched & set(g.get('must_not_touch', [])))
        rows.append(row)
    fields = ['s3_question', 's3_evidence', 'action', 'questions', 'same_as', 'revises', 'opposes', 'independent', 'untouched']
    print('| case | status | ' + ' | '.join(fields) + ' |')
    print('|---|---|' + '---|' * len(fields))
    for row in rows:
        print(f"| {row['case']}{' (held out)' if row['held_out'] else ''} | {row['status']} | " + ' | '.join({True: 'ok', False: 'MISS', None: '-'}[row[f]] for f in fields) + ' |')
    for held in (False, True):
        sub = [r for r in rows if r['held_out'] == held]
        print(('held-out' if held else 'development') + ' totals: ' + ', '.join(f"{f} {sum(1 for r in sub if r[f] is True)}/{sum(1 for r in sub if r[f] is not None)}" for f in fields))
    save(arm, 'scores.json' if gold_path == GOLD else 'scores-' + os.path.basename(gold_path).replace('.json', '') + '.json', rows)


def variance(arm, gold_path=GOLD):
    """Per case with extra samples: whether the three draws agree on each exact field, and how many of the three the gold accepts."""
    gold = json.load(open(gold_path, encoding='utf-8'))
    results = load(arm, 'results.json')['cases']
    names = sorted({k.split('.s')[0] for k in results if '.s' in k})
    fields = ['action', 'question_ids', 'same_as', 'revises', 'opposes', 'independent']
    print(f'| case | draws | ' + ' | '.join(f'{f} agree' for f in fields) + ' | action accepted by gold |')
    print('|---|---|' + '---|' * (len(fields) + 1))
    for name in names:
        draws = [normalised(results[k]['answer']) for k in [name] + [f'{name}.s{i}' for i in (1, 2)] if k in results and results[k].get('answer')]
        g = gold.get(name, {})
        agree = []
        for f in fields:
            values = [json.dumps(sorted(d[f]) if isinstance(d[f], list) else d[f]) for d in draws]
            agree.append(f'{len(set(values))==1 and "yes" or "no"} ({len(set(values))})')
        ok = sum(1 for d in draws if d['action'] in g.get('action_any', [g.get('action')]))
        print(f'| {name} | {len(draws)} | ' + ' | '.join(agree) + f' | {ok}/{len(draws)} |')


if __name__ == '__main__':
    command, arm = sys.argv[1], sys.argv[2]
    if command == 'build':
        build(arm, sys.argv[3] if len(sys.argv) > 3 else CASES)
    elif command == 'send':
        send(arm, float(sys.argv[3]) if len(sys.argv) > 3 else 1.0, int(sys.argv[4]) if len(sys.argv) > 4 else 1, sys.argv[5].split(',') if len(sys.argv) > 5 else None)
    elif command == 'variance':
        variance(arm, sys.argv[3] if len(sys.argv) > 3 else GOLD)
    elif command == 'score':
        score(arm, sys.argv[3] if len(sys.argv) > 3 else GOLD)
