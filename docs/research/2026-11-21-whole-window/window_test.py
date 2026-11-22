"""The whole-window measurement of the linking version (poc-v119) against old-2 (poc-v118, 2026-07-01..09-20), D699.

  python3 window_test.py neither <scratch>      # $0: poc-v119 over the whole window, every link question answered "neither", every
                                                #     other request from a copy of old-2's archive; the result must equal old-2
  python3 window_test.py census-dry <scratch>   # $0: the census pass with every eligible pair answered "reads"; must stay old-2
  python3 window_test.py probe-v2-dry / probe-v2   # RETIRED after D705 (the probe's record stays; see RETIRED_PROBE)
  python3 window_test.py v120-replay <scratch> <draw>   # $0: poc-v120 with probe draw <draw>'s own answers by request hash
  python3 window_test.py census <scratch> <draw> <ledger> <approved ceiling>   # paid (Jev only, at most $0.10, the ceiling Alex
                                                #     names): the same pass with each link job sent to Jev and no link written, so the
                                                #     replay stays old-2; one draw of the link decisions

The `neither` pass proves that poc-v119 without links is old-2 over all 1,884 articles (DESIGN.md table 3, first row, extended from the
July prefix to the whole window), and lists every link question the version would ask: each opening of a number question with the
number questions it was shown, the pairs eligible under D695, and the pairs not eligible with their reason.
"""
import json
import math
import shutil
import sqlite3
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
JULY = REPO / 'docs/research/2026-11-20-production-readiness/dependency-design'
sys.path.insert(0, str(REPO / 'src'))
sys.path.insert(0, str(JULY))
from hivemind import config, live_lock, model, replay, universe       # noqa: E402
from hivemind.views import links                           # noqa: E402
import july_test                                            # noqa: E402
import rebuild_control                                      # noqa: E402

HERE = Path(__file__).resolve().parent

OLD2 = july_test.OLD2
ITEMS = july_test.ITEMS
V119 = july_test.V119
UNIVERSE = july_test.UNIVERSE
WINDOW = ('2026-07-01', '2026-09-20')


def refused_rows():
    """old-2's answers its own run refused (the archive keeps them under the request's hash with a ':refused:' suffix, so no later
    identical request is answered with them): {request hash: stored provider response}. A replay must meet each refusal again to
    reach the stored retry."""
    stored = sqlite3.connect(f'file:{OLD2 / "archive.sqlite"}?mode=ro', uri=True)
    return {sha.split(':refused:')[0]: json.loads(response) for sha, response in
            stored.execute("select request_sha256, response_json from model_calls where request_sha256 like '%:refused:%' order by call_id")}


def replay_window(folder, link_answer, cfg_path=V119):
    """poc-v119 from an empty ledger over the whole window: link questions go to `link_answer`; every other request must be answered
    from the copy of old-2's archive (an answer old-2's own run refused is given back once, so the check refuses it again); anything
    else stops the pass. Returns the census: equality with old-2, every link job, every opening with its pairs."""
    if folder.exists():
        raise SystemExit(f'{folder} exists: a pass starts from an empty folder')
    folder.mkdir(parents=True)
    shutil.copyfile(OLD2 / 'archive.sqlite', folder / 'archive.sqlite')
    views = folder / 'views.sqlite'
    marker = sqlite3.connect(views)                 # marked harness-only before the first item: ordinary writers refuse it (D694 §0)
    marker.execute('create table harness_only (name text, day text)')
    marker.execute("insert into harness_only values ('window_test.py', '2026-11-21')")
    marker.commit()
    marker.close()
    held = live_lock.acquire(str(views))            # the store lock for the whole pass: no second writer
    asked, refused_again = [], []
    stored_refusals = refused_rows()

    def transport(*args):
        if len(args) == 1 and july_test.is_link_request(args[0]):
            asked.append(sorted(args[0]['questions']))
            return link_answer(args[0])
        response = stored_refusals.pop(model.request_identity(args[-1])[1], None)
        if response is not None:                   # old-2's own run refused this answer: give it back, so the check refuses it again
            refused_again.append(model.request_identity(args[-1])[1][:12])
            return response
        (folder / 'missed-request.json').write_text(json.dumps(args[-1], ensure_ascii=False, indent=1))
        raise july_test.Stop('a request other than a link question missed the archive')
    started = time.time()
    try:
        totals = replay.run(testdb_path=str(ITEMS), views_path=str(views), archive=model.Archive(str(folder / 'archive.sqlite')),
                            cfg=config.load(str(cfg_path)), universe=universe.load(str(UNIVERSE)), from_day=WINDOW[0], until_day=WINDOW[1],
                            transport=transport, log=lambda *a: None, only_objects={'NVDA'})
    finally:
        live_lock.release(held)
    print('totals:', totals, 'seconds:', round(time.time() - started))
    conn = sqlite3.connect(f'file:{folder / "views.sqlite"}?mode=ro', uri=True)
    last_seq = conn.execute('select max(seq) from days_completed').fetchone()[0]
    stored_last = sqlite3.connect(f'file:{OLD2 / "views.sqlite"}?mode=ro', uri=True).execute('select max(seq) from days_completed').fetchone()[0]
    print('last completed seq', last_seq, 'old-2', stored_last)
    equal = last_seq == stored_last and rebuild_control.compare(folder / 'views.sqlite', last_seq)
    openings = []
    for attempt, seq, status, record_json in conn.execute('select attempt_id, seq, status, record_json from link_selections order by id'):
        record = json.loads(record_json)
        if status == 'proposed' and record.get('pairs'):
            openings.append({'attempt': attempt, 'seq': seq, 'pairs': record['pairs'], 'calls': record.get('calls', []),
                             'proposed': record.get('proposed', []), 'corrections': record.get('corrections', [])})
    census = {'equal to old-2': equal, 'link jobs asked': len(asked), 'questions in them': sum(len(a) for a in asked),
              "old-2's refused answers met again": refused_again, 'left unmet': sorted(sha[:12] for sha in stored_refusals),
              'link rows written': conn.execute("select count(*) from dependencies where kind='reads'").fetchone()[0],
              'openings with a pair shown': openings}
    (folder / 'census.json').write_text(json.dumps(census, indent=1))
    print(json.dumps({k: v for k, v in census.items() if k != 'openings with a pair shown'}, indent=1))
    for opening in openings:
        eligible = [p['thesis'] for p in opening['pairs'] if p.get('eligible')]
        print(opening['seq'], 'eligible', eligible, 'not eligible', len(opening['pairs']) - len(eligible))
    return census


def neither(scratch):
    return replay_window(scratch / 'neither-v119', july_test.fake_jev(set()))['equal to old-2']


CENSUS_CEILING = 0.10


class Everything:
    def __contains__(self, item):
        return True


def without_links(run):
    """Run `run()` with the writer handed no proposed link (the census's only change to the product path)."""
    from hivemind.views import writing
    original_write = writing.write

    def write_without_links(*args, **keywords):
        keywords['proposed_links'] = None
        return original_write(*args, **keywords)
    writing.write = write_without_links
    try:
        return run()
    finally:
        writing.write = original_write


def complete(result):
    """A draw counts only when it asked every registered pair and finished each stage: the READS answers per opening are exactly the
    eligible pairs of the `neither` pass, every READS answer that passed (a reading direction at 0.5 or more) has its SIGN answer, and
    every Jev job was answered. Returns (complete, problems)."""
    expected = {(o['seq'], p['thesis']) for o in json.loads((HERE / 'neither-census.json').read_text())['openings with a pair shown']
                for p in o['pairs'] if p.get('eligible')}
    problems, reads, signs = [], set(), set()
    for opening in result['openings with a pair shown']:
        for pair in opening['pairs']:
            if 'reads' in pair:
                reads.add((opening['seq'], pair['thesis']))
                choice = pair['reads']
                if choice != links.NEITHER and pair['probabilities'].get(choice, 0) >= links.THRESHOLD:
                    signs.add((opening['seq'], pair['thesis']))
        answered_signs = {(opening['seq'], p['thesis']) for p in opening['pairs'] if 'sign' in p}
        missing = {s for s in signs if s[0] == opening['seq']} - answered_signs
        if missing:
            problems.append(f'seq {opening["seq"]}: no SIGN answer for {sorted(missing)}')
        problems += [f'seq {opening["seq"]}: a job {c.get("stage")} ended {c.get("status")}' for c in opening['calls'] if c.get('status') != 'answered']
    if reads != expected:
        problems.append(f'READS pairs differ from the registered manifest: missing {sorted(expected - reads)}, extra {sorted(reads - expected)}')
    return not problems, problems


def census_dry(scratch):
    """$0: the census pass with a fake Jev that answers every eligible pair "the THESIS reads the CANDIDATE", sign together (the
    largest number of proposals); with the writer handed no link, the pass must still end equal to old-2 with no link row, and the
    draw must be complete (every registered READS pair, a SIGN answer for each)."""
    result = without_links(lambda: replay_window(scratch / 'census-dry', july_test.fake_jev(Everything())))
    proposed = sum(len(o['proposed']) for o in result['openings with a pair shown'])
    whole, problems = complete(result)
    print('links proposed by the fake answers:', proposed, 'complete:', whole, problems)
    return result['equal to old-2'] and result['link rows written'] == 0 and proposed == 105 and whole


def census(scratch, draw, ledger_path, approved):
    """One draw of the link decisions over the window: each link job sent to Jev as poc-v119 builds it, through the comparison runs'
    reservation ledger (`july_test.budget_module`: Jev reserved at its published 64K limit for each of its three attempts); the
    writer is handed no proposed link, so no link row is written and every later request stays old-2's (the pass checks equality at the
    end). The ledger is created beforehand with the ceiling Alex approved; each draw registers its launcher, so the stop gate stops
    every draw when one dies. A draw is counted only when it is complete and the ledger never stopped."""
    budget = july_test.budget_module()
    if not (isinstance(approved, float) and math.isfinite(approved) and 0 < approved <= CENSUS_CEILING):
        raise SystemExit(f'the approved ceiling must be a finite amount above 0 and at most ${CENSUS_CEILING}')
    if not Path(ledger_path).exists():
        raise SystemExit('the ledger does not exist: create it first (budget_replay.py --init-ledger L --ceiling <approved>)')
    ledger = budget.SharedLedger(str(ledger_path))
    ceiling = ledger.read()['ceiling']
    if not (isinstance(ceiling, (int, float)) and math.isfinite(ceiling) and ceiling == approved):
        raise SystemExit(f'the ledger ceiling {ceiling!r} is not the approved ${approved}: refused')
    label = f'census-{draw}'
    lock_handle = open(Path(ledger_path).with_name(f'{label}.launcher.lock'), 'a+')
    if not ledger.claim_launcher(label, lock_handle):
        raise SystemExit(f'another launch of {label} is running')
    budget.install_stop_gate(ledger)
    try:
        return census_pass(scratch / label, draw, budget.BudgetTransport(ledger), ledger.read, 'paid')
    finally:
        ledger.remove_launcher(label)


JULY_SEQ = 148
JULY_HASHES = {'6dcb76643aea831174f8c0811f5f9329ebf5ac60f072a6be4f6992fac2e698a1',     # READS, v14's opening against v1, v2, v8, v9
               'd118a387e9861b93b1d19c79dc9d46f18f78c06b8e7243aa33940f269c9d81a2'}     # SIGN, v9


def census_pass(folder, draw, inner, ledger_state, transport_kind, stored=None):
    """One census draw into `folder`: the seq-148 jobs answered by this draw's July sample, every other link job by `inner`, the writer
    handed no link. A link job at seq 148 whose request is not one of the two pinned July requests stops the pass before `inner`
    (nothing is bought there). Writes `draw.json` with the transport kind ('paid' or 'dry'); the draw is counted only when it is
    complete, reused both July answers, ended equal to old-2 with no link row, and the ledger neither stopped nor overran."""
    from hivemind.views import round as round_module
    stored = july_answers(draw) if stored is None else stored
    reused, current = [], {'seq': None}

    def link_answer(request):
        sha = model.request_identity(request)[1]
        if sha in stored:                          # the July sample of this draw for the same request (seq 148): not bought again
            reused.append(sha[:12])
            return stored[sha]
        if current['seq'] == JULY_SEQ:
            raise july_test.Stop(f'a link job at seq {JULY_SEQ} is not one of the pinned July requests ({sha[:12]}): not sent')
        return inner(request)
    original_run = round_module.run

    def run_noting_seq(conn, archive, cfg, uni, item, seq, *args, **keywords):
        current['seq'] = seq
        return original_run(conn, archive, cfg, uni, item, seq, *args, **keywords)
    round_module.run = run_noting_seq
    try:
        result = without_links(lambda: replay_window(folder, link_answer))
    finally:
        round_module.run = original_run
    state = ledger_state()
    whole, problems = complete(result)
    if sorted(reused) != sorted(sha[:12] for sha in stored):
        whole, problems = False, problems + [f'July samples reused {reused}, expected {sorted(sha[:12] for sha in stored)}']
    counted = result['equal to old-2'] and result['link rows written'] == 0 and whole and not state.get('stopped') and not state.get('overrun')
    (folder / 'draw.json').write_text(json.dumps({'draw': draw, 'transport': transport_kind, 'counted': counted, 'complete': whole, 'problems': problems,
                                                  'equal to old-2': result['equal to old-2'], 'july samples reused': reused,
                                                  'ledger': state}, indent=1))
    print('ledger:', state, 'complete:', whole, problems, 'july reused:', reused)
    return counted


def census_reuse_dry(scratch):
    """$0: a census draw whose bought jobs are answered "neither" by a fake Jev: the seq-148 jobs must be answered by draw 1's July
    sample (both reused), the draw complete and counted, and the record must show v9 reads v14 proposed at seq 148."""
    counted = census_pass(scratch / 'census-reuse-dry', '1', july_test.fake_jev(set()), lambda: {'stopped': False, 'overrun': False}, 'dry')
    conn = sqlite3.connect(f'file:{scratch / "census-reuse-dry" / "views.sqlite"}?mode=ro', uri=True)
    proposed = [json.loads(r)['proposed'] for (r,) in conn.execute("select record_json from link_selections where status='proposed' and seq=148")]
    print('seq 148 proposed:', proposed)
    return counted and proposed and len(proposed[0]) == 1


JULY_DRAWS = {'1': 'linked-1', '2': 'linked-2', '3': 'linked-3'}


def july_answers(draw):
    """The July test's answers to the seq-148 link jobs (READS, call 8738; SIGN, call 8739) of the linked sequence paired with this
    draw: {request hash: stored Jev response}. The census rebuilds the same READS request (sha 6dcb7664…); the SIGN request matches
    when the READS answer passes the same pairs, which the reused answer guarantees."""
    if draw not in JULY_DRAWS:
        raise SystemExit(f'draw must be one of {sorted(JULY_DRAWS)} (each reuses one July sequence\'s seq-148 answers)')
    archive = sqlite3.connect(f'file:{REPO / "poc/data/july-link-test-2026-11-21" / JULY_DRAWS[draw] / "archive.sqlite"}?mode=ro', uri=True)
    return pinned({sha: json.loads(response) for sha, response in
                   archive.execute('select request_sha256, response_json from model_calls where call_id in (8738, 8739)')})


def pinned(stored):
    """The July answers, refused unless they are exactly the two pinned requests (checked before anything is sent)."""
    if set(stored) != JULY_HASHES:
        raise SystemExit(f'the July answers are not the two pinned requests: {sorted(s[:12] for s in stored)}')
    return stored


def reuse_refusals(scratch):
    """$0: (1) a July loader missing one pinned row is refused before anything runs; (2) a seq-148 link job whose request is not
    pinned stops the pass before the inner transport (the pass is given draw 1's SIGN answer only, so the seq-148 READS job is
    unpinned); the inner transport records every call it receives."""
    full = july_answers('1')
    one = {sha: answer for sha, answer in full.items() if sha.startswith('d118')}
    try:
        pinned(one)
        loader = 'NOT REFUSED'
    except SystemExit as error:
        loader = f'refused: {error}'
    received = []

    def recording(request):
        received.append(sorted(request['questions']))
        return july_test.fake_jev(set())(request)
    try:
        census_pass(scratch / 'reuse-refusal', '1', recording, lambda: {'stopped': False, 'overrun': False}, 'dry', stored=one)
        stop = 'NOT STOPPED'
    except july_test.Stop as error:
        stop = f'stopped: {error}'
    except RuntimeError as error:                   # replay.run wraps a failed item's stop
        stop = f'stopped: {error}'
    at_148 = [q for q in received if 'reads__v9' in q]
    print(json.dumps({'loader missing a pinned row': loader, 'unpinned seq-148 job': stop,
                      'seq-148 READS job reached the inner transport': bool(at_148), 'inner calls before the stop': len(received)}, indent=1))
    return loader.startswith('refused') and stop.startswith('stopped') and not at_148



# ---------- version 2 of the link question (WORDING-V2.md, D703): a harness-only probe ----------

V2_TIE_BREAK = (" When either question could be judged with the other in view, the one whose answer the supplied text anchors less (no "
                "guidance, consensus or reported figure for the quantity and full period the question asks about) is the one judged "
                "with the other's conclusion in view.")
V2_PERIODS = (" or quantities of different periods when the supplied text does not state how one period's answer moves the other's (a "
              "retailer's sales this year and its sales growth next year, when the text only names both);")
V2_BASE = "; one year's sales and the next year's sales growth at a given next-year level, since a higher base lowers the growth)"


def wording_v2():
    """The version-2 READS and SIGN criteria: the current texts with the three changes of WORDING-V2.md §2 (each anchored on a unique
    phrase of the current text, so a moved text fails loudly)."""
    reads, sign = dict(links.READS), dict(links.SIGN)
    reads[links.CANDIDATE_READS] = reads[links.CANDIDATE_READS] + V2_TIE_BREAK
    anchor = "for the same period and scope;"
    assert reads[links.NEITHER].count(anchor) == 1
    reads[links.NEITHER] = reads[links.NEITHER].replace(anchor, "for the same period and scope," + V2_PERIODS)
    tail = "a retailer's markdowns and its gross margin)"
    assert sign[links.OPPOSITE].endswith(tail)
    sign[links.OPPOSITE] = sign[links.OPPOSITE][:-1] + V2_BASE
    return reads, sign


def with_wording_v2(run):
    reads, sign = wording_v2()
    original = links.READS, links.SIGN
    links.READS, links.SIGN = reads, sign
    try:
        return run()
    finally:
        links.READS, links.SIGN = original


def probe_pass(folder, draw, inner, ledger_state, transport_kind):
    """One version-2 draw into `folder`: every link job asked with the version-2 texts (none matches a July request, so all are sent to
    `inner`), the writer handed no link. Every request must carry the version-2 texts (checked as it is sent). Writes `draw.json`; the
    draw is counted only when it is complete, ended equal to old-2 with no link row, and the ledger neither stopped nor overran."""
    reads, sign = wording_v2()
    carried = []

    def link_answer(request):
        texts = [q['criteria'] for q in request['questions'].values()]
        expected = reads if next(iter(request['questions'])).startswith('reads__') else sign
        if any(criteria != {k: v for k, v in expected.items() if k in criteria} for criteria in texts):
            raise july_test.Stop('a link job does not carry the version-2 criteria: not sent')
        carried.append(len(texts))
        return inner(request)
    result = with_wording_v2(lambda: without_links(lambda: replay_window(folder, link_answer)))
    state = ledger_state()
    whole, problems = complete(result)
    counted = result['equal to old-2'] and result['link rows written'] == 0 and whole and bool(carried) and not state.get('stopped') and not state.get('overrun')
    (folder / 'draw.json').write_text(json.dumps({'draw': draw, 'wording': 'v2', 'transport': transport_kind, 'counted': counted,
                                                  'complete': whole, 'problems': problems, 'equal to old-2': result['equal to old-2'],
                                                  'jobs carrying version 2': len(carried), 'ledger': state}, indent=1))
    print('ledger:', state, 'complete:', whole, problems, 'jobs carrying version 2:', len(carried))
    return counted


RETIRED_PROBE = ('retired after D705: links.py now builds version 2 itself (poc-v120, `matching.link_questions` links-v2) and its '
                 'builders read QUESTION_SETS, so patching links.READS / links.SIGN no longer changes a request; the probe draws stay '
                 'the record, and `v120-replay` proves the product builds their bytes')


def probe_v2_dry(scratch):
    """$0: the version-2 pass with every pair answered "reads", sign together: complete, equal to old-2, every job carrying the
    version-2 texts, 105 proposals."""
    counted = probe_pass(scratch / 'probe-v2-dry', 'dry', july_test.fake_jev(Everything()), lambda: {'stopped': False, 'overrun': False}, 'dry')
    conn = sqlite3.connect(f'file:{scratch / "probe-v2-dry" / "views.sqlite"}?mode=ro', uri=True)
    proposed = sum(len(json.loads(r)['proposed']) for (r,) in conn.execute("select record_json from link_selections where status='proposed'"))
    print('proposals:', proposed)
    return counted and proposed == 105


def probe_v2(scratch, draw, ledger_path, approved):
    """One paid version-2 draw on D700's ledger (the same checks as `census`: approved finite ceiling equal to the ledger's, launcher
    registered, stop gate installed)."""
    budget = july_test.budget_module()
    if not (isinstance(approved, float) and math.isfinite(approved) and 0 < approved <= CENSUS_CEILING):
        raise SystemExit(f'the approved ceiling must be a finite amount above 0 and at most ${CENSUS_CEILING}')
    ledger = budget.SharedLedger(str(ledger_path))
    ceiling = ledger.read()['ceiling']
    if not (isinstance(ceiling, (int, float)) and math.isfinite(ceiling) and ceiling == approved):
        raise SystemExit(f'the ledger ceiling {ceiling!r} is not the approved ${approved}: refused')
    if draw not in ('1', '2', '3'):
        raise SystemExit('draw must be 1, 2 or 3')
    label = f'probe-v2-{draw}'
    lock_handle = open(Path(ledger_path).with_name(f'{label}.launcher.lock'), 'a+')
    if not ledger.claim_launcher(label, lock_handle):
        raise SystemExit(f'another launch of {label} is running')
    budget.install_stop_gate(ledger)
    try:
        return probe_pass(scratch / label, draw, budget.BudgetTransport(ledger), ledger.read, 'paid')
    finally:
        ledger.remove_launcher(label)


V120 = REPO / 'poc/config/poc-v120.json'


def probe_answers(draw):
    """The link jobs a version-2 probe draw sent and their answers: {request hash: stored Jev response}."""
    archive = sqlite3.connect(f'file:{REPO / "poc/data/link-census-2026-11-21" / f"probe-v2-{draw}" / "archive.sqlite"}?mode=ro', uri=True)
    top = sqlite3.connect(f'file:{OLD2 / "archive.sqlite"}?mode=ro', uri=True).execute('select max(call_id) from model_calls').fetchone()[0]
    out = {}
    for sha, request_json, response_json in archive.execute('select request_sha256, request_json, response_json from model_calls where call_id > ?', (top,)):
        if july_test.is_link_request(json.loads(request_json)):
            out[sha] = json.loads(response_json)
    return out


def v120_replay(scratch, draw):
    """$0: the product configuration poc-v120 over the whole window, its link jobs answered only by the probe draw's own answers
    matched by request hash (a job the probe did not send stops the pass), the writer handed no link as in the probe: every probe job
    must be met, nothing else asked, and the pass must end equal to old-2. This proves the product's version-2 requests are the bytes
    the probe sent."""
    stored, met = probe_answers(draw), []

    def link_answer(request):
        sha = model.request_identity(request)[1]
        if sha not in stored:
            raise july_test.Stop(f'poc-v120 built a link job the probe did not send ({sha[:12]})')
        met.append(sha)
        return stored[sha]
    result = without_links(lambda: replay_window(scratch / f'v120-replay-{draw}', link_answer, V120))
    every = sorted(met) == sorted(stored) and len(set(met)) == len(met)
    print(json.dumps({'draw': draw, 'probe jobs': len(stored), 'met': len(met), 'every probe job met once': every,
                      'equal to old-2': result['equal to old-2'], 'link rows written': result['link rows written']}, indent=1))
    return every and result['equal to old-2'] and result['link rows written'] == 0

if __name__ == '__main__':
    command, scratch = sys.argv[1], Path(sys.argv[2])
    if command == 'neither':
        sys.exit(0 if neither(scratch) else 1)
    if command == 'census-dry':
        sys.exit(0 if census_dry(scratch) else 1)
    if command == 'census-reuse-dry':
        sys.exit(0 if census_reuse_dry(scratch) else 1)
    if command == 'reuse-refusals':
        sys.exit(0 if reuse_refusals(scratch) else 1)
    if command == 'v120-replay':
        sys.exit(0 if v120_replay(scratch, sys.argv[3]) else 1)
    if command in ('probe-v2-dry', 'probe-v2'):
        raise SystemExit(RETIRED_PROBE)
    if command == 'census':
        sys.exit(0 if census(scratch, sys.argv[3], Path(sys.argv[4]), float(sys.argv[5])) else 1)
    raise SystemExit(f'unknown command {command}')
