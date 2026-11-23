"""D368's dependency channel on stored, correctly directed cases ($0; D533). In the frozen seeded draws the preset questions carry
"supports" edges, stored as the supporting (driver) question depending on the supported (root) one; D368 decides the reading the other
way: the supported question reads its supporting questions' conclusions. For every stored edge of one draw this script builds the line
the supported question's judge would receive under D368 (the supporting question's current conclusion at the supported question's last
judgement, in the production format: the band and the first 600 characters of the reasons), and compares its figures with the
supported question's own last request. Read-only; nothing is sent; nothing is judged again.

  python3 channel_assessment.py <run folder holding views.sqlite and archive.sqlite>
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

FIGURE = re.compile(r'\$\s?\d[\d,.]*\s?(?:billion|million|trillion|bn|B|M)?|\d[\d,.]*\s?%|\d[\d,.]*\s?(?:billion|million|trillion|GW|gigawatts?|GPUs?|units)', re.I)


def figures_of(text):
    return {re.sub(r'\s+', '', match.group(0)).lower().rstrip('.,') for match in FIGURE.finditer(text or '')}


def main():
    folder = Path(sys.argv[1])
    store = sqlite3.connect(f"file:{folder / 'views.sqlite'}?mode=ro", uri=True)
    archive = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
    question = {row[0]: row[1] for row in store.execute('select view_id, question from views')}
    out = []
    for supporting, supported, direction in store.execute("select d.view_id, coalesce(r.resolved_to, d.depends_on), d.direction from dependencies d left join dependency_resolutions r on r.dependency_id = d.dependency_id where coalesce(r.resolved_to, d.depends_on) != ''"):
        last = store.execute('select seq, publication_day, rung, request_sha256 from judgements where view_id = ? order by seq desc, judgement_id desc limit 1', (supported,)).fetchone()
        if last is None:
            out.append({'supporting': supporting, 'supported': supported, 'status': 'the supported question was never judged'})
            continue
        seq, day, rung, sha = last
        state = store.execute('select seq, rung, reasons from judgements where view_id = ? and seq <= ? order by seq desc, judgement_id desc limit 1', (supporting, seq)).fetchone()
        if state is None:
            out.append({'supporting': supporting, 'supported': supported, 'status': 'the supporting question had no conclusion by then'})
            continue
        label = store.execute('select label from rungs where view_id = ? and position = ?', (supporting, state[1])).fetchone()[0]
        line = f"- {supporting} (open; {direction}) {question[supporting]}: now rung {state[1]} {label}; reasons: {state[2][:600]}"
        request = json.loads(archive.execute('select request_json from model_calls where request_sha256 = ?', (sha,)).fetchone()[0])['messages'][-1]['content']
        carried, known = figures_of(state[2][:600]), figures_of(request)
        out.append({'supporting': supporting, 'supported': supported, 'status': 'built', 'supported_last_judged': day, 'supporting_conclusion_of_article': state[0], 'line': line,
                    'figures_in_the_line': sorted(carried), 'figures_not_in_the_supported_request': sorted(carried - known),
                    'supported_request_already_shows_the_reverse_edge': supporting in re.findall(r'^- (v\d+) \(', request, re.M)})
    built = [row for row in out if row['status'] == 'built']
    print(f"edges: {len(out)}; lines built: {len(built)}; with at least one figure: {sum(1 for r in built if r['figures_in_the_line'])}; "
          f"with a figure the supported question's own last request does not hold: {sum(1 for r in built if r['figures_not_in_the_supported_request'])}")
    for row in out:
        if row['status'] != 'built':
            print(f"  {row['supporting']} -> {row['supported']}: {row['status']}")
            continue
        print(f"  {row['supporting']} supports {row['supported']} [{question[row['supported']][:60]}]: figures in the line {len(row['figures_in_the_line'])}, new to the supported request {row['figures_not_in_the_supported_request'][:6]}")
    (Path(__file__).resolve().parent / f'channel-{folder.name}.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
    example = max(built, key=lambda r: len(r['figures_not_in_the_supported_request']), default=None)
    if example:
        print('\nthe line with the most figures new to its reader, as the judge would receive it:\n ', example['line'][:900])


if __name__ == '__main__':
    main()
