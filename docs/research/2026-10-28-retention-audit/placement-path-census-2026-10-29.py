"""Count candidate and placement routes in stored v38 answers, without value labels."""
import collections
import json
import re
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCHIVE = '/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/archive.sqlite'


def main():
    articles = json.loads((HERE / 'ledger.json').read_text())['v38']
    archive = sqlite3.connect(f'file:{ARCHIVE}?mode=ro', uri=True)
    rows = []
    calls = 0
    for call_id, request, answer in archive.execute("SELECT call_id,request_json,answer_json FROM model_calls WHERE purpose='place' AND request_sha256 NOT LIKE '%:%'"):
        calls += 1
        user = json.loads(request)['messages'][1]['content']
        head, body = user.split('\n\n[Statements]\n', 1)
        matches = [a for a in articles if head.splitlines()[0].endswith(': ' + a['title'])]
        assert len(matches) == 1, (call_id, len(matches))
        article = matches[0]
        ids = re.findall(r'^  - (e\d+) \[', body, re.M)
        assert ids and len(ids) == len(set(ids))
        allowed = set(re.findall(r'^  - (v\d+) \(', head, re.M))
        placements = json.loads(answer)['placements']
        assert len({p['id'] for p in placements}) == len(placements)
        assert {p['id'] for p in placements} <= set(ids)
        assert all(set(p['links']) <= allowed for p in placements)
        decided = {p['id']: p['links'] for p in placements}
        records = {e['id']: e for e in article['records']}
        for ident in ids:
            e = records[ident]
            candidate = [x for x in e['final_links'] if re.fullmatch(r'c\d+', x)]
            assert set(candidate) <= set(e['links'])
            result = decided.get(ident)
            final_views = [x for x in e['final_links'] if re.fullmatch(r'v\d+', x)]
            assert set(final_views) == set(result or []), (article['article_no'], ident)
            rows.append({'article_no': article['article_no'], 'input_id': article['input_id'], 'id': ident,
                         'placement_call_id': call_id, 'candidate_links': candidate,
                         'placement_links': result, 'final_status': e['final_status'],
                         'stored_id': e['stored_id'], 'stored_links': e['stored_links'],
                         'one_line': e['one_line']})
    assert calls == 95 and len(rows) == 831 and len({(r['input_id'], r['id']) for r in rows}) == 831
    known = {(r['article_no'], r['id']): r for r in rows}
    assert known[(70, 'e7')]['candidate_links'] and known[(70, 'e7')]['placement_links'] == [] and known[(70, 'e7')]['final_status'] == 'written'
    assert not known[(65, 'e3')]['candidate_links'] and known[(65, 'e3')]['placement_links'] == [] and known[(65, 'e3')]['final_status'] == 'dropped'
    assert known[(86, 'e5')]['placement_links'] is None
    counts = collections.Counter((bool(r['candidate_links']), 'missing' if r['placement_links'] is None else bool(r['placement_links']), r['final_status']) for r in rows)
    output = {'scope': '95 stored v38 placement requests and their 831 input records; no assessment of investment value or suitable destination',
              'routes': [{'has_candidate': c, 'placement': p, 'final_status': s, 'count': n}
                         for (c, p, s), n in sorted(counts.items(), key=lambda x: str(x[0]))], 'rows': rows}
    with (HERE / 'placement-path-census-2026-10-29.json').open('x') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps(output['routes'], ensure_ascii=False))


if __name__ == '__main__':
    main()
