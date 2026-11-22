"""The paid whole-window comparison of poc-v120 against fresh controls (PAID-DESIGN.md, D707). One sequence per process.

  python3 paid_run.py plan                                  # $0: each draw's links, readers, link days and the controls' retired rows
  python3 paid_run.py pin <dry out>                         # $0: pinned-plan.json from the plan and the dry linked graphs (labels)
  python3 paid_run.py dry <out> <kind> <draw>               # $0: one sequence with a fake judge (markers) for the bought judgements
  python3 paid_run.py dry-refused-upstream <out> <draw>     # $0: v14's first attempt refused once on its third judgement, then answered
  python3 paid_run.py dry-double-refusal <out> <kind> <draw>  # $0: v9 refused twice on its second judgement (a terminal refusal)
  python3 paid_run.py send <out> <kind> <draw> <ledger> <approved ceiling>   # paid, after the council's review and Alex's ceiling

kind is `linked` (poc-v120; its link jobs answered only by probe draw <draw>'s answers, matched by request hash; links written) or
`control` (poc-v118; the readers' old judgement rows retired by reader and day from each reader's link day). Every other request must
be answered from the sequence's copy of old-2's archive, except the four answers old-2's own run refused (non-readers; given back once
each). A request reaches the paid transport only when it is a judgement request (schema `judgement`) of a reader, made inside the
day's judging (`round.judge_day`, its day bound for the round and cleared after) on a day at or after the reader's link day, under July's
latch (admission and the inner call under one lock; the first refusal closes the sequence). Any other miss stops the sequence.

One acceptance gate (`acceptance`) decides both the dry runs and the paid send: the window completed with no stop; the committed graph
equal to the pinned one, labels included (none in a control); the probe jobs consumed exactly the pinned set; every post-link reader
judgement answered by a fresh call made during its own day's judging, every pre-link one from the archive; the upstream snapshot check
run and clean (each dependency entry of each reader request rendered from that dependency's latest accepted conclusion recorded when the
prompt was built); the fixed trajectory (H2) by the pinned reader set. `send` exits non-zero when the gate fails.
"""
import json
import math
import shutil
import sqlite3
import sys
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / 'src'))
sys.path.insert(0, str(REPO / 'docs/research/2026-11-20-production-readiness/dependency-design'))
sys.path.insert(0, str(HERE))
from hivemind import config, live_lock, model, replay, universe       # noqa: E402
from hivemind.views import judging, store                              # noqa: E402
from hivemind.views import round as round_module                       # noqa: E402
import july_test                                                        # noqa: E402
import window_test                                                      # noqa: E402

OLD2 = july_test.OLD2
ITEMS = july_test.ITEMS
V118 = REPO / 'poc/config/poc-v118.json'
V120 = REPO / 'poc/config/poc-v120.json'
UNIVERSE = july_test.UNIVERSE
WINDOW = ('2026-07-01', '2026-09-20')
CALENDAR = ('2026-07-01', '2026-09-20')     # the calendar every sequence must complete, fixed apart from the replay's own window
DRAWS = ('1', '2', '3')
PINNED = HERE / 'pinned-plan.json'
CEILING_LIMIT = 15.0                       # the harness refuses a ceiling above this whatever is passed; Alex names the actual one
COMPARISON = 'Comparison point stated by that judgement: '
FORECAST = "The system's forecast for it (our own judgement, not evidence): "


def old2():
    return sqlite3.connect(f'file:{OLD2 / "views.sqlite"}?mode=ro', uri=True)


def day_of_seq(seq):
    return old2().execute('select publication_day from processing_steps where sequence_no=? limit 1', (seq,)).fetchone()[0]


def opened_at(seq):
    """The question old-2 opened at `seq` (the link step's candidate `c1` there)."""
    rows = old2().execute('select view_id from views where created_seq=? and view_id in (select view_id from view_keys)', (seq,)).fetchall()
    if len(rows) != 1:
        raise SystemExit(f'seq {seq}: {len(rows)} number questions opened, expected one')
    return rows[0][0]


def probe_links(draw):
    """Probe draw <draw>'s proposed links as [(reader, read, sign, seq)], candidate ids resolved to the question old-2 opened there."""
    conn = sqlite3.connect(f'file:{REPO / "poc/data/link-census-2026-11-21" / f"probe-v2-{draw}" / "views.sqlite"}?mode=ro', uri=True)
    out = []
    for seq, record_json in conn.execute("select seq, record_json from link_selections where status='proposed' order by id"):
        for p in json.loads(record_json).get('proposed', []):
            resolve = (lambda node, s=seq: opened_at(s) if not node.startswith('v') else node)
            out.append((resolve(p['reader']), resolve(p['read']), p['sign'], seq))
    return out


def readers(draw):
    """{reader: its link day}: the day of the article that writes its first link."""
    days = {}
    for reader, _, _, seq in probe_links(draw):
        day = day_of_seq(seq)
        days[reader] = min(days.get(reader, day), day)
    return days


def retired_rows(reader_days):
    """The old judge rows of each reader on its link day or later: old-2's accepted judgements by reader and day. Checked: every judge row
    of that reader in old-2's archive from the first of them on is in the set (no refused first attempt or other row left behind)."""
    conn, archive = old2(), sqlite3.connect(f'file:{OLD2 / "archive.sqlite"}?mode=ro', uri=True)
    rows = {}
    for reader, day in reader_days.items():
        accepted = [c for (c,) in conn.execute('select call_id from judgements where view_id=? and publication_day>=? order by call_id', (reader, day))]
        if not accepted:
            continue
        family = [c for c, r in archive.execute("select call_id, request_json from model_calls where purpose='judge' and call_id>=?", (accepted[0],))
                  if july_test.judged_view(json.loads(r)) == reader]
        if sorted(family) != sorted(accepted):
            raise SystemExit(f'{reader}: judge rows from call {accepted[0]} on are not exactly its accepted judgements from {day}: '
                             f'{sorted(set(family) ^ set(accepted))[:5]}')
        rows[reader] = accepted
    return rows


def plan():
    out = {}
    for draw in DRAWS:
        days = readers(draw)
        retired = retired_rows(days)
        out[draw] = {'links': probe_links(draw), 'readers': days, 'retired per reader': {r: len(c) for r, c in retired.items()}}
    print(json.dumps(out, indent=1))
    return out


def pin(dry_out):
    """pinned-plan.json: per draw the readers and link days, the probe's job hashes, and the committed graph of the dry linked run
    (labels included). The acceptance gate and H2 read this file, never the admission code's own tables."""
    pinned = {}
    for draw in DRAWS:
        summary = json.loads((Path(dry_out) / f'linked-{draw}' / 'summary.json').read_text())
        pinned[draw] = {'readers': readers(draw), 'graph': summary['links committed'], 'probe jobs': sorted(window_test.probe_answers(draw))}
    PINNED.write_text(json.dumps(pinned, indent=1))
    print(json.dumps({d: {'readers': p['readers'], 'graph': p['graph'], 'probe jobs': len(p['probe jobs'])} for d, p in pinned.items()}, indent=1))


def pinned_plan(draw):
    if not PINNED.exists():
        raise SystemExit('pinned-plan.json is missing: run `pin` on the reviewed dry runs first')
    return json.loads(PINNED.read_text())[draw]


def planned_days():
    """The days old-2's run completed over the window, in order: the calendar every sequence must complete."""
    return [r[0] for r in old2().execute('select day from days_completed where day between ? and ? order by seq', CALENDAR)]


def is_judgement_request(request):
    schema = (request.get('response_format') or {}).get('json_schema') or {}
    return schema.get('name') == 'judgement' and july_test.judged_view(request) is not None


class SequenceRun:
    """One sequence: its transport, its latch, the judging day, the upstream snapshots and the record of every judge attempt."""

    def __init__(self, kind, draw, inner, folder):
        self.kind, self.draw, self.inner, self.folder = kind, draw, inner, folder
        self.reader_days = readers(draw)
        self.probe = window_test.probe_answers(draw) if kind == 'linked' else {}
        self.stored_refusals = window_test.refused_rows()
        self.latch = july_test.Latch()
        self.day = None
        self.attempts, self.refusals_given, self.link_jobs = [], [], []
        self.snapshots, self.snapshot_problems, self.snapshot_checks = [], [], 0
        self.day_windows, self.terminal = {}, None
        self.lock = threading.Lock()

    def transport(self, *args):
        request = args[-1]
        if len(args) == 1:
            if july_test.is_link_request(request) and self.kind == 'linked':
                sha = model.request_identity(request)[1]
                if sha not in self.probe:
                    raise july_test.Stop(f'a link job outside probe draw {self.draw} ({sha[:12]}): not sent')
                self.link_jobs.append(sha)
                return self.probe[sha]
            raise july_test.Stop('a Jev request missed the archive: not sent')
        sha = model.request_identity(request)[1]
        view_id = july_test.judged_view(request) if is_judgement_request(request) else None
        if view_id is not None and view_id not in self.reader_days:
            response = self.stored_refusals.pop(sha, None)
            if response is not None:
                self.refusals_given.append(sha[:12])
                return response
        day = self.day
        allowed = view_id in self.reader_days and day is not None and day >= self.reader_days[view_id]
        text = request['messages'][-1]['content']
        with self.lock:
            self.attempts.append({'view': view_id, 'day': day, 'sha': sha, 'retry': 'Correct it and answer again' in text, 'admitted': allowed})
        if allowed:
            self.check_snapshot(view_id, day, text)
        return self.latch.run(allowed, f'unapproved request on {day} (thesis {view_id}): not sent', (view_id, day),
                              lambda: self.inner(*args))

    def build_prompt(self, original):
        def wrapped(conn, view_id, prompt_version):
            system, user = original(conn, view_id, prompt_version)
            reads = {}
            for dependency in store.dependencies_of(conn, view_id):
                target = dependency['resolved_to']
                state = store.current_state(conn, target) if target else None
                reads[target] = None if not state else {k: state.get(k) for k in ('judgement_id', 'publication_day', 'rung', 'reasons',
                                                                                   'reference', 'implied_outcome')}
            with self.lock:
                self.snapshots.append({'view': view_id, 'user': user, 'reads': reads, 'day': self.day})
            return system, user
        return wrapped

    def check_snapshot(self, view_id, day, text):
        """Each dependency entry of the request, found by its own target id, is rendered from that dependency's conclusion recorded when
        the prompt was built: its judgement day in the header, its comparison point, forecast and reasons excerpt line for line (a retry
        carries the same prompt with the correction lines after it)."""
        with self.lock:
            built = [s for s in self.snapshots if s['view'] == view_id and text.startswith(s['user'])]
        if not built:
            if self.kind == 'linked':
                self.snapshot_problems.append((view_id, day, 'no prompt recorded for this request'))
            return
        reads = built[-1]['reads']
        if self.kind == 'linked' and not reads:
            self.snapshot_problems.append((view_id, day, 'a linked reader request with no dependency recorded'))
        lines = text.split('\n')
        checked = False
        for target, state in reads.items():
            if state is None:
                continue
            headers = [i for i, line in enumerate(lines) if line.startswith(f'- {target} (')]
            if len(headers) != 1:
                self.snapshot_problems.append((view_id, day, f'{target}: {len(headers)} dependency entries'))
                continue
            i = headers[0]
            expected = [f'    {COMPARISON}{judging._indented(state.get("reference") or "not stated")}',
                        f'    {FORECAST}{judging._indented(state.get("implied_outcome") or "not stated")}',
                        f'    Reasons (excerpt): {judging._indented((state.get("reasons") or "")[:600])}']
            block = '\n'.join(lines[i + 1:])
            if not lines[i].endswith(f', judged {state["publication_day"]}') or not block.startswith('\n'.join(expected)):
                self.snapshot_problems.append((view_id, day, f'{target}: entry is not its latest conclusion at prompt time '
                                                              f'(judgement {state["judgement_id"]})'))
            checked = True
        if checked:
            with self.lock:
                self.snapshot_checks += 1

    def judge_day(self, original):
        def wrapped(conn, archive_, cfg_, day, seq, **keywords):
            before = archive_.conn.execute('select coalesce(max(call_id), 0) from model_calls').fetchone()[0]
            self.day = day
            try:
                result = original(conn, archive_, cfg_, day, seq, **keywords)
            finally:
                self.day = None
                after = archive_.conn.execute('select coalesce(max(call_id), 0) from model_calls').fetchone()[0]
                self.day_windows[day] = (before, after)
            failed = getattr(result, 'failed', None)
            if failed and self.terminal is None:
                text = str(failed)
                view = text.split('judgement refused twice: ', 1)[1].split(':', 1)[0] if 'judgement refused twice: ' in text else None
                self.terminal = ({'outcome': 'double refusal', 'view': view, 'day': day, 'reader': view in self.reader_days}
                                 if view else {'outcome': 'infrastructure stop', 'day': day, 'reason': text[:300]})
            return result
        return wrapped


def prepare(folder, kind, draw):
    if folder.exists():
        raise SystemExit(f'{folder} exists: a sequence starts from an empty folder and is never resumed')
    folder.mkdir(parents=True)
    shutil.copyfile(OLD2 / 'archive.sqlite', folder / 'archive.sqlite')
    archive = model.Archive(str(folder / 'archive.sqlite'))
    top = archive.conn.execute('select coalesce(max(call_id), 0) from model_calls').fetchone()[0]
    retired = []
    if kind == 'control':
        for reader, calls in retired_rows(readers(draw)).items():
            for call_id in calls:
                archive.retire(call_id)
                retired.append((reader, call_id))
    views = folder / 'views.sqlite'
    marker = sqlite3.connect(views)
    marker.execute('create table harness_only (name text, day text)')
    marker.execute("insert into harness_only values ('paid_run.py', '2026-11-21')")
    marker.commit()
    marker.close()
    return archive, top, retired


def trajectory_check(views, reader_set):
    """H2: every non-reader judgement equal to old-2's by question and day (the request and every substantive field); every other table
    equal, typed keys included."""
    built, stored = sqlite3.connect(f'file:{views}?mode=ro', uri=True), old2()
    fields = ('view_id, publication_day, rung, reasons, reference, implied_outcome, cited_evidence_json, cited_views_json, pushes_json, '
              'theme_pushes_json, changed, why_changed, request_sha256')

    def rows(conn):
        return sorted(tuple(r) for r in conn.execute(f'select {fields} from judgements') if r[0] not in reader_set)
    tables = {'non-reader judgements': rows(built) == rows(stored)}
    for name, sql in {'views': 'select view_id, question, created_seq from views',
                      'view_keys': 'select view_id, measure, scope, period_start, period_end, unit from view_keys',
                      'evidence': 'select evidence_id, quote, created_seq from evidence',
                      'evidence_links': 'select evidence_id, view_id, seq from evidence_links',
                      'rungs': 'select view_id, position, label, condition, lo, hi from rungs',
                      'view_switches': 'select view_id, open, reason, after_seq from view_switches',
                      'successions': 'select view_id, succeeds, seq from successions'}.items():
        tables[name] = sorted(tuple(r) for r in built.execute(sql)) == sorted(tuple(r) for r in stored.execute(sql))
    return {f'{k} equal': v for k, v in tables.items()}


def run_sequence(out, kind, draw, inner, ledger_state, transport_kind):
    if kind not in ('linked', 'control') or draw not in DRAWS:
        raise SystemExit('kind must be linked or control, draw 1, 2 or 3')
    pinned = pinned_plan(draw)
    folder = out / f'{kind}-{draw}'
    archive, top, retired = prepare(folder, kind, draw)
    run = SequenceRun(kind, draw, inner, folder)
    cfg = config.load(str(V120 if kind == 'linked' else V118))
    summary = {'kind': kind, 'draw': draw, 'transport': transport_kind, 'config': cfg.version, 'archive_top': top,
               'reader days': run.reader_days, 'retired rows': len(retired), 'stopped': ''}
    original_judge_day, original_build = round_module.judge_day, judging.build_prompt
    round_module.judge_day, judging.build_prompt = run.judge_day(original_judge_day), run.build_prompt(original_build)
    held = live_lock.acquire(str(folder / 'views.sqlite'))
    try:
        replay.run(testdb_path=str(ITEMS), views_path=str(folder / 'views.sqlite'), archive=archive, cfg=cfg, universe=universe.load(str(UNIVERSE)),
                   from_day=WINDOW[0], until_day=WINDOW[1], transport=run.transport, log=lambda *a: None, only_objects={'NVDA'})
    except Exception as error:
        summary['stopped'] = f'{type(error).__name__}: {error}'[:500]
        if run.terminal is None:
            run.terminal = {'outcome': 'infrastructure stop', 'reason': summary['stopped']}
    finally:
        live_lock.release(held)
        round_module.judge_day, judging.build_prompt = original_judge_day, original_build
    conn = sqlite3.connect(f'file:{folder / "views.sqlite"}?mode=ro', uri=True)
    reader_judgements = [dict(zip(('view', 'day', 'call_id', 'judgement_id'), r)) for r in conn.execute(
        'select view_id, publication_day, call_id, judgement_id from judgements where view_id in (%s) order by judgement_id'
        % ','.join('?' * len(pinned['readers'])), tuple(pinned['readers']))]
    for j in reader_judgements:
        window = run.day_windows.get(j['day'], (None, None))
        j['must be fresh'] = j['day'] >= pinned['readers'][j['view']]
        j['fresh on its day'] = window[0] is not None and window[0] < j['call_id'] <= window[1]
        j['from the archive'] = j['call_id'] <= top
    archive_conn = sqlite3.connect(f'file:{folder / "archive.sqlite"}?mode=ro', uri=True)
    attempt_rows = []
    for call_id, request_json, sha in archive_conn.execute("select call_id, request_json, request_sha256 from model_calls where purpose='judge' and call_id > ?", (top,)):
        view = july_test.judged_view(json.loads(request_json))
        day = next((d for d, (b, a) in run.day_windows.items() if b < call_id <= a), None)
        attempt_rows.append({'call_id': call_id, 'view': view, 'day': day, 'refused': ':refused:' in sha, 'reader': view in pinned['readers']})
    committed = sorted(list(r) for r in conn.execute("select view_id, depends_on, direction, seq from dependencies where kind='reads'"))
    days_completed = [r[0] for r in conn.execute('select day from days_completed order by seq')]
    with open(folder / 'snapshots.jsonl', 'w') as handle:
        for snapshot in run.snapshots:
            handle.write(json.dumps({'view': snapshot['view'], 'day': snapshot['day'], 'reads': snapshot['reads']}) + '\n')
    summary.update({
        'terminal': run.terminal or {'outcome': 'complete'},
        'days completed': days_completed,
        'links committed': committed,
        'link jobs consumed': sorted(run.link_jobs),
        'judge attempts at the transport': run.attempts,
        'archive judge rows written (dated)': attempt_rows,
        'stored refusals given back': run.refusals_given,
        'reader judgements': reader_judgements,
        'snapshot problems': run.snapshot_problems, 'snapshot checks': run.snapshot_checks,
        'trajectory (H2)': trajectory_check(folder / 'views.sqlite', set(pinned['readers'])),
        'latch': run.latch.reason, 'ledger': ledger_state(),
    })
    summary['acceptance'] = acceptance(summary, pinned, kind)
    (folder / 'summary.json').write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    return summary


def acceptance(summary, pinned, kind):
    """The one gate for the dry runs and the paid send."""
    judgements = summary['reader judgements']
    checks = {
        'window completed, no stop': summary['stopped'] == '' and summary['terminal'] == {'outcome': 'complete'},
        'calendar completed (every day old-2 completed)': summary.get('days completed') == planned_days(),
        'committed graph equals the pinned one (labels included)': summary['links committed'] == (pinned['graph'] if kind == 'linked' else []),
        'probe jobs consumed exactly the pinned set': summary['link jobs consumed'] == (pinned['probe jobs'] if kind == 'linked' else []),
        'every post-link reader judgement fresh on its own day': all(j['fresh on its day'] for j in judgements if j['must be fresh']),
        'every pre-link reader judgement from the archive': all(j['from the archive'] for j in judgements if not j['must be fresh']),
        'reader judgements present': bool(judgements),
        'upstream snapshot clean': not summary['snapshot problems'],
        'upstream snapshot exercised (linked)': kind == 'control' or summary['snapshot checks'] > 0,
        'fixed trajectory (H2)': all(summary['trajectory (H2)'].values()),
        'ledger clean (not stopped, no overrun)': not (summary.get('ledger') or {}).get('stopped') and not (summary.get('ledger') or {}).get('overrun'),
    }
    return dict(checks, accepted=all(checks.values()))


def refusing_judge(label, refuse, twice=False):
    """July's marker judge, except that the first attempt of each (view, n) in `refuse` cites an evidence id it was not shown, so the
    code refuses it; with `twice` the retry is refused the same way (a terminal refusal), else answered normally."""
    plain, attempts = july_test.fake_judge(label, {}), {}

    def answer(provider, request):
        text = request['messages'][-1]['content']
        view_id = july_test.judged_view(request)
        retry = 'Correct it and answer again' in text
        if not retry:
            attempts[view_id] = attempts.get(view_id, 0) + 1
        if (view_id, attempts.get(view_id)) in refuse and (twice or not retry):
            data = {'rung': 3, 'reference': f'REFUSED|{label}|{view_id}', 'implied_outcome': f'REFUSED|{label}|{view_id}', 'reasons': 'x',
                    'cites': ['e999999'], 'cites_views': [], 'pushes': [], 'changed': True, 'why_changed': '', 'theme_pushes': []}
            return {'choices': [{'message': {'content': json.dumps(data)}}], 'usage': {'prompt_tokens': 100, 'completion_tokens': 10}}
        return plain(provider, request)
    return answer


def dry(out, kind, draw, refuse=(), twice=False):
    """$0: the sequence with a fake judge answering every bought judgement with markers unique to the sequence, the question and the
    attempt (every one says changed, so propagation is at its largest), through the same acceptance gate as the send."""
    judge = refusing_judge(f'{kind}-{draw}', set(refuse), twice) if refuse else july_test.fake_judge(f'{kind}-{draw}', {})
    summary = run_sequence(out, kind, draw, july_test.dispatcher(judge, july_test.fake_jev(set()), []), lambda: {}, 'dry')
    print(json.dumps({'sequence': f'{kind}-{draw}', 'terminal': summary['terminal'], 'stopped': summary['stopped'][:200],
                      'bought (admitted attempts)': sum(1 for a in summary['judge attempts at the transport'] if a['admitted']),
                      'snapshot checks': summary['snapshot checks'], **summary['acceptance']}, indent=1))
    return summary


def send(out, kind, draw, ledger_path, approved):
    budget = july_test.budget_module()
    if not (isinstance(approved, float) and math.isfinite(approved) and 0 < approved <= CEILING_LIMIT):
        raise SystemExit('the approved ceiling must be a finite amount above 0 (and within the harness limit)')
    ledger = budget.SharedLedger(str(ledger_path))
    ceiling = ledger.read()['ceiling']
    if not (isinstance(ceiling, (int, float)) and math.isfinite(ceiling) and ceiling == approved):
        raise SystemExit(f'the ledger ceiling {ceiling!r} is not the approved ${approved}: refused')
    label = f'{kind}-{draw}'
    lock_handle = open(Path(ledger_path).with_name(f'{label}.launcher.lock'), 'a+')
    if not ledger.claim_launcher(label, lock_handle):
        raise SystemExit(f'another launch of {label} is running')
    budget.install_stop_gate(ledger)
    try:
        summary = run_sequence(out, kind, draw, budget.BudgetTransport(ledger), ledger.read, 'paid')
    finally:
        ledger.remove_launcher(label)
    print(json.dumps({'sequence': label, 'terminal': summary['terminal'], 'stopped': summary['stopped'][:300],
                      'ledger': summary['ledger'], **summary['acceptance']}, indent=1))
    return summary['acceptance']['accepted']


if __name__ == '__main__':
    command = sys.argv[1]
    if command == 'plan':
        plan()
    elif command == 'pin':
        pin(sys.argv[2])
    elif command == 'dry':
        sys.exit(0 if dry(Path(sys.argv[2]), sys.argv[3], sys.argv[4])['acceptance']['accepted'] else 1)
    elif command == 'dry-refused-upstream':
        sys.exit(0 if dry(Path(sys.argv[2]), 'linked', sys.argv[3], refuse={('v14', 3)})['acceptance']['accepted'] else 1)
    elif command == 'dry-double-refusal':
        summary = dry(Path(sys.argv[2]), sys.argv[3], sys.argv[4], refuse={('v9', 2)}, twice=True)
        expected = {'outcome': 'double refusal', 'view': 'v9', 'reader': True}
        sys.exit(0 if all(summary['terminal'].get(k) == v for k, v in expected.items()) and not summary['acceptance']['accepted'] else 1)
    elif command == 'send':
        sys.exit(0 if send(Path(sys.argv[2]), sys.argv[3], sys.argv[4], Path(sys.argv[5]), float(sys.argv[6])) else 1)
    else:
        raise SystemExit(f'unknown command {command}')
