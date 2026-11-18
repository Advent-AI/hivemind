"""Sizing the missing-input mechanism, step 1 ($0; D530): for each settled unsupported answer of the census (D519), the statements that
existed in that run's store by the judgement's sequence, were NOT printed in the judge's request, and match a pattern for the matter
the question asks about. A search by pattern only lists candidates for reading: it shows neither relevance nor a cause. Read-only.

  python3 search_missing_inputs.py <folder holding the two reading keys>
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

DATA = Path('/Users/lchingen/hivemind/poc/data')
MONEY = r'(\$\s?\d[\d.,]*\s?(billion|million|trillion|bn|B|M)\b|\d[\d.,]*\s?(billion|million|trillion)\s?(US )?dollars?)'
FINANCING = rf'(backstop|guarantee|credit[- ]support|financing commitment|repurchase)[^\n]{{0,160}}{MONEY}|{MONEY}[^\n]{{0,160}}(backstop|guarantee|credit[- ]support|financing commitment)'
CUSTOM = rf'(Broadcom|custom (AI )?(chip|silicon|accelerator|ASIC)|\bTPU\b|Trainium|MTIA|Maia)[^\n]{{0,200}}{MONEY}|{MONEY}[^\n]{{0,200}}(Broadcom|custom (AI )?(chip|silicon|accelerator|ASIC)|\bTPU\b|Trainium|MTIA|Maia)'
CASES = [
    ('baseline d1 v9 #5', 'baseline', 'd1', 'v9', 5, DATA / 'clean-unseeded-2026-11-10/draw-d1/judged', FINANCING),
    ('baseline d3 v9 #1', 'baseline', 'd3', 'v9', 1, DATA / 'clean-unseeded-2026-11-10/draw-d3/judged', FINANCING),
    ('baseline d3 v9 #5', 'baseline', 'd3', 'v9', 5, DATA / 'clean-unseeded-2026-11-10/draw-d3/judged', FINANCING),
    ('baseline d2 v16 #1', 'baseline', 'd2', 'v16', 1, DATA / 'clean-unseeded-2026-11-10/draw-d2/judged', CUSTOM),
    ('stage B u2 v7 #1', 'stage-b', 'u2', 'v7', 1, DATA / 'clean-stage-b-2026-11-11/draw-u2', CUSTOM),
    ('stage B u3 v10 #1', 'stage-b', 'u3', 'v10', 1, DATA / 'clean-stage-b-2026-11-11/draw-u3', r'wafer|HBM[^\n]{0,80}capacity|capacity[^\n]{0,80}HBM'),
    ('stage B u3 v8 #3', 'stage-b', 'u3', 'v8', 3, DATA / 'clean-stage-b-2026-11-11/draw-u3', rf'(purchase|supply)[^\n]{{0,40}}(commitment|obligation)s?[^\n]{{0,160}}{MONEY}|{MONEY}[^\n]{{0,160}}(purchase|supply)[^\n]{{0,40}}(commitment|obligation)'),
    ('stage B u1 v6 #5', 'stage-b', 'u1', 'v6', 5, DATA / 'clean-stage-b-2026-11-11/draw-u1', r'Kyber|Rubin Ultra|NVL144'),
]


def store_of(folder):
    for candidate in (folder, *sorted(p for p in folder.iterdir() if p.is_dir())):
        if (candidate / 'views.sqlite').exists() and (candidate / 'archive.sqlite').exists():
            return candidate
    raise SystemExit(f'no store under {folder}')


def main():
    held = Path(sys.argv[1])
    keys = {'baseline': json.loads((held / 'stage-b-baseline-key.json').read_text()), 'stage-b': json.loads((held / 'stage-b-reading-key.json').read_text())}
    out = []
    for label, reading, draw, view, number, folder, pattern in CASES:
        entry = next(e for e in keys[reading].values() if e['kind'] == 'stored' and (e['draw'], e['view'], e['number_in_view']) == (draw, view, number))
        folder = store_of(folder)
        store = sqlite3.connect(f"file:{folder / 'views.sqlite'}?mode=ro", uri=True)
        archive = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        seq, day, rung, sha = store.execute('select seq, publication_day, rung, request_sha256 from judgements where judgement_id = ?', (entry['judgement_id'],)).fetchone()
        question = store.execute('select question from views where view_id = ?', (view,)).fetchone()[0]
        user = json.loads(archive.execute('select request_json from model_calls where request_sha256 = ?', (sha,)).fetchone()[0])['messages'][-1]['content']
        printed = set(re.findall(r'^- (e\d+) \[', user, re.M))
        hidden = re.search(r'\[Not shown: (\d+) more pieces', user)
        linked_now = {row[0] for row in store.execute('select evidence_id from evidence_links where view_id = ? and seq <= ?', (view, seq))}
        hits = []
        for evidence_id, created, one_line, quote in store.execute('select evidence_id, created_seq, one_line, quote from evidence where created_seq <= ?', (seq,)):
            if evidence_id in printed or not re.search(pattern, f'{one_line}\n{quote}', re.I):
                continue
            homes = sorted(row[0] for row in store.execute('select view_id from evidence_links where evidence_id = ? and seq <= ?', (evidence_id, seq)))
            hits.append({'statement': evidence_id, 'article': created, 'filed_under': homes, 'linked_to_this_question_but_not_printed': evidence_id in linked_now, 'summary': one_line})
        in_request = sum(1 for e in printed if re.search(pattern, ' '.join(store.execute('select one_line, quote from evidence where evidence_id = ?', (e,)).fetchone() or ('', '')), re.I))
        out.append({'case': label, 'question': question, 'day': day, 'band': rung, 'statements_printed': len(printed), 'not_shown_note': hidden.group(1) if hidden else None,
                    'printed_statements_matching_the_pattern': in_request, 'candidates': hits})
        print(f"\n{label} ({day}, band {rung}): {question[:110]}\n   request prints {len(printed)} statements ({in_request} match the matter's pattern)"
              + (f"; {hidden.group(1)} more not shown" if hidden else '') + f"; in the store by then and not printed, matching: {len(hits)}")
        for hit in hits[:6]:
            print(f"      {hit['statement']} (article {hit['article']}; filed under {hit['filed_under'] or 'no question'}{'; LINKED HERE, not printed' if hit['linked_to_this_question_but_not_printed'] else ''}): {hit['summary'][:190]}")
    (Path(__file__).resolve().parent / 'candidates.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
