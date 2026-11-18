#!/usr/bin/env python3
"""Every judgement the frozen judge's check refused and re-asked, in the saved D392 draws (clean and production): the refused answer's
rung, the accepted re-send's rung, the reason given back, and whether that question's rung at the window end is the re-send's rung
carried on. Read-only; no model call. A re-sent request is the refused request's text with the retry note appended
(judging.round_of_judgements), so each refused row is paired with the accepted row whose user text starts with the refused one's.

Usage: refusal_census.py <output json>"""
import collections, glob, json, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRAWS = ROOT / 'poc/data/clean-e2e-2026-11-09'
WINDOW_END = '2026-07-14'


def runs():
    for draw in (1, 2, 3):
        yield f'clean-d{draw}', Path(sorted(glob.glob(str(DRAWS / f'stage2-clean-d{draw}/judged*')))[-1])
    for draw in (1, 3, 4):
        yield f'control-d{draw}', DRAWS / f'stage2-control-d{draw}'


def main(output_path):
    rows, totals = [], collections.Counter()
    for label, folder in runs():
        archive = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        views = sqlite3.connect(f"file:{folder / 'views.sqlite'}?mode=ro", uri=True)
        calls = archive.execute("select call_id, request_sha256, request_json, answer_json from model_calls where purpose='judge' order by call_id").fetchall()
        accepted_by_sha = {sha: (call_id, json.loads(req), json.loads(ans)) for call_id, sha, req, ans in calls if ':' not in sha and ans}
        judgement_of = {sha: (view, day, rung) for view, day, rung, sha in views.execute('select view_id, publication_day, rung, request_sha256 from judgements')}
        totals[label, 'judgements'] = len(judgement_of)
        for call_id, sha, request_json, answer_json in calls:
            if ':refused:' not in sha or not answer_json:
                continue
            refused_user = json.loads(request_json)['messages'][-1]['content']
            refused = json.loads(answer_json)
            retry = [(cid, req, ans, s) for s, (cid, req, ans) in accepted_by_sha.items()
                     if cid > call_id and req['messages'][-1]['content'].startswith(refused_user) and len(req['messages'][-1]['content']) > len(refused_user)]
            note = retry[0][1]['messages'][-1]['content'][len(refused_user):].strip() if retry else None
            if retry:
                _, _, retry_answer, retry_sha = retry[0]
                view, day, rung = judgement_of.get(retry_sha, (None, None, None))
            else:
                view = day = rung = retry_answer = None
            if view is None:   # the re-send was refused too (the day stopped), or no pair was found
                totals[label, 'refused with no accepted re-send'] += 1
                rows.append({'run': label, 'call': call_id, 'refused rung': refused['rung'], 'accepted rung': None, 'note': note})
                continue
            path = [r for r, in views.execute('select rung from judgements where view_id=? and publication_day>=? and publication_day<=? order by judgement_id',
                                               (view, day, WINDOW_END))]
            final = path[-1] if path else None
            rows.append({'run': label, 'call': call_id, 'view': view, 'day': day, 'refused rung': refused['rung'], 'accepted rung': rung,
                         'rung changed by the re-send': refused['rung'] != rung, 'window-end rung': final,
                         'held from the re-send to the window end': all(r == rung for r in path), 'note': note})
            totals[label, 'refused and re-sent'] += 1
            totals[label, 'the re-send changed the rung'] += refused['rung'] != rung
            totals[label, 'changed and held to the window end'] += (refused['rung'] != rung) and all(r == rung for r in path)
    notes = collections.Counter()
    for row in rows:
        reason = (row['note'] or '').split('because:', 1)[-1].split('|')[0].strip()[:90]
        notes[reason.split(';')[0]] += 1
    summary = {f'{run} {name}': n for (run, name), n in sorted(totals.items())}
    Path(output_path).write_text(json.dumps({'summary': summary, 'reasons': notes.most_common(), 'rows': rows}, ensure_ascii=False, indent=1))
    print(json.dumps(summary, indent=1))
    print('reasons given back (first clause):')
    for reason, n in notes.most_common(12):
        print(f'  {n:>3}  {reason}')
    print('re-sends that changed the rung:')
    for row in rows:
        if row.get('rung changed by the re-send'):
            print(f"  {row['run']:<11} {row['view']:<4} {row['day']} refused {row['refused rung']} -> accepted {row['accepted rung']}; window end {row['window-end rung']}; "
                  f"held {row['held from the re-send to the window end']} | {(row['note'] or '')[:110]}")


if __name__ == '__main__':
    main(sys.argv[1])
