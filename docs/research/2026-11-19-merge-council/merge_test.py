"""The merge test (D678, D679; EXECUTION-PLAN.md): clean Step 1 (c8, unchanged) reads each article with the old system's open
questions as its open theses, and the frozen production judge answers the target questions on the old history to 09-06 plus c8's
window evidence.

  python3 merge_test.py lists                 # $0: the open list per draw and article, and the request preflight
  python3 merge_test.py send <ledger>         # paid: one single-item c8 run per draw and article, 8 at a time
  python3 merge_test.py census                # $0: what c8 filed under the target questions, and the theses it proposed
  python3 merge_test.py judge <ledger> <arm>  # paid: the frozen judge, day by day, on the target questions only (arm: hybrid, control)
  python3 merge_test.py cards                 # $0: one card per answer, in the comparison deck's format

Everything is written under OUT. The old stores are read through read-only connections or copied, never written."""
import concurrent.futures
import copy
import importlib.util
import json
import sqlite3
import sys
import traceback
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT / 'clean-arch/step1'), str(ROOT / 'src')]
RUN = ROOT / 'poc/data/comparison-2026-11-17/run'
ITEMS = ROOT / 'poc/data/comparison-2026-11-17/items-comparison.sqlite'
PRD = ROOT / 'clean-arch/PRD.md'
OUT = ROOT / 'poc/data/merge-test-2026-11-19'
STEP1 = RUN / 'new-2/step1'                        # the stored c8 configuration: settings, limits, manifest
PROD_CONFIG = ROOT / 'poc/config/poc-v118.json'    # the configuration the old draws ran (their judge)
TARGETS = {'old-2': {'v5': 'M04', 'v40': 'M17'}, 'old-3': {'v6': 'M04', 'v47': 'M17', 'v48': 'M17'}}
BOUNDARY_DAY = '2026-09-06'                        # the history kept from the old store ends with this day
LAST_DAY = '2026-09-20'
FIRST_NEW_EVIDENCE = 900001                        # c8 evidence ids e900001…, beyond every old id


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def old_store(draw):
    conn = sqlite3.connect(f'file:{RUN / draw / "prod/views.sqlite"}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def articles():
    """Every test article once, in the old draws' processing order: (old seq, input id, publication day). Both old draws processed the
    same items in the same order (checked)."""
    chosen = json.loads((HERE / 'articles.json').read_text())
    wanted = set(chosen['capex']) | set(chosen['anthropic'])
    found = {}
    for draw in TARGETS:
        conn = old_store(draw)
        for input_id in wanted:
            row = conn.execute('select min(sequence_no), publication_day from processing_steps where input_id=?', (input_id,)).fetchone()
            if row[0] is None:
                raise SystemExit(f'{input_id} was not processed by {draw}')
            if found.setdefault(input_id, tuple(row)) != tuple(row):
                raise SystemExit(f'{input_id} has a different sequence in {draw}')
    return sorted((seq, input_id, day) for input_id, (seq, day) in found.items())


def open_views_at(conn, seq):
    """The old views open when the article with this sequence number was read: created at or before it, and not switched off at or
    before it. The views an article opened are included, since opening runs before filing in the merge."""
    out = []
    for view in conn.execute('select view_id from views where created_seq<=? order by created_seq, view_id', (seq,)):
        switch = conn.execute('select open from view_switches where view_id=? and after_seq<=? order by id desc limit 1',
                              (view['view_id'], seq)).fetchone()
        if switch is None or switch['open']:
            out.append(view['view_id'])
    return out


def thesis_of(conn, view_id):
    """An old view as a Step 1 open thesis (code-owned conversion): its id, its question, its observable focus as the outcome, and
    the reporting period and the deadline as two labelled parts. The answer choices stay with the judge."""
    view = conn.execute('select * from views where view_id=?', (view_id,)).fetchone()
    key = conn.execute('select * from view_keys where view_id=?', (view_id,)).fetchone()
    reporting = f"reporting period {key['period_start']} to {key['period_end']}; " if key and key['period_start'] else ''
    return {'id': view_id, 'entity': 'NVDA', 'description': view['question'], 'outcome': view['looks_at'],
            'period': f"{reporting}resolved by {view['due_day']}"}


def c8_configuration():
    settings = json.loads((STEP1 / 'settings.json').read_text())
    limits = json.loads((STEP1 / 'limits.json').read_text())
    manifest = json.loads((STEP1 / 'manifest.json').read_text())
    return settings, limits, manifest


def lists():
    """$0. Writes OUT/lists.json and checks that the request this test sends is the stored c8 request's bytes for the same state."""
    import runner
    from hivemind import config, model
    OUT.mkdir(parents=True, exist_ok=True)
    work = articles()
    plan = {}
    for draw in TARGETS:
        conn = old_store(draw)
        plan[draw] = [{'seq': seq, 'input_id': input_id, 'day': day,
                       'open': [thesis_of(conn, v) for v in open_views_at(conn, seq)]} for seq, input_id, day in work]
    (OUT / 'lists.json').write_text(json.dumps(plan, indent=1, ensure_ascii=False))
    # Preflight: rebuild new-2's stored request for one of these articles from its stored state with the code this test runs.
    settings, _, manifest = c8_configuration()
    stored = sqlite3.connect(f'file:{STEP1 / "trace.sqlite"}?mode=ro', uri=True)
    input_id = work[0][1]
    before, request = stored.execute('select before_state, request from trace where input_id=?', (input_id,)).fetchone()
    prompt, schema = runner.draft(PRD)
    closing = runner.closing_check(PRD)
    item = runner.selected_items(str(ITEMS), dict(manifest, item_ids=[input_id], item_limit=1))[0]
    shown = [{k: t[k] for k in ('id', 'description', 'outcome', 'period')} for t in json.loads(before)]
    tags = [x['value'] for x in item['object_identifiers'] if x.get('kind') == 'ticker']
    payload = {'current_entity': manifest['entity'], 'company_tags': tags, 'open_theses': shown, 'source_item': {
        'id': item['input_id'], 'publisher': item['publisher'], 'publication_date': item['publication_day'],
        'published_at': item['published_at'], 'publisher_type': item.get('publisher_type'), 'authors': item.get('authors'),
        'category': item.get('category'), 'source_uri': item['source_uri'], 'title': item['title'], 'text': item['text']}}
    setting = config.Setting('clean-step1', settings['model'], 'clean-step1', settings['reasoning_effort'], settings['max_output_tokens'])
    rebuilt = model.build_request(setting, prompt, json.dumps(payload, ensure_ascii=False) + f'\n\n{closing}', schema, 'clean_step1',
                                  settings['provider'])
    same = json.dumps(rebuilt) == request
    print(json.dumps({'articles': len(work), 'draws': list(plan),
                      'open theses per article (old-2 min/max)': [min(len(a['open']) for a in plan['old-2']),
                                                                  max(len(a['open']) for a in plan['old-2'])],
                      'preflight: rebuilt request equals the stored c8 request': same, 'preflight article': input_id}, indent=1))
    if not same:
        raise SystemExit('the request this test would send is not the stored c8 request: stop')


def send(ledger_path):
    """Paid. One single-item c8 run per draw and article, 8 at a time, each in its own folder; the ledger caps the total."""
    import runner
    from live import LiveTransport
    budget_replay = load('budget_replay', ROOT / 'clean-arch/e2e-comparison-2026-11-13/budget_replay.py')
    ledger = budget_replay.SharedLedger(ledger_path)
    budget_replay.install_stop_gate(ledger)
    settings, limits, manifest = c8_configuration()
    settings = dict(settings, live_limits=limits)
    plan = json.loads((OUT / 'lists.json').read_text())
    jobs = [(draw, entry) for draw in plan for entry in plan[draw]]

    def one(job):
        draw, entry = job
        folder = OUT / 'c8' / draw / f"{entry['seq']:05d}"
        if (folder / 'outcome.json').exists():
            return draw, entry['seq'], json.loads((folder / 'outcome.json').read_text())
        folder.mkdir(parents=True, exist_ok=False)
        try:
            outcome = runner.run(str(ITEMS), folder / 'trace.sqlite', dict(manifest, item_ids=[entry['input_id']], item_limit=1),
                                 copy.deepcopy(entry['open']), settings, LiveTransport(limits, ledger=ledger), PRD)
        except Exception as error:
            outcome = {'status': 'crashed', 'error': f'{type(error).__name__}: {error}', 'trace': traceback.format_exc()[-1500:]}
        (folder / 'outcome.json').write_text(json.dumps(outcome, indent=1))
        return draw, entry['seq'], outcome

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for draw, seq, outcome in pool.map(one, jobs):
            print(json.dumps({'draw': draw, 'seq': seq, 'status': outcome.get('status'), 'error': (outcome.get('error') or '')[:200]}),
                  flush=True)
    print('ledger', json.dumps(json.loads(Path(ledger_path).read_text())))


def records(draw):
    """c8's kept records of every completed article of a draw, with the old sequence number of their article."""
    run_forward = load('run_forward', ROOT / 'clean-arch/step2/run_forward.py')
    out = []
    for folder in sorted((OUT / 'c8' / draw).iterdir()):
        trace = folder / 'trace.sqlite'
        if not trace.exists():
            continue
        found, _, _ = run_forward.step1_records(str(trace))
        conn = sqlite3.connect(f'file:{trace}?mode=ro', uri=True)
        status, result = conn.execute('select status, result from trace').fetchone()
        proposed = (json.loads(result) or {}).get('new_theses', []) if result else []
        out.append({'seq': int(folder.name), 'status': status, 'records': [r for article in found for r in article],
                    'proposed': proposed})
    return out


def census():
    """$0. Per draw and target question: the c8 records filed under it, by article; and every thesis c8 proposed (none is opened)."""
    summary = {}
    for draw, targets in TARGETS.items():
        rows = records(draw)
        filed = {v: [] for v in targets}
        for row in rows:
            for record in row['records']:
                for view_id in set(record['thesis_ids']) & set(targets):
                    filed[view_id].append({'seq': row['seq'], 'day': record['publication_date'], 'summary': record['summary'],
                                           'verified': [p for p in (record['verified_passages'] or []) if p]})
        summary[draw] = {'articles read': len(rows), 'not complete': [r['seq'] for r in rows if r['status'] != 'complete'],
                         'records': sum(len(r['records']) for r in rows),
                         'filed under target': {v: len(x) for v, x in filed.items()},
                         'filed': filed,
                         'proposed theses': [{'seq': r['seq'], 'description': t['description'], 'outcome': t['outcome']}
                                             for r in rows for t in r['proposed']]}
    (OUT / 'census.json').write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps({d: {k: v for k, v in s.items() if k not in ('filed', 'proposed theses')} | {'proposed': len(s['proposed theses'])}
                      for d, s in summary.items()}, indent=1))


def judging_copy(draw, path):
    """A copy of the old store holding only what existed at the end of BOUNDARY_DAY: every row written after it is removed, so no later
    state leaks into a judgement. The store's append-only triggers are lifted in this copy for the cut and put back, as stored, before
    anything is written. The target questions created later are put back on the day they were created (`restore_view`)."""
    source = sqlite3.connect(f'file:{RUN / draw / "prod/views.sqlite"}?mode=ro', uri=True)
    target = sqlite3.connect(path)
    source.backup(target)
    source.close()
    triggers = target.execute("select name, sql from sqlite_master where type='trigger'").fetchall()
    for name, _ in triggers:
        target.execute(f'drop trigger {name}')
    boundary = target.execute('select seq from days_completed where day=?', (BOUNDARY_DAY,)).fetchone()[0]
    later_views = [r[0] for r in target.execute('select view_id from views where created_seq>?', (boundary,))]
    for table, column in (('judgements', 'seq'), ('evidence_links', 'seq'), ('evidence_sources', 'seq'), ('same_claims', 'seq'),
                          ('revisions', 'seq'), ('replacements', 'seq'), ('view_switches', 'after_seq'), ('successions', 'seq'),
                          ('days_completed', 'seq'), ('evidence', 'created_seq')):
        target.execute(f'delete from {table} where {column}>?', (boundary,))
    for table in ('views', 'rungs', 'view_keys'):
        target.execute(f"delete from {table} where view_id in ({','.join('?' * len(later_views))})", later_views)
    for _, sql in triggers:
        target.execute(sql)
    target.commit()
    counts = {t: target.execute(f'select max({c}) from {t}').fetchone()[0] for t, c in (('judgements', 'seq'), ('evidence_links', 'seq'),
              ('evidence', 'created_seq'), ('evidence_sources', 'seq'), ('views', 'created_seq'))}
    if any(v is not None and v > boundary for v in counts.values()):
        raise SystemExit(f'the cutoff copy holds a later row: {counts}')
    target.close()
    return boundary


def restore_closures(conn, draw, targets, seq):
    """After a day's judging, the target questions the old system switched off by the end of that day are switched off as it did."""
    source = old_store(draw)
    marks = ','.join('?' * len(targets))
    for row in source.execute(f'select * from view_switches where view_id in ({marks}) and open=0 and after_seq<=?', (*targets, seq)):
        if not conn.execute('select 1 from view_switches where view_id=? and open=0 and after_seq=?', (row['view_id'], row['after_seq'])).fetchone():
            conn.execute('insert into view_switches (view_id, open, reason, by_whom, after_seq) values (?,?,?,?,?)',
                         (row['view_id'], 0, row['reason'], row['by_whom'], row['after_seq']))


def restore_view(conn, draw, view_id):
    """Put a target question back as the old system created it: its row, choices, key and opening switch."""
    source = old_store(draw)
    for table in ('views', 'rungs', 'view_keys'):
        for row in source.execute(f'select * from {table} where view_id=?', (view_id,)):
            conn.execute(f"insert into {table} ({','.join(row.keys())}) values ({','.join('?' * len(row))})", tuple(row))
    row = source.execute('select * from view_switches where view_id=? and open=1 order by id limit 1', (view_id,)).fetchone()
    conn.execute('insert into view_switches (view_id, open, reason, by_whom, after_seq) values (?,?,?,?,?)',
                 (view_id, 1, row['reason'], row['by_whom'], row['after_seq']))


def copy_rows(conn, source, table, where, args):
    """Copy the old store's rows of one table that match `where` into the judging copy, all columns as stored; returns how many."""
    rows = source.execute(f'select * from {table} where {where}', args).fetchall()
    for row in rows:
        conn.execute(f"insert or ignore into {table} ({','.join(row.keys())}) values ({','.join('?' * len(row))})", tuple(row))
    return len(rows)


def hybrid_feed(draw, targets, conn, store, adapter, log):
    """The hybrid arm: c8's records filed under the target questions, written at their article's old sequence number with the clean
    adapter's field mapping. Returns a function (day, previous day's seq, day's seq, pending) -> the views that got a link."""
    by_day = {}
    for row in records(draw):
        for record in row['records']:
            if set(record['thesis_ids']) & set(targets):
                by_day.setdefault(record['publication_date'], []).append((row['seq'], record))
    counter = [FIRST_NEW_EVIDENCE]

    def feed(day, previous_seq, seq, pending):
        changed = set()
        for article_seq, record in sorted(by_day.get(day, []), key=lambda x: (x[0], x[1]['id'])):
            quote = adapter.quote_of(record)
            if not quote:
                log.append({'day': day, 'dropped': record['id'], 'reason': 'no verified passage'})
                continue
            evidence_id = f'e{counter[0]}'
            counter[0] += 1
            store.add_evidence(conn, evidence_id=evidence_id, quote=quote, one_line=record['summary'],
                               speaker=record.get('reporting_speaker') or record.get('original_party') or '',
                               original_who=record.get('original_party') or '', original_day=record.get('statement_date') or '',
                               tier=record['tier'], event_time=None, seq=article_seq, input_id=record['input_id'])
            store.add_source(conn, evidence_id, record['input_id'], 'news', record['publication_date'], None, article_seq)
            log.append({'day': day, 'evidence': evidence_id, 'record': record['id'], 'views': sorted(set(record['thesis_ids']) & set(targets))})
            for view_id in set(record['thesis_ids']) & set(targets):
                if view_id in pending:
                    log.append({'day': day, 'record': record['id'], 'reason': f'{view_id} not yet created'})
                    continue
                if store.link(conn, evidence_id, view_id, article_seq):
                    changed.add(view_id)
        return changed
    return feed


def control_feed(draw, targets, conn, log):
    """The control arm: the old system's own window links to the target questions, with the evidence they point to and its sources,
    copied with the ids and sequence numbers the old system gave them; and every repeat, revision or replacement relation touching
    evidence linked to a target question, with its counterpart's evidence and sources, from the day it was written."""
    old = old_store(draw)
    marks = ','.join('?' * len(targets))
    relations = (('same_claims', 'old_evidence_id', 'new_evidence_id'), ('revisions', 'old_evidence_id', 'new_evidence_id'),
                 ('replacements', 'old_evidence_id', 'new_evidence_id'))
    copied = set()

    def bring(evidence_id, seq):
        copy_rows(conn, old, 'evidence', 'evidence_id=?', (evidence_id,))
        copy_rows(conn, old, 'evidence_sources', 'evidence_id=? and seq<=?', (evidence_id, seq))

    def feed(day, previous_seq, seq, pending):
        changed = set()
        for link in old.execute(f'select * from evidence_links where view_id in ({marks}) and seq>? and seq<=? order by seq, id',
                                (*targets, previous_seq, seq)).fetchall():
            bring(link['evidence_id'], seq)
            conn.execute('insert into evidence_links (evidence_id, view_id, seq) values (?,?,?)', (link['evidence_id'], link['view_id'], link['seq']))
            changed.add(link['view_id'])
            log.append({'day': day, 'evidence': link['evidence_id'], 'view': link['view_id'], 'seq': link['seq']})
        for evidence_id in [r[0] for r in conn.execute(f'select distinct evidence_id from evidence_links where view_id in ({marks})', tuple(targets))]:
            copy_rows(conn, old, 'evidence_sources', 'evidence_id=? and seq>? and seq<=?', (evidence_id, previous_seq, seq))
        linked = {r[0] for r in conn.execute(f'select evidence_id from evidence_links where view_id in ({marks})', tuple(targets))}
        for table, a, b in relations:
            for row in old.execute(f'select * from {table} where seq<=? order by seq, id', (seq,)).fetchall():
                if (table, row['id']) in copied or not ({row[a], row[b]} & linked):
                    continue
                for evidence_id in (row[a], row[b]):
                    bring(evidence_id, seq)
                copy_rows(conn, old, table, 'id=?', (row['id'],))
                copied.add((table, row['id']))
                log.append({'day': day, 'relation': table, 'pair': [row[a], row[b]], 'seq': row['seq']})
        return changed
    return feed


class ReplayOld:
    """$0 transport for the replay check: answers each judge request with the old system's archived answer for the same view on the
    same day, and records whether the request text equals the archived request (theme questions) or shows the same evidence ids."""

    def __init__(self, draw):
        from hivemind.views import judging
        self.judging = judging
        self.old = sqlite3.connect(f'file:{RUN / draw / "prod/views.sqlite"}?mode=ro', uri=True, check_same_thread=False)
        self.old.row_factory = sqlite3.Row
        self.archive = sqlite3.connect(f'file:{RUN / draw / "prod/archive.sqlite"}?mode=ro', uri=True, check_same_thread=False)
        self.seq = None
        self.checks = []

    def __call__(self, provider, request):
        import re
        text = request['messages'][-1]['content']
        view_id = re.search(r'^Thesis (\S+) \(', text, re.M).group(1)
        row = self.old.execute('select call_id from judgements where view_id=? and seq=? order by judgement_id limit 1', (view_id, self.seq)).fetchone()
        old_request, old_response = self.archive.execute('select request_json, response_json from model_calls where call_id=?', (row['call_id'],)).fetchone()
        old_text = json.loads(old_request)['messages'][-1]['content']
        self.checks.append({'seq': self.seq, 'view': view_id, 'same text': text == old_text,
                            'same evidence shown': sorted(self.judging.evidence_shown_in(text)) == sorted(self.judging.evidence_shown_in(old_text))})
        return json.loads(old_response)


def judge(ledger_path, arm, replay_check=False):
    """Paid. Per draw: the judging copy, then day by day the arm's evidence for the target questions is written, and the frozen
    judge's own round judges the target questions that got a link that day, with that day's old closing sequence number. No other
    view is judged: the round's queue is restricted to the changed target questions. With replay_check ($0, control arm only), each
    request is answered with the old archived answer and compared with the archived request."""
    from hivemind import config, model
    from hivemind.views import judging, store
    budget_replay = load('budget_replay', ROOT / 'clean-arch/e2e-comparison-2026-11-13/budget_replay.py')
    adapter = load('clean_adapter', ROOT / 'clean-arch/e2e-2026-11-09/adapter.py')
    if not replay_check:
        ledger = budget_replay.SharedLedger(ledger_path)
        budget_replay.install_stop_gate(ledger)
        transport = budget_replay.BudgetTransport(ledger)
    cfg = config.load(PROD_CONFIG)
    judging.queued_by_change = lambda conn, view_id: []        # judge the target questions only
    judging.queued_by_ledger = lambda conn, seq: []
    results = {}
    only = [d for d in sys.argv[4:]]            # optional: the draws to judge in this process
    for draw, targets in TARGETS.items():
        if only and draw not in only:
            continue
        folder = OUT / (f'judge-{arm}' if not replay_check else 'judge-replaycheck') / draw
        folder.mkdir(parents=True, exist_ok=False)
        if replay_check:
            transport = ReplayOld(draw)
        boundary = judging_copy(draw, folder / 'views.sqlite')
        conn = store.open_db(str(folder / 'views.sqlite'))
        archive = model.Archive(str(folder / 'archive.sqlite'))
        old = old_store(draw)
        day_seq = dict(old.execute('select day, seq from days_completed').fetchall())
        created = {v: old.execute('select created_seq from views where view_id=?', (v,)).fetchone()[0] for v in targets}
        pending = {v for v, s in created.items() if s > boundary}
        log = []
        feed = hybrid_feed(draw, targets, conn, store, adapter, log) if arm == 'hybrid' else control_feed(draw, targets, conn, log)
        previous_seq = boundary
        for day in sorted(d for d in day_seq if BOUNDARY_DAY < d <= LAST_DAY):
            seq = day_seq[day]
            for view_id in sorted(pending):
                if created[view_id] <= seq:
                    restore_view(conn, draw, view_id)
                    pending.discard(view_id)
            changed = feed(day, previous_seq, seq, pending)
            previous_seq = seq
            conn.commit()
            if replay_check:      # the old system's own schedule, so each request can be compared with the archived one
                changed = {r[0] for r in old.execute(f"select view_id from judgements where seq=? and view_id in ({','.join('?' * len(targets))})",
                                                       (seq, *targets))}
            else:                 # one schedule for both arms: every open target question with evidence in force, every day to 09-20
                changed = {v for v in targets if v not in pending}
            if changed:
                if replay_check:
                    transport.seq = seq
                judged = judging.round_of_judgements(archive, cfg, conn, sorted(changed), seq, {'input_id': f'day:{day}', 'publication_day': day},
                                                     transport=transport)
                conn.commit()
                for j in judged:
                    log.append({'day': day, 'view': j['view_id'], 'rung': j['rung'], 'changed': j['changed']})
                    print(json.dumps({'draw': draw, 'day': day, 'view': j['view_id'], 'rung': j['rung']}), flush=True)
            restore_closures(conn, draw, list(targets), seq)
            conn.commit()
        results[draw] = log
        (folder / 'log.json').write_text(json.dumps(log, indent=1, ensure_ascii=False))
        if replay_check:
            (folder / 'checks.json').write_text(json.dumps(transport.checks, indent=1))
            print(draw, json.dumps(transport.checks))
    if not replay_check:
        print('ledger', json.dumps(json.loads(Path(ledger_path).read_text())))


def card(conn, view_id, cutoff_seq):
    """The deck's card text for a view: question, choices, the last answer at or before the cutoff, its reasons and the material that
    judgement was shown (the frozen selection rebuilt at that judgement)."""
    view = conn.execute('select * from views where view_id=?', (view_id,)).fetchone()
    rungs = conn.execute('select label, condition from rungs where view_id=? order by position', (view_id,)).fetchall()
    last = conn.execute('select * from judgements where view_id=? and seq<=? order by seq desc, judgement_id desc limit 1',
                        (view_id, cutoff_seq)).fetchone()
    return view, rungs, last


def cards():
    """$0. Writes OUT/cards/<draw>-<view>-{old,hybrid}.json: the question, the choices, the last answer at the cutoff, its reasons, and
    every piece of evidence the request of that answer listed, read back from the archived request."""
    from hivemind.views import judging
    out = OUT / 'cards'
    out.mkdir(parents=True, exist_ok=True)
    for draw, targets in TARGETS.items():
        for arm, views_path, archive_path in (('old', RUN / draw / 'prod/views.sqlite', RUN / draw / 'prod/archive.sqlite'),
                                              ('control', OUT / 'judge-control' / draw / 'views.sqlite', OUT / 'judge-control' / draw / 'archive.sqlite'),
                                              ('hybrid', OUT / 'judge-hybrid' / draw / 'views.sqlite', OUT / 'judge-hybrid' / draw / 'archive.sqlite')):
            conn = sqlite3.connect(f'file:{views_path}?mode=ro', uri=True)
            conn.row_factory = sqlite3.Row
            archive = sqlite3.connect(f'file:{archive_path}?mode=ro', uri=True)
            cutoff = conn.execute('select max(seq) from judgements').fetchone()[0]
            for view_id in targets:
                view, rungs, last = card(conn, view_id, cutoff)
                if last is None:
                    (out / f'{draw}-{view_id}-{arm}.json').write_text(json.dumps({'draw': draw, 'view': view_id, 'arm': arm, 'answer': None}))
                    continue
                request = archive.execute('select request_json from model_calls where call_id=?', (last['call_id'],)).fetchone()
                text = json.loads(request[0])['messages'][-1]['content'] if request else ''
                shown = judging.evidence_shown_in(text) if text else set()
                pieces = []
                for evidence_id in sorted(shown, key=lambda e: int(e[1:])):
                    row = conn.execute('select * from evidence where evidence_id=?', (evidence_id,)).fetchone()
                    source = conn.execute('select * from evidence_sources where evidence_id=? order by seq limit 1', (evidence_id,)).fetchone()
                    pieces.append({'evidence_id': evidence_id, 'tier': row['tier'], 'speaker': row['speaker'], 'original_who': row['original_who'],
                                   'original_day': row['original_day'], 'published': source['publication_day'] if source else None,
                                   'input_id': source['input_id'] if source else None, 'one_line': row['one_line'], 'quote': row['quote']})
                (out / f'{draw}-{view_id}-{arm}.json').write_text(json.dumps(
                    {'draw': draw, 'view': view_id, 'arm': arm, 'question': view['question'], 'opened': view['created_at'][:10],
                     'due': view['due_day'], 'choices': [r['condition'] for r in rungs], 'answer_rung': last['rung'],
                     'answer': rungs[last['rung'] - 1]['condition'], 'reasons': last['reasons'], 'judged_day': last['publication_day'],
                     'judgements': conn.execute('select count(*) from judgements where view_id=?', (view_id,)).fetchone()[0],
                     'material': pieces}, indent=1, ensure_ascii=False))
                print(draw, view_id, arm, 'rung', last['rung'], 'material', len(pieces))


KEY = Path.home() / '.hivemind-keys/merge-test-2026-11-19/key.json'
DIAGNOSTIC_DECK = ROOT / 'poc/data/comparison-2026-11-17/reading-diagnostic/deck'
DIAGNOSTIC_KEY = Path.home() / '.hivemind-keys/comparison-2026-11-17/deck-key.json'
STAGE0 = ROOT / 'docs/research/2026-11-17-product-comparison/stage0'


def card_entry(build_cards, views_path, archive_path, view_id):
    """`build_cards.library`'s entry for one question, read from one store and its own archive: the arms' copies hold other questions
    whose judgements were made in the old archive, which the library builder would look for in the arm's archive."""
    conn, archive, items = build_cards.ro(views_path), build_cards.ro(archive_path), build_cards.ro(ITEMS)
    v = conn.execute('select view_id, question, due_day, created_seq, created_from_input from views where view_id=?', (view_id,)).fetchone()
    latest = conn.execute('select rung, reasons, request_sha256, seq from judgements where view_id=? order by seq desc limit 1', (view_id,)).fetchone()
    rungs = build_cards.conditions(view_id, conn)
    publisher_of = lambda input_id: (items.execute('select publisher from items where input_id=?', (input_id,)).fetchone() or [None])[0]
    day = (items.execute('select publication_day from items where input_id=?', (v['created_from_input'],)).fetchone() or [None])[0]
    entry = {'question_id': view_id, 'question': v['question'], 'due': v['due_day'], 'opened': day, 'opened_from': v['created_from_input'],
             'possible_answers': [rungs[p] for p in sorted(rungs)], 'answer': None, 'reasons': None, 'material': []}
    if latest is not None:
        row = archive.execute('select request_json from model_calls where request_sha256=? limit 1', (latest['request_sha256'],)).fetchone()
        entry['answer'] = rungs.get(latest['rung'])
        entry['rung'] = latest['rung']
        entry['reasons'] = latest['reasons']
        entry['material'] = [dict(item, publisher=publisher_of(item['input_id'])) for item in build_cards.material(row['request_json'])]
        entry['context'] = build_cards.context(row['request_json'], conn)
        if entry['context']['previous']:
            entry['context']['previous']['answer'] = rungs.get(entry['context']['previous']['rung'])
    return entry


def deck():
    """$0. The reading deck, in the comparison's card form (`build_cards.card_text`, card-spec.md): every target question in three arms
    (the old answer as archived, the control and the hybrid), each card's library list taken from the old store so the arms show the
    same list; plus five controls copied from the diagnostic deck (three plants confirmed not supported, two cards confirmed
    supported). Shuffled; the key is kept outside the repository."""
    import random
    sys.path[:0] = [str(STAGE0), str(STAGE0 / 'census')]
    import build_cards
    folder = OUT / 'deck'
    folder.mkdir(parents=True, exist_ok=False)
    if KEY.exists():
        raise SystemExit(f'refused: {KEY} exists')
    cards = []
    for draw, targets in TARGETS.items():
        old_lib = build_cards.library(RUN / draw / 'prod/views.sqlite', RUN / draw / 'prod/archive.sqlite', ITEMS)
        for arm, views, archive in (('old', RUN / draw / 'prod/views.sqlite', RUN / draw / 'prod/archive.sqlite'),
                                    ('control', OUT / 'judge-control' / draw / 'views.sqlite', OUT / 'judge-control' / draw / 'archive.sqlite'),
                                    ('hybrid', OUT / 'judge-hybrid' / draw / 'views.sqlite', OUT / 'judge-hybrid' / draw / 'archive.sqlite')):
            for view_id, matter in targets.items():
                entry = card_entry(build_cards, views, archive, view_id)
                cards.append({'draw': draw, 'view': view_id, 'matter': matter, 'arm': arm, 'role': 'product',
                              'answered': entry['answer'] is not None, 'answer': entry['answer'],
                              'material': len(entry['material']), 'text': build_cards.card_text(entry, old_lib)})
    diagnostic = json.loads(DIAGNOSTIC_KEY.read_text())
    plants = sorted(c for c, k in diagnostic.items() if k['role'] == 'plant' and k['draw'].startswith('old'))[:3]
    supported = sorted(c for c, k in diagnostic.items() if k['role'] == 'supported control')[:2]
    for cid in plants + supported:
        cards.append({'draw': diagnostic[cid]['draw'], 'view': diagnostic[cid]['question'], 'matter': None, 'arm': 'diagnostic ' + cid,
                      'role': diagnostic[cid]['role'], 'answered': True, 'text': (DIAGNOSTIC_DECK / f'{cid}.txt').read_text()})
    random.Random(20261119).shuffle(cards)
    key = {}
    for n, card in enumerate(cards, 1):
        cid = f'C{n:03d}'
        key[cid] = {k: v for k, v in card.items() if k != 'text'}
        (folder / f'{cid}.txt').write_text(card['text'])
    KEY.parent.mkdir(parents=True, exist_ok=True)
    KEY.write_text(json.dumps(key, indent=1) + '\n')
    print(f'{len(cards)} cards; key in {KEY}')
    for cid, k in key.items():
        print(cid, k['draw'], k['view'], k['arm'], k['role'], 'material', k.get('material'))


def read():
    """Both reader families mark every card (`mark_cards.mark`), then debate rounds 1 and 2 on differing marks; prints each card's
    final marks beside its key."""
    sys.path[:0] = [str(STAGE0), str(STAGE0 / 'census')]
    import mark_cards
    mark_cards.KEY = KEY                     # this deck's key (outside the repository), not the comparison deck's
    folder = OUT / 'deck'
    if not (folder / 'round-0.done').exists():
        mark_cards.mark(folder)
    for round_number in (1, 2):
        if not (folder / f'round-{round_number}.done').exists():
            mark_cards.debate(folder, round_number)
    key = json.loads(KEY.read_text())
    finals = {cid: mark_cards.final(folder, cid) for cid in sorted(key)}
    (OUT / 'marks.json').write_text(json.dumps({cid: dict(key[cid], marks=finals[cid]) for cid in key}, indent=1, ensure_ascii=False))
    for cid in sorted(key):
        k = key[cid]
        print(cid, k['draw'], k['view'], k['arm'], k['role'], json.dumps(finals[cid]))


if __name__ == '__main__':
    command = sys.argv[1]
    {'lists': lambda: lists(), 'send': lambda: send(sys.argv[2]), 'census': lambda: census(),
     'judge': lambda: judge(sys.argv[2], sys.argv[3]), 'replaycheck': lambda: judge(None, 'control', replay_check=True),
     'cards': lambda: cards(), 'deck': lambda: deck(), 'read': lambda: read()}[command]()
