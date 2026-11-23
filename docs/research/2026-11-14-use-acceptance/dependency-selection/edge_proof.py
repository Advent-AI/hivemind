"""What one dependency edge would do to filing and to judging, on stored data ($0; council round 28, under D439).

The edge: data-center revenue FY2027 (`v4`) depends on total revenue FY2027 (`v2`), written at the article that opened `v4` (13),
as the matching call could have chosen it (PRD 06, D51). Nothing is sent; the stored run is read only; scratch copies take the edge.

Part F, filing. Every stored reading answer of the week is filed again by the production entry point (`extraction.extract`, the
answer taken from the stored archive), once with the day's list as stored (the control: it must reproduce the stored handover) and
once with the list read from a store that holds the edge. The edge reaches filing through `direct_parents` and the narrowest rule
(`extraction.narrowest_links`): a statement linked to a question and to a question it depends on keeps the first only.

Part J, judging. The last day's judging round is run from the stored state before it (rebuilt here from stored answers and
compared with the stored run), with the edge added: every request the stored archive holds is answered from it, the one request that changes is answered by a
labelled fake. Registered expectations fail the script.

  python3 edge_proof.py <scratch folder>          (EDGE_MUTANT=none|reverse: must fail)
"""
import difflib
import json
import os
import re
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, dispatch, extraction, model, replay, testdb, universe  # noqa: E402
from hivemind.views import judging, round as rounds, store  # noqa: E402

RUN = ROOT / 'poc/data/clean-lean-week-2026-11-14/week/p1/prod'
NEW, EARLIER, OPENED_AT, LAST_DAY = 'v4', 'v2', 13, '2026-09-28'
UNRELATED = ('v12', 'v1')                       # the negative case: the Hugging Face commitments question and the financing-commitments question
BLOCK = '[Current conclusions of the theses it depends on]'
HERE = Path(__file__).parent


def refuse(*args, **kwargs):
    raise RuntimeError('a request was not in the stored archive: the network is refused')


def state_before_the_last_round(folder, cfg, uni):
    """The stored week rebuilt from stored answers alone: whole days to the day before the last, then the last day's articles
    without its judging round. Returns what the comparison with the stored run found."""
    folder.mkdir(parents=True)
    shutil.copy(RUN / 'archive.sqlite', folder / 'archive.sqlite')
    archive, items = model.Archive(str(folder / 'archive.sqlite')), str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite')
    replay.run(testdb_path=items, views_path=str(folder / 'views.sqlite'), archive=archive, cfg=cfg, universe=uni, from_day='2026-09-22', until_day='2026-09-27',
               only_objects={'NVDA'}, transport=refuse, log=lambda *parts: None)
    conn = store.open_db(str(folder / 'views.sqlite'))
    for item in testdb.feed(testdb.open_db(items), LAST_DAY, LAST_DAY):
        if not any(o['value'] == 'NVDA' for o in item['object_identifiers']):
            continue
        route = dispatch.route(conn, item, uni)
        if route.kind == 'merged':
            dispatch.mark(conn, item, 0, 'merged', 'ok', route.reason)
            conn.commit()
        elif route.kind == 'extract':
            result = rounds.run(conn, archive, cfg, uni, item, route.sequence_no, resume_from=route.resume_from, transport=refuse, log=lambda *parts: None)
            assert not result.failed, result.failed
    conn.commit()
    stored = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
    last = stored.execute('select max(seq) from days_completed').fetchone()[0]
    same = {name: [tuple(row) for row in conn.execute(query)] == stored.execute(query).fetchall() for name, query in (          # the store's rows are not tuples
        ('questions', 'select view_id, created_seq, question from views order by view_id'), ('statements', 'select evidence_id, created_seq, quote from evidence order by evidence_id'),
        ('links', 'select evidence_id, view_id, seq from evidence_links order by evidence_id, view_id'), ('handovers', 'select input_id, seq, handover_json from handovers order by seq'),
        ('judgements before the last round', f'select view_id, seq, rung, reasons from judgements where seq < {last} order by judgement_id'))}
    same['no judgement of the last round yet'] = conn.execute('select count(*) from judgements where seq >= ?', (last,)).fetchone()[0] == 0
    conn.close()
    return same


def add_edge(conn, view_id, depends_on):
    """The writer's own steps for one chosen dependency (`views/writing.py`): refuse a cycle, then insert."""
    if store.would_cycle(conn, view_id, depends_on):
        return False
    store.insert(conn, 'dependencies', view_id=view_id, depends_on=depends_on, wait_chain_view_id='', wait_year='', direction='first_is_bullish', seq=OPENED_AT)   # the higher end of the earlier question favours the higher end of the new one
    conn.commit()
    return True


def filing(scratch, cfg, uni, edge):
    """Returns {article: {statement id: links}} filed from the stored answers, the day's list read from a store with or without the edge."""
    folder = scratch / ('filing-edge-' + '-'.join(edge) if edge else 'filing-control')
    folder.mkdir(parents=True)
    for name in ('views.sqlite', 'archive.sqlite'):
        shutil.copy(RUN / name, folder / name)
    conn, archive = store.open_db(str(folder / 'views.sqlite')), model.Archive(str(folder / 'archive.sqlite'))
    if edge:
        assert add_edge(conn, *edge)
    articles = {row['input_id']: row['seq'] for row in conn.execute('select input_id, seq from handovers')}
    filed = {}
    for item in testdb.feed(testdb.open_db(str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite')), '2026-09-22', LAST_DAY):
        if item['input_id'] not in articles:
            continue
        objects = [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
        shown = extraction.shown_views(conn, cfg, item, objects)
        handover = extraction.extract(archive, cfg, item, item['text'], shown, uni, transport=refuse)
        filed[articles[item['input_id']]] = {'evidence': {e['id']: (sorted(e['links']), e['one_line']) for e in handover.evidence}, 'dropped': len(handover.dropped), 'candidates': len(handover.candidates)}
    conn.close()
    return filed


def part_f(scratch, cfg, uni):
    stored = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
    control = filing(scratch, cfg, uni, None)
    reproduced = 0
    for input_id, seq, handover_json in stored.execute('select input_id, seq, handover_json from handovers'):
        saved = json.loads(handover_json)
        reproduced += {e['id']: sorted(e['links']) for e in saved['evidence']} == {k: v[0] for k, v in control[seq]['evidence'].items()} and len(saved['dropped']) == control[seq]['dropped']
    out = {'articles': len(control), 'control_reproduces_the_stored_filing': reproduced}
    for name, edge in (('edge', (NEW, EARLIER)), ('unrelated_edge', UNRELATED)):
        with_edge = filing(scratch, cfg, uni, edge)
        changed = []
        for seq in sorted(control):
            assert control[seq]['dropped'] == with_edge[seq]['dropped'] and control[seq]['candidates'] == with_edge[seq]['candidates'], seq
            for statement, (links, one_line) in control[seq]['evidence'].items():
                now = with_edge[seq]['evidence'][statement][0]
                if now != links:
                    changed.append({'article': seq, 'statement': statement, 'links_as_stored': links, 'links_with_the_edge': now, 'home_removed': sorted(set(links) - set(now)), 'summary': one_line})
        out[name] = changed
    return out


def part_j(state, scratch, cfg, mutant):
    work = scratch / 'judging'
    shutil.copytree(state, work)
    conn, archive = store.open_db(str(work / 'views.sqlite')), model.Archive(str(work / 'archive.sqlite'))
    stored = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
    stored_archive = sqlite3.connect(f"file:{RUN / 'archive.sqlite'}?mode=ro", uri=True)
    seq = store.next_sequence(conn) - 1
    facts = {'no cycle before the edge': not store.would_cycle(conn, NEW, EARLIER)}
    if mutant == 'reverse':
        add_edge(conn, EARLIER, NEW)
    elif mutant != 'none':
        facts['the edge is written by the writer\'s own steps'] = add_edge(conn, NEW, EARLIER)
    facts['the reverse edge would now be refused as a cycle'] = store.would_cycle(conn, EARLIER, NEW)
    facts['filing reads the new question as the narrower one'] = store.direct_parents(conn, NEW) == [EARLIER] and store.direct_parents(conn, EARLIER) == []
    facts['a changed conclusion of the earlier question queues the new one'] = NEW in judging.queued_by_change(conn, EARLIER)
    sent = []
    bands = {row['view_id']: store.current_state(conn, row['view_id'])['rung'] for row in conn.execute('select distinct view_id from judgements')}   # read here: the transport runs in other threads

    def fake_for_changed(provider, request):                    # reached only by a request the stored archive does not hold
        user = request['messages'][-1]['content']
        view = re.match(r'Thesis (v\d+) ', user).group(1)
        sent.append((view, user))
        label = f'LABELLED FAKE OUTPUT for {view}'
        answer = {'rung': bands[view], 'reference': label, 'implied_outcome': label, 'reasons': label + ': the edge proof, not a model answer.', 'cites': [], 'cites_views': [EARLIER] if view == NEW else [],
                  'pushes': [], 'changed': False, 'why_changed': '', 'theme_pushes': []}
        return {'choices': [{'message': {'content': json.dumps(answer)}}], 'usage': {'prompt_tokens': 0, 'completion_tokens': 0}, 'synthetic': True}

    result = rounds.judge_day(conn, archive, cfg, LAST_DAY, seq, transport=fake_for_changed, log=lambda *parts: None)
    conn.commit()
    query = 'select view_id, rung, reasons, request_sha256 from judgements where seq = ? order by judgement_id'
    ours, theirs = [tuple(row) for row in conn.execute(query, (seq,))], stored.execute(query, (seq,)).fetchall()
    order = [row[0] for row in ours]
    untouched = {row[0]: row for row in theirs if row[0] != NEW}
    stored_request = json.loads(stored_archive.execute('select request_json from model_calls where request_sha256 = ?', (dict((r[0], r[3]) for r in theirs)[NEW],)).fetchone()[0])['messages'][-1]['content']
    new_request = dict(sent).get(NEW, '')
    added = [line[2:] for line in difflib.ndiff(stored_request.split('\n'), new_request.split('\n')) if line.startswith('+ ')]
    removed = [line[2:] for line in difflib.ndiff(stored_request.split('\n'), new_request.split('\n')) if line.startswith('- ')]
    earlier_conclusion = dict((r[0], r[2]) for r in theirs)[EARLIER]
    line = next((text for text in added if text.startswith(f'- {EARLIER} ')), '')
    facts.update({
        'the round finished without a refusal': not result.failed,
        'the same questions are judged as in the stored round': sorted(order) == sorted(row[0] for row in theirs),
        'the earlier question is judged before the new one': EARLIER in order and NEW in order and order.index(EARLIER) < order.index(NEW),
        'every other judgement equals the stored one (request, band, reasons), the unrelated pair included': all(tuple(row) == tuple(untouched[row[0]]) for row in ours if row[0] != NEW) and all(v in untouched for v in UNRELATED),
        'only the new question\'s request was not in the stored archive': [view for view, _ in sent] == [NEW],
        'its request is the stored one plus the dependency block, with the closing sentence naming dependency ids, and nothing else':
            [text for text in added if text.strip()][:1] == [BLOCK] and len([text for text in added if text.strip()]) == 3 and len(removed) == 1
            and removed[0].startswith('Answer per the JSON schema.') and [text for text in added if text.strip()][2].startswith('Answer per the JSON schema.'),
        'the block shows the earlier question\'s conclusion of this round, its first 600 characters': bool(line) and line.endswith('reasons: ' + earlier_conclusion[:600]),
        'the judge\'s own check accepts an answer that cites the earlier question': dict((r[0], r[1]) for r in ours).get(NEW) is not None and json.loads(conn.execute('select cited_views_json from judgements where view_id = ? and seq = ?', (NEW, seq)).fetchone()[0]) == [EARLIER],
    })
    conn.close()
    return facts, {'order': order, 'added_lines': added, 'removed_lines': removed, 'characters_of_the_line': len(line), 'refusal': result.failed}


def main():
    scratch, mutant = Path(sys.argv[1]), os.environ.get('EDGE_MUTANT', '')
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    cfg, uni = config.load(str(ROOT / 'poc/config/poc-v118.json')), universe.load(str(ROOT / 'poc/universe.json'))
    same = state_before_the_last_round(scratch / 'state', cfg, uni)
    print('the state before the last day\'s round, rebuilt from stored answers, against the stored run:', same)
    if not all(same.values()):
        raise SystemExit(1)
    facts, detail = part_j(scratch / 'state', scratch, cfg, mutant)
    print('Part J, judging on the last day with the edge' + (f' (mutant: {mutant})' if mutant else ''))
    print('  judged, in order:', detail['order'])
    for text in detail['added_lines']:
        print('  added to the request   |', text[:260])
    for text in detail['removed_lines']:
        print('  removed from the request |', text[:260])
    if detail['refusal']:
        print('  the round stopped:', detail['refusal'][:300])
    for name, held in facts.items():
        print(f"  {'ok  ' if held else 'FAIL'} {name}")
    if mutant:
        raise SystemExit(0 if all(facts.values()) else 1)
    filed = part_f(scratch, cfg, uni)
    print(f"\nPart F, filing: {filed['articles']} articles filed again from their stored answers; the control reproduces the stored filing on {filed['control_reproduces_the_stored_filing']}")
    for name in ('edge', 'unrelated_edge'):
        print(f"  with {'the edge' if name == 'edge' else 'an edge between the unrelated pair instead'}: {len(filed[name])} statements change their homes")
        for row in filed[name]:
            print(f"     article {row['article']} {row['statement']}: {row['links_as_stored']} -> {row['links_with_the_edge']} | {row['summary'][:170]}")
    (HERE / 'edge-proof.json').write_text(json.dumps({'judging': {'expectations': facts, **detail}, 'filing': filed}, indent=1, ensure_ascii=False) + '\n')
    filing_ok = filed['control_reproduces_the_stored_filing'] == filed['articles']
    print(f"  {'ok  ' if filing_ok else 'FAIL'} the control reproduces the stored filing of every article")
    if not all(facts.values()) or not filing_ok:
        raise SystemExit(1)
    print('\nPASS: every registered expectation holds (the reading of the changed homes against the filing rule is on the result page, not a check)')


if __name__ == '__main__':
    main()
