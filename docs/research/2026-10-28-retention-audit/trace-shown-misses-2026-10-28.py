"""Reconcile the 49 previously labelled shown-home losses to archived requests and raw placement answers.

Does not judge whether a labelled home is economically correct; input labels remain unchanged.
"""
import collections
import json
import re
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCHIVE = '/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/archive.sqlite'

def read(name):
    return json.loads((HERE / name).read_text())

def main():
    articles = read('ledger.json')['v38']
    selected = [x for x in read('loss-traces-v38.json') if x['cause'] == 'placer_missed_shown_question']
    assert len(selected) == 49 and len({(x['article_no'], x['id']) for x in selected}) == 49
    conn = sqlite3.connect('file:' + ARCHIVE + '?mode=ro', uri=True)
    calls = []
    for call_id, request, answer in conn.execute("select call_id,request_json,answer_json from model_calls where purpose='place' and request_sha256 not like '%:%'"):
        req = json.loads(request)
        calls.append((call_id, req['messages'][1]['content'], json.loads(answer)))
    traced = []
    for case in selected:
        article = articles[case['article_no'] - 1]
        assert article['article_no'] == case['article_no']
        match = [(call_id, user, answer) for call_id, user, answer in calls
                 if user.split('\n', 1)[0].endswith(': ' + article['title'])]
        assert len(match) == 1, case
        call_id, user, answer = match[0]
        questions, statements = user.split('\n\n[Statements]\n', 1)
        blocks = re.findall(r'^  - (v\d+) \([^\n]*\n      [^\n]*', questions, re.M)
        ids_shown = set(blocks)
        assert ids_shown == set(case['shown_homes'])
        wanted = set(case['expected_homes']) & ids_shown
        assert wanted
        lines = [line for line in statements.splitlines() if line.startswith('  - ' + case['id'] + ' [')]
        replies = [x for x in answer['placements'] if x['id'] == case['id']]
        assert len(lines) == len(replies) == 1
        rec = next(r for r in article['records'] if r['id'] == case['id'])
        assert not rec['links'] and not replies[0]['links'] and rec['drop_reason'] == 'no home' and not rec['stored_id']
        question_blocks = re.findall(r'^  - (v\d+) \([^\n]*\n      [^\n]*', questions, re.M)
        full_blocks = re.findall(r'^  - v\d+ \([^\n]*\n      [^\n]*', questions, re.M)
        views = dict(zip(question_blocks, full_blocks))
        traced.append({'article_no': case['article_no'], 'id': case['id'], 'input_id': article['input_id'],
                       'placement_call_id': call_id, 'source_quote': rec['quote'], 'summary': rec['one_line'],
                       'sent_statement': lines[0], 'expected_home_label': sorted(wanted),
                       'shown_question_texts': {k: views[k] for k in sorted(wanted)},
                       'raw_placement': replies[0], 'handover_reason': rec['drop_reason']})
    counts = collections.Counter(x['article_no'] for x in traced)
    result = {'scope': '49 earlier labelled losses; what was actually sent and answered, not validation of the economic labels',
              'count': len(traced), 'all_shown_have_labelled_home': True, 'all_raw_answers_empty': True,
              'all_no_candidate_links': True, 'articles': len(counts), 'by_article': dict(sorted(counts.items())), 'cases': traced}
    path = HERE / 'trace-shown-misses-2026-10-28.json'
    with path.open('x', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}, ensure_ascii=False))

if __name__ == '__main__':
    main()
