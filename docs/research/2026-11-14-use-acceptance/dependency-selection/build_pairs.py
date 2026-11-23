"""The pairs a dependency choice could have been made on, in the stored unseeded fresh week of the old system ($0; D536).

For each question the run opened: the questions its candidate was compared with when it opened (the comparison list and the questions
shown that day, as the stored matching record names them) and the other candidates opened from the same article. D51 and PRD 06
let the matching call choose a new question's dependencies only among these. Writes `pairs.json` (with the relation the matching
engine recorded) and `packet.md` for blind readers (without it). Reads the stored run only.

  python3 build_pairs.py
"""
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
RUN = ROOT / 'poc/data/clean-lean-week-2026-11-14/week/p1/prod'
HERE = Path(__file__).parent


def main():
    db = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    views = {row['view_id']: dict(row) for row in db.execute('select view_id, object_id, object_kind, kind, looks_at, year, due_day, created_seq, question from views')}
    for view_id, view in views.items():
        view['answers'] = [f"{row['label']}: {row['condition']}" for row in db.execute('select label, condition from rungs where view_id = ? order by position', (view_id,))]
        view['day'] = db.execute('select publication_day from processing_steps where sequence_no = ? limit 1', (view['created_seq'],)).fetchone()[0]
    by_article = {}
    for view_id, view in sorted(views.items(), key=lambda pair: int(pair[0][1:])):
        by_article.setdefault(view['created_seq'], []).append(view_id)
    pairs = []
    for article, opened in sorted(by_article.items()):
        record = db.execute('select shown_json, decisions_json from match_records where seq = ? order by id', (article,)).fetchone()
        shown, decisions = json.loads(record['shown_json']), json.loads(record['decisions_json'])
        candidates = [c for c in decisions['candidates'] if c['outcome'] in ('new', 'succession')]
        assert len(candidates) == len(opened), (article, opened)
        for view_id, candidate in zip(opened, candidates):             # candidates are written in order: the first new candidate is the lower question number
            recorded = dict((name, (relation, float(probability))) for name, relation, probability in re.findall(r'(v\d+): (\w+) (\d\.\d+)', candidate['reason'].split('collision judge')[0]))
            compared = sorted(set(shown['candidates'].get(candidate['id'], [])) | set(recorded), key=lambda name: int(name[1:]))
            judge = dict(re.findall(r'(v\d+): (\w+)', candidate['reason'].split('collision judge:')[1])) if 'collision judge:' in candidate['reason'] else {}
            for other in compared:
                assert views[other]['created_seq'] <= article and other != view_id
                pairs.append({'new': view_id, 'other': other, 'how_permitted': 'compared when it opened', 'matching_engine_relation': recorded.get(other, (None, None))[0],
                              'matching_engine_probability': recorded.get(other, (None, None))[1], 'comparison_judge_relation': judge.get(other), 'outcome_recorded': candidate['outcome']})
            for sibling in opened:
                if sibling != view_id:
                    pairs.append({'new': view_id, 'other': sibling, 'how_permitted': 'opened from the same article', 'matching_engine_relation': None, 'matching_engine_probability': None,
                                  'comparison_judge_relation': None, 'outcome_recorded': candidate['outcome']})
    (HERE / 'pairs.json').write_text(json.dumps({'run': str(RUN.relative_to(ROOT)), 'questions': views, 'pairs': pairs}, indent=1, ensure_ascii=False) + '\n')
    lines = ['# Fifteen questions and the questions each could have drawn on when it opened', '',
             'One company (NVIDIA) was followed for a week of news. The system opened the fifteen questions below, in this order. "Theme" questions are about the wider market or policy;',
             'the system already shows every theme question\'s current conclusion to every company question, so no link is needed for that.', '']
    for view_id, view in sorted(views.items(), key=lambda pair: int(pair[0][1:])):
        lines += [f"## {view_id} ({'theme' if view['object_kind'] == 'theme' else 'company'}; opened {view['day']}, article {view['created_seq']}; answer due {view['due_day']})", '', view['question'], '',
                  'Possible answers: ' + ' / '.join(view['answers']), '']
    lines += ['# The pairs to mark', '', 'For each newly opened question, the earlier questions it was compared with when it opened, and any question opened from the same article:', '']
    for view_id in sorted(views, key=lambda name: int(name[1:])):
        others = [p for p in pairs if p['new'] == view_id]
        if others:
            lines.append(f"- {view_id}: " + ', '.join(p['other'] + (' (same article)' if p['how_permitted'].startswith('opened') else '') for p in others))
    (HERE / 'packet.md').write_text('\n'.join(lines) + '\n')
    relations = {}
    for pair in pairs:
        relations[pair['matching_engine_relation']] = relations.get(pair['matching_engine_relation'], 0) + 1
    print(f"questions {len(views)}; pairs {len(pairs)} ({sum(1 for p in pairs if p['how_permitted'].startswith('opened'))} from the same article); relation recorded by the matching engine: {relations}")
    for pair in pairs:
        if pair['matching_engine_relation'] not in ('different', None) or pair['comparison_judge_relation'] not in ('different', None):
            print(f"   {pair['new']} against {pair['other']}: {pair['matching_engine_relation']} {pair['matching_engine_probability']}; comparison judge: {pair['comparison_judge_relation']}")


if __name__ == '__main__':
    main()
