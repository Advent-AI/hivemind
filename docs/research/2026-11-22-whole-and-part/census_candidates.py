"""$0 census, step 1: list every stored judgement of a question whose quantity contains other quantities (total revenue, its
growth, Data Center revenue, total CPU revenue) whose implied outcome or reasons name a component (a CPU line, a GPU generation,
networking), for reading by hand. Distinct judgements only: the pilots' non-reader rows copy old-2, so only their fresh reader rows
(call_id above the copied prefix) are listed. Read-only on copies and finished runs.

Usage: python3 census_candidates.py <out.txt>
"""
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRATCH = Path('/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad')
PILOT_TOP = 8737                     # the pilots' archives copy old-2's rows up to this call
STORES = [('old-1', REPO / 'poc/data/comparison-2026-11-17/run/old-1/prod', 0),
          ('old-2', REPO / 'poc/data/comparison-2026-11-17/run/old-2/prod', 0),
          ('old-3', REPO / 'poc/data/comparison-2026-11-17/run/old-3/prod', 0),
          ('control-1', SCRATCH / 'control-1-copy', PILOT_TOP),
          ('linked-1', SCRATCH / 'linked-1-copy', PILOT_TOP)]
WHOLE = re.compile(r'total revenue|data center segment revenue|data-center revenue|total cpu revenue', re.I)
COMPONENT = re.compile(r'\bCPU|stand-?alone|\bVera\b|\bGrace\b|\bRubin\b|networking', re.I)


def main(out_path):
    lines, counts = [], []
    for label, folder, top in STORES:
        conn = sqlite3.connect(f'file:{folder / "views.sqlite"}?mode=ro', uri=True)
        conn.row_factory = sqlite3.Row
        wholes = {r['view_id']: r['question'] for r in conn.execute("select view_id, question from views where object_id='NVDA'")
                  if WHOLE.search(r['question'])}
        rows = conn.execute(f"select * from judgements where view_id in ({','.join('?' * len(wholes))}) and call_id > ? order by seq",
                            (*wholes, top)).fetchall()
        flagged = [r for r in rows if COMPONENT.search((r['implied_outcome'] or '') + ' ' + (r['reasons'] or ''))]
        counts.append((label, len(rows), len(flagged)))
        for r in flagged:
            lines.append(f'### {label} {r["view_id"]} {r["publication_day"]} rung {r["rung"]} call {r["call_id"]} cites_views {r["cited_views_json"]}\n'
                         f'Q: {wholes[r["view_id"]]}\nREF: {r["reference"]}\nIMPLIED: {r["implied_outcome"]}\nREASONS: {r["reasons"]}\n')
    Path(out_path).write_text('\n'.join(lines))
    for label, total, flagged in counts:
        print(f'{label}: {total} distinct judgements of whole questions, {flagged} name a component')


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1].startswith('-'):
        raise SystemExit('usage: census_candidates.py <out.txt>')
    main(sys.argv[1])
