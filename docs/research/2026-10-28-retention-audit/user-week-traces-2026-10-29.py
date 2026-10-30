"""Record source, production requests, and persisted links for user-decided cases."""
import hashlib
import json
import re
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = Path('/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28')

# These associations were reviewed against their full articles. Other articles
# can repeat the event; this is a trace, not an exhaustive event census.
CASES = {
    'growth': [(42, 'e3'), (64, 'e2')],
    'capex': [(42, 'e1'), (42, 'e2'), (64, 'e1'), (94, 'e2'), (96, 'e1'), (96, 'e2')],
    'omniverse': [(33, 'e1'), (33, 'e4'), (33, 'e5')],
    'sharon': [(2, 'e9'), (18, 'e6'), (35, 'e7'), (41, 'e5'), (52, 'e36')],
    'product_progress': [(65, 'e3'), (67, 'e4'), (70, 'e3'), (70, 'e7')],
    'singapore_case_overview': [(15, 'e8'), (17, 'e4'), (21, 'e9'), (91, 'e12')],
}


def main():
    ledger = json.loads((HERE / 'ledger.json').read_text())['v38']
    assert len(ledger) == 98 and sum(len(a['records']) for a in ledger) == 841
    archive = sqlite3.connect(f'file:{DATA / "archive.sqlite"}?mode=ro', uri=True)
    views = sqlite3.connect(f'file:{DATA / "views.sqlite"}?mode=ro', uri=True)
    views.row_factory = sqlite3.Row
    calls = []
    for call_id, request, answer in archive.execute("SELECT call_id, request_json, answer_json FROM model_calls WHERE purpose='place'"):
        user = json.loads(request)['messages'][1]['content']
        calls.append((call_id, user, json.loads(answer)))
    result = {}
    for case, indexes in CASES.items():
        assert len(indexes) == len(set(indexes))
        rows = []
        for number, local_id in indexes:
            article = ledger[number - 1]
            matches = [e for e in article['records'] if e['id'] == local_id]
            assert article['article_no'] == number and len(matches) == 1
            e = matches[0]
            steps = views.execute('SELECT DISTINCT sequence_no FROM processing_steps WHERE input_id=?', (article['input_id'],)).fetchall()
            assert len(steps) == 1
            sequence = steps[0][0]
            matching = [(cid, user, ans) for cid, user, ans in calls if user.split('\n', 1)[0].endswith(': ' + article['title'])]
            assert len(matching) == 1
            call_id, user, answer = matching[0]
            placements = [r for r in answer['placements'] if r['id'] == local_id]
            assert len(placements) <= 1
            stored, links = None, []
            if e['stored_id'] is not None:
                found = views.execute('SELECT * FROM evidence WHERE evidence_id=?', (e['stored_id'],)).fetchall()
                assert len(found) == 1
                stored = dict(found[0])
                assert stored['created_from_input'] == article['input_id'] and stored['created_seq'] == sequence
                links = [dict(x) for x in views.execute('''SELECT el.view_id, el.seq, v.question, v.created_seq
                           FROM evidence_links el JOIN views v ON v.view_id=el.view_id
                           WHERE el.evidence_id=? ORDER BY el.seq, el.view_id''', (e['stored_id'],))]
                assert {x['view_id'] for x in links} == set(e['stored_links'])
            else:
                assert e['final_status'] == 'dropped'
            rows.append({'article_no': number, 'input_id': article['input_id'], 'publication_day': article['day'],
                         'title': article['title'], 'source': article['source'], 'source_sha256': article['source_sha256'],
                         'sequence': sequence, 'extracted': e, 'placement_call_id': call_id,
                         'placement_request': user, 'placement_answer': placements or None,
                         'stored_evidence': stored, 'stored_links_with_dates': links})
        result[case] = rows
    # Lexical search discovers candidates only; the absence is not a semantic
    # exhaustive claim (a record could describe a change without its name).
    pattern = re.compile(r'\bomniverse\b', re.IGNORECASE)
    written_named = [(a['article_no'], e['id']) for a in ledger for e in a['records']
                     if e['final_status'] == 'written' and (pattern.search(e['quote']) or pattern.search(e['one_line']))]
    assert written_named == []
    output = {'scope': 'User-decided cases on saved v38 week; selected related records, not an exhaustive event census',
              'archive_sha256': hashlib.sha256((DATA / 'archive.sqlite').read_bytes()).hexdigest(),
              'ledger_sha256': hashlib.sha256((HERE / 'ledger.json').read_bytes()).hexdigest(),
              'case_counts': {k: len(v) for k, v in result.items()},
              'omniverse_written_exact_name_in_quote_or_summary': written_named,
              'cases': result}
    with (HERE / 'user-week-traces-2026-10-29.json').open('x') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({'case_counts': output['case_counts'], 'written_exact_name': len(written_named)}))


if __name__ == '__main__':
    main()
