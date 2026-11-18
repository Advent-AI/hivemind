"""Do the kept financial figures reach the judgements? Step 3 ($0; DELIVERY-CHECK-DESIGN.md version 2). Read-only on a finished run.

Joins both reader families' lists (the table lines whose figure bears on each question) to the census and to the stored judgement
requests. For every (question, line) either family lists it prints: who listed it; whether a statement of the line itself was shown
to the question; if not, where the question's last stored request mentions the figure's first number (snippets to be read by hand:
the search decides nothing); and whether the question was already open when the figure's article was read. It refuses a question
that lacks a completion line from a family. It writes `delivery-candidates.json` and prints the instrument's own check (the lines the
system did show, against the readers' lists). It judges nothing about what a question needs.

  python3 tally_delivery.py <run folder of the clean draw>
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TABLE = HERE.parent / 'record-3' / 'table-rows-week.json'
FAMILIES = ('codex', 'claude')


def objects(path):
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find('{"question"', position)
        if start == -1:
            return out
        row, position = decoder.raw_decode(text, start)
        out.append(row)


def main():
    run = Path(sys.argv[1])
    census = json.loads((HERE / 'delivery-census.json').read_text())
    table = json.loads(TABLE.read_text())
    views = sqlite3.connect(f"file:{run / 'judge/draw-c1/views.sqlite'}?mode=ro", uri=True)
    archive = sqlite3.connect(f"file:{run / 'judge/draw-c1/archive.sqlite'}?mode=ro", uri=True)
    opened_at = {view_id: created_seq for view_id, created_seq in views.execute('select view_id, created_seq from views')}
    last_request = {}
    for view_id, call_id in views.execute('select view_id, call_id from judgements order by seq, judgement_id'):
        request = json.loads(archive.execute('select request_json from model_calls where call_id = ?', (call_id,)).fetchone()[0])
        last_request[view_id] = request['messages'][-1]['content']
    listed = {family: {} for family in FAMILIES}
    for family in FAMILIES:
        for view in sorted(census['questions']):
            rows = objects(HERE / f'{family}-needed-{view}.jsonl')
            if not any(row.get('done') for row in rows):
                raise SystemExit(f'{family} has no completion line for {view}: the question is not read; run it again')
            listed[family][view] = {row['line']: row.get('how') for row in rows if row.get('line')}
            unknown = [line for line in listed[family][view] if line not in table]
            if unknown:
                raise SystemExit(f'{family} {view} lists lines that are not in the table: {unknown}')
    candidates = []
    print('PER QUESTION: lines listed by each family, and of those the lines whose own statement was shown to the question')
    for view in sorted(census['questions']):
        sets = {family: set(listed[family][view]) for family in FAMILIES}
        both, either = sets['codex'] & sets['claude'], sets['codex'] | sets['claude']
        shown = {line for line, entry in census['lines'].items() if view in entry['shown_to']}
        print(f"\n{view} (opened at article {opened_at[view]}): {census['questions'][view][:140]}")
        print(f"  listed: codex {len(sets['codex'])}, claude {len(sets['claude'])}, both {len(both)}, either {len(either)}; the system showed {len(shown)} table lines")
        print(f"  the instrument: of the {len(shown)} lines the system showed, the readers also list: codex {len(shown & sets['codex'])}, claude {len(shown & sets['claude'])}, both {len(shown & both)}; "
              f"of the {len(both)} lines both list, shown {len(both & shown)}, not shown {len(both - shown)}")
        for line in sorted(either):
            if line in shown:
                continue
            members = table[line]
            first = members[0]
            number = re.search(r'\d+(?:\.\d+)?', str(first['value']))
            snippets = []
            if number:
                for match in re.finditer(rf'(?<![\d.]){re.escape(number.group(0))}(?![\d])', last_request[view]):
                    snippets.append(last_request[view][max(0, match.start() - 110):match.end() + 90].replace('\n', ' '))
            articles = sorted({m['article'] for m in members})
            before = [a for a in articles if a < opened_at[view]]
            candidates.append({'question': view, 'line': line, 'listed_by': 'both' if line in both else ('codex' if line in sets['codex'] else 'claude'),
                               'measure': first['measure'], 'value': first['value'], 'period': first['period'], 'source': first['source'],
                               'articles': articles, 'articles_read_before_the_question_opened': before,
                               'how': {family: listed[family][view].get(line) for family in FAMILIES},
                               'same_claim_lead': view in census['lines'][line]['same_claim_lead_for'],
                               'request_mentions_of_the_number': snippets[:4]})
            print(f"  NOT SHOWN {line} [{'both' if line in both else ('codex only' if line in sets['codex'] else 'claude only')}] {first['measure'][:40]}: {str(first['value'])[:34]} | {str(first['period'])[:24]} | {str(first['source'])[:26]} "
                  f"| articles {articles} ({len(before)} read before the question opened) | number in the last request: {len(snippets)} places")
    (HERE / 'delivery-candidates.json').write_text(json.dumps(candidates, ensure_ascii=False, indent=1))
    by = {'both': 0, 'codex': 0, 'claude': 0}
    for candidate in candidates:
        by[candidate['listed_by']] += 1
    print(f"\n{len(candidates)} (question, line) pairs listed by a reader and not shown by the line's own statement: by both {by['both']}, Codex only {by['codex']}, Claude only {by['claude']}")


if __name__ == '__main__':
    main()
