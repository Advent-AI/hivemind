"""Production's matched views as controls, built exactly as Stage B built the clean arm's (`clean-arch/step4-2026-11-10/stage_b/
control_theses.py`, whose functions this imports: `evidence_entries`, `agrees`, `packet_texts`), so the two arms are read with one brief
(`stage_b/control-reader-brief.md`) and counted by one rule (DESIGN.md v4, procedure 5–6).

A record pairs a ruler question with the production view the matching read confirmed SAME (`mapping-prod.json`: {draw: {view_id:
question_id}}), and holds reader B's decisive items, the view's rungs, its last judgement on or before 2026-07-14, and every evidence
entry the view's judge requests listed through that day (the entries' own text, as Stage B showed them).

  packets <readers' folder> <facts path> <mapping-prod.json> <draw=run folder> ...
"""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'clean-arch/step4-2026-11-10/stage_b'))
import control_theses  # noqa: E402  (evidence_entries, agrees, packet_texts, GOLD, WINDOW_END)

GOLD = control_theses.GOLD
WINDOW_END = control_theses.WINDOW_END


def facts(mapping_path, folders):
    questions = {q['id']: q for q in json.loads((GOLD / 'questions-v1.json').read_text())['questions']}
    gold = {entry['question_id']: entry for entry in json.loads((GOLD / 'gold-v1.json').read_text())['entries']}
    items = {item['id']: item for item in json.loads((GOLD / 'packet-v1.json').read_text())['items']}
    out = []
    for draw, views in json.loads(Path(mapping_path).read_text()).items():
        folder = Path(folders[draw])
        connection = sqlite3.connect(f"file:{folder / 'views.sqlite'}?mode=ro", uri=True)
        connection.row_factory = sqlite3.Row
        archive = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        for view_id, question_id in views.items():
            view = connection.execute('select * from views where view_id = ?', (view_id,)).fetchone()
            if view is None:
                raise SystemExit(f'{draw}: {view_id} is not in {folder}: refused')
            rungs = [dict(row) for row in connection.execute('select position, label, condition, lo, hi from rungs where view_id = ? order by position', (view_id,))]
            judged = connection.execute('select judgement_id, rung, call_id, publication_day from judgements where view_id = ? and publication_day <= ? '
                                        'order by judgement_id', (view_id, WINDOW_END)).fetchall()
            last = judged[-1] if judged else None
            shown, seen = [], set()
            for judgement in judged:
                row = archive.execute('select request_json from model_calls where call_id = ?', (judgement['call_id'],)).fetchone()
                if row is None:
                    raise SystemExit(f'{draw}/{view_id}: judgement call {judgement["call_id"]} is not in the archive: refused')
                for evidence_id, text in control_theses.evidence_entries(json.loads(row[0])['messages'][-1]['content']):
                    if (evidence_id, text) not in seen:
                        seen.add((evidence_id, text))
                        shown.append(text)
            entry, ruler = gold[question_id], questions[question_id]
            out.append({'control': f'{draw}/{view_id}', 'question_id': question_id, 'ohio': 'Ohio' in ruler['question'],
                        'ruler': {key: ruler[key] for key in ('question', 'unit', 'due_day', 'rungs')},
                        'gold_answer': entry.get('implied_outcome'), 'gold_open': not entry.get('implied_outcome') or bool(entry.get('no_view')),
                        'decisive_items': [{key: items[item].get(key) for key in ('id', 'day', 'title', 'passage', 'meaning')} for item in entry.get('decisive_items', [])],
                        'view': {key: view[key] for key in ('view_id', 'question', 'looks_at', 'due_day', 'year', 'kind')},
                        'rungs': rungs, 'last_judgement': None if last is None else {'rung': last['rung'], 'day': last['publication_day']},
                        'requests_searched': len(judged), 'evidence_shown': shown})
    return out


def packets(readers_folder, facts_path, mapping_path, folders):
    readers_folder, facts_path = Path(readers_folder), Path(facts_path)
    if facts_path.resolve().is_relative_to(readers_folder.resolve()):
        raise SystemExit("the facts hold reader B's answers: they must sit outside the readers' folder")
    records = facts(mapping_path, folders)
    (readers_folder / 'controls').mkdir(parents=True, exist_ok=False)
    for number, text in enumerate(control_theses.packet_texts(records), start=1):
        (readers_folder / 'controls' / f'control-packet-{number}.json').write_text(text)
    facts_path.parent.mkdir(parents=True, exist_ok=True)
    facts_path.write_text(json.dumps([{k: v for k, v in r.items() if k != 'evidence_shown'} for r in records], indent=1, ensure_ascii=False) + '\n')
    print(f'{len(records)} controls; judged by {WINDOW_END} {sum(1 for r in records if r["last_judgement"])}; Ohio {sum(1 for r in records if r["ohio"])}')


if __name__ == '__main__':
    if sys.argv[1:2] == ['packets']:
        folders = dict(arg.split('=', 1) for arg in sys.argv[5:])
        packets(sys.argv[2], sys.argv[3], sys.argv[4], folders)
    else:
        raise SystemExit(__doc__)
