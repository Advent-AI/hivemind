"""Every amount question of the stored runs of both systems: its ranges, the judge's answer day by day, and the amounts the judge
cited on the days it sat on an end range ($0; D545). A sheet for reading, not a score: whether an opening article gives a
comparable amount, whether a filed amount is comparable with the boundary it passes, and whether the end range hides what the
question was meant to track are read by hand from this sheet and the articles.

  python3 range_census.py
"""
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
DATA = ROOT / 'poc/data'
HERE = Path(__file__).parent
RUNS = {'new, fresh week': DATA / 'clean-lean-week-2026-11-14/week-r2/c1/judge/draw-c1', 'old, fresh week': DATA / 'clean-lean-week-2026-11-14/week/p1/prod'}
for draw in (1, 2, 3):
    RUNS[f'new, July run {draw}'] = DATA / f'clean-e2e-full-2026-11-13/c{draw}/judge/draw-c{draw}'
    RUNS[f'old, July run {draw}'] = DATA / f'clean-e2e-full-2026-11-13/p{draw}/prod'
EVENT_LABELS = {'yes', 'no', 'ruled out', 'still open'}
AMOUNT = re.compile(r'\$\s?\d[\d,.]*\s?(?:billion|bn|million|trillion|B|M)?\b|\d[\d,.]*\s?%|\d[\d,.]*\s?(?:billion|million|trillion|gigawatts?|GW)\b', re.I)
ITEMS = sqlite3.connect(f"file:{DATA / 'items-nvda-2026-07-01-10-27.sqlite'}?mode=ro", uri=True)


def article_of(input_id):
    row = ITEMS.execute('select publication_day, title, text from items where input_id = ?', (input_id,)).fetchone()
    return {'day': row[0], 'title': row[1], 'text': row[2]} if row else None


def main():
    columns = [row[1] for row in ITEMS.execute('pragma table_info(items)')]
    assert 'text' in columns and 'title' in columns, columns
    sheet = []
    for name, folder in RUNS.items():
        db = sqlite3.connect(f"file:{folder / 'views.sqlite'}?mode=ro", uri=True)
        db.row_factory = sqlite3.Row
        for view in db.execute('select view_id, object_id, object_kind, question, created_from_input, due_day from views order by created_seq'):
            rungs = [dict(row) for row in db.execute('select label, condition from rungs where view_id = ? order by position', (view['view_id'],))]
            if not rungs or {rung['label'].strip().lower() for rung in rungs} & EVENT_LABELS:
                continue
            judgements = db.execute('select input_id, rung, reasons, cited_evidence_json from judgements where view_id = ? order by judgement_id', (view['view_id'],)).fetchall()
            ends = [j for j in judgements if j['rung'] in (1, len(rungs))]
            cited = {}
            for judgement in ends:
                for evidence_id in json.loads(judgement['cited_evidence_json'] or '[]'):
                    row = db.execute('select one_line from evidence where evidence_id = ?', (evidence_id,)).fetchone()
                    if row and AMOUNT.search(row[0]):
                        cited[evidence_id] = row[0]
            article = article_of(view['created_from_input'])
            opening_amounts = sorted({m.group(0) for m in AMOUNT.finditer(article['text'])}) if article else None
            sheet.append({'run': name, 'view': view['view_id'], 'kind': view['object_kind'], 'question': view['question'], 'due_day': view['due_day'],
                          'ranges': [rung['condition'] for rung in rungs], 'answers_by_day': [(j['input_id'].replace('day:', ''), j['rung']) for j in judgements],
                          'days_judged': len(judgements), 'days_on_an_end_range': len(ends), 'end_range': ends[-1]['rung'] if ends else None,
                          'last_reasons_on_an_end_range': ends[-1]['reasons'][:500] if ends else None, 'amount_statements_cited_on_end_range_days': cited,
                          'opening_article': {'input_id': view['created_from_input'], 'day': article and article['day'], 'title': article and article['title'],
                                              'amounts_in_text': opening_amounts}})
    (HERE / 'range-census-sheet.json').write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + '\n')
    print(f"amount questions: {len(sheet)} over {len(RUNS)} runs; with at least one day on an end range: {sum(1 for row in sheet if row['days_on_an_end_range'])}; "
          f"judgement days: {sum(row['days_judged'] for row in sheet)}, on an end range: {sum(row['days_on_an_end_range'] for row in sheet)}")
    for row in sheet:
        mark = f"{row['days_on_an_end_range']}/{row['days_judged']} end-range days (range {row['end_range']})" if row['days_on_an_end_range'] else f"0/{row['days_judged']}"
        print(f"{row['run']:18} {row['view']:4} {row['kind']:8} {mark:34} | {row['question'][:105]}")


if __name__ == '__main__':
    main()
