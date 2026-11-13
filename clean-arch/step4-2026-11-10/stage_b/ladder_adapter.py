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
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT / 'clean-arch' / 'e2e-2026-11-09'), str(ROOT / 'src')]
import adapter  # noqa: E402
import budget  # noqa: E402
from hivemind import config, model  # noqa: E402
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
LADDER_COLUMNS = ('thesis_id', 'view_id', 'status', 'reason', 'reference_status', 'checked_answer', 'outcome_record', 'config_checksum',
                  'article_seq', 'article_day')


class LedgerBudget(budget.Budget):
    """The Stage 2 adapter's spending limit, with each attempt's reserve and its charge written to a ledger file inside the same
    locked step that takes or releases it: one whole JSON object a line, flushed and synced."""

    def __init__(self, cap_usd, ledger_path, attempt=None, sleep=None):
        super().__init__(cap_usd, attempt=attempt, **({'sleep': sleep} if sleep else {}))
        self.ledger_path = Path(ledger_path)
        self.spent_usd = ledger_total(self.ledger_path)          # what earlier processes spent under this ledger counts against the cap
        self.attempts = max(attempt_ids(self.ledger_path), default=0)

    def _write(self, line):
        with self.ledger_path.open('a') as handle:
            handle.write(json.dumps(line) + '\n')
            handle.flush()
            os.fsync(handle.fileno())

    def send(self, provider, request):
        reserve = budget.worst_cost(request)
        for attempt_number in range(budget.ATTEMPTS):
            with self.lock:
                if self.spent_usd + self.reserved_usd + reserve > self.cap_usd:
                    raise budget.OverBudget(f'spent ${self.spent_usd:.4f}, ${self.reserved_usd:.4f} in flight; '
                                            f'${reserve:.4f} more would pass the ${self.cap_usd:.2f} cap')
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
            if response is not None:
                return response
            retried = getattr(failure, 'http_status', None) not in budget.NOT_RETRIED and str(failure) not in budget.UNDECODABLE
            if not retried or attempt_number + 1 == budget.ATTEMPTS:
                raise failure
            self.sleep(5 * (attempt_number + 1))


def attempt_ids(ledger_path):
    return [json.loads(line)['attempt'] for line in Path(ledger_path).read_text().splitlines()] if Path(ledger_path).exists() else []


def ledger_total(ledger_path):
    """What the ledger says was spent: a charge where there is one, the reserve where an attempt has none."""
    reserves, charges = {}, {}
    for line in Path(ledger_path).read_text().splitlines() if Path(ledger_path).exists() else []:
        entry = json.loads(line)
        if 'reserve' in entry:
            reserves[entry['attempt']] = entry['reserve']
        else:
            charges[entry['attempt']] = entry['charge']
    return sum(charges.values()) + sum(reserve for attempt, reserve in reserves.items() if attempt not in charges)


class LadderAdapter(adapter.Adapter):
    """The Stage 2 adapter in its ladder mode: no seed, no ruler view; views come only from the ladder step's answers."""

    def __init__(self, views_path, archive_path, ledger_path, *, transport=None, cap_usd=0.66, sleep=None, limit=None):
        self.conn = store.open_db(views_path)
        self.conn.execute(f"create table if not exists clean_ladders ({', '.join(LADDER_COLUMNS)}, primary key (thesis_id))")
        self.conn.commit()
        self.archive = model.Archive(archive_path)
        self.cfg = config.load(adapter.CONFIG)
        self.transport = transport
        self.budget = limit if limit is not None else LedgerBudget(cap_usd, ledger_path, attempt=transport, sleep=sleep)
        self.q23 = None
        self.views = set()
        self.mapping = {}
        self.unjudged = set()            # theses with a ladder row and no view
        self.evidence_of = {}
        self.counts = collections.Counter()
        self.next_number = 1
        self.sent = []

    def open_thesis(self, thesis_id, outcome, k, day, input_id, source):
        """Write the thesis's ladder row and, for a written ladder, its view; not committed here."""
        status = STATUS[outcome['status']]
        number = thesis_id.split('-', 1)[1]
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
        else:
            checked = answer if status == 'no ladder' else None
        store.insert(self.conn, 'clean_ladders', thesis_id=thesis_id, view_id=view_id, status=status,
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
                          seq=k, input_id=input_id, created_at=f'{day}T00:00:00Z')
        self.views.add(view_id)
        self.mapping[thesis_id] = [view_id]
        self.counts['views written from a ladder'] += 1

    def _link(self, evidence_id, thesis_id, k, changed):
        if evidence_id is not None and thesis_id in self.unjudged:
            self.counts['links to an unjudged thesis'] += 1
            return
        if evidence_id is not None and thesis_id in self.mapping:
            for view_id in self.mapping[thesis_id]:
                self.counts['links from a laddered thesis to its view'] += 1
                super()._link(evidence_id, view_id, k, changed)
            return
        super()._link(evidence_id, thesis_id, k, changed)

    def due_day_guard(self, day):
        for view_id in sorted(self.views):
            due = store.view(self.conn, view_id)['due_day']
            if due and due <= day and store.is_open(self.conn, view_id):
                raise SystemExit(f'{view_id} is open and due {due}, on or before the replay day {day}: closing is pull mode\'s, not run here')


def ladders_for(run, opened, days_of):
    """{thesis id: stored outcome} for the draw, after checking that the stored cases are exactly the theses the trace opened, each
    with the same description, and that each has exactly one outcome."""
    cases = {case['case']: case for case in json.loads(CASES.read_text()) if case['case'].startswith(f'{run}/')}
    outcomes = collections.defaultdict(list)
    for line in LADDERS.read_text().splitlines():
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
        if len(outcomes[name]) != 1 or outcomes[name][0]['pass'] != 1 or outcomes[name][0]['status'] not in STATUS:
            raise SystemExit(f'{name}: not exactly one first-send outcome with a known status in {LADDERS.name}')
    return {name.split('/', 1)[1]: outcomes[name][0] for name in cases}


def ladder_configuration():
    """The checksum of the ladder configuration that wrote the stored answers, as its model archive records it: exactly one."""
    import sqlite3
    conn = sqlite3.connect(f'file:{LADDER_ARCHIVE}?mode=ro', uri=True)
    try:
        found = conn.execute('select distinct config_version, config_checksum from model_calls').fetchall()
    finally:
        conn.close()
    if len(found) != 1:
        raise SystemExit(f'the ladder archive names {len(found)} configurations, not one')
    return f'{found[0][0]} {found[0][1]}'


def replay(run, output_folder, *, transport=None, cap_usd=0.66, sleep=None, limit=None):
    output = Path(output_folder).resolve()
    if transport is None and OUTPUT_ROOT.resolve() not in output.parents:
        raise SystemExit(f'a live replay writes only under {OUTPUT_ROOT}')
    output.mkdir(parents=True, exist_ok=False)
    trace_path, step2_folder = DRAWS[run]
    by_article, library = adapter.load_draw(trace_path, step2_folder)
    days_of, opened, failed = adapter.trace_articles(trace_path)
    ladders = ladders_for(run, opened, days_of)
    source = ladder_configuration()
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
                           limit=limit)
    spent_before = runner.budget.spent_usd
    runner.counts['articles not completed by Step 1'] = len(failed)
    runner.counts['ladder configuration'] = source
    runner.counts['ladder answers file sha256'] = hashlib.sha256(LADDERS.read_bytes()).hexdigest()
    for day, articles in days.items():
        runner.due_day_guard(day)
        changed = set()
        for k in articles:
            input_id = by_article[k][0]['input_id'] if k in by_article else f'article:{k}'
            opened_here = sorted(opened.get(k, {}), key=lambda name: int(name.split('-', 1)[1]))
            for thesis_id in opened_here:
                runner.open_thesis(thesis_id, ladders[thesis_id], k, day, input_id, source)
            runner.article(k, by_article.get(k, []), library, revisions_by_record, later_by_article.get(k, []), changed)
            for thesis_id in opened_here:
                for view_id in runner.mapping.get(thesis_id, []):
                    if runner.conn.execute('select count(*) from evidence_links where view_id=?', (view_id,)).fetchone()[0] == 0:
                        runner.counts['views with no opening evidence'] += 1
        runner.due_day_guard(day)                    # again, so a view opened today and already due is never judged
        runner.conn.commit()
        if changed:
            runner.judge(day, max(articles), changed)
    runner.due_day_guard(list(days)[-1])
    runner.counts['judging usd this draw (from tokens)'] = round(runner.budget.spent_usd - spent_before, 4)
    runner.counts['judging usd of the whole limit so far (from its ledger)'] = round(ledger_total(runner.budget.ledger_path), 4)
    (output / 'adapter-counts.json').write_text(json.dumps(runner.counts, indent=1))
    (output / 'judge-requests.json').write_text(json.dumps(runner.sent, indent=1))
    return runner


if __name__ == '__main__':
    raise SystemExit('Stage B is sent through run_stage_b.py, which runs the three draws under one spending limit')
