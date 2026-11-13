"""Reference packet ($0): every candidate ladder production's frozen extraction (v74i) wrote in the three same-day control draws of
2026-11-09, as a judge would be shown it, with the article it was written from. Read with the Stage A marks, it says how sound the
ladders production writes are, without sending anything. Writes packet.json beside this file.

Usage: PYTHONDONTWRITEBYTECODE=1 python3 build_packet.py"""
import json, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DRAWS = [ROOT / f'poc/data/clean-e2e-2026-11-09/stage2-control-{d}/archive.sqlite' for d in ('d1', 'd3', 'd4')]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import extraction  # noqa: E402

CLOSING = '\n\nReturn evidence and candidates per the JSON schema.'


def main():
    packet = []
    for path in DRAWS:
        conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
        try:
            rows = conn.execute("select call_id, request_json, answer_json from model_calls where purpose = 'extract'").fetchall()
        finally:
            conn.close()
        for call_id, request, answer in rows:
            candidates = (json.loads(answer) or {}).get('candidates') or []
            if not candidates:
                continue
            user = json.loads(request)['messages'][-1]['content']
            start = user.index('[Item] id ')
            article = user[start:user.index(CLOSING, start)]
            evidence = {e['id']: e['one_line'] for e in json.loads(answer).get('evidence') or []}
            for c in candidates:
                problem = extraction.check_ladder(c['rungs'], c['kind']) or extraction.check_bounds(c['rungs'])
                rungs = c['rungs'] if problem else extraction.normalise_ladder(c['rungs'], c['kind'])
                packet.append({'item': len(packet) + 1, 'draw': path.parent.name, 'call': call_id,
                               'article': article, 'statements_the_question_was_opened_from': [evidence[i] for i in c.get('evidence_ids', []) if i in evidence],
                               'ladder_as_the_judge_is_shown_it': {'object': c['object'], 'kind': c['kind'], 'question': c['question'], 'year': c['year'], 'due_day': c['due_day'],
                                                                   'rungs': [{'position': n, 'label': r['label'], 'condition': r['condition']} for n, r in enumerate(rungs, 1)]},
                               'refused_by_production_check': problem})
    if not packet:
        raise SystemExit('no candidate ladder found: the packet would be empty')
    (HERE / 'packet.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False))
    print(len(packet), 'ladders;', sum(1 for p in packet if len(p['ladder_as_the_judge_is_shown_it']['rungs']) == 2), 'yes/no;', (HERE / 'packet.json').stat().st_size, 'bytes')


if __name__ == '__main__':
    main()
