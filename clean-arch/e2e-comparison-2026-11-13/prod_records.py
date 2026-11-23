"""Production record reader for the end-to-end comparison (D442; design shape B'): for one ruler question and one view of a production
views database, the view's outcome against reader B, by the frozen scorer's own rule (`docs/research/2026-11-01-e2e-loop/
judgement-gold/score_judgement.py`, read, never edited): the view's last judgement with publication_day on or before the day; for a
yes/no question, the chosen rung's label "yes" against reader B's answer; for a figure, the chosen rung's band overlapping reader B's
implied range. The scorer refuses runs without the 22 seed views, so this reader applies its rule to any view the comparison names.

  outcome(views_db, question_id, view_id, day='2026-07-14') -> dict(outcome=..., detail=...)
    outcome is one of: 'no_view' and 'gold open' (not graded, as the scorer reports them), 'not in run' (no view named),
    'no judgement', 'no comparison' (a figure rung with neither bound, which the scorer would count as agreeing), 'agree', 'disagree'.

  shown_evidence(run_folder, view_id, day) -> the evidence ids the judge's requests listed for the view by the day

  python3 prod_records.py validate-shown <run folder> ...   positive and negative checks of shown_evidence on stored runs
  python3 prod_records.py validate <run folder> ...   compares this reader on the seed views (q01..q22 -> v1..v22, q23 as the scorer
                                                      finds it) with the frozen scorer's printed outcome, question by question
"""
import hashlib
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GOLD_DIR = ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold'
GOLD_SHA256 = '636c056d1e4252fa759660803067e6ccd67a81067b012905e918aa9dec4005f2'


def gold_and_questions():
    raw = (GOLD_DIR / 'gold-v1.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != GOLD_SHA256:
        raise SystemExit('gold-v1.json is not the frozen gold: refused')
    gold = {e['question_id']: e for e in json.loads(raw)['entries']}
    questions = {q['id']: q for q in json.loads((GOLD_DIR / 'questions-v1.json').read_text(encoding='utf-8'))['questions']}
    return gold, questions


def outcome(views_db, question_id, view_id, day='2026-07-14', gold=None, questions=None):
    if gold is None:
        gold, questions = gold_and_questions()
    entry, question = gold[question_id], questions[question_id]
    if entry.get('no_view'):
        return {'outcome': 'no_view', 'detail': ''}
    if not entry.get('implied_outcome'):
        return {'outcome': 'gold open', 'detail': ''}
    if not view_id:
        return {'outcome': 'not in run', 'detail': ''}
    implied = (entry.get('resolution') or entry)['implied_outcome']
    conn = sqlite3.connect(f'file:{views_db}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    judgement = conn.execute('select rung, publication_day from judgements where view_id=? and publication_day<=? '
                             'order by judgement_id desc limit 1', (view_id, day)).fetchone()
    rungs = [dict(r) for r in conn.execute('select position, label, lo, hi from rungs where view_id=? order by position', (view_id,))]
    if judgement is None:
        return {'outcome': 'no judgement', 'detail': f'{view_id} never judged by {day}'}
    chosen = rungs[judgement['rung'] - 1]
    if question['unit'] == 'yes/no':
        agree = (chosen['label'].lower() == 'yes') == bool(implied['yes_no'])
        return {'outcome': 'agree' if agree else 'disagree', 'detail': f"{view_id} rung {judgement['rung']} {chosen['label']} on {judgement['publication_day']}"}
    lo, hi = chosen['lo'], chosen['hi']
    if lo is None and hi is None:
        return {'outcome': 'no comparison', 'detail': f"{view_id} rung {judgement['rung']} {chosen['label']} has no bound"}
    agree = (lo is None or implied['high'] >= lo) and (hi is None or implied['low'] < hi)
    return {'outcome': 'agree' if agree else 'disagree', 'detail': f"{view_id} rung {judgement['rung']} {chosen['label']} {lo}..{hi}"}


def scorer_outcomes(run_folder):
    """The frozen scorer's printed outcome per question for a seeded run."""
    out = subprocess.run([sys.executable, str(GOLD_DIR / 'score_judgement.py'), str(run_folder)], capture_output=True, text=True, check=True).stdout
    result = {}
    for line in out.splitlines():
        m = re.match(r'^(q\d\d)\s+(agree|DISAGREE|no judgement|not in run|gold open|no_view)\b', line)
        if m:
            result[m.group(1)] = m.group(2).lower()
    return result, out


def validate(run_folders):
    gold, questions = gold_and_questions()
    judged = mismatches = 0
    for folder in run_folders:
        expected, text = scorer_outcomes(folder)
        db = Path(folder) / 'views.sqlite'
        conn = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
        mapping = {f'q{k:02d}': f'v{k}' for k in range(1, 23)}
        hit = conn.execute("select view_id from views where question like '%Ohio%' and question like '%guarantee%' order by created_seq limit 1").fetchone()
        if hit:
            mapping['q23'] = hit[0]
        for qid in sorted(gold):
            mine = outcome(db, qid, mapping.get(qid), gold=gold, questions=questions)['outcome']
            mine_as_scorer = 'agree' if mine == 'no comparison' else mine      # the scorer counts a boundless band as agreeing
            judged += 1
            if expected.get(qid) != mine_as_scorer:
                mismatches += 1
                print(f'MISMATCH {folder} {qid}: scorer {expected.get(qid)}, reader {mine}')
        print(f'{folder}: scorer outcomes {dict(sorted(__import__("collections").Counter(expected.values()).items()))}')
    print(f'{judged} question outcomes compared, {mismatches} mismatches')
    return mismatches == 0 and judged > 0


EVIDENCE_LINE = re.compile(r'(?m)^- (e\d+) \[')
SAME_CLAIM_NOTE = re.compile(r'same claim as ((?:e\d+(?:, )?)+)')


def shown_evidence(run_folder, view_id, day='2026-07-14'):
    """The evidence ids listed in the judge requests behind the view's judgements published on or before the day (the requests are
    the stored archive rows the judgements name by call_id). A judge call the code refused made no judgement and is not included."""
    views = sqlite3.connect(f"file:{Path(run_folder) / 'views.sqlite'}?mode=ro", uri=True)
    archive = sqlite3.connect(f"file:{Path(run_folder) / 'archive.sqlite'}?mode=ro", uri=True)
    shown = set()
    for (call_id,) in views.execute('select call_id from judgements where view_id=? and publication_day<=?', (view_id, day)):
        row = archive.execute('select request_json from model_calls where call_id=?', (call_id,)).fetchone()
        if row is None:
            raise SystemExit(f'{run_folder}: judgement call {call_id} of {view_id} is not in the archive: refused')
        user = json.loads(row[0])['messages'][-1]['content']
        shown |= set(EVIDENCE_LINE.findall(user))
    return shown


def validate_shown(run_folders):
    """Positive: every evidence id a judgement cites is listed in that judgement's own request. Negative: an evidence item of the view
    created after a judgement's request is not listed in that request."""
    positives = negatives = failures = 0
    for folder in run_folders:
        views = sqlite3.connect(f"file:{Path(folder) / 'views.sqlite'}?mode=ro", uri=True)
        for view_id, call_id, cited, day, seq in views.execute('select view_id, call_id, cited_evidence_json, publication_day, seq from judgements'):
            archive = sqlite3.connect(f"file:{Path(folder) / 'archive.sqlite'}?mode=ro", uri=True)
            user = json.loads(archive.execute('select request_json from model_calls where call_id=?', (call_id,)).fetchone()[0])['messages'][-1]['content']
            listed = set(EVIDENCE_LINE.findall(user))
            missing = set(json.loads(cited or '[]')) - listed
            positives += 1
            if missing:
                failures += 1
                print(f'POSITIVE FAIL {folder} {view_id} call {call_id}: cited but not listed {sorted(missing)[:5]}')
            # an id named only in a duplicate note ("the same claim as e30, e32") is not an entry shown to the judge
            entry_ids = {line.split()[1] for line in user.splitlines() if re.match(r'^- e\d+ \[', line)}
            for group in SAME_CLAIM_NOTE.findall(user):
                for evidence_id in re.findall(r'e\d+', group):
                    if evidence_id in entry_ids:
                        continue
                    negatives += 1
                    if evidence_id in listed:
                        failures += 1
                        print(f'NEGATIVE FAIL {folder} {view_id} call {call_id}: {evidence_id} named only in a duplicate note but counted as shown')
        created = dict(views.execute('select evidence_id, created_seq from evidence'))
        for view_id, call_id, seq in views.execute('select view_id, call_id, seq from judgements'):
            later = [e for (e,) in views.execute('select distinct evidence_id from evidence_links where view_id=?', (view_id,)) if created.get(e, -1) > seq]
            if not later:
                continue
            archive = sqlite3.connect(f"file:{Path(folder) / 'archive.sqlite'}?mode=ro", uri=True)
            listed = set(EVIDENCE_LINE.findall(json.loads(archive.execute('select request_json from model_calls where call_id=?', (call_id,)).fetchone()[0])['messages'][-1]['content']))
            for evidence_id in later:
                negatives += 1
                if evidence_id in listed:
                    failures += 1
                    print(f'NEGATIVE FAIL {folder} {view_id} call {call_id}: {evidence_id} created after the request but listed')
    print(f'shown-evidence check: {positives} judgements checked (cited within listed), {negatives} (judgement, later evidence) pairs checked (not listed), {failures} failures')
    return failures == 0 and positives > 0 and negatives > 0



def expected_shown(run_folder, view_id, day):
    """Built independently of shown_evidence: every judgement row of the view up to the day, its request's user text split into lines,
    and the second token of each line that starts with '- e' followed by digits and ' ['."""
    views = sqlite3.connect(f"file:{Path(run_folder) / 'views.sqlite'}?mode=ro", uri=True)
    archive = sqlite3.connect(f"file:{Path(run_folder) / 'archive.sqlite'}?mode=ro", uri=True)
    ids = set()
    rows = views.execute('select call_id, publication_day from judgements where view_id=?', (view_id,)).fetchall()
    for call_id, published in rows:
        if published > day:
            continue
        text = json.loads(archive.execute('select request_json from model_calls where call_id=?', (call_id,)).fetchone()[0])['messages'][-1]['content']
        for line in text.split('\n'):
            parts = line.split(' ')
            if len(parts) > 2 and parts[0] == '-' and parts[1][:1] == 'e' and parts[1][1:].isdigit() and parts[2].startswith('['):
                ids.add(parts[1])
    return ids


def validate_shown_function(run_folders):
    """Calls shown_evidence itself: equal to the independent set for every view at every judgement day; a cutoff before a view's
    later judgements excludes ids listed only after it; another view's set differs where its requests differ; a missing archive call
    is refused."""
    import shutil, tempfile
    compared = cutoffs = cross = failures = 0
    for folder in run_folders:
        views = sqlite3.connect(f"file:{Path(folder) / 'views.sqlite'}?mode=ro", uri=True)
        days_of = {}
        for view_id, published in views.execute('select view_id, publication_day from judgements order by publication_day'):
            days_of.setdefault(view_id, []).append(published)
        for view_id, days in days_of.items():
            for day in sorted(set(days)):
                got, want = shown_evidence(folder, view_id, day), expected_shown(folder, view_id, day)
                compared += 1
                if got != want:
                    failures += 1
                    print(f'FAIL {folder} {view_id} {day}: function {len(got)} ids, independent {len(want)}')
            if len(set(days)) > 1:
                first, last = sorted(set(days))[0], sorted(set(days))[-1]
                only_late = expected_shown(folder, view_id, last) - expected_shown(folder, view_id, first)
                if only_late:
                    cutoffs += 1
                    if only_late & shown_evidence(folder, view_id, first):
                        failures += 1
                        print(f'CUTOFF FAIL {folder} {view_id}: ids listed only after {first} returned for {first}')
        view_ids = sorted(days_of)
        for a, b in zip(view_ids, view_ids[1:]):
            sa, sb = shown_evidence(folder, a, '2026-07-14'), shown_evidence(folder, b, '2026-07-14')
            if expected_shown(folder, a, '2026-07-14') != expected_shown(folder, b, '2026-07-14'):
                cross += 1
                if sa == sb:
                    failures += 1
                    print(f'CROSS FAIL {folder}: {a} and {b} returned the same set')
    # a missing archive call must be refused
    folder = Path(run_folders[0])
    with tempfile.TemporaryDirectory() as scratch:
        for name in ('views.sqlite', 'archive.sqlite'):
            shutil.copy(folder / name, Path(scratch) / name)
        views = sqlite3.connect(Path(scratch) / 'views.sqlite')
        view_id, call_id = views.execute('select view_id, call_id from judgements order by judgement_id limit 1').fetchone()
        archive = sqlite3.connect(Path(scratch) / 'archive.sqlite')
        archive.execute('delete from model_calls where call_id=?', (call_id,))
        archive.commit(); archive.close(); views.close()
        try:
            shown_evidence(scratch, view_id, '2026-07-14')
            failures += 1
            print('MISSING-CALL FAIL: a judgement whose call is not in the archive was not refused')
            refused = False
        except SystemExit:
            refused = True
    print(f'shown_evidence called: {compared} (view, day) sets equal the independent set check, {cutoffs} cutoff cases, {cross} cross-view '
          f'cases, missing call refused: {refused}; failures {failures}')
    return failures == 0 and compared > 0 and cutoffs > 0 and cross > 0 and refused


if __name__ == '__main__':
    if sys.argv[1:2] == ['validate']:
        sys.exit(0 if validate(sys.argv[2:]) else 1)
    if sys.argv[1:2] == ['validate-shown']:
        sys.exit(0 if (validate_shown(sys.argv[2:]) and validate_shown_function(sys.argv[2:])) else 1)
    raise SystemExit(__doc__)
