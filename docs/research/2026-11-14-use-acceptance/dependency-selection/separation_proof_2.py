"""The second $0 proof of the separation design (council round 30): real writers store the kind, real readers read it, across a
whole week; the two edge combinations; the reading of rows written before a kind was stored.

W1. The seeding module (production), wrapped so that it stores the kind of what it writes, on an empty scratch store.
W2. The unseeded fresh week replayed from its stored answers with one change: at the article that opened the data-center revenue
    question, the matching answer names total revenue as a dependency. The production check accepts it and the production
    writer writes the edge (wrapped: kind `reads` stored). Every reading and matching answer must still come from the stored
    archive; the only requests the archive does not hold are that question's seven judgements, answered by handing back the
    stored answer of the same day (no model is asked).
X.  The two combinations of a `supports` edge with a `reads` edge between the same questions, and a pair of `reads` edges.
M.  Rows written before a kind was stored: the inventory of every stored ledger, and the refusal of a row of neither writer.

  python3 separation_proof_2.py <scratch folder>      (SEPARATION_MUTANT=unseparated|duplicates-written|kind-not-stored: must fail)
"""
import difflib
import json
import os
import re
import shutil
import sqlite3
import sys
import threading
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).parent
sys.path[:0] = [str(ROOT / 'src'), str(HERE), str(HERE.parent / 'dependency-channel')]
from hivemind import config, model, replay, seeding, universe  # noqa: E402
from hivemind.views import jev_matching, store  # noqa: E402
import rebuild_seeded_state  # noqa: E402
import separated_edges  # noqa: E402

FRESH = ROOT / 'poc/data/clean-lean-week-2026-11-14/week/p1/prod'
ITEMS = str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite')
OPENING_ARTICLE, NEW, EARLIER = 'gnews:0f3e2249080cb45434dcabf7', 'v4', 'v2'
BLOCK = '[Current conclusions of the theses it depends on]'


def rows(conn, query, args=()):
    return [tuple(row) for row in conn.execute(query, args)]


def part_w1(scratch, facts):
    conn = store.open_db(str(scratch / 'w1.sqlite'))
    seeding.seed_views(conn, str(ROOT / 'poc/seeds/nvda-2026-07-01-v2.json'), created_at='2026-07-01T00:00:00Z')
    conn.commit()
    edges = rows(conn, 'select dependency_id, view_id, depends_on from dependencies')
    kinds = [separated_edges.stored_kind(conn, edge[0]) for edge in edges]
    views = [row[0] for row in rows(conn, 'select view_id from views')]
    facts['W1: the seeding module wrote 17 edges and stored the kind supports with each'] = len(edges) == 17 and kinds == ['supports'] * 17
    facts['W1: filing reads them as the code does today, for every question'] = all(store.direct_parents(conn, view) == separated_edges._ORIGINAL['direct_parents'](conn, view) for view in views)
    facts['W1: judging reads them the other way (total revenue reads its five supporters; data-center revenue is read by total revenue only)'] = (
        sorted(dep['resolved_to'] for dep in store.dependencies_of(conn, 'v1')) == ['v15', 'v2', 'v3', 'v4', 'v9'] and store.dependants_of(conn, 'v2') == ['v1'])
    conn.close()


def part_w2(scratch, facts, cfg, uni, mutant):
    work = scratch / 'w2'
    work.mkdir()
    shutil.copy(FRESH / 'archive.sqlite', work / 'archive.sqlite')
    stored, stored_archive = sqlite3.connect(f"file:{FRESH / 'views.sqlite'}?mode=ro", uri=True), sqlite3.connect(f"file:{FRESH / 'archive.sqlite'}?mode=ro", uri=True)
    answers = [(seq, json.loads(stored_archive.execute('select request_json, response_json from model_calls where request_sha256 = ?', (sha,)).fetchone()[1]),
                json.loads(stored_archive.execute('select request_json from model_calls where request_sha256 = ?', (sha,)).fetchone()[0])['messages'][-1]['content'])
               for seq, sha in stored.execute('select seq, request_sha256 from judgements where view_id = ? order by judgement_id', (NEW,))]
    handed, lock = [], threading.Lock()

    def transport(*args, **kwargs):                   # reached only by a request the copied archive does not hold
        request = args[1] if len(args) == 2 else None
        name = ((request or {}).get('response_format') or {}).get('json_schema', {}).get('name') if isinstance(request, dict) else None
        user = request['messages'][-1]['content'] if name == 'judgement' else ''
        if name == 'judgement' and user.startswith(f'Thesis {NEW} '):
            with lock:
                handed.append(user)
                return answers[len(handed) - 1][1]    # the stored answer of the same day, handed back: no model is asked
        raise RuntimeError(f'a request the stored archive does not hold, and not a judgement of {NEW} (kind: {name or "matching engine"})')

    original_decide = jev_matching.decide

    def decide(archive, cfg_, conn, item, candidates, *args, **kwargs):
        answer = original_decide(archive, cfg_, conn, item, candidates, *args, **kwargs)
        if item['input_id'] == OPENING_ARTICLE:       # the one change: the matching answer names a dependency for the question it opens
            for candidate in answer.data['candidates']:
                if candidate['outcome'] == 'new':
                    candidate['dependencies'] = [{'view_id': EARLIER, 'wait_chain_view_id': '', 'wait_year': '', 'direction': 'first_is_bullish'}]
        return answer

    jev_matching.decide = decide
    try:
        totals = replay.run(testdb_path=ITEMS, views_path=str(work / 'views.sqlite'), archive=model.Archive(str(work / 'archive.sqlite')), cfg=cfg, universe=uni,
                            from_day='2026-09-22', until_day='2026-09-28', only_objects={'NVDA'}, transport=transport, log=lambda *parts: None)
        outcome = None if not totals.get('failed') else f"failed {totals.get('failed')}"
    except Exception as error:
        outcome = repr(error)[:300]
    finally:
        jev_matching.decide = original_decide
    facts['W2: the whole week replays: every reading and matching answer comes from the stored archive'] = outcome is None
    if outcome:
        print('W2 stopped:', outcome)
        return
    conn = store.open_read_only(str(work / 'views.sqlite'))
    edges = rows(conn, 'select dependency_id, view_id, depends_on, direction, seq from dependencies')
    record = json.loads(conn.execute('select decisions_json, checks_json from match_records where seq = 13').fetchone()[1])
    facts['W2: the production check accepted the dependency and the production writer wrote one edge (data-center revenue to total revenue, at the opening article)'] = (
        not record['refusals'] and [edge[1:] for edge in edges] == [(NEW, EARLIER, 'first_is_bullish', 13)])
    facts['W2: the writer stored the kind reads with the edge'] = bool(edges) and separated_edges.stored_kind(conn, edges[0][0]) == 'reads'
    same = {name: rows(conn, query) == stored.execute(query).fetchall() for name, query in (
        ('questions', 'select view_id, created_seq, question from views order by view_id'), ('statements', 'select evidence_id, created_seq, quote from evidence order by evidence_id'),
        ('links', 'select evidence_id, view_id, seq from evidence_links order by evidence_id, view_id'), ('filings', 'select input_id, seq, handover_json from handovers order by seq'),
        ('other judgements', f"select view_id, seq, rung, reasons, request_sha256 from judgements where view_id != '{NEW}' order by judgement_id"),
        ('its own answers', f"select seq, rung, reasons from judgements where view_id = '{NEW}' order by judgement_id"))}
    facts['W2: questions, statements, links and all 235 filings equal the stored run (the company-wide outlook keeps its total-revenue home)'] = all(same[name] for name in ('questions', 'statements', 'links', 'filings'))
    facts['W2: every judgement of every other question equals the stored one (request, band, reasons)'] = same['other judgements']
    order_ok, lines_ok, shape_ok = [], [], []
    for (seq, _, stored_request), new_request in zip(answers, handed):
        ids = dict((view, number) for number, view in conn.execute('select judgement_id, view_id from judgements where seq = ? and view_id in (?, ?)', (seq, NEW, EARLIER)))
        order_ok.append(ids.get(EARLIER, 10 ** 9) < ids.get(NEW, 0))
        conclusion = stored.execute('select reasons from judgements where view_id = ? and seq = ?', (EARLIER, seq)).fetchone()[0]
        diff = list(difflib.ndiff(stored_request.split('\n'), new_request.split('\n')))
        added, removed = [line[2:] for line in diff if line.startswith('+ ') and line[2:].strip()], [line[2:] for line in diff if line.startswith('- ')]
        shape_ok.append(len(added) == 3 and added[0] == BLOCK and len(removed) == 1 and removed[0].startswith('Answer per the JSON schema.') and added[2].startswith('Answer per the JSON schema.'))
        lines_ok.append(len(added) > 1 and added[1].startswith(f'- {EARLIER} ') and added[1].endswith('reasons: ' + conclusion[:600]))
    facts['W2: the data-center question is judged on the same seven days with the stored answers, each time after total revenue'] = same['its own answers'] and len(handed) == 7 and all(order_ok)
    facts['W2: each of its seven requests is the stored one plus the dependency block and the closing sentence'] = len(shape_ok) == 7 and all(shape_ok)
    facts['W2: the block shows total revenue\'s conclusion of that same round, its first 600 characters, on each of the seven days'] = len(lines_ok) == 7 and all(lines_ok)
    before, after = stored_archive.execute('select count(*) from model_calls').fetchone()[0], sqlite3.connect(work / 'archive.sqlite').execute('select count(*) from model_calls').fetchone()[0]
    facts['W2: the only requests the stored archive did not hold are those seven'] = after - before == 7
    print(f"W2: edge {edges}; the first day's added line: {next((line[2:160] for line in difflib.ndiff(answers[0][2].split(chr(10)), handed[0].split(chr(10))) if line.startswith('+ - ')), None)}")
    conn.close()


def part_x_and_m(scratch, facts):
    state = scratch / 'seeded-state'
    separated_edges.restore()                                 # the stored history is rebuilt as stored, outside the seam
    sys.argv = [sys.argv[0], str(state)]
    rebuild_seeded_state.main()
    separated_edges.install()
    conn = store.open_db(str(state / 'views.sqlite'))
    views = [row[0] for row in rows(conn, 'select view_id from views')]
    seq = store.next_sequence(conn) - 1
    narrower = lambda: {view: store.direct_parents(conn, view) for view in views}
    reading = lambda: {view: sorted(dep['resolved_to'] for dep in store.dependencies_of(conn, view)) for view in views}
    narrower_before, reading_before, count = narrower(), reading(), conn.execute('select count(*) from dependencies').fetchone()[0]
    first = separated_edges.propose(conn, 'v1', 'v2', 'reads', seq)          # total revenue reads data-center revenue: the supports edge already says so
    facts['X: a reads edge in the direction a supports edge already reads is not written, and is reported as a label that cannot be compared (the seed label is undefined); nothing changes for judging or filing'] = (
        first == 'label undefined' and conn.execute('select count(*) from dependencies').fetchone()[0] == count and reading() == reading_before and narrower() == narrower_before)
    facts['X: a reads edge against a supports edge (each would read the other) is refused as a circle'] = separated_edges.propose(conn, 'v2', 'v1', 'reads', seq) == 'cycle'
    written = separated_edges.propose(conn, 'v19', 'v7', 'reads', seq)
    last = conn.execute('select max(dependency_id) from dependencies').fetchone()[0]
    facts['X: a reads edge that closes no circle is written with its kind stored; its opposite is refused; its repeat with the same label is not written'] = (
        written == 'written' and separated_edges.stored_kind(conn, last) == 'reads' and separated_edges.propose(conn, 'v7', 'v19', 'reads', seq) == 'cycle'
        and separated_edges.propose(conn, 'v19', 'v7', 'reads', seq) == 'already read')
    facts['X: the same reading pair proposed with another direction label is refused as a conflict, not dropped as a duplicate'] = (
        separated_edges.propose(conn, 'v19', 'v7', 'reads', seq, direction='last_is_bullish') == 'conflicting label' and conn.execute('select count(*) from dependencies').fetchone()[0] == count + 1)
    facts['X: filing\'s reading is the same after all of it'] = narrower() == narrower_before
    print('X:', first, '|', written, '| what the Vera CPU question reads now:', reading()['v19'], '| what total revenue reads:', reading()['v1'])
    inventory = json.loads((HERE / 'edge-inventory.json').read_text())
    facts[f"M: every dependency row of the {inventory['ledgers_scanned']} ledger files scanned carries one of the two writers' marks ({inventory['rows_by_writer']}; none other)"] = (
        'other' not in inventory['rows_by_writer'] and not inventory['ledgers_with_other_rows'])
    store.insert(conn, 'dependencies', view_id='v3', depends_on='v2', wait_chain_view_id='', wait_year='', direction='first_is_bullish', seq=seq)   # a seed-created question with an article-time row: neither writer's marks
    conn.commit()
    try:
        store.dependencies_of(conn, 'v3')
        refused = False
    except separated_edges.AmbiguousEdge:
        refused = True
    facts['M: a row of neither writer without a stored kind is refused, not guessed'] = refused
    conn.close()


def main():
    scratch, mutant = Path(sys.argv[1]), os.environ.get('SEPARATION_MUTANT', '')
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    cfg, uni = config.load(str(ROOT / 'poc/config/poc-v118.json')), universe.load(str(ROOT / 'poc/universe.json'))
    separated_edges.KIND_NOT_STORED, separated_edges.DUPLICATES_WRITTEN = mutant == 'kind-not-stored', mutant == 'duplicates-written'
    facts = {}
    separated_edges.install_writers()
    separated_edges.install()
    try:
        part_w1(scratch, facts)
        if mutant == 'unseparated':
            separated_edges.restore()
        part_w2(scratch, facts, cfg, uni, mutant)
        if mutant == 'unseparated':
            separated_edges.install()
        try:
            part_x_and_m(scratch, facts)
            facts['X and M: every edge met could be read'] = True
        except separated_edges.AmbiguousEdge as error:          # an edge with no stored kind and neither writer's marks: a registered failure, not a crash
            facts['X and M: every edge met could be read'] = False
            print('X and M stopped:', str(error)[:200])
    finally:
        separated_edges.restore()
        separated_edges.restore_writers()
    print()
    for name, held in facts.items():
        print(f"  {'ok  ' if held else 'FAIL'} {name}")
    if not mutant:
        (HERE / 'separation-proof-2.json').write_text(json.dumps(facts, indent=1, ensure_ascii=False) + '\n')
    if not all(facts.values()):
        raise SystemExit(1)
    print(f'\nPASS: all {len(facts)} registered expectations hold (no model was asked; no package or frozen file changed)')


if __name__ == '__main__':
    main()
