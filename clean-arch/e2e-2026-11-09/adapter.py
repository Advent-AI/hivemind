"""Seeded end-to-end diagnostic (D392): feed one clean draw (Step 1 trace and Step 3 library) to the frozen production judge and write
a views.sqlite that the frozen judgement scorer reads.

The replay follows production's dispatch order. Article k (its position in the Step 1 manifest, as Step 2 numbers it) gets sequence
number k. Its records are written in Step 1's record order, each as evidence `e<N>` with its source and its Step 1 links at seq k:
- A repeat member is stored as its own evidence with a same_claims relation to its group's original (D204).
- A revision is written when the record that brought it (library `revises[].by`) is written. It is one revisions row from the revised
  group's original to that record, and the new piece inherits the old piece's links (writing.py:256-261). Several revisions of one
  piece are several rows; the judge shows the latest, as production does (store.revision_of).
- After an article's records, the later links its processing made (library.later_log) are written at seq k.

After a day's last article, the frozen `judging.round_of_judgements` judges the views that got a new link that day, with that article's
seq, as round.judge_day does.

**Leakage checks:**
- Before each judging round, no table holds a row after the round's seq and no source is published after its day.
- Every request shows exactly the evidence ids, in order, that production's selection (`evidence_in_view`) chose for that view when
  the prompt was built.

The prompt text is built by the frozen judging code from that database, so these two checks bound what the judge can read.

**Views.** Only the 22 seeds are views, plus at most one clean-opened thesis passed as `q23`, after a reader confirmed it asks q23's
question (plan v4). It is created when its opening article is written, with a yes/no ladder; the scorer finds it by its own rule. Links
to any other clean-opened thesis are counted and dropped. A record with no verified passage is dropped and counted, as production drops
a quote not in its item.

**Field mapping.** quote = the verified passages, joined; one_line = summary; speaker = reporting speaker (falling back to the original
party); original_who = original party; original_day = statement date.

Usage:
- `adapter.py candidates <trace> <step2 folder>` lists clean-opened theses that match the scorer's q23 rule.
- `adapter.py live <trace> <step2 folder> <output folder> [--q23 <clean thesis id>] [--unseeded] [--map clean-N=vK ...] [--cap 3]`"""
import argparse, collections, hashlib, importlib.util, json, re, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.dont_write_bytecode = True
sys.path[:0] = [str(HERE), str(ROOT / 'src')]
from hivemind import config, model, seeding  # noqa: E402
from hivemind.views import judging, store  # noqa: E402
import budget  # noqa: E402

SEEDS = ROOT / 'poc/seeds/nvda-2026-07-01-v2.json'
CONFIG = ROOT / 'poc/config/poc-v108.json'
OUTPUT_ROOTS = (ROOT / 'poc/data/clean-e2e-2026-11-09', ROOT / 'poc/data/clean-unseeded-2026-11-10')
SEED_IDS = {q['view_id'] for q in json.loads(SEEDS.read_text())['questions']}
RULER_QUESTIONS = ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold/questions-v1.json'
Q23_VIEW = 'v23'   # the ruler's Ohio-guarantee question, created only when a mapping names it
SHOWN_EVIDENCE = re.compile(r'^- (e\d+) \[', re.M)
JUDGED_VIEW = re.compile(r'^Thesis (\S+) \(', re.M)   # judging._lines_english's first line names the view judged
DATE = re.compile(r'\d{4}-\d{2}-\d{2}')
RECORD_FIELDS = ('article', 'input_id', 'summary', 'passages', 'original_party', 'reporting_speaker', 'tier', 'statement_date',
                 'publication_date', 'thesis_ids')


class Leak(Exception):
    pass


def _step1_records():
    spec = importlib.util.spec_from_file_location('run_forward', ROOT / 'clean-arch/step2/run_forward.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.step1_records


def trace_articles(trace_path):
    """Per completed article, by manifest position: its publication day, and the theses it opened ({id: thesis}); the positions of
    articles no segment completed. `trace_path` may join continuation segments with '+' (as run_forward.step1_records reads them): an
    article is numbered by its position in the first segment's manifest, and an article a later segment completed is not failed."""
    days, opened, failed = {}, {}, set()
    position = None
    for part in str(trace_path).split('+'):
        conn = sqlite3.connect(f'file:{part}?mode=ro', uri=True)
        try:
            if position is None:
                position = {iid: n for n, iid in enumerate(json.loads(conn.execute('select manifest from run').fetchone()[0])['item_ids'], 1)}
            rows = conn.execute('select input_id, request, before_state, after_state, status from trace order by sequence').fetchall()
        finally:
            conn.close()
        for input_id, request, before, after, status in rows:
            k = position[input_id]
            if status != 'complete':
                failed.add(k)
                continue
            failed.discard(k)
            days[k] = json.JSONDecoder().raw_decode(json.loads(request)['messages'][1]['content'])[0]['source_item']['publication_date']
            before_ids = {t['id'] for t in json.loads(before)}
            opened[k] = {t['id']: t for t in json.loads(after) if t['id'] not in before_ids}
    return days, opened, sorted(failed - set(days))


def q23_candidates(opened):
    """Clean-opened theses the scorer's own q23 rule would find (question like '%Ohio%' and like '%guarantee%', case-insensitive)."""
    return [{'article': k, **thesis} for k, theses in sorted(opened.items()) for thesis in theses.values()
            if 'ohio' in thesis['description'].lower() and 'guarantee' in thesis['description'].lower()]


def load_draw(trace_path, step2_folder):
    articles, _, _ = _step1_records()(str(trace_path))
    library = json.loads((Path(step2_folder) / 'library.json').read_text())
    stamp = Path(step2_folder) / 'inputs.sha256'
    expected = [hashlib.sha256(Path(part).read_bytes()).hexdigest() for part in str(trace_path).split('+')]
    expected.append(hashlib.sha256((Path(step2_folder) / 'library.json').read_bytes()).hexdigest())
    if not stamp.exists() or [line.split()[0] for line in stamp.read_text().splitlines()] != expected:
        raise SystemExit(f'{stamp} does not name this trace and this library as the launcher stamped them after Step 2')
    records = {r['id']: r for article in articles for r in article}
    if set(records) != set(library['placement']):
        raise SystemExit('the Step 1 records and the Step 3 library hold different records')
    copies = [g['original'] for g in library['groups'].values()] + [m for g in library['groups'].values() for m in g['members']]
    for copy in copies:
        differing = [f for f in RECORD_FIELDS if copy.get(f) != records[copy['id']].get(f)]
        if differing:
            raise SystemExit(f"the library's copy of {copy['id']} differs from the trace in {differing}: not this draw's library")
    for group in library['groups'].values():
        for revision in group['revises']:
            if revision['group'] not in library['groups'] or revision['by'] not in records:
                raise SystemExit(f'a revision names an unknown group or record: {revision}')
    for entry in library['later_log']:
        if any(record_id not in records for record_id in entry['linked']):
            raise SystemExit(f"a later link names an unknown record: {entry}")
    return {article[0]['article']: article for article in articles}, library


def quote_of(record):
    return ' … '.join(p for p in (record.get('verified_passages') or []) if p)


class Adapter:
    def __init__(self, views_path, archive_path, *, transport=None, cap_usd=3.0, q23=None, mapping=None, created_at='2026-07-01T00:00:00Z'):
        """mapping (unseeded runs, D395): {clean thesis id: [ruler view ids]}. A clean thesis matched to ruler questions by the frozen rule
        (unseeded-2026-11-10/MATCHING-v2.md) feeds its links to each matched question's view, which carries the ruler's text and ladder;
        every other clean thesis's links are dropped and counted. In mapping mode all 23 ruler views exist from seq 0 (the ruler's q23
        included). q23 (seeded runs) and mapping are exclusive."""
        if q23 is not None and mapping:
            raise SystemExit('q23 is for seeded runs and mapping for unseeded runs; not both')
        self.conn = store.open_db(views_path)
        self.archive = model.Archive(archive_path)
        self.cfg = config.load(CONFIG)
        self.transport = transport
        self.budget = budget.Budget(cap_usd, attempt=transport)
        self.q23 = q23
        self.views = set(SEED_IDS)
        self.mapping = {clean_id: ([views] if isinstance(views, str) else list(views)) for clean_id, views in (mapping or {}).items()}
        seeding.seed_views(self.conn, SEEDS, created_at)
        self.evidence_of = {}            # clean record id -> evidence id
        self.counts = collections.Counter()
        if mapping is not None:
            self.create_ruler_q23(created_at)
        self.next_number = 1
        self.sent = []                   # one entry per judge request: day, seq, view, evidence shown

    def create_ruler_q23(self, created_at):
        """The ruler's q23 as a view from the start, with its own text and ladder (questions-v1.json), as the seeds are."""
        questions = json.loads(RULER_QUESTIONS.read_text())
        q23 = next(q for q in (questions['questions'] if isinstance(questions, dict) else questions) if q['id'] == 'q23')
        store.create_view(self.conn, view_id=Q23_VIEW, object_id='NVDA', object_kind='company', kind=q23['kind'], looks_at=q23['question'],
                          question=q23['question'], due_day=q23['due_day'], year=q23['due_day'][:4],
                          rungs=[{'label': r['label'], 'condition': r['condition'], 'lo': None, 'hi': None} for r in q23['rungs']],
                          seq=0, input_id='ruler:questions-v1.json', created_at=created_at)
        self.views.add(Q23_VIEW)
        self.counts['ruler q23 view created'] += 1

    def open_q23(self, thesis, k, input_id, day):
        due = DATE.search(thesis.get('period') or '')
        store.create_view(self.conn, view_id=thesis['id'], object_id='NVDA', object_kind='company', kind='asset', looks_at=thesis['outcome'],
                          question=thesis['description'], due_day=due.group(0) if due else '', year=due.group(0)[:4] if due else '',
                          rungs=[{'label': 'Yes', 'condition': 'It has happened by the due day.', 'lo': None, 'hi': None},
                                 {'label': 'No', 'condition': 'It has not.', 'lo': None, 'hi': None}],
                          seq=k, input_id=input_id, created_at=f'{day}T00:00:00Z')
        self.views.add(thesis['id'])
        self.counts['q23 view opened'] += 1

    def _new_evidence(self, record, k):
        quote = quote_of(record)
        if not quote:
            self.counts['records dropped: no verified passage'] += 1
            return None
        if len(quote) > 400:
            self.counts['quotes cut by the judge at 400 characters'] += 1
        evidence_id = f'e{self.next_number}'
        self.next_number += 1
        store.add_evidence(self.conn, evidence_id=evidence_id, quote=quote, one_line=record['summary'],
                           speaker=record.get('reporting_speaker') or record.get('original_party') or '',
                           original_who=record.get('original_party') or '', original_day=record.get('statement_date') or '',
                           tier=record['tier'], event_time=None, seq=k, input_id=record['input_id'])
        store.add_source(self.conn, evidence_id, record['input_id'], 'news', record['publication_date'], None, k)
        self.evidence_of[record['id']] = evidence_id
        self.counts['evidence written'] += 1
        return evidence_id

    def _link(self, evidence_id, thesis_id, k, changed):
        if evidence_id is None:
            self.counts['links lost with a dropped record'] += 1
            return
        if thesis_id in self.mapping:
            for view_id in self.mapping[thesis_id]:
                self.counts['links through a matched clean thesis'] += 1
                self._link(evidence_id, view_id, k, changed)
            return
        if thesis_id not in self.views:
            self.counts['links to other clean-opened theses dropped'] += 1
            return
        if store.link(self.conn, evidence_id, thesis_id, k):
            changed.add(thesis_id)
            self.counts['links written'] += 1

    def article(self, k, records, library, revisions_by_record, later_entries, changed):
        for record in records:
            evidence_id = self._new_evidence(record, k)
            for thesis_id in record['thesis_ids']:
                self._link(evidence_id, thesis_id, k, changed)
            group = library['groups'][library['placement'][record['id']]]
            if group['original']['id'] != record['id']:
                original = self.evidence_of.get(group['original']['id'])
                if evidence_id and original:
                    store.relate_same(self.conn, original, evidence_id, k)
                    self.counts['same_claims written'] += 1
                else:
                    self.counts['same_claims lost with a dropped record'] += 1
            for revised_group in revisions_by_record.get(record['id'], []):
                old = self.evidence_of.get(library['groups'][revised_group]['original']['id'])
                if not (evidence_id and old):
                    self.counts['revisions lost with a dropped record'] += 1
                    continue
                store.revise(self.conn, old, evidence_id, record.get('statement_date') or record['publication_date'], k)
                self.counts['revisions written'] += 1
                for view_id in store.views_linked_to(self.conn, old):
                    self._link(evidence_id, view_id, k, changed)
        for entry in later_entries:
            for record_id in entry['linked']:
                self._link(self.evidence_of.get(record_id), entry['thesis'], k, changed)

    def leakage_check(self, day, seq):
        for table, column in (('views', 'created_seq'), ('evidence', 'created_seq'), ('evidence_sources', 'seq'), ('evidence_links', 'seq'),
                              ('same_claims', 'seq'), ('revisions', 'seq')):
            top = self.conn.execute(f'select max({column}) from {table}').fetchone()[0]
            if top is not None and top > seq:
                raise Leak(f'{table}.{column} {top} is after day {day} (seq {seq})')
        late = self.conn.execute('select count(*) from evidence_sources where publication_day > ?', (day,)).fetchone()[0]
        if late:
            raise Leak(f'{late} sources published after {day}')

    def judge(self, day, seq, changed):
        """Judge the day's changed views with the frozen judge. The selection is recorded in this thread when each prompt is built; the
        comparison with the request is made in the sending thread without touching the database."""
        self.leakage_check(day, seq)
        selected_by_view = {}
        production_selection = judging.evidence_in_view
        def recording_selection(conn, view_id):
            result = production_selection(conn, view_id)
            selected_by_view[view_id] = [piece['evidence_id'] for piece in result[0]]
            return result
        def watching(provider, request):
            text = request['messages'][-1]['content']
            shown = SHOWN_EVIDENCE.findall(text)
            named = JUDGED_VIEW.search(text)
            view_id = named.group(1) if named else None
            if view_id not in self.views or view_id not in selected_by_view:
                raise Leak(f'a request on {day} judges {view_id}, not a view this replay built a prompt for')
            if shown != selected_by_view[view_id]:
                raise Leak(f'{view_id} on {day}: the request shows {shown}, the selection was {selected_by_view[view_id]}')
            response = self.budget.send(provider, request)
            with self.budget.lock:
                self.sent.append({'day': day, 'seq': seq, 'view': view_id, 'shown': shown})
            return response
        item = {'input_id': f'day:{day}', 'publication_day': day}
        judging.evidence_in_view = recording_selection
        try:
            judged = judging.round_of_judgements(self.archive, self.cfg, self.conn, sorted(changed), seq, item, transport=watching)
        finally:
            judging.evidence_in_view = production_selection
        self.conn.commit()
        self.counts['judgements'] += len(judged)
        return judged


def replay(trace_path, step2_folder, output_folder, *, transport=None, cap_usd=3.0, q23=None, mapping=None):
    output = Path(output_folder).resolve()
    if transport is None and not any(root.resolve() in output.parents for root in OUTPUT_ROOTS):
        raise SystemExit(f'a live replay writes only under {OUTPUT_ROOTS}')
    output.mkdir(parents=True, exist_ok=False)
    by_article, library = load_draw(trace_path, step2_folder)
    days_of, opened, failed = trace_articles(trace_path)
    if q23 is not None and q23 not in {t['id'] for t in q23_candidates(opened)}:
        raise SystemExit(f'{q23} is not a clean-opened thesis matching the scorer rule')
    opened_ids = {thesis_id for theses in opened.values() for thesis_id in theses}
    for clean_id, views in (mapping or {}).items():
        if clean_id not in opened_ids:
            raise SystemExit(f'{clean_id} is not a thesis this run opened')
        for view_id in ([views] if isinstance(views, str) else views):
            if view_id not in SEED_IDS | {Q23_VIEW}:
                raise SystemExit(f'{view_id} is not a ruler question view')
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
    adapter = Adapter(output / 'views.sqlite', output / 'archive.sqlite', transport=transport, cap_usd=cap_usd, q23=q23, mapping=mapping)
    adapter.counts['articles not completed by Step 1'] = len(failed)
    for day, articles in days.items():
        changed = set()
        for k in articles:
            for thesis_id, thesis in opened.get(k, {}).items():
                if thesis_id == q23:
                    adapter.open_q23(thesis, k, by_article[k][0]['input_id'] if k in by_article else f'article:{k}', day)
            adapter.article(k, by_article.get(k, []), library, revisions_by_record, later_by_article.get(k, []), changed)
        adapter.conn.commit()
        if changed:
            adapter.judge(day, max(articles), changed)
    adapter.counts['judging usd (from tokens)'] = round(adapter.budget.spent_usd, 4)
    (output / 'adapter-counts.json').write_text(json.dumps(adapter.counts, indent=1))
    (output / 'judge-requests.json').write_text(json.dumps(adapter.sent, indent=1))
    return adapter


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['candidates', 'live'])
    parser.add_argument('trace'); parser.add_argument('step2'); parser.add_argument('output', nargs='?')
    parser.add_argument('--q23'); parser.add_argument('--cap', type=float, default=3.0)
    parser.add_argument('--unseeded', action='store_true', help='mapping mode even when no thesis matched (an empty mapping)')
    parser.add_argument('--map', action='append', default=[], help='clean-N=vK[,vJ]: an unseeded run\'s matched thesis (D395); repeatable')
    args = parser.parse_args()
    mapping = {}
    for entry in args.map:   # clean-N=vK, or clean-N=vK,vJ for a thesis matched to two ruler questions; a repeated key adds views
        clean_id, views = entry.split('=', 1)
        mapping.setdefault(clean_id, []).extend(v for v in views.split(',') if v)
    mapping = mapping if (args.map or args.unseeded) else None
    if args.mode == 'candidates':
        print(json.dumps(q23_candidates(trace_articles(args.trace)[1]), indent=1, ensure_ascii=False))
    else:
        if not args.output:
            parser.error('live needs an output folder')
        result = replay(args.trace, args.step2, args.output, cap_usd=args.cap, q23=args.q23, mapping=mapping)
        print(json.dumps(result.counts, indent=1))
