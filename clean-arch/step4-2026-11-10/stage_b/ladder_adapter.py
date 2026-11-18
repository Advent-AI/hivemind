"""Stage B: production's frozen judge over the ladder step's own questions (DESIGN.md §5.4, §6, §7.1, §8; D426, D428, D429).

One unseeded draw is replayed in production's dispatch order, as the Stage 2 adapter replays it (`e2e-2026-11-09/adapter.py`),
with three differences, the adapter's "new mode":
- **No seed and no ruler view.** The views are only those the ladder step wrote.
- **Each thesis Step 1 opened gets its ladder at its opening article**, before that article's records are written: the ladder
  step's answer from the fourth Stage A's first send, fixed before any Stage B result exists (`LADDERS`). A written ladder becomes
  view `v<N>` for thesis `clean-<N>` (its stored view, as `ladder_step.write_view` built it) and a row of `clean_ladders`; a thesis
  with no ladder gets the row alone. No ladder call is made here.
- **Links follow the ladder.** A link to a laddered thesis is written to its view; a link to a thesis with no ladder is counted
  "links to an unjudged thesis" and not written.

Everything a replay day writes before its round is one commit, as the Stage 2 adapter commits (the store's writers do not commit).
The frozen judge then judges the day's changed views, with the Stage 2 adapter's leakage and selection checks. A due-day guard runs at
the start of every replay day and once after the last: an open view due on or before the day stops the replay. Every judge attempt's
reserve and charge are written to `spend.jsonl` as they happen, so the spend survives a crash. The run folder is created once; a
stopped replay is not resumed. One spending limit can be shared by several replays (`run_stage_b.py` runs the three draws and
any redo in one process under one limit); a limit starts from what its ledger already records, so a later process cannot spend
past a cap that earlier ones used up.
"""
import collections
import datetime
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT / 'clean-arch' / 'e2e-2026-11-09'), str(ROOT / 'src')]
import adapter  # noqa: E402
import budget  # noqa: E402
from hivemind import config, live_lock, model, pull  # noqa: E402
from hivemind.views import store  # noqa: E402

UNSEEDED = ROOT / 'poc/data/clean-unseeded-2026-11-10'
DRAWS = {'u1': (str(UNSEEDED / 'draw-d1/trace.sqlite'), UNSEEDED / 'draw-d1/step2'),
         'u2': (str(UNSEEDED / 'draw-d2/trace.sqlite'), UNSEEDED / 'draw-d2/step2'),
         'u3': (f"{UNSEEDED / 'draw-d3/trace.sqlite'}+{UNSEEDED / 'draw-d3-segment-2/trace.sqlite'}", UNSEEDED / 'draw-d3-segment-2/step2')}
LADDERS = ROOT / 'poc/data/clean-ladder-stage-a-2026-11-10/run-4/send-1/outcomes.jsonl'
LADDER_ARCHIVE = LADDERS.parent / 'archive.sqlite'          # its model_calls carry the ladder configuration's checksum
CASES = STEP / 'stage_a' / 'cases.json'
OUTPUT_ROOT = ROOT / 'poc/data/clean-stage-b-2026-11-11'
STATUS = {'ladder': 'ladder', 'no ladder': 'no ladder', 'refused twice': 'no ladder: refused'}
LADDER_COLUMNS = ('thesis_id', 'period', 'view_id', 'status', 'reason', 'reference_status', 'checked_answer', 'outcome_record',
                  'config_checksum', 'article_seq', 'article_day')
CANONICAL_TOPIC = re.compile(r'clean-[1-9][0-9]*')        # Step 1's counter (step1/runner.py); every stored topic id has this form
YEAR = re.compile(r'(?:FY)?([0-9]{4})')
SPLIT_STATUS = {'ladder': 'ladder', 'no ladder': 'no ladder', 'no ladder: refused': 'no ladder: refused', 'refused twice': 'no ladder: refused'}



class LedgerBudget(budget.Budget):
    """The Stage 2 adapter's spending limit, with each attempt's reserve and its charge written to a ledger file inside the same
    locked step that takes or releases it: one whole JSON object a line, flushed and synced.

    **One stop rule.** The first stop of any kind ends every later send: the limit's own refusal at the cap, or a stop the caller
    records (`stop`). The stop is written to the ledger under the lock before it is raised, so no other thread sends after it and
    a limit built later on the same ledger starts stopped."""

    def __init__(self, cap_usd, ledger_path, attempt=None, sleep=None, shared=None):
        super().__init__(cap_usd, attempt=attempt, **({'sleep': sleep} if sleep else {}))
        self.ledger_path = Path(ledger_path)
        self.shared = shared            # a run's shared ledger (WIRING-DESIGN.md §B2, D448): reserved and settled inside each attempt
        self.spent_usd = ledger_total(self.ledger_path)          # what earlier processes spent under this ledger counts against the cap
        self.attempts = max(attempt_ids(self.ledger_path), default=0)
        self.stopped = ledger_stop(self.ledger_path)             # None, or the reason an earlier send stopped

    def stop(self, reason):
        """Record a stop: written to the ledger once, under the lock; every later send refuses."""
        with self.lock:
            self._stop(reason)

    def _stop(self, reason):
        if self.stopped is None:
            self.stopped = reason
            self._write({'stop': reason})
            if self.shared is not None:
                self.shared.stop(f'the judge: {reason}')     # every recorded judge stop is final (run_stage_b's redo never calls it)

    def _write(self, line):
        with self.ledger_path.open('a') as handle:
            handle.write(json.dumps(line) + '\n')
            handle.flush()
            os.fsync(handle.fileno())

    def send(self, provider, request):
        reserve = budget.worst_cost(request)
        for attempt_number in range(budget.ATTEMPTS):
            with self.lock:
                if self.stopped is not None:
                    raise budget.OverBudget(f'the send is stopped ({self.stopped}); nothing more is sent')
                if self.spent_usd + self.reserved_usd + reserve > self.cap_usd:
                    reason = (f'the spending cap: spent ${self.spent_usd:.4f}, ${self.reserved_usd:.4f} in flight; '
                              f'${reserve:.4f} more would pass the ${self.cap_usd:.2f} cap')
                    self._stop(reason)
                    raise budget.OverBudget(reason)
                shared_reserve = self.shared.estimate(request) if self.shared is not None else None
                if self.shared is not None and not self.shared.reserve(shared_reserve):
                    self._stop('the shared ledger refused the reservation')
                    raise budget.OverBudget('the shared ledger refused the reservation')
                self.reserved_usd += reserve
                self.attempts += 1
                attempt_id = self.attempts
                self._write({'attempt': attempt_id, 'reserve': reserve})
            response, failure = None, None
            try:
                response = self.attempt(provider, request)
            except model.TransportError as error:
                failure = error
            finally:
                with self.lock:
                    self.reserved_usd -= reserve
                    charged = budget.cost(request, response) if response is not None else None
                    self.spent_usd += reserve if charged is None else charged
                    self._write({'attempt': attempt_id, 'charge': reserve if charged is None else charged, 'known': charged is not None})
                    if self.shared is not None:
                        self.shared.settle(shared_reserve, charged)       # the ledger settles a missing or zero charge at its reservation
            if response is not None:
                return response
            retried = getattr(failure, 'http_status', None) not in budget.NOT_RETRIED and str(failure) not in budget.UNDECODABLE
            if not retried or attempt_number + 1 == budget.ATTEMPTS:
                raise failure
            self.sleep(5 * (attempt_number + 1))


def ledger_lines(ledger_path):
    return [json.loads(line) for line in Path(ledger_path).read_text().splitlines()] if Path(ledger_path).exists() else []


def attempt_ids(ledger_path):
    return [line['attempt'] for line in ledger_lines(ledger_path) if 'attempt' in line]


def ledger_stop(ledger_path):
    """The first stop the ledger records, or None."""
    return next((line['stop'] for line in ledger_lines(ledger_path) if 'stop' in line), None)


def ledger_total(ledger_path):
    """What the ledger says was spent: a charge where there is one, the reserve where an attempt has none."""
    reserves, charges = {}, {}
    for entry in ledger_lines(ledger_path):
        if 'reserve' in entry:
            reserves[entry['attempt']] = entry['reserve']
        elif 'charge' in entry:
            charges[entry['attempt']] = entry['charge']
    return sum(charges.values()) + sum(reserve for attempt, reserve in reserves.items() if attempt not in charges)


def article_inputs(trace_path):
    """Per article, by manifest position (as `adapter.trace_articles` numbers them): its input id, from the first segment's manifest."""
    first = str(trace_path).split('+')[0]
    conn = sqlite3.connect(f'file:{first}?mode=ro', uri=True)
    try:
        return {n: iid for n, iid in enumerate(json.loads(conn.execute('select manifest from run').fetchone()[0])['item_ids'], 1)}
    finally:
        conn.close()


STORE_SIZE_LIMIT = 64 * 1024 * 1024        # the -wal's size after a reset (live-service/OPERATING-CONTRACT.md, row 5)
FREE_SPACE_FACTOR = 20                     # free space needed before a day, as a multiple of the store's size (main file and -wal)
CHECKPOINT_FAILURES_TO_STOP = 3            # consecutive completed days whose truncating checkpoint failed


class WriterStopped(Exception):
    """The writer stopped before a day, its store holding every completed day (OPERATING-CONTRACT.md, "The writer's start, stops and
    end"); a stop no resend can change."""

    def __init__(self, reason, last_completed_day):
        self.reason, self.last_completed_day = reason, last_completed_day
        super().__init__(reason)


def open_wal_store(path):
    """The new store, created empty and exclusively, locked (live_lock: refused if another process holds it), put in WAL mode
    (checked) before `store.open_db` writes its schema, with the -wal size limit on the writer's own connection; its identity checked
    after the open. Returns (connection, held lock). Anything failing after the lock is taken closes what was opened and releases the
    lock before raising, so the caller only ever owns a fully opened store."""
    path = Path(path)
    descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    created = os.fstat(descriptor)
    os.close(descriptor)
    held = live_lock.acquire(path)
    conn = None
    try:
        if held.identity != (created.st_dev, created.st_ino):
            raise live_lock.PathChanged(f'{path} was replaced between its creation and its lock')
        first = sqlite3.connect(str(path))
        try:
            mode = first.execute('pragma journal_mode=wal').fetchone()[0]
        finally:
            first.close()
        if mode != 'wal':
            raise SystemExit(f'{path}: the journal mode is {mode!r}, not wal: refused')
        conn = store.open_db(str(path))
        conn.execute(f'pragma journal_size_limit={STORE_SIZE_LIMIT}')
        live_lock.verify(held)
        return conn, held
    except BaseException:
        if conn is not None:
            conn.close()
        live_lock.release(held)
        raise


def store_bytes(path):
    path = Path(path)
    return sum(p.stat().st_size for p in (path, path.with_name(path.name + '-wal')) if p.exists())


def free_bytes(folder):
    return shutil.disk_usage(folder).free


def held_by_another(error):
    """SQLite's own messages for SQLITE_BUSY and SQLITE_LOCKED: another connection held the store; any other error is not that."""
    return str(error).startswith(('database is locked', 'database table is locked', 'database schema is locked'))


def truncate_checkpoint(conn):
    """A truncating checkpoint with a short wait: 'done', 'busy' when another connection held it back (SQLite shows contention,
    not who), or else the error's own text."""
    try:
        conn.execute('pragma busy_timeout=1000')
        busy = conn.execute('pragma wal_checkpoint(TRUNCATE)').fetchone()[0]
    except sqlite3.OperationalError as error:
        return 'busy' if held_by_another(error) else str(error)
    return 'busy' if busy else 'done'


def leave_wal(conn):
    """The change to rollback-journal mode at the writer's end: (the mode it ends in, why WAL was kept or None). A reader holding
    the store and any other failure are reported apart."""
    try:
        conn.execute('pragma busy_timeout=1000')
        mode = conn.execute('pragma journal_mode=delete').fetchone()[0]
    except sqlite3.OperationalError as error:
        return 'wal', ('another connection held the store at the end' if held_by_another(error) else f'leaving WAL failed: {error}')
    return mode, (None if mode == 'delete' else f'the mode stayed {mode}')


class LadderAdapter(adapter.Adapter):
    """The Stage 2 adapter in its ladder mode: no seed, no ruler view; views come only from the ladder step's answers."""

    def __init__(self, views_path, archive_path, ledger_path, *, transport=None, cap_usd=0.66, sleep=None, limit=None, shared=None):
        self.conn, self.lock = open_wal_store(views_path)
        try:
            columns = ', '.join(f"{column} not null default ''" if column == 'period' else column for column in LADDER_COLUMNS)
            self.conn.execute(f'create table if not exists clean_ladders ({columns}, primary key (thesis_id, period))')
            self.conn.commit()
            self._finish_init(archive_path, ledger_path, transport, cap_usd, sleep, limit, shared)
        except BaseException:
            self.close()
            raise

    def close(self):
        """The writer's end on every path: the store taken out of WAL mode when no reader holds it (so no WAL-mode store is left
        without its side files, which a read-only reader could not open), its connection closed, then its lock released (no
        writable connection outlives it). Returns the store's journal mode at the end."""
        mode = None
        try:
            if self.conn is not None:
                try:
                    mode, _ = leave_wal(self.conn)
                finally:
                    self.conn.close()
                    self.conn = None
        finally:
            if self.conn is None and self.lock is not None:      # a connection that failed to close keeps the lock (until the process ends)
                live_lock.release(self.lock)
                self.lock = None
        return mode

    def _finish_init(self, archive_path, ledger_path, transport, cap_usd, sleep, limit, shared):
        self.archive = model.Archive(archive_path)
        self.cfg = config.load(adapter.CONFIG)
        self.transport = transport
        self.budget = limit if limit is not None else LedgerBudget(cap_usd, ledger_path, attempt=transport, sleep=sleep, shared=shared)
        self.q23 = None
        self.views = set()
        self.mapping = {}
        self.unjudged = set()            # theses with a ladder row and no view
        self.evidence_of = {}
        self.counts = collections.Counter()
        self.next_number = 1
        self.sent = []

    def open_thesis(self, thesis_id, outcome, k, seq, day, input_id, source):
        """Write the thesis's ladder row and, for a written ladder, its view; not committed here. `k` is the trace's article number
        (kept in the row as the source article), `seq` the store's sequence the loop gave the article (CLOSING-DESIGN.md §1)."""
        if not CANONICAL_TOPIC.fullmatch(thesis_id):
            raise SystemExit(f'{thesis_id}: a topic id is clean- and a number without a leading zero (as Step 1 numbers them), so no '
                             'ordinary view id can begin with 0 as a yearly one does')
        number = thesis_id.split('-', 1)[1]
        if outcome['status'] == 'split':                 # the period split (splitting/DESIGN.md v4)
            return self.open_split(thesis_id, outcome, k, seq, day, input_id, source)
        status = STATUS[outcome['status']]
        view_id = f'v{number}' if status == 'ladder' else None
        answer = outcome['answer']
        reference_status = None
        if status == 'ladder':
            ladder = answer['ladder']
            if ladder.get('figure') is not None:
                reference_status = outcome['view'].get('reference_status')
            checked = json.loads(json.dumps(answer))
            if checked['ladder'].get('reference') is not None and outcome['passage'] is not None:
                checked['ladder']['reference']['words'] = outcome['passage']
        elif status == 'no ladder':                 # §5.4: the answer as given, the reason and a null ladder
            checked = answer if answer is not None else {'ladder': None, 'no_ladder': outcome['reason']}
        else:
            checked = None
        store.insert(self.conn, 'clean_ladders', thesis_id=thesis_id, period='', view_id=view_id, status=status,
                     reason=outcome['reason'] if status == 'no ladder' else None, reference_status=reference_status,
                     checked_answer=None if checked is None else json.dumps(checked, ensure_ascii=False),
                     outcome_record=json.dumps(outcome['requests'], ensure_ascii=False), config_checksum=source, article_seq=k, article_day=day)
        if view_id is None:
            self.unjudged.add(thesis_id)
            self.counts[f'theses with {status}'] += 1
            return
        view = outcome['view']
        store.create_view(self.conn, view_id=view_id, object_id=view['object_id'], object_kind=view['object_kind'], kind=view['kind'],
                          looks_at=view['looks_at'], question=view['question'], due_day=view['due_day'], year=view['year'],
                          rungs=[{'label': rung['label'], 'condition': rung['condition'], 'lo': rung.get('lo'), 'hi': rung.get('hi')}
                                 for rung in view['rungs']],
                          seq=seq, input_id=input_id, created_at=f'{day}T00:00:00Z')
        self.views.add(view_id)
        self.mapping[thesis_id] = [view_id]
        self.counts['views written from a ladder'] += 1

    def open_split(self, thesis_id, outcome, k, seq, day, input_id, source):
        """A topic declined as one quantity over two open years and re-asked per year (splitting/DESIGN.md v4): the parent's row with
        status `split`; one row per year, whatever its outcome; one view per written year, its id v, 0, the parent's number and the
        four-digit year (digits only, as the frozen judge reads view ids; the leading 0 keeps it apart from every ordinary id); every
        statement linked to the parent reaches every written year's view.
        A written year whose sibling has no view lists that year as not judged, with the model's own reason or code's words."""
        if str(STEP / 'ladder') not in sys.path:
            sys.path.append(str(STEP / 'ladder'))       # last: none of its modules shares a name with the writer's own folders
        import ladder_split
        periods = outcome['periods']
        if (not isinstance(periods, list) or len(periods) != 2 or len(set(periods)) != 2
                or not all(isinstance(p, str) and YEAR.fullmatch(p) for p in periods) or len({p.startswith('FY') for p in periods}) != 1):
            raise SystemExit(f'{thesis_id}: a split names two different years written alike (2026, or FY2027), not {periods!r}')
        number = thesis_id.split('-', 1)[1]
        store.insert(self.conn, 'clean_ladders', thesis_id=thesis_id, period='', view_id=None, status='split', reason=None,
                     reference_status=None, checked_answer=json.dumps({'ladder': None, 'no_ladder': outcome['reason']}, ensure_ascii=False),
                     outcome_record=json.dumps(outcome['requests'], ensure_ascii=False), config_checksum=source, article_seq=k, article_day=day)
        written = {}
        for year in outcome['periods']:
            child = outcome['children'][year]
            if child['status'] == 'ladder':
                written[year] = f'v0{number}{YEAR.fullmatch(year).group(1)}'   # digits only (the judge reads v\d+); the leading 0 no ordinary id has
        for year in outcome['periods']:
            child = outcome['children'][year]
            status = SPLIT_STATUS[child['status']]
            view_id = written.get(year)
            checked = None
            if view_id is not None:
                checked = json.loads(json.dumps(child['answer']))
                if checked['ladder'].get('reference') is not None and child['passage'] is not None:
                    checked['ladder']['reference']['words'] = child['passage']
                for other in outcome['periods']:     # the model's own parts pass unchanged; code adds only a year with no question
                    if other != year and other not in written:
                        checked['ladder']['not_judged'] = list(checked['ladder'].get('not_judged') or []) + [
                            {'part': f'{other}: no question written', 'why': ladder_split.shown_reason(outcome['children'][other])}]
            elif child['status'] == 'no ladder':
                checked = {'ladder': None, 'no_ladder': child['reason']}
            store.insert(self.conn, 'clean_ladders', thesis_id=thesis_id, period=year, view_id=view_id, status=status,
                         reason=None if view_id else ladder_split.shown_reason(child),
                         reference_status=(child.get('view') or {}).get('reference_status') if view_id else None,
                         checked_answer=None if checked is None else json.dumps(checked, ensure_ascii=False),
                         outcome_record=json.dumps(child['requests'], ensure_ascii=False), config_checksum=source, article_seq=k, article_day=day)
            if view_id is None:
                continue
            view = child['view']
            store.create_view(self.conn, view_id=view_id, object_id=view['object_id'], object_kind=view['object_kind'], kind=view['kind'],
                              looks_at=view['looks_at'], question=view['question'], due_day=view['due_day'], year=view['year'],
                              rungs=[{'label': rung['label'], 'condition': rung['condition'], 'lo': rung.get('lo'), 'hi': rung.get('hi')}
                                     for rung in view['rungs']],
                              seq=seq, input_id=input_id, created_at=f'{day}T00:00:00Z')
            self.views.add(view_id)
            self.counts['views written from a yearly ladder'] += 1
        if written:
            self.mapping[thesis_id] = [written[y] for y in outcome['periods'] if y in written]
        else:
            self.unjudged.add(thesis_id)
            self.counts['split theses with no yearly view'] += 1

    def _link(self, evidence_id, thesis_id, k, changed):
        if evidence_id is not None and thesis_id in self.unjudged:
            self.counts['links to an unjudged thesis'] += 1
            return
        if evidence_id is not None and thesis_id in self.mapping:
            for view_id in self.mapping[thesis_id]:
                self.counts['links from a laddered thesis to its view'] += 1
                self._write_link(evidence_id, view_id, k, changed)
            return
        self._write_link(evidence_id, thesis_id, k, changed)

    def _write_link(self, evidence_id, view_id, k, changed):
        """A link to a closed question is written as production's writer writes one and not judged (production's round takes open
        questions only); each new one is counted, since it arises from Step 1's library not learning closings (CLOSING-DESIGN.md
        §2, §6). A link that already exists writes nothing and is not counted."""
        closed = evidence_id is not None and view_id in self.views and not store.is_open(self.conn, view_id)
        linked = lambda: self.conn.execute('select 1 from evidence_links where evidence_id=? and view_id=?', (evidence_id, view_id)).fetchone() is not None
        before = closed and linked()
        super()._link(evidence_id, view_id, k, changed)
        if closed and not before and linked():
            self.counts['links to a closed question written (not judged)'] += 1

    def overdue_invariant(self, day):
        """At a day's start no open question is due before that day: every earlier day closed its due questions (D54, D356). It holds
        by construction; a breach refuses the run (CLOSING-DESIGN.md §2)."""
        for view_id in sorted(self.views):
            due = store.view(self.conn, view_id)['due_day']
            if due and due < day and store.is_open(self.conn, view_id):
                raise SystemExit(f'{view_id} is open and was due {due}, before {day}: every earlier day closes its due questions; refused')

    def close_and_complete(self, day):
        """The day's end in production's order (replay.py): after the day's judging round, production's closing step freezes every
        question due by the day, then the day is completed at the last sequence it wrote, a closing's own included."""
        closed = pull.end_of_day(self.conn, day, store.next_sequence(self.conn) - 1)
        self.counts['questions closed at their due day'] += len(closed)
        store.complete_day(self.conn, day, store.next_sequence(self.conn) - 1, day)
        self.conn.commit()
        return closed


    def record_article(self, k, input_id, day):
        """The processing record the product's read side places items in time by (store.mark_step; `service.seq_day_map`): the
        article's sequence and day. Its time field is the day itself: no clock orders anything (AGENTS §3)."""
        store.mark_step(self.conn, input_id, k, 'handed_over', 'ok', None, day, day)


def ladders_for(run, opened, days_of, cases_path=None, ladders_path=None):
    """{thesis id: stored outcome} for the draw, after checking that the stored cases are exactly the theses the trace opened, each
    with the same description, and that each has exactly one outcome. The cases and ladder files default to Stage B's."""
    cases_path, ladders_path = Path(cases_path or CASES), Path(ladders_path or LADDERS)
    cases = {case['case']: case for case in json.loads(cases_path.read_text()) if case['case'].startswith(f'{run}/')}
    outcomes = collections.defaultdict(list)
    for line in ladders_path.read_text().splitlines():
        row = json.loads(line)
        if row['case'].startswith(f'{run}/'):
            outcomes[row['case']].append(row)
    opened_theses = {thesis_id: thesis for theses in opened.values() for thesis_id, thesis in theses.items()}
    opening_day = {thesis_id: days_of[k] for k, theses in opened.items() for thesis_id in theses}
    if {name.split('/', 1)[1] for name in cases} != set(opened_theses):
        raise SystemExit(f'the stored cases of {run} are not the theses its trace opened')
    for name, case in cases.items():
        thesis_id = name.split('/', 1)[1]
        in_trace = opened_theses[thesis_id]
        differing = [field for field in ('description', 'outcome', 'period') if field not in in_trace or case['thesis'].get(field) != in_trace[field]]
        if differing:
            raise SystemExit(f'{name}: the stored case and the trace describe different theses ({differing})')
        if case['item']['publication_date'] != opening_day[thesis_id]:
            raise SystemExit(f'{name}: the stored case\'s article is of {case["item"]["publication_date"]}, the trace opened it on {opening_day[thesis_id]}')
        if len(outcomes[name]) != 1 or outcomes[name][0]['pass'] != 1 or outcomes[name][0]['status'] not in (*STATUS, 'split'):
            raise SystemExit(f'{name}: not exactly one first-send outcome with a known status in {ladders_path.name}')
    return {name.split('/', 1)[1]: outcomes[name][0] for name in cases}


def ladder_configuration(archive_path=None):
    """The checksum of the ladder configuration that wrote the stored answers, as its model archive records it: exactly one."""
    import sqlite3
    conn = sqlite3.connect(f'file:{Path(archive_path or LADDER_ARCHIVE)}?mode=ro', uri=True)
    try:
        found = conn.execute('select distinct config_version, config_checksum from model_calls').fetchall()
    finally:
        conn.close()
    if len(found) != 1:
        raise SystemExit(f'the ladder archive names {len(found)} configurations, not one')
    return f'{found[0][0]} {found[0][1]}'


def calendar_days(first, last):
    day = datetime.date.fromisoformat(first)
    while day.isoformat() <= last:
        yield day.isoformat()
        day += datetime.timedelta(days=1)


def replay(run, output_folder, *, transport=None, cap_usd=0.66, sleep=None, limit=None, inputs=None, shared=None, end_day=None):
    """`inputs` (WIRING-DESIGN.md §A, D448) names a fresh draw's files: {'trace', 'step2', 'ladders', 'ladder_archive', 'cases',
    'output_root'}; any key left out takes Stage B's value for `run`. `shared` is the run's shared ledger. The loop walks every
    calendar day from the first article's day to `end_day` (the last article's day when left out) and closes due questions at each
    day's end as production does (D566, CLOSING-DESIGN.md)."""
    inputs = dict(inputs or {})
    output_root = Path(inputs.get('output_root', OUTPUT_ROOT))
    output = Path(output_folder).resolve()
    if transport is None and output_root.resolve() not in output.parents:
        raise SystemExit(f'a live replay writes only under {output_root}')
    output.mkdir(parents=True, exist_ok=False)
    trace_path, step2_folder = (inputs['trace'], Path(inputs['step2'])) if 'trace' in inputs else DRAWS[run]
    ladders_path = Path(inputs.get('ladders', LADDERS))
    by_article, library = adapter.load_draw(trace_path, step2_folder)
    days_of, opened, failed = adapter.trace_articles(trace_path)
    ladders = ladders_for(run, opened, days_of, inputs.get('cases'), ladders_path)
    source = ladder_configuration(inputs.get('ladder_archive'))
    revisions_by_record = collections.defaultdict(list)
    for group in library['groups'].values():
        for revision in group['revises']:
            revisions_by_record[revision['by']].append(revision['group'])
    later_by_article = collections.defaultdict(list)
    for entry in library['later_log']:
        later_by_article[entry['article']].append(entry)
    days = collections.OrderedDict()
    for k in sorted(days_of):
        days.setdefault(days_of[k], []).append(k)
    if list(days) != sorted(days):
        raise SystemExit('the Step 1 articles are not in day order')
    runner = LadderAdapter(output / 'views.sqlite', output / 'archive.sqlite', output / 'spend.jsonl', transport=transport, cap_usd=cap_usd, sleep=sleep,
                           limit=limit, shared=shared)
    try:
        spent_before = runner.budget.spent_usd
        runner.counts['articles not completed by Step 1'] = len(failed)
        runner.counts['ladder configuration'] = source
        runner.counts['ladder answers file sha256'] = hashlib.sha256(ladders_path.read_bytes()).hexdigest()
        inputs_of = article_inputs(trace_path)
        last_article_day = list(days)[-1]
        end_day = end_day or last_article_day
        if end_day < last_article_day:
            raise SystemExit(f'the end day {end_day} is before the last article day {last_article_day}: refused')
        sequences = {}                                   # the trace's article number k -> the store's sequence (CLOSING-DESIGN.md §1)
        views_path, failed_checkpoints, last_completed, checkpoint_error = output / 'views.sqlite', 0, None, None

        def stop(reason):
            """Record the stop and the store's last completed day beside the store, then stop before the day."""
            last = last_completed                    # the loop's own record: a stop never depends on reading the store
            mode, kept = leave_wal(runner.conn)
            runner.counts['store journal mode at the end'] = mode
            if kept:
                runner.counts['WAL kept'] = kept
            runner.counts['stopped'] = reason
            runner.counts['last completed day'] = last
            (output / 'adapter-counts.json').write_text(json.dumps(runner.counts, indent=1))
            raise WriterStopped(reason, last)

        for day in calendar_days(list(days)[0], end_day):
            try:
                live_lock.verify(runner.lock)                # the store and its lock file still the ones locked (OPERATING-CONTRACT row 7)
            except live_lock.PathChanged as changed:
                stop(f'{changed} before {day}')
            if checkpoint_error is not None:
                stop(f'the truncating checkpoint after {last_completed} failed: {checkpoint_error}')
            if failed_checkpoints >= CHECKPOINT_FAILURES_TO_STOP:
                stop(f'the truncating checkpoint failed after {failed_checkpoints} consecutive completed days (another connection held the store)')
            needed = FREE_SPACE_FACTOR * store_bytes(views_path)
            if free_bytes(output) < needed:
                stop(f'free space below {FREE_SPACE_FACTOR} times the store ({needed} bytes needed) before {day}')
            articles = days.get(day, [])
            runner.overdue_invariant(day)
            changed = set()
            for k in articles:
                seq = sequences[k] = max(k, store.next_sequence(runner.conn))
                input_id = by_article[k][0]['input_id'] if k in by_article else f'article:{k}'
                opened_here = sorted(opened.get(k, {}), key=lambda name: int(name.split('-', 1)[1]))
                for thesis_id in opened_here:
                    runner.open_thesis(thesis_id, ladders[thesis_id], k, seq, day, input_id, source)
                runner.article(seq, by_article.get(k, []), library, revisions_by_record, later_by_article.get(k, []), changed)
                runner.record_article(seq, inputs_of[k], day)       # after its records are written, as production marks a handover
                for thesis_id in opened_here:
                    for view_id in runner.mapping.get(thesis_id, []):
                        if runner.conn.execute('select count(*) from evidence_links where view_id=?', (view_id,)).fetchone()[0] == 0:
                            runner.counts['views with no opening evidence'] += 1
            runner.conn.commit()
            if changed:
                runner.judge(day, sequences[max(articles)], changed)
            runner.close_and_complete(day)
            last_completed = day
            checkpoint = truncate_checkpoint(runner.conn)
            if checkpoint == 'done':
                failed_checkpoints = 0
            elif checkpoint == 'busy':
                failed_checkpoints += 1
            else:
                checkpoint_error = checkpoint             # not a reader: the writer stops before the next day with this reason
        if checkpoint_error is not None:
            runner.counts['the truncating checkpoint after the last day failed'] = checkpoint_error
        mode, kept = leave_wal(runner.conn)
        runner.counts['store journal mode at the end'] = mode
        if kept:
            runner.counts['stopped in order'] = f'WAL kept: {kept}'
        (output / 'sequences.json').write_text(json.dumps({str(k): seq for k, seq in sequences.items()}, indent=1) + '\n')
        runner.counts['judging usd this draw (charged: from tokens, or the reserve when no usage came back)'] = round(runner.budget.spent_usd - spent_before, 4)
        runner.counts['judging usd of the whole limit so far (from its ledger)'] = round(ledger_total(runner.budget.ledger_path), 4)
        (output / 'adapter-counts.json').write_text(json.dumps(runner.counts, indent=1))
        (output / 'judge-requests.json').write_text(json.dumps(runner.sent, indent=1))
    finally:
        runner.close()                                   # every exit: the connection closed, then the lock released
    return runner


if __name__ == '__main__':
    raise SystemExit('Stage B is sent through run_stage_b.py, which runs the three draws under one spending limit')
