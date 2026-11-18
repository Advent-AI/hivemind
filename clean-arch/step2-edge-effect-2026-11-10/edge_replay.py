#!/usr/bin/env python3
"""Does one unsupported Step 2 revision relation change what the frozen judge reads? An offline replay of the saved D392 clean draw 1.

No request leaves this process: every judge request is answered from the saved judging archive of the draw
(`poc/data/clean-e2e-2026-11-09/stage2-clean-d1/judged/archive.sqlite`) by `control_v108.ReferenceArchiveTransport`, which answers
only a byte-identical canonical request and raises on any other. The credential reader and the production transport are replaced by a
refusal while a replay runs.

  edge_replay.py control <new folder>
      The untouched draw through the current adapter and the frozen judge. Passes only when every request finds its saved answer,
      every saved row is used, and the ledger, the judge requests and the answers equal the saved run's.
  edge_replay.py counterfactual <new folder> <control folder> --uncarry 70:e4:v22 [--draw 3]
      The same replay over the saved library, with the one link a relation carried (record:question) not written; the relation itself
      stays. `--draw` selects the saved draw for every mode (default 1); a control of the same draw must have passed.
  edge_replay.py counterfactual <new folder> <control folder> --by 70:e4 --revised-group 69:e5 [--keep-links]
      The same replay over a copy of the library with exactly that one revision relation removed (the copy carries its own stamp; the
      saved library is not touched). It stops at the first judging round whose requests differ from the control's (a request with other
      text, a request the control did not send, or a control request not sent) and writes the requests of that round, both versions.
      Nothing after that round is replayed: later state would rest on answers to requests the archive does not hold.
      --keep-links removes the relation but writes the links the new record inherited through it, to separate the inherited link from
      the relation itself.

What a replay shows: whether, and in which round, the judge's input changes. What it cannot show: any answer to a changed request."""
import argparse, collections, contextlib, difflib, hashlib, json, re, shutil, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
E2E = ROOT / 'clean-arch/e2e-2026-11-09'
sys.dont_write_bytecode = True
sys.path[:0] = [str(E2E), str(ROOT / 'src')]
import adapter as e2e_adapter  # noqa: E402
import control_v108  # noqa: E402
from hivemind import model  # noqa: E402
from hivemind.views import store  # noqa: E402

DRAW = ROOT / 'poc/data/clean-e2e-2026-11-09'
TRACE = f"{DRAW / 'stage2-clean-d1/trace.sqlite'}+{DRAW / 'stage2-clean-d1-segment-2/trace.sqlite'}"
STEP2 = DRAW / 'stage2-clean-d1-segment-2/step2'
SAVED = DRAW / 'stage2-clean-d1/judged'
REFUSED = re.compile(r':refused:[0-9a-f]+$')
# Columns the replay cannot reproduce by construction: an archive row number is given in the order answers return from 32 threads.
ARCHIVE_ROW_COLUMNS = {'judgements': {'call_id'}}
LEDGER_TABLES = ('views', 'rungs', 'view_keys', 'view_switches', 'judgements', 'evidence', 'evidence_sources', 'evidence_links',
                 'replacements', 'revisions', 'same_claims', 'dependencies', 'dependency_resolutions', 'successions', 'handovers',
                 'match_records', 'processing_steps', 'review_pool_entries', 'late_statements', 'days_completed', 'thesis_groups',
                 'thesis_group_members', 'thesis_group_aliases')


class Divergence(Exception):
    """The first judging round whose requests differ from the control's."""


class LiveCallRefused(BaseException):
    """A credential or the production transport was reached during an offline replay."""


def refuse_live_calls():
    def refusal(*arguments, **keywords):
        raise LiveCallRefused('an offline replay reached the credential reader or the production transport')
    model._key = refusal
    model.openai_transport = refusal


class RecordingTransport:
    """Passes each request to the reference archive transport and records it with the judging round it belongs to."""

    def __init__(self, reference):
        self.reference = reference
        self.round = None                 # (day, seq) of the judging round in progress
        self.requests = []                # one entry per request, answered or not

    def __call__(self, provider, request):
        canonical = control_v108.canonical_text(request)
        text = request['messages'][-1]['content']
        named = e2e_adapter.JUDGED_VIEW.search(text)
        entry = {'day': self.round[0], 'seq': self.round[1], 'view': named.group(1) if named else None,
                 'sha256': control_v108.text_sha256(canonical), 'answered': False, 'request': request}
        self.requests.append(entry)       # list.append is atomic; the round's requests are sent from a thread pool
        response = self.reference(provider, request)
        entry['answered'] = True
        return response

    def of_round(self, day):
        return [entry for entry in self.requests if entry['day'] == day]


def round_signature(entries):
    """The requests of one round as a sorted list of (view, request sha256): the retry after a refused answer is its own request."""
    return sorted((entry['view'], entry['sha256']) for entry in entries)


def use_draw(draw):
    """Point the replays at one of the three saved draws (draw 1 is the default). Draw 3's completed judging is `judged-2`."""
    global TRACE, STEP2, SAVED
    TRACE = f"{DRAW / f'stage2-clean-d{draw}/trace.sqlite'}+{DRAW / f'stage2-clean-d{draw}-segment-2/trace.sqlite'}"
    STEP2 = DRAW / f'stage2-clean-d{draw}-segment-2/step2'
    SAVED = sorted((DRAW / f'stage2-clean-d{draw}').glob('judged*'))[-1]


def clean_thesis_judged():
    """The clean-opened thesis the saved run judged as the ruler's Ohio question (adapter `--q23`), or None: the one view that is not a seed."""
    with contextlib.closing(sqlite3.connect(f"file:{SAVED / 'views.sqlite'}?mode=ro", uri=True)) as conn:
        extra = [view_id for (view_id,) in conn.execute('select view_id from views') if view_id not in e2e_adapter.SEED_IDS]
    if len(extra) > 1:
        raise SystemExit(f'{SAVED} holds more than one view that is not a seed: {extra}')
    return extra[0] if extra else None


def run_replay(output, step2_folder, *, on_round=None, keep_links=None, uncarried=None):
    """Replay the draw into `output` with every request answered from the saved archive. `on_round(day, entries, error)` is called after
    each judging round (error is the ReferenceMissError that ended it, or None). `uncarried` is {record id: [question ids]}: links the
    record would take from a record it revises and is not given here (the relation itself is still written)."""
    refuse_live_calls()
    reference = control_v108.ReferenceArchiveTransport(SAVED / 'archive.sqlite')
    recorder = RecordingTransport(reference)
    production_judge = e2e_adapter.Adapter.judge
    production_article = e2e_adapter.Adapter.article
    production_revise, production_linked = store.revise, store.views_linked_to
    writing = {}                      # the adapter and the record whose relation is being written

    def revise(conn, old_id, new_id, said_day, seq):
        writing['new'] = new_id
        return production_revise(conn, old_id, new_id, said_day, seq)

    def views_linked_to(conn, evidence_id):
        """The adapter's one call that reads the older record's links, made right after `revise` names the pair."""
        linked = production_linked(conn, evidence_id)
        record_id = next((r for r, e in writing['adapter'].evidence_of.items() if e == writing.get('new')), None)
        return [view_id for view_id in linked if view_id not in (uncarried or {}).get(record_id, ())]

    def judge(self, day, seq, changed):
        recorder.round = (day, seq)
        error = None
        try:
            return production_judge(self, day, seq, changed)
        except control_v108.ReferenceMissError as miss:
            error = miss
            raise
        finally:
            if on_round:
                on_round(day, recorder.of_round(day), error)

    def article(self, k, records, library, revisions_by_record, later_entries, changed):
        writing['adapter'] = self
        production_article(self, k, records, library, revisions_by_record, later_entries, changed)
        for record_id, view_ids in (keep_links or {}).items():
            if any(record['id'] == record_id for record in records):
                for view_id in view_ids:
                    self._link(self.evidence_of.get(record_id), view_id, k, changed)
                    self.counts['links kept without their relation'] += 1

    e2e_adapter.Adapter.judge, e2e_adapter.Adapter.article = judge, article
    store.revise, store.views_linked_to = revise, views_linked_to
    try:
        finished = e2e_adapter.replay(TRACE, step2_folder, output, transport=recorder, cap_usd=3.0, q23=clean_thesis_judged())
    finally:
        e2e_adapter.Adapter.judge, e2e_adapter.Adapter.article = production_judge, production_article
        store.revise, store.views_linked_to = production_revise, production_linked
    return finished, recorder, reference


def ledger_rows(path, table):
    with contextlib.closing(sqlite3.connect(f'file:{path}?mode=ro', uri=True)) as conn:
        columns = [row[1] for row in conn.execute(f'pragma table_info({table})')]
        kept = [column for column in columns if column not in ARCHIVE_ROW_COLUMNS.get(table, ())]
        return kept, conn.execute(f"select {', '.join(kept)} from {table} order by rowid").fetchall()


def archive_answers(path):
    """Every archived call as (request sha256 without its refusal mark, refused or not, answer): the multiset a replay must reproduce."""
    with contextlib.closing(sqlite3.connect(f'file:{path}?mode=ro', uri=True)) as conn:
        rows = conn.execute('select request_sha256, answer_json from model_calls').fetchall()
    return collections.Counter((REFUSED.sub('', sha), bool(REFUSED.search(sha)), answer) for sha, answer in rows)


def control(output):
    output = Path(output).resolve()
    adapter, recorder, reference = run_replay(output, STEP2)
    adapter.conn.close()
    failures = []
    if reference.misses:
        failures.append(f'{len(reference.misses)} requests had no saved answer')
    if reference.unused_rows():
        failures.append(f'saved archive rows never asked for: {reference.unused_rows()}')
    compared = {}
    for table in LEDGER_TABLES:
        saved_columns, saved_rows = ledger_rows(SAVED / 'views.sqlite', table)
        replay_columns, replay_rows = ledger_rows(output / 'views.sqlite', table)
        compared[table] = len(saved_rows)
        if saved_columns != replay_columns or saved_rows != replay_rows:
            differing = next((n for n, pair in enumerate(zip(saved_rows, replay_rows)) if pair[0] != pair[1]), min(len(saved_rows), len(replay_rows)))
            failures.append(f'ledger table {table}: {len(saved_rows)} saved rows, {len(replay_rows)} replayed, first difference at row {differing}')
    saved_sent = json.loads((SAVED / 'judge-requests.json').read_text())
    key = lambda entry: (entry['day'], entry['seq'], entry['view'], tuple(entry['shown']))
    if collections.Counter(map(key, saved_sent)) != collections.Counter(map(key, adapter.sent)):
        failures.append('the judge requests (day, seq, view, evidence shown) differ from the saved judge-requests.json')
    if archive_answers(SAVED / 'archive.sqlite') != archive_answers(output / 'archive.sqlite'):
        failures.append('the replayed archive does not hold the saved requests and answers')
    saved_counts = json.loads((SAVED / 'adapter-counts.json').read_text())
    replay_counts = json.loads((output / 'adapter-counts.json').read_text())
    if saved_counts != replay_counts:
        failures.append(f'adapter counts differ: saved {saved_counts}, replayed {replay_counts}')
    rounds = collections.OrderedDict()
    for entry in recorder.requests:
        rounds.setdefault(entry['day'], []).append({name: entry[name] for name in ('day', 'seq', 'view', 'sha256')})
    (output / 'control-rounds.json').write_text(json.dumps(rounds, indent=1))
    requests_by_sha = {entry['sha256']: entry['request'] for entry in recorder.requests}
    (output / 'control-requests.json').write_text(json.dumps(requests_by_sha, ensure_ascii=False))
    report = {'passed': not failures, 'saved run': str(SAVED), 'failures': failures, 'requests answered from the saved archive': sum(reference.matched.values()),
              'saved archive rows': reference.reference_rows, 'ledger rows compared, by table': compared,
              'ledger columns not compared': {table: sorted(columns) for table, columns in ARCHIVE_ROW_COLUMNS.items()},
              'judging rounds': len(rounds), 'adapter counts': replay_counts}
    (output / 'control-report.json').write_text(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))
    if failures:
        raise SystemExit(1)


def library_without_relation(folder, by, revised_group):
    """A copy of the draw's library with exactly one revision relation removed, stamped as its own (a labelled departure from the draw)."""
    library = json.loads((STEP2 / 'library.json').read_text())
    found = [(group_id, n) for group_id, group in library['groups'].items() for n, revision in enumerate(group['revises'])
             if revision['by'] == by and revision['group'] == revised_group]
    if len(found) != 1:
        raise SystemExit(f'{len(found)} relations from {by} to group {revised_group}; exactly one is removed')
    group_id, position = found[0]
    removed = library['groups'][group_id]['revises'].pop(position)
    folder.mkdir(parents=True)
    (folder / 'library.json').write_text(json.dumps(library, ensure_ascii=False))
    digests = [hashlib.sha256(Path(part).read_bytes()).hexdigest() + '  ' + part for part in TRACE.split('+')]
    digests.append(hashlib.sha256((folder / 'library.json').read_bytes()).hexdigest() + '  ' + str(folder / 'library.json'))
    (folder / 'inputs.sha256').write_text('\n'.join(digests) + '\n')
    return {'held by group': group_id, 'removed': removed, 'revised original': library['groups'][revised_group]['original']['id'],
            'revised original thesis ids': library['groups'][revised_group]['original']['thesis_ids']}


def user_text(request):
    return request['messages'][-1]['content']


def counterfactual(output, control_folder, by, revised_group, keep_links, uncarried=None):
    output, control_folder = Path(output).resolve(), Path(control_folder).resolve()
    control_report = json.loads((control_folder / 'control-report.json').read_text())
    if not control_report['passed']:
        raise SystemExit('the control did not pass; no counterfactual is replayed against it')
    if control_report.get('saved run') != str(SAVED):
        raise SystemExit(f"the control is of {control_report.get('saved run')}, not of {SAVED}")
    control_rounds = json.loads((control_folder / 'control-rounds.json').read_text(), object_pairs_hook=collections.OrderedDict)
    control_requests = json.loads((control_folder / 'control-requests.json').read_text())
    if uncarried:
        step2_folder, removed, kept = STEP2, {'links not carried': uncarried}, None
    else:
        scratch = output.parent / (output.name + '-inputs')
        removed = library_without_relation(scratch / 'step2', by, revised_group)
        step2_folder, kept = scratch / 'step2', ({by: removed['revised original thesis ids']} if keep_links else None)
    rounds_seen = []
    found = {}

    def on_round(day, entries, error):
        earlier_missing = [control_day for control_day in control_rounds if control_day < day and control_day not in rounds_seen]
        rounds_seen.append(day)
        expected = sorted((entry['view'], entry['sha256']) for entry in control_rounds.get(day, []))
        if earlier_missing or error or round_signature(entries) != expected:
            found.update(day=day, entries=entries, rounds_without_judging=earlier_missing, error=str(error) if error else None)
            if not error:
                raise Divergence(day)

    diverged = True
    try:
        adapter, recorder, reference = run_replay(output, step2_folder, on_round=on_round, keep_links=kept, uncarried=uncarried)
        adapter.conn.close()
        never_judged = [day for day in control_rounds if day not in rounds_seen]
        if never_judged:
            found.update(day=None, entries=[], rounds_without_judging=never_judged, error=None)
        else:
            diverged = False
    except (Divergence, control_v108.ReferenceMissError):
        pass
    report = {'relation removed': removed, 'links kept without the relation': kept, 'diverged': diverged,
              'rounds identical to the control before the first difference': [day for day in rounds_seen if day != found.get('day')]}
    if diverged:
        day = found['day']
        control_by_view = collections.defaultdict(list)
        for entry in control_rounds.get(day, []):
            control_by_view[entry['view']].append(entry['sha256'])
        replay_by_view = collections.defaultdict(list)
        for entry in found['entries']:
            replay_by_view[entry['view']].append(entry)
        changed = []
        for view_id in sorted(set(control_by_view) | set(replay_by_view)):
            control_shas = control_by_view.get(view_id, [])
            replay_entries = replay_by_view.get(view_id, [])
            if sorted(control_shas) == sorted(entry['sha256'] for entry in replay_entries):
                continue
            first_control = control_requests[control_shas[0]] if control_shas else None
            first_replay = next((entry['request'] for entry in replay_entries if entry['sha256'] not in control_shas), None)
            detail = {'view': view_id, 'control requests': len(control_shas), 'counterfactual requests': len(replay_entries)}
            if first_control and first_replay:
                control_shown = e2e_adapter.SHOWN_EVIDENCE.findall(user_text(first_control))
                replay_shown = e2e_adapter.SHOWN_EVIDENCE.findall(user_text(first_replay))
                detail['evidence only in the control request'] = [e for e in control_shown if e not in replay_shown]
                detail['evidence only in the counterfactual request'] = [e for e in replay_shown if e not in control_shown]
                detail['system text identical'] = first_control['messages'][0] == first_replay['messages'][0]
                detail['diff of the user text'] = list(difflib.unified_diff(user_text(first_control).splitlines(), user_text(first_replay).splitlines(),
                                                                            'control', 'counterfactual', lineterm='', n=0))
                (output / f'request-{view_id}-control.json').write_text(json.dumps(first_control, ensure_ascii=False, indent=1))
                (output / f'request-{view_id}-counterfactual.json').write_text(json.dumps(first_replay, ensure_ascii=False, indent=1))
            changed.append(detail)
        report.update({'first differing round': day, 'control days with no judging round in the counterfactual': found['rounds_without_judging'],
                       'reference miss': found['error'], 'views whose requests differ in that round': changed,
                       'views with identical requests in that round': sorted(v for v in control_by_view if sorted(control_by_view[v]) ==
                                                                              sorted(e['sha256'] for e in replay_by_view.get(v, [])))})
    output.mkdir(parents=True, exist_ok=True)
    (output / 'counterfactual-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(json.dumps({name: value for name, value in report.items() if name != 'views whose requests differ in that round'}, ensure_ascii=False, indent=1))
    for detail in report.get('views whose requests differ in that round', []):
        print(json.dumps({name: value for name, value in detail.items() if name != 'diff of the user text'}, ensure_ascii=False))
        print('\n'.join(detail.get('diff of the user text', [])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['control', 'counterfactual'])
    parser.add_argument('output')
    parser.add_argument('control_folder', nargs='?')
    parser.add_argument('--by'); parser.add_argument('--revised-group'); parser.add_argument('--keep-links', action='store_true')
    parser.add_argument('--draw', type=int, choices=(1, 2, 3), default=1)
    parser.add_argument('--uncarry', action='append', default=[], help='record:question, a carried link not to write; repeatable')
    args = parser.parse_args()
    use_draw(args.draw)
    if args.mode == 'control':
        control(args.output)
    else:
        uncarried = collections.defaultdict(list)
        for entry in args.uncarry:
            record_id, question = entry.rsplit(':', 1)
            uncarried[record_id].append(question)
        if not args.control_folder or not (uncarried or (args.by and args.revised_group)):
            parser.error('counterfactual needs the control folder and either --uncarry or --by with --revised-group')
        counterfactual(args.output, args.control_folder, args.by, args.revised_group, args.keep_links, dict(uncarried) or None)
