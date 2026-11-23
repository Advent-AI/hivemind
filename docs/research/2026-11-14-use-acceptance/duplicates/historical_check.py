"""The $0 check of historical inputs and filing checks for a same-day visibility probe (D522). Nothing is sent and nothing is written
to any run. For each case (the article that opened the second question of a same-day pair):

1. the stored reading request is rebuilt by the production code (`extraction.shown_views`, `extraction.request_for`,
   `model.build_request`) from the article and the run's store read at the day's start, and must have the stored archive key;
2. the same production code builds the list of the questions committed before the article (the store read at the article's own
   sequence minus one: `store.day_start_seq` answers with that number for this one call), and the two lists are compared line by line;
3. the stored answer goes through the production checks and filing (`extraction.sift_with_groups`, `extraction.file_reading`) on the
   day-start list, and must give the stored handover;
4. a synthetic answer (the stored one with the second question's candidate removed and its statements linked to the earlier question)
   goes through the same checks on both lists.

  python3 historical_check.py
"""
import copy
import json
import sqlite3
import sys
import types
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, extraction, model, placement, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

DATA = ROOT / 'poc/data'
CASES = [('week-rtx', DATA / 'clean-lean-week-2026-11-14/week/p1/prod', 'v14', 'v15', 'both reviewing teams: duplicate'),
         ('week-rubin', DATA / 'clean-lean-week-2026-11-14/week/p1/prod', 'v9', 'v11', 'both reviewing teams: duplicate'),
         ('july2-h200', DATA / 'clean-e2e-full-2026-11-13/p2/prod', 'v10', 'v11', 'unsettled: not read by reviewers'),
         ('july3-credit', DATA / 'clean-e2e-full-2026-11-13/p3/prod', 'v1', 'v2', 'unsettled: not read by reviewers')]
HERE = Path(__file__).resolve().parent


def main():
    cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    items_db = testdb.open_db(str(DATA / 'items-nvda-2026-07-01-10-27.sqlite'))
    report = []
    for name, folder, earlier, later, standing in CASES:
        conn = store.open_read_only(str(folder / 'views.sqlite'))
        archive = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        later_row = conn.execute('select created_from_input, created_seq from views where view_id = ?', (later,)).fetchone()
        input_id, item_seq = later_row['created_from_input'], later_row['created_seq']
        day = conn.execute('select publication_day from processing_steps where input_id = ? limit 1', (input_id,)).fetchone()[0]
        item = next((i for i in testdb.feed(items_db, day, day) if i['input_id'] == input_id), None)
        if item is None:
            raise SystemExit(f'{name}: article {input_id} is not in the article database on {day}: refused')
        objects = [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
        stored_sha, stored_answer = archive.execute("select request_sha256, answer_json from model_calls where purpose = 'extract' and request_json like ? order by call_id desc limit 1", (f'%{input_id}%',)).fetchone()
        at_start = extraction.shown_views(conn, cfg, item, objects)
        setting, system, user_start, schema = extraction.request_for(cfg, item, item['text'], at_start, uni)
        rebuilt_sha = model.request_identity(model.build_request(setting, system, user_start, schema, 'extraction', cfg.provider))[1]
        original = store.day_start_seq
        store.day_start_seq = lambda connection, publication_day: item_seq - 1
        try:
            before_item = extraction.shown_views(conn, cfg, item, objects)
            _, _, user_item, _ = extraction.request_for(cfg, item, item['text'], before_item, uni)
        finally:
            store.day_start_seq = original
        lines_start = {v['view_id']: '\n'.join(placement.question_lines([v])) for v in at_start}
        lines_item = {v['view_id']: '\n'.join(placement.question_lines([v])) for v in before_item}
        added = [v for v in lines_item if v not in lines_start]
        changed = [v for v in lines_start if v in lines_item and lines_start[v] != lines_item[v]]
        removed = [v for v in lines_start if v not in lines_item]
        # the stored answer through the production checks on the day-start list: must give the stored handover
        answer = json.loads(stored_answer)
        handle = types.SimpleNamespace(data=answer, call_id=0, request_sha256=stored_sha, cached=True, cost_usd=0.0)

        def through(data, shown):
            evidence, candidates, dropped, new_groups = extraction.sift_with_groups(copy.deepcopy(data), item, item['text'], {v['view_id'] for v in shown}, uni)
            handover = extraction.file_reading(extraction.Reading(evidence, candidates, dropped, new_groups, handle, 'x'), item, shown)
            return ({e['id']: sorted(e['links']) for e in handover.evidence}, [c['id'] for c in handover.candidates], [list(d) for d in handover.dropped])
        kept, candidates, dropped = through(answer, at_start)
        stored_handover = json.loads(conn.execute('select handover_json from handovers where input_id = ? order by id desc limit 1', (input_id,)).fetchone()[0])
        same_handover = (kept == {e['id']: sorted(e['links']) for e in stored_handover['evidence']} and candidates == [c['id'] for c in stored_handover['candidates']]
                         and dropped == [list(d) for d in stored_handover['dropped']])
        # a synthetic answer: the candidate that became the later question removed, its statements linked to the earlier question
        opened = [c for c in answer.get('candidates') or [] if c.get('question') == conn.execute('select question from views where view_id = ?', (later,)).fetchone()[0]]
        synthetic_note = 'the stored answer holds no candidate with the later question\'s exact wording: not exercised'
        if opened:
            gone = opened[0]['id']
            synthetic = copy.deepcopy(answer)
            synthetic['candidates'] = [c for c in synthetic['candidates'] if c['id'] != gone]
            for statement in synthetic['evidence']:
                statement['links'] = [earlier if link == gone else link for link in statement.get('links') or []]
            moved = [s['id'] for s in answer['evidence'] if gone in (s.get('links') or [])]
            kept_item, _, dropped_item = through(synthetic, before_item)
            kept_start, _, dropped_start = through(synthetic, at_start)
            synthetic_note = (f"statements re-linked to {earlier}: {moved}; on the list before the article kept under {earlier}: {[i for i in moved if earlier in kept_item.get(i, [])]}, "
                              f"dropped {[d for d in dropped_item if d[0] in moved]}; on the day-start list kept under {earlier}: {[i for i in moved if earlier in kept_start.get(i, [])]}, "
                              f"dropped {[d for d in dropped_start if d[0] in moved]}")
        row = {'case': name, 'standing': standing, 'article': input_id, 'article_seq': item_seq, 'day': day, 'stored_request_rebuilt_by_production_code': rebuilt_sha == stored_sha,
               'questions_at_day_start': len(lines_start), 'questions_before_the_article': len(lines_item), 'added': added, 'lines_changed_since_day_start': changed,
               'removed': removed, 'earlier_question_lines': lines_item.get(earlier), 'request_characters': [len(user_start), len(user_item)],
               'stored_answer_through_the_checks_gives_the_stored_handover': same_handover, 'synthetic_answer': synthetic_note}
        report.append(row)
        print(f"\n=== {name} ({standing}): article {item_seq} of {day}")
        print(f"  1. stored request rebuilt by the production code from the article and the day-start state: {'the stored key' if rebuilt_sha == stored_sha else 'NOT the stored key'}")
        print(f"  2. questions listed: {len(lines_start)} at the day's start, {len(lines_item)} before the article; added {added}; lines changed {changed}; removed {removed}; request {len(user_start)} -> {len(user_item)} characters")
        print(f"     the earlier question as the production code prints it at that sequence:\n       " + str(lines_item.get(earlier)).replace('\n', '\n       ')[:520])
        print(f"  3. stored answer through sift and filing on the day-start list gives the stored handover: {same_handover}")
        print(f"  4. synthetic answer: {synthetic_note}")
    (HERE / 'historical-check.json').write_text(json.dumps(report, indent=1, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
