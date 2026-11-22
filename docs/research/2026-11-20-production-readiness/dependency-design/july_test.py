"""The July test of the reading-links version (D694 (c), D695; DESIGN.md, TEST-PLAN.md). The only entry point that runs poc-v119.

  python3 july_test.py prefix  <scratch>                 # $0: poc-v119 over 07-01..07-09 with every link question answered "neither"
  python3 july_test.py archive <scratch>                 # $0: the per-sequence archive hides the v9/v14 judge rows, keeps the rest
  python3 july_test.py dry     <scratch> <prefix ledger> # $0: the whole harness on 07-10..07-12 with fake answers for every bought call
  python3 july_test.py price   <scratch>                 # $0: the stored v9/v14 judge calls of the window priced at published rates
  python3 july_test.py send    <scratch> <prefix ledger> <out>   # paid, after the council has passed the $0 proof: six sequences

Each sequence: its own copy of the prefix ledger (old-2 rebuilt to the end of 07-09, `rebuild_control.py`), marked harness-only, held
under the store lock; its own copy of old-2's archive with every v9 and v14 judge row retired, so both questions are judged fresh;
`replay.run` with a serial item runner as its day runner. Requests that miss the archive pass an allow-list before any transport: the
day's judging may send only v9/v14 judge requests; an item may send only link questions, and only at seq 148 in the linked arm. After
seq 148 commits, a link whose reader is not v9 or v14 stops the sequence. A stopped sequence is final.
"""
import json
import shutil
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / 'src'))
from hivemind import config, live_lock, model, replay, universe       # noqa: E402
from hivemind.views import links, store                                # noqa: E402
from hivemind.views import round as rounds                             # noqa: E402

OLD2 = REPO / 'poc/data/comparison-2026-11-17/run/old-2/prod'
ITEMS = REPO / 'poc/data/comparison-2026-11-17/items-comparison.sqlite'
V118 = REPO / 'poc/config/poc-v118.json'
V119 = REPO / 'poc/config/poc-v119.json'
UNIVERSE = REPO / 'poc/universe.json'
LINK_SEQ, PREFIX_SEQ = 148, 147
TARGETS = ('v9', 'v14')
WINDOW = ('2026-07-10', '2026-07-12')
CEILING = 0.15
INTENDED = ('v9', 'v14')                       # Data Center FY2027 reads total revenue FY2027


class Stop(RuntimeError):
    """The harness stopped a sequence (an unapproved request, an out-of-pair link); the sequence is final."""


def judged_view(request):
    """The thesis a judge request is about (its user text begins "Thesis <id> ("), or None for any other request."""
    if 'messages' not in request:
        return None
    text = request['messages'][-1]['content']
    return text.split(' ', 2)[1] if text.startswith('Thesis v') else None


def is_link_request(request):
    questions = request.get('questions') or {}
    return bool(questions) and all(qid.startswith(('reads__', 'sign__')) for qid in questions)


class Latch:
    """One per sequence. Admission and the inner call happen under one lock, so the sequence's paid calls run one at a time: a request
    is refused, or is admitted and runs to its end, before the next is looked at. The first refusal closes the latch, and every later
    request of the sequence, in any thread, a retry included, is refused before the inner transport."""

    def __init__(self):
        import threading
        self.lock, self.reason, self.admitted = threading.Lock(), '', []

    def run(self, allowed, refusal, label, call):
        with self.lock:
            if self.reason:
                raise Stop(f'the sequence is stopped ({self.reason}): not sent')
            if not allowed:
                self.reason = refusal
                raise Stop(refusal)
            self.admitted.append(label)
            return call()


class JudgingScope:
    """The day's judging: only a v9 or v14 judge request may reach the inner transport."""

    def __init__(self, inner, latch):
        self.inner, self.latch, self.sent = inner, latch, []

    def __call__(self, *args):
        request = args[-1]
        view_id = judged_view(request) if len(args) == 2 else None

        def call():
            self.sent.append(view_id)
            return self.inner(*args)
        return self.latch.run(view_id in TARGETS, f'unapproved request in judging (thesis {view_id}): not sent', view_id, call)


class ItemScope:
    """One item's transport: only link questions, only at seq 148, only in the linked arm."""

    def __init__(self, inner, seq, linked, sent, latch, link_seq=LINK_SEQ):
        self.inner, self.seq, self.linked, self.sent, self.latch, self.link_seq = inner, seq, linked, sent, latch, link_seq

    def __call__(self, *args):
        request = args[-1]
        link = len(args) == 1 and is_link_request(request)

        def call():
            self.sent.append(('jev', self.seq, sorted(request['questions'])))
            return self.inner(*args)
        return self.latch.run(link and self.linked and self.seq == self.link_seq,
                              f'unapproved request at seq {self.seq} ({"link questions" if link else "not a link question"}): not sent', ('jev', self.seq), call)


class SerialRunner:
    """replay.run's day runner: each routed item through round.run with a transport bound to its own sequence; after seq 148 commits,
    the committed links are inspected before anything else runs."""

    def __init__(self, inner, linked, latch, link_seq=LINK_SEQ):
        self.inner, self.linked, self.latch, self.link_seq, self.sent, self.links = inner, linked, latch, link_seq, [], []

    def __call__(self, conn, archive, cfg, uni, items, *, day, transport=None, log=print):
        for item, route in items:
            result = rounds.run(conn, archive, cfg, uni, item, route.sequence_no, resume_from=route.resume_from,
                                transport=ItemScope(self.inner, route.sequence_no, self.linked, self.sent, self.latch, self.link_seq), log=log)
            if not result.failed and route.sequence_no == LINK_SEQ:
                self.links = [tuple(r) for r in conn.execute("select view_id, depends_on, direction, seq from dependencies where kind=?", (links.KIND,))]
                outside = [r for r in self.links if r[0] not in TARGETS]
                if outside:
                    self.latch.run(False, f'out-of-pair link committed at seq {LINK_SEQ}: {outside}: the sequence is not comparable', None, None)
            yield result


def retire_targets(archive_path, also=()):
    archive = model.Archive(str(archive_path))
    rows = archive.conn.execute("select call_id, request_json from model_calls where purpose='judge'").fetchall()
    retired = 0
    for call_id, request_json in rows:
        if judged_view(json.loads(request_json)) in TARGETS + tuple(also):
            archive.retire(call_id)
            retired += 1
    top = archive.conn.execute('select coalesce(max(call_id), 0) from model_calls').fetchone()[0]
    return archive, retired, top


def prepare(folder, prefix_ledger, also_retire=()):
    if folder.exists():
        raise SystemExit(f'{folder} exists: a sequence starts from an empty folder and is never resumed')
    folder.mkdir(parents=True)
    views, archive_path = folder / 'views.sqlite', folder / 'archive.sqlite'
    shutil.copyfile(prefix_ledger, views)
    conn = sqlite3.connect(views)
    last, last_day = conn.execute('select seq, day from days_completed order by seq desc limit 1').fetchone()
    unfinished = conn.execute('select count(*) from processing_steps where sequence_no > ?', (last,)).fetchone()[0]
    if last != PREFIX_SEQ or last_day != '2026-07-09' or unfinished:
        raise SystemExit(f'the prefix ledger is not the finished end of 07-09 (last completed {last_day} seq {last}, {unfinished} later steps)')
    sys.path.insert(0, str(Path(__file__).parent))
    import rebuild_control
    if not rebuild_control.compare(views, PREFIX_SEQ):           # the copy equals old-2's finished store up to seq 147, as proved
        raise SystemExit('the prefix ledger differs from old-2 up to seq 147: refused')
    conn.execute('create table harness_only (name text, day text)')
    conn.execute("insert into harness_only values ('july_test.py', '2026-11-21')")
    conn.commit()
    conn.close()
    shutil.copyfile(OLD2 / 'archive.sqlite', archive_path)
    archive, retired, top = retire_targets(archive_path, also_retire)
    return views, archive, retired, top


def run_sequence(scratch, name, prefix_ledger, cfg_path, linked, inner, log, *, link_seq=LINK_SEQ, also_retire=()):
    folder = scratch / name
    summary = {'name': name, 'config': None, 'linked': linked, 'started': True, 'stopped': '', 'comparable': False}
    views = archive_path = None
    try:
        views, archive, retired, top = prepare(folder, prefix_ledger, also_retire)
        archive_path = folder / 'archive.sqlite'
        cfg, uni = config.load(str(cfg_path)), universe.load(str(UNIVERSE))
        latch = Latch()
        judging_scope, runner = JudgingScope(inner, latch), SerialRunner(inner, linked, latch, link_seq)
        summary.update(config=cfg.version, retired_target_rows=retired, archive_top=top)
        held = live_lock.acquire(str(views))
        try:
            replay.run(testdb_path=str(ITEMS), views_path=str(views), archive=archive, cfg=cfg, universe=uni, from_day=WINDOW[0],
                       until_day=WINDOW[1], transport=judging_scope, day_runner=runner, only_objects={'NVDA'}, log=log)
        except Exception as error:
            summary['stopped'] = f'{type(error).__name__}: {error}'[:400]
        finally:
            live_lock.release(held)
        conn = sqlite3.connect(f'file:{views}?mode=ro', uri=True)
        judgements = [dict(zip(('view_id', 'day', 'call_id', 'rung', 'changed', 'reference', 'implied_outcome', 'reasons'), r)) for r in conn.execute(
            'select view_id, publication_day, call_id, rung, changed, reference, implied_outcome, reasons from judgements where seq > ? and view_id in (?, ?) order by judgement_id',
            (PREFIX_SEQ, *TARGETS))]
        calls = [j['call_id'] for j in judgements]
        fresh = bool(judgements) and all(c > top for c in calls) and len(set(calls)) == len(calls)
        intended = (not linked) or any(r[:2] == INTENDED for r in runner.links)
        summary.update(links=runner.links, judge_requests_sent=judging_scope.sent, link_requests_sent=runner.sent, judgements=judgements,
                       all_target_judgements_fresh=fresh, intended_link=intended, latch=latch.reason,
                       handovers_after_link_seq=conn.execute("select count(*) from processing_steps where sequence_no > ? and step='handed_over'", (LINK_SEQ,)).fetchone()[0],
                       selection=[tuple(r) for r in conn.execute('select attempt_id, status, record_json from link_selections order by id')])
        summary['comparable'] = not summary['stopped'] and fresh
    except BaseException as error:
        summary['stopped'] = summary['stopped'] or f'{type(error).__name__}: {error}'[:400]
        raise
    finally:
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'summary.json').write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    return summary, views, archive_path


# ---------- fakes for the $0 runs ----------

def marker(kind, label, view_id, n):
    return f'{kind}|{label}|{view_id}|{n}'


def fake_judge(label, changed_on):
    """A judge answering every v9/v14 request with markers unique to the sequence, the question and the attempt; `changed_on` maps
    (view, n) to the changed flag of that view's n-th judgement in the sequence; a first judgement always says changed."""
    calls = {}

    def answer(provider, request):
        text = request['messages'][-1]['content']
        view_id = judged_view(request)
        calls[view_id] = n = calls.get(view_id, 0) + 1
        changed = True if '[Previous conclusion] none' in text else changed_on.get((view_id, n), True)
        data = {'rung': 3, 'reference': marker('P', label, view_id, n), 'implied_outcome': marker('F', label, view_id, n),
                'reasons': marker('M', label, view_id, n), 'cites': [], 'cites_views': [], 'pushes': [], 'changed': changed,
                'why_changed': '', 'theme_pushes': []}
        return {'choices': [{'message': {'content': json.dumps(data)}}], 'usage': {'prompt_tokens': 100, 'completion_tokens': 10}}
    return answer


def fake_jev(readers):
    """Link questions: `readers` are the theses answered "the THESIS reads the CANDIDATE" (sign together); every other pair neither."""
    def answer(request):
        answers = {}
        for qid, question in request['questions'].items():
            view_id = qid.split('__', 1)[1]
            chosen = (links.THESIS_READS if view_id in readers else links.NEITHER) if qid.startswith('reads__') else links.TOGETHER
            others = [k for k in question['criteria'] if k != chosen]
            probabilities = {k: round(0.2 / len(others), 4) for k in others}
            probabilities[chosen] = round(1 - sum(probabilities.values()), 4)
            answers[qid] = {'type': 'choice', 'choice': chosen, 'confidence': probabilities[chosen], 'probabilities': probabilities}
        return {'model': request['model'], 'answers': answers, 'usage': {'input_tokens': 100, 'output_tokens': 10}}
    return answer


def dispatcher(judge, jev_answer, counter):
    def transport(*args):
        counter.append(len(args))
        return jev_answer(args[0]) if len(args) == 1 else judge(*args)
    return transport


def calls_of(archive_path, top):
    """The target judge calls a sequence made, in order: {view: [(user text, answer data)]}."""
    archive = sqlite3.connect(f'file:{archive_path}?mode=ro', uri=True)
    out = {}
    for request_json, answer_json in archive.execute("select request_json, answer_json from model_calls where purpose='judge' and call_id > ? order by call_id", (top,)):
        request = json.loads(request_json)
        out.setdefault(judged_view(request), []).append((request['messages'][-1]['content'], json.loads(answer_json)))
    return out


def previous_reasons(text):
    if '[Previous conclusion] none' in text:
        return None
    return text.split('[Previous conclusion, for comparison only] rung ', 1)[1].split('; reasons: ', 1)[1].split('\n', 1)[0]


def chain_checks(summary, archive_path, prefix_ledger, label):
    """Each target request carries exactly the previous accepted answer of its own question in this sequence (the first: the prefix's);
    in the linked arm each v9 request shows exactly that day's accepted v14 comparison point and forecast."""
    calls = calls_of(archive_path, summary['archive_top'])
    prefix = sqlite3.connect(f'file:{prefix_ledger}?mode=ro', uri=True)
    stored_v9 = prefix.execute("select reasons from judgements where view_id='v9' order by judgement_id desc limit 1").fetchone()[0]
    checks = {}
    for view_id in TARGETS:
        rows = calls.get(view_id, [])
        expected = [None if view_id == 'v14' else stored_v9[:800]] + [answer['reasons'] for _, answer in rows[:-1]]
        checks[f'{view_id}: each request carries exactly its previous accepted answer'] = bool(rows) and \
            [previous_reasons(text) for text, _ in rows] == expected
    if summary['linked']:
        v9_days = [j['day'] for j in summary['judgements'] if j['view_id'] == 'v9']
        v14 = {j['day']: (j['reference'], j['implied_outcome']) for j in summary['judgements'] if j['view_id'] == 'v14'}
        checks['v9: each request shows that day\'s accepted v14 comparison point and forecast'] = bool(v9_days) and all(
            f'Comparison point stated by that judgement: {v14[day][0]}' in text and f'(our own judgement, not evidence): {v14[day][1]}' in text
            for (text, _), day in zip(calls.get('v9', []), v9_days))
    return checks


def latch_race():
    """Worker A is admitted and its call is held open; worker B (an unapproved v8 request) arrives meanwhile; then worker C (v9). B
    must wait for A to finish, then be refused and close the latch; C must be refused; only A reaches the inner transport."""
    import threading
    started, release, inner_calls, outcomes = threading.Event(), threading.Event(), [], {}

    def inner(provider, request):
        inner_calls.append(judged_view(request))
        started.set()
        release.wait(5)
        return {'ok': True}
    scope = JudgingScope(inner, Latch())

    def worker(name, view_id):
        try:
            scope('openai', {'messages': [{'role': 'user', 'content': f'Thesis {view_id} (NVDA'}]})
            outcomes[name] = 'sent'
        except Stop as error:
            outcomes[name] = f'refused: {error}'
    a = threading.Thread(target=worker, args=('A', 'v9'))
    a.start()
    started.wait(5)
    b = threading.Thread(target=worker, args=('B', 'v8'))
    b.start()
    b_waited = b.is_alive()
    release.set()
    a.join(5)
    b.join(5)
    worker('C', 'v14')
    return {'A admitted and finished': outcomes.get('A') == 'sent', 'B waited for A, then was refused': b_waited and outcomes.get('B', '').startswith('refused: unapproved'),
            'C refused after the latch closed': outcomes.get('C', '').startswith('refused: the sequence is stopped'), 'only A reached the inner transport': inner_calls == ['v9']}


def dry(scratch, prefix_ledger):
    scratch.mkdir(parents=True, exist_ok=True)
    checks, log = {}, (lambda *a: None)
    checks['latch: a request arriving during an admitted call'] = latch_race()
    plans = {'control-A': (V118, False, {}), 'control-B': (V118, False, {}),
             'linked-A': (V119, True, {('v14', 2): True}), 'linked-B': (V119, True, {('v14', 2): False})}
    for name, (cfg_path, linked, changed_on) in plans.items():
        summary, _, archive_path = run_sequence(scratch, name, prefix_ledger, cfg_path, linked,
                                                dispatcher(fake_judge(name, changed_on), fake_jev({'v9'}), []), log)
        days = {(j['view_id'], j['day']) for j in summary['judgements']}
        checks[name] = {'not stopped': summary['stopped'] == '', 'comparable (fresh, not stopped)': summary['comparable'],
                        'v14 judged each day': {d for v, d in days if v == 'v14'} == {'2026-07-10', '2026-07-11', '2026-07-12'},
                        'v9 days': sorted(d for v, d in days if v == 'v9'), **chain_checks(summary, archive_path, prefix_ledger, name)}
        if linked:
            checks[name]['link written'] = summary['links'] == [('v9', 'v14', 'first_is_bullish', LINK_SEQ)] and summary['intended_link']
            expected = ['2026-07-10', '2026-07-11', '2026-07-12'] if changed_on.get(('v14', 2)) else ['2026-07-10', '2026-07-12']
            checks[name]['v9 queued by a changed v14 only'] = checks[name]['v9 days'] == expected
        else:
            checks[name]['no link'] = summary['links'] == [] and summary['link_requests_sent'] == []
            checks[name]['v9 only on the stored days'] = checks[name]['v9 days'] == ['2026-07-10', '2026-07-12']
    # the stop paths, each driven through replay with a recording transport
    forwarded = []
    unapproved, _, _ = run_sequence(scratch, 'stop-unapproved-judge', prefix_ledger, V118, False,
                                    dispatcher(fake_judge('stop-unapproved-judge', {}), fake_jev(set()), forwarded), log, also_retire=('v8',))
    checks['stop: an unapproved judge request'] = {
        'stopped on v8': 'unapproved request in judging (thesis v8)' in unapproved['stopped'] or 'thesis v8' in unapproved.get('latch', ''),
        'v8 never forwarded': 'v8' not in unapproved['judge_requests_sent'],
        'nothing judged after 07-10': not any(j['day'] > WINDOW[0] for j in unapproved['judgements'])}
    forwarded = []
    wrong_seq, _, _ = run_sequence(scratch, 'stop-link-other-seq', prefix_ledger, V119, True,
                                   dispatcher(fake_judge('stop-link-other-seq', {}), fake_jev({'v9'}), forwarded), log, link_seq=LINK_SEQ + 1)
    checks['stop: a link request at another sequence'] = {
        'stopped at seq 148': 'unapproved request at seq 148 (link questions)' in wrong_seq['stopped'] + wrong_seq.get('latch', ''),
        'no request forwarded': forwarded == [] and wrong_seq['judge_requests_sent'] == [] and wrong_seq['link_requests_sent'] == []}
    out_of_pair, _, _ = run_sequence(scratch, 'stop-out-of-pair', prefix_ledger, V119, True,
                                     dispatcher(fake_judge('stop-out-of-pair', {}), fake_jev({'v9', 'v1', 'v2', 'v5', 'v6', 'v10', 'v11', 'v12'}), []), log)
    checks['stop: an out-of-pair link'] = {
        'stopped at inspection': out_of_pair['stopped'].startswith('Stop: out-of-pair link'),
        'no judge attempt': out_of_pair['judge_requests_sent'] == [],
        'no item handed over after seq 148': out_of_pair['handovers_after_link_seq'] == 0}
    (scratch / 'dry-checks.json').write_text(json.dumps(checks, indent=1))
    print(json.dumps(checks, indent=1))
    flat = [v for c in checks.values() for v in c.values() if isinstance(v, bool)]
    return all(flat)


# ---------- the other $0 checks ----------

def prefix(scratch):
    """poc-v119 from an empty ledger over 07-01..07-09: link questions answered "neither", every other request from old-2's archive."""
    folder = scratch / 'prefix-v119'
    if folder.exists():
        raise SystemExit(f'{folder} exists')
    folder.mkdir(parents=True)
    shutil.copyfile(OLD2 / 'archive.sqlite', folder / 'archive.sqlite')
    asked = []

    def transport(*args):
        if len(args) == 1 and is_link_request(args[0]):
            asked.append(sorted(args[0]['questions']))
            return fake_jev(set())(args[0])
        raise Stop('a request other than a link question missed the archive')
    replay.run(testdb_path=str(ITEMS), views_path=str(folder / 'views.sqlite'), archive=model.Archive(str(folder / 'archive.sqlite')),
               cfg=config.load(str(V119)), universe=universe.load(str(UNIVERSE)), from_day='2026-07-01', until_day='2026-07-09',
               transport=transport, log=lambda *a: None, only_objects={'NVDA'})
    sys.path.insert(0, str(Path(__file__).parent))
    import rebuild_control
    equal = rebuild_control.compare(folder / 'views.sqlite', PREFIX_SEQ)
    conn = sqlite3.connect(f'file:{folder / "views.sqlite"}?mode=ro', uri=True)
    selections = [(a, s, json.loads(r)) for a, s, r in conn.execute('select attempt_id, status, record_json from link_selections order by id')]
    pairs = [(a, p['candidate'], p['thesis']) for a, s, r in selections if s == 'proposed' for p in r['pairs'] if p.get('eligible') and 'thesis' in p]
    print('link questions asked before 07-10 (answered neither):', len(asked), 'eligible pairs:', pairs)
    return equal


def archive_proof(scratch):
    folder = scratch / 'archive-proof'
    folder.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(OLD2 / 'archive.sqlite', folder / 'archive.sqlite')
    stored = sqlite3.connect(f'file:{OLD2 / "archive.sqlite"}?mode=ro', uri=True)
    rows = {}
    for call_id, request_json in stored.execute("select call_id, request_json from model_calls where purpose='judge' order by call_id"):
        view_id = judged_view(json.loads(request_json))
        rows.setdefault(view_id, (call_id, json.loads(request_json)))
    archive, retired, _ = retire_targets(folder / 'archive.sqlite')
    sent = []

    def recording(provider, request):
        sent.append(judged_view(request))
        data = {'rung': 0, 'reference': '', 'implied_outcome': '', 'reasons': '', 'cites': [], 'cites_views': [], 'pushes': [], 'changed': True,
                'why_changed': '', 'theme_pushes': []}
        return {'choices': [{'message': {'content': json.dumps(data)}}], 'usage': {'prompt_tokens': 1, 'completion_tokens': 1}}
    cfg = config.load(str(V118))
    results = {}
    for view_id in ('v9', 'v14', 'v8'):
        call_id, request = rows[view_id]
        system, user = request['messages'][0]['content'], request['messages'][1]['content']
        schema = request['response_format']['json_schema']['schema']
        answer = model.call(archive, cfg, cfg.rejudging, system, user, schema, 'judgement', 'judge', transport=recording)
        results[view_id] = {'sent to the transport': sent[-1:] == [view_id], 'call id kept': answer.cached and answer.call_id == call_id,
                            'answer call id': answer.call_id}
    archive.retire(results['v9']['answer call id'])           # as round_of_judgements retires an answer its check refuses
    call_id, request = rows['v9']
    before = len(sent)
    model.call(archive, cfg, cfg.rejudging, request['messages'][0]['content'], request['messages'][1]['content'],
               request['response_format']['json_schema']['schema'], 'judgement', 'judge', transport=recording)
    proof = {'retired target rows': retired,
             'an exact old v9 request goes to the transport': results['v9']['sent to the transport'],
             'an exact old v14 request goes to the transport': results['v14']['sent to the transport'],
             'an exact old v8 request is answered from the archive with its call id': results['v8']['call id kept'] and sent.count('v8') == 0,
             'a retired (refused) answer is not returned again': len(sent) == before + 1}
    print(json.dumps(proof, indent=1))
    return all(v for k, v in proof.items() if isinstance(v, bool))


CACHE_WRITE_SHARE = 1.25        # gpt-6-luna page and the prompt-caching guide, read 2026-11-21: cache writes $0.125 per 1M tokens, 1.25x input
JEV_REQUEST_TOKENS = 64000       # TypeSafe's published default per-request limit (docs.typesafe.ai/models, context length), council R round 11


def settled_llm_cost(response, request):
    """The charge at the published rates: uncached input, cached input (0.1x) and cache writes (1.25x) are three disjoint parts of the
    prompt tokens (the guide: "input tokens use the uncached-input, cached-input, or cache-write rate"), plus output; None when the
    usage counts are not whole numbers with some input (the call then stays charged at its reservation)."""
    usage = response.get('usage') if isinstance(response, dict) else None
    if not isinstance(usage, dict):
        return None
    tokens_in, tokens_out = usage.get('prompt_tokens'), usage.get('completion_tokens')
    details = usage.get('prompt_tokens_details') or {}
    cached = details.get('cached_tokens') or 0 if isinstance(details, dict) else None
    written = details.get('cache_write_tokens') or 0 if isinstance(details, dict) else None
    whole = lambda n: isinstance(n, int) and not isinstance(n, bool) and n >= 0
    if not all(whole(n) for n in (tokens_in, tokens_out, cached, written)) or tokens_in == 0:
        return None
    price_in, price_out = model.PRICES[request['model']]
    cached = min(tokens_in, cached)
    written = min(tokens_in - cached, written)
    plain = tokens_in - cached - written
    return (plain * price_in + cached * price_in * model.CACHED_INPUT_SHARE + written * price_in * CACHE_WRITE_SHARE + tokens_out * price_out) / 1e6


def budget_module():
    """The comparison runs' budget transport, with this harness's settlement (cache writes at their published rate) and Jev's
    reservation at its published per-request limit for each of its attempts; the module is loaded for this harness alone."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('budget_replay_july', REPO / 'clean-arch/e2e-comparison-2026-11-13/budget_replay.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.llm_cost = settled_llm_cost
    original_jev_estimate = module.jev_estimate
    module.jev_estimate = lambda request: max(original_jev_estimate(request),
                                              module.jev.ATTEMPTS * JEV_REQUEST_TOKENS * model.PRICES[request['model']][0] / 1e6)
    return module


def bounds():
    """Every reservation the budget transport makes is an upper bound of what it then settles, checked on all of old-2's stored calls:
    a Luna call settles its reported usage at published rates (`llm_cost`), never above `llm_estimate`; a Jev call settles
    ATTEMPTS x reported input tokens, never above `jev_estimate`. With every settlement at or below its reservation, and a reservation
    refused when spent + reserved + it would pass the ceiling, the ledger's spent never passes $0.15."""
    budget = budget_module()
    archive = sqlite3.connect(f'file:{OLD2 / "archive.sqlite"}?mode=ro', uri=True)
    worst = {'judge': 0.0, 'collision judge': 0.0, 'match (Jev)': 0.0}
    counts = {'judge': 0, 'collision judge': 0, 'match (Jev)': 0}
    for purpose, model_name, request_json, response_json, tokens_in in archive.execute(
            "select purpose, model, request_json, response_json, input_tokens from model_calls where purpose in ('judge', 'match')"):
        request = json.loads(request_json)
        if model_name.startswith('jev'):
            if not tokens_in:
                continue
            settled = budget.jev.ATTEMPTS * tokens_in * model.PRICES[model_name][0] / 1e6
            ratio, key = settled / budget.jev_estimate(request), 'match (Jev)'
        else:
            settled = budget.llm_cost(json.loads(response_json), request)
            if settled is None:
                continue
            ratio, key = settled / budget.llm_estimate(request), ('judge' if purpose == 'judge' else 'collision judge')
        counts[key] += 1
        worst[key] = max(worst[key], ratio)
    result = {'calls checked': counts, 'largest settled / reserved': {k: round(v, 4) for k, v in worst.items()},
              'every settlement within its reservation': all(v <= 1 for v in worst.values()) and all(counts.values())}
    print(json.dumps(result, indent=1))
    return result['every settlement within its reservation']


def price():
    stored = sqlite3.connect(f'file:{OLD2 / "archive.sqlite"}?mode=ro', uri=True)
    views = sqlite3.connect(f'file:{OLD2 / "views.sqlite"}?mode=ro', uri=True)
    shas = [r[0] for r in views.execute("select request_sha256 from judgements where view_id in ('v9','v14') and publication_day between ? and ?", WINDOW)]
    price_in, price_out = model.PRICES['gpt-6-luna']
    total, rows = 0.0, []
    for sha in shas:
        tokens_in, tokens_out = stored.execute('select input_tokens, output_tokens from model_calls where request_sha256=?', (sha,)).fetchone()
        cost = tokens_in / 1e6 * price_in + tokens_out / 1e6 * price_out
        rows.append((tokens_in, tokens_out, round(cost, 5)))
        total += cost
    v9 = [r for r, sha in zip(rows, shas) if views.execute("select view_id from judgements where request_sha256=?", (sha,)).fetchone()[0] == 'v9']
    extra_v9 = max(r[2] for r in v9) * 1.1               # a v9 call on 07-11 when v14 changes, with the dependency block (about 700 characters)
    jev_in = model.PRICES['jev-1.14.0'][0]
    jev_calls = 2 * 3 * 20000 * jev_in / 1e6             # two link jobs, Jev's three attempts, a generous 20,000 input tokens each
    linked = total + extra_v9 + jev_calls
    print(json.dumps({'stored v9/v14 judge calls in the window': rows, 'control sequence (uncached)': round(total, 4),
                      'linked sequence, upper estimate (an extra v9 call, two link jobs)': round(linked, 4),
                      'six sequences': round(3 * total + 3 * linked, 4), 'ceiling': CEILING}, indent=1))


ORDER = [('control-1', V118, False), ('linked-1', V119, True), ('control-2', V118, False), ('linked-2', V119, True),
         ('control-3', V118, False), ('linked-3', V119, True)]       # alternated, so a ceiling stop falls on both arms alike


def send(prefix_ledger, out):
    """The paid comparison (run only after the council passed the $0 proof, D694 (c)): six sequences through the shared reservation ledger
    of the comparison runs, one ceiling of $0.15; the ledger is read after each sequence, and a refused reservation or a stop makes the
    comparison inconclusive and ends it."""
    budget = budget_module()
    out.mkdir(parents=True, exist_ok=False)
    ledger_path = out / 'ledger.json'
    budget.SharedLedger.init(str(ledger_path), CEILING)
    ledger = budget.SharedLedger(str(ledger_path))
    remove_gate = budget.install_stop_gate(ledger)
    transport = budget.BudgetTransport(ledger)
    results, outcome = [], 'complete'
    with open(out / 'send.log', 'a', encoding='utf-8') as log_file:
        def log(*parts):
            log_file.write(' '.join(str(p) for p in parts) + '\n')
            log_file.flush()
        try:
            for index, (name, cfg_path, linked) in enumerate(ORDER):
                log(f'--- start {name}')
                try:
                    summary, _, _ = run_sequence(out, name, prefix_ledger, cfg_path, linked, transport, log)
                except BaseException as error:              # a Python exception outside the sequence's own handling (an abrupt kill
                    summary = {'name': name, 'started': True, 'stopped': f'{type(error).__name__}: {error}'[:400], 'comparable': False}
                    outcome = f'stopped: {name} raised before its summary'          # leaves the start log and the ledger for inspection)
                    results.append(summary)
                    results.extend({'name': n, 'started': False} for n, _, _ in ORDER[index + 1:])
                    raise
                state = ledger.read()
                summary['ledger_after'] = state
                results.append(summary)
                log(f'--- finish {name}: stopped={summary["stopped"]!r} comparable={summary["comparable"]} spent ${state["spent"]:.4f} '
                    f'reserved ${state["reserved"]:.4f} refused {state["refused"]}')
                if state.get('stopped') or state.get('refused') or state.get('overrun'):
                    outcome = 'inconclusive: the shared ledger stopped, refused or overran'
                    results.extend({'name': n, 'started': False} for n, _, _ in ORDER[index + 1:])
                    break
                # a sequence that is not comparable stays stopped and is scored as such (the frozen rule counts comparable sequences);
                # the other sequences are independent and go on while the shared ledger allows
        finally:
            remove_gate()
            (out / 'send-summary.json').write_text(json.dumps({'outcome': outcome, 'ledger': ledger.read(), 'sequences': results}, indent=1, ensure_ascii=False))
    print(outcome, ledger.read())


if __name__ == '__main__':
    mode, scratch = sys.argv[1], Path(sys.argv[2])
    scratch.mkdir(parents=True, exist_ok=True)
    if mode == 'prefix':
        sys.exit(0 if prefix(scratch) else 1)
    if mode == 'archive':
        sys.exit(0 if archive_proof(scratch) else 1)
    if mode == 'dry':
        sys.exit(0 if dry(scratch, Path(sys.argv[3])) else 1)
    if mode == 'price':
        price()
        sys.exit(0)
    if mode == 'bounds':
        sys.exit(0 if bounds() else 1)
    if mode == 'send':
        send(Path(sys.argv[3]), Path(sys.argv[4]))
