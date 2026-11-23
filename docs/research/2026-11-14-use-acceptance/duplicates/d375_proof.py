"""The $0 proof of D375's per-article list (D375-PROOF-DESIGN.md, version 3; D526). Built stage by stage; this file holds the stages
done so far. No model call, no external comparison call, no change to any package or frozen file.

  python3 d375_proof.py state <rebuilt scratch folder>        stage 1: the rebuilt store against the stored run, every table, column by column
  python3 d375_proof.py control <rebuilt scratch folder>      stage 2: the tested article through the real entry point on the day-start list, stored answers only
  python3 d375_proof.py discover <rebuilt scratch folder>     stage 3a: the requests the per-article list makes that the stored run never made (each is refused and listed)
  python3 d375_proof.py later <rebuilt scratch folder>        stage 4b: a later article behind an interrupted one (exits 1 if a requirement is broken)
  python3 d375_proof.py recover <rebuilt scratch folder>      stage 4: four interruptions through the bounded replay, each run again and compared with the uninterrupted run
  python3 d375_proof.py arm <rebuilt scratch folder> <same|same-repeat|different|veto|direct>   stage 3b: case A on the per-article list with a labelled fake answer to the one new relation
"""
import collections
import copy
import json
import os
import shutil
import sqlite3
import types
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, dispatch, extraction, model, replay, testdb, universe  # noqa: E402
from hivemind.views import round as rounds, store  # noqa: E402

ARTICLE_DAY, ARTICLE = '2026-09-27', 'gnews:2e603d9182199771803bce9b'      # article 175 of the week: it opened the second RTX question
OTHER_CASES = {'B': ('2026-09-24', 98), 'C': ('2026-09-22', 11)}            # case B: a distinct earlier same-day question; case C: a same-article pair
CASE = 'A'
# The only requests the fake may answer that the stored run never made, by case: anything else is refused and fails the arm.
PLANNED = {'A': {'relations': {'rel__v14'}, 'peers': {'v14'}, 'pieces': {'piece__v14__e278', 'piece__v14__e282', 'piece__v14__e283', 'piece__v14__e284'}},
           'B': {'relations': set(), 'peers': set(), 'pieces': set()}, 'C': {'relations': set(), 'peers': set(), 'pieces': set()}}
SECOND_QUESTION_ROWS = {'rungs', 'thesis_group_members', 'view_keys', 'view_switches', 'views', 'views_fts'}       # rows that exist only because the second question was opened
# The tables allowed to differ from the control arm, by content, registered before the checked run (case, arm). The "direct" arm's set
# was registered after its first, unchecked run showed the group's other names missing: only a candidate declares them (council round 18).
ALLOWED = {('A', 'same'): {'evidence_links', 'match_records', 'processing_steps'} | SECOND_QUESTION_ROWS,
           ('A', 'same-repeat'): {'evidence_links', 'match_records', 'processing_steps'} | SECOND_QUESTION_ROWS,
           ('A', 'different'): {'match_records'}, ('A', 'veto'): {'match_records'},
           ('A', 'direct'): {'evidence_links', 'handovers', 'match_records', 'processing_steps', 'thesis_group_aliases', 'groups_fts'} | SECOND_QUESTION_ROWS,
           ('B', 'different'): set(), ('C', 'different'): set()}
# What each arm of case A must end with: questions created by the article, the links of its statements, the decision on its candidate.
MUST_END = {'same': ([], {('e303', 'v14'), ('e303', 'v6'), ('e304', 'v14'), ('e304', 'v6')}, ('merge', 'v14')),
            'same-repeat': ([], {('e303', 'v14'), ('e303', 'v6'), ('e304', 'v14'), ('e304', 'v6')}, ('merge', 'v14')),
            'different': (['v15'], {('e303', 'v15'), ('e303', 'v6'), ('e304', 'v15'), ('e304', 'v6')}, ('new', '')),
            'veto': (['v15'], {('e303', 'v15'), ('e303', 'v6'), ('e304', 'v15'), ('e304', 'v6')}, ('new', '')),
            'direct': ([], {('e303', 'v14'), ('e303', 'v6'), ('e304', 'v14'), ('e304', 'v6')}, None)}
RUN = ROOT / 'poc/data/clean-lean-week-2026-11-14/week/p1/prod'
WALL_CLOCK = {'created_at', 'at', 'recorded_at', 'updated_at', 'marked_at', 'completed_at', 'timestamp'}
SEQUENCE_COLUMNS = ('seq', 'created_seq', 'after_seq', 'sequence_no')


def tables_of(conn):
    names = [row[0] for row in conn.execute("select name from sqlite_master where type = 'table' order by name")]
    return [name for name in names if name != 'sqlite_sequence' and not any(name.endswith(suffix) for suffix in ('_data', '_idx', '_content', '_docsize', '_config'))]


def rows_of(conn, table, top, allowed_views, allowed_groups):
    """The rows of one table that belong to the history up to article `top`, without wall-clock columns, as a sorted list."""
    columns = [row[1] for row in conn.execute(f'pragma table_info("{table}")')]
    kept = [c for c in columns if c not in WALL_CLOCK]
    rows = [dict(zip(columns, row)) for row in conn.execute(f'select {", ".join(chr(34) + c + chr(34) for c in columns)} from "{table}"')]
    sequence = next((c for c in SEQUENCE_COLUMNS if c in columns), None)
    if sequence:
        rows, rule = [r for r in rows if (r[sequence] or 0) <= top], f'{sequence} <= {top}'
    elif 'view_id' in columns:
        rows, rule = [r for r in rows if r['view_id'] in allowed_views], 'its question exists by then'
    elif 'group_id' in columns:
        rows, rule = [r for r in rows if r['group_id'] in allowed_groups], 'its group exists by then'
    else:
        rule = 'whole table'
    return sorted(tuple(str(r[c]) for c in kept) for r in rows), kept, [c for c in columns if c in WALL_CLOCK], rule


def stage_state(scratch):
    rebuilt = sqlite3.connect(f"file:{scratch / 'views.sqlite'}?mode=ro", uri=True)
    stored = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
    top = rebuilt.execute("select max(sequence_no) from processing_steps where step = 'handed_over' and result = 'ok'").fetchone()[0]
    allowed_views = {row[0] for row in stored.execute('select view_id from views where created_seq <= ?', (top,))}
    allowed_groups = {row[0] for row in stored.execute('select group_id from thesis_groups where created_seq <= ?', (top,))}
    print(f'the rebuilt store holds the history to article {top}; compared with the stored run, table by table (wall-clock columns set aside)')
    different = []
    for table in tables_of(stored):
        ours, kept, clocks, rule = rows_of(rebuilt, table, top, allowed_views, allowed_groups)
        theirs, _, _, _ = rows_of(stored, table, top, allowed_views, allowed_groups)
        same = ours == theirs
        print(f"  {table:26s} {len(theirs):5d} rows ({rule}); columns compared {len(kept)}" + (f", set aside {clocks}" if clocks else '') + f": {'identical' if same else 'DIFFERENT'}")
        if not same:
            different.append(table)
            only_ours = collections.Counter(ours) - collections.Counter(theirs)
            only_theirs = collections.Counter(theirs) - collections.Counter(ours)
            for label, extra in (('only in the rebuilt store', only_ours), ('only in the stored run', only_theirs)):
                for row in list(extra)[:4]:
                    print(f"      {label}: {dict(zip(kept, row))}"[:420])
            print(f"      rows only in the rebuilt store {sum(only_ours.values())}, only in the stored run {sum(only_theirs.values())}")
    print('tables that differ:', different or 'none')
    # the three expected differences, each checked and not assumed
    later_names = {row[0] for row in stored.execute('select alias from thesis_group_aliases where seq > ?', (top,))}
    extra_fts = collections.Counter(r[1] for r in stored.execute('select group_id, text from groups_fts')) - collections.Counter(r[1] for r in rebuilt.execute('select group_id, text from groups_fts'))
    explained = all(all(name in text for name in [n for n in later_names if n in text]) and any(n in text for n in later_names) for text in extra_fts)
    print(f"  groups_fts: every row the stored run has beyond the rebuilt store is made of other names added after article {top}: {explained}")
    content = 'select input_id, sequence_no, step, result, reason, publication_day from processing_steps where sequence_no between 1 and ?'
    ours, theirs = collections.Counter(rebuilt.execute(content, (top,)).fetchall()), collections.Counter(stored.execute(content, (top,)).fetchall())
    left = list((ours - theirs).elements())
    print(f"  processing_steps of articles 1 to {top}, by content (row numbers set aside): stored rows all present {not (theirs - ours)}; "
          f"rows only in the rebuilt store: {[(r[0], r[2], r[3]) for r in left]}")
    pool = rebuilt.execute('select kind, key, seq from review_pool_entries where id not in (select id from review_pool_entries limit 0)').fetchall()
    stored_pool = stored.execute('select kind, key, seq from review_pool_entries where seq <= ?', (top,)).fetchall()
    print(f"  review_pool_entries only in the rebuilt store: {list((collections.Counter(pool) - collections.Counter(stored_pool)).elements())}")
    print("  so the refused part-day judgement left two records (one processing step for the day, one review-pool entry); the item's entry point reads the processing steps of its own article only")


def refuse(*args, **kwargs):
    raise RuntimeError('a request was not in the stored archive: the network is refused')


def stage_control(scratch):
    """Case A, control arm: article 175 through dispatch and the real entry point on a copy of the rebuilt store, day-start list, stored answers only."""
    work = scratch.parent / (scratch.name + '-control')
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(scratch, work)
    cfg, uni = config.load(str(ROOT / 'poc/config/poc-v118.json')), universe.load(str(ROOT / 'poc/universe.json'))
    item = next(i for i in testdb.feed(testdb.open_db(str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite')), ARTICLE_DAY, ARTICLE_DAY) if i['input_id'] == ARTICLE)
    conn, archive = store.open_db(str(work / 'views.sqlite')), model.Archive(str(work / 'archive.sqlite'))
    calls_before = sqlite3.connect(work / 'archive.sqlite').execute('select count(*) from model_calls').fetchone()[0]
    route = dispatch.route(conn, item, uni)
    conn.commit()
    result = rounds.run(conn, archive, cfg, uni, item, route.sequence_no, resume_from=route.resume_from, transport=refuse, log=lambda *parts: None)
    conn.commit()
    conn.close()
    calls_after = sqlite3.connect(work / 'archive.sqlite').execute('select count(*) from model_calls').fetchone()[0]
    print(f"article dispatched at sequence {route.sequence_no} (resume {route.resume_from}); result: evidence {result.evidence}, candidates {result.candidates}, dropped {result.dropped}, failed {getattr(result, 'failed', None)}; "
          f"archive rows {calls_before} -> {calls_after}")
    rebuilt = sqlite3.connect(f"file:{work / 'views.sqlite'}?mode=ro", uri=True)
    stored = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
    top = route.sequence_no
    allowed_views = {row[0] for row in stored.execute('select view_id from views where created_seq <= ?', (top,))}
    allowed_groups = {row[0] for row in stored.execute('select group_id from thesis_groups where created_seq <= ?', (top,))}
    different = []
    for table in tables_of(stored):
        if table in ('processing_steps', 'review_pool_entries', 'groups_fts'):
            continue
        ours, kept, _, _ = rows_of(rebuilt, table, top, allowed_views, allowed_groups)
        theirs, _, _, _ = rows_of(stored, table, top, allowed_views, allowed_groups)
        if ours != theirs:
            different.append(table)
            only_ours, only_theirs = collections.Counter(ours) - collections.Counter(theirs), collections.Counter(theirs) - collections.Counter(ours)
            print(f"  {table}: DIFFERENT; only rebuilt {[dict(zip(kept, r)) for r in list(only_ours)[:2]]}; only stored {[dict(zip(kept, r)) for r in list(only_theirs)[:2]]}"[:900])
    content = 'select input_id, sequence_no, step, result, reason, publication_day from processing_steps where sequence_no = ?'
    steps_same = collections.Counter(rebuilt.execute(content, (top,)).fetchall()) == collections.Counter(stored.execute(content, (top,)).fetchall())
    fts = 'select group_id, text from groups_fts'
    names_after = {row[0] for row in stored.execute('select alias from thesis_group_aliases where seq > ?', (top,))}
    fts_extra = [t for t in (collections.Counter(r[1] for r in stored.execute(fts) if r[0] in allowed_groups) - collections.Counter(r[1] for r in rebuilt.execute(fts)))
                 if not any(n in t for n in names_after)]       # only groups that exist by the tested article; later groups are not a difference
    if different or not steps_same or fts_extra:
        print('FAIL: the control does not reproduce the stored run')
        raise SystemExit(1)
    print('PASS: the control reproduces the stored run')
    record = rebuilt.execute('select decisions_json from match_records where seq = ? order by id', (top,)).fetchall()
    print(f"tables compared to article {top} (all but the processing log, the review pool and the group search rows): differing {different or 'none'}; "
          f"the article's own processing steps identical by content: {steps_same}; group search rows the stored run has that later names do not explain: {fts_extra}")
    print(f"the question opened: {rebuilt.execute('select view_id, question from views where created_seq = ?', (top,)).fetchall()}")
    print(f"its stored reason (first 260 characters): {str(record[0][0])[:260] if record else None}")


class Unplanned(RuntimeError):
    pass


def stand_in_reader(stored_answer, call_id, request_sha256):
    """The stored reading answer of the article, through the real checks and filing on whatever list the entry point passes: a
    stand-in for the reading step on a changed list (it does not exercise the changed request or its archive key)."""
    def read(archive, cfg, item, text, shown, uni, *, transport=None):
        evidence, candidates, dropped, new_groups = extraction.sift_with_groups(copy.deepcopy(stored_answer), item, text, {v['view_id'] for v in shown}, uni)
        handle = types.SimpleNamespace(data=stored_answer, call_id=call_id, request_sha256=request_sha256, cached=True, cost_usd=0.0)
        return extraction.file_reading(extraction.Reading(evidence, candidates, dropped, new_groups, handle, 'stand-in'), item, shown)
    return read


def stage_discover(scratch):
    """Stage 3a: run the tested article on the per-article list with the stand-in reader and a transport that answers nothing; every
    request the run makes that is not in the stored archive is listed (kind and question ids) and refused. Repeated with each listed
    request answered would be stage 3b; this stage only maps what must be faked."""
    work = scratch.parent / (scratch.name + '-discover')
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(scratch, work)
    cfg, uni = config.load(str(ROOT / 'poc/config/poc-v118.json')), universe.load(str(ROOT / 'poc/universe.json'))
    item = next(i for i in testdb.feed(testdb.open_db(str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite')), ARTICLE_DAY, ARTICLE_DAY) if i['input_id'] == ARTICLE)
    conn, archive = store.open_db(str(work / 'views.sqlite')), model.Archive(str(work / 'archive.sqlite'))
    stored_archive = sqlite3.connect(f"file:{RUN / 'archive.sqlite'}?mode=ro", uri=True)
    call_id, sha, answer = stored_archive.execute("select call_id, request_sha256, answer_json from model_calls where purpose = 'extract' and request_json like ? order by call_id desc limit 1", (f'%{ARTICLE}%',)).fetchone()
    seen = []

    def listing_transport(*args):
        request = args[-1]
        if len(args) == 1:      # the external comparison is called with the request alone
            stored_match = None
            for other_json, other_answer in stored_archive.execute("select request_json, answer_json from model_calls where purpose = 'match'"):
                other = json.loads(other_json)
                if other.get('state') == request['state']:
                    stored_match = (other, json.loads(other_answer) if other_answer else None)
                    break
            old_questions = stored_match[0]['questions'] if stored_match else {}
            seen.append({'kind': 'comparison', 'questions': sorted(request['questions']), 'a stored request has the same state': bool(stored_match),
                         'unchanged questions': sorted(q for q in request['questions'] if old_questions.get(q) == request['questions'][q]),
                         'new or changed questions': sorted(q for q in request['questions'] if old_questions.get(q) != request['questions'][q]),
                         'criteria of a new question': next((request['questions'][q].get('criteria') for q in request['questions'] if q not in old_questions), None)})
        else:
            seen.append({'kind': 'model call', 'model': request.get('model'), 'schema': (request.get('response_format') or {}).get('json_schema', {}).get('name'),
                         'user text starts': request['messages'][-1]['content'][:160]})
        raise Unplanned(json.dumps(seen[-1])[:300])

    route = dispatch.route(conn, item, uni)
    conn.commit()
    original = store.day_start_seq
    store.day_start_seq = lambda connection, publication_day: route.sequence_no - 1
    try:
        result = rounds.run(conn, archive, cfg, uni, item, route.sequence_no, resume_from=route.resume_from, transport=listing_transport, log=lambda *parts: None,
                            extractor=stand_in_reader(json.loads(answer), call_id, sha))
    finally:
        store.day_start_seq = original
    conn.commit()
    print(f"sequence {route.sequence_no}; the run ended with: {[(r[0], r[1], r[2][:200]) for r in conn.execute('select step, result, reason from processing_steps where sequence_no = ? order by id', (route.sequence_no,))]}")
    for request in seen:
        print('  request made and refused:', json.dumps(request, ensure_ascii=False)[:900])


def stage_arm(scratch, arm, *, runner='direct', inject=None, work_name=None, resume=False, reference=None, bound=15, quiet=False):
    """Stage 3b, case A: the tested article on the per-article list, the stored reading answer as stand-in, and a fake comparison
    transport that assembles the response to the changed request from the individually stored answers to its unchanged questions
    plus one labelled value for the new relation. Any other request is refused and listed."""
    # each arm is a pair of labelled fake values: the first comparison's relation to v14, and the second comparison's verdict on v14
    # and, where the candidate is joined, the value given to each comparison of its statements with the statements already under v14
    wanted, judge_says, piece_says = {'same': ('same_quantity_or_event', 'same_question', 'different'), 'same-repeat': ('same_quantity_or_event', 'same_question', 'same_statement'),
                                      'different': ('different', 'different', 'different'), 'veto': ('same_quantity_or_event', 'different', None),
                                      'direct': (None, None, 'different')}[arm]
    work = scratch.parent / (work_name or (scratch.name + '-arm-' + arm))
    if not resume:
        if work.exists():
            shutil.rmtree(work)
        shutil.copytree(scratch, work)
    fired, reads, lists_seen = {}, {'count': 0}, {}
    cfg, uni = config.load(str(ROOT / 'poc/config/poc-v118.json')), universe.load(str(ROOT / 'poc/universe.json'))
    item = next(i for i in testdb.feed(testdb.open_db(str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite')), ARTICLE_DAY, ARTICLE_DAY) if i['input_id'] == ARTICLE)
    conn, archive = store.open_db(str(work / 'views.sqlite')), model.Archive(str(work / 'archive.sqlite'))
    stored_archive = sqlite3.connect(f"file:{RUN / 'archive.sqlite'}?mode=ro", uri=True)
    call_id, sha, answer = stored_archive.execute("select call_id, request_sha256, answer_json from model_calls where purpose = 'extract' and request_json like ? order by call_id desc limit 1", (f'%{ARTICLE}%',)).fetchone()
    every_match = [(json.loads(r), json.loads(a)) for r, a in stored_archive.execute("select request_json, answer_json from model_calls where purpose = 'match' and answer_json is not null")]
    stored_matches = [(r, a) for r, a in every_match if 'questions' in r]            # the first comparison's requests
    stored_collisions = [(r, a) for r, a in every_match if 'messages' in r and isinstance(a, dict) and 'relations' in a]     # the second comparison's
    made = []

    def fake_transport(*args):
        request = args[-1]
        if inject == 'comparison' and len(args) == 1 and not fired.get('comparison'):
            fired['comparison'] = True
            raise RuntimeError('injected failure: the comparison call')
        if len(args) != 1:
            schema_name = (request.get('response_format') or {}).get('json_schema', {}).get('name')
            user = request['messages'][-1]['content']
            if schema_name != 'collision' or '\n\nTHESES:\n' not in user:
                made.append({'kind': 'model call REFUSED', 'schema': schema_name, 'user text starts': user[:300]})
                raise Unplanned(json.dumps(made[-1])[:300])
            # the second comparison (one model call): the candidate's state, then one block a peer question
            state_text, peer_text = user.split('\n\nTHESES:\n', 1)
            blocks = {block.split('\n', 1)[0].strip(): block for block in peer_text.rsplit('\n\nFor each thesis id', 1)[0].split('--- ')[1:]}
            relations, reused, faked = [], [], []
            for peer, block in blocks.items():
                source = None
                for stored_request, stored_answer in stored_collisions:
                    stored_user = stored_request['messages'][-1]['content']
                    if stored_user.startswith(state_text + '\n\nTHESES:\n') and ('--- ' + block) in stored_user:
                        source = next((r for r in stored_answer['relations'] if r['thesis_id'] == peer), None)
                        break
                if source is not None:
                    relations.append(source)
                    reused.append(peer)
                elif peer in PLANNED[CASE]['peers'] and judge_says:
                    relations.append({'thesis_id': peer, 'relation': judge_says, 'why': 'LABELLED FAKE VALUE (the proof\'s arm), not a model\'s answer'})
                    faked.append(peer)
                else:
                    made.append({'kind': 'second comparison REFUSED', 'unplanned peer': peer})
                    raise Unplanned(json.dumps(made[-1])[:300])
            made.append({'kind': 'second comparison answered (synthetic response)', 'stored verdicts reused': {p: next(r['relation'] for r in relations if r['thesis_id'] == p) for p in reused},
                         'labelled fake values': {p: judge_says for p in faked}})
            return {'choices': [{'message': {'content': json.dumps({'relations': relations})}}], 'usage': {'prompt_tokens': 0, 'completion_tokens': 0}, 'synthetic': True}
        same_state = [(q, a) for q, a in stored_matches if q.get('state') == request['state']]
        answers, reused, faked = {}, [], []
        for qid, question in request['questions'].items():
            source = next((a[qid] for q, a in same_state if q['questions'].get(qid) == question and qid in a), None)
            if source is not None:
                answers[qid] = source
                reused.append(qid)
            elif qid in PLANNED[CASE]['pieces'] and piece_says in question.get('criteria', {}):
                others = [c for c in question['criteria'] if c != piece_says]
                answers[qid] = {'type': 'choice', 'choice': piece_says, 'probabilities': {piece_says: 0.9, **{c: round(0.1 / len(others), 6) for c in others}}}
                faked.append(qid)
            elif qid in PLANNED[CASE]['relations'] and wanted in question.get('criteria', {}):       # the one planned relation the stored run never asked: the arm's labelled value
                others = [c for c in question['criteria'] if c != wanted]
                answers[qid] = {'type': 'choice', 'choice': wanted, 'probabilities': {wanted: 0.9, **{c: round(0.1 / len(others), 6) for c in others}}}
                faked.append(qid)
            else:
                made.append({'kind': 'comparison REFUSED', 'unplanned question': qid, 'type': question.get('type'), 'criteria': list(question.get('criteria') or [])[:6],
                             'a stored request has the same state': bool(same_state)})
                raise Unplanned(json.dumps(made[-1])[:300])
        made.append({'kind': 'comparison answered (synthetic response)', 'stored answers reused': len(reused), 'labelled fake values': {q: answers[q]['choice'] for q in faked}})
        return {'answers': answers, 'usage': {'input_tokens': 0, 'output_tokens': 0}, 'synthetic': True}

    reading = json.loads(answer)
    if arm == 'direct':      # a labelled synthetic reading answer: no candidate, the candidate's statements linked straight to the earlier question
        gone = [c['id'] for c in reading['candidates']]
        reading['candidates'] = []
        for statement in reading['evidence']:
            statement['links'] = list(dict.fromkeys('v14' if link in gone else link for link in statement.get('links') or []))
    base_reader = stand_in_reader(reading, call_id, sha)

    def counting_reader(archive_, cfg_, item_, text_, shown_, uni_, *, transport=None):
        if inject == 'reading' and not fired.get('reading'):
            fired['reading'] = True
            raise RuntimeError('injected failure: the reading call')
        reads['count'] += 1
        return base_reader(archive_, cfg_, item_, text_, shown_, uni_, transport=transport)

    stopped = None
    if runner == 'direct':
        route = dispatch.route(conn, item, uni)
        conn.commit()
        original = store.day_start_seq
        store.day_start_seq = lambda connection, publication_day: route.sequence_no - 1
        try:
            rounds.run(conn, archive, cfg, uni, item, route.sequence_no, resume_from=route.resume_from, transport=fake_transport, log=lambda *parts: None,
                       extractor=counting_reader)
        finally:
            store.day_start_seq = original
        conn.commit()
        top = route.sequence_no
    else:       # through dispatch and the replay loop, bounded to the day's first items; only the tested article is still to be processed
        conn.close()
        top = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True).execute("select sequence_no from processing_steps where input_id = ? and step = 'dispatched'", (ARTICLE,)).fetchone()[0]
        originals = (store.day_start_seq, extraction.extract, store.add_evidence)
        original_shown = extraction.shown_views

        def shown_before_the_item(connection, cfg_, item_, objects_):
            """The per-article list for whichever item the loop is on: the store read at that item's own sequence minus one."""
            sequence = connection.execute('select max(sequence_no) from processing_steps where input_id = ?', (item_['input_id'],)).fetchone()[0]
            store.day_start_seq = lambda c, publication_day: sequence - 1
            listed = original_shown(connection, cfg_, item_, objects_)
            lists_seen.setdefault(item_['input_id'], []).append([v['view_id'] for v in listed])
            return listed

        def reader_for_the_item(archive_, cfg_, item_, text_, shown_, uni_, *, transport=None):
            if item_['input_id'] == ARTICLE:
                return counting_reader(archive_, cfg_, item_, text_, shown_, uni_, transport=transport)
            other_call, other_sha, other_answer = stored_archive.execute(     # another article of the bounded day: its own stored reading answer, as a stand-in
                "select call_id, request_sha256, answer_json from model_calls where purpose = 'extract' and request_json like ? order by call_id desc limit 1", (f"%{item_['input_id']}%",)).fetchone()
            return stand_in_reader(json.loads(other_answer), other_call, other_sha)(archive_, cfg_, item_, text_, shown_, uni_, transport=transport)

        extraction.shown_views = shown_before_the_item
        extraction.extract = reader_for_the_item
        if inject == 'writing':
            def failing_add(connection, **fields):
                fired['writes'] = fired.get('writes', 0) + 1
                if fired['writes'] == 2 and not fired.get('writing'):
                    fired['writing'] = True
                    fired['statements written before the error'] = connection.execute('select count(*) from evidence where created_seq = ?', (top,)).fetchone()[0]
                    raise RuntimeError('injected failure: inside the writer, after its first write')
                return originals[2](connection, **fields)
            store.add_evidence = failing_add
        try:
            replay.run(testdb_path=str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'), views_path=str(work / 'views.sqlite'), archive=archive, cfg=cfg, universe=uni,
                       from_day=ARTICLE_DAY, until_day=ARTICLE_DAY, only_objects={'NVDA'}, max_items_per_day=bound, transport=fake_transport, log=lambda *parts: None)
        except RuntimeError as error:
            stopped = str(error)[:170]
        finally:
            store.day_start_seq, extraction.extract, store.add_evidence = originals
            extraction.shown_views = original_shown
        conn = store.open_db(str(work / 'views.sqlite'))
    summary = {'stopped': stopped, 'reading calls': reads['count'], 'fired': dict(fired), 'lists': lists_seen,
               'statements of the article in the store': conn.execute('select count(*) from evidence where created_seq = ?', (top,)).fetchone()[0],
               'steps': [(r[0], r[1]) for r in conn.execute('select step, result from processing_steps where sequence_no = ? order by id', (top,))],
               'later articles with a step beyond dispatch': conn.execute("select count(*) from processing_steps where sequence_no > ? and step != 'dispatched'", (top,)).fetchone()[0],
               'later articles dispatched': conn.execute("select count(distinct sequence_no) from processing_steps where sequence_no > ?", (top,)).fetchone()[0]}
    if quiet:
        conn.close()
        return work, summary
    print(f"arm '{arm}' (labelled fakes: first comparison says '{wanted}' for v14, second comparison says '{judge_says}'); steps of article {top}: {[(r[0], r[1], r[2][:150]) for r in conn.execute('select step, result, reason from processing_steps where sequence_no = ? order by id', (top,))]}")
    for request in made:
        print('  request:', json.dumps(request, ensure_ascii=False)[:600])
    print(f"  questions created at article {top}: {[r[0] for r in conn.execute('select view_id from views where created_seq = ?', (top,))]}")
    print(f"  statements of the article and their links: {[(r[0], r[1]) for r in conn.execute('select l.evidence_id, l.view_id from evidence_links l join evidence e using(evidence_id) where e.created_seq = ? order by 1, 2', (top,))]}")
    for decisions, in conn.execute('select decisions_json from match_records where seq = ? order by id', (top,)):
        for candidate in json.loads(decisions).get('candidates') or []:
            print(f"  match record: {candidate.get('id')} -> {candidate.get('outcome')} {candidate.get('target_view_id')}; reason: ...{(candidate.get('reason') or '')[-330:]}")
    print(f"  group members added at article {top}: {[tuple(r) for r in conn.execute('select group_id, view_id from thesis_group_members where seq = ?', (top,))]}; "
          f"same-claim records: {[tuple(r)[:4] for r in conn.execute('select * from same_claims where seq = ?', (top,))]}")
    conn.close()
    # the product state after the article, against the control arm's (stage 2), table by table, by content
    control = reference or (scratch.parent / (scratch.name + '-control'))
    if control.exists():
        ours, theirs = sqlite3.connect(f"file:{work / 'views.sqlite'}?mode=ro", uri=True), sqlite3.connect(f"file:{control / 'views.sqlite'}?mode=ro", uri=True)
        everything = {row[0] for row in ours.execute('select view_id from views')} | {row[0] for row in theirs.execute('select view_id from views')}
        groups = {row[0] for row in theirs.execute('select group_id from thesis_groups')}
        lines = []
        for table in tables_of(theirs):
            mine, kept, _, _ = rows_of(ours, table, top, everything, groups)
            other, _, _, _ = rows_of(theirs, table, top, everything, groups)
            strip = [i for i, c in enumerate(kept) if c == 'id']
            mine = collections.Counter(tuple(v for i, v in enumerate(r) if i not in strip) for r in mine)
            other = collections.Counter(tuple(v for i, v in enumerate(r) if i not in strip) for r in other)
            if mine != other:
                lines.append(f"{table}: {sum((mine - other).values())} rows only in this arm, {sum((other - mine).values())} only in the control")
        print('  against the control arm, tables that differ by content: ' + ('; '.join(lines) or 'none'))
        # the registered expectations: a difference outside the allowed tables, an unplanned request, or a wrong end state fails the arm
        differing = {line.split(':', 1)[0] for line in lines}
        problems = []
        if os.environ.get('D375_MUTANT') == 'unrelated-row':       # positive control: an unrelated link is added to a table that is allowed to differ (the store is append-only); the arm must fail
            tamper = sqlite3.connect(work / 'views.sqlite')
            tamper.execute("insert into evidence_links (evidence_id, view_id, seq) values ('e1', 'v2', 5)")
            tamper.commit()
            tamper.close()
        # row by row: every differing row must be one the tested article explains, on the side the arm's registration says
        second_question = 'v15'
        rows_differing, _ = differences(work, control, top)
        for table, sides in rows_differing.items():
            for side, rows in sides.items():
                for row in rows:
                    of_the_article = any(str(row.get(column)) == str(top) for column in SEQUENCE_COLUMNS if column in row)
                    of_the_second_question = row.get('view_id') == second_question
                    of_its_group_names = table == 'groups_fts' and side == 'only in the reference'
                    if arm in ('different', 'veto') or CASE != 'A':
                        fine = table == 'match_records' and of_the_article
                    elif of_the_second_question or of_its_group_names:
                        fine = side == 'only in the reference'          # the second question's rows and its group's added names exist only in the control
                    else:
                        fine = of_the_article
                    if not fine:
                        problems.append(f"an unexplained differing row in {table} ({side}): {str(row)[:160]}")
        if (CASE, arm) not in ALLOWED:
            problems.append(f'no expectation is registered for case {CASE}, arm {arm}')
        elif not differing <= ALLOWED[(CASE, arm)]:
            problems.append(f'tables differ outside the allowed ones: {sorted(differing - ALLOWED[(CASE, arm)])}')
        if any('REFUSED' in request['kind'] for request in made):
            problems.append('an unplanned request was made')
        if summary['steps'][-1] != ('handed_over', 'ok'):
            problems.append(f"the article did not complete: {summary['steps']}")
        if CASE == 'A':
            check = sqlite3.connect(f"file:{work / 'views.sqlite'}?mode=ro", uri=True)
            created = [row[0] for row in check.execute('select view_id from views where created_seq = ?', (top,))]
            linked = set(check.execute('select l.evidence_id, l.view_id from evidence_links l join evidence e using(evidence_id) where e.created_seq = ?', (top,)).fetchall())
            decided = [(c.get('outcome'), c.get('target_view_id') or '') for d, in check.execute('select decisions_json from match_records where seq = ? order by id', (top,)) for c in json.loads(d).get('candidates') or []]
            must_create, must_link, must_decide = MUST_END[arm]
            if created != must_create or linked != must_link or (must_decide is not None and must_decide not in decided) or (must_decide is None and decided):
                problems.append(f'end state: created {created}, links {sorted(linked)}, decisions {decided}')
        print('  ' + ('PASS: the registered expectations hold' if not problems else 'FAIL: ' + '; '.join(problems)))
        if problems:
            raise SystemExit(1)
    return work, summary


def differences(work, reference, top):
    """Tables that differ by content (row numbers and wall-clock columns set aside) between two stores, up to article `top`."""
    ours, theirs = sqlite3.connect(f"file:{work / 'views.sqlite'}?mode=ro", uri=True), sqlite3.connect(f"file:{reference / 'views.sqlite'}?mode=ro", uri=True)
    everything = {row[0] for row in ours.execute('select view_id from views')} | {row[0] for row in theirs.execute('select view_id from views')}
    groups = {row[0] for row in theirs.execute('select group_id from thesis_groups')}
    out = {}
    for table in tables_of(theirs):
        mine, kept, _, _ = rows_of(ours, table, top, everything, groups)
        other, _, _, _ = rows_of(theirs, table, top, everything, groups)
        strip = [i for i, c in enumerate(kept) if c == 'id']
        mine = collections.Counter(tuple(v for i, v in enumerate(r) if i not in strip) for r in mine)
        other = collections.Counter(tuple(v for i, v in enumerate(r) if i not in strip) for r in other)
        if mine != other:
            out[table] = {'only here': [dict(zip([c for c in kept if c != 'id'], r)) for r in (mine - other).elements()], 'only in the reference': [dict(zip([c for c in kept if c != 'id'], r)) for r in (other - mine).elements()]}
    duplicates = ours.execute('select count(*) - count(distinct evidence_id || view_id) from evidence_links').fetchone()[0]
    return out, duplicates


def stage_later(scratch):
    """A later article behind an interrupted one (council round 18, point 3): the bounded replay takes the day's first sixteen items, so
    article 176 follows the tested article 175, whose comparison is made to fail once. Exits with an error if a requirement is broken."""
    stored = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
    later = stored.execute("select input_id from processing_steps where sequence_no = 176 and step = 'dispatched'").fetchone()[0]
    folder = scratch.name + '-later'
    work, first = stage_arm(scratch, 'same', runner='replay', inject='comparison', bound=16, work_name=folder, quiet=True)
    conn = sqlite3.connect(f"file:{work / 'views.sqlite'}?mode=ro", uri=True)
    after_failure = conn.execute('select step, result from processing_steps where input_id = ? order by id', (later,)).fetchall()
    conn.close()
    work, second = stage_arm(scratch, 'same', runner='replay', bound=16, work_name=folder, resume=True, quiet=True)
    conn = sqlite3.connect(f"file:{work / 'views.sqlite'}?mode=ro", uri=True)
    after_resume = conn.execute('select id, step, result from processing_steps where input_id = ? order by id', (later,)).fetchall()
    tested_done = conn.execute("select max(id) from processing_steps where input_id = ? and step = 'handed_over' and result = 'ok'", (ARTICLE,)).fetchone()[0]
    later_started = min((row[0] for row in after_resume if row[1] != 'dispatched'), default=None)
    links = sorted(conn.execute('select l.evidence_id, l.view_id from evidence_links l join evidence e using(evidence_id) where e.created_seq = 176').fetchall())
    stored_links = sorted(stored.execute('select l.evidence_id, l.view_id from evidence_links l join evidence e using(evidence_id) where e.created_seq = 176').fetchall())
    list_of_later = (second['lists'].get(later) or [[]])[-1]
    resumed_list = (second['lists'].get(ARTICLE) or [[]])[-1]
    first_list = (first['lists'].get(ARTICLE) or [[]])[-1]
    requirements = {
        'after the failure the later article is routed and not processed': after_failure == [('dispatched', 'ok')],
        'after the failure the day stopped on the failed item': bool(first['stopped']) and 'item failed' in first['stopped'],
        'on resume the tested article finishes before the later one starts': tested_done is not None and later_started is not None and tested_done < later_started,
        'the tested article is not read again on resume': second['reading calls'] == 0,
        'the list built at resume is the list of the first attempt': resumed_list == first_list and 'v14' in resumed_list,
        'the later article completes': [row[1:] for row in after_resume][-1] == ('handed_over', 'ok'),
        "the later article's list holds the earlier question and no second one": 'v14' in list_of_later and 'v15' not in list_of_later,
        "the later article's statements are filed as in the stored run": links == stored_links and len(links) > 0,
    }
    print(f"first run: stopped '{first['stopped']}'; steps of the later article: {after_failure}")
    print(f"run again: steps of the later article: {[row[1:] for row in after_resume]}; its list: {list_of_later}; its links: {links}")
    for name, held in requirements.items():
        print(f"  {'ok  ' if held else 'FAIL'} {name}")
    if not all(requirements.values()):
        raise SystemExit(1)


def stage_recover(scratch):
    """Stage 4: the tested article through dispatch and the bounded replay loop on the per-article list with the fakes of arm 'same',
    interrupted once at each of four places and run again; each final state against the uninterrupted run at the same point."""
    reference, clean = stage_arm(scratch, 'same', runner='replay', work_name=scratch.name + '-recover-reference', quiet=True)
    print(f"uninterrupted, through the bounded replay: {clean}")
    top = 175
    for name, label in (('reading', '1. the reading fails before any handover is saved'), ('comparison', '2. the handover is saved and the comparison fails'),
                        ('writing', '3. an error inside the writer after its first write'), (None, '4. the completed item is run again')):
        folder = scratch.name + '-recover-' + (name or 'again')
        work, first = stage_arm(scratch, 'same', runner='replay', inject=name, work_name=folder, quiet=True)
        print(f"\n{label}\n   first run: {first}")
        work, second = stage_arm(scratch, 'same', runner='replay', work_name=folder, resume=True, quiet=True)
        print(f"   run again: {second}")
        differing, duplicate_links = differences(work, reference, top)
        print(f"   against the uninterrupted run, tables that differ by content: {sorted(differing) or 'none'}; duplicate links: {duplicate_links}")
        # the registered expectations of this interruption: anything else fails the script
        failed_step = {'reading': 'extracted', 'comparison': 'matched', 'writing': 'written'}.get(name)
        pool_kind = {'reading': 'extraction_failed', 'comparison': 'matching_failed', 'writing': 'writing_failed', None: 'judging_failed'}[name]
        allowed_tables = {'processing_steps', 'review_pool_entries'} | ({'match_records'} if name == 'writing' else set())
        problems = []
        if not set(differing) <= allowed_tables:
            problems.append(f'product tables differ: {sorted(set(differing) - allowed_tables)}')
        if duplicate_links:
            problems.append('a link exists twice')
        if any(rows['only in the reference'] for rows in differing.values()):
            problems.append('a record of the uninterrupted run is missing')
        for row in differing.get('processing_steps', {}).get('only here', []):
            is_copy_mark = row['step'] == 'merged' and str(row['sequence_no']) == '0'
            is_failed_step = failed_step and row['input_id'] == ARTICLE and row['step'] == failed_step and row['result'] == 'failed'
            is_repeated_comparison = name == 'writing' and row['input_id'] == ARTICLE and row['step'] == 'matched' and row['result'] == 'ok'
            is_refused_judgement = row['input_id'].startswith('day:') and row['step'] == 'judged' and row['result'] == 'failed'
            if not (is_copy_mark or is_failed_step or is_repeated_comparison or is_refused_judgement):
                problems.append(f"an unexpected processing record: {row['input_id']} {row['step']} {row['result']}")
        if [row['kind'] for row in differing.get('review_pool_entries', {}).get('only here', [])] not in ([pool_kind], [] if name else [pool_kind]):
            problems.append(f"review-pool entries other than one {pool_kind}")
        if name == 'writing' and (len(differing.get('match_records', {}).get('only here', [])) != 2 or first['fired'].get('statements written before the error') != 1
                                  or first['statements of the article in the store'] != 0):
            problems.append('the mid-write case: not exactly one write before the error, a write left after it, or not exactly two repeated match records')
        # required, not merely allowed: the interruption happened and left exactly its failure record
        extra_steps = differing.get('processing_steps', {}).get('only here', [])
        if name:
            if not first['fired'].get(name):
                problems.append('the interruption did not happen')
            if sum(1 for row in extra_steps if row['input_id'] == ARTICLE and row['step'] == failed_step and row['result'] == 'failed') != 1:
                problems.append(f"not exactly one failed '{failed_step}' record for the article")
            if [row['kind'] for row in differing.get('review_pool_entries', {}).get('only here', [])] != [pool_kind]:
                problems.append(f'not exactly one review-pool entry of kind {pool_kind}')
            if not first['stopped'] or 'item failed' not in first['stopped']:
                problems.append('the first run did not stop on the failed item')
        else:
            if first['steps'][:5] != second['steps'][:5] or any(row['input_id'] == ARTICLE for row in extra_steps):
                problems.append('running the completed item again added a step for the article')
        if second['reading calls'] != (1 if name == 'reading' else 0):
            problems.append(f"reading calls on the second run: {second['reading calls']}")
        if second['statements of the article in the store'] != clean['statements of the article in the store']:
            problems.append('the article ends with another number of statements')
        print('   ' + ('PASS: the registered expectations hold' if not problems else 'FAIL: ' + '; '.join(problems)))
        if problems:
            raise SystemExit(1)
        for table, rows in differing.items():
            for side, items in rows.items():
                for row in items[:3]:
                    print(f"      {table}, {side}: " + str({k: str(v)[:110] for k, v in row.items() if k in ('input_id', 'sequence_no', 'step', 'result', 'reason', 'kind', 'key', 'seq', 'call_no')})[:420])


if __name__ == '__main__':
    # positive controls of the checks themselves: each breaks one registered expectation and must make the script fail
    if os.environ.get('D375_MUTANT') == 'unplanned':
        PLANNED['A'] = {'relations': set(), 'peers': set(), 'pieces': set()}          # the new relation is no longer planned: the arm must fail
    if os.environ.get('D375_MUTANT') == 'allowed':
        ALLOWED[('A', 'different')] = set()                                         # the match record may no longer differ: the arm must fail
    if os.environ.get('D375_MUTANT') == 'end-state':
        MUST_END['same'] = (['v15'], MUST_END['same'][1], MUST_END['same'][2])       # a second question is wrongly expected: the arm must fail
    if sys.argv[-1] in OTHER_CASES:
        CASE = sys.argv[-1]
        day, sequence = OTHER_CASES[sys.argv.pop()]
        source = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
        ARTICLE_DAY, ARTICLE = day, source.execute("select input_id from processing_steps where sequence_no = ? and step = 'dispatched'", (sequence,)).fetchone()[0]
    if sys.argv[1] == 'state':
        stage_state(Path(sys.argv[2]))
    elif sys.argv[1] == 'control':
        stage_control(Path(sys.argv[2]))
    elif sys.argv[1] == 'discover':
        stage_discover(Path(sys.argv[2]))
    elif sys.argv[1] == 'arm':
        stage_arm(Path(sys.argv[2]), sys.argv[3])
    elif sys.argv[1] == 'recover':
        stage_recover(Path(sys.argv[2]))
    elif sys.argv[1] == 'later':
        stage_later(Path(sys.argv[2]))
