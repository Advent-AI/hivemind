"""The stored judgements of the three unseeded replays, as the Stage B reading form describes a judgement ($0, read-only).

A judgement is given with the request as sent (the user message of the call whose answer was accepted), the answer as stored,
and `not_shown`: the evidence linked to the question by that judgement and not replaced by then, which the request did not
list. The replays are finished runs; their databases are opened read-only.
"""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind.views import judging  # noqa: E402

DRAWS = {'d1': ROOT / 'poc/data/clean-unseeded-2026-11-10/draw-d1/judged',
         'd2': ROOT / 'poc/data/clean-unseeded-2026-11-10/draw-d2/judged',
         'd3': ROOT / 'poc/data/clean-unseeded-2026-11-10/draw-d3/judged'}


def read_only(path):
    connection = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def user_text_of(request):
    """The user message of a stored request, whichever of the two request shapes it has."""
    return request['messages'][-1]['content'] if 'messages' in request else request['input'][-1]['content']


def shape_of(rungs):
    if len(rungs) == 2:
        return 'yes/no'
    return 'figure' if any(rung['lo'] is not None or rung['hi'] is not None for rung in rungs) else 'state'


def not_shown_of(library, view_id, judgement_seq, shown_ids):
    """Evidence linked to the view at or before the judgement's sequence number, not replaced by then, and not listed in the
    request."""
    replaced = {row['old_evidence_id'] for row in library.execute('select old_evidence_id from replacements where seq <= ?', (judgement_seq,))}
    out, seen = [], set()
    for link in library.execute('select evidence_id, seq from evidence_links where view_id = ? and seq <= ? order by id', (view_id, judgement_seq)):
        evidence_id = link['evidence_id']
        if evidence_id in shown_ids or evidence_id in replaced or evidence_id in seen:
            continue
        seen.add(evidence_id)
        record = library.execute('select one_line, quote, speaker, original_who, original_day, tier from evidence where evidence_id = ?', (evidence_id,)).fetchone()
        source = library.execute('select publication_day, category from evidence_sources where evidence_id = ? order by id limit 1', (evidence_id,)).fetchone()
        revised = library.execute('select old_evidence_id from revisions where new_evidence_id = ? and seq <= ?', (evidence_id, judgement_seq)).fetchone()
        revised_line = library.execute('select one_line from evidence where evidence_id = ?', (revised['old_evidence_id'],)).fetchone() if revised else None
        out.append({'evidence_id': evidence_id, 'published': source['publication_day'] if source else None, 'tier': record['tier'], 'speaker': record['speaker'],
                    'one_line': record['one_line'], 'quote': record['quote'],
                    'revises': {'evidence_id': revised['old_evidence_id'], 'one_line': revised_line['one_line'] if revised_line else None} if revised else None})
    return out


STAGE_B = ROOT / 'poc/data/clean-stage-b-2026-11-11'


def stage_b_folders():
    """{draw: folder} of Stage B's completed draws, from its run record: the folder of the attempt that completed."""
    record = json.loads((STAGE_B / 'run.json').read_text())
    folders = {}
    for draw in ('u1', 'u2', 'u3'):
        entry = record.get(draw, {})
        if entry.get('state') != 'complete':
            raise SystemExit(f'Stage B draw {draw} is not complete: {entry.get("state")}')
        folders[draw] = STAGE_B / next(attempt['folder'] for attempt in entry['attempts'] if 'judgements' in attempt)
    return folders


def views_of(draw, folder=None):
    """[{draw, view, question, shape, rungs, judgements: [...]}] of one draw, the judgements in the order they were made. `folder`
    is a run folder holding views.sqlite and archive.sqlite; by default the baseline's unseeded replay of that draw."""
    folder = Path(folder) if folder is not None else DRAWS[draw]
    library, archive = read_only(folder / 'views.sqlite'), read_only(folder / 'archive.sqlite')
    out = []
    for view_row in library.execute('select distinct view_id from judgements order by cast(substr(view_id, 2) as integer)'):
        view_id = view_row['view_id']
        view = library.execute('select * from views where view_id = ?', (view_id,)).fetchone()
        rungs = [dict(row) for row in library.execute('select position, label, condition, lo, hi from rungs where view_id = ? order by position', (view_id,))]
        labels = {rung['position']: rung['label'] for rung in rungs}
        judgements = []
        for row in library.execute('select * from judgements where view_id = ? order by judgement_id', (view_id,)):
            request = json.loads(archive.execute('select request_json from model_calls where call_id = ?', (row['call_id'],)).fetchone()[0])
            request_text = user_text_of(request)
            judgements.append({'judgement_id': row['judgement_id'], 'seq': row['seq'], 'day': row['publication_day'], 'request_as_sent': request_text,
                               'answer': {'rung': row['rung'], 'rung_label': labels[row['rung']], 'reference': row['reference'], 'implied_outcome': row['implied_outcome'],
                                          'reasons': row['reasons'], 'changed': bool(row['changed']), 'why_changed': row['why_changed']},
                               'not_shown': not_shown_of(library, view_id, row['seq'], judging.evidence_shown_in(request_text))})
        out.append({'draw': draw, 'view': view_id, 'question': view['question'], 'object': view['object_id'], 'kind': view['kind'], 'due_day': view['due_day'],
                    'shape': shape_of(rungs), 'rungs': rungs, 'judgements': judgements})
    return out


def main():
    total = 0
    for draw in DRAWS:
        for view in views_of(draw):
            judgements = view['judgements']
            total += len(judgements)
            sizes = [len(judgement['request_as_sent']) for judgement in judgements]
            path = [judgement['answer']['rung'] for judgement in judgements]
            print(f"{draw} {view['view']:4s} {view['shape']:6s} {len(judgements):2d} judgements | rungs chosen {path} | request chars {min(sizes)}–{max(sizes)} | "
                  f"not shown {[len(judgement['not_shown']) for judgement in judgements]} | {view['question'][:90]}")
    print('judgements:', total)


if __name__ == '__main__':
    main()


def split_rows_present(conn):
    """Whether a store holds the period split's yearly rows (splitting/DESIGN.md v4 §0c): the frozen Stage B accounting and research
    readers refuse such a store by name. A historical store without the `period` column holds none."""
    columns = {row[1] for row in conn.execute('pragma table_info(clean_ladders)')}
    return 'period' in columns and conn.execute("select 1 from clean_ladders where period != '' limit 1").fetchone() is not None


def refuse_split_store(conn, reader):
    if split_rows_present(conn):
        raise SystemExit(f'{reader}: this store holds period-split rows (splitting/DESIGN.md v4); the frozen Stage B accounting does not '
                         'map them, so this reader refuses it')
